---
title: Continuous Integration Discipline
category: foundations
status: complete
difficulty: beginner
prerequisites:
  - Git, Branching & Pull Requests
related:
  - CI/CD Pipelines
  - Testing Strategy
---

<!-- icon: pipeline -->
# Continuous Integration

> Continuous Integration is the team discipline of merging small changes frequently with automated verification — the practice behind the pipeline, not the pipeline itself.

## 1. What Is It?

Picking up from **[Git, Branching & Pull Requests](../01-source-control/git-branching-pull-requests.md)**, where the PR gate was built — CI is the discipline that makes the gate meaningful: integrate daily, verify automatically, fix immediately.

- **Integrate:** merge to shared `main` at least daily; branches live hours-to-days, never weeks.
- **Verify:** every merge runs build + test + scan (see [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md) for the machinery).
- **Fix:** a red `main` is the team's top priority — stop the line, revert or fix forward, then resume.

## 2. Why Does It Exist?

Integration pain grows with branch age: two-day branches merge in minutes, two-month branches merge in weeks. CI converts one terrifying merge into dozens of trivial ones.

## 3. PR Gates & Merge Queues

- **PR gate:** required status checks (green CI + approvals) enforced by branch protection. No green, no merge — no exceptions, no admin overrides "just this once."
- **Merge queue:** on busy `main`, merges serialize through a queue that rebases each PR onto the latest green `main` and re-verifies before landing. Prevents the "green on branch, red on main" race.
- **Linear history** (rebase/squash merges) keeps `main` bisectable: any commit builds, any commit reverts cleanly.
- **Preflight builds:** validate the diff on CI infrastructure *before* it lands on `main` — prevention beats fast reverts on busy branches.

## 4. Trunk Discipline

- Tiny branches, daily merges; feature flags hide unfinished work instead of long branches.
- `main` is always releasable — a broken `main` blocks everyone, so whoever breaks it fixes it first.
- Measure: merge frequency per developer per week. Falling numbers mean branches are growing teeth.
- **Build master (large teams):** a rotating shepherd who tends the pipeline and reverts lingering breakage — a temporary discipline role, not a title.
- **Ratcheting gates:** fail the build when warnings, duplication, or style violations *increase* versus the last green commit — quality can only move one direction without a big-bang cleanup.

## 5. Failure Modes

- Long-lived branches → merge hell; fix with WIP limits and flags hiding unfinished work.
- Red `main` normalized ("someone else will fix it") → quality collapse; fix with stop-the-line culture.
- Flaky gates → developers bypass checks; fix by quarantining flakes, never by disabling gates.

## 6. Interview Notes

- CI practice vs CI pipeline: discipline vs machinery.
- Why merge queues exist (the rebase race on busy `main`).
- Trunk-based vs Git Flow, and what each demands of the team.

## Related Topics

- [Git, Branching & Pull Requests](../01-source-control/git-branching-pull-requests.md)
- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Testing Strategy](../04-testing/testing-strategy.md)

Small merges, verified automatically, fixed immediately — that discipline feeds every pipeline downstream. Continue in **[CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)**.
