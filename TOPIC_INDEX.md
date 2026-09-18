# CI/CD Topic Index

> Map of the whole knowledge base. Updated on every structural change.
> 2026-09-17 merge: 40 small sources consolidated into 9 merged handbooks + 5 standalone docs (14 website books). Member sources remain on disk as merge inputs; merged files are canonical.

## Start Here (merged)

- [Start Here: Foundations, Git & CI](00-foundations/start-here-merged.md) — lifecycle, branching, PR gates, merge queues, trunk (merges `00-foundations/cicd-overview.md`, `01-source-control/git-branching-pull-requests.md`, `02-continuous-integration/continuous-integration.md`)

## Pipelines & Verification (merged + standalone)

- [Pipelines, Build & Test](06-ci-cd-pipelines/pipelines-build-test.md) — stages/jobs/runners, hermetic builds, caching, pyramid, flakes (merges `06-ci-cd-pipelines/pipelines.md`, `03-build-systems/build-systems.md`, `04-testing/testing-strategy.md`)
- [Artifact Management](05-artifacts-and-packaging/artifact-management.md) — Artifact, Registry, versioning, promotion

## Delivery & Operations (merged + standalone)

- [Delivery, Envs & IaC](07-continuous-delivery/delivery-envs-iac.md) — approvals, auto-to-prod, env topology, Terraform state per env (merges `07-continuous-delivery/continuous-delivery.md`, `08-continuous-deployment/continuous-deployment.md`, `09-environments-and-release/environments-release.md`, `12-infrastructure-and-configuration/iac-environments.md`)
- [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) — Rolling, Blue/Green, Canary, Recreate, Feature Flags
- [Observe, Recover & Secure](13-observability-and-feedback/observe-recover-secure.md) — golden signals, rollback drills, postmortems, secrets, SBOM (merges `13-observability-and-feedback/observability-feedback.md`, `14-reliability-and-recovery/rollback-recovery.md`, `11-security/cicd-security.md`)

## Platforms & Tools (merged + standalone)

- [Jenkins Core](15-platforms-and-tools/jenkins/jenkins-core-merged.md) — concept map, architecture, setup, pipelines, agents (merges `jenkins/README.md`, `jenkins-architecture.md`, `jenkins-setup.md`, `jenkins-pipelines.md`, `jenkins-agents.md`)
- [Jenkins Advanced & Operations](15-platforms-and-tools/jenkins/jenkins-advanced-ops.md) — Groovy, credentials, plugins, webhooks, security, JCasC, troubleshooting (merges `jenkins-groovy-cheatsheet.md`, `jenkins-credentials.md`, `jenkins-plugins.md`, `jenkins-webhooks.md`, `jenkins-security.md`, `jenkins-advanced.md`, `jenkins-troubleshooting.md`)
- [GitHub Actions](15-platforms-and-tools/github-actions.md) — workflows, jobs, runners, environments as gates
- [GitLab & ArgoCD](15-platforms-and-tools/gitlab-argocd.md) — stages with needs DAG, review apps, pull delivery, sync waves (merges `gitlab-ci.md`, `argocd-gitops.md`)

## Labs (merged handbooks)

- [Core Labs Handbook](16-labs/core-labs-handbook.md) — pipeline, build/test, artifacts, deployment, rollback, Jenkins live, shared lib, DR (merges `16-labs/01-first-pipeline.md` → `08-jenkins-backup-restore.md`)
- [Jenkins Labs Handbook](16-labs/jenkins-labs-handbook.md) — webhooks, Docker/DockerHub, multibranch, shared library, Terraform FLOCI (merges all 5 `jenkins labs/*.md`; canonical copy lives in `16-labs/` because `jenkins labs/` is gitignored)

## Reference

- [Command Cheatsheet](17-reference/command-cheatsheet.md) — every lab command grouped by tool
