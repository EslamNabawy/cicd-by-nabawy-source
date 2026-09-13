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

## 3. Placement Rules

- PR pipeline: unit + contract + fast integration (< 10 min total). Anything slower moves post-merge.
- Staging: full integration + E2E + smoke after deploy; failures block promotion, not merges.
- Post-deploy: synthetic smoke probes continuously — the pipeline's last test never ends.

## 4. Flaky Policy

Flaky test protocol: quarantine to a non-blocking suite immediately (same day), assign an owner, fix-or-delete deadline of one sprint. A flaky gate teaches developers that red is meaningless — the most expensive test debt there is.

## 5. Failure Modes

- Testing pyramid inverted → 40-minute PR suites developers ignore; rebalance toward units.
- E2E in PR → queue pileups; move to staging.
- No contract tests in microservices → integration surprises at deploy; add consumer-driven contracts.
- Coverage % as a target → gaming (assert-free tests); treat coverage as smoke signal, not goal.

## 6. Interview Notes

- Why contract tests exist (microservice API drift).
- Flaky quarantine protocol, step by step.
- What runs in PR vs staging vs post-deploy, and why.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Build Systems](../03-build-systems/build-systems.md)
- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)

Proven correct — now ship it releasably. Continue in **[Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)**.
