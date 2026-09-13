---
title: "Lab 05 — Rollback"
category: labs
status: complete
difficulty: intermediate
prerequisites:
  - Lab 04
  - Rollback & Recovery
related:
  - Rollback & Recovery
  - Observability & Feedback
---

<!-- icon: monitoring -->
# Lab 05 — Rollback

## Objective

Break production deliberately, then recover by redeploying the previous known-good digest — and write the postmortem.

## Prerequisites

- Lab 04 green with two successful production deploys (you need a previous good digest); concepts: [Rollback & Recovery](../14-reliability-and-recovery/rollback-recovery.md).

## Architecture

Bad merge → staging green-but-wrong (tests miss it) → approved to prod → incident → redeploy previous digest → postmortem with a pipeline action item.

## Setup

Note the current production digest; keep its value handy.

## Step 1 — Cause the incident

### Execute

Merge a change that passes tests but breaks the app's visible output (e.g. wrong port, broken route). Promote to production.

### Expected Result

Production is broken despite a green pipeline.

### Why

Green ≠ correct: tests cover what you thought of. This is why recovery must be engineered, not improvised.

## Step 2 — Roll back, don't rebuild

### Execute

Redeploy the previous digest to production (re-run the old `deploy-prod` or dispatch with the saved digest). Time yourself.

### Expected Result

Production healthy in minutes; no fresh build involved.

### Why

Old digests are proven; fresh builds add untested variables to a fire (see [rollback rule](../14-reliability-and-recovery/rollback-recovery.md)).

## Step 3 — Postmortem with teeth

### Execute

Write: timeline, root cause, and one action item that becomes a pipeline change (a new test, check, or alert) — then implement it.

### Expected Result

A merged pipeline change that would have caught this incident.

### Why

Postmortems without merged changes are diary entries.

## Verification

- [ ] Recovery time measured (aim: minutes).
- [ ] Previous digest redeployed, not a fresh build.
- [ ] One preventive pipeline change merged.

## Failure Scenarios

- Previous digest unknown: promotion didn't record digests — log every deployed digest from now on.
- Rollback also broken: data migrated forward — forward-fix with expand-contract instead.

## Cleanup

Keep the postmortem in the repo (`docs/postmortems/`).

## What This Proved

Recovery as a practiced path. General labs complete — Jenkins track starts at [Lab 06](06-jenkins-controller.md).
