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
├── 00-foundations/           [cicd-overview.md]
├── 01-source-control/        [git-branching-pull-requests.md]
├── 02-continuous-integration/ [continuous-integration.md]
├── 03-build-systems/          [build-systems.md]
├── 04-testing/                [testing-strategy.md]
├── 05-artifacts-and-packaging/ [artifact-management.md]
├── 06-ci-cd-pipelines/       [pipelines.md]
├── 07-continuous-delivery/   [continuous-delivery.md]
├── 08-continuous-deployment/ [continuous-deployment.md]
├── 09-environments-and-release/ [environments-release.md]
├── 10-deployment-strategies/ [deployment-strategies.md]
├── 11-security/               [cicd-security.md]
├── 13-observability-and-feedback/ [observability-feedback.md]
├── 14-reliability-and-recovery/ [rollback-recovery.md]
├── 16-labs/                   [01-first-pipeline → 08-jenkins-backup-restore]
├── 17-reference/               [command-cheatsheet.md]
└── 15-platforms-and-tools/
    ├── github-actions.md
    └── jenkins/              [12 files, see below]
```

## Jenkins Domain (Exists)

```text
15-platforms-and-tools/jenkins/
├── README.md                 domain index + concept→Jenkins map
├── jenkins-architecture.md
├── jenkins-setup.md
├── jenkins-pipelines.md
├── jenkins-groovy-cheatsheet.md
├── jenkins-agents.md
├── jenkins-credentials.md
├── jenkins-plugins.md
├── jenkins-webhooks.md
├── jenkins-security.md
├── jenkins-advanced.md
└── jenkins-troubleshooting.md
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
