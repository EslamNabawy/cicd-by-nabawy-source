---
title: Core Labs Handbook
status: complete
merged_from:
  - 16-labs/01-first-pipeline.md
  - 16-labs/02-build-and-test.md
  - 16-labs/03-artifacts.md
  - 16-labs/04-deployment.md
  - 16-labs/05-rollback.md
  - 16-labs/06-jenkins-controller.md
  - 16-labs/07-jenkins-shared-library.md
  - 16-labs/08-jenkins-backup-restore.md
---

# Core Labs Handbook

> Merged handbook. Sources: 16-labs/01-first-pipeline.md, 16-labs/02-build-and-test.md, 16-labs/03-artifacts.md, 16-labs/04-deployment.md, 16-labs/05-rollback.md, 16-labs/06-jenkins-controller.md, 16-labs/07-jenkins-shared-library.md, 16-labs/08-jenkins-backup-restore.md.


---

<!-- merged-part-1-from: 16-labs/01-first-pipeline.md -->

<!-- icon: pipeline -->
## Part 1: Lab 01 — First Pipeline

## Objective

Ship a green CI pipeline on GitHub Actions: push → build → test → status check on the PR.

## Prerequisites

- A GitHub repo you own; Node 20+ locally (any tiny JS project works, even `package.json` + one test file).
- Concepts: [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md), [GitHub Actions](../15-platforms-and-tools/github-actions.md).

## Architecture

Push → GitHub webhook → hosted runner (`ubuntu-latest`) → checkout → setup-node → `npm ci` → `npm test` → green check on PR.

## Setup

Repo with `package.json` containing a `test` script (even `"test": "node --test"`).

## Step 1 — Add the workflow

### Execute

Create `.github/workflows/ci.yml`:

```yaml
name: ci
on:
  push:
  pull_request:
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test
```

Push to a branch, open a PR.

### Expected Result

Actions tab shows the run green; the PR shows a green check.

### Why

This is the smallest closed loop: trigger → runner → job → feedback on the PR (see [pipeline anatomy](../06-ci-cd-pipelines/pipelines.md)).

## Step 2 — Require the check

### Execute

Repo Settings → Branches → protect `main` → require `build` status check. Push a breaking change to a PR.

### Expected Result

Merge button blocked until green.

### Why

An unenforced gate is decoration; branch protection makes CI a rule (see [PR gates](../02-continuous-integration/continuous-integration.md)).

## Verification

- [ ] PR shows green check from the workflow.
- [ ] Merging to `main` without green is blocked.
- [ ] Breaking the test turns the PR red.

## Failure Scenarios

- `npm ci` fails: lockfile missing or out of sync — run `npm install` locally, commit the lockfile.
- Runner queues long: free-tier concurrency; retry, or shrink the job.

## Cleanup

Keep the workflow — every later lab extends it.

## What This Proved

Triggers fire pipelines, runners execute jobs, checks gate merges. Continue with [Lab 02](02-build-and-test.md).

## Interview Notes

- What the green check actually proves — and which misconfiguration lets red code merge anyway.
- Why breaking the test on purpose is the real verification, not the green run.


---

<!-- merged-part-2-from: 16-labs/02-build-and-test.md -->

<!-- icon: build -->
## Part 2: Lab 02 — Build and Test

## Objective

Split Lab 01's single job into a fast, cached PR pipeline: hermetic build job → unit test job, total under 10 minutes.

## Prerequisites

- Lab 01 green; concepts: [Build Systems](../03-build-systems/build-systems.md), [Testing Strategy](../04-testing/testing-strategy.md).

## Architecture

PR → job `build` (`npm ci`, cache on lockfile) → job `test` (`needs: build`, unit suite) → combined status check.

## Setup

Add a second test file so the suite has something real to run.

## Step 1 — Split and cache

### Execute

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test
```

### Expected Result

Two jobs, `test` waits for `build`; reruns are faster (warm npm cache).

### Why

`needs:` is the DAG edge; cache keyed on the lockfile is the hermetic speedup (see [pipelines DAG](../06-ci-cd-pipelines/pipelines.md)).

## Step 2 — Prove hermeticity

### Execute

Delete `node_modules` locally, run `npm ci && npm test` — same result as CI.

### Expected Result

Identical pass/fail locally and on the runner.

### Why

Lockfile-exact install means the runner builds what you built — no ambient-machine surprises.

## Verification

- [ ] Two jobs visible, ordered by `needs`.
- [ ] Cache hit shown on rerun.
- [ ] Local `npm ci` reproduces CI result.

## Failure Scenarios

- Cache never hits: lockfile not committed or key inputs changed — verify `package-lock.json` is tracked.
- `test` runs before `build` finishes: missing `needs:` — add the edge.

## Cleanup

Keep; Lab 03 packages this build's output.

## What This Proved

DAG ordering, hermetic installs, lockfile caching. Continue with [Lab 03](03-artifacts.md).

## Interview Notes

- What `needs:` actually guarantees — and the failure you get when the edge is missing.
- Why the cache key includes the lockfile, and what "cache never hits" tells you about the repo.


---

<!-- merged-part-3-from: 16-labs/03-artifacts.md -->

<!-- icon: artifact -->
## Part 3: Lab 03 — Artifacts

## Objective

Build a Docker image once, tag it by commit SHA, push to GHCR, attach an SBOM — then prove staging and prod would run the same digest.

## Prerequisites

- Lab 02 green; a `Dockerfile` (multi-stage, `node:20-slim` runtime); concepts: [Artifact Management](../05-artifacts-and-packaging/artifact-management.md).

## Architecture

Merge to `main` → build image → tag `ghcr.io/<you>/<app>:sha-<short>` → push GHCR → generate SBOM → print digest (the deployable identity).

## Setup

Enable GitHub Packages (GHCR) on the repo; workflow needs `packages: write` permission.

## Step 1 — Build once, tag SHA

### Execute

```yaml
jobs:
  image:
    runs-on: ubuntu-latest
    permissions: { packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=sha,prefix=sha-
      - uses: docker/build-push-action@v6
        with: { push: true, tags: ${{ steps.meta.outputs.tags }} }
```

### Expected Result

GHCR shows `sha-<short>` tag; logs print the digest.

### Why

SHA tag = immutable identity; the digest (not `:latest`) is what every environment deploys (see [versioning](../05-artifacts-and-packaging/artifact-management.md)).

## Step 2 — Attach SBOM

### Execute

Add after push: `anchore/sbom-action@v0` on the pushed image; inspect the artifact.

### Expected Result

SBOM artifact lists every package inside the image.

### Why

The ingredient list that makes the next CVE answerable in minutes, not days.

## Verification

- [ ] GHCR holds an immutable SHA tag.
- [ ] Same digest referenced twice = same bytes.
- [ ] SBOM artifact present.

## Failure Scenarios

- 403 on push: missing `packages: write` — add the permission block.
- `latest` deployed somewhere: retag nothing; fix consumers to pin the digest.

## Cleanup

Keep images; they are small and prove immutability.

## What This Proved

Build-once identity, SHA discipline, SBOM habit. Continue with [Lab 04](04-deployment.md).

## Interview Notes

- Digest vs tag: why redeploying `latest` can silently change what's running.
- The 403 on push — which single permission block fixes it and why least privilege demands it.


---

<!-- merged-part-4-from: 16-labs/04-deployment.md -->

<!-- icon: deployment -->
## Part 4: Lab 04 — Deployment

## Objective

Promote Lab 03's digest through staging to production with an explicit approval gate — same digest, two environments.

## Prerequisites

- Lab 03 digest in GHCR; concepts: [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md), [Environments & Release](../09-environments-and-release/environments-release.md).

## Architecture

`main` → deploy digest to staging (auto) → smoke check → GitHub Environment `production` (required reviewer) → deploy same digest → verify.

## Setup

Repo Settings → Environments → create `staging` and `production`; set a required reviewer on `production`.

## Step 1 — Staging auto-deploys

### Execute

```yaml
deploy-staging:
  needs: image
  environment: staging
  runs-on: ubuntu-latest
  steps:
    - run: echo "deploy ${{ needs.image.outputs.digest }} to staging"
```

### Expected Result

Every `main` merge deploys staging without human action.

### Why

Staging proves the artifact continuously; automation here is safe because users never see it.

## Step 2 — Production needs a human

### Execute

Add `deploy-prod` with `environment: production` and `needs: [deploy-staging]`; merge, then approve the pending deployment.

### Expected Result

Production waits for approval; after approval it runs the same digest.

### Why

This is Continuous Delivery's one gate: releasable always, deployed by decision (see [delivery vs deployment](../07-continuous-delivery/continuous-delivery.md)).

## Verification

- [ ] Staging deploys on every merge, no clicks.
- [ ] Production blocks until approved.
- [ ] Both environments ran the identical digest.

## Failure Scenarios

- Approval never arrives: check environment reviewers and notifications.
- Digests differ between envs: promotion passed a tag, not a digest — pass `${{ outputs.digest }}` explicitly.

## Cleanup

Keep environments; Lab 05 breaks production on purpose.

## What This Proved

Promotion paths, environment gates, digest discipline. Continue with [Lab 05](05-rollback.md).

## Interview Notes

- What the production approval gate actually blocks — and where reviewers are configured.
- Tag vs digest promotion: how you prove both environments ran identical bytes.


---

<!-- merged-part-5-from: 16-labs/05-rollback.md -->

<!-- icon: monitoring -->
## Part 5: Lab 05 — Rollback

## Objective

Break production deliberately, then recover by redeploying the previous known-good digest — and write the postmortem.

## Prerequisites

- Lab 04 green with two successful production deploys (you need a previous good digest); concepts: [Rollback & Recovery](../14-reliability-and-recovery/rollback-recovery.md).

## Architecture

Bad merge → staging green-but-wrong (tests miss it) → approved to prod → incident → redeploy previous digest → postmortem with a pipeline action item.

## Setup

Note the current production digest; keep its value handy.

## Step 1 — Cause the incident

### Execute

Merge a change that passes tests but breaks the app's visible output (e.g. wrong port, broken route). Promote to production.

### Expected Result

Production is broken despite a green pipeline.

### Why

Green ≠ correct: tests cover what you thought of. This is why recovery must be engineered, not improvised.

## Step 2 — Roll back, don't rebuild

### Execute

Redeploy the previous digest to production (re-run the old `deploy-prod` or dispatch with the saved digest). Time yourself.

### Expected Result

Production healthy in minutes; no fresh build involved.

### Why

Old digests are proven; fresh builds add untested variables to a fire (see [rollback rule](../14-reliability-and-recovery/rollback-recovery.md)).

## Step 3 — Postmortem with teeth

### Execute

Write: timeline, root cause, and one action item that becomes a pipeline change (a new test, check, or alert) — then implement it.

### Expected Result

A merged pipeline change that would have caught this incident.

### Why

Postmortems without merged changes are diary entries.

## Verification

- [ ] Recovery time measured (aim: minutes).
- [ ] Previous digest redeployed, not a fresh build.
- [ ] One preventive pipeline change merged.

## Failure Scenarios

- Previous digest unknown: promotion didn't record digests — log every deployed digest from now on.
- Rollback also broken: data migrated forward — forward-fix with expand-contract instead.

## Cleanup

Keep the postmortem in the repo (`docs/postmortems/`).

## What This Proved

Recovery as a practiced path. General labs complete — Jenkins track starts at [Lab 06](06-jenkins-controller.md).

## Interview Notes

- Rollback vs forward-fix: which failure forces expand-contract instead of reverting.
- Why the deployed digest must be recorded — what "previous digest unknown" costs you mid-incident.


---

<!-- merged-part-6-from: 16-labs/06-jenkins-controller.md -->

<!-- icon: jenkins -->
## Part 6: Lab 06 — Jenkins Controller & First Pipeline

## Objective

Run a real controller + agent with Docker Compose, connect them, and execute the canonical three-stage Jenkinsfile.

## Prerequisites

- Docker; concepts: [Jenkins Setup](../15-platforms-and-tools/jenkins/jenkins-setup.md), [Jenkins Pipelines](../15-platforms-and-tools/jenkins/jenkins-pipelines.md).

## Architecture

Compose: `jenkins` (controller, port 8080, volume `jenkins_home`) + `agent` (inbound, label `docker-agent`) → Multibranch or Pipeline job → Build/Test/Deploy stages.

## Setup

```bash
mkdir jenkins-lab && cd jenkins-lab
## Part 6: docker-compose.yml: jenkins/jenkins:lts + inbound agent joined with the secret from the controller UI
docker compose up -d
```

Get the admin password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`.

## Step 1 — Connect the agent

### Execute

Manage Jenkins → Nodes → create node `agent-1`, labels `docker-agent`, launch via inbound; run the agent container with the secret + controller URL. Install suggested plugins.

### Expected Result

Node page shows `agent-1` online with 2–4 executors.

### Why

Controller schedules, agents execute — this split is the whole architecture (see [Jenkins Architecture](../15-platforms-and-tools/jenkins/jenkins-architecture.md)).

## Step 2 — Run the canonical pipeline

### Execute

New Pipeline job, agent `docker-agent`, script:

```groovy
pipeline {
  agent { label 'docker-agent' }
  stages {
    stage('Build') { steps { sh 'echo build' } }
    stage('Test')  { steps { sh 'echo test' } }
    stage('Deploy'){ steps { echo 'deploy' } }
  }
}
```

### Expected Result

Stage View shows three green boxes on `agent-1`.

### Why

The minimal pipeline that proves scheduling, execution, and visualization all work.

## Verification

- [ ] Agent online, labeled, executors idle after run.
- [ ] Three green stages in Stage View.
- [ ] Controller ran zero builds (check: no executors on `master`).

## Failure Scenarios

- Agent offline: wrong secret/URL or controller unreachable — check container logs, use `http://jenkins:8080` in-Compose.
- No executors on controller is correct — never enable them in prod.

## Cleanup

`docker compose down` keeps `jenkins_home` volume; `down -v` wipes everything.

## What This Proved

Controller/agent split hands-on. Continue with [Lab 07](07-jenkins-shared-library.md).

## Interview Notes

- `down` vs `down -v`: which one wipes `jenkins_home` and why that distinction is the whole lesson.
- Zero executors on the controller — what you check to prove no build ever ran there.


---

<!-- merged-part-7-from: 16-labs/07-jenkins-shared-library.md -->

<!-- icon: jenkins -->
## Part 7: Lab 07 — Jenkins Shared Library

## Objective

Extract a duplicated pipeline step into a versioned shared library consumed by two pipelines — reuse without copy-paste.

## Prerequisites

- Lab 06 running; a second pipeline job; a git repo to host the library.

## Architecture

Library repo (`vars/notifySlack.groovy`-style step) → Global Pipeline Libraries → two Jenkinsfiles call the same step → one fix propagates to both.

## Setup

Create repo `pipeline-library` with `vars/standardTest.groovy`:

```groovy
def call(Map cfg = [:]) {
  sh "${cfg.cmd ?: 'npm test'}"
}
```

## Step 1 — Register the library

### Execute

Manage Jenkins → System → Global Pipeline Libraries → add `my-lib`, default version `main`, source pointing at the repo.

### Expected Result

Library listed, HEAD resolved.

### Why

Versioned libraries are dependencies: pinned, reviewed, rollback-able — unlike copy-pasted steps.

## Step 2 — Consume from two pipelines

### Execute

In both Jenkinsfiles:

```groovy
@Library('my-lib') _
pipeline {
  agent { label 'docker-agent' }
  stages { stage('Test') { steps { standardTest(cmd: 'npm test') } } }
}
```

### Expected Result

Both pipelines green, both calling the shared step.

### Why

One definition, N consumers — the DRY payoff, with the version pin as the safety rail.

## Verification

- [ ] Both pipelines call the library step.
- [ ] Breaking the library breaks both (proves sharing); reverting fixes both.
- [ ] Library change went through PR review on its own repo.

## Failure Scenarios

- `Library my-lib not found`: name mismatch or version unresolvable — check Global config + repo branch.
- Untrusted library on sandbox: approve signatures or restrict to trusted source.

## Cleanup

Keep the library repo — it is the seed of pipeline governance.

## What This Proved

Reusable pipeline code with versioning. Continue with [Lab 08](08-jenkins-backup-restore.md).

## Interview Notes

- `Library not found`: the two causes (name vs version) and where each is configured.
- Why library changes go through PR review on their own repo — what unreviewed shared code risks.


---

<!-- merged-part-8-from: 16-labs/08-jenkins-backup-restore.md -->

<!-- icon: jenkins -->
## Part 8: Lab 08 — Jenkins Backup & Restore

## Objective

Prove disaster recovery: back up `JENKINS_HOME`, destroy the controller, restore on fresh infra, replay the smoke pipeline.

## Prerequisites

- Lab 06 controller with job history; concepts: [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md) backup section.

## Architecture

Running controller → stop → archive `jenkins_home` volume → wipe → fresh controller → restore archive → verify jobs, credentials, history → run smoke pipeline.

## Setup

Note one job's last build number and one credential ID — these are what you will verify after restore.

## Step 1 — Back up

### Execute

```bash
docker compose stop jenkins
docker run --rm -v jenkins-lab_jenkins_home:/data -v "$PWD":/out alpine \
  tar czf /out/jenkins-backup.tar.gz -C /data .
docker compose start jenkins
```

### Expected Result

`jenkins-backup.tar.gz` exists, timestamped; controller restarts normally.

### Why

Offline backup = consistent snapshot; live copies risk half-written state.

## Step 2 — Destroy and restore

### Execute

```bash
docker compose down -v          # destroy EVERYTHING, including the volume
docker compose up -d            # fresh controller
docker compose stop jenkins
docker run --rm -v jenkins-lab_jenkins_home:/data -v "$PWD":/in alpine \
  tar xzf /in/jenkins-backup.tar.gz -C /data
docker compose start jenkins
```

### Expected Result

Jobs, build history, credentials, and plugins all present; recorded build number matches.

### Why

Backup untested = backup imaginary. This drill is the quarterly DR practice from the advanced doc.

## Verification

- [ ] Job list + history identical (check the recorded build number).
- [ ] Credential ID present and usable.
- [ ] Smoke pipeline (Lab 06's) runs green on the restored controller.

## Failure Scenarios

- Plugin version drift: restore on a different image tag — pin `jenkins:lts` digests for controller + backup.
- Permission errors: volume owned by wrong UID — `chown -R 1000:1000` on the volume.

## Cleanup

Store one backup off-machine; delete the rest.

## What This Proved

Recovery measured, not assumed. Labs complete — return to the [Topic Index](../TOPIC_INDEX.md).

## Interview Notes

- The restore proof: which pipeline you run post-restore and what green actually verifies.
- Plugin drift and UID ownership — the two restore failures and their one-line fixes.
