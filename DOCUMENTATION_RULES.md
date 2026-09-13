# Documentation Rules (Summary)

> Full architect brief lives with the maintainer. This file enforces what matters for contributors.

## Source of Truth

```text
SOURCE MATERIAL → KNOWLEDGE BASE (this Markdown) → PDF / WEBSITE
```

Never add knowledge directly to a PDF or website that contradicts this Markdown. Update Markdown first.

## File Philosophy

- Smallest number of files that gives the clearest architecture.
- Merge strongly related topics (Pipeline + Stages + Jobs + Runners → one file).
- Split only on conceptual boundaries, not heading count.
- Kebab-case filenames: `continuous-delivery.md`, never `CICD_Final.md`.

## Terminology (Binding)

| Term | Meaning |
|------|---------|
| Pipeline | The automated workflow |
| Stage | Logical phase of a pipeline |
| Job | Unit of executable work |
| Step | Operation inside a job |
| Runner / Agent | Execution environment |
| Artifact | Generated, versioned output |
| Registry | Stores and distributes artifacts |
| Environment | Target runtime context |
| Promotion | Move validated artifact toward next environment |
| Release | Version made available for deployment/users |
| Deployment | Installing/running a release in an environment |

Vendor-neutral concepts first, platform implementations second (`GitHub Actions`, `GitLab CI`, `Jenkins` map onto the generic model).

## File Structure

Adapt this template; omit unsupported sections, never leave empty ones:

```markdown
# Topic Name

> One-sentence definition.

## 1. What Is It?
## 2. Why Does It Exist?
## 3. Where Does It Fit?
## 4. Core Concepts
## 5. How It Works
## 6. Architecture / Flow
## 7. Example
## 8. Commands / Configuration
## 9. Failure Modes
## 10. Troubleshooting
## 11. Best Practices
## 12. Common Misconceptions
## 13. Real-World Scenario
## 14. Interview / Exam Notes
## 15. Related Topics
```

## Jenkins / Platform Rules (Binding)

- Concepts stay vendor-neutral (`06-ci-cd-pipelines/` explains *what a pipeline is*). Jenkins files under `15-platforms-and-tools/jenkins/` explain only *how Jenkins implements it*.
- Litmus test: if a paragraph is true for GitHub Actions too, it belongs in the generic doc — not in Jenkins.
- No `jenkins-*` files outside `15-platforms-and-tools/jenkins/`. No vendor folders until material justifies them (`other-tools/` stays planned).
- Every Jenkins doc links back to its generic parent (e.g. jenkins-pipelines → `06-ci-cd-pipelines/pipelines.md`).
- Jenkins docs feed PDF 06 (core) + PDF 07 (advanced); never let PDF order rename files.

## Standards

- Context per topic: WHAT, WHY, WHERE, WHEN, HOW, producer, consumer, failure modes.
- Mermaid for diagrams; labeled code blocks (` ```yaml `, ` ```bash `); comparison tables.
- PDF-aware: no walls of text, no ultra-wide tables, no interactive-only content.
- Website-aware: stable filenames, meaningful headings, relative links only, no knowledge hidden in images.
- Every major doc ends with `Related Topics` using relative links to files that exist.
- New terms → add row to `GLOSSARY.md`. New coverage → update `TOPIC_INDEX.md` + `ROADMAP.md`.

## Content Clarity (Binding)

- Clearer, not longer: every added sentence must remove ambiguity, explain a relationship, clarify responsibility, or make an example understandable. No trivia, filler, or repeated definitions.
- No vague verbs: expand "manages/handles/runs/stores" into WHAT + HOW + result. Explain WHY behind every "use X" rule in one sentence.
- Terms before use: first mention of jargon (hermetic, SBOM, SLO, DORA, digest, GHCR, OIDC…) gets a one-clause definition; hard terms also get a `GLOSSARY.md` row.
- WHO does WHAT: when components interact, name the actor per step (controller schedules, agent executes, registry stores).
- Relationships over isolation: cross-link related docs instead of re-explaining; keep explanations next to the concept they explain.
- Commands/configs carry context: what it does + when to use it + one-line mechanism. Diagrams get a one-sentence reading guide.
- If already clear, leave it alone.
