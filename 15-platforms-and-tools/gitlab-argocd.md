---
title: Gitlab Argocd
status: complete
merged_from:
  - 15-platforms-and-tools/gitlab-ci.md
  - 15-platforms-and-tools/argocd-gitops.md
---

# Gitlab Argocd

> Merged handbook. Sources: 15-platforms-and-tools/gitlab-ci.md, 15-platforms-and-tools/argocd-gitops.md.


---

<!-- merged-part-1-from: 15-platforms-and-tools/gitlab-ci.md -->

<!-- icon: gitlab -->
## Part 1: GitLab CI

> GitLab CI is the pipeline engine inside GitLab: one YAML file in the repo (`.gitlab-ci.yml`) driving stages, runners, and environments — the same concepts as Jenkins and Actions, with GitLab's own vocabulary.

## 1. What Is It?

Picking up from **[GitHub Actions](../15-platforms-and-tools/github-actions.md)**, where workflows lived beside the code — GitLab goes further: repo, pipeline, registry, and environments are one product, so the pipeline natively knows about merge requests, environments, and review apps.

## 2. Pipeline Anatomy (GitLab Vocabulary)

```yaml
stages: [build, test, deploy]
build:
  stage: build
  script: [npm ci, npm run build]
test:
  stage: test
  needs: [build]          # DAG edge — runs as soon as build passes
```

- **Stages** run in order; **jobs** in the same stage run in parallel.
- **`needs:`** builds a DAG (like Actions), skipping stage waits.
- **`rules:`** decides when jobs run (merge request only, `main` only, paths changed) — replaces the older `only/except`.
- **`artifacts:`** passes files between jobs (reports, coverage, JUnit); **`cache:`** speeds reruns (lockfile-keyed, same discipline as everywhere).

## 3. Runners & Tags

| Runner scope | Use |
|--------------|-----|
| Shared | Fleet managed by the instance; default for most jobs |
| Group / project (specific) | GPU, private network, compliance isolation |
| Tags (`tags: [gpu]`) | Route jobs to capable runners |

One job = one runner by default; scale = more runners. Self-managed runners need the same patching/scaling discipline as any self-hosted fleet.

## 4. Environments, Review Apps & Merge Trains

- **Environments** (`environment: staging/production`) track what's deployed where; production gates add manual approvals — the same delivery-vs-deployment line as everywhere.
- **Review apps** (`on_stop:` teardown) spin a live environment per merge request and destroy it on merge — GitLab's built-in preview environments.
- **Merge trains** serialize merges onto latest green `main` with re-verification — the same race the merge queue solves elsewhere.

## 5. GitLab vs the Sisters

| | GitLab CI | GitHub Actions | Jenkins |
|---|---|---|---|
| Config lives | `.gitlab-ci.yml` in repo | `.github/workflows/` | Jenkinsfile in repo |
| Runners | Shared fleet + tags | Hosted + ARC | Controller + agents |
| Environments | Built-in (+ review apps) | Environments as gates | Manual promotion jobs |
| Best when | Already on GitLab; want one product | Already on GitHub | Need total control |

## 6. Failure Modes

- Shared-runner queues at peak → pin critical jobs to tagged runners or add project runners.
- `rules:` mis-scoping → jobs silently skip; every `rules:` change deserves a pipeline dry-run on a test MR.
- Artifacts bloating storage → expire aggressively (`expire_in:`), keep images in the registry not in job artifacts.

## 7. Interview Notes

- `needs:` vs stage ordering: when the DAG matters.
- Review apps lifecycle: create on MR, destroy on merge (`on_stop`).
- Merge trains: which race they eliminate.

## Related Topics

- [GitHub Actions](../15-platforms-and-tools/github-actions.md)
- [Continuous Integration](../02-continuous-integration/continuous-integration.md)
- [Environments & Release](../09-environments-and-release/environments-release.md)

Pipelines push changes — something has to keep the cluster matching git. Continue in **[ArgoCD & GitOps](argocd-gitops.md)**.


---

<!-- merged-part-2-from: 15-platforms-and-tools/argocd-gitops.md -->

<!-- icon: argocd -->
## Part 2: ArgoCD & GitOps

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
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [GitLab CI](gitlab-ci.md)

GitOps declares app state — but environments themselves are infrastructure. Continue in **[IaC for Environments](../12-infrastructure-and-configuration/iac-environments.md)**.
