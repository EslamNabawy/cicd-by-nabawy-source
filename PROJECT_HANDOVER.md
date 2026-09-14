# Project Handover — CICD BY Nabawy

## What this is
A CI/CD knowledge base: **48 books in `website/content/books.json`** (canonical manifest with time/prereqs/outcomes/tags/path/updated/version) → **print PDFs + 9 omnibus series books** → a **static library website** (map + shelf + 48 readers + 48 book landing pages + glossary + roadmap + updates), all live.
Latest audit: `WEBSITE_AUDIT_FIXES.md` (2026-09-14) supersedes `WEBSITE_IMPROVEMENT_PLAN.md` (39-book era).

## Live URLs & repos
- Site: https://eslamnabawy.github.io/cicd-by-nabawy/ (branch `gh-pages` on site repo)
- Site repo: `EslamNabawy/cicd-by-nabawy` (deployed artifact only — `dist/` contents)
- Source repo: `EslamNabawy/cicd-by-nabawy-source` ← all work happens here, root `CI-CD/`

## Layout (source repo)
```text
CI-CD/
├── 00-foundations/ … 17-reference/   # 39 content docs (kebab-case, frontmatter)
├── 15-platforms-and-tools/           # jenkins/ (12 files) + github-actions, gitlab-ci, argocd-gitops
├── pdf/ 36 × pdf-*.html + series/9   # print editions (A4, Nabawy sig, m-reflow mobile)
├── assets/icons/ + README.md         # single icon source; ids mapped READY (23/23, 0 missing)
├── website/content/books.json        # manifest (48: id/title/file/category/difficulty/desc/time/prereqs/outcomes/tags/path/updated/version)
├── website/content/paths.json         # 9 ordered learning paths (single taxonomy source)
├── website/scripts/build.py          # ONLY generator (1753 lines) — map, shelf, readers, book landings, glossary, roadmap, updates, search.json
├── website/dist/                     # build output (committed; deployed as-is to gh-pages)
├── scripts/qc-check.py               # THE GATE — run before every push
├── scripts/build_series.py           # omnibus S01–S09 generator
├── .github/workflows/deploy.yml      # CI: qc → build → sitemap/robots verify → gh-pages
└── *.md roots                        # README, ROADMAP, TOPIC_INDEX, CONTENT_MAP, GLOSSARY + specs
```

## The golden rules
1. **Markdown is canonical.** Never edit `pdf/` or `dist/` by hand — change md/manifest, rebuild.
2. **Run the gate:** `cd CI-CD && python scripts/qc-check.py` → must print ALL GREEN.
3. **Rebuild rule:** any change to `pdf/*`, `books.json`, `paths.json`, `GLOSSARY.md`, or `build.py` → `python website/scripts/build.py` → republish `dist/`.
4. **Vendor-neutral generics.** Concepts live in generic docs; Jenkins/GitLab/etc. files contain only what's distinctively theirs.
5. **Icons:** semantic `<!-- icon: id -->` in md only; SVG-only assets; missing ids recorded, never faked.

## Deploy — automated + manual fallback
- **Automated (preferred):** `.github/workflows/deploy.yml` — on `push` to `main` runs `qc-check → build → verify sitemap/robots` → `peaceiris/actions-gh-pages` to `EslamNabawy/cicd-by-nabawy` (`gh-pages`). Requires secret `GH_PAGES_PAT` (fine-grained PAT, Contents: Read & Write on `cicd-by-nabawy`). Until PAT is set, workflow still builds, QCs, and uploads `dist` artifact but skips deploy.
- **Manual fallback (two pushes):**
```bash
# 1. site (fresh tmp dir each time — never rm -rf, never reuse)
export DEP="$LOCALAPPDATA/Temp/cicd-deployN" && mkdir -p "$DEP" && cp -r website/dist/* "$DEP/" \
&& touch "$DEP/.nojekyll" && cd "$DEP" && git init -q -b gh-pages && git add -A \
&& git -c user.name=EslamNabawy -c user.email=eslam@local commit -qm "<msg>" \
&& git remote add origin https://github.com/EslamNabawy/cicd-by-nabawy.git && git push -f origin gh-pages
# 2. source
cd CI-CD && git add -A && git commit -m "<msg>" && git push origin main
```
PAT setup: GitHub → Settings → Developer settings → Personal access tokens → Fine-grained → Repository access → Only selected → `cicd-by-nabawy` → Permissions → Contents: Read and write → Generate → Source repo → Settings → Secrets → Actions → New secret `GH_PAGES_PAT` → paste.

## Design system (site)
Mintlify-based: Inter + Geist Mono (Google Fonts @import, degrades gracefully offline),
dark default `#0B0D10` + light theme + sepia in reader, brand `#18E299`, per-category accents
(`[data-cat]` map in build.py), 12px radius, pill everything. Reader = flow mode
(print chrome stripped at build, covers kept as openers). IA: structure map (landing) +
shelf (search + category/level filter + sort + path rails) + book landing pages
(`book/{id}.html`: meta, outcomes, prereqs, related, prefetch) + readers with nested
numbered TOC + global `search.json`. 9 ordered paths in `paths.json` are the single
taxonomy — no separate "Quick topics" grouping.

## Known quirks (2026-09-14 audit — see WEBSITE_AUDIT_FIXES.md §§A–C)
- CRLF warnings on Windows checkouts — cosmetic, ignore.
- Google Fonts needs network; offline falls back to system fonts; no `preconnect` yet (P0).
- Shelf hero "Start Here 5 books" vs path `start-here` 2 books — undecided, P0 fix pending.
- Glossary Topic column renders raw `[label](path)` markdown, Link column `#`, counter shows "0 terms" — P0.
- Lab Verification `[ ]` is plain text (0 checkboxes), "Reset checks" unwired — P0.
- Lab code blocks lack `<pre>` semantics; copy grabs prose + code — P0.
- Lab names collide (generic `Lab 01–05` vs Jenkins `Lab 01–05` + `Jenkins Labs` omnibus) — P1.
- Roadmap page repeats Map category grouping instead of ordered stepper — P1.
- Updates page: all rows `v2.0 / 2026-09-01`, no real freshness signal — P1.
- Drawer focus-trap + `aria-modal` missing; `loading=lazy` ×0; OG images SVG-only — P0/P1.
- Old repo names/URLs redirect automatically (cicd-library, cicd-knowledge-base).

## If extending
- New book: md → TOPIC_INDEX/ROADMAP/GLOSSARY/CONTENT_MAP → pdf-NN.html (copy nearest template, keep sig/footers/m-reflow) → books.json → build → QC → deploy ×2.
- New series: add entry in `scripts/build_series.py` SERIES → run it → rebuild site.
- New icon: content-first (ICON_ASSET_SPEC.md), Lucide ISC / Simple Icons CC0, register in assets/icons/README.md.
