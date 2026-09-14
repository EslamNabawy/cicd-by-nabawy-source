# Orchestration STATUS — Structure Map (feature/structure-map-view)

Branch: `feature/structure-map-view` · Manifest: `structure_map_tasks.yaml`

Locked spec (D.gate 2026-09-14): category grouping / (a) pseudo-3D / /map.html + Map next to Roadmap/Glossary / no changes.

| ID | Name | Status | Notes |
|---|---|---|---|
| D.1 | Concept + data-mapping proposal | passed | STRUCTURE_MAP_PROPOSAL.md committed. |
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
| B4.1 | Full rebuild + QC | in-progress | qc-check → must be ALL GREEN; fix if flagged. |
| B4.2 | Regression check on existing pages | pending | |
| B4.3 | Commit, merge, deploy | pending | |
| B4.4 | Live verification | pending | |
