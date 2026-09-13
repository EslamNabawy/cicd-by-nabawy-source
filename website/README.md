# CICD BY Nabawy — Website

Static, no-build website generated from the knowledge base (per `WEBSITE_BUILD_SPEC.md`).

## Run

Open `dist/index.html` in a browser. No server, no dependencies — works from `file://`.

## Rebuild

```bash
python scripts/build.py
```

Reads `content/books.json` + `../pdf/*.html` + `../GLOSSARY.md`, writes `dist/`.
Adding a book = one manifest entry + re-run. Icons are copied from the single
source `../assets/` into `dist/assets/` on every build.

> Rule: readers embed PDF content at build time, so **any** change to
> `../pdf/*`, `content/books.json`, `GLOSSARY.md`, or `scripts/build.py`
> requires a rebuild + republish of `dist/`. Verify with
> `python ../scripts/qc-check.py` before pushing.

## What's inside

- Library: search, category filter, progress, continue reading, topics
- Reader (per book): TOC with scroll-spy, Original/Light themes, A−/A+/width,
  in-book search (Ctrl+K), copy buttons, prev/next, print stylesheet, PDF link
- Glossary page generated from `GLOSSARY.md`
- Preferences + progress persist in `localStorage`; no accounts
