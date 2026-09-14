# Technical and Performance Audit

Audit date: 2026-09-14.

## Measurements

| Metric | Finding | Severity |
|---|---|---|
| Generated site size | 234 files, 9,342,556 bytes under `website/dist`. | moderate |
| Largest generated pages | `shelf.html` 260,740 bytes; `index.html` 169,327; `read/jenkins-labs.html` 140,907; `search.json` 122,052. | moderate |
| Reader HTML duplication | Each reader embeds the shared base CSS and JS, increasing aggregate cache cost across 48 pages. | moderate |
| Fonts | `BASE_CSS` uses Google Fonts via CSS `@import`; system fallbacks exist, but the import remains render-path work and can cause typography/layout shift. | moderate |
| Search index | `search.json` is 122 KB for 48 books and section/body snippets. This is reasonable for a static site, but is loaded as a large single payload. | cosmetic |
| Build/QC | `python website/scripts/build.py` succeeds; `python scripts/qc-check.py` reports `QC: ALL GREEN (0 findings)`. | no issue |
| Internal link/overflow coverage | `qc-check.py` checks document structure, signatures, reflow markers, assets, and footer patterns, but does not run a browser, check horizontal overflow, or verify all generated internal links. | moderate |
| Icon coverage | `qc-check.py` does not validate semantic icon mapping completeness or orphaned CSS selectors. | cosmetic |
| Deploy reliability | The deploy workflow has failed immediately in recent history; manual two-push deployment remains the operational path. | high |

## Recommended audit follow-ups

1. Add a browser-based generated-link and overflow smoke check to QC.
2. Add explicit checks for orphaned CSS/component hooks and icon registry drift.
3. Measure font loading with and without network access before changing the
   typography strategy.
4. Keep manual deployment documented until the Pages token/workflow failure is
   resolved and one successful workflow run is observed.

