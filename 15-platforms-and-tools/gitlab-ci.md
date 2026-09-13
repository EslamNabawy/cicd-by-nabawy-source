---
title: GitLab CI
category: platforms
status: complete
difficulty: intermediate
prerequisites:
  - CI/CD Pipelines
  - GitHub Actions (sister platform)
related:
  - GitHub Actions
  - ArgoCD & GitOps
---

<!-- icon: gitlab -->
# GitLab CI

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
