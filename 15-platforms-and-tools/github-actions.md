---
title: GitHub Actions
category: platforms
status: complete
difficulty: beginner
prerequisites:
  - CI/CD Pipelines (generic)
related:
  - Jenkins Pipelines (sister implementation)
  - Artifact Management
---

<!-- icon: github -->
# GitHub Actions

> GitHub Actions is GitHub's CI/CD implementation: **workflows** (YAML in `.github/workflows/`) run **jobs** of **steps** on **runners** — the generic pipeline concept, hosted where your code already lives.

## 1. Concept → Actions Map

Picking up from **[Jenkins Troubleshooting](jenkins/jenkins-troubleshooting.md)**, where the self-hosted domain concluded — here is the same CI/CD loop with zero infrastructure: every generic concept mapped to its Actions equivalent.

| Generic Concept | GitHub Actions |
|---|---|
| Pipeline | Workflow (`.yml` file) |
| Stage | Job (or a group of jobs) |
| Job | `jobs.<id>` — runs on one runner, parallel by default, `needs:` for sequencing |
| Step | `run:` command or `uses:` action |
| Runner | GitHub-hosted (`ubuntu-latest`) or self-hosted |
| CI Trigger | `on:` (push, pull_request, schedule, workflow_dispatch) |
| Secrets | `secrets.*` + Environments protection rules |
| Artifact | `actions/upload-artifact`, packages via GHCR |

## 2. Why It Exists

Zero infrastructure: the repo, the pipeline, the secrets, and the PR checks live in one place. A workflow file in the repo *is* the pipeline — reviewed, versioned, and enforced as branch protection like any code.

## 3. Canonical Workflow (CI: Build → Test → Scan)

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
    permissions:
      contents: read
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - run: npm audit --audit-level=high
```

## 4. CD: Staging Auto, Production Gated

```yaml
deploy-staging:
  needs: [test, scan]
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  environment: staging          # auto-deploy
  steps:
    - run: ./deploy.sh staging

deploy-production:
  needs: deploy-staging
  runs-on: ubuntu-latest
  environment: production       # required reviewers = approval gate
  steps:
    - run: ./deploy.sh production
```

`environment: production` + required reviewers reproduces the Delivery approval gate from [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md).

## 5. Core Mechanics

- **Triggers (`on:`):** `push`, `pull_request`, `schedule` (cron), `workflow_dispatch` (manual), `release` (tags). PR triggers + required status checks = the merge gate.
- **Marketplace actions:** reusable steps (`actions/checkout`, `docker/build-push-action`). Pin to full SHAs for supply-chain safety, not floating `@v4` tags, in security-sensitive repos.
- **Secrets:** repo/org/environment levels; `GITHUB_TOKEN` is auto-issued per run (least-privilege via `permissions:`). Never `echo` secrets — masking is automatic but layer-baking still leaks.
- **Caching:** `cache:` on setup actions (npm, pip, gradle) + `actions/cache` for custom paths — the biggest free speedup.
- **Artifacts vs images:** `upload-artifact` for PR-scoped files (reports, bundles); registry push (GHCR = GitHub Container Registry, or any OCI registry) for promotable release images.

<!-- icon: server -->
### Runners

| Type | Who manages | Best for |
|------|-------------|----------|
| GitHub-hosted (`ubuntu/windows/macos-latest`) | GitHub, fresh VM per job | Default — zero maintenance, clean env every run |
| Self-hosted (VM/bare metal) | You (persistent agent process) | Special hardware, GPUs, private network, license-locked tools |
| ARC scale sets (K8s) | You via Actions Runner Controller | Elastic ephemeral runners on your cluster |

- **Labels select runners:** `runs-on: ubuntu-latest` or `runs-on: [self-hosted, linux, gpu]`. A job waits in queue until a matching idle runner appears — wrong labels = stuck queue.
- **Ephemeral beats persistent:** hosted runners die after each job (no drift); mirror that with ARC or just-in-time self-hosted runners.
- **Trust boundary:** never run untrusted fork PRs on persistent self-hosted runners — a malicious workflow gets a shell on your machine with your secrets. Forks get hosted runners or credential-free sandboxes.
- **Sizing:** one job per runner by default (no executor math like Jenkins); scale = more runners, controlled via concurrency groups and ARC min/max.

### ARC Scale Set (Self-Hosted That Scales)

```yaml
# arc-runner-set: ephemeral runners on your cluster, zero idle cost
apiVersion: actions.github.com/v1alpha1
kind: AutoscalingRunnerSet
metadata: { name: acme-runners }
spec:
  githubConfigUrl: https://github.com/acme/org
  minRunners: 0
  maxRunners: 20
  template:
    spec:
      containers:
        - name: runner
          image: ghcr.io/actions/actions-runner:latest
```

Scale-to-zero when idle, burst to `maxRunners` on PR storms. Runner pods are ephemeral (no drift); cache via remote backends, not pod disks. Use when hosted minutes cost more than cluster ops — heavy Linux matrices, private-network builds.

### Cost (rates as of 2026, verify in GitHub billing docs)

- **Public repos + self-hosted runners:** free (self-hosted draws no per-minute charge; a small platform charge regime was announced for 2026 — confirm current rules before budgeting).
- **Private repos:** monthly free pool — Free 2,000 min, Pro/Team 3,000 min, Enterprise 50,000 min. Beyond quota, per-minute: Linux 2-core ~$0.006, Windows ~$0.010, macOS ~$0.062. A macOS minute costs ~10× a Linux minute.
- **Larger runners** bill from the first minute (free pool doesn't apply) and need a payment method on file.
- **Cost killers:** macOS builds, uncached deps, sprawling matrices, failed jobs (billed like green ones), minutes rounded up per job. Cap with `timeout-minutes`, concurrency groups, and cached Linux jobs.

### Pipeline Patterns

```yaml
# Reusable pipeline: defined once, called from many repos
# .github/workflows/reusable-ci.yml
on:
  workflow_call:
    inputs:
      node-version: { required: true, type: string }
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: ${{ inputs.node-version }}, cache: npm }
      - run: npm ci && npm run build && npm test
```

```yaml
# Caller + matrix + concurrency + path filter
on:
  pull_request:
    paths: ['src/**', 'package.json']   # skip CI for docs-only PRs
concurrency:
  group: ci-${{ github.ref }}           # auto-cancel stale runs on push
  cancel-in-progress: true
jobs:
  ci:
    strategy:
      matrix: { node: [18, 20, 22] }    # 3 parallel jobs, one per version
    uses: ./.github/workflows/reusable-ci.yml
    with: { node-version: ${{ matrix.node }} }
```

- **Reusable (`workflow_call`):** one canonical pipeline, N repos call it — fixes copy-paste drift.
- **Matrix:** fan-out across versions/OSes in one block; keep matrices small or minutes explode.
- **Concurrency:** same-branch pushes cancel stale runs — stops queue pileups and wasted minutes.
- **Path filters:** docs-only changes skip the pipeline entirely.

<!-- icon: terminal -->
### Setup: First Green Build

GitHub Actions (minutes, no server):

1. In your repo, create `.github/workflows/ci.yml` (use the §3 workflow).
2. Commit + push → **Actions tab** shows the run live; green check appears on the commit.
3. Enforce it: *Settings → Branches → Add rule → Require status checks* → select `ci`. PRs now can't merge red.

Jenkins (see [setup](jenkins/jenkins-setup.md) + [pipelines](jenkins/jenkins-pipelines.md)):

1. Run the controller (Docker), set executors to 0, connect a labeled agent.
2. Commit a `Jenkinsfile` to the repo; create a Multibranch Pipeline job pointing at it.
3. Add the GitHub webhook so pushes trigger builds; protect `main` with the Jenkins status check.

Same shape both times — trigger → build/test/scan → gate → merge — only the machinery differs.

## 6. Without It (or Without Any CI Runner)

Same failure as manual CI: merges unverified, releases from laptops, secrets in chat history, no required checks — GitHub Actions just happens to be the shortest path from "repo on GitHub" to "every PR verified."

## 7. Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Minutes quota burned | `macos` runners, no caching, matrix sprawl | `ubuntu`, cache, trim matrix |
| Flaky "works locally" | Unpinned actions/deps | Pin SHAs + lockfiles |
| Secret leaked in logs | Echoed or baked into image | Rotate immediately; use `permissions:` + env-scoped secrets |
| Slow PR feedback | Everything serial, E2E in PR | Parallel jobs; E2E to post-merge/staging |
| Fork PRs fail on secrets | Secrets withheld from forks by design | `pull_request_target` carefully, or label-gated workflows |

## 8. Best Practices

- Fast PR workflow (< 10 min); heavy suites post-merge.
- `permissions:` minimal on every job; environment protection rules on production.
- Reusable workflows (`.github/workflows/reusable-*.yml` + `workflow_call`) instead of copy-pasted YAML across repos.
- Same artifact digest staging → production; never rebuild per environment.

## 9. GitHub Actions vs Jenkins

| | GitHub Actions | Jenkins |
|---|---|---|
| Model | Hosted SaaS (+ optional self-hosted) | Self-hosted server you operate |
| Pipeline language | YAML workflows in `.github/workflows/` | Groovy Jenkinsfile (Declarative/Scripted) |
| Runners | Fresh VM per job; `runs-on:` labels | Persistent/ephemeral agents; executors + labels |
| Secrets | `secrets.*`, environments, auto `GITHUB_TOKEN` | Credentials store + `withCredentials` bindings |
| Extensibility | Marketplace actions | 1,800+ plugins |
| PR gates | Status checks + required checks natively | Multibranch + webhooks you wire up |
| Cost | Free pool (2–3k min/mo private; public free), then per-minute meter | Free license; you pay servers + your maintenance labor |
| Best when | Code on GitHub, want zero infra | Air-gapped/special HW, full control, no per-minute billing |

One line: Actions trades control for convenience; Jenkins trades convenience for control.

## 10. Interview Notes

- Workflow → job → step → runner, precisely.
- `needs:` vs parallel; `environments` as approval gates; `GITHUB_TOKEN` permissions model.
- GitHub Actions vs Jenkins in one line: hosted, YAML, repo-local vs self-hosted, Groovy, controller/agents.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md) (generic — read first)
- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Jenkins Domain](jenkins/README.md) (sister implementation)

Both implementations behind you — Jenkins self-hosted, Actions hosted — the full arc from commit to production is now yours. Return to the **[Topic Index](../TOPIC_INDEX.md)** for planned chapters (deployment strategies, labs), or start building.
