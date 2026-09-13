---
title: "Lab 02 — Build and Test"
category: labs
status: complete
difficulty: beginner
prerequisites:
  - Lab 01
  - Build Systems
  - Testing Strategy
related:
  - Build Systems
  - Testing Strategy
---

<!-- icon: build -->
# Lab 02 — Build and Test

## Objective

Split Lab 01's single job into a fast, cached PR pipeline: hermetic build job → unit test job, total under 10 minutes.

## Prerequisites

- Lab 01 green; concepts: [Build Systems](../03-build-systems/build-systems.md), [Testing Strategy](../04-testing/testing-strategy.md).

## Architecture

PR → job `build` (`npm ci`, cache on lockfile) → job `test` (`needs: build`, unit suite) → combined status check.

## Setup

Add a second test file so the suite has something real to run.

## Step 1 — Split and cache

### Execute

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - run: npm test
```

### Expected Result

Two jobs, `test` waits for `build`; reruns are faster (warm npm cache).

### Why

`needs:` is the DAG edge; cache keyed on the lockfile is the hermetic speedup (see [pipelines DAG](../06-ci-cd-pipelines/pipelines.md)).

## Step 2 — Prove hermeticity

### Execute

Delete `node_modules` locally, run `npm ci && npm test` — same result as CI.

### Expected Result

Identical pass/fail locally and on the runner.

### Why

Lockfile-exact install means the runner builds what you built — no ambient-machine surprises.

## Verification

- [ ] Two jobs visible, ordered by `needs`.
- [ ] Cache hit shown on rerun.
- [ ] Local `npm ci` reproduces CI result.

## Failure Scenarios

- Cache never hits: lockfile not committed or key inputs changed — verify `package-lock.json` is tracked.
- `test` runs before `build` finishes: missing `needs:` — add the edge.

## Cleanup

Keep; Lab 03 packages this build's output.

## What This Proved

DAG ordering, hermetic installs, lockfile caching. Continue with [Lab 03](03-artifacts.md).
