# CI/CD Topic Index

> Map of the whole knowledge base. Updated on every structural change.

## Foundations

- [CI/CD Overview](00-foundations/cicd-overview.md) — CI, CD, why automation, the end-to-end graph

## Source Control & Change Flow

- [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) — Git, Branching, Pull Request, CI Trigger
- [Continuous Integration](02-continuous-integration/continuous-integration.md) — merge discipline, PR gates, merge queues, trunk

## Pipelines & Verification

- [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) — Pipeline, Stages, Jobs, Steps, Runners, Build, Test, Security Scan, CI Trigger execution
- [Build Systems](03-build-systems/build-systems.md) — Maven/Gradle/npm, caching, hermetic builds
- [Testing Strategy](04-testing/testing-strategy.md) — pyramid, contract/integration/E2E, flaky policy

## Artifacts & Supply Chain

- [Artifact Management](05-artifacts-and-packaging/artifact-management.md) — Artifact, Registry, versioning, promotion

## Delivery & Environments

- [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) — CD, Staging, Production, approvals, promotion flow
- [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) — Rolling, Blue/Green, Canary, Recreate, Feature Flags
- [Continuous Deployment](08-continuous-deployment/continuous-deployment.md) — auto-to-prod prereqs, kill criteria
- [Environments & Release](09-environments-and-release/environments-release.md) — topology, config vs code, release trains

## Feedback & Operations

- [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) — Observability, Feedback loop to developers
- [Rollback & Recovery](14-reliability-and-recovery/rollback-recovery.md) — rollback per strategy, MTTR drills, postmortems

## Security & Supply Chain

- [CI/CD Security](11-security/cicd-security.md) — secrets, signing, SBOM, least privilege, supply-chain gates

## Infrastructure as Code

- [IaC for Environments](12-infrastructure-and-configuration/iac-environments.md) — Terraform envs, state per env, drift, preview automation

## Platforms & Tools

- [Jenkins Domain](15-platforms-and-tools/jenkins/README.md) — concept→Jenkins map
  - [Architecture](15-platforms-and-tools/jenkins/jenkins-architecture.md) · [Setup](15-platforms-and-tools/jenkins/jenkins-setup.md) · [Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) · [Groovy Cheatsheet](15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md) · [Agents](15-platforms-and-tools/jenkins/jenkins-agents.md) · [Credentials](15-platforms-and-tools/jenkins/jenkins-credentials.md) · [Plugins](15-platforms-and-tools/jenkins/jenkins-plugins.md) · [Webhooks](15-platforms-and-tools/jenkins/jenkins-webhooks.md) · [Security](15-platforms-and-tools/jenkins/jenkins-security.md) · [Advanced](15-platforms-and-tools/jenkins/jenkins-advanced.md) · [Troubleshooting](15-platforms-and-tools/jenkins/jenkins-troubleshooting.md)
- [GitHub Actions](15-platforms-and-tools/github-actions.md) — workflows, jobs, runners, environments as gates
- [GitLab CI](15-platforms-and-tools/gitlab-ci.md) — stages, runners+tags, review apps, merge trains
- [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) — pull delivery, sync waves, ApplicationSets

## Labs

- [Lab 01 — First Pipeline](16-labs/01-first-pipeline.md) — push → build → test → PR check
- [Lab 02 — Build and Test](16-labs/02-build-and-test.md) — DAG, caching, hermeticity
- [Lab 03 — Artifacts](16-labs/03-artifacts.md) — SHA tags, GHCR, SBOM
- [Lab 04 — Deployment](16-labs/04-deployment.md) — staging auto, production approval
- [Lab 05 — Rollback](16-labs/05-rollback.md) — break prod, redeploy digest, postmortem
- [Lab 06 — Jenkins Controller](16-labs/06-jenkins-controller.md) — compose, agent, first pipeline
- [Lab 07 — Shared Library](16-labs/07-jenkins-shared-library.md) — versioned reuse
- [Lab 08 — Backup & Restore](16-labs/08-jenkins-backup-restore.md) — DR drill

## Reference

- [Command Cheatsheet](17-reference/command-cheatsheet.md) — every lab command grouped by tool
