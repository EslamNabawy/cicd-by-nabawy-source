# Project Completion Plan — fill every gap

> Source: ROADMAP.md + TOPIC_INDEX.md planned + CONTENT_MAP.md planned + ICON registry MISSING.
> Rule per batch: md → indexes (TOPIC_INDEX/ROADMAP/GLOSSARY/CONTENT_MAP) → PDF → books.json → rebuild → QC → redeploy.

## Batch A — Expansions (no new files, 8 roadmap flips)

| # | File | Add | Flips |
|---|------|-----|-------|
| A1 | `06-ci-cd-pipelines/pipelines.md` | Runners deep-dive subsection (self-hosted vs managed, caches) + parallelism/dependencies/failure-handling expansion | Runners deep dive [x], Parallelism expand [x] |
| A2 | `05-artifacts-and-packaging/artifact-management.md` | Versioning schemes subsection (semver/SHA/build numbers) + SBOM/signing/provenance subsection | Versioning [x], SBOM [x] |
| A3 | `13-observability-and-feedback/observability-feedback.md` | SLI/SLO/alerting subsection + DORA metrics subsection | SLO expansion [x], DORA [x] |
| A4 | `15-platforms-and-tools/github-actions.md` | ARC scale-set example + self-hosted setup | ARC [x] |
| A5 | `15-platforms-and-tools/jenkins/jenkins-advanced.md` | Production topology subsection (HA controller, agent fleets, DR) | JCasC/prod topology [x] |
| PDFs rebuilt: 03, 04, 06, 17, 19 → site rebuild → redeploy | | | |

## Batch B — New concept files (7 files, 7 folders)

| # | File | Covers | Closes |
|---|------|--------|--------|
| B1 | `02-continuous-integration/continuous-integration.md` | CI discipline, PR gates, merge queues, trunk discipline | folder 02 |
| B2 | `03-build-systems/build-systems.md` | Maven/Gradle/npm, caching, hermetic builds, BuildKit link | folder 03 |
| B3 | `04-testing/testing-strategy.md` | Pyramid in pipelines: unit/contract/integration/E2E, flaky policy | folder 04 + TOPIC planned |
| B4 | `08-continuous-deployment/continuous-deployment.md` | Auto-to-prod prereqs, progressive delivery, kill criteria | folder 08 |
| B5 | `09-environments-and-release/environments-release.md` | Env topology, config vs code, release trains, promotion paths | folder 09 |
| B6 | `11-security/cicd-security.md` | Secrets, signing, SBOM, least privilege, supply-chain (links Jenkins/GHA specifics, no duplication) | folder 11 + TOPIC planned |
| B7 | `14-reliability-and-recovery/rollback-recovery.md` | Rollback procedures, MTTR drills, Jenkins backup/restore links | folder 14 + Delivery rollback [x] |
| PDFs 21–27 → manifest → rebuild → redeploy. Connectivity bridges wired both sides. | | | |

## Batch C — Labs (8 files) + reference

| # | Files | Format per lab (§19 of architect brief: Objective→What This Proved) |
|---|-------|------------------------------------------------------------------------|
| C1 | `16-labs/general/01-first-pipeline.md` … `05-rollback.md` | Vendor-neutral (mirrors ROADMAP labs 01–05) |
| C2 | `16-labs/jenkins/01-jenkinsfile.md`, `02-agents.md`, `03-credentials.md` | Jenkins hands-on (closes Jenkins labs [ ]) |
| C3 | `17-reference/jenkinsfile-reference.md` (stages/steps/agent/options quick ref) | folder 17 seed |
| PDFs 28–38 → manifest → rebuild → redeploy | | |

## Batch D — Cleanup + icons + final gate

| # | Task |
|---|------|
| D1 | Download 4 MISSING icons (server, terminal, troubleshooting, plugin — Lucide) → register → mapping READY |
| D2 | CONTENT_MAP: fix stale labels (PDF spec "not yet", 10 still planned, jenkins count, PDF mapping → per-file reality, website mapping → dist/read reality) |
| D3 | TOPIC_INDEX planned section → empty (all created); GLOSSARY sweep for new terms |
| D4 | PDF 01–08 series consolidation — only on explicit request (per-file set is canonical) |
| D5 | Final gate: full link check + full PDF QC + site validation + redeploy + report |

## Execution order

A → (verify + redeploy) → B → (verify + redeploy) → C → (verify + redeploy) → D → done. ALL BATCHES COMPLETE — final gate green, site live with 36 books.
