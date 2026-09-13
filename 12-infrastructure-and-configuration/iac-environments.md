---
title: IaC for Environments
category: infrastructure
status: complete
difficulty: intermediate
prerequisites:
  - Environments & Release
  - ArgoCD & GitOps
related:
  - Environments & Release
  - ArgoCD & GitOps
---

<!-- icon: terraform -->
# IaC for Environments

> Environments are too important to be clicked into existence: Terraform (or equivalent) declares every environment's infrastructure so staging and production differ only by config — never by history.

## 1. What Is It?

Picking up from **[ArgoCD & GitOps](../15-platforms-and-tools/argocd-gitops.md)**, where app state became declarative — IaC does the same for everything underneath: VPCs, clusters, databases, DNS, IAM. Same modules, different inputs per environment.

## 2. Structure That Scales

```text
envs/
├── modules/          # vpc, cluster, db — written once
├── dev/              # small sizes, short retention
├── staging/          # prod-shaped, sanitized data
└── prod/             # real sizes, real data, approvals
```

- **State per environment** (never shared): one blast radius per state file; remote backend with locking.
- **Modules pinned by version** — floating module sources are `:latest` with extra steps.
- **Env diff = input diff:** instance sizes, counts, secrets references. A behavioral difference not explainable by inputs is a bug.

## 3. IaC in the Pipeline

- `terraform plan` on every PR touching `envs/` — the plan is the review.
- `apply` gated like any production deployment (approvals on prod, auto on dev).
- **Drift detection** on schedule: `plan` nightly, alert on unexpected diffs — the IaC equivalent of ArgoCD's self-heal.
- Jenkins controller itself can be code too (JCasC — see [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md)).

## 4. Preview Environments, Automated

Combine the pieces: PR → pipeline runs a Terraform workspace (or ArgoCD ApplicationSet) → ephemeral env with sanitized data → destroy on merge. The highest-leverage environment pattern, fully automated, zero snowflakes.

## 5. Failure Modes

- Shared state across envs → dev `apply` deletes prod tables; separate states, separate credentials.
- Unreviewed `apply` on prod → treat IaC changes like code: PR, plan output, approval.
- Secrets in state files → state holds secrets in plaintext; encrypt backends, restrict access, prefer external secret stores.
- ClickOps drift → someone "fixes" prod in the console; drift alerts + periodic `apply` reconciliation.

## 6. Interview Notes

- Why state-per-environment (blast radius).
- Plan-as-review: what makes IaC changes safe to approve.
- Where JCasC fits (controller config as code, same discipline).

## Related Topics

- [Environments & Release](../09-environments-and-release/environments-release.md)
- [ArgoCD & GitOps](../15-platforms-and-tools/argocd-gitops.md)
- [Jenkins Advanced](../15-platforms-and-tools/jenkins/jenkins-advanced.md)

Infrastructure declared — the library's platform arc is complete. Return to the **[Topic Index](../TOPIC_INDEX.md)**.
