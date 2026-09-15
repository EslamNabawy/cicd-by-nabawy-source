---
title: Testing Strategy in Pipelines
category: testing
status: complete
difficulty: intermediate
prerequisites:
  - CI/CD Pipelines
  - Build Systems
related:
  - CI/CD Pipelines
  - Continuous Delivery
---

<!-- icon: testing -->
# Testing Strategy

> Testing strategy decides *which tests run where*: fast unit tests gate every PR, slow E2E proves staging — the pyramid keeps feedback fast without losing coverage.

## 1. What Is It?

Picking up from **[Build Systems](../03-build-systems/build-systems.md)**, where output became deterministic — now prove it's correct, at the right stage, at the right cost.

## 2. The Pyramid in Pipelines

| Layer | Speed | Runs in | Guards |
|-------|-------|---------|--------|
| Unit | ms each, minutes total | Every PR | Logic correctness |
| Contract | seconds | Every PR (provider + consumer) | API compatibility between services |
| Integration | minutes | Post-merge / staging | Wiring, DBs, queues |
| E2E / smoke | minutes–tens of minutes | Staging, post-deploy | Real user journeys |

Many unit, fewer E2E: an inverted pyramid (all Selenium, no units) is slow, flaky, and tells you nothing a unit test couldn't in milliseconds.

Test doubles, cheapest first: stub (canned answers) → fake (working shortcut, e.g. in-memory store) → mock (verifies interactions). Mock roles and boundaries, never implementation trivia — over-mocked suites shatter on every refactor while missing real regressions.

## 3. Placement Rules

- PR pipeline: unit + contract + fast integration (< 10 min total). Anything slower moves post-merge.
- Staging: full integration + E2E + smoke after deploy; failures block promotion, not merges.
- Post-deploy: synthetic smoke probes continuously — the pipeline's last test never ends.
- Acceptance criteria as executable specs: analyst + tester + developer agree the criteria before coding, written so the pipeline can run them (Given-When-Then). Docs that can't fail the build drift from behavior.

## 4. Flaky Policy

Flaky test protocol: quarantine to a non-blocking suite immediately (same day), assign an owner, fix-or-delete deadline of one sprint. A flaky gate teaches developers that red is meaningless — the most expensive test debt there is.

## 5. Capacity & Performance Placement

Functional tests prove correctness; capacity tests prove survival. Treat performance as a requirement with a number, not a wish:

- Quantify first: convert expected load into thresholds (p99 latency, sustained throughput, concurrent users) — unquantified goals justify unbounded effort.
- Placement: short performance smoke sentinels in the PR pipeline; full load scenarios post-merge/staging on isolated, production-like hosts (shared or noisy hosts produce phantom regressions).
- Derive load from reality: adapt acceptance flows into composable load scenarios; warm up caches/JIT before measuring.
- Ratchet thresholds: start at minimum viable target, raise as headroom proves stable; investigate before lowering.
- Vocabulary: latency (one transaction's time) vs throughput (transactions per interval) vs capacity (max sustainable throughput within latency budget).

## 6. Failure Modes

- Testing pyramid inverted → 40-minute PR suites developers ignore; rebalance toward units.
- E2E in PR → queue pileups; move to staging.
- No contract tests in microservices → integration surprises at deploy; add consumer-driven contracts.
- Coverage % as a target → gaming (assert-free tests); treat coverage as smoke signal, not goal.

## 7. Interview Notes

- Why contract tests exist (microservice API drift).
- Flaky quarantine protocol, step by step.
- What runs in PR vs staging vs post-deploy, and why.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Build Systems](../03-build-systems/build-systems.md)
- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)

Proven correct — now ship it releasably. Continue in **[Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)**.
