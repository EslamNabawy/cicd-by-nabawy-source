# CONTENT-DRIVEN ICON DISCOVERY & ASSET MANAGEMENT

## 1. PURPOSE

Icons must be selected **from the actual content of the Markdown files**.

Do not start by downloading a generic collection of icons.

The workflow must be:

```text
Markdown Content
      ↓
Understand the Topics
      ↓
Identify Visual Concepts
      ↓
Determine Which Concepts Need Icons
      ↓
Search for Appropriate Free Icons
      ↓
Verify License
      ↓
Download SVG
      ↓
Store in Central Asset Library
      ↓
Register Asset
      ↓
Map Icon to Concept
      ↓
Use in HTML / PDF / Website
```

The Markdown content is the source of truth.

---

## 2. NEVER CHOOSE ICONS RANDOMLY

Do not choose icons based only on the filename or title of the Markdown file.

Read the actual content.

For example, if the Markdown contains:

```text
Jenkins
Pipeline
Agent
Stage
Build
Git
Docker
Testing
Deployment
Webhook
Credentials
```

analyze the content and determine which concepts actually benefit from visual representation.

Do NOT automatically create an icon for every word.

---

## 3. CONTENT ANALYSIS FIRST

Before generating or modifying a document, inspect the entire Markdown file.

Identify:

### Technologies

Examples:

```text
Jenkins
Git
GitHub
Docker
Kubernetes
AWS
Terraform
Prometheus
Grafana
```

### Technical concepts

Examples:

```text
Pipeline
Build
Artifact
Deployment
Testing
Security
Monitoring
Networking
Database
Container
```

### Processes

Examples:

```text
Commit
Build
Test
Package
Deploy
Monitor
Rollback
```

### Infrastructure

Examples:

```text
Server
Cloud
Container
Cluster
Node
Registry
Database
Network
```

### Actions

Examples:

```text
Upload
Download
Deploy
Run
Build
Test
Scan
Monitor
Configure
```

### Warnings / semantic states

Examples:

```text
Warning
Important
Tip
Success
Failure
Info
```

Use this analysis to determine the visual vocabulary of the document.

---

## 4. ICON DECISION RULE

For every identified concept, classify it as:

```text
REQUIRES ICON
OPTIONAL ICON
NO ICON
```

### REQUIRES ICON

Use when an icon materially improves understanding or navigation.

Examples:

```text
Jenkins
Git
Docker
Kubernetes
Cloud
Security
Deployment
Testing
Pipeline
Server
Database
```

### OPTIONAL ICON

Use when an icon can improve a visual component without creating clutter.

Examples:

```text
Build
Package
Monitoring
Configuration
Documentation
Reference
```

### NO ICON

Do not use icons for:

```text
Normal paragraphs
Every heading
Every sentence
Every bullet
Every technical term
Words that do not benefit visually
```

---

## 5. SEARCH FOR ICONS BASED ON SEMANTIC MEANING

Do not search only for the exact Markdown word.

Search using the concept.

For example:

```text
Markdown:
"artifact"

Search:
package icon
artifact package icon
software package icon
archive icon
```

For:

```text
"deployment"
```

search:

```text
deployment icon
rocket deploy icon
cloud deployment icon
server deployment icon
```

For:

```text
"pipeline"
```

search:

```text
pipeline icon
workflow icon
process flow icon
automation pipeline icon
```

The selected icon must represent the concept clearly.

---

## 6. TECHNOLOGY LOGOS VS CONCEPT ICONS

Use two different strategies.

## Technology

For:

```text
Jenkins
Git
GitHub
Docker
Kubernetes
AWS
Terraform
Grafana
Prometheus
```

prefer legitimate technology logos from:

* Official project repositories
* Official documentation
* Simple Icons
* Devicon
* Other reputable open-source sources

## Generic Concepts

For:

```text
Pipeline
Build
Test
Security
Deployment
Server
Database
Cloud
Package
Webhook
```

use a consistent general-purpose icon library such as:

* Lucide
* Tabler
* Heroicons
* Material Symbols
* Font Awesome Free
* Bootstrap Icons

Do not use technology logos for generic concepts.

---

## 7. APPROVED ICON SOURCE PRIORITY

Search sources in this order:

```text
1. Existing local asset library
2. Official technology/project assets
3. Simple Icons
4. Devicon
5. Lucide
6. Tabler Icons
7. Heroicons
8. Material Symbols
9. Font Awesome Free
10. Other reputable open-source icon libraries
```

Avoid random icon-download websites unless no suitable licensed alternative exists.

Do not download assets from sources where the license cannot be determined.

---

## 8. LICENSE VERIFICATION

Before downloading an icon, verify:

```text
Source
License
Usage permission
Attribution requirement
Modification requirement
Redistribution permission
```

Record the result.

Never assume:

```text
"Free download"
```

means:

```text
"Free to redistribute."
```

Those are not the same thing, because apparently even tiny pictures need legal paperwork.

---

## 9. PREFERRED FORMAT

Prefer:

```text
SVG
```

over:

```text
PNG
JPG
WEBP
GIF
```

SVG is preferred because it:

* Scales cleanly
* Works well in HTML
* Works well in PDFs
* Works well on high-DPI displays
* Can often inherit CSS colors
* Can be reused by the future website

---

## 10. CENTRAL ICON DIRECTORY

Store icons centrally:

```text
assets/
└── icons/
    ├── technology/
    │   ├── jenkins/
    │   ├── git/
    │   ├── github/
    │   ├── docker/
    │   ├── kubernetes/
    │   └── ...
    │
    ├── concepts/
    │   ├── pipeline/
    │   ├── build/
    │   ├── testing/
    │   ├── deployment/
    │   ├── security/
    │   ├── artifact/
    │   ├── server/
    │   └── ...
    │
    └── README.md
```

Do not create folders that are not needed.

> NOTE — current on-disk layout predates this spec (`ci-cd/`, `jenkins/`, `git/`, `docker/`, … flat by topic). Keep the existing layout; apply the `technology/` + `concepts/` split only if a reorganization is explicitly requested. Do not churn paths that PDFs already reference.

---

## 11. REUSE EXISTING ICONS

Before downloading anything:

```text
SEARCH LOCAL ICON LIBRARY
```

If an appropriate icon already exists:

```text
USE IT
```

Do not download duplicates.

Example:

```text
Existing:
assets/icons/concepts/deployment.svg

New Markdown:
"deployment"

→ Reuse deployment.svg
```

Do not create:

```text
deployment.svg
deployment-2.svg
deployment-new.svg
deploy-icon.svg
deploy-final.svg
```

---

## 12. ICON STYLE CONSISTENCY

The agent must maintain a consistent icon language.

For generic concepts, prefer one primary icon family.

For example:

```text
Lucide
```

may be used for:

```text
Pipeline
Build
Test
Deploy
Security
Server
Database
Cloud
```

while official logos are used for:

```text
Jenkins
Git
Docker
Kubernetes
```

Do not mix five unrelated generic icon styles.

---

## 13. ICON MANIFEST

Maintain:

```text
assets/icons/README.md
```

with an asset registry.

Example:

```markdown
# Icon Registry

| ID | Concept | Asset | Source | License | Usage |
|---|---|---|---|---|---|
| icon-jenkins | Jenkins | technology/jenkins/jenkins.svg | Jenkins | Verified license | Jenkins |
| icon-git | Git | technology/git/git.svg | Simple Icons | CC0 | Git |
| icon-pipeline | Pipeline | concepts/pipeline/pipeline.svg | Lucide | ISC | Pipelines |
| icon-test | Testing | concepts/testing/test.svg | Lucide | ISC | Testing |
| icon-deploy | Deployment | concepts/deployment/deployment.svg | Lucide | ISC | Deployment |
```

Include:

* ID
* Concept
* File path
* Source
* Original URL
* License
* Attribution requirement
* Where it is used

---

## 14. CONTENT → ICON MAPPING

Create a mapping layer.

Example:

```json
{
  "jenkins": "icons/technology/jenkins/jenkins.svg",
  "git": "icons/technology/git/git.svg",
  "pipeline": "icons/concepts/pipeline/pipeline.svg",
  "testing": "icons/concepts/testing/test.svg",
  "deployment": "icons/concepts/deployment/deployment.svg",
  "security": "icons/concepts/security/shield.svg"
}
```

This allows:

```text
Markdown concept
        ↓
Semantic concept ID
        ↓
Icon mapping
        ↓
SVG asset
        ↓
HTML/PDF/Website
```

Do not hardcode the same asset path throughout the application.

> NOTE — the machine-readable registry (`icon-registry.json`) does not exist yet. Create it when the second consumer (website renderer or PDF-02 build) needs programmatic resolution; until then the `assets/icons/README.md` table is the registry.

---

## 15. ICON USAGE MUST BE CONTEXTUAL

The agent should determine where an icon actually belongs.

Possible locations:

```text
Section header
Concept card
Technology card
Architecture diagram
Pipeline stage
Callout
Lab step
Comparison component
Book metadata
Navigation
```

Example:

```text
SOURCE
  [Git]

BUILD
  [Build]

TEST
  [Test]

ARTIFACT
  [Package]

DEPLOY
  [Deployment]

OBSERVE
  [Monitoring]
```

This is useful because the icons reinforce the pipeline.

Do not put:

```text
[Git] Git is a distributed version control system...
```

on every paragraph.

---

## 16. ANALYZE THE WHOLE DOCUMENT BEFORE DOWNLOADING

Do not download icons one section at a time without considering the entire Markdown file.

Instead:

```text
READ COMPLETE MARKDOWN
        ↓
BUILD CONCEPT LIST
        ↓
REMOVE DUPLICATES
        ↓
CHECK EXISTING ICONS
        ↓
DOWNLOAD MISSING ICONS
        ↓
APPLY ICONS THROUGHOUT DOCUMENT
```

This prevents duplicate downloads and inconsistent visual language.

---

## 17. CROSS-DOCUMENT REUSE

The icon system is global.

If:

```text
jenkins.svg
```

already exists because of:

```text
jenkins.md
```

and another document contains:

```text
Jenkins
```

reuse the same asset.

Do not download another Jenkins logo.

The same applies to:

```text
Git
Docker
Kubernetes
Security
Testing
Deployment
Pipeline
Server
Database
Cloud
```

---

## 18. ICON DISCOVERY WORKFLOW

For every new Markdown file:

```text
STEP 1
Read Markdown

STEP 2
Understand the document

STEP 3
Extract technologies

STEP 4
Extract important technical concepts

STEP 5
Extract major processes

STEP 6
Identify visual opportunities

STEP 7
Remove unnecessary icon candidates

STEP 8
Check existing icon library

STEP 9
Search approved sources for missing icons

STEP 10
Verify licenses

STEP 11
Download SVG assets

STEP 12
Register assets

STEP 13
Create concept → icon mappings

STEP 14
Apply icons to the document

STEP 15
Render HTML

STEP 16
Render PDF

STEP 17
Visually inspect

STEP 18
Fix missing, duplicated, or inappropriate icons
```

---

## 19. SEARCH QUERIES

Search queries should be generated from the actual content.

Example Markdown:

```text
Jenkins Pipeline uses stages, agents, credentials,
webhooks, Docker containers and automated tests.
```

The agent may derive:

```text
Jenkins logo
Pipeline icon
Stage/workflow icon
Agent/server icon
Credentials/lock icon
Webhook icon
Docker logo
Testing icon
```

But it must still decide which ones are actually useful.

---

## 20. DO NOT DOWNLOAD EVERYTHING YOU FIND

Search results may contain many possible icons.

Select the **best semantic match**, not every available variation.

For example:

```text
Pipeline
```

does not require:

```text
pipeline-1.svg
pipeline-2.svg
pipeline-3.svg
workflow.svg
process.svg
automation.svg
flow.svg
```

Select one appropriate icon.

---

## 21. ICON PRIORITY

When multiple icons represent the same concept, choose according to:

```text
1. Semantic accuracy
2. License clarity
3. Visual consistency
4. SVG quality
5. Simplicity
6. Reusability
7. Appropriate visual weight
```

Do not choose an icon merely because it looks impressive.

---

## 22. AVOID DECORATIVE ICONS

Do not download icons merely to fill empty space.

Every icon must answer:

> "What information does this icon communicate?"

If the answer is:

```text
"It looks nice."
```

do not use it.

---

## 23. ICONS IN DIAGRAMS

When the Markdown describes a process, architecture, or workflow, icons may be used to improve the diagram.

Example:

```text
Developer
   │
   ▼
[Git]
   │
   ▼
[Jenkins]
   │
   ▼
[Build]
   │
   ▼
[Test]
   │
   ▼
[Artifact]
   │
   ▼
[Deploy]
```

Use the same assets used elsewhere.

Do not create special duplicate icons only for diagrams unless absolutely necessary.

---

## 24. ICONS IN PDF GENERATION

The PDF generator must use the centralized asset library.

The HTML should reference:

```text
../assets/icons/...
```

or the appropriate relative path.

Do not embed random external icon URLs into the generated HTML.

This ensures:

```text
HTML
↓
PDF
```

works without requiring internet access.

---

## 25. ICONS IN WEBSITE GENERATION

The website must use the same centralized assets whenever possible.

Therefore:

```text
Markdown
     ↓
Concept
     ↓
Icon Registry
     ↓
SVG
   ↙   ↘
PDF   Website
```

The website should not independently download another icon for the same concept.

---

## 26. ALT TEXT

Icons that communicate information must have appropriate accessibility treatment.

For meaningful icons:

```html
<img
    src="..."
    alt="Jenkins"
>
```

For purely decorative icons:

```html
alt=""
```

Do not duplicate visible text unnecessarily in accessibility labels.

---

## 27. TECHNOLOGY LOGO RULE

When the Markdown contains a technology name, determine whether the visual should use:

```text
Official technology logo
```

or:

```text
Generic semantic icon
```

Example:

```text
Jenkins
→ Jenkins logo

Git
→ Git logo

Docker
→ Docker logo

Pipeline
→ Generic pipeline/workflow icon

Security
→ Generic shield/lock icon
```

Do not use a generic icon when a legitimate technology logo is more informative.

Do not use a technology logo for a generic concept.

---

## 28. ICON USAGE DENSITY

Maintain a controlled density.

Recommended:

```text
Major concept:
    Icon allowed

Major technology:
    Logo allowed

Section:
    Icon optional

Paragraph:
    Usually no icon

Bullet:
    Usually no icon

Sentence:
    No icon
```

The reader should never feel like they are reading an icon catalog.

---

## 29. ICON COLOR

Generic icons may adapt to the document theme.

For example:

```text
Original Theme
→ Theme accent

Light Theme
→ Theme-compatible dark/accent version
```

Use SVGs that support recoloring when practical.

Technology logos should preserve appropriate brand identity.

---

## 30. MISSING ICON HANDLING

If no suitable free icon exists:

```text
DO NOT:
- invent a fake logo
- use an emoji
- use a random copyrighted image
- download an unknown asset
```

Instead:

```text
Use an appropriate generic icon
```

or:

```text
Use no icon
```

Content quality is more important than visual decoration.

---

## 31. ICON QUALITY CHECK

Before accepting an asset:

```text
[ ] Correct concept
[ ] Correct category
[ ] Free/legal usage verified
[ ] SVG preferred
[ ] No watermark
[ ] No background unless needed
[ ] No unnecessary text
[ ] Good visual quality
[ ] Consistent style
[ ] Works in HTML
[ ] Works in PDF
[ ] Works on both themes
```

---

## 32. AUTOMATIC ICON AUDIT

Before finalizing a Markdown document, generate an internal audit:

```text
DOCUMENT:
Jenkins Pipelines

CONCEPTS FOUND:
Jenkins
Pipeline
Stage
Agent
Build
Testing
Credentials
Webhook
Docker

ICON STATUS:

Jenkins       → FOUND → jenkins.svg
Pipeline      → FOUND → pipeline.svg
Stage         → FOUND → workflow.svg
Agent         → FOUND → server.svg
Build         → FOUND → build.svg
Testing       → FOUND → test.svg
Credentials   → FOUND → lock.svg
Webhook       → FOUND → webhook.svg
Docker        → FOUND → docker.svg
```

If an icon is missing:

```text
MISSING:
Artifact

ACTION:
Search approved sources → verify license → download → register
```

---

## 33. DO NOT MODIFY MARKDOWN CONTENT UNNECESSARILY

Icon discovery must not alter the technical meaning of the Markdown.

If the Markdown contains:

```markdown
# Jenkins Pipeline
```

do not rewrite it simply to insert an icon.

The icon should be handled by the rendering/design layer whenever possible.

Prefer:

```text
Markdown
    ↓
Semantic rendering
    ↓
Icon added by renderer
```

rather than polluting the knowledge source with presentation-specific markup.

---

## 34. PRESENTATION SEPARATION

Maintain:

```text
CONTENT
```

separately from:

```text
VISUAL PRESENTATION
```

Markdown describes:

```text
Jenkins Pipeline
```

The design system decides:

```text
Jenkins logo
Pipeline icon
Layout
Color
Size
Position
```

This is critical because the same Markdown will later generate:

```text
PDF
Website
Potential mobile app
Potential eBook
```

---

## 35. WHEN TO ADD AN ICON TO MARKDOWN

Only add explicit icon metadata to Markdown if the renderer genuinely needs semantic information that cannot be inferred.

If needed, use metadata such as:

```yaml
icon: pipeline
```

instead of embedding raw image paths everywhere.

Example:

```yaml
---
title: Jenkins Pipelines
icon: jenkins
category: ci-cd
---
```

The renderer can then resolve:

```text
jenkins
    ↓
Icon Registry
    ↓
jenkins.svg
```

---

## 36. GLOBAL ICON REGISTRY

Maintain a machine-readable registry.

Example:

```json
{
  "jenkins": {
    "type": "technology",
    "asset": "/assets/icons/technology/jenkins/jenkins.svg",
    "source": "verified-source",
    "license": "verified-license"
  },
  "pipeline": {
    "type": "concept",
    "asset": "/assets/icons/concepts/pipeline/pipeline.svg",
    "source": "verified-source",
    "license": "verified-license"
  }
}
```

This registry becomes the central source for:

```text
PDF
HTML
Website
Search
Book cards
Diagrams
```

---

## 37. FINAL PRINCIPLE

The agent must follow:

```text
CONTENT FIRST
     ↓
SEMANTIC ANALYSIS
     ↓
ICON DISCOVERY
     ↓
LICENSE VERIFICATION
     ↓
ASSET DOWNLOAD
     ↓
CENTRAL REGISTRATION
     ↓
CONSISTENT REUSE
     ↓
PDF + WEBSITE
```

Never:

```text
Download random icons
     ↓
Try to find places to use them
```

The Markdown determines the required visual vocabulary.

The icon library serves the content.

The content does not exist to justify the icon library.

---

## 38. FINAL VALIDATION

Before completing any document:

```text
[ ] Markdown was fully analyzed
[ ] Important technologies identified
[ ] Important concepts identified
[ ] Icon candidates were evaluated
[ ] Existing assets were checked first
[ ] Missing assets were searched
[ ] Licenses were verified
[ ] Required assets were downloaded
[ ] Assets were stored centrally
[ ] Asset registry updated
[ ] Concept → icon mapping updated
[ ] Duplicate assets avoided
[ ] Icons are semantically appropriate
[ ] Icons are not overused
[ ] No emoji used as technical icons
[ ] HTML references local assets
[ ] PDF renders all icons correctly
[ ] Website can reuse the same assets
[ ] Both themes support the icons
[ ] Accessibility requirements are satisfied
```

## GOLDEN RULE

> **Read the Markdown first. Understand what it teaches. Identify the concepts that genuinely benefit from visual representation. Then search for the smallest, highest-quality set of properly licensed icons needed to communicate those concepts. Download them, register them, reuse them consistently, and never use icons merely to fill space.**

---

# PART B: INSTRUCTION FILE DISCOVERY & ENFORCEMENT

> This file (`CI-CD/ICON_ASSET_SPEC.md`) IS the project's authoritative icon instruction file — the equivalent of the `ICON_INSTRUCTIONS.md` referenced below. Do not create a duplicate. Do not rename without explicit request.

## B1. FIND THE ICON INSTRUCTION FILE

Do NOT assume the icon instruction file has a specific filename. The agent MUST first inspect the project structure and identify the Markdown file containing icon usage and asset-management rules (here: `CI-CD/ICON_ASSET_SPEC.md`, referenced from `CONTENT_MAP.md`). Judge authoritativeness by content, location, and references — not filename.

## B2. DISCOVERY PROCESS

```text
Inspect project → find rules Markdown files → identify icon-rules file →
read it completely → use as implementation contract
```

Do NOT create another instruction file if one already contains these rules.

## B3. MANDATORY READ-BEFORE-WORK

Before modifying icons: (1) read this file completely, (2) inspect the icon registry (`assets/icons/README.md`), (3) inspect existing mappings/usage, (4) inspect the Markdown content, (5) inspect existing rendered output — then begin.

## B4. MANDATORY RE-READ

After implementing, return to this SAME file: implementation → icon audit → re-read → compliance check → final build. Mandatory.

## B5. EXISTING PROJECT REPAIR

When these instructions land in an existing project, assume icon implementation is incomplete. Audit: existing Markdown → HTML → PDF → icons → registry → mappings. Compare everything. "Icons exist" ≠ "implementation complete."

## B6. MISSING ICON REPAIR

Per document: concept → benefits from icon? → exists? → reuse, else search/download → register → map → integrate → render → verify.

## B7. ACTUALLY APPLY THE RULES

Never stop at reading or updating this file. If the project has 10 important concepts and 3 icons, investigate the remaining 7.

## B8. FINAL VERIFICATION

```text
[ ] Correct instruction file discovered/read fully
[ ] Existing icons + mappings audited
[ ] Markdown content analyzed
[ ] Missing concepts identified + repaired
[ ] New assets registered, mappings updated
[ ] HTML regenerated, PDF regenerated
[ ] Icon visibility verified (rendered, not just referenced)
[ ] Same instruction file re-read; implementation complies
```

## B9. FINAL RULE

```text
DISCOVER → READ → APPLY → AUDIT → REPAIR → RE-READ → VERIFY → FINISH.
```

The filename is an implementation detail. The instructions are what matter.

---

# PART C: ICON SYSTEM REPAIR & ENFORCEMENT

## C1. PURPOSE

This file is the authoritative instruction file for the project's icon system. Every renderer and workflow handling icons MUST follow it. Goal: not a library — **the right icon visibly used for the right concept in the generated document**.

## C2. PRIORITY

```text
1. This file (ICON_ASSET_SPEC.md)
2. Project-wide design/documentation rules
3. Existing icon registry
4. Existing content structure
5. Agent implementation preferences
```

## C3. READ → IMPLEMENT → AUDIT → RE-READ → FINALIZE

Read this file + Markdown + registry + mappings + generated HTML before work; re-read before finalizing. Prevents read-once-forget-half behavior.

## C4. REPAIR MODE (existing projects)

First execution performs a complete audit: scan all Markdown → extract visual concepts → check current usage → find missing → repair. Never assume existing docs comply.

## C5. COVERAGE, NOT EXISTENCE

`pipeline.svg exists` ≠ `pipeline concept uses it`. Verify usage in rendered output. Per document mark each concept USED / NOT NEEDED (with reason) / MISSING. No unexplained MISSING entries allowed.

## C6. DO NOT BE TOO CONSERVATIVE

"Don't overuse" ≠ "use almost none." Actively icon: architecture, workflows, pipelines, technology lists, concept cards, labs, comparisons, callouts, navigation, book metadata — where a concept meets the threshold (major technology/component/stage/action, appears in a visual workflow, repeatedly referenced, worth distinguishing).

## C7. HIGH-PRIORITY CONCEPTS

Technologies (Jenkins, Git, GitHub, Docker, K8s, clouds, Terraform, Prometheus, Grafana, Argo CD) → official logos. Pipeline concepts (source→feedback), infrastructure (server→registry), security (auth→shield), operations (logs→rollback) → one consistent generic family (Lucide). Icons follow content — never add the whole list blindly.

## C8. DOWNLOADING/REGISTERING/REFERENCING IS NOT COMPLETION

Completion = downloaded + registered + mapped + referenced + rendered + **visibly verified in output**. If verification fails: repair → render again → verify again.

## C9. REPAIR COMMANDS (conceptual)

`icon-audit`: scan Markdown, check mappings/assets/usage, report missing/unused/broken/unlicensed. `icon-repair`: analyze → reuse → download approved → register → map → integrate → rebuild → audit. If auto-download is impossible, emit an actionable missing-assets report — never silently skip.

## C10. BUILD GATE

BUILD = PASS only when: audit clean, no broken refs, no missing required icons, no unverified production assets, no duplicates, HTML renders, PDF renders. Else FAIL (or WARNING for optional-only gaps).

## C11. EVOLVE THIS FILE

Recurring problem discovered (unused downloads, wrong category, diagram gaps, duplicate logos, broken PDF SVGs, theme issues)? Add a preventive rule here. Never edit this file to make a bad implementation look compliant — fix implementation first.

## C12. CHANGE LOG

### 2026-09-09
- Initial spec: content-driven discovery, licensing, central library, registry, density, presentation separation.
- Added Part B: discovery-by-content (this file declared authoritative, no duplicates), read-before-work, mandatory re-read, repair assumptions.
- Added Part C: repair mode, coverage-not-existence, USED/NOT-NEEDED/MISSING audits, build gate, icon-audit/icon-repair commands, change log.
- Repair run on PDF-01: added build-stage icon (`hammer.svg`), wired stage icons (git/build/test/artifact) into pipeline component; Jenkins logo NOT NEEDED (generic foundations doc, no Jenkins content).
- Stage/flow repair on PDF-01: cover 6/6, lifecycle strips, §12 flow (new `database.svg` → `registry` id), failure flow 4/4; lanes + APPROVAL intentionally text-only with recorded reasons.

---

# PART D: MARKDOWN ICON PLACEMENT & ANNOTATION

## D1. OBJECTIVE

Modify the Markdown files themselves so they explicitly state where icons belong — via semantic annotations. Markdown answers WHAT concept + WHERE; registry answers WHICH svg; renderer answers HOW. Never hardcode asset paths into Markdown.

## D2. AUTHORITATIVE RULES DISCOVERED

Project rules: `DOCUMENTATION_RULES.md` (structure/terminology) → this file (icon system). Most-specific applicable rule wins; higher rules still respected. This Part D was read before editing (D-spec + registry + all content files inspected).

## D3. ANNOTATION FORMAT (only mechanism used)

```markdown
<!-- icon: <concept-id> -->
```

placed immediately BEFORE the heading/callout it belongs to. No `<img>`, no `![alt](path)`, no raw `/assets/...` paths in Markdown. No frontmatter `icon:` duplication — heading annotations only. Never inside fenced code blocks. Concept-ids are canonical, reused verbatim (`jenkins`, not `jenkins-logo`/`jenkins-ci`).

## D4. CANONICAL CONCEPT IDS (this project)

Technologies → `jenkins` `git` `github` `docker`. Concepts → `pipeline` `build` `testing` `deployment` `security` `monitoring` `artifact` `server` `terminal` `troubleshooting` `plugin` `webhook`. States/callouts → only where the design system supports them (none wired yet — do not annotate callouts until renderer supports it).

## D5. PLACEMENT DENSITY

Annotate: document title (main technology/concept), major architecture components, workflow/stage sections, labs, security/troubleshooting sections. Do NOT annotate: normal paragraphs, bullets, commands, table rows, repeated mentions, every heading. One annotation per concept per document unless genuinely distinct sections.

## D6. CONTENT UNTOUCHED

Annotations are presentation-semantic only: no rewritten explanations, no changed commands/code/links/diagrams/terminology. Markdown stays valid and renders identically without the renderer.

## D7. MISSING-ASSET PROTOCOL

Annotate anyway with the canonical id; record the id in `assets/icons/README.md` → Missing identifiers. Never fake a path, invent an SVG, or use emoji. Current missing: `server` `terminal` `troubleshooting` `plugin` (`artifact` resolved → `general/package.svg`).

## D8. ANNOTATION RUN LOG — 2026-09-09 (all KB content files)

cicd-overview `pipeline` · git-branching-pull-requests `git`+`webhook` · pipelines `pipeline`+`build`+`testing`+`security`+`docker` · artifact-management `artifact` · continuous-delivery `deployment` · observability-feedback `monitoring` · jenkins/README `jenkins` · jenkins-architecture `jenkins`+`docker` · jenkins-setup `jenkins`+`terminal` · jenkins-pipelines `jenkins`+`docker` · jenkins-agents `server` · jenkins-credentials `security` · jenkins-plugins `plugin` · jenkins-webhooks `webhook` · jenkins-security `security` · jenkins-troubleshooting `troubleshooting` · jenkins-groovy-cheatsheet: none (reference tables, visual noise) · github-actions `github`+`server`+`terminal`.

## D9. STAGE/FLOW ICON REPAIR RUN — 2026-09-09 (PDF-01)

Cover vpipe 6/6 · p2 lifecycle strip 6/6 · p5 stages 4/4 · p6 lanes 0 (intentional: color-coded environment tracks, no matching asset) · p6 flow 5/6 (APPROVAL intentionally text-only: decision gate, ◌+amber is its language) · p8 §12 flow 5/5 (new `database.svg` for REGISTRY) · p9 failure flow 4/4 · p10 map strip 4/4. New id: `registry` → `general/database.svg`. Still missing: `server` `terminal` `troubleshooting` `plugin`.
