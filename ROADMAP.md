# Roadmap

> `[x]` complete · `[~]` in progress · `[ ]` planned. Complete = file exists and is sufficiently developed.

## Foundations

- [x] CI/CD overview + end-to-end graph
- [x] CI vs Delivery vs Deployment distinction

## Source Control

- [x] Git essentials for CI/CD
- [x] Branching models
- [x] Pull Requests + status checks
- [x] CI triggers (push, PR, schedule, manual)
- [x] CI discipline, PR gates, merge queues, trunk (02)

## Pipelines

- [x] Pipeline, stages, jobs, steps, runners
- [x] Build stage
- [x] Test stage
- [x] Security scan stage
- [x] Runners deep dive (self-hosted vs managed, caching)
- [x] Parallelism, dependencies, failure handling
- [x] Build systems: Maven/Gradle/npm, caching, hermetic (03)
- [x] Testing strategy: pyramid, contract/E2E, flaky policy, capacity placement, test doubles (04)

## Artifacts

- [x] Artifact concept + registry + promotion
- [x] Versioning schemes (semver, sha, build numbers, date-based)
- [x] SBOM / signing / provenance

## Delivery

- [x] CD concept, staging, production, approvals
- [x] Deployment strategies (rolling, blue/green, canary, recreate, feature flags)
- [x] Continuous deployment: prereqs, kill criteria (08)
- [x] Environments & release: topology, config vs code, trains (09)
- [x] Rollback & recovery procedures + data migration practice (14)

## Feedback

- [x] Observability basics + feedback loop
- [x] SLI/SLO/alerting (burn-rate alerts, runbooks)
- [x] DORA metrics (four signals + elite hints)

## Security

- [x] CI/CD security: secrets, signing, SBOM, least privilege, gates (11)

## Platforms (Jenkins Domain)

- [x] Architecture (controller/agents)
- [x] Setup (Docker, first job)
- [x] Pipelines (Declarative, Jenkinsfile, multibranch)
- [x] Agents (labels, executors, ephemeral)
- [x] Credentials (kinds, scopes, bindings)
- [x] Plugins (essential set, pinning)
- [x] Webhooks & triggers
- [x] Security (matrix, agent trust)
- [x] Advanced (shared libs, parallel/matrix, JCasC, backup, Script Console)
- [x] Troubleshooting
- [x] Jenkins labs 06–08 (controller, shared library, backup/restore in 16-labs/)
- [x] JCasC + production topology (HA, fleets, zones, DR drill)

## Platforms (GitHub Actions)

- [x] Workflows, jobs, steps, runners, triggers
- [x] CI + gated CD example
- [x] Reusable workflows, matrix, concurrency, path filters
- [x] Self-hosted runners + ARC scale set

## Platforms (GitLab CI, ArgoCD)

- [x] GitLab: stages, needs DAG, rules, runners+tags, review apps, merge trains
- [x] ArgoCD: push vs pull, Application, sync waves, ApplicationSets

## Infrastructure

- [x] IaC for environments: modules, state per env, plan-as-review, drift, preview automation

## Publication (PDF Phase — In Progress)

- [x] Per-file PDFs 01–39 in `pdf/` (standalone A4 HTML, spec system, Nabawy signature, all QC green)
- [x] Series edition S01–S09 in `pdf/series/` (omnibus generator `scripts/build_series.py`, all QC green)
- [x] Series on the website (Series edition section + print PDFs ship in `dist/`)

## Website (Live)

- [x] Library + reader in `website/dist/` per `WEBSITE_BUILD_SPEC.md` (36 books, TOC, 2 themes, font/width, search, progress, glossary, mobile, print)
- [x] Deployed: https://eslamnabawy.github.io/cicd-library/ (repo `EslamNabawy/cicd-library`, `gh-pages` branch)
- Standing: rebuild via `website/scripts/build.py` + repush `dist/` after each new book
- [x] Knowledge content complete (36 md files) — HTML/PDF work unblocked

## Labs

- [x] 01-first-pipeline (GHA green + branch protection)
- [x] 02-build-and-test (DAG, cache, hermetic proof)
- [x] 03-artifacts (SHA tags, GHCR, SBOM)
- [x] 04-deployment (staging auto, prod approval)
- [x] 05-rollback (incident, digest redeploy, postmortem)
- [x] 06-jenkins-controller (compose, agent, first pipeline)
- [x] 07-jenkins-shared-library (versioned reuse)
- [x] 08-jenkins-backup-restore (DR drill)

## Reference

- [x] Command cheatsheet (grouped by tool)
