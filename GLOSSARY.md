# Glossary

| Term | Definition | Related Topic |
|------|------------|---------------|
| Artifact | Versioned output produced by a build (e.g. Docker image, jar, zip) | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Approval | Human or policy gate before promotion to an environment | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Blue/Green Deployment | Two identical environments, traffic switched from blue to green | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Branch | Independent line of development in Git | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Build | Compiling/bundling source into a runnable artifact | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Continuous Delivery | Every good change is releasable; production deploy is a human/policy decision | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Continuous Deployment | Every good change reaches production automatically | [Continuous Deployment](08-continuous-deployment/continuous-deployment.md) |
| CI | Continuous Integration: frequent merges verified by automated build+test | [CI/CD Overview](00-foundations/cicd-overview.md) |
| CI Trigger | Event that starts a pipeline (push, PR, schedule, manual) | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
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
| Trunk-Based Development | Small, frequent merges to main with feature flags; releasable always | [Continuous Integration](02-continuous-integration/continuous-integration.md) |
| GitOps | Already listed above — git as source of truth for cluster state | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Helm Chart | Versioned, templated Kubernetes manifests with per-env values | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Docker Image | Frozen filesystem plus metadata; the artifact that moves through envs | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Kubernetes (K8s) | Container orchestrator: desired-state scheduler for pods and services | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Terraform | IaC tool that declares envs; plan is the review, apply is gated | [IaC for Environments](12-infrastructure-and-configuration/iac-environments.md) |
| Loki | Log aggregation indexed by labels; cheap exact-error forensics | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Prometheus | Metrics engine that scrapes time series and alerts on burn rate | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Grafana | Unified dashboards over Loki and Prometheus with deploy annotations | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| ArgoCD | GitOps operator that pulls manifests into clusters with sync waves | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Immutable Artifact | Digest-pinned output that never changes after build | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Provenance | Signed attestation proving who built what, when, from which commit | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Cosign | Tool that signs and verifies artifact signatures | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| SLSA | Framework for supply-chain levels of assurance | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Canary Analysis | Automated promotion decision based on golden signals | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Rollback Window | Time after deploy when revert is safe without data migration | [Rollback & Recovery](14-reliability-and-recovery/rollback-recovery.md) |
| Drift | Live state that no longer matches declared git or IaC | [IaC for Environments](12-infrastructure-and-configuration/iac-environments.md) |
| Sealed Secret | Encrypted secret safe to store in git; decrypted in cluster | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| BuildKit | Fast, cached, hermetic Docker build engine | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| OIDC | OpenID Connect: short-lived identity tokens for keyless auth in CI | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Rolling Deployment | Batch-by-batch rollout behind readiness probes; no downtime | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Recreate Deployment | Stop old, start new — simplest, causes downtime | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Dark Launch | Release behind flag to subset without user impact; measure silently | [Deployment Strategies](10-deployment-strategies/deployment-strategies.md) |
| Parallelism | Jobs or steps running concurrently to cut lead time | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Matrix Build | Fan-out of one job across versions/envs in a single pipeline | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Cache | Reused layer keyed on inputs to avoid rebuilding unchanged work | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Monorepo | Single repo holding many services; one pipeline fans out | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Trunk | Main branch that must stay green and releasable | [Continuous Integration](02-continuous-integration/continuous-integration.md) |
| Rebase | Replay commits onto latest main to keep linear history | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Cherry-Pick | Copy single commit to another branch without full merge | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Code Review | Human approval gate on a pull request before merge | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Status Check | Automated CI gate reported on a PR; blocks merge if red | [Git, Branching & Pull Requests](01-source-control/git-branching-pull-requests.md) |
| Webhook | HTTP callback that triggers a pipeline on git events | [Jenkins Webhooks](15-platforms-and-tools/jenkins/jenkins-webhooks.md) |
| JCasC | Jenkins Configuration as Code: declarative controller setup in YAML | [Jenkins Advanced](15-platforms-and-tools/jenkins/jenkins-advanced.md) |
| Declarative Pipeline | Opinionated Jenkinsfile syntax with stages/steps; validated upfront | [Jenkins Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) |
| Scripted Pipeline | Full Groovy Jenkinsfile with imperative control flow | [Jenkins Pipelines](15-platforms-and-tools/jenkins/jenkins-pipelines.md) |
| Groovy | JVM language powering Jenkins pipelines and shared libraries | [Jenkins Advanced](15-platforms-and-tools/jenkins/jenkins-advanced.md) |
| Pipeline as Code | Pipelines versioned in git alongside app code | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Self-Hosted Runner | Runner you own and scale; controller schedules onto it | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| Ephemeral Runner | Short-lived runner pod or VM created per job then destroyed | [CI/CD Pipelines](06-ci-cd-pipelines/pipelines.md) |
| GHCR | GitHub Container Registry: where images and attestations live | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Attestation | Provenance record attached to an artifact for verification | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Digest | Content hash pinning the exact artifact bytes | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Tag | Human name for an image version; mutable, unlike digest | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| SemVer | Semantic versioning MAJOR.MINOR.PATCH with breaking-change rules | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
| Staging | Prod-like rehearsal environment with sanitized data | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Production | Live environment serving real users with real data | [Continuous Delivery](07-continuous-delivery/continuous-delivery.md) |
| Preview Environment | Ephemeral env per PR destroyed on merge; proves the change | [Environments & Release](09-environments-and-release/environments-release.md) |
| Infrastructure as Code (IaC) | Env definitions in versioned code; plan is the review | [IaC for Environments](12-infrastructure-and-configuration/iac-environments.md) |
| Drift Detection | Scheduled check that live state matches declared code | [IaC for Environments](12-infrastructure-and-configuration/iac-environments.md) |
| ApplicationSet | ArgoCD template that fans one app definition into N envs | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Sync Wave | Ordered phase for ArgoCD to apply resources | [ArgoCD & GitOps](15-platforms-and-tools/argocd-gitops.md) |
| Golden Signals | Latency, traffic, errors, saturation — the four to watch | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| RED Method | Rate, Errors, Duration — microservice health triplet | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| USE Method | Utilization, Saturation, Errors for resource focus | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| LogQL | Query language for Loki log lines | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| PromQL | Query language for Prometheus metrics | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| Runbook | Step-by-step ops guide linked from an alert | [Observability & Feedback](13-observability-and-feedback/observability-feedback.md) |
| MTTR | Mean Time To Recovery after failure | [Rollback & Recovery](14-reliability-and-recovery/rollback-recovery.md) |
| Postmortem | Blameless review turning an incident into pipeline changes | [Rollback & Recovery](14-reliability-and-recovery/rollback-recovery.md) |
| Supply Chain | Path from source through build to registry to cluster | [Artifact Management](05-artifacts-and-packaging/artifact-management.md) |
