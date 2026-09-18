---
title: Pipelines Build Test
status: complete
merged_from:
  - 06-ci-cd-pipelines/pipelines.md
  - 03-build-systems/build-systems.md
  - 04-testing/testing-strategy.md
---

# Pipelines Build Test

> Merged handbook. Sources: 06-ci-cd-pipelines/pipelines.md, 03-build-systems/build-systems.md, 04-testing/testing-strategy.md.


---

<!-- merged-part-1-from: 06-ci-cd-pipelines/pipelines.md -->

<!-- icon: pipeline -->
## Part 1: CI/CD Pipelines

> A pipeline is the automated workflow from trigger to deployment — stages (phases) contain jobs (units of work) contain steps (operations), executed by runners.

## 1. What Is It?

Picking up from **[Git, Branching & Pull Requests](../01-source-control/git-branching-pull-requests.md)**, where a merge fires the trigger — we now examine the pipeline that the trigger starts.

| Term | Meaning | Example |
|------|---------|---------|
| Pipeline | Whole automated workflow | `.github/workflows/ci.yml` |
| Stage | Logical phase | build → test → scan |
| Job | Unit of work (often parallel) | `unit-tests`, `docker-build` |
| Step | Single operation in a job | `npm ci`, `npm test` |
| Runner / Agent | Machine executing jobs | GitHub-hosted `ubuntu-latest`, self-hosted agent |

## 2. Why Does It Exist?

Manual build → test → scan → package is slow and inconsistent. A pipeline makes verification **automatic, repeatable, and fast** on every change.

## 3. Where Does It Fit?

```mermaid
flowchart LR
    T[CI Trigger] --> B[Build]
    B --> TE[Test]
    TE --> S[Security Scan]
    S --> A[Artifact → Registry]
    A --> D[CD]
```

## 4. How It Works

1. Trigger fires (PR, push, schedule).
2. Runner checks out code, sets up toolchain (with dependency cache).
3. **Build** compiles/bundles; **Test** runs unit/integration suites; **Security Scan** checks deps/secrets/config.
4. Fail-fast or continue-on-error per policy; results + logs return as feedback.
5. On success of all required jobs, the artifact job packages and pushes.

## 5. Example (GitHub Actions)

```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test -- --coverage

  scan:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
      # - uses: gitleaks/gitleaks-action@v2  # secret scan
```

<!-- icon: build -->
<!-- icon: testing -->
<!-- icon: security -->
## 6. The Three Verification Stages

- **Build:** `npm ci → npm run build`, `docker build`. Must be hermetic — sealed from the ambient machine: pinned dependencies, clean environment, no hidden host tools — so the same commit builds byte-identically anywhere. Failure = code doesn't compile/bundle.
- **Test:** unit (fast, per-PR) → integration (services) → E2E/smoke (staging). Keep PR suites < 10 min; move slow suites to post-merge.
- **Security Scan:** dependency audit (`npm audit`), secret scan (gitleaks), SAST/image scan (Trivy). Run on every PR — shifting left is cheaper than incident response.

Now that you understand what can fail, the next question is where successful builds go — which is exactly what **[Artifact Management](../05-artifacts-and-packaging/artifact-management.md)** covers: the versioned output that survives the pipeline.

<!-- icon: docker -->
### Building Images Without a Docker Daemon: BuildKit & Kaniko

Socket mounts and DinD both hand builds daemon power. Two tools shrink or remove that privilege:

**BuildKit** (the modern `docker build` engine):

- **WHAT:** the builder behind `docker buildx` — parallel stage execution, content-addressed caching, secret/SSH/cache mounts.
- **WHY:** classic builds re-download dependencies every run and leak secrets into layers; BuildKit makes builds fast (shared cache) and safe (mounts never persist).
- **HOW:** point the CLI at a builder (local daemon or remote `BUILDKIT_HOST`), declare mounts in the Dockerfile, push with registry cache refs.

```bash
## Part 1: BuildKit via buildx: parallel stages, layer + inline caching, secret mounts
docker buildx build --push \
  --cache-to type=registry,ref=registry/app:cache \
  --cache-from type=registry,ref=registry/app:cache \
  --secret id=REG_PWD,env=REG_PWD \
  -t registry/app:$GIT_COMMIT .
```

```dockerfile
## Part 1: Cache mounts: dependencies survive rebuilds without bloating layers
RUN --mount=type=cache,target=/root/.npm npm ci
RUN --mount=type=secret,id=REG_PWD npm publish
```

**Kaniko** (daemonless, for Kubernetes agents that forbid sockets and privileged mode):

- **WHAT:** a container image (`gcr.io/kaniko/executor`) that builds Docker images from a Dockerfile entirely in userspace — no daemon, no privileged flag.
- **WHY:** hardened clusters ban socket mounts (host root) and DinD (privileged); Kaniko is the only compliant way to build images there.
- **HOW:** run the executor container with the build context mounted, pass `--destination` for the registry target; it snapshots each Dockerfile instruction into layers itself. (Jenkins calling convention: see [Jenkins Pipelines](../15-platforms-and-tools/jenkins/jenkins-pipelines.md#kaniko-on-kubernetes-agents).)

| | BuildKit (`buildx`) | Kaniko |
|---|---|---|
| Needs daemon | Yes (local or remote `BUILDKIT_HOST`) | No — unprivileged userspace build |
| Best in | Jenkins Docker agents, dev machines, GHA runners | Locked-down K8s (no socket, no `--privileged`) |
| Caching | Registry + local + GitHub Actions cache backends | Registry cache (`--cache=true --cache-repo=...`) |
| Secrets | `--secret` mounts (never in layers) | Build args only — prefer short-lived tokens |

Rule: default to BuildKit everywhere a daemon exists; reach for Kaniko exactly where daemons are banned (hardened clusters, shared multitenant agents).

## 7. Execution: Dependencies & Parallelism

- `needs: build` = sequential gate; independent jobs (`test`, `scan`) run in parallel.
- Fail-fast default; use `continue-on-error` only for advisory (non-blocking) checks.
- Cache dependencies (`cache: npm`, Docker layer cache) — biggest free speedup.

### Runners Deep Dive

| | Managed (GitHub-hosted, Jenkins Docker cloud) | Self-hosted (VM, bare metal, ARC) |
|---|---|---|
| You manage | Nothing — fresh env per job | OS, patches, scaling, idle cost |
| Best for | Standard builds, burst capacity | GPUs, private nets, licenses, exotic OS |
| Caches | Cold each run (use registry/remote cache) | Warm local cache (fast, but drift risk) |

Cache layers, fastest first: dependency cache (`~/.npm`, `~/.m2`) → build-tool remote cache (BuildKit registry cache, Gradle remote) → artifact reuse (skip rebuild when inputs unchanged). Cache key must include lockfiles; stale keys cause "works in CI, fails locally" in reverse.

### Parallelism, Dependencies & Failure Handling

- **DAG, not sequence:** express `needs:` truthfully; independent jobs fan out, gates fan in. A linear pipeline is usually an unoptimized one.
- **Matrices** multiply one definition across versions/OSes — cap axes (3×3=9 jobs burns quota and attention).
- **Fail-fast** (default) stops the run at first red; use for PR signal. **Advisory** (`continue-on-error`) for experimental checks that must not block merges.
- **Retry** only idempotent steps (network fetches), never deployments. **Quarantine** flaky tests to a non-blocking suite with an owner and a deadline — a flaky gate trains developers to ignore red.

## 8. Failure Modes & Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Flaky tests | Shared state, time deps | Quarantine, fix or delete flaky test |
| Slow pipeline | No cache, huge matrices | Cache, split jobs, parallelize |
| "Works locally" | Unpinned deps, dirty env | Lockfiles, containerized runners |
| Red main | Post-merge suite not required | Require it; revert-or-fix-forward policy |

## 9. Best Practices

- Fast PR pipeline (< 10 min), thorough post-merge pipeline.
- Pin action/tool versions (`@v4`, exact image tags).
- Never bake secrets into logs/images; use masked CI secrets.
- Same steps locally and in CI (`npm ci && npm test`) to kill env drift.

## 10. Common Misconceptions

- "More stages = more safety." Each stage must earn its minutes; slow pipelines get bypassed.
- "Green pipeline = correct software." It means *checked* software — coverage gaps still ship bugs.

## 11. Real-World Scenario

Team's PR suite takes 35 min → developers stack PRs without waiting → `main` breaks weekly. Fix: cache deps, parallelize test/scan, move E2E to staging; PR time drops to 7 min, `main` stays green.

## 12. Interview / Exam Notes

- Define pipeline → stage → job → step → runner precisely.
- Explain fail-fast vs advisory checks, sequential vs parallel jobs.
- What belongs in PR pipeline vs post-merge vs staging gates.

This pipeline produces one thing that outlives it — the artifact. Continue in **[Artifact Management](../05-artifacts-and-packaging/artifact-management.md)**.

## Related Topics

- [Git, Branching & Pull Requests](../01-source-control/git-branching-pull-requests.md)
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)


---

<!-- merged-part-2-from: 03-build-systems/build-systems.md -->

<!-- icon: build -->
## Part 2: Build Systems

> A build system turns source into runnable output deterministically: dependency resolution, compilation, bundling — the same inputs must always produce the same outputs.

## 1. What Is It?

Picking up from **[CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)**, where the build stage was defined — here is what actually runs inside it: Maven/Gradle (JVM), npm (JS), Go modules, Cargo — each resolving declared dependencies into a compiled/bundled artifact.

## 2. Hermetic Builds

Hermetic = sealed from the ambient machine (see glossary). Concretely: pinned dependency versions (lockfiles: `package-lock.json`, `pom.xml` versions, `go.sum`), clean container per build, no `latest` tags, no host-installed toolchains. Violation symptom: "works in CI, fails locally" in reverse — the build drank something from its environment.

## 3. Caching Done Right

Cache layers, fastest first: dependency cache keyed on lockfiles → remote build cache (Gradle remote, BuildKit registry cache) → artifact reuse (skip rebuild when inputs unchanged). Golden rule: the cache key must include every input; a stale key ships stale code silently.

## 4. Tool Notes

- **Maven/Gradle:** standard layouts, wrapper scripts (`mvnw`, `gradlew`) pin the toolchain itself — commit them.
- **npm:** `npm ci` (lockfile-exact) in CI, never `npm install`; cache `~/.npm`.
- **Docker builds:** BuildKit with `--secret` mounts and registry cache (see [pipelines BuildKit section](../06-ci-cd-pipelines/pipelines.md)); multi-stage so SDKs never ship in runtime images.

## 5. Failure Modes

- Unpinned deps → "it built yesterday"; fix with lockfiles + dependabot-style updates as PRs.
- Bloated images (SDK in prod) → slow pulls, huge attack surface; fix with multi-stage builds.
- Cache poisoning (stale key) → phantom green; fix by keying on lockfiles + periodic cache-bust verification.

## 6. Interview Notes

- Hermetic vs reproducible: sealed environment vs byte-identical output (reproducible is stricter).
- Why `npm ci` over `npm install` in CI.
- Multi-stage Docker: what ships vs what builds.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Continuous Integration](../02-continuous-integration/continuous-integration.md)

Deterministic builds produce trustworthy artifacts. Continue in **[Artifact Management](../05-artifacts-and-packaging/artifact-management.md)**.


---

<!-- merged-part-3-from: 04-testing/testing-strategy.md -->

<!-- icon: testing -->
## Part 3: Testing Strategy

> Testing strategy decides *which tests run where*: fast unit tests gate every PR, slow E2E proves staging — the pyramid keeps feedback fast without losing coverage.

## 1. What Is It?

Picking up from **[Build Systems](../03-build-systems/build-systems.md)**, where output became deterministic — now prove it's correct, at the right stage, at the right cost.

## 2. The Pyramid in Pipelines

| Layer | Speed | Runs in | Guards |
|-------|-------|---------|--------|
| Unit | ms each, minutes total | Every PR | Logic correctness |
| Contract | seconds | Every PR (provider + consumer) | API compatibility between services |
| Integration | minutes | Post-merge / staging | Wiring, DBs, queues |
| E2E / smoke | minutes–tens of minutes | Staging, post-deploy | Real user journeys |

Many unit, fewer E2E: an inverted pyramid (all Selenium, no units) is slow, flaky, and tells you nothing a unit test couldn't in milliseconds.

Test doubles, cheapest first: stub (canned answers) → fake (working shortcut, e.g. in-memory store) → mock (verifies interactions). Mock roles and boundaries, never implementation trivia — over-mocked suites shatter on every refactor while missing real regressions.

## 3. Placement Rules

- PR pipeline: unit + contract + fast integration (< 10 min total). Anything slower moves post-merge.
- Staging: full integration + E2E + smoke after deploy; failures block promotion, not merges.
- Post-deploy: synthetic smoke probes continuously — the pipeline's last test never ends.
- Acceptance criteria as executable specs: analyst + tester + developer agree the criteria before coding, written so the pipeline can run them (Given-When-Then). Docs that can't fail the build drift from behavior.

## 4. Flaky Policy

Flaky test protocol: quarantine to a non-blocking suite immediately (same day), assign an owner, fix-or-delete deadline of one sprint. A flaky gate teaches developers that red is meaningless — the most expensive test debt there is.

## 5. Capacity & Performance Placement

Functional tests prove correctness; capacity tests prove survival. Treat performance as a requirement with a number, not a wish:

- Quantify first: convert expected load into thresholds (p99 latency, sustained throughput, concurrent users) — unquantified goals justify unbounded effort.
- Placement: short performance smoke sentinels in the PR pipeline; full load scenarios post-merge/staging on isolated, production-like hosts (shared or noisy hosts produce phantom regressions).
- Derive load from reality: adapt acceptance flows into composable load scenarios; warm up caches/JIT before measuring.
- Ratchet thresholds: start at minimum viable target, raise as headroom proves stable; investigate before lowering.
- Vocabulary: latency (one transaction's time) vs throughput (transactions per interval) vs capacity (max sustainable throughput within latency budget).

## 6. Failure Modes

- Testing pyramid inverted → 40-minute PR suites developers ignore; rebalance toward units.
- E2E in PR → queue pileups; move to staging.
- No contract tests in microservices → integration surprises at deploy; add consumer-driven contracts.
- Coverage % as a target → gaming (assert-free tests); treat coverage as smoke signal, not goal.

## 7. Interview Notes

- Why contract tests exist (microservice API drift).
- Flaky quarantine protocol, step by step.
- What runs in PR vs staging vs post-deploy, and why.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Build Systems](../03-build-systems/build-systems.md)
- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)

Proven correct — now ship it releasably. Continue in **[Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)**.
