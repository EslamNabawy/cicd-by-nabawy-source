# Content Analysis — "Continuous Delivery" (Humble & Farley) vs. Site Content

Source: local PDF extract (`Continuous Delivery Reliable Software Releases Through Build, Test And
Deployment Automation.pdf`, ~194k words, read in full via three parallel passes over Parts I–III).
Site state at analysis time: 44 books (the prompt's "48" predates the four lab merges), 9 learning paths.
All notes below are paraphrased; no sentences from the book are reproduced.

## Application status (execution pass, 2026-09-15)

- Phase 1 (P0): report contained no P0 items — nothing to fix.
- Phase 2 (P1) applied in `41dbb4b`: data-migration section in `14-reliability-and-recovery`
  (+ interview Q), migration bullets in `10-deployment-strategies` (.md + `pdf-20` callouts for
  migration sequencing and branch by abstraction), capacity-testing section in `04-testing`.
- Phase 3 (P2) applied in `2466c21`: glossary CD split; deployment-auto trunk wording softened;
  test doubles + executable acceptance specs in `04-testing`; preflight/build-master/ratcheting in
  `02-continuous-integration` (.md + `pdf-21` callout); release checklist + injection timing in
  `09-environments-and-release`; integration-pipeline callout in `pdf-03`; walking-skeleton phrase in
  labs path desc; ROADMAP rows updated. Build + `qc-check` ALL GREEN after each phase; 0 dead anchors.
- Judgment calls: full-manual books (`pdf-03/20/21`) got unnumbered `.kv` callout mirrors instead of new
  numbered sections, so no section renumbering and no TOC churn; `.md` edits carry the full prose.
- Governance appendix: resolved without a new book — scoped at ~30 lines (maturity ladder, pipeline-as-evidence, change control, risk one-liner, value-stream mapping), closest fit is `11-security/cicd-security.md` (approvals, audit trails, separation of duties already live there), added as section 6. A standalone book would be one thin section; not recommended.
- Skipped: everything under "Not recommended for action," per instructions.

## Summary

The site holds up well against this source. Its core spine — build once and promote the same digest,
the deploy/release/promote vocabulary split, stop-the-line red-main discipline, trunk-plus-flags,
expand-contract migrations, hermetic builds with lockfiles, the test pyramid with contract tests and a
flaky-quarantine policy, progressive delivery with kill criteria — matches the book's central arguments,
and in several places the site is deliberately more current than the book (merge queues, SBOM/signing,
policy gates, error budgets, ephemeral preview environments). Where the site diverges from the book's
stricter stances (short-lived branches with PR gates instead of trunk-only, coverage-as-signal instead of
fixed thresholds), the site is right and the book is dated.

The headline gap is data: the book devotes a full chapter to versioned database migrations, decoupled
migration sequencing, test-data strategy, and rollback without data loss, while the site covers only the
expand-contract pattern (in four places) with none of the surrounding practice. The second gap is
capacity/performance testing — the book treats it as a pipeline stage with its own vocabulary and
method, and the site has zero coverage (no load, capacity, soak, or performance-testing content
anywhere outside SLO definitions). Both are P1. Everything else is P2 polish: executable acceptance
specs, commit-stage discipline details, release-strategy checklists, config-management depth, component
pipelines/branch-by-abstraction, and a governance/maturity appendix the site may reasonably decline.

## Terminology corrections

- Glossary `CD` entry lumps Delivery and Deployment into one line, while `07-continuous-delivery`
  teaches the distinction carefully (a human/policy decision vs. automatic). Fix: split the glossary row
  into two entries pointing at `07-continuous-delivery/continuous-delivery.md` and
  `08-continuous-deployment/continuous-deployment.md`. P2, files: `GLOSSARY.md`.
- `08-continuous-deployment` prerequisites say unfinished work hides behind flags and "never branches,"
  while `02-continuous-integration` allows branches that live hours-to-days. Both are defensible in
  context, but a reader doing both paths back-to-back meets two absolute-sounding rules. Fix: soften the
  deployment-auto line to match the CI book (short-lived branches acceptable, long-lived ones not), or add
  one sentence explaining the stricter bar applies once a service auto-ships. P2, files:
  `08-continuous-deployment/continuous-deployment.md`.
- No other terminology fix recommended: deploy vs. release vs. promote, artifact vs. binary, staging vs.
  production, smoke vs. E2E are all used the way the book uses them.

## Content gaps (missing concepts)

- **P1 — Database migration practice.** The site teaches expand-contract (`10-deployment-strategies`,
  `14-reliability-and-recovery`, `08-continuous-deployment`, Lab 05) but not: versioned incremental
  migration scripts with a runner, forward/reverse script discipline, dual-compatible (old-code-on-new-
  schema) rollout sequencing, verifying migrations inside the pipeline, rollback-without-data-loss
  procedures, or test-data strategy (minimal constructed data vs. production dumps, seeded state via APIs).
  Home: extend `14-reliability-and-recovery/rollback-recovery.md` (data-safe rollback section) and
  `10-deployment-strategies/deployment-strategies.md` (migration sequencing section); if either grows past
  ~60 lines, split a new `12.x`-adjacent data book instead.
- **P1 — Capacity and performance testing as a pipeline stage.** The book's method (quantified NFR
  thresholds, scenario-derived load from acceptance flows, isolated perf environment, warm-up, trend
  thresholds that ratchet) has no counterpart on site; `04-testing/testing-strategy.md` stops at E2E and
  `13-observability-and-feedback` defines SLOs without saying how load behavior gets proven pre-release.
  Home: new section in `04-testing/testing-strategy.md` (placement: post-merge/staging stage, vocabulary:
  throughput vs. capacity vs. scalability, anti-patterns: unquantified goals, shared-host measurements).
- **P2 — Executable acceptance specifications.** The site has the pyramid and contract tests but nothing on
  acceptance criteria written as runnable specs, the analyst-tester-developer kickoff habit, or
  Given-When-Then structuring. Home: short section in `04-testing/testing-strategy.md`.
- **P2 — Commit-stage discipline details.** `02-continuous-integration` covers stop-the-line and trunk;
  missing: pretested/preflight builds (validate before landing on main), a rotating build-master role for
  large teams, and ratcheting quality gates (fail only when warnings/duplication increase). Home: extend
  section 3 or 4 of `02-continuous-integration/continuous-integration.md`.
- **P2 — Release strategy/plan checklists.** `07-continuous-delivery` teaches the flow; the book's
  stakeholder template (owners, asset config, environments, approvals, monitoring, data, disaster recovery,
  support) would make a practical appendix. Home: new final section in
  `07-continuous-delivery/continuous-delivery.md` or `09-environments-and-release/environments-release.md`.
- **P2 — Configuration-management depth.** `09-environments-and-release` covers config-vs-code and IaC, but
  the book's "version everything, inject config as late as possible, keep environments rebuildable from
  automation" deserves one consolidated section (injection timing: build vs. package vs. deploy vs. runtime;
  environment parity as a reproducibility test). Home: extend
  `09-environments-and-release/environments-release.md`.
- **P2 — Component pipelines and branch by abstraction.** Feature flags exist (`10-deployment-strategies`);
  the abstraction-branch technique for large refactors without long branches, and the component-pipeline /
  integration-pipeline split for multi-binary systems, do not. Home: short section in
  `10-deployment-strategies/deployment-strategies.md` (abstraction) and `06-ci-cd-pipelines/pipelines.md`
  (integration pipeline).
- **P2 — Test-double taxonomy.** The pyramid names layers but never distinguishes dummy/fake/stub/spy/mock
  or warns against over-mocked interaction tests. Home: 5-line addition to `04-testing/testing-strategy.md`.
- **P2 (optional, may decline) — Governance appendix.** Maturity model, value-stream mapping, risk process,
  compliance-as-automation-evidence. None exists on site; the site is a practitioner reference, not a
  management guide, so declining is legitimate — but if accepted, home is a new reference book, not an
  insertion into existing ones.

## Framing/accuracy corrections

- Nothing on site currently contradicts the book in a way that needs fixing. The two spots checked most
  carefully both resolve in the site's favor: staging-data handling (sanitized snapshots, never prod data —
  matches the book's cautions) and blue-green database changes (site prescribes expand-contract throughout
  and never suggests the book's read-only-window maneuver, which modern practice has superseded).
- One wording watch-item, not a correction: `10-deployment-strategies` line 70 correctly scopes
  expand-contract as "necessary but not sufficient" for stateful systems — keep that framing when the P1
  data work lands, so the new migration content reads as completing the thought rather than contradicting it.

## Structural/sequencing observations

- Path order (`start-here` → `ci-core` → `delivery` → `jenkins-core` → `jenkins-advanced` → `platforms` →
  `labs`) mirrors the book's own dependency logic (version everything → CI → pipeline → delivery →
  ecosystem/tooling). No reorder recommended.
- The content gaps cluster exactly where the site's structure has no home: data has no book or path slot
  (Ch12 equivalent), capacity has no stage slot (Ch9 equivalent), governance has no appendix slot (Ch15
  equivalent). When the P1 items are scheduled, decide first whether data gets its own book (recommended if
  the migration-practice content exceeds one section) or extends `14-reliability-and-recovery`, since that
  choice ripples through `TOPIC_INDEX.md`, `ROADMAP.md`, `GLOSSARY.md`, `CONTENT_MAP.md`, `books.json`,
  and `paths.json` per project rules.
- The book's "walking skeleton" idea (minimal end-to-end pipeline in iteration zero, then grow) is implicitly
  how Labs 01–04 sequence (pipeline → artifacts → deployment) but is never named; consider naming it in the
  labs path intro when convenient, P2.

## Not recommended for action

- **Trunk-only absolutism.** The book permits branching in narrow exceptions; the site teaches short-lived
  branches + PR gates + merge queues + flags. The site's synthesis is current mainstream practice — do not
  regress toward the stricter rule.
- **Fixed coverage thresholds.** The book's era-typical 75–80% stance is already superseded on site
  (`04-testing` treats coverage as a smoke signal and calls out assert-free gaming). No change.
- **Absolute build-time budgets.** The book's ten-minute commit-stage ideal survives on site in modernized
  form (`04-testing` placement rules: PR pipeline under ~10 minutes, slower suites post-merge). No change.
- **2010 tool references** (period CI servers, build tools, config managers, middleware). The site already
  teaches the modern equivalents (Actions/runners, BuildKit, IaC, lockfiles, SBOM). Do not backfill the
  book's tooling.
- **Manual approval gates as the default risk control.** The book leans on human gates; the site teaches
  policy gates, progressive delivery, and kill criteria. The site is current — no change.
- **VCS history chapter.** Pre-Git-dominated comparisons have no action value for the site's Git-based
  `01-source-control` book.
- **Heavyweight compliance framing (ITIL/PRINCE2-era).** Unless the optional governance appendix is
  commissioned, leave regulated-industry guidance at its current level (delivery-vs-deployment choice table
  + decision guide row).
- **Virtualization-skeptic capacity advice.** The book's avoid-virtual-hosts rule is dated; when writing the
  P1 capacity section, base it on ephemeral production-like environments, not on the book's constraint.
