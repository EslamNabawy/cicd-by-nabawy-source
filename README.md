# CICD BY Nabawy — Library

> 8 merged handbooks, SIGNAL study-guide design, static website. Live:
> https://eslamnabawy.github.io/cicd-by-nabawy/

## Books (source: `pdf/`, manifest: `website/content/books.json`)

| # | Book | File | Path |
|---|---|---|---|
| 1 | Start Here: Foundations, Git & CI | `pdf-merged-01-start-here.html` | start-here |
| 2 | Pipelines, Build, Test & Artifacts | `pdf-merged-10-build-artifacts.html` | build |
| 3 | Delivery, Deployment & Operations | `pdf-merged-11-deliver-operate.html` | deliver |
| 4 | Observability: Loki, Prometheus & Grafana | `pdf-43-observability.html` | observability |
| 5 | Jenkins Complete | `pdf-merged-12-jenkins-complete.html` | jenkins |
| 6 | Platforms & 2026 Roadmaps | `pdf-merged-13-platforms-roadmaps.html` | platforms |
| 7 | Labs Handbook | `pdf-merged-14-labs-handbook.html` | labs |
| 8 | Command Cheatsheet | `pdf-36-command-cheatsheet.html` | reference |

Every book: one cover, Contents sheet, chapters with EXAM boxes, glossary,
interview, cheat sheet, quiz. Zero `PDF NN` seams.

## Learning Flow

```mermaid
flowchart LR
    A[Start Here] --> B[Build, Test & Artifacts]
    B --> C[Deliver & Operate]
    C --> D[Observability]
    D --> E[Jenkins Complete]
    E --> F[Platforms & Roadmaps]
    F --> G[Labs Handbook]
```

## Map (Markdown sources — search index + print fallback)

| Area | Document |
|---|---|
| Foundations | [Start Here](00-foundations/start-here-merged.md) |
| Pipelines/Build/Test | [Pipelines + Builds](06-ci-cd-pipelines/pipelines-build-test.md), [Artifacts](05-artifacts-and-packaging/artifact-management.md) |
| Delivery/Ops | [Delivery + IaC](07-continuous-delivery/delivery-envs-iac.md), [Strategies](10-deployment-strategies/deployment-strategies.md), [Observe/Recover](13-observability-and-feedback/observe-recover-secure.md) |
| Jenkins | [Core](15-platforms-and-tools/jenkins/jenkins-core-merged.md), [Advanced](15-platforms-and-tools/jenkins/jenkins-advanced-ops.md) |
| Platforms | [Actions](15-platforms-and-tools/github-actions.md), [GitLab + ArgoCD](15-platforms-and-tools/gitlab-argocd.md) |
| Labs | [Core](16-labs/core-labs-handbook.md), [Jenkins](16-labs/jenkins-labs-handbook.md) |
| Reference | [Cheatsheet](17-reference/command-cheatsheet.md) |

## Rules

- Source of truth: `pdf/` print editions first, Markdown second (search + fallback).
- Website: `website/` — rebuild after any change (`website/scripts/build.py`),
  verify (`scripts/qc-check.py`), push source, manual `gh-pages` deploy.
- Track gaps in [CONTENT-BRIEF.md](CONTENT-BRIEF.md) and [ROADMAP.md](ROADMAP.md).
- Terms defined in [GLOSSARY.md](GLOSSARY.md).
- Stale planning docs live in `_archive/` — do not resurrect.
