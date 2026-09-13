---
title: "Lab 04 — Deployment"
category: labs
status: complete
difficulty: intermediate
prerequisites:
  - Lab 03
  - Continuous Delivery
  - Deployment Strategies
related:
  - Continuous Delivery
  - Environments & Release
---

<!-- icon: deployment -->
# Lab 04 — Deployment

## Objective

Promote Lab 03's digest through staging to production with an explicit approval gate — same digest, two environments.

## Prerequisites

- Lab 03 digest in GHCR; concepts: [Continuous Delivery](../07-continuous-delivery/continuous-delivery.md), [Environments & Release](../09-environments-and-release/environments-release.md).

## Architecture

`main` → deploy digest to staging (auto) → smoke check → GitHub Environment `production` (required reviewer) → deploy same digest → verify.

## Setup

Repo Settings → Environments → create `staging` and `production`; set a required reviewer on `production`.

## Step 1 — Staging auto-deploys

### Execute

```yaml
deploy-staging:
  needs: image
  environment: staging
  runs-on: ubuntu-latest
  steps:
    - run: echo "deploy ${{ needs.image.outputs.digest }} to staging"
```

### Expected Result

Every `main` merge deploys staging without human action.

### Why

Staging proves the artifact continuously; automation here is safe because users never see it.

## Step 2 — Production needs a human

### Execute

Add `deploy-prod` with `environment: production` and `needs: [deploy-staging]`; merge, then approve the pending deployment.

### Expected Result

Production waits for approval; after approval it runs the same digest.

### Why

This is Continuous Delivery's one gate: releasable always, deployed by decision (see [delivery vs deployment](../07-continuous-delivery/continuous-delivery.md)).

## Verification

- [ ] Staging deploys on every merge, no clicks.
- [ ] Production blocks until approved.
- [ ] Both environments ran the identical digest.

## Failure Scenarios

- Approval never arrives: check environment reviewers and notifications.
- Digests differ between envs: promotion passed a tag, not a digest — pass `${{ outputs.digest }}` explicitly.

## Cleanup

Keep environments; Lab 05 breaks production on purpose.

## What This Proved

Promotion paths, environment gates, digest discipline. Continue with [Lab 05](05-rollback.md).
