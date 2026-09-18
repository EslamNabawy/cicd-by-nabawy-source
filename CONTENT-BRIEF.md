# CONTENT BRIEF — cross-linking, basics spine & tool guidance (no content written yet)

Date: 2026-09-18. Method: measured from `pdf/*.html` (chapter inventory, mention counts,
heading duplicates, anchor audits) — not guessed. This file specifies WHAT to create and
WHERE it lands. Content generation is a separate step.

## 1 · Current map (8 books, verified 2026-09-18)

| Book (id) | Chapters (pghead h1 order) | Appendix |
|---|---|---|
| start-here | Foundations, Continuous Integration, CI vs CD, Pipeline & Status, Environments & Flow, Console, Artifact & Gate, Failure & Recovery, Check & Map, Source Control, Flow & Commands, Models & Discipline, Check & Handoff, Integration, Gates, Handoff + Map/Glossary/Interview/Cheat/Quiz | full |
| build-artifacts | Pipelines, Execution, Stages & Builders, Discipline, Handoff, Build Systems, Testing Strategy (+cont), Artifacts, Lifecycle, Trust & Handoff + appendix | full |
| deliver-operate | Strategies, Mechanics, Check & Handoff, CD, Staging, Failure Modes, Release Trains, Preview Envs, CD(2), IaC, Observability, Best Practices, Recovery Drills, Secrets, + appendix | full |
| jenkins-complete | 12 chapters (Jenkins→Troubleshooting) + appendix | full |
| platforms-roadmaps | Actions, GitLab CI, ArgoCD/GitOps, Roadmap Jenkins/Actions, Choice + appendix | full |
| labs-handbook | 9 labs + appendix | full |
| cheatsheet | 7 tool sections | none (is appendix) |
| observability | 20 chapters, reference-built | full |

Known defects to fix while editing (measured):
- D1 deliver duplicate pghead h1 `1. What Is It?` ×5 → rename: s14 Continuous Deployment,
  s15 Environments & Release, s17 IaC for Environments, s27 Rollback & Recovery,
  s30 CI/CD Security (continued sheets keep suffix).
- D2 platforms duplicate h1s → s08/s09 `ArgoCD & GitOps (+continued)`; s10 is a pure
  Related-Topics tail → merge into s09, delete, renumber; s11/s12 `GitLab CI (+cont)`;
  s13/s14 `GitOps Delivery (+cont)`; s19 `Roadmap Risks & Handoff`; s25
  `Platform Risks & Handoff`; s31 `Decision Risks & Handoff` (continued keep suffix).
- D3 jenkins duplicate h1s → s14 `Agent Wiring`; s25 `Webhook Wiring`; s20
  `Bindings & Handoff`; s23 `Plugins & Handoff`; s26 `Webhooks & Handoff`; s29
  `Security & Handoff`.
- D4 labs `System Map` ×10 → rename to `<prev-sheet-topic> · Map` using preceding sheet h1
  (measured pairs: Hermetic Builds, The Production Gate, Canonical Pipeline, Library
  Consumption, Backup & Restore, Lab 02 End-To-End Trigger, End-To-End Delivery,
  Lifecycle Management, Conditional Validation, Provisioning & Recovery).

## 2 · Link architecture (the rule)

Every content sheet keeps its folio Prev/Next/TOC (already true, verified). ON TOP:
- R1 Each book's Handoff/closing sheet links the NEXT book in path order with a ⏭️ bridge
  (start-here already does: s14→build, book-end→build-artifacts).
- R2 Every tool-introduction sheet links its tool's WHEN-TO-USE box (G2) and the
  tool-vs-tool matrix (G3).
- R3 No new `#anchor` may dangle: run `verify_phase3.py` anchor check after every edit.
- R4 Link text is the destination's pghead h1 verbatim (no "PDF NN", no "click here").

Chain (path order): start-here → build-artifacts → deliver-operate → observability →
jenkins-complete → platforms-roadmaps → labs-handbook (+ cheatsheet as reference).

## 3 · Gap catalog (content to create)

### G1 — WHAT-IS spine (basics: what actually is CI/CD)
Status: scattered (start-here Foundations/CI-vs-CD covers it, but no single spine page).
Create ONE new sheet in start-here after The Map (id s03, shift rest):
- pghead: kick `START HERE`, h1 `What CI/CD Actually Is`, hmeta new number.
- p.lead thesis (2 sentences) + zone flow: commit → CI → artifact → CD → observe.
- tb.tight 4 rows: CI vs Delivery vs Deployment vs GitOps (question each answers).
- m-key: "CI answers does-it-work; Delivery keeps it releasable; Deployment ships it."
- m-exam closing + ⏭️ bridge to Foundations.
Source material: start-here s04 (CI vs CD), s06 (loop), deliver-operate glossary rows.

### G2 — WHEN-TO-USE boxes (one per tool, same shape)
Status: ~1 hit per book (measured) — effectively missing.
Create one `m-tip` box per tool, placed on that tool's intro sheet, identical shape:
`WHEN TO USE <TOOL> — use when: <3 bullets> · avoid when: <2 bullets>`.
Placements (sheet ids current; re-resolve after renumber):
- Jenkins → jenkins-complete Setup sheet (s06): self-hosted, complex pipelines, plugin
  ecosystem; avoid for greenfield SaaS with no ops team.
- GitHub Actions → platforms-roadmaps Actions sheet (s02): GitHub-hosted repos, zero
  infra, supply-chain-gated; avoid for heavy self-hosted compliance fleets.
- GitLab CI → platforms-roadmaps GitLab sheet (s11 after D2 rename): single-platform
  shops, review apps, merge trains; avoid polyglot multi-platform estates.
- ArgoCD/GitOps → platforms-roadmaps ArgoCD sheet (s08 after D2 rename): Kubernetes
  fleets, pull-model audit needs; avoid non-K8s or tiny estates.
- Labs tools (Docker/Jenkins/Terraform/FLOCI) → labs-handbook Lab 01 sheet (s03):
  what each tool does IN the labs and when you'd pick it outside.
- Loki/Prometheus/Grafana → observability chapters ch-01/ch-04/ch-06 (when-to-use
  per pillar: logs vs metrics vs traces).
Acceptance: 6 boxes, same visual shape, each ends with tlink to G3 matrix.

### G3 — TOOL-VS-TOOL matrix (one comparative sheet per rivalry)
Status: comparisons exist as tables (deliver 40 hits) but no decision clock.
Create ONE new sheet in platforms-roadmaps after Decision Framework (s29):
- pghead h1 `Tool vs Tool — The Whole Field`.
- tb.tight 6 rows × cols (Jenkins | Actions | GitLab | ArgoCD): config lives, runners,
  gates, secrets, cost shape, best-fit (each cell ≤12 words, distilled from book texts).
- m-warn: "No best tool — only best fit for team size, hosting, and audit needs."
- m-exam: one-line pick rule per team shape (solo dev, startup SaaS, regulated bank,
  K8s platform team).
- ⏭️ bridge to Convergence + backlink from each G2 box.
Source material: platforms-roadmaps Side-by-Side (s28), GitLab-vs-Sisters table (s12),
  roadmap decision content (s27–s31), jenkins-complete Topology/Agents.

### G4 — BASICS checklist (fill don't-think gaps, one sheet each max)
- G4a start-here: `DevOps vs CI/CD vs CD` m-key box on Foundations sheet (s03) —
  measured: never stated in one place.
- G4b build-artifacts: `Build vs Buy runners` m-tip on Execution sheet (s03) —
  hosted vs self-hosted decision in 4 bullets.
- G4c deliver-operate: `Staging vs Production data rule` m-warn on Environments
  sheet (s15 after D1 rename) — sanitized-shape rule, measured as scattered.
- G4d labs-handbook: `What each lab proves` summary table on TOC-adjacent new sheet
  after Lab 01? NO — cheaper: extend existing TOC legend area? Decision: new sheet
  `Lab Map` after toc (9 rows: lab → proves → needs). Source: lab pgheads.

### G5 — Appendix backlinks (close the loop)
Each book's Quiz FINAL CHECK already points onward except: add tlink from
labs-handbook quiz → cheatsheet, and cheatsheet → start-here (cycle). One line each.

## 4 · Execution order
1. D1–D4 heading fixes (mechanical, renumber, anchor-verify).
2. G1 spine sheet (renumber start-here).
3. G2 six boxes (no renumber — inline appends before folio).
4. G3 matrix sheet + G2 backlinks.
5. G4a–d boxes/sheet.
6. G5 two lines.
7. Per step: rebuild + `verify_phase3.py` anchors + `fill_rig.py` clip check on touched
   sheets + QC. Any clip → split per established procedure.

## 5 · Out of scope (explicitly NOT this brief)
- Rewriting existing prose, new chapters beyond above, Arabic edition, print export,
  homepage changes.
