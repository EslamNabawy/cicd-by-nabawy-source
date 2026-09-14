# Content Completeness Audit

Audit date: 2026-09-14. The current `books.json` contains 48 books, not the
39 stated by the orchestration prompt. Audit compares rendered PDF HTML bodies,
heading counts, plain-text depth, and the canonical root docs.

## Concrete gaps

| Book ID | Section / scope | Gap type | Evidence |
|---|---|---|---|
| `build` | Entire book | missing entirely | `pdf-22-build-systems.html`: 5,072 bytes, no `<body>`, 0 headings, 0 body text. |
| `testing` | Entire book | missing entirely | `pdf-23-testing-strategy.html`: 4,882 bytes, no `<body>`, 0 headings, 0 body text. |
| `deployment-auto` | Entire book | missing entirely | `pdf-24-continuous-deployment.html`: 4,962 bytes, no `<body>`, 0 headings, 0 body text. |
| `envs` | Entire book | missing entirely | `pdf-25-environments-release.html`: 4,691 bytes, no `<body>`, 0 headings, 0 body text. |
| `security` | Entire book | missing entirely | `pdf-26-cicd-security.html`: 4,955 bytes, no `<body>`, 0 headings, 0 body text. |
| `rollback` | Entire book | missing entirely | `pdf-27-rollback-recovery.html`: 4,885 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-01` | First Pipeline exercise | missing entirely | `pdf-28-lab-first-pipeline.html`: 4,405 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-02` | Build & Test exercise | missing entirely | `pdf-29-lab-build-test.html`: 4,403 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-03` | Artifacts exercise | missing entirely | `pdf-30-lab-artifacts.html`: 4,398 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-04` | Deployment exercise | missing entirely | `pdf-31-lab-deployment.html`: 4,399 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-05` | Rollback exercise | missing entirely | `pdf-32-lab-rollback.html`: 4,293 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-06` | Jenkins Live exercise | missing entirely | `pdf-33-lab-jenkins-controller.html`: 4,407 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-07` | Shared Library exercise | missing entirely | `pdf-34-lab-shared-library.html`: 4,403 bytes, no `<body>`, 0 headings, 0 body text. |
| `lab-08` | Backup & Restore exercise | missing entirely | `pdf-35-lab-backup-restore.html`: 4,405 bytes, no `<body>`, 0 headings, 0 body text. |
| `cheatsheet` | Entire reference book | missing entirely | `pdf-36-command-cheatsheet.html`: 4,068 bytes, no `<body>`, 0 headings, 0 body text. |
| `gitlab` | Entire platform book | missing entirely | `pdf-37-gitlab-ci.html`: 4,885 bytes, no `<body>`, 0 headings, 0 body text. |
| `argocd` | Entire platform book | missing entirely | `pdf-38-argocd-gitops.html`: 4,887 bytes, no `<body>`, 0 headings, 0 body text. |
| `iac` | Entire platform book | missing entirely | `pdf-39-iac-environments.html`: 4,688 bytes, no `<body>`, 0 headings, 0 body text. |

## Thin but non-empty books

`strategies`, `ci`, and several Jenkins core books contain bodies, but their
plain-text depth is about 1.9k–2.3k characters, substantially below the newer
Jenkins Labs books at roughly 11.6k–25.2k characters. They should be reviewed
for WHAT/WHY/WHEN/HOW/WHAT-CAN-FAIL, Interview Check, and Gotcha coverage after
the missing-body books are restored.

## Source-map observations

`TOPIC_INDEX.md`, `CONTENT_MAP.md`, and `ROADMAP.md` describe the missing
topics as real curriculum areas, so these are structural/content omissions,
not intentionally empty shells. Writing the six core books, eight original
labs, and three platform/reference books is a dedicated content pass; no
placeholder content should be generated during the level-up execution.

