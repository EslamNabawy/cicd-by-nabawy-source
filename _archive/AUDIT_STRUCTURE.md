# P1.1 Cross-Book Structure Audit

**Date:** 2026-09-14 · **Branch:** `levelup/ui-ux-content` · **Repo root:** `C:/Users/eslam/OneDrive/Desktop/CI CD/CI-CD`  
**Manifest:** `website/content/books.json` (42 books) · **Build script:** `website/scripts/build.py`  
**Scope:** For each book, resolve its source `.md` (git-tracked files under `CI-CD/` subfolders; `pdf/` holds built HTML). Three roadmap books have no `.md` source — they are HTML-only (`pdf/pdf-40/41/42`). Checked both `.md` and built PDF for those.  
**Method:** Regex heading detection on source `.md` (or fallback `pdf/*.html` when no `.md` exists).  
Definitions used — the actual editorial headings that encode the requested structure:

| Spec token | Detected heading (literal) | Meaning |
|---|---|---|
| **WHAT** | `## 1. What Is It?` | Book's core definition |
| **WHY** | `## 2. Why Does It Exist?` / `Why It Exists` | Motivation / problem it solves |
| **WHEN** | `## 3. Where Does It Fit?` | Placement in the lifecycle = *when* to apply (WHERE = WHEN in this library) |
| **HOW** | `## 4. How It Works` / `How Each Works` | Mechanics / walkthrough |
| **WHAT-CAN-FAIL** | `## *. Failure Modes` / `Failure Scenarios` | Failure catalogue + troubleshooting |

> `Interview Check` = any heading containing `Interview` (variants: `Interview / Exam Notes`, `Interview Notes`).  
> `Gotcha/Danger callout` = heading or callout containing `Gotcha` / `Danger` (spec literal: `<!-- icon: ... -->` count is separate; Danger callouts in this codebase are editorial sections, not `[!WARNING]` blockquotes — none of the 42 use that blockquote syntax).

---

## Evidence counts (whole library, n=42)

| Signal | Present | Absent | % present | Verdict |
|---|---|---:|---:|---|
| WHAT (`What Is It?`) | 18 | 24 | 43% | **Inconsistent** — only core concept books |
| WHY (`Why Does It Exist?`) | 9 | 33 | 21% | **Inconsistent** — only 7 of the 19 core + `github-actions`/`foundations` |
| WHEN (`Where Does It Fit?`) | 7 | 35 | 17% | **Inconsistent** — only 7 core books |
| HOW (`How It Works`) | 7 | 35 | 17% | **Inconsistent** — same 7 core books |
| WHAT-CAN-FAIL (`Failure Modes/Scenarios`) | 35 | 7 | 83% | **Consistent** — missing in 7 books only |
| Interview section | 22 | 20 | 52% | **Borderline consistent** — missing in all 8 labs, `cheatsheet`, `jenkins-domain`, `jenkins-setup`, `jenkins-agents/credentials/plugins/webhooks`, `jenkins-troubleshooting`, and the 3 roadmap books |
| Gotcha/Danger callout | 1 | 41 | 2% | **Not a library pattern** — only `groovy` (`## Sandbox Gotchas`) |

**Icon markers (`<!-- icon: ... -->`):** range 0–5, median 1. Four books have zero: `groovy` (0) and the three HTML-only roadmaps (0 by construction — icons are `<img src="assets/icons/...">` in built HTML, not `<!-- icon:` markers). Six books have >1 marker: `pipelines` (5), `github-actions` (3), `git-branching`/`jenkins-architecture`/`jenkins-setup`/`jenkins-pipelines` (2 each). 32/42 have exactly 1.

**Word counts (source `.md` words; pdf-only books = stripped HTML words):** range 222–2,049, mean ≈656, median ≈431. Shortest: `cheatsheet` (222) · Longest: `cicd-decision-guide` (2,049 pdf words). Core books average ≈640; labs average ≈345; Jenkins advanced books (pipelines/github-actions) are outliers at 1,597–1,656 words.

**PDF icon cross-check (built HTML `<img src="assets/icons/...">`):** roadmap pdfs do carry icons (jenkins-roadmap 9, github-actions-roadmap 14, decision-guide 8) — they just lack the `<!-- icon:` source marker because they have no `.md` source.

---

## Full table — 42 books

Legend: `Y` = present, `N` = absent. `WHAT/WHY/WHEN/HOW/FAIL` map to the headings above. `Interview` = Interview section. `Gotcha` = Gotcha/Danger callout. `Icons` = count of `<!-- icon: ... -->` markers (spec literal). `Words` = source `.md` split count (roadmaps = stripped HTML words). Source column gives the resolved file.

| # | ID | Title | PDF | Source file | WHAT | WHY | WHEN | HOW | FAIL | Interview | Gotcha | Icons | Words |
|---:|---|---|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|
| 01 | `foundations` | CI/CD Foundations | `pdf-01-foundations.html` | `00-foundations/cicd-overview.md` | Y | Y | Y | N | N | Y | N | 1 | 775 |
| 02 | `git-branching` | Git, Branching & Pull Requests | `pdf-02-git-branching-pull-requests.html` | `01-source-control/git-branching-pull-requests.md` | Y | Y | Y | Y | Y | Y | N | 2 | 767 |
| 03 | `pipelines` | CI/CD Pipelines | `pdf-03-pipelines.html` | `06-ci-cd-pipelines/pipelines.md` | Y | Y | Y | Y | Y | Y | N | 5 | 1363 |
| 04 | `artifacts` | Artifact Management | `pdf-04-artifact-management.html` | `05-artifacts-and-packaging/artifact-management.md` | Y | Y | Y | Y | Y | Y | N | 1 | 674 |
| 05 | `delivery` | Continuous Delivery | `pdf-05-continuous-delivery.html` | `07-continuous-delivery/continuous-delivery.md` | Y | Y | Y | Y | Y | Y | N | 1 | 680 |
| 06 | `strategies` | Deployment Strategies | `pdf-20-deployment-strategies.html` | `10-deployment-strategies/deployment-strategies.md` | Y | Y | Y | Y | Y | Y | N | 1 | 776 |
| 07 | `ci` | Continuous Integration | `pdf-21-continuous-integration.html` | `02-continuous-integration/continuous-integration.md` | Y | Y | N | N | Y | Y | N | 1 | 426 |
| 08 | `build` | Build Systems | `pdf-22-build-systems.html` | `03-build-systems/build-systems.md` | Y | N | N | N | Y | Y | N | 1 | 348 |
| 09 | `testing` | Testing Strategy | `pdf-23-testing-strategy.html` | `04-testing/testing-strategy.md` | Y | N | N | N | Y | Y | N | 1 | 388 |
| 10 | `deployment-auto` | Continuous Deployment | `pdf-24-continuous-deployment.html` | `08-continuous-deployment/continuous-deployment.md` | Y | N | N | N | Y | Y | N | 1 | 367 |
| 11 | `envs` | Environments & Release | `pdf-25-environments-release.html` | `09-environments-and-release/environments-release.md` | Y | N | N | N | Y | Y | N | 1 | 422 |
| 12 | `security` | CI/CD Security | `pdf-26-cicd-security.html` | `11-security/cicd-security.md` | Y | N | N | N | Y | Y | N | 1 | 431 |
| 13 | `rollback` | Rollback & Recovery | `pdf-27-rollback-recovery.html` | `14-reliability-and-recovery/rollback-recovery.md` | Y | N | N | N | Y | Y | N | 1 | 464 |
| 14 | `lab-01` | Lab 01: First Pipeline | `pdf-28-lab-first-pipeline.html` | `16-labs/01-first-pipeline.md` | N | N | N | N | Y | N | N | 1 | 360 |
| 15 | `lab-02` | Lab 02: Build & Test | `pdf-29-lab-build-test.html` | `16-labs/02-build-and-test.md` | N | N | N | N | Y | N | N | 1 | 338 |
| 16 | `lab-03` | Lab 03: Artifacts | `pdf-30-lab-artifacts.html` | `16-labs/03-artifacts.md` | N | N | N | N | Y | N | N | 1 | 333 |
| 17 | `lab-04` | Lab 04: Deployment | `pdf-31-lab-deployment.html` | `16-labs/04-deployment.md` | N | N | N | N | Y | N | N | 1 | 306 |
| 18 | `lab-05` | Lab 05: Rollback | `pdf-32-lab-rollback.html` | `16-labs/05-rollback.md` | N | N | N | N | Y | N | N | 1 | 372 |
| 19 | `lab-06` | Lab 06: Jenkins Live | `pdf-33-lab-jenkins-controller.html` | `16-labs/06-jenkins-controller.md` | N | N | N | N | Y | N | N | 1 | 356 |
| 20 | `lab-07` | Lab 07: Shared Library | `pdf-34-lab-shared-library.html` | `16-labs/07-jenkins-shared-library.md` | N | N | N | N | Y | N | N | 1 | 328 |
| 21 | `lab-08` | Lab 08: Backup & Restore | `pdf-35-lab-backup-restore.html` | `16-labs/08-jenkins-backup-restore.md` | N | N | N | N | Y | N | N | 1 | 360 |
| 22 | `cheatsheet` | Command Cheatsheet | `pdf-36-command-cheatsheet.html` | `17-reference/command-cheatsheet.md` | N | N | N | N | N | N | N | 1 | 222 |
| 23 | `gitlab` | GitLab CI | `pdf-37-gitlab-ci.html` | `15-platforms-and-tools/gitlab-ci.md` | Y | N | N | N | Y | Y | N | 1 | 540 |
| 24 | `argocd` | ArgoCD and GitOps | `pdf-38-argocd-gitops.html` | `15-platforms-and-tools/argocd-gitops.md` | Y | N | N | N | Y | Y | N | 1 | 459 |
| 25 | `iac` | IaC for Environments | `pdf-39-iac-environments.html` | `12-infrastructure-and-configuration/iac-environments.md` | Y | N | N | N | Y | Y | N | 1 | 416 |
| 26 | `observability` | Observability & Feedback | `pdf-06-observability-feedback.html` | `13-observability-and-feedback/observability-feedback.md` | Y | Y | Y | Y | Y | Y | N | 1 | 776 |
| 27 | `jenkins-domain` | Jenkins Domain | `pdf-07-jenkins-domain.html` | `15-platforms-and-tools/jenkins/README.md` | N | N | N | N | N | N | N | 1 | 392 |
| 28 | `jenkins-architecture` | Jenkins Architecture | `pdf-08-jenkins-architecture.html` | `15-platforms-and-tools/jenkins/jenkins-architecture.md` | Y | N | N | Y | Y | Y | N | 2 | 596 |
| 29 | `jenkins-setup` | Jenkins Setup | `pdf-09-jenkins-setup.html` | `15-platforms-and-tools/jenkins/jenkins-setup.md` | N | N | N | N | Y | N | N | 2 | 795 |
| 30 | `jenkins-pipelines` | Jenkins Pipelines | `pdf-10-jenkins-pipelines.html` | `15-platforms-and-tools/jenkins/jenkins-pipelines.md` | N | N | N | N | Y | Y | N | 2 | 1656 |
| 31 | `groovy` | Groovy Cheatsheet | `pdf-11-groovy-cheatsheet.html` | `15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md` | N | N | N | N | N | N | Y | 0 | 458 |
| 32 | `jenkins-agents` | Jenkins Agents | `pdf-12-jenkins-agents.html` | `15-platforms-and-tools/jenkins/jenkins-agents.md` | N | N | N | N | Y | N | N | 1 | 361 |
| 33 | `jenkins-credentials` | Jenkins Credentials | `pdf-13-jenkins-credentials.html` | `15-platforms-and-tools/jenkins/jenkins-credentials.md` | N | N | N | N | Y | N | N | 1 | 333 |
| 34 | `jenkins-plugins` | Jenkins Plugins | `pdf-14-jenkins-plugins.html` | `15-platforms-and-tools/jenkins/jenkins-plugins.md` | N | N | N | N | Y | N | N | 1 | 294 |
| 35 | `jenkins-webhooks` | Jenkins Webhooks | `pdf-15-jenkins-webhooks.html` | `15-platforms-and-tools/jenkins/jenkins-webhooks.md` | N | N | N | N | Y | N | N | 1 | 377 |
| 36 | `jenkins-security` | Jenkins Security | `pdf-16-jenkins-security.html` | `15-platforms-and-tools/jenkins/jenkins-security.md` | N | N | N | N | N | Y | N | 1 | 375 |
| 37 | `jenkins-advanced` | Jenkins Advanced | `pdf-17-jenkins-advanced.html` | `15-platforms-and-tools/jenkins/jenkins-advanced.md` | N | N | N | N | N | Y | N | 1 | 939 |
| 38 | `jenkins-troubleshooting` | Jenkins Troubleshooting | `pdf-18-jenkins-troubleshooting.html` | `15-platforms-and-tools/jenkins/jenkins-troubleshooting.md` | N | N | N | N | N | N | N | 1 | 439 |
| 39 | `github-actions` | GitHub Actions | `pdf-19-github-actions.html` | `15-platforms-and-tools/github-actions.md` | N | Y | N | N | Y | Y | N | 3 | 1597 |
| 40 | `jenkins-roadmap-2026` | Jenkins Roadmap 2026 | `pdf-40-jenkins-roadmap-2026.html` | `pdf/pdf-40-jenkins-roadmap-2026.html (no .md — HTML-only)` | N | N | N | N | Y | N | N | 0 | 1858 |
| 41 | `github-actions-roadmap-2026` | GitHub Actions Roadmap 2026 | `pdf-41-github-actions-roadmap-2026.html` | `pdf/pdf-41-github-actions-roadmap-2026.html (no .md — HTML-only)` | N | N | N | N | Y | N | N | 0 | 2008 |
| 42 | `cicd-decision-guide` | CI/CD Decision Guide: Jenkins vs GitHub Actions | `pdf-42-cicd-decision-guide.html` | `pdf/pdf-42-cicd-decision-guide.html (no .md — HTML-only)` | N | N | N | N | Y | N | N | 0 | 2049 |

> Detailed heading evidence per book is in the appendix at the bottom. Icon counts are literal `<!-- icon:` marker counts, verified by `grep`. Word counts via `wc -w` semantics (whitespace split).

---

## Gap checklist — every book missing a pattern others use consistently

> Rule applied: flag every book missing a signal that is **consistent** in its genre. Globally consistent = WHAT-CAN-FAIL (83%) and Interview (52%, borderline). Locally consistent = WHAT (95% of the 19 core concept books have it). Labs intentionally use a different schema (Objective/Steps/Failure Scenarios) so their WHAT/WHY/WHEN/HOW gaps are *by design* but still flagged for visibility. No fixes applied.

### A. WHAT-CAN-FAIL gaps (FAIL = N) — 7 books (the only FAIL misses — this is the most consistent signal)

- [ ] `foundations` (`00-foundations/cicd-overview.md`) — has `Core Concepts` / `Realistic Example` / `Common Misconceptions` but no dedicated `Failure Modes`/`What Can Fail` section. Words: 775.
- [ ] `groovy` (`15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md`) — cheatsheet, no Failure Modes (has `Sandbox Gotchas` as the failure-adjacent section). Words: 458, icons: 0.
- [ ] `jenkins-domain` (`15-platforms-and-tools/jenkins/README.md`) — domain map/overview, no Failure Modes. Words: 392.
- [ ] `jenkins-security` (`15-platforms-and-tools/jenkins/jenkins-security.md`) — no `Failure Modes` heading (has interview notes; security content implies failures but no catalogue). Words: 375.
- [ ] `jenkins-advanced` (`15-platforms-and-tools/jenkins/jenkins-advanced.md`) — no `Failure Modes` heading (6 feature sections + interview notes). Words: 939.
- [ ] `jenkins-troubleshooting` (`15-platforms-and-tools/jenkins/jenkins-troubleshooting.md`) — no `Failure Modes` heading — paradoxically, the entire book *is* troubleshooting (Triage Table / Build Log / Recovery) but does not use the canonical `Failure Modes` heading. Words: 439.
- [ ] `cheatsheet` (`17-reference/command-cheatsheet.md`) — reference, no Failure Modes (expected — but flagged for completeness). Words: 222.

### B. Interview section gaps (Interview = N) — 20 books

**Consistent in core concept books (100% of 19 core concept books that are not jenkins-advanced labs have it — so missing it elsewhere is a gap):**

- [ ] `lab-01` through `lab-08` (8 labs, `16-labs/0*.md`) — all have `Failure Scenarios` but zero Interview sections. Expected for hands-on labs, but flagged: labs are the only genre with 0% Interview coverage.
- [ ] `cheatsheet` (`17-reference/command-cheatsheet.md`) — no Interview section.
- [ ] `jenkins-domain` (`15-platforms-and-tools/jenkins/README.md`) — no Interview section.
- [ ] `jenkins-setup` (`15-platforms-and-tools/jenkins/jenkins-setup.md`) — has `Failure Modes` but no Interview Notes (unlike `jenkins-architecture`/`jenkins-pipelines` which do).
- [ ] `jenkins-agents` (`15-platforms-and-tools/jenkins/jenkins-agents.md`) — has `Failure Modes`, no Interview.
- [ ] `jenkins-credentials` (`15-platforms-and-tools/jenkins/jenkins-credentials.md`) — has `Failure Modes`, no Interview.
- [ ] `jenkins-plugins` (`15-platforms-and-tools/jenkins/jenkins-plugins.md`) — has `Failure Modes`, no Interview.
- [ ] `jenkins-webhooks` (`15-platforms-and-tools/jenkins/jenkins-webhooks.md`) — has `Failure Modes`, no Interview.
- [ ] `groovy` (`15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md`) — cheatsheet, no Interview.
- [ ] `jenkins-troubleshooting` (`15-platforms-and-tools/jenkins/jenkins-troubleshooting.md`) — no Interview section (only book in jenkins-advanced group without it besides the three above).
- [ ] `jenkins-roadmap-2026` (`pdf/pdf-40-jenkins-roadmap-2026.html`, no .md) — HTML-only, no Interview section.
- [ ] `github-actions-roadmap-2026` (`pdf/pdf-41-github-actions-roadmap-2026.html`, no .md) — HTML-only, no Interview section.
- [ ] `cicd-decision-guide` (`pdf/pdf-42-cicd-decision-guide.html`, no .md) — HTML-only, no Interview section.

### C. WHAT/WHY/WHEN/HOW gaps (the canonical 4 before Failure)

> These four are **not globally consistent** (WHAT 43%, WHY 21%, WHEN 17%, HOW 17%) — but they *are* locally consistent inside the 19-book "core concept" genre (WHAT 95%, WHY 47%, WHEN 37%, HOW 37%). Flagging by genre:

**Core concept books that break the genre pattern:**

- [ ] `foundations` — missing HOW (`How It Works`) and FAIL (see A). Has WHAT/WHY/WHEN. Heading `## 4. Core Concepts` replaces the usual `How It Works`.
- [ ] `strategies` — fully canonical (WHAT/WHY/WHEN/HOW/FAIL all Y) — actually *not* a gap; variant heading `How Each Works` correctly detected as HOW.
- [ ] `ci` (`02-continuous-integration/continuous-integration.md`) — missing WHEN and HOW. Headings are `PR Gates & Merge Queues` / `Trunk Discipline` instead of `Where Does It Fit?` / `How It Works`.
- [ ] `build` (`03-build-systems/build-systems.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL). Headings: `Hermetic Builds` / `Caching Done Right` / `Tool Notes`.
- [ ] `testing` (`04-testing/testing-strategy.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL). Headings: `The Pyramid in Pipelines` / `Placement Rules` / `Flaky Policy`.
- [ ] `deployment-auto` (`08-continuous-deployment/continuous-deployment.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL + Interview). Headings: `Prerequisites (All Non-Negotiable)`.
- [ ] `envs` (`09-environments-and-release/environments-release.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL).
- [ ] `security` (`11-security/cicd-security.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL). Headings: `Secrets Discipline` / `Signing, SBOM & Provenance`.
- [ ] `rollback` (`14-reliability-and-recovery/rollback-recovery.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL).
- [ ] `iac` (`12-infrastructure-and-configuration/iac-environments.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL).
- [ ] `gitlab` (`15-platforms-and-tools/gitlab-ci.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL) — has `Pipeline Anatomy` / `Runners & Tags` instead.
- [ ] `argocd` (`15-platforms-and-tools/argocd-gitops.md`) — missing WHY/WHEN/HOW (only WHAT + FAIL) — headings `Push vs Pull` / `Core Objects`.
- [ ] `github-actions` (`15-platforms-and-tools/github-actions.md`) — missing WHAT/WHEN/HOW (only WHY + FAIL + Interview). Starts with `Concept → Actions Map` instead of `What Is It?`, no `Where Does It Fit?` / `How It Works` canonical heading.

**Jenkins books (none are canonical — by design they use topology/operation headings, not WHAT/WHY/WHEN/HOW):**

- [ ] All 10 Jenkins books except `jenkins-architecture` (which has WHAT+HOW+FAIL+Interview) lack WHAT/WHY/WHEN/HOW. This is genre-consistent for Jenkins (they are *implementation* books, not concept books) — flagged here as informational, not as defects. Detail: `jenkins-domain` (0/5), `jenkins-setup` (0/5 + FAIL Y), `jenkins-pipelines` (0/5 + FAIL Y), `groovy` (0/5), `jenkins-agents/credentials/plugins/webhooks` (0/5 + FAIL Y), `jenkins-security` (0/5), `jenkins-advanced` (0/5), `jenkins-troubleshooting` (0/5).

**Labs & Reference (different schema — Objective/Steps):**

- [ ] All 8 labs + `cheatsheet` — 0/5 on WHAT/WHY/WHEN/HOW by construction. Their structure is `Objective → Prerequisites → Architecture → Setup → Step N → Verification → Failure Scenarios → Cleanup`. Not defects, but recorded as divergent from the canonical 5.

**Roadmap books (HTML-only, editorial layout — not concept books):**

- [ ] `jenkins-roadmap-2026`, `github-actions-roadmap-2026`, `cicd-decision-guide` — 0/5 on WHAT/WHY/WHEN/HOW (they use horizon/product-theme headings: `Release Cadence`, `Pipeline Authoring`, `Optimization Vectors`, etc.). No Interview sections. Icons present in built HTML (9/14/8 `<img>`), but zero `<!-- icon:` markers.

### D. Icon marker gaps (spec literal: `<!-- icon: ... -->`)

- [ ] `groovy` — 0 markers (only book with a `.md` source that has zero). All other `.md` sources have ≥1. For a Jenkins book with `Sandbox Gotchas` callout, the absence of an icon marker is the sole icon gap among `.md` sources.
- [ ] `jenkins-roadmap-2026` — 0 markers (no `.md`, HTML-only — 9 built `<img>` icons in pdf).
- [ ] `github-actions-roadmap-2026` — 0 markers (no `.md` — 14 built `<img>` icons).
- [ ] `cicd-decision-guide` — 0 markers (no `.md` — 8 built `<img>` icons).

> If the audit counted built-HTML `<img src="assets/icons/...">` instead of source `<!-- icon:` markers, roadmaps would pass (they are icon-rich). Per the task's literal `<!-- icon: ... -->` criterion they are gaps.

### E. Word-count outliers (not a pass/fail, but flagged for review)

- [ ] Shortest: `cheatsheet` (222 words) — reference, expected to be terse.
- [ ] Labs cluster: 306–372 words (all 8 labs under 380) — deliberately concise, but notably shorter than core books.
- [ ] Thin concept books: `build` (348), `deployment-auto` (367), `testing` (388), `jenkins-agents` (361), `jenkins-credentials` (333), `jenkins-plugins` (294), `jenkins-webhooks` (377), `jenkins-security` (375), `jenkins-domain` (392) — all under 400 words, flagged for potential under-coverage vs. `pipelines` (1,363) / `github-actions` (1,597) / `jenkins-pipelines` (1,656) in same library.
- [ ] Heavyweight books: `jenkins-pipelines` (1,656), `github-actions` (1,597), `pipelines` (1,363) — 3× the median; `cicd-decision-guide` (2,049), `github-actions-roadmap-2026` (2,008), `jenkins-roadmap-2026` (1,858) — roadmap pdfs are longer because they are built HTML stripped word counts (include nav/CSS residue; true prose is slightly less).

### F. Gotcha/Danger callout — absent as a library pattern (41/42 missing)

- [ ] Only `groovy` has a Gotcha/Danger section (`## Sandbox Gotchas`). No book uses a `> [!WARNING]` / `> [!DANGER]` / `> **Danger**` / `> **Gotcha**` blockquote callout. If this callout is intended as a consistent safety pattern, 41 books are missing it.
- [ ] Incidental `WARNING` strings in `strategies` (feature flag note) and `jenkins-plugins` (Warnings NG table row) are **not** Danger callouts — discounted.

---

## Method & limits

- Source resolution: `website/content/books.json` → `pdf/<file>` → git-tracked `.md` via CONTENT_MAP / TOPIC_INDEX / git ls-files. Mapping verified exhaustively (39 `.md` + 3 pdf-only roadmaps). Full mapping in appendix.
- Word count: `len(text.split())` on raw `.md` (or stripped HTML for pdf-only). Includes code fences and tables — comparable across books but not prose-only.
- Icon count: `len(re.findall(r"<!--\s*icon\s*:", text))` — spec literal. Does **not** count built-Html `<img src="assets/icons/...">` (reported separately as cross-check).
- Structural detection is heading-aware: `What Is It?`, `Why Does It Exist?`, `Where Does It Fit?`, `How It Works`/`How Each Works`, `Failure Modes`/`Failure Scenarios`. Variants like `Common Misconceptions`, `Best Practices`, `Realistic Example` are not counted toward the 5.
- No fixes applied — report only.

---

## Appendix 1 — Source mapping (42 books → resolved source)

| # | ID | `website/content/books.json` `file` | Resolved source (tracked) | Type |
|---:|---|---|---|---|
| 01 | `foundations` | `pdf-01-foundations.html` | `00-foundations/cicd-overview.md` | md |
| 02 | `git-branching` | `pdf-02-git-branching-pull-requests.html` | `01-source-control/git-branching-pull-requests.md` | md |
| 03 | `pipelines` | `pdf-03-pipelines.html` | `06-ci-cd-pipelines/pipelines.md` | md |
| 04 | `artifacts` | `pdf-04-artifact-management.html` | `05-artifacts-and-packaging/artifact-management.md` | md |
| 05 | `delivery` | `pdf-05-continuous-delivery.html` | `07-continuous-delivery/continuous-delivery.md` | md |
| 06 | `strategies` | `pdf-20-deployment-strategies.html` | `10-deployment-strategies/deployment-strategies.md` | md |
| 07 | `ci` | `pdf-21-continuous-integration.html` | `02-continuous-integration/continuous-integration.md` | md |
| 08 | `build` | `pdf-22-build-systems.html` | `03-build-systems/build-systems.md` | md |
| 09 | `testing` | `pdf-23-testing-strategy.html` | `04-testing/testing-strategy.md` | md |
| 10 | `deployment-auto` | `pdf-24-continuous-deployment.html` | `08-continuous-deployment/continuous-deployment.md` | md |
| 11 | `envs` | `pdf-25-environments-release.html` | `09-environments-and-release/environments-release.md` | md |
| 12 | `security` | `pdf-26-cicd-security.html` | `11-security/cicd-security.md` | md |
| 13 | `rollback` | `pdf-27-rollback-recovery.html` | `14-reliability-and-recovery/rollback-recovery.md` | md |
| 14 | `lab-01` | `pdf-28-lab-first-pipeline.html` | `16-labs/01-first-pipeline.md` | md |
| 15 | `lab-02` | `pdf-29-lab-build-test.html` | `16-labs/02-build-and-test.md` | md |
| 16 | `lab-03` | `pdf-30-lab-artifacts.html` | `16-labs/03-artifacts.md` | md |
| 17 | `lab-04` | `pdf-31-lab-deployment.html` | `16-labs/04-deployment.md` | md |
| 18 | `lab-05` | `pdf-32-lab-rollback.html` | `16-labs/05-rollback.md` | md |
| 19 | `lab-06` | `pdf-33-lab-jenkins-controller.html` | `16-labs/06-jenkins-controller.md` | md |
| 20 | `lab-07` | `pdf-34-lab-shared-library.html` | `16-labs/07-jenkins-shared-library.md` | md |
| 21 | `lab-08` | `pdf-35-lab-backup-restore.html` | `16-labs/08-jenkins-backup-restore.md` | md |
| 22 | `cheatsheet` | `pdf-36-command-cheatsheet.html` | `17-reference/command-cheatsheet.md` | md |
| 23 | `gitlab` | `pdf-37-gitlab-ci.html` | `15-platforms-and-tools/gitlab-ci.md` | md |
| 24 | `argocd` | `pdf-38-argocd-gitops.html` | `15-platforms-and-tools/argocd-gitops.md` | md |
| 25 | `iac` | `pdf-39-iac-environments.html` | `12-infrastructure-and-configuration/iac-environments.md` | md |
| 26 | `observability` | `pdf-06-observability-feedback.html` | `13-observability-and-feedback/observability-feedback.md` | md |
| 27 | `jenkins-domain` | `pdf-07-jenkins-domain.html` | `15-platforms-and-tools/jenkins/README.md` | md |
| 28 | `jenkins-architecture` | `pdf-08-jenkins-architecture.html` | `15-platforms-and-tools/jenkins/jenkins-architecture.md` | md |
| 29 | `jenkins-setup` | `pdf-09-jenkins-setup.html` | `15-platforms-and-tools/jenkins/jenkins-setup.md` | md |
| 30 | `jenkins-pipelines` | `pdf-10-jenkins-pipelines.html` | `15-platforms-and-tools/jenkins/jenkins-pipelines.md` | md |
| 31 | `groovy` | `pdf-11-groovy-cheatsheet.html` | `15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md` | md |
| 32 | `jenkins-agents` | `pdf-12-jenkins-agents.html` | `15-platforms-and-tools/jenkins/jenkins-agents.md` | md |
| 33 | `jenkins-credentials` | `pdf-13-jenkins-credentials.html` | `15-platforms-and-tools/jenkins/jenkins-credentials.md` | md |
| 34 | `jenkins-plugins` | `pdf-14-jenkins-plugins.html` | `15-platforms-and-tools/jenkins/jenkins-plugins.md` | md |
| 35 | `jenkins-webhooks` | `pdf-15-jenkins-webhooks.html` | `15-platforms-and-tools/jenkins/jenkins-webhooks.md` | md |
| 36 | `jenkins-security` | `pdf-16-jenkins-security.html` | `15-platforms-and-tools/jenkins/jenkins-security.md` | md |
| 37 | `jenkins-advanced` | `pdf-17-jenkins-advanced.html` | `15-platforms-and-tools/jenkins/jenkins-advanced.md` | md |
| 38 | `jenkins-troubleshooting` | `pdf-18-jenkins-troubleshooting.html` | `15-platforms-and-tools/jenkins/jenkins-troubleshooting.md` | md |
| 39 | `github-actions` | `pdf-19-github-actions.html` | `15-platforms-and-tools/github-actions.md` | md |
| 40 | `jenkins-roadmap-2026` | `pdf-40-jenkins-roadmap-2026.html` | `pdf/pdf-40-jenkins-roadmap-2026.html` | **pdf-only** (no `.md`) |
| 41 | `github-actions-roadmap-2026` | `pdf-41-github-actions-roadmap-2026.html` | `pdf/pdf-41-github-actions-roadmap-2026.html` | **pdf-only** (no `.md`) |
| 42 | `cicd-decision-guide` | `pdf-42-cicd-decision-guide.html` | `pdf/pdf-42-cicd-decision-guide.html` | **pdf-only** (no `.md`) |

---

## Appendix 2 — Heading evidence (sample, per book)

> Full headings dump — proves Y/N assignments. Headings taken from `grep -E "^#{1,6}\s"` on each source.

| ID | Headings (truncated) |
|---|---|
| `foundations` | CI/CD Overview; 1. What Is It?; 2. Why Does It Exist?; What Happens Without CI/CD?; 3. Where Does It Fit?; 4. Core Concepts; 5. Realistic Example; 6. Common Misconceptions; 7. Interview / Exam Notes; Related Topics |
| `git-branching` | Git, Branching & Pull Requests; 1. What Is It?; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How It Works; 5. Commands / Configuration; GitHub Actions trigger: run CI on every PR + every push to m; GitLab equivalent; |
| `pipelines` | CI/CD Pipelines; 1. What Is It?; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How It Works; 5. Example (GitHub Actions); # - uses: gitleaks/gitleaks-action@v2  # secret scan; 6. The Three Verification Stages; Buildin |
| `artifacts` | Artifact Management; 1. What Is It?; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How It Works; 5. Commands / Configuration; 6. Versioning; Versioning Schemes; 7. Failure Modes; 8. Best Practices; Signing, SBOM & Pro |
| `delivery` | Continuous Delivery; 1. What Is It?; Delivery vs Deployment; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How It Works; 5. Example; Conceptual CD flow (platform syntax varies); 6. Staging vs Production; 7. Failure Mo |
| `strategies` | Deployment Strategies; 1. What Is It?; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How Each Works; 5. Choosing; 6. Failure Modes; 7. Best Practices; 8. Common Misconceptions; 9. Interview / Exam Notes; Related Topic |
| `ci` | Continuous Integration; 1. What Is It?; 2. Why Does It Exist?; 3. PR Gates & Merge Queues; 4. Trunk Discipline; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `build` | Build Systems; 1. What Is It?; 2. Hermetic Builds; 3. Caching Done Right; 4. Tool Notes; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `testing` | Testing Strategy; 1. What Is It?; 2. The Pyramid in Pipelines; 3. Placement Rules; 4. Flaky Policy; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `deployment-auto` | Continuous Deployment; 1. What Is It?; 2. Prerequisites (All Non-Negotiable); 3. Failure Modes; 4. Delivery vs Deployment: When Each; 5. Interview Notes; Related Topics |
| `envs` | Environments & Release; 1. What Is It?; 2. Environment Topology; 3. Config vs Code; 4. Release Trains & Promotion Paths; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `security` | CI/CD Security; 1. What Is It?; 2. Secrets Discipline; 3. Signing, SBOM & Provenance; 4. Least Privilege Everywhere; 5. Supply-Chain Gates; 6. Failure Modes; 7. Interview Notes; Related Topics |
| `rollback` | Rollback & Recovery; 1. What Is It?; 2. Rollback per Strategy; 3. Rollback vs Forward-Fix Decision; 4. Recovery Drills (MTTR Practice); 5. Postmortems That Prevent Recurrence; 6. Failure Modes; 7. Interview Notes; Relate |
| `lab-01` | Lab 01 — First Pipeline; Objective; Prerequisites; Architecture; Setup; Step 1 — Add the workflow; Execute; Expected Result; Why; Step 2 — Require the check; Execute; Expected Result; Why; Verification; Failure Scenarios |
| `lab-02` | Lab 02 — Build and Test; Objective; Prerequisites; Architecture; Setup; Step 1 — Split and cache; Execute; Expected Result; Why; Step 2 — Prove hermeticity; Execute; Expected Result; Why; Verification; Failure Scenarios; |
| `lab-03` | Lab 03 — Artifacts; Objective; Prerequisites; Architecture; Setup; Step 1 — Build once, tag SHA; Execute; Expected Result; Why; Step 2 — Attach SBOM; Execute; Expected Result; Why; Verification; Failure Scenarios; Cleanu |
| `lab-04` | Lab 04 — Deployment; Objective; Prerequisites; Architecture; Setup; Step 1 — Staging auto-deploys; Execute; Expected Result; Why; Step 2 — Production needs a human; Execute; Expected Result; Why; Verification; Failure Sc |
| `lab-05` | Lab 05 — Rollback; Objective; Prerequisites; Architecture; Setup; Step 1 — Cause the incident; Execute; Expected Result; Why; Step 2 — Roll back, don't rebuild; Execute; Expected Result; Why; Step 3 — Postmortem with tee |
| `lab-06` | Lab 06 — Jenkins Controller & First Pipeline; Objective; Prerequisites; Architecture; Setup; docker-compose.yml: jenkins/jenkins:lts + inbound agent join; Step 1 — Connect the agent; Execute; Expected Result; Why; Step 2 |
| `lab-07` | Lab 07 — Jenkins Shared Library; Objective; Prerequisites; Architecture; Setup; Step 1 — Register the library; Execute; Expected Result; Why; Step 2 — Consume from two pipelines; Execute; Expected Result; Why; Verificati |
| `lab-08` | Lab 08 — Jenkins Backup & Restore; Objective; Prerequisites; Architecture; Setup; Step 1 — Back up; Execute; Expected Result; Why; Step 2 — Destroy and restore; Execute; Expected Result; Why; Verification; Failure Scenar |
| `cheatsheet` | Command Cheatsheet; Git; npm / Builds; Docker / GHCR; Jenkins (Compose lab); Jenkins backup; GitHub Actions snippets; Related Topics |
| `gitlab` | GitLab CI; 1. What Is It?; 2. Pipeline Anatomy (GitLab Vocabulary); 3. Runners & Tags; 4. Environments, Review Apps & Merge Trains; 5. GitLab vs the Sisters; 6. Failure Modes; 7. Interview Notes; Related Topics |
| `argocd` | ArgoCD & GitOps; 1. What Is It?; 2. Push vs Pull; 3. Core Objects; 4. Where It Fits; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `iac` | IaC for Environments; 1. What Is It?; 2. Structure That Scales; 3. IaC in the Pipeline; 4. Preview Environments, Automated; 5. Failure Modes; 6. Interview Notes; Related Topics |
| `observability` | Observability & Feedback; 1. What Is It?; 2. Why Does It Exist?; 3. Where Does It Fit?; 4. How It Works; 5. Example; 6. Failure Modes; SLI / SLO / Alerting; 7. Best Practices; DORA Metrics (What Good Looks Like); 8. Inte |
| `jenkins-domain` | Jenkins; Concept → Jenkins Map; Why Jenkins?; Reading Order; The Golden Rule; Jenkins vs GitHub Actions |
| `jenkins-architecture` | Jenkins Architecture; 1. What Is It?; 2. Diagram; 3. Key Directories (`JENKINS_HOME`); 4. Sizing Rules; 5. Jenkins in Docker: How It Works; 6. Failure Modes; 7. Interview Notes; Related Topics |
| `jenkins-setup` | Jenkins Setup; 1. Recommended Install (Docker); 2. Alternatives; 3. Windows vs WSL2: Where to Run Jenkins; 4. First Pipeline Job (Smoke Test); 5. Run & Use: Step by Step; Step 1 — Run the controller; Step 2 — Unlock; Ste |
| `jenkins-pipelines` | Jenkins Pipelines; 1. Concept → Jenkins Mapping; 2. Declarative vs Scripted; The Language: Groovy; 3. Canonical Jenkinsfile; 4. Multibranch Pipelines; 5. Failure Modes; 6. CI/CD with Jenkins in Docker; Docker-in-Docker ( |
| `groovy` | Groovy Cheatsheet (Jenkins Subset); Variables & Strings; Collections; Conditionals; Loops & Dynamic Stages (Scripted); Functions; Maps (Options, Config); Safe Navigation & Elvis (Null-Proof Pipelines); Jenkinsfile Idioms |
| `jenkins-agents` | Jenkins Agents; 1. Types; 2. Labels & Executors; 3. Minimal Docker-Agent Pipeline; 4. Connection Methods; 5. Failure Modes; Related Topics |
| `jenkins-credentials` | Jenkins Credentials; 1. Kinds & Scopes; 2. Usage (Bindings); 3. Rules; 4. Failure Modes; Related Topics |
| `jenkins-plugins` | Jenkins Plugins; 1. Essential Plugin Set; 2. Management Rules; plugins.txt (pinned, version-controlled); 3. Failure Modes; Related Topics |
| `jenkins-webhooks` | Jenkins Webhooks & Triggers; 1. Trigger Options; 2. GitHub Webhook Setup; 3. Multibranch = PR Gates Done Right; 4. Failure Modes; Related Topics |
| `jenkins-security` | Jenkins Security; 1. Authentication & Authorization; 2. Agent-to-Controller Rules; 3. Secrets Hygiene; 4. Update Discipline; 5. Interview Notes; Related Topics |
| `jenkins-advanced` | Jenkins Advanced; 1. Shared Libraries (Don't Repeat Yourself); 2. Parallel & Matrix Execution; 3. Configuration as Code (JCasC); jenkins.yaml (values redacted; secrets via Vault/credentials; 4. Backup & Restore; 5. Scrip |
| `jenkins-troubleshooting` | Jenkins Troubleshooting; 1. Triage Table; 2. Reading a Build Log; 3. Groovy Sandbox Notes; 4. Recovery; Related Topics |
| `github-actions` | GitHub Actions; 1. Concept → Actions Map; 2. Why It Exists; 3. Canonical Workflow (CI: Build → Test → Scan); 4. CD: Staging Auto, Production Gated; 5. Core Mechanics; Runners; ARC Scale Set (Self-Hosted That Scales); arc |
| `jenkins-roadmap-2026` | JENKINSROADMAP 2026; Orientation; 01 / Release Cadence — Current Model; 02 / How Horizons Work; READING RULE; Product Themes (pdf-only) |
| `github-actions-roadmap-2026` | GITHUB ACTIONSSECURITY ROADMAP 2026; Context; 01 / Incidents That Drove the Roadmap; THE PATTERN; 02 / Roadmap Pillars; Pillars A &amp; B (pdf-only) |
| `cicd-decision-guide` | CI/CDDECISION GUIDE; Orientation; 01 / Optimization Vectors; 02 / Governance Contrast; Side-by-Side; 03 / The Two Roadmaps — Full Dimension Table (pdf-only) |

---

## Appendix 3 — Counts for reviewers

- Total books audited: **42** (`website/content/books.json` — verified count matches table rows).
- Source `.md` found for: **39** books. **3** are HTML-only (no `.md`; audited via `pdf/*.html`).
- `<!-- icon: ... -->` total markers across 39 `.md` sources: **48** (verified `grep -R "<!-- icon:" --count`). Roadmap pdfs carry 31 additional `<img src="assets/icons/...">` in built HTML.
- Word-count file list available on request (`wc -w` on each source; this report uses `len(text.split())` — identical semantics).

---

*No files were modified. This is a report only. Re-run: `git ls-files | grep \.md` and `grep -R "<!-- icon:"` to re-verify icon counts; `grep -E "^#{2,6}\s" <file>` to re-verify headings.*
