# Site-Wide Level-Up Plan

Audit date: 2026-09-14. This plan is intentionally stopped at the required
human gate. No implementation fixes have been made in this phase.

## CRITICAL

1. Restore real rendered content for the 17 stylesheet-only curriculum books
   listed in `CONTENT_AUDIT.md`, or explicitly split that work into dedicated
   content-writing batches; current reader routes otherwise present empty books.
2. Repair the GitHub Pages workflow failure and observe one successful
   `qc -> build -> deploy` run before relying on automated deployment again.
3. Add browser-level generated-link and overflow checks to the release gate so
   static QC cannot pass a broken route or narrow-screen layout unnoticed.

## CONSISTENCY

1. Apply the reader's compact mobile navigation model to landing, Browse,
   glossary, roadmap, and map pages so the site has one responsive chrome model.
2. Review the 1.9k–2.3k-character non-empty books against the newer book/lab
   structure and standardize missing section patterns without flattening their
   subject-specific voice.
3. Unify glossary table, roadmap cards, and map detail density around the
   established accent, card, badge, and spacing tokens.
4. Refresh stale root status/spec copy so book counts, branch names, and live
   route descriptions match the current 48-book implementation.

## CONTENT

1. Write complete core material for Build Systems, Testing Strategy,
   Continuous Deployment, Environments & Release, CI/CD Security, and Rollback
   & Recovery, matching the depth of Foundations and Jenkins core books.
2. Write the eight original Labs as executable exercises with prerequisites,
   setup, commands, expected output, failure modes, verification, and cleanup.
3. Write the GitLab CI, ArgoCD/GitOps, IaC, and Command Cheatsheet books.
4. Re-audit thin existing books and update TOPIC_INDEX, CONTENT_MAP, ROADMAP,
   and GLOSSARY for any newly introduced terms.

## POLISH

1. Improve the discoverability/focus treatment of the transient Back-to-top
   control after live user testing.
2. Add subtle loading-state and focus refinements to map previews and long
   shelf rails, respecting reduced motion.
3. Improve narrow glossary scanning with sticky context or an accessible
   stacked representation if the responsive audit confirms the need.

## NOT doing this round

- Do not fabricate the 17 missing books with placeholder paragraphs; they need
  dedicated technical writing and verification.
- Do not redesign the visual language or replace the static generator; the
  existing token/card system is coherent and should be reused.
- Do not switch font providers before measuring the actual first-load cost.
- Do not declare automated deployment fixed until a real workflow run succeeds.

