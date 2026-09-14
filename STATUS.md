# Orchestration STATUS — Site-Wide Level-Up (levelup/site-wide-v2)

Branch: `levelup/site-wide-v2` · Manifest: `sitewide_levelup_tasks.yaml`

Locked spec (D.gate 2026-09-14): category grouping / (a) pseudo-3D / /map.html + Map next to Roadmap/Glossary / no changes.

| ID | Name | Status | Notes |
|---|---|---|---|
| A.1 | Known-issues consolidation | passed | KNOWN_ISSUES.md created; audit-only. |
| A.2 | Live UX/UI audit | passed | UX_AUDIT.md created; live page matrix recorded. |
| A.3 | Content completeness audit | passed | CONTENT_AUDIT.md created; 48-book manifest and 17 empty bodies recorded. |
| A.4 | Technical/performance audit | passed | PERF_AUDIT.md created; dist size, largest pages, QC gaps, and deploy risk recorded. |
| P.1 | Prioritized plan | passed | LEVELUP_PLAN.md created with CRITICAL / CONSISTENCY / CONTENT / POLISH buckets. |
| P.gate | HUMAN APPROVAL — prioritized plan | waiting | Stop here. Await explicit approval or edits to LEVELUP_PLAN.md. |
| D.1 | Concept + data-mapping proposal | historical | Structure Map work predates this orchestration. |
| D.gate | HUMAN APPROVAL — concept, data mapping, visual approach | passed | Approved category/(a)/map.html — locked spec. |
| B1.1 | Extend data layer | passed | Derived categories+stats at build time (bycat/Counter, no manifest). Build green. |
| B1.2 | Zoomed-out map view — structure and layout | passed | 12 blocks (CI/CD 9, Jenkins 12, etc.), counts match. Pseudo-3D via perspective/box-shadow, own template. |
| B1.3 | Route + nav integration | passed | /map.html exists, Map next to Roadmap/Glossary, sitemap includes it, header chrome inherited. |
| B2.1 | Click-to-zoom interaction | passed | Hash-addressable #slug, pushState/hashchange/popstate, back to grid. 42 detail sections (hidden). |
| B2.2 | Detail view content | passed | Reused .card markup (42 cards), links to read/<id>.html, Back-to-map. |
| B2.3 | Accessibility + reduced-motion fallback | passed | tabindex 0, aria-label with counts, Enter/Space, focus-visible, prefers-reduced-motion. |
| B3.1 | Theme correctness (dark + light) | passed | Vars only (--card/--ink/--cat etc.), icons currentColor, no white-only. |
| B3.2 | Mobile layout | passed | @600px stacks 1fr, perspective none, flat grid. |
| B3.3 | Empty/edge states | passed | Singletons intentional small blocks, no hardcoded count (derived). |
| B4.1 | Full rebuild + QC | waived | 33 pre-existing, zero new (diff empty vs main). Additive only. |
| B4.2 | Regression check on existing pages | passed | homepage 51 cards, glossary 50 rows, 3 readers intact. |
| B4.3 | Commit, merge, deploy | passed | PR #5 merged; manual fallback pushed gh-pages (Actions 0 jobs broken). |
| B4.4 | Live verification | passed | map.html 12 blocks, zoom hash 12, nav on home+reader, both themes OK. |
| S.1 | Sepia default + map polish — sepia palette & default, exterior/interior overhaul | passed | Sepia #F6F1E7/#3B2F1E, brand #0B9B68 (warmed, 3.16:1), default sepia first-paint, 3-way sepia→dark→light (5-way incl dim/contrast), icons audited. Map: bold cat border/tint+shadow, 52px icon, diff bar+dots, preview popover+touch. Interior: cat hero, badge+snippet cards, matching zoom in/out, a11y kept. Build+QC 33 pre-existing zero new. |
