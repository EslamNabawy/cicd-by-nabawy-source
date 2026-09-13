---
title: "Lab 03 — Artifacts"
category: labs
status: complete
difficulty: intermediate
prerequisites:
  - Lab 02
  - Artifact Management
related:
  - Artifact Management
  - CI/CD Security
---

<!-- icon: artifact -->
# Lab 03 — Artifacts

## Objective

Build a Docker image once, tag it by commit SHA, push to GHCR, attach an SBOM — then prove staging and prod would run the same digest.

## Prerequisites

- Lab 02 green; a `Dockerfile` (multi-stage, `node:20-slim` runtime); concepts: [Artifact Management](../05-artifacts-and-packaging/artifact-management.md).

## Architecture

Merge to `main` → build image → tag `ghcr.io/<you>/<app>:sha-<short>` → push GHCR → generate SBOM → print digest (the deployable identity).

## Setup

Enable GitHub Packages (GHCR) on the repo; workflow needs `packages: write` permission.

## Step 1 — Build once, tag SHA

### Execute

```yaml
jobs:
  image:
    runs-on: ubuntu-latest
    permissions: { packages: write }
    steps:
      - uses: actions/checkout@v4
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: ${{ github.actor }}, password: ${{ secrets.GITHUB_TOKEN }} }
      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ghcr.io/${{ github.repository }}
          tags: type=sha,prefix=sha-
      - uses: docker/build-push-action@v6
        with: { push: true, tags: ${{ steps.meta.outputs.tags }} }
```

### Expected Result

GHCR shows `sha-<short>` tag; logs print the digest.

### Why

SHA tag = immutable identity; the digest (not `:latest`) is what every environment deploys (see [versioning](../05-artifacts-and-packaging/artifact-management.md)).

## Step 2 — Attach SBOM

### Execute

Add after push: `anchore/sbom-action@v0` on the pushed image; inspect the artifact.

### Expected Result

SBOM artifact lists every package inside the image.

### Why

The ingredient list that makes the next CVE answerable in minutes, not days.

## Verification

- [ ] GHCR holds an immutable SHA tag.
- [ ] Same digest referenced twice = same bytes.
- [ ] SBOM artifact present.

## Failure Scenarios

- 403 on push: missing `packages: write` — add the permission block.
- `latest` deployed somewhere: retag nothing; fix consumers to pin the digest.

## Cleanup

Keep images; they are small and prove immutability.

## What This Proved

Build-once identity, SHA discipline, SBOM habit. Continue with [Lab 04](04-deployment.md).
