---
title: Environments & Release
category: delivery
status: complete
difficulty: intermediate
prerequisites:
  - Continuous Delivery
  - Deployment Strategies
related:
  - Continuous Delivery
  - Continuous Deployment
---

<!-- icon: deployment -->
# Environments & Release

> Environments are runtime contexts with different data, scale, and risk; release is the discipline of moving one artifact across them safely — same binary, different config, explicit promotion paths.

## 1. What Is It?

Picking up from **[Continuous Deployment](../08-continuous-deployment/continuous-deployment.md)**, where automation needed safe landing zones — here is how those zones are built and governed.

## 2. Environment Topology

| Env | Purpose | Data | Deploys |
|-----|---------|------|---------|
| Dev | Individual velocity | Fake/local | Continuous, anything |
| Preview (per-PR) | Review the actual change | Sanitized snapshot | Auto per PR, destroyed on merge |
| Staging | Prod rehearsal | Sanitized/anonymized prod-like | Auto on main |
| Production | Real users | Real | Gated (delivery) or automated (deployment) |

Preview environments are the highest-leverage addition: reviewers click the change instead of imagining it.

## 3. Config vs Code

The artifact never changes between environments; everything else does via config: env vars for simple values, secret stores for credentials, config maps/files for structured settings. Twelve-factor discipline: a diff between staging and production behavior must be explainable by config diff alone — never by "we built it differently."

## 4. Release Trains & Promotion Paths

- **Release train:** scheduled departures (e.g. Tuesdays/Thursdays); whatever is green and approved rides, the rest waits for the next train. Predictable for stakeholders, calming for on-call.
- **Promotion path:** dev → preview → staging → production, each gate explicit (checks + approvals + signals). Skipping environments is the process smell that precedes incidents.
- **Hotfix lane:** a documented fast path (fewer approvals, same checks) for production fires — used rarely, reviewed always.

## 5. Failure Modes

- Snowflake environments (hand-configured staging) → "works in staging" lies; environments are code (IaC), rebuilt identically.
- Real prod data in staging → breach waiting to happen; sanitize/anonymize with production-like shape.
- Config in code (URLs baked into images) → rebuild per env, voiding artifact immutability; externalize everything.

## 6. Interview Notes

- Why preview environments beat screenshots for review quality.
- Config-vs-code: what breaks when the artifact differs per env.
- Design a hotfix lane that stays safe under pressure.

## Related Topics

- [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md)
- [Continuous Deployment](../08-continuous-deployment/continuous-deployment.md)
- [Deployment Strategies](../10-deployment-strategies/deployment-strategies.md)

Zones built and governed — now lock down the supply chain running through them. Continue in **[CI/CD Security](../11-security/cicd-security.md)**.
