# PROMPT: CONTENT CONNECTIVITY & HANDOFF REWRITE

## OBJECTIVE
Rewrite the CI/CD knowledge base markdown so every section explicitly **hands off** to the next, creating a single continuous learning narrative from 00-foundations through 15-platforms-and-tools. The reader should never feel a conceptual gap.

## RULES

### 1. FORWARD HANDOFF (Required)
At the end of **every major section** (`##`), add exactly one sentence that:
- Names the next concept the reader will encounter
- Explains *why* it follows logically
- Uses this template:

> "Now that you understand [CURRENT CONCEPT], the next question is [NEXT QUESTION] — which is exactly what [NEXT SECTION/DOC] covers."

### 2. BACKWARD LINK (Required)
At the start of **every major section** (`##`), add exactly one sentence that:
- References what the reader just learned
- Shows how this section builds on it

> "Building on [PREVIOUS CONCEPT] from [PREVIOUS SECTION/DOC], we now examine [THIS CONCEPT]."

### 3. CROSS-DOCUMENT BRIDGES (Required)
When a concept spans multiple `.md` files, the *last section* of the first file must end with:

> "This workflow continues in **[NEXT DOC TITLE]** → [relative link], where we explore [SPECIFIC NEXT TOPIC]."

And the *first section* of the next file must open with:

> "Picking up from **[PREVIOUS DOC TITLE]**, where we left off at [LAST CONCEPT]..."

### 4. NO DUPLICATION
- Do not repeat definitions. Instead: "As defined in [DOC], an artifact is..."
- Do not re-explain mechanisms. Instead: "The mechanism (see [DOC] §3) works by..."

### 5. TERMINOLOGY CONSISTENCY
- Use the exact term from `GLOSSARY.md` every time
- First use in a document: link to glossary (`[Artifact](../GLOSSARY.md#artifact)`)
- Subsequent uses: plain text

### 5. PRESERVE EXISTING
- All commands, YAML, diagrams, tables, icons, annotations, glossary rows
- All section structure, frontmatter, icon annotations
- Do not add fluff, history, or motivational text

## EXECUTION ORDER
Process files in learning order (from `ROADMAP.md`):

1. `00-foundations/cicd-overview.md`
2. `01-source-control/git-branching-pull-requests.md`
3. `06-ci-cd-pipelines/pipelines.md`
4. `05-artifacts-and-packaging/artifact-management.md`
5. `07-continuous-delivery/continuous-delivery.md`
6. `13-observability-and-feedback/observability-feedback.md`
7. `15-platforms-and-tools/jenkins/README.md`
8. `15-platforms-and-tools/jenkins/jenkins-architecture.md`
9. `15-platforms-and-tools/jenkins/jenkins-setup.md`
10. `15-platforms-and-tools/jenkins/jenkins-pipelines.md`
11. `15-platforms-and-tools/jenkins/jenkins-agents.md`
12. `15-platforms-and-tools/jenkins/jenkins-credentials.md`
13. `15-platforms-and-tools/jenkins/jenkins-plugins.md`
14. `15-platforms-and-tools/jenkins/jenkins-webhooks.md`
15. `15-platforms-and-tools/jenkins/jenkins-security.md`
16. `15-platforms-and-tools/jenkins/jenkins-advanced.md`
17. `15-platforms-and-tools/jenkins/jenkins-troubleshooting.md`
17. `15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md`
18. `15-platforms-and-tools/github-actions.md`

## VERIFICATION CHECKLIST (Per File)
- [ ] Every `##` has backward link (1 sentence)
- [ ] Every `##` has forward handoff (1 sentence)
- [ ] Cross-doc bridges at file boundaries (both sides)
- [ ] Zero repeated definitions (cross-links instead)
- [ ] Glossary terms linked on first use
- [ ] All existing content preserved
- [ ] Icons, annotations, frontmatter untouched

## OUTPUT
Modified markdown files in place. Final report: list of files changed + handoff sentences added.

---

**Run this prompt by iterating through the 19 files in order, applying the rules, saving each file, then reporting.**