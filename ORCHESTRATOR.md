# Orchestrator — CICD BY Nabawy Level-Up

This is the single entry point. Paste the block below into a Claude Code
session opened at the root of `cicd-by-nabawy-source`, with `tasks.yaml`
(same folder as this file) also placed at the repo root or referenced by
path. Claude Code then drives the entire plan itself — reading the
manifest, executing tasks in dependency order, checking each gate, and
stopping cleanly at anything that needs a human.

You do not run the Phase 1–4 prompts by hand. You run this once, then
respond to whatever it stops on.

---

## The orchestration prompt

```
You are orchestrating a multi-phase project using the task manifest at
tasks.yaml. Read it fully before doing anything.

RULES:
1. Execute tasks in dependency order (respect `depends_on`). Never start a
   task whose dependencies haven't passed their gate.
2. For each task: announce its id and name, run its `action` and/or
   `prompt` as written, then evaluate its `gate`.
3. Gate types and how to handle them:
   - exit_code_zero_and_output_contains: run the action, check the command
     exited 0 AND stdout contains the pattern. Pass/fail, no judgment call.
   - file_exists: check the file was actually written, not just claimed.
   - build_and_visual_diff / build_and_spotcheck / query_test /
     build_and_link_check: run the rebuild, then perform the described
     check yourself (fetch the rendered page, grep the anchors, run the
     search queries) — do not mark this passed on the basis of "I made the
     change" alone. Show me the evidence (the fetched HTML snippet, the
     query results) as part of your pass/fail statement.
   - manual_approval / manual_approval_for_deletions / manual_checklist /
     per_file_confirmation: STOP. Present exactly what needs review (diff,
     list, or checklist) and wait for my explicit go-ahead before marking
     the task's gate passed and moving to the next task. Do not proceed
     past a manual gate on your own judgment, even if the change looks
     obviously fine to you.
4. On any failed gate: stop, report which task failed and why, and follow
   its `on_fail` instruction if present. Do not silently skip to the next
   task or improvise a different fix without telling me first.
5. Maintain a running STATUS.md at the repo root: one line per task
   (id, name, status: pending/in-progress/passed/failed/blocked-on-human),
   updated after every task. This is the source of truth if this session
   is interrupted — on resume, read STATUS.md first and continue from the
   first non-passed task rather than restarting.
6. Never touch `pdf/` or `website/dist/` by hand — only via
   `website/scripts/build.py`. Never edit anything on `main` directly —
   all work happens on the branch created in P0.1.
7. Treat `AUDIT_STRUCTURE.md` and `AUDIT_UX.md` (produced in Phase 1) as
   the sole source of scope for Phase 2 and Phase 3 tasks — don't expand
   scope beyond what those audits + their approved "top 5" surfaced.
8. Batch related file edits into single diffs per task rather than one
   commit per line — but keep Phase 2 (UI/UX) changes and Phase 3
   (content) changes in separate commits, so they can be bisected
   independently if something breaks post-deploy.
9. When a task's gate is `build_success` or similar automated checks pass
   but you're not fully confident the change matches intent, say so
   explicitly rather than marking it passed — surface the uncertainty as
   part of your report, and let me decide.

Begin with P0.1. After each task completes (gate passed), print the
updated STATUS.md table, then proceed automatically to the next
ready task — except for manual_* gates, where you stop and wait for me.
```

---

## What "fully orchestrated" means here, concretely

- **One command to start it**, not 14 prompts pasted by hand.
- **Dependency-ordered execution** — `tasks.yaml`'s `depends_on` is the
  scheduler; Claude Code won't jump ahead.
- **Machine-checkable gates where possible** (file exists, build exits 0,
  a search query returns a hit) instead of "looks good to me."
- **Explicit human checkpoints** at the points that actually matter: after
  audits set scope (P1.gate), after each destructive/subjective content
  change (glossary deletions, difficulty reclassification), and before
  merging to `main` / deploying (P4.3). Nothing auto-merges or auto-deploys.
- **A resumable state file** (`STATUS.md`) so a dropped session doesn't
  mean starting over — this matters because Phase 3 alone touches all 39
  books and is likely to span multiple sessions.
- **Separated blast radius** — UI/UX commits and content commits stay
  separate, so a bad UI change doesn't force reverting content fixes too.

## Files in this bundle

- `ORCHESTRATOR.md` (this file) — the prompt you actually run.
- `tasks.yaml` — the manifest it executes. Edit this directly if you want
  to add/remove/reorder tasks; the orchestrator prompt reads it fresh each
  time, so changes take effect on the next run without touching the prompt.

## Running it again after an interruption

Open a new Claude Code session in the repo, and simply say:

```
Resume orchestration. Read STATUS.md and tasks.yaml, continue from the
first task that isn't marked passed.
```

## If you want to run only one phase

```
Read tasks.yaml. Execute only tasks in phase P2, in dependency order,
following all the same rules as full orchestration (gates, STATUS.md,
manual stops). Skip phases not requested.
```