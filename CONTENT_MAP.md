# Content Map

> Full intended architecture: what exists, what is planned, and how it becomes PDFs + website. Empty/planned folders are NOT created on disk until content justifies them — this map holds their place.

## On Disk (Exists)

```text
CI-CD/
├── README.md
├── ROADMAP.md
├── DOCUMENTATION_RULES.md
├── TOPIC_INDEX.md
├── CONTENT_MAP.md          ← this file
├── GLOSSARY.md
├── PDF_BUILD_SPEC.md       ← publication spec (drives all 36 PDFs)
├── WEBSITE_BUILD_SPEC.md   ← website spec (drives website/dist)
├── ICON_ASSET_SPEC.md      ← icon discovery + asset rules (live: governs every PDF/website build)
├── CONTENT_CONNECTIVITY_PROMPT.md ← handoff-rewrite prompt (applied across all 19 content files)
├── 00-foundations/           [start-here-merged.md ← cicd-overview + git-branching + CI]
├── 06-ci-cd-pipelines/       [pipelines-build-test.md ← pipelines + build-systems + testing]
├── 05-artifacts-and-packaging/ [artifact-management.md — standalone]
├── 07-continuous-delivery/   [delivery-envs-iac.md ← delivery + deployment + envs + iac]
├── 10-deployment-strategies/ [deployment-strategies.md — standalone]
├── 13-observability-and-feedback/ [observe-recover-secure.md ← observability + rollback + security]
├── 16-labs/                   [core-labs-handbook.md ← 01-first-pipeline → 08-jenkins-backup-restore]
├── jenkins labs/              [JENKINS_LABS_HANDBOOK.md ← 5 lab sources]
├── 17-reference/               [command-cheatsheet.md — standalone]
└── 15-platforms-and-tools/
    ├── github-actions.md     — standalone
    ├── gitlab-argocd.md      ← gitlab-ci + argocd-gitops
    └── jenkins/              [jenkins-core-merged.md (5) + jenkins-advanced-ops.md (7), see below]
> Member sources (pre-merge files) remain on disk as merge inputs. Merged
> files are canonical for website (`books.json`) and reader (`MD_MAP`).
```

## Jenkins Domain (Merged 2026-09-17 — 12 files → 2 handbooks)

```text
15-platforms-and-tools/jenkins/
├── jenkins-core-merged.md    ← README + architecture + setup + pipelines + agents
└── jenkins-advanced-ops.md   ← groovy + credentials + plugins + webhooks + security + advanced + troubleshooting
(member sources retained on disk as merge inputs)
```

## Planned (Not Yet on Disk)

```text
└── (nothing — all planned domains are on disk)
```

## PDF Series Mapping

```text
PDF 01 — CI/CD Foundations            ← 00
PDF 02 — Continuous Integration       ← 01 + 02
PDF 03 — Build + Testing + Artifacts  ← 03 + 04 + 05
PDF 04 — CI/CD Pipelines              ← 06
PDF 05 — Continuous Delivery & Deployment ← 07 + 08 + 09 + 10
PDF 06 — Jenkins                      ← 15/jenkins (core: architecture, setup, pipelines, agents)
PDF 07 — Jenkins Advanced             ← 15/jenkins (credentials, plugins, webhooks, security, troubleshooting)
PDF 08 — CI/CD Labs                   ← 16
```

## Series Edition (Built — `pdf/series/`, generator `scripts/build_series.py`)

```text
S01 Foundations              ← pdf-01 (12p)
S02 Continuous Integration   ← pdf-02 + pdf-21 (11p)
S03 Build, Test & Artifacts  ← pdf-22 + pdf-23 + pdf-04 (14p)
S04 Pipelines                ← pdf-03 (8p)
S05 Delivery & Deployment    ← pdf-05 + pdf-24 + pdf-25 + pdf-20 + pdf-27 + pdf-06 (28p)
S06 Jenkins Core             ← pdf-07 + pdf-08 + pdf-09 + pdf-10 + pdf-12 (22p)
S07 Jenkins Advanced         ← pdf-11 + pdf-13 + pdf-14 + pdf-15 + pdf-16 + pdf-17 + pdf-18 + pdf-26 (33p)
S08 Labs                     ← pdf-28…pdf-36 (29p)
S09 GitHub Actions           ← pdf-19 (7p)
```

## Website Mapping

Same Markdown source; routes mirror the tree (`/platforms/jenkins/pipelines` ← `15-platforms-and-tools/jenkins/jenkins-pipelines.md`). PDF order must never dictate filenames or hierarchy.
