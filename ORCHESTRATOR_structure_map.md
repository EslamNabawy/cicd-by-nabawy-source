# Orchestrator — "Structure Map" Zoomable View Feature

Single entry point. Paste the block below into Claude Code, opened at the
root of `cicd-by-nabawy-source`, with `structure_map_tasks.yaml` placed at
the repo root (or reference its path in the prompt).

---

## Why this manifest has ONE human gate (unlike a pure bugfix)

Adding new UI/UX — a new metaphor, a new interaction, a new page — is a
different risk profile than fixing a known bug. A bugfix has a clear
"broken vs fixed" test. A new "building/cube" view has many equally
plausible interpretations of what a block maps to, what zooming reveals,
and how literal the 3D should be — and an autonomous agent will pick
*something* and build it fully, 10 tasks deep, before you see it if nothing
stops it. Unwinding that after the fact costs far more than one review
pass up front.

So: **Phase D produces a written design proposal and stops for your
explicit sign-off.** Every phase after that (B1–B4) runs fully
autonomously through build, verify, commit, merge, and deploy — same as
the bugfix orchestration — because once the concept and data mapping are
locked, the remaining work is genuinely mechanical and low-ambiguity.

---

## The orchestration prompt

```
You are orchestrating a new-feature build using the task manifest at
structure_map_tasks.yaml. Read it fully before doing anything.

RULES:
1. Execute tasks in dependency order (respect `depends_on`).
2. Phase D is different from every other phase: D.1 produces a design
   document (STRUCTURE_MAP_PROPOSAL.md) and D.gate is a hard stop. Do not
   write any implementation code during Phase D. After D.1, present the
   proposal and explicitly wait for my written answers to the questions it
   raises (grouping choice, pseudo-3D vs true-3D, route, any changes)
   before touching B1. This is the only phase where you ask before acting.
3. From B1 onward, run fully autonomously: no approval stops. For gates
   marked `manual_checklist`, perform the check yourself (render the page,
   test the interaction, inspect the color pairs) and report the checklist
   results as evidence in your own final report — don't ask me to verify
   them, verify them yourself and show me what you found.
4. For `build_and_visual_diff` / `build_and_spotcheck` / `build_and_link_check`
   gates: actually fetch/render the page and check the described property.
   Don't mark a gate passed on the basis of "I wrote the code for it."
5. On any failed automated gate (build_success, exit_code_zero_and_output_contains):
   fix it yourself and retry until it passes. Only stop and report to me if
   something is genuinely unrecoverable after reasonable retries.
6. Treat the human's answer at D.gate as the locked spec for the rest of
   the build. Do not deviate from it in later tasks — if a later task
   surfaces a reason the locked spec doesn't work (e.g. true-3D transforms
   are unworkably broken on mobile), note the conflict in your final report
   rather than silently reverting to a different approach you weren't
   authorized for.
7. Reuse existing site infrastructure wherever the manifest says to:
   existing book-card markup for the detail view, existing CSS theme
   variables, existing books.json as the single data source (generate any
   derived structure at build time in build.py, never hand-author a second
   manifest). Do not introduce a new JS framework or build dependency for
   a static Mintlify-based site.
8. This feature must be strictly additive — homepage, reader pages, and
   glossary must be unchanged. Verify this explicitly at B4.2, not just
   assume it because you didn't intend to touch them.
9. Keep this feature on its own branch (feature/structure-map-view) for
   its entire build — don't mix it into other work.
10. Maintain STATUS.md at repo root: one line per task (id, name, status),
    updated after every task, so this is resumable if the session drops.
    On resume, read STATUS.md first and continue from the first non-passed
    task — don't restart, and don't re-open the D.gate question if it was
    already answered and recorded.
11. This project has a known recurring bug class: icons/text breaking
    across dark/light theme (some icons are white-only and vanish in light
    mode). B3.1 explicitly re-checks for this in the new view — treat that
    check as mandatory, not optional, given the project's history.

Begin with D.1. Stop at D.gate and wait for my answer. After I answer,
proceed through B1–B4 automatically, printing the updated STATUS.md table
after each task, until B4.4 is done or something is truly blocked.
```

---

## What happens when you run this

1. **You get one document to read** (`STRUCTURE_MAP_PROPOSAL.md`) — not
   code, not a partially-built feature. It proposes what a "block" means
   in terms of your actual `books.json` data, whether to go literal-3D or
   a cheaper pseudo-3D treatment (recommended, given this is a solo-
   maintained static site and true 3D is expensive to theme/mobile-proof),
   the route, and the accessibility fallback.
2. **You answer a short set of concrete questions** (grouping choice,
   visual approach, route) — this is the only manual step in the entire
   feature.
3. **Everything else runs on its own**: data layer → zoomed-out map →
   click-to-zoom → detail view (reusing existing book cards, not a new
   content renderer) → accessibility/reduced-motion → theme correctness
   (explicitly re-checking the icon-visibility bug class from your last
   fix) → mobile → QC → commit → merge → deploy → live verification.
4. You see a final report once it's live, with the design decisions
   documented and every checklist item shown as evidence, not asserted.

## Files in this bundle

- `ORCHESTRATOR_structure_map.md` (this file) — the prompt you run.
- `structure_map_tasks.yaml` — the manifest it executes.

## Resuming after an interruption

```
Resume Structure Map orchestration. Read STATUS.md and
structure_map_tasks.yaml, continue from the first task not marked passed.
If D.gate was already answered, do not re-ask — use the recorded answer.
```