---
title: Continuous Deployment
category: delivery
status: complete
difficulty: advanced
prerequisites:
  - Continuous Delivery
  - Deployment Strategies
  - Observability & Feedback
related:
  - Continuous Delivery
  - Deployment Strategies
---

<!-- icon: deployment -->
# Continuous Deployment

> Continuous Deployment removes the last human gate: every change passing all automated checks reaches production by itself. Freedom bought with automation rigor most teams haven't built yet.

## 1. What Is It?

Picking up from **[Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)**, where a human approved production — here the pipeline approves itself. Delivery asks "could we ship?"; Deployment ships.

## 2. Prerequisites (All Non-Negotiable)

- **Full automation:** build, test, scan, staging deploy, smoke, promotion — zero manual steps. Any human errand becomes the bottleneck that breaks the model.
- **Progressive delivery:** canary or flags on every release (see [Deployment Strategies](../10-deployment-strategies/deployment-strategies.md)) — automation needs a small blast radius to be safe.
- **Kill criteria:** automated halt conditions (error-budget burn, p99 regression, business KPI drop) that stop and roll back without asking.
- **Observability:** version-labeled everything, SLOs with burn alerts, on-call that trusts the automation (see [Observability](../13-observability-and-feedback/observability-feedback.md)).
- **Trunk discipline + flags:** unfinished work hides behind flags; branches live hours-to-days, never weeks — main is always shippable.

## 3. Failure Modes

- Automating a flaky pipeline → auto-shipping bugs at machine speed; fix gates first, automate second.
- No kill criteria → bad release reaches 100% "successfully"; every auto-promotion needs an automated halt.
- Database migrations without expand-contract → auto-deploy corrupts state; migrations must be backward-compatible across versions.
- On-call distrusts automation → humans re-add manual gates; fix with practiced, boring rollbacks that build confidence.

## 4. Delivery vs Deployment: When Each

- **Delivery** (human gate): regulated industries, data migrations, marketing-coordinated launches, teams still building gate maturity.
- **Deployment** (no gate): SaaS with progressive delivery, strong SLOs, practiced rollback, and trunk discipline. Start with low-risk services, expand the blast radius as confidence compounds.

## 5. Interview Notes

- Five prerequisites from memory, and how to verify each exists.
- Why automating a bad pipeline multiplies harm.
- Expand-contract migrations: why they're the price of auto-deploy.

## Related Topics

- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)
- [Deployment Strategies](../10-deployment-strategies/deployment-strategies.md)
- [Observability & Feedback](../13-observability-and-feedback/observability-feedback.md)

Auto-shipping needs somewhere to land safely. Continue in **[Environments & Release](../09-environments-and-release/environments-release.md)**.
