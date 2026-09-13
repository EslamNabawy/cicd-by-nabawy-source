---
title: CI/CD Security
category: security
status: complete
difficulty: advanced
prerequisites:
  - Artifact Management
  - Jenkins Credentials
related:
  - Artifact Management
  - Jenkins Security
---

<!-- icon: security -->
# CI/CD Security

> The pipeline is production infrastructure with production secrets and the power to ship code — attack it like one: least privilege, signed artifacts, verified supply chain.

## 1. What Is It?

Picking up from **[Environments & Release](../09-environments-and-release/environments-release.md)**, whose zones carry real credentials — the pipeline itself is the highest-value target in the estate: it holds deploy keys, signs releases, and runs attacker-influenced PR code.

## 2. Secrets Discipline

- Store in managers (Vault, cloud KMS, Jenkins credentials store, GitHub environments) — never in repos, images, logs, or chat.
- Scope narrowly (per-env, per-job), rotate on schedule and on any leak, audit every access.
- PR builds from forks get zero production secrets — credential-free sandboxes only (see [Jenkins Agents](../15-platforms-and-tools/jenkins/jenkins-agents.md) trust boundary).

## 3. Signing, SBOM & Provenance

Build once, then: sign the digest (cosign), generate the SBOM (Syft/Trivy), attest provenance (SLSA: who built, from which commit, in which pipeline). Deploy policies admit only signed, attested images — see [Artifact Management](../05-artifacts-and-packaging/artifact-management.md). When the next CVE lands, query SBOMs to find affected digests in minutes.

## 4. Least Privilege Everywhere

- CI tokens: per-repo, minimal scopes, short TTL (OIDC federation beats long-lived keys — workloads mint credentials, nobody stores them).
- Pipeline permissions: `GITHUB_TOKEN` minimal scopes; Jenkins agents can't read other jobs' secrets (agent→controller deny).
- Humans: matrix authorization, SSO + MFA, no shared admin accounts, no standing prod access without review.

## 5. Supply-Chain Gates

Pin everything: action SHAs (not `@v4` tags), base image digests (not `:latest`), plugin versions, lockfiles. Verify checksums on download. Each PR that bumps a dependency re-runs the full gate — Dependabot PRs are untrusted code until proven otherwise.

## 6. Failure Modes

- Secret in git history → rotate immediately; history rewrites don't unsee it (it's cloned everywhere).
- Floating tags (`:latest`, `@v4`) → silent supply-chain swaps; pin digests/SHAs.
- Over-permissioned CI token → one compromised workflow owns the org; scope to the repo, expire fast.
- Unsigned images admitted → provenance theater; enforce admission, don't just generate attestations.

## 7. Interview Notes

- OIDC federation vs long-lived keys for CI auth.
- Design fork-PR isolation for a public repo with deploy secrets.
- SBOM in incident response: CVE lands at 2am, what do you query first?

## Related Topics

- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Jenkins Security](../15-platforms-and-tools/jenkins/jenkins-security.md)
- [GitHub Actions](../15-platforms-and-tools/github-actions.md)

Locked down — now plan for when things break anyway. Continue in **[Rollback & Recovery](../14-reliability-and-recovery/rollback-recovery.md)**.
