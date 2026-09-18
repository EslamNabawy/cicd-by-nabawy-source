# CICD BY Nabawy — Website

Static, no-build website generated from the knowledge base. No server, no
dependencies — works from `file://`.

- Source repo: `EslamNabawy/cicd-by-nabawy-source` (branch `main`)
- Site repo: `EslamNabawy/cicd-by-nabawy` (branch `gh-pages`, force-pushed)
- Live: https://eslamnabawy.github.io/cicd-by-nabawy/
- CI auto-deploy is broken (pre-existing) — deploy is manual via temp clone.

## Run

Open `dist/index.html` in a browser.

## Rebuild (from repo root `CI-CD/`)

```bash
python website/scripts/build.py
python scripts/qc-check.py
```

Reads `website/content/books.json`, `website/content/paths.json`,
`website/content/threads.json`, `pdf/*.html`, `GLOSSARY.md` — writes `dist/`.
Adding a book = one manifest entry + re-run. Icons are copied from the single
source `assets/` into `dist/assets/` on every build. Stale `read/`, `labs/`,
`og/`, `book/`, `downloads/` outputs are wiped and regenerated.

> Rule: readers embed content at build time, so **any** change to `pdf/*`,
> `content/*`, `GLOSSARY.md`, or `scripts/build.py` requires rebuild + QC +
> push + manual deploy.

## What's inside

- Home: SIGNAL cover hero, category chips, contents rows, search filter,
  saved row, resume pill
- Reader (per book): numbered contents sidebar with scroll-spy + section links
  that don't spam history, sepia (default) / dark / light themes, header theme
  cycle, fullscreen island (contents/theme/zoom/progress/exit), in-book search
  (Ctrl+K), copy buttons, prev/next book, print stylesheet, print edition link
- Concept threads page: 9 cross-book threads + zoomable book↔thread graph
- Tool picker page: 5 questions → ranked stack with deep links
- Roadmap, glossary, updates, sitemap pages
- Thread pills on sheets link both directions (book ↔ thread)
- Preferences + progress persist in `localStorage`; no accounts
