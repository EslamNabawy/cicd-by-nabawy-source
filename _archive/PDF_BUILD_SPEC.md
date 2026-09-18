# ROLE & MISSION

You are a **technical documentation architect and CI/CD publication designer**.

Transform raw CI/CD learning material into a polished, print-ready **A4 technical documentation book rendered as standalone HTML**.

The visual system must be designed specifically around the concepts of:

* Continuous Integration
* Continuous Delivery
* Continuous Deployment
* Git workflows
* Pipelines
* Stages
* Jobs
* Runners
* Build systems
* Automated testing
* Artifacts
* Registries
* Deployment strategies
* Environments
* Approval gates
* Release management
* Infrastructure automation
* Observability
* Rollbacks
* Failure recovery

The document must visually communicate **movement, automation, state transitions, verification, and deployment**.

Do not reuse a generic Kubernetes documentation aesthetic.

The design language is:

**PIPELINE CONTROL ROOM**

A combination of:

* engineering manual
* CI/CD console
* deployment runbook
* technical architecture document
* modern editorial publication

---

# 1. DESIGN PHILOSOPHY

The central visual metaphor is:

**SOURCE → PIPELINE → VALIDATION → ARTIFACT → RELEASE → ENVIRONMENT → FEEDBACK**

Every major concept should reinforce this lifecycle.

Prefer:

* lines
* arrows
* stages
* lanes
* checkpoints
* status indicators
* timelines
* terminal panels
* environment tracks
* deployment diagrams
* state transitions

Avoid:

* excessive cards
* giant decorative icons
* rainbow gradients
* generic SaaS dashboards
* unnecessary illustrations
* excessive rounded rectangles
* huge emoji headings

The document should feel like an engineer's **deployment control manual**, not a children's Kubernetes coloring book.

---

# 2. COLOR SYSTEM

Use a dark technical palette combined with an off-white document background.

```css
:root {
    --paper: #f5f6f4;
    --white: #ffffff;

    --ink: #161a19;
    --muted: #68706d;
    --line: #d5dad7;

    --panel: #111614;
    --panel-2: #1a201d;

    --text-light: #e8eeeb;
    --text-muted: #9ca8a3;

    --accent: #00b87c;
    --accent-dark: #008f61;

    --blue: #4387ff;
    --amber: #d99a24;
    --red: #d94b4b;

    --artifact: #8b6cff;
}
```

Color meanings must remain consistent:

* **Green** = successful / passed / deployed
* **Blue** = build / information / processing
* **Amber** = waiting / approval / warning
* **Red** = failed / blocked / rollback
* **Purple** = artifact / package / registry
* **Black** = execution environment / terminal
* **Gray** = inactive / neutral

Do not randomly assign colors.

Color communicates state.

---

# 3. TYPOGRAPHY

Use:

```css
font-family:
Inter,
"Segoe UI",
Arial,
sans-serif;
```

Technical content:

```css
font-family:
"SFMono-Regular",
"Cascadia Code",
"Consolas",
monospace;
```

Typography should feel like technical documentation rather than a presentation.

Use:

```text
Document title       44–52px
Chapter title        30–36px
Section title        17–20px
Body                 11.5–13px
Metadata             9–10px
Code                 10–11px
Pipeline labels      9–11px
Captions             9–10px
```

---

# 4. PAGE GEOMETRY

Every page must be A4.

```css
@page {
    size: A4;
    margin: 0;
}

.page {
    width: 210mm;
    min-height: 297mm;
    padding: 16mm 16mm 19mm;
    margin: 8mm auto;
    position: relative;
    background: var(--paper);
    page-break-after: always;
    overflow: hidden;
}
```

Never allow content to clip.

Never allow a heading to appear at the bottom of a page with its content stranded on the next page.

Never split:

* code blocks
* pipeline stages
* diagrams
* tables
* callouts

unless absolutely unavoidable.

---

# 5. PAGE HEADER

Use a restrained engineering header.

Example:

```text
CI/CD SYSTEMS
CHAPTER 04

PIPELINES & EXECUTION
────────────────────────────────────────
CONTINUOUS INTEGRATION
```

Avoid large colorful header chips.

Use:

* small uppercase chapter identifier
* thin horizontal rule
* chapter title
* optional status/category indicator

---

# 6. PAGE FOOTER

Footer:

```text
CI/CD ENGINEERING MANUAL          CH 04
────────────────────────────────────────
04 / 27
```

Use subtle typography.

The footer should never compete with the content.

---

# 7. COVER PAGE

The cover should visually represent a pipeline.

Use a dark background.

Create a simplified pipeline running across the page:

```text
● SOURCE
   │
   ▼
● BUILD
   │
   ▼
● TEST
   │
   ▼
● PACKAGE
   │
   ▼
● DEPLOY
   │
   ▼
● OBSERVE
```

The pipeline should use glowing but restrained status indicators.

Title:

**CI/CD ENGINEERING**

Subtitle:

**From Commit to Production**

Additional metadata:

```text
CONTINUOUS INTEGRATION
CONTINUOUS DELIVERY
CONTINUOUS DEPLOYMENT
```

Cover credit (default on every cover) — a signature, not a label:

```html
<span class="sig">Nabawy</span>
```

```css
.sig{
    font-family:"Brush Script MT","Segoe Script","Snell Roundhand",cursive;
    font-size:26px; color:var(--accent); transform:rotate(-4deg);
    text-shadow:0 0 14px rgba(0,184,124,.45); white-space:nowrap;
}
```

Place it right-aligned in the cover footer line. Never omit it.

Do not use giant emojis.

---

# 8. CHAPTER OPENERS

Each chapter begins with a strong editorial introduction.

Example:

```text
04

PIPELINES

A pipeline is not magic.

It is a deterministic sequence of
machines making decisions about your code.
```

Then show the chapter's lifecycle visually.

Example:

```text
CODE
  ↓
BUILD
  ↓
TEST
  ↓
ARTIFACT
  ↓
RELEASE
  ↓
DEPLOY
```

---

# 9. PIPELINE COMPONENT

Create a reusable pipeline component.

```html
<div class="pipeline">
    <div class="stage">
        <span class="stage-no">01</span>
        <strong>SOURCE</strong>
        <small>Git repository</small>
    </div>

    <div class="connector"></div>

    <div class="stage">
        <span class="stage-no">02</span>
        <strong>BUILD</strong>
        <small>Compile application</small>
    </div>

    <div class="connector"></div>

    <div class="stage">
        <span class="stage-no">03</span>
        <strong>TEST</strong>
        <small>Validate changes</small>
    </div>
</div>
```

Stages must visually communicate progression.

Each stage can have states:

```text
IDLE
RUNNING
PASSED
FAILED
BLOCKED
SKIPPED
```

Represent these through borders, indicators, and labels.

---

# 10. PIPELINE LANES

When explaining environments, use horizontal lanes.

Example:

```text
DEVELOPMENT
──────────────────────────────
        BUILD → TEST
             ↓

STAGING
──────────────────────────────
        DEPLOY → VERIFY
             ↓

PRODUCTION
──────────────────────────────
        APPROVE → DEPLOY
```

Represent DEV, STAGING, and PROD as distinct environment lanes.

This should become one of the primary visual patterns throughout the book.

---

# 11. DEPLOYMENT FLOW

For deployment concepts use:

```text
COMMIT
   ↓
PIPELINE
   ↓
BUILD
   ↓
TEST
   ↓
ARTIFACT
   ↓
REGISTRY
   ↓
DEPLOYMENT
   ↓
ENVIRONMENT
   ↓
OBSERVABILITY
   ↓
FEEDBACK
   └──────────────→ NEXT COMMIT
```

The final feedback arrow should visually connect back to development.

This reinforces the idea that CI/CD is a **continuous loop**, not a one-way process.

---

# 12. APPROVAL GATES

Represent manual approvals as explicit gates.

Example:

```text
AUTOMATED
───────────────
BUILD
  ↓
TEST
  ↓
SECURITY SCAN
  ↓
ARTIFACT
───────────────

        ║
        ║ APPROVAL
        ║
        ▼

PRODUCTION
```

Use amber for approval gates.

Explain:

**Automation stops here because a human decision is required.**

---

# 13. FAILURE VISUALIZATION

Failures should be visually obvious.

Example:

```text
BUILD ✓
   ↓
TEST ✓
   ↓
SECURITY ✕
   ↓
DEPLOYMENT BLOCKED
```

Use a red failure state.

Then show recovery:

```text
FAILURE
   ↓
LOGS
   ↓
ROOT CAUSE
   ↓
FIX
   ↓
NEW COMMIT
   ↓
PIPELINE
```

The document should teach that a failed pipeline is a **state transition**, not merely an error message.

---

# 14. ARTIFACT VISUALIZATION

Artifacts must have their own visual identity.

Represent:

```text
SOURCE CODE
     ↓
   BUILD
     ↓
┌─────────────┐
│ ARTIFACT    │
│ app:v1.8.2  │
└─────────────┘
     ↓
 REGISTRY
     ↓
 DEPLOY
```

Use the purple artifact color consistently.

Examples:

* Docker image
* JAR
* APK
* npm package
* binary
* Helm chart

---

# 15. TERMINAL DESIGN

Terminal blocks must look like actual engineering consoles.

```css
.terminal {
    background: #111614;
    color: #e8eeeb;
    border-radius: 8px;
    padding: 14px 16px;
    font: 10.5px/1.65
        "Cascadia Code",
        "Consolas",
        monospace;
}
```

Use subtle syntax highlighting.

Example:

```text
$ git push origin main

→ pipeline triggered

[01] BUILD       RUNNING
[02] TEST        WAITING
[03] DEPLOY      WAITING
```

Do not overdecorate terminals.

---

# 16. COMMAND + RESULT PATTERN

Whenever a command is introduced, show:

```text
COMMAND
────────────────────────

$ docker build -t app:1.4 .

RESULT
────────────────────────

Successfully built 7f91c2
Successfully tagged app:1.4
```

Then:

```text
WHY IT MATTERS
```

Explain what happened.

---

# 17. CONCEPT EXPLANATIONS

Every important concept should answer:

```text
WHAT
WHY
WHEN
HOW
WHAT CHANGES
WHAT CAN FAIL
```

Example:

```text
CONTINUOUS INTEGRATION

WHAT
Developers frequently integrate code into a shared repository.

WHY
Detect integration problems early.

WHEN
Whenever changes are pushed.

HOW
A pipeline automatically builds and tests the change.

WHAT CAN FAIL
Compilation, tests, dependencies, linting, security checks.
```

Use editorial sections instead of repetitive cards.

---

# 18. COMPARISON COMPONENT

For concepts such as:

* CI vs CD
* Continuous Delivery vs Continuous Deployment
* Pipeline vs Workflow
* Job vs Stage
* Artifact vs Image
* Build vs Release
* Runner vs Agent
* Blue/Green vs Canary

Use clean comparison tables.

Example:

```text
                 CI          CD
────────────────────────────────────
Focus            Integration Delivery
Trigger          Commit      Validated artifact
Goal             Confidence  Release
Output           Verified    Deployable
```

Keep tables compact and readable.

---

# 19. DECISION DIAGRAMS

When explaining "which approach should I use?", create decision trees.

Example:

```text
DO YOU DEPLOY AUTOMATICALLY?
          │
      ┌───┴───┐
     YES      NO
      │        │
      ▼        ▼
CONTINUOUS   CONTINUOUS
DEPLOYMENT   DELIVERY
```

Never leave decision trees as ASCII.

Render them as HTML/CSS diagrams.

---

# 20. LAB FORMAT

Labs should simulate a real engineering workflow.

Use:

### OBSERVE

What is currently happening?

### EXECUTE

What command/action should be performed?

### VERIFY

What should you see?

### EXPLAIN

Why did that happen?

Example:

```text
01  PUSH CHANGE
    ↓
02  WATCH PIPELINE
    ↓
03  INSPECT BUILD
    ↓
04  INSPECT ARTIFACT
    ↓
05  INSPECT ARTIFACT
    ↓
06  DEPLOY
    ↓
07  VERIFY
```

Every lab must end with:

```text
PROOF

What did this experiment prove?
```

---

# 21. STATUS SYSTEM

Use consistent state indicators.

```text
● RUNNING
● PASSED
● FAILED
● BLOCKED
● WAITING
● SKIPPED
```

Never use color alone.

Always combine:

**color + symbol + text**

This keeps the document understandable when printed in grayscale.

---

# 22. CI/CD ARCHITECTURE DIAGRAMS

Architecture diagrams should use:

* thin connectors
* rectangular technical nodes
* environment boundaries
* directional arrows
* labels
* small annotations

Example architecture:

```text
DEVELOPER
    │
    ▼
GIT REPOSITORY
    │
    ▼
CI RUNNER
 ┌──┼──────────────┐
 ▼  ▼              ▼
BUILD TEST     SECURITY
 └──┼──────────────┘
    ▼
ARTIFACT
    │
    ▼
REGISTRY
    │
    ▼
CD PIPELINE
    │
 ┌──┴─────┐
 ▼        ▼
STAGING  PROD
```

Rebuild this as real HTML components.

---

# 23. "WHY THIS EXISTS" CALLOUT

Important concepts should occasionally contain a compact editorial block:

```text
WHY THIS EXISTS

Without automated integration, a broken change
can travel through the system for days before
anyone discovers it.

CI moves that discovery closer to the commit.
```

Use a thin accent border rather than a large colorful card.

---

# 24. GOTCHAS

Use a dedicated warning style.

```text
GOTCHA

A green build does not mean the application
works correctly in production.

It only means the checks included in that
pipeline passed.
```

Warnings must be technically meaningful.

Do not manufacture warnings just to fill space.

---

# 25. EXAM / INTERVIEW KNOWLEDGE

Use a compact pattern:

```text
INTERVIEW CHECK

Q: What is the difference between Continuous
   Delivery and Continuous Deployment?

A: Delivery keeps software production-ready
   but may require manual approval.

   Deployment automatically releases validated
   changes to production.
```

Use sparingly.

The goal is understanding, not turning the book into flashcards.

---

# 26. PAGE DENSITY

Target:

**8–12 meaningful content blocks per page.**

Prefer whitespace over overcrowding.

Never shrink text excessively just to fit content.

If a concept requires another page:

**create another page.**

Do not commit typographic crimes against A4 paper.

---

# 27. CHAPTER STRUCTURE

Use this structure when appropriate:

```text
CHAPTER
│
├── Concept
├── Why it exists
├── Architecture
├── Lifecycle
├── Example
├── Failure modes
├── Real-world workflow
├── Lab
└── Knowledge check
```

Do not force every chapter to contain every section.

Use the structure that matches the material.

---

# 28. DOCUMENT ARC

The complete book should gradually move from:

```text
WHY
 ↓
WHAT
 ↓
HOW
 ↓
PIPELINE
 ↓
AUTOMATION
 ↓
DEPLOYMENT
 ↓
FAILURE
 ↓
RECOVERY
 ↓
REAL SYSTEM
```

The reader should feel like they are progressively operating a real CI/CD system.

---

# 29. CONTINUITY

Reference previous concepts where useful.

Example:

```text
Earlier we created the artifact.

Now we need to answer the uncomfortable question:

Who is allowed to deploy it?
```

Use continuity to make the document feel like one coherent engineering system.

---

# 30. FINAL SECTION

End with a **CI/CD SYSTEM MAP**.

Example:

```text
┌──────────────┐
│ SOURCE       │
└──────┬───────┘
       ↓
┌──────────────┐
│ CI           │
│ BUILD / TEST │
└──────┬───────┘
       ↓
┌──────────────┐
│ ARTIFACT     │
└──────┬───────┘
       ↓
┌──────────────┐
│ CD           │
│ RELEASE      │
└──────┬───────┘
       ↓
┌──────────────┐
│ ENVIRONMENT  │
└──────┬───────┘
       ↓
┌──────────────┐
│ OBSERVE      │
└──────┬───────┘
       │
       └──────────→ FEEDBACK
```

Then provide:

* key commands
* important terminology
* common failure modes
* architecture summary
* interview questions
* troubleshooting flow

---

# 31. QUALITY CONTROL

Before returning the HTML, verify:

☐ Complete `<!DOCTYPE html>` through `</html>`

☐ No raw Markdown visible

☐ No raw ASCII diagrams visible

☐ All diagrams rebuilt using HTML/CSS

☐ All commands rendered as terminal components

☐ All tables converted into styled HTML tables

☐ Pipeline stages visually communicate progression

☐ CI/CD colors remain consistent

☐ DEV/STAGING/PROD are visually distinguishable

☐ Success/failure states are explicit

☐ Artifacts have consistent visual identity

☐ Approval gates are visually distinct

☐ Failure flows show recovery

☐ No content is clipped

☐ No page contains awkward orphaned headings

☐ Section headings use the mandatory shape `<span class="n">05 /</span> Title` with real whitespace after `</span>` (margin alone is not trusted), and titles are editorial noun phrases — never meta-labels (`One table…`) or shout-suffixes (`— WHAT`). No `§` symbol anywhere.

☐ Page numbering is correct

☐ Chapter structure is coherent

☐ Print layout works on A4

☐ Code remains readable when printed

☐ Background graphics are enabled through print instructions

---

# 32. FINAL DELIVERY

## 32.0 SPEC COMPLIANCE GATE (read before writing a single line)

```text
Building PDF/HTML  → read PDF_BUILD_SPEC.md + ICON_ASSET_SPEC.md (Parts A–D) fully
Placing any icon   → ICON_ASSET_SPEC.md Parts A–D + assets/icons/README.md mapping
Starting website   → WEBSITE_BUILD_SPEC.md + ICON_ASSET_SPEC.md
```

No improvising from memory. If a rule is missing, add it to the spec first, then build. The spec leads, the artifact follows.

Return:

1. One complete standalone HTML file.
2. No explanation between sections of the HTML.
3. No partial code.
4. No omitted CSS.
5. No placeholders.
6. No "continue generating" instructions.

After the HTML, provide a compact page map.

Then:

**Open in browser → Ctrl/Cmd+P → Save as PDF → enable Background graphics.**

---

# PART: PDF TYPOGRAPHY AND PAGE SPACE OPTIMIZATION

## 1. PRIMARY GOAL

Improve readability and visual density by increasing font size, easing section reading, using page space effectively, letting sections occupy the full useful area when content permits, avoiding large unnecessary empty areas, artificial stretching, and awkward breaks. Better use of space, not filling pixels.

## 2. FONT SCALE (baseline — readability over page count)

```css
body / paragraph: 11pt–12pt; line-height: 1.5–1.7;
section heading: 18pt–24pt; subsection: 14pt–18pt;
supporting/small text: minimum 9pt–10pt; code: 9.5pt–11pt, line-height 1.4–1.6;
```

A longer PDF with excellent readability beats a compressed one. Never shrink text to cut pages.

## 3. SECTION-FIRST LAYOUT

Keep heading + explanation + diagram/table/example + details visually connected on one page when they naturally fit. Never fragment a coherent section across pages to force the next section to start early.

## 4. USE THE WHOLE PAGE WHEN CONTENT SUPPORTS IT

Scale up through layout (larger text, spacing, diagrams, tables, callouts, code readability) — never through `padding:100px` hacks. Do NOT manufacture content: no repeats, filler paragraphs, decorative text, duplicated diagrams, or fake examples to fill space.

## 5. WHEN IT DOESN'T FIT

Move the section to the next page; never strand fragments. No orphan headings (heading alone at page bottom). No splits between heading/first-paragraph, Q/A, diagram/explanation, code/explanation, or mid-sentence.

```css
h1, h2, h3 { break-after: avoid; }
.callout, .diagram, .code-block, .table-container,
.pipeline, .lane, .terminal, .cmdres, .vflow, .dec, table.cmp { break-inside: avoid; }
```

Apply `break-inside: avoid` only to small units — never to giant containers (creates blank holes).

## 6. PAGE BREAK PREFERENCE

Break before: new major section, large diagram/table, lab, chapter. Split only at semantic boundaries (end of explanation/example/diagram/subsection). Full-page composition allowed for major sections with enough content; short sections keep natural whitespace.

## 7. QA PER PAGE

Body comfortably readable and larger than before · no tiny text · no accidental empty areas · no orphan headings · no bad splits · readable diagrams/tables/code · breaks at semantic boundaries · nothing clipped/overlapping · consistent margins · balanced density · intentional whitespace preserved.

## 8. CORE RULE

> If enough meaningful content exists to use the page, let it. If not, do not invent or stretch content to kill whitespace. Optimize for best reading experience per page, not minimum page count.
