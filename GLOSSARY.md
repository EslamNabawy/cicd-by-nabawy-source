# Glossary

| Term | Definition | Related Topic |
|------|------------|---------------|
| Artifact | Versioned output produced by a build (e.g. Docker image, jar, zip) | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Approval | Human or policy gate before promotion to an environment | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Blue/Green Deployment | Two identical environments, traffic switched from blue to green | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Branch | Independent line of development in Git | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Build | Compiling/bundling source into a runnable artifact | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| CD | Continuous Delivery / Continuous Deployment | [CI/CD Overview](00-foundations/cicd-overview.md) |
| CI | Continuous Integration: frequent merges verified by automated build+test | [CI/CD Overview](00-foundations/cicd-overview.md) |
| CI Trigger | Event that starts a pipeline (push, PR, schedule, manual) | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Continuous Delivery | Every good change is releasable; deployment is a decision | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Continuous Deployment | Every good change reaches production automatically | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Canary Deployment | Release to a small subset first, expand on success | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Contract Test | Verifies API compatibility between provider and consumer services | [Testing Strategy](04-testing/testing-strategy.md) |
| Deployment | Installing/running a release in an environment | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| DORA | DevOps Research & Assessment; four delivery signals (deploy frequency, lead time, change-fail rate, MTTR) | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Environment | Target runtime context (staging, production) | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Expand-Contract | Migration pattern: add nullable → migrate → enforce; safe both directions | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| GitOps | Git as desired state; in-cluster operator pulls reality toward it | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Game Day | Planned failure injection in staging to practice recovery | [Rollback & Recovery](14-reliability-and-recovery/rollback-recovery.md) |
| Merge Queue | Serializes merges onto latest green main with re-verification | [Continuous Integration](02-continuous-integration/continuous-integration.md) |
| Multibranch Pipeline | Auto-created sub-job per branch/PR with Jenkinsfile; reports checks, prunes dead branches | [Jenkins Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) |
| Error Budget | Allowable failure quota; burn it too fast and releases halt | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Feedback | Signals (test results, metrics, alerts) returned to developers | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Feature Flags | Runtime toggles switching code paths without redeploying; instant rollback | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Floci | AWS API simulator used as a no-cost deploy target for pipeline practice | [Jenkins Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) |
| Jenkins Agent | Machine offering executors to the controller, selected by labels | [Jenkins Agents](15-platforms-and-tools/jenkins/jenkins-agents.md) |
| Jenkinsfile | Pipeline-as-code file (Declarative or Scripted) in the repo | [Jenkins Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) |
| Jenkins Controller | Schedules work, serves UI, holds JENKINS_HOME; runs no builds in prod | [Jenkins Architecture](15-platforms-and-tools/jenkins/jenkins-architecture.md) |
| Jenkins Credentials | Typed secrets store injected via bindings | [Jenkins Credentials](15-platforms-and-tools/jenkins/jenkins-credentials.md) |
| Jenkins Executor | One build slot on an agent | [Jenkins Agents](15-platforms-and-tools/jenkins/jenkins-agents.md) |
| Jenkins Plugin | Extension adding capabilities (git, docker, credentials) | [Jenkins Plugins](15-platforms-and-tools/jenkins/jenkins-plugins.md) |
| GitHub Actions | GitHub's CI/CD: workflows of jobs/steps on hosted or self-hosted runners | [GitHub Actions](15-platforms-and-tools/github-actions.md) |
| Hermetic Build | Sealed from ambient machine state: pinned deps, clean env — same commit builds identically anywhere | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Job | Unit of executable work inside a stage | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Observability | Logs, metrics, traces that reveal system behavior | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Pipeline | Automated workflow from commit to deployment | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Promotion | Moving a validated artifact toward the next environment | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Pull Request (PR) | Proposal to merge a branch, with review + automated checks | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Review App | Ephemeral live environment per merge request, destroyed on merge | [GitLab CI](15-platforms-and-tools/gitlab-ci.md) |
| Registry | System storing and distributing artifacts/images | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Release | Version made available for deployment or users | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Release Train | Scheduled departures; green + approved changes ride, rest wait | [Environments & Release](09-environments-and-release/environments-release.md) |
| Runner / Agent | Execution environment that runs pipeline jobs | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| SBOM | Software Bill of Materials: machine-readable ingredient list of every package in an artifact | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Security Scan | Automated check for vulnerabilities/secrets/misconfig | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| SLO | Service Level Objective, e.g. 99.9% successful requests; breaching it burns the error budget | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| SLI | Service Level Indicator: what you measure (success ratio, p99 latency) | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Stage | Logical phase of a pipeline (build, test, deploy) | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Shared Library | Versioned reusable pipeline code (`vars/`) consumed by N pipelines | [Lab 07](16-labs/07-jenkins-shared-library.md) |
| Smoke Test | Minimal post-deploy probe proving the app answers | [Testing Strategy](04-testing/testing-strategy.md) |
| Step | Individual operation inside a job | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
