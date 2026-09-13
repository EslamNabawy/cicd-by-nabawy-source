---
title: Build Systems
category: build
status: complete
difficulty: intermediate
prerequisites:
  - CI/CD Pipelines
related:
  - Artifact Management
  - Continuous Integration
---

<!-- icon: build -->
# Build Systems

> A build system turns source into runnable output deterministically: dependency resolution, compilation, bundling — the same inputs must always produce the same outputs.

## 1. What Is It?

Picking up from **[CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)**, where the build stage was defined — here is what actually runs inside it: Maven/Gradle (JVM), npm (JS), Go modules, Cargo — each resolving declared dependencies into a compiled/bundled artifact.

## 2. Hermetic Builds

Hermetic = sealed from the ambient machine (see glossary). Concretely: pinned dependency versions (lockfiles: `package-lock.json`, `pom.xml` versions, `go.sum`), clean container per build, no `latest` tags, no host-installed toolchains. Violation symptom: "works in CI, fails locally" in reverse — the build drank something from its environment.

## 3. Caching Done Right

Cache layers, fastest first: dependency cache keyed on lockfiles → remote build cache (Gradle remote, BuildKit registry cache) → artifact reuse (skip rebuild when inputs unchanged). Golden rule: the cache key must include every input; a stale key ships stale code silently.

## 4. Tool Notes

- **Maven/Gradle:** standard layouts, wrapper scripts (`mvnw`, `gradlew`) pin the toolchain itself — commit them.
- **npm:** `npm ci` (lockfile-exact) in CI, never `npm install`; cache `~/.npm`.
- **Docker builds:** BuildKit with `--secret` mounts and registry cache (see [pipelines BuildKit section](../06-ci-cd-pipelines/pipelines.md)); multi-stage so SDKs never ship in runtime images.

## 5. Failure Modes

- Unpinned deps → "it built yesterday"; fix with lockfiles + dependabot-style updates as PRs.
- Bloated images (SDK in prod) → slow pulls, huge attack surface; fix with multi-stage builds.
- Cache poisoning (stale key) → phantom green; fix by keying on lockfiles + periodic cache-bust verification.

## 6. Interview Notes

- Hermetic vs reproducible: sealed environment vs byte-identical output (reproducible is stricter).
- Why `npm ci` over `npm install` in CI.
- Multi-stage Docker: what ships vs what builds.

## Related Topics

- [CI/CD Pipelines](../06-ci-cd-pipelines/pipelines.md)
- [Artifact Management](../05-artifacts-and-packaging/artifact-management.md)
- [Continuous Integration](../02-continuous-integration/continuous-integration.md)

Deterministic builds produce trustworthy artifacts. Continue in **[Artifact Management](../05-artifacts-and-packaging/artifact-management.md)**.
