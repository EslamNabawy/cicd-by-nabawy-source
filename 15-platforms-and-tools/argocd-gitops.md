---
title: ArgoCD & GitOps
category: platforms
status: complete
difficulty: advanced
prerequisites:
  - Continuous Delivery
  - Deployment Strategies
related:
  - Continuous Delivery
  - IaC for Environments
---

<!-- icon: argocd -->
# ArgoCD & GitOps

> GitOps: git is the desired state, an in-cluster operator pulls reality toward it. ArgoCD is that operator for Kubernetes — the pipeline stops pushing to prod and starts committing to git.

## 1. What Is It?

Picking up from **[GitLab CI](gitlab-ci.md)**, where pipelines pushed artifacts outward — ArgoCD inverts the last mile: the CI pipeline builds the image and commits the new digest to a manifests repo; ArgoCD (running inside the cluster) notices and syncs. Cluster credentials never leave the cluster.

## 2. Push vs Pull

| | Push (classic CD) | Pull (GitOps) |
|---|---|---|
| Actor | External pipeline holds cluster creds | In-cluster agent, creds stay inside |
| Source of truth | Pipeline run history | Git commit |
| Rollback | Redeploy old digest | `git revert` |
| Drift | Silent until noticed | Detected + optionally auto-healed |

## 3. Core Objects

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata: { name: checkout }
spec:
  source: { repoURL: https://git/ops, targetRevision: main, path: apps/checkout }
  destination: { server: https://kubernetes.default.svc, namespace: prod }
  syncPolicy: { automated: { prune: true, selfHeal: true } }
```

- **Application:** what (repo+path+revision) goes where (cluster+namespace).
- **Sync waves + hooks:** order resources (CRDs before CRs, migrations before app) — the deployment strategy's sequencing, declaratively.
- **ApplicationSet:** one template → N environments/tenants; preview environments become a generator, not a script.
- **Image Updater (optional):** tracks new digests and commits them — automation with git as the audit trail.

## 4. Where It Fits

CI still builds, tests, scans, signs (everything upstream unchanged). The handoff changes: instead of `kubectl apply` from CI, CI commits `image: sha-9f3a` to the ops repo. Promotion = pull request between env branches/folders — reviewable, revertable, auditable.

## 5. Failure Modes

- Auto-sync + bad commit → bad state propagates at machine speed; gate with manual sync on prod or automated kill criteria.
- Secrets in the manifests repo → use external secret operators (External Secrets, Sealed Secrets); git holds references, never values.
- `selfHeal` fighting hotfixes → emergency `kubectl` edits get reverted; declare a break-glass procedure (pause sync, fix, commit).
- Monorepo scale → thousands of Applications; shard by team/cluster with ApplicationSets.

## 6. Interview Notes

- Push vs pull: credential blast radius is the core argument.
- What sync waves solve (ordering without scripts).
- Rollback in GitOps: why `git revert` beats redeploy.

## Related Topics

- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)
- [Deployment Strategies](../10-deployment-strategies/deployment-strategies.md)
- [GitLab CI](gitlab-ci.md)

GitOps declares app state — but environments themselves are infrastructure. Continue in **[IaC for Environments](../12-infrastructure-and-configuration/iac-environments.md)**.
