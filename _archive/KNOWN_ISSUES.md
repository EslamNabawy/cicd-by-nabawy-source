# Known Issues Inventory

Audit date: 2026-09-14. Branch: `levelup/site-wide-v2`.

## Current status

| Issue | Status | Evidence |
|---|---|---|
| Reader TOC links generated as `#ppN` | fixed-and-verified-live | `98018e8`; live reader now emits `#pN` and active TOC state updates. |
| Reader Back control missing | fixed-and-verified-live | `0a7cfff`; live reader contains one history-aware Back link. |
| Reader feedback/rating widget | fixed-and-verified-live | `0a7cfff`; live reader has no `ratebox`, `rateup`, or `ratedown`. |
| Reader mobile header consumed multiple rows | fixed-and-verified-live | `98018e8`; live reader contains compact mobile menu controls and one toolbar row. |
| Reader Back-to-top control | fixed-and-verified-live | `98018e8`; live reader contains `topbtn` and reduced-motion rule. |
| Legacy Labs and several roadmap/reference books have stylesheet-only PDFs | reported-but-not-yet-fixed | Source audit finds no rendered `<body>` content in the files listed in `CONTENT_AUDIT.md`. This was explicitly deferred in the prior fix. |
| Automated GitHub Pages workflow deploy | reported-but-not-yet-fixed | `.github/workflows/deploy.yml` exists, but recent runs failed immediately; manual gh-pages fallback was used for commits `ab991e1`, `0a7cfff`, and `98018e8`. |
| Historical STATUS/spec documents are stale | reported-but-not-yet-fixed | `STATUS.md` still describes the Structure Map phase and reports old book counts/branch context. |

## Deployment discrepancy check

The two latest reader fixes were checked against both the live HTML and the
`gh-pages` raw branch with cache-busting query strings. The current compact
header, single Back link, and Back-to-top markup are present live. No earlier
claim in this audit was found to be currently unverified.

