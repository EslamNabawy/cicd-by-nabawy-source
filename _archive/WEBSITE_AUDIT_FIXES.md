# Website Audit — Content, Display, UI/UX — All Required Modifications
**Date:** 2026-09-14
**Scope:** live site `https://eslamnabawy.github.io/cicd-by-nabawy/` + source `website/dist/`, `website/content/books.json`, `website/content/paths.json`, `website/scripts/build.py` (1753 lines), `GLOSSARY.md`
**Method:** live browser pass (map, shelf, reader, book landing, lab reader, glossary, roadmap, updates) + dist/code inspection + manifest counts. Previous `WEBSITE_IMPROVEMENT_PLAN.md` (39-book era) is stale — site is now 48 books with P0/P1 partly shipped. This file supersedes it as the fix list.

## Resolution log — 2026-09-15 (orchestrated fix pass, `cicd-by-nabawy-source` `main`)
- **Phase 0 (handoff TOC bug):** prior session's per-heading anchors were real but incomplete — scroll-spy still tracked page-level ids (highlight died entirely) and bare `<h2>`/`<h3>` (237/511) got no ids. Fixed `mark_heading` regex, rewrote `tocUpdate` to resolve per-heading anchors (exactly one `.cur`), rebuilt reader TOC post-strip reusing injected ids (chapter `h2`s live inside stripped `phead` chrome). Verified: 62/62 reader pages, 0 dead anchors, click→1 highlight, scroll advances, mobile drawer. Commit `daae575`.
- **A1:** resolved by RENAMING the shelf strip to "★ First week — new to CI/CD" (user decision) instead of moving books — extending the path would have gutted CI Core (5→3) and Labs. Single taxonomy preserved.
- **A2:** fixed — Topic column renders real `read/{id}.html` links (50/50 via inverted MD_MAP), Link column is a `¶` permalink, counter fixed (`<tr ` not `<tr>`).
- **A5:** per-book git dates at build time + ≤60-day ribbon; caveat: repo history is 2 days deep so all rows read 2026-09-14 today — mechanism correct, dates diverge going forward. Commit `c8c0162` (Phase 1).
- **B1:** fixed — `markdown_pages` emits `<li class="step">` for `[ ]` items; existing `labChecks()` now finds them. Verified persist/reload/reset.
- **B2:** fixed — fenced code emits `<pre class="codeblock" data-lang>` (Copy/Wrap via existing codehead, lang label fixed to evaluate `dataset.lang`); pdf `.terminal` blocks got `white-space:pre`. Verified yaml label + copy + wrap + terminal render.
- **B4:** done — Pillow PNG social cards (49 files, optional dep with SVG fallback), `og:image` → `.png`.
- **C1:** done — 44px touch targets on reader + non-reader mobile headers, glossary gained theme toggle, no overflow at 320px. Esc/drawer behavior pre-existing. Commit `9a64704` (Phases 2+3).
- **A3:** fixed — track prefixes (`Lab 01 · Core` vs `Lab J-01 · Jenkins`), ids untouched.
- **A4:** fixed — roadmap rebuilt as 9-path ordered stepper (Quick topics gone), per-stop time, done-ticks from stored progress, dynamic SEO count.
- **B3:** verified already-clean — tokens cover all 3 themes, full settings present (no code change).
- **B5:** lightbox/lazy/alt pre-existing; added sticky thead + zebra tables.
- **C2:** done — shelf 261KB → 167KB (body-free inline index + compact JSON; full index fetched over HTTP, file:// keeps light index); rails collapse at 6 with View-all toggle; filter auto-expands.
- **C3:** done — ranked dropdown pre-existing; added in-reader Enter-cycling (`match n of m`) + Esc-clears.
- **C4–C8 remainder:** preferences Reset button added; font preconnect ×9 heads; print forces light ink; roadmap done-ticks; shelf resume/progress pre-existing. NOT done (deferred): per-section read-dots, history row, focus-trap/`aria-modal`, drawer focus management, PWA, Lab 09, cheatsheet board, highlights/notes — propose as next batch.
**Good news:** metadata model, paths, book landing pages, nested TOC, filters, related footer, updates page all live. Fixes below are what remains.

---

## A. Content correctness bugs (fix first — trust damage)

### A1. Two different "Start Here" definitions on the same page — CONFIRMED
- Evidence: `books.json` path `start-here` = 2 books (`foundations`, `git-branching`, ~50 min). Shelf hero says "★ START HERE — NEW TO CI/CD, 5 books · ~155 min" (adds Pipelines + CI + Lab 01). Map page "Start Here, 2 books · ~50 min".
- Impact: user counts 2 vs 5, time 50 vs 155. Looks like drift.
- Fix: one source of truth. Either extend `paths.json` `start-here` to 5 and rebuild map, or rename hero to "Suggested first week" and keep path at 2. Rebuild + verify counts match on map/shelf/reader breadcrumbs. File: `website/content/paths.json`, `website/scripts/build.py` (`paths_section_html`, shelf hero block).

### A2. Glossary Topic column renders raw Markdown, Link column dead — CONFIRMED
- Evidence: live glossary rows show literal `[Artifact Management](05-artifacts-and-packaging/artifact-management.md)` in Topic, `#` in Link. Header says "0 terms · shared by books" while table has ~50+ rows.
- Impact: looks broken, links unusable, term count wrong.
- Fix: run glossary topics through existing `md_inline()` at build; Link column should deep-link to book reader (`read/{id}.html`) or drop the column and make Term anchorable (`glossary.html#artifact`). Fix counter from parsed rows. Files: `build.py` glossary template, `GLOSSARY.md` (also verify no dupes — current parse shows 0 dupes, old Canary dupe is gone).

### A3. Lab naming collisions — CONFIRMED
- Evidence: `labs` path (14 books) mixes `Lab 01–08` generic series with `Lab 01–05` Jenkins/descriptive titles (`Lab 01: First Pipeline` vs `Lab 01: Automated Integration Foundations`, `Lab 02: Build & Test` vs `Lab 02: Container Delivery`, etc.) + `Jenkins Labs` omnibus.
- Impact: "Up next" and Related show near-duplicate titles side by side; users can't tell which track they're on.
- Fix: rename with track prefix at manifest level (`Lab 01 · Core: First Pipeline`, `Lab J-01 · Jenkins: Automated Integration…`) or split `labs` path into `labs-core` + `labs-jenkins`. Update `books.json` titles, `paths.json`, rebuild. No content rewrite needed.

### A4. Roadmap page duplicates Map instead of being a path — CONFIRMED
- Evidence: `/roadmap/` header reads "MAP — Every book, one map. 48 docs grouped by category" with a "Quick topics · 7" group that exists in neither `paths.json` (9 paths) nor shelf paths. It is category grouping, not ordered by dependency.
- Impact: Roadmap ≠ path; "Quick topics" is a third taxonomy (paths vs categories vs quick topics).
- Fix: rebuild roadmap as linear stepper in `paths.json` order with mile numbers, per-stop time + level + done check from progress; delete "Quick topics" grouping or define it in `paths.json` so all three pages share one taxonomy. File: `build.py` `build_roadmap_page`.

### A5. Updates page is a static snapshot — CONFIRMED
- Evidence: `updates.html` header "P0+P1 shipped Sep 2026", all 48 rows `v2.0 / 2026-09-01`.
- Impact: identical dates = no real freshness signal; returning users can't see what's new.
- Fix: per-book `updated` from git log at build (or manual `CHANGELOG.md`), "New/Updated" ribbon if <60 days, changelog entries on updates page. Files: `books.json` dates, `build.py` updates template.

---

## B. Reader display gaps (content is good, presentation leaks)

### B1. Lab Verification checklist is plain text, "Reset checks" does nothing — CONFIRMED
- Evidence: live `read/lab-01.html` Verification shows `[ ] PR shows green check…` as text; `input[type=checkbox]` count = 0 despite header "Reset checks".
- Impact: lab progress can't be tracked; spec's persisted lab-checkbox feature is half-shipped.
- Fix: render `[ ]` lines as real checkboxes persisted per book (`cicdlib:checks:{id}`), wire Reset button. File: `build.py` reader post-process + `READER_JS`.

### B2. Code blocks: 0 `<pre>` on lab page, copy is unstructured — CONFIRMED
- Evidence: workflow YAML renders inside generic block with a bare "Copy" prefixing the whole text; no `<pre>`, no language label, no wrap toggle. Copy likely grabs prose + code together.
- Impact: copy-paste breaks YAML indentation; no distinction between command vs output.
- Fix: emit semantic `<pre><code class="lang-yaml">` at build from PDF code extraction; header bar (lang + filename + Copy-code-only + Wrap); terminal blocks split `data-cmd` (copied) vs output (dimmed, not copied). Files: `build.py` `parse_book`/`scope_css`, `READER_JS`.

### B3. Light theme leaks + no Sepia in reader chrome (partially shipped)
- Evidence: `build.py` has `sepia` ×112 and `[data-theme=light]` overrides, but PDF-embedded tables/diagrams/callouts historically keep dark backgrounds; reader toolbar detected has Save/Back/A+ but no visible theme control in sampled HTML (`themeBtn=false` on reader string scan).
- Impact: half-themed pages, contrast failures on tables/diagrams in light/sepia.
- Fix: scope all PDF remnants (`.readbody table, pre, .callout, .terminal, svg`) to site tokens per theme; ensure theme switcher (Dark/Light/Sepia) exists on reader, not just landing. Screenshot-diff 4 pages × 3 themes before sign-off.

### B4. Covers are initials only ("CF" block)
- Evidence: book landing shows flat `CF` tile; no category-hue band, glyph, difficulty dots, or OG differentiation.
- Impact: library looks like an index, low visual memory; OG images are `.svg` (Twitter/Discord don't unfurl SVG — need PNG).
- Fix: build-time SVG covers (hue band + initial + pipeline glyph + difficulty dots) reused for card, landing, and OG; generate PNG fallbacks for `og:image`. Files: `build.py` `og_svg` + new `make_og.py`, card/landing templates.

### B5. Tables/diagrams fragile on mobile; images never lazy
- Evidence: `loading=lazy` ×0 in `build.py`; tables rely on overflow fallback; no lightbox wiring found on sampled pages (`lightbox` ×7 in code but no viewer confirmed live).
- Impact: architecture diagrams unreadable at 360px; shelf (259KB) + index (168KB) + search.json (125KB) all parse on load.
- Fix: diagram click → lightbox with zoom/pan + always-rendered caption/alt; sticky table headers + zebra + scroll-shadow hint; `loading=lazy` + width/height on all content images.

---

## C. UI/UX gaps

### C1. Reader has compact mobile chrome; other pages use old generic header — CONFIRMED (matches UX_AUDIT.md)
- Fix: unify single-row mobile header everywhere (logo mark + search-icon overlay + theme dot + menu). Separate TOC drawer vs Settings drawer, `Esc` closes. Then re-check 320px (wordmark currently hides by design — confirm touch targets ≥44px on device).

### C2. Shelf density — CONFIRMED (shelf.html 259KB, repeated cards/rails)
- Fix: cap rails to 6 visible + "View all" (deep-link filtered shelf), collapse past paths behind "Show path", keep result-count live. Target shelf <180KB.

### C3. Search is title/desc-only on shelf; search.json (125KB) ships but ranking unclear
- Fix: rank headings + tags above body, excerpt jump with prev/next + highlight-all, `Esc` clears; offline/`file://` fallback (inline index as `<script>` when fetch fails). No new deps.

### C4. Progress = scroll % only; Save exists but History/Completed unclear
- Evidence: `bookmark` ×3, `history` ×5 in build.py — feature is thin.
- Fix: per-section read dots (seen 3s in viewport) + "Mark complete" per chapter; library rows: Continue (cover + % + page), History (last 6), Bookmarks; completed → "Read again / Review cheatsheet" instead of vanishing.

### C5. Settings limited (Theme, zoom-A+, width)
- Fix: add line-height (1.6/1.75/1.9), font (Sans/Serif), Reset button. Replace `zoom` with `font-size: calc(18px * var(--fs))` so headings scale and AT text-scaling isn't broken.

### C6. Accessibility holes — CONFIRMED by code grep
- Missing: `preconnect` ×0 (fonts `@import` blocks render), `focus-trap` ×0, `aria-modal` ×0 (drawers trap nothing), `aria-current` ×3 only, `aria-label` on rails/arrows/search unverified, `--cat` yellows (#EAB308) on dark fail small-text contrast.
- Fix: `preconnect + display=swap + subset` fonts; drawer focus trap + `aria-modal`; `aria-current` on TOC; labeled rails/arrows/search; `--cat-ink` text-on-accent tokens for AA.

### C7. SEO partial
- Have: canonical, OG/Twitter tags, JSON-LD, sitemap, robots, `theme-color`, `prefetch` on book pages. Missing: OG PNGs, breadcrumb JSON-LD with prev/next in readers, `map.html` (451-byte redirect) weak as shared/standalone doc.

### C8. Print CSS thin; 404 exists but empty-state copy thin
- Fix: print forces light ink, expands rails, page-breaks per `.page`, never cuts code; 404 + empty search get search box + 3 suggested books.

---

## D. Prioritized fix list

### P0 (trust + reading, ~1 week)
1. A1 Start-Here single source of truth
2. A2 glossary markdown-link + counter fix
3. B1 lab checkboxes real + persisted, Reset wired
4. B2 code/terminal semantics + copy-code-only
5. B3 light/sepia leak sweep + reader theme switcher
6. C6 a11y minimum (focus trap, aria-current/labels, font preconnect, reduced-motion already ×5 — verify)
7. C8 print + 404/empty states

### P1 (discovery + retention, ~2 weeks)
8. A3 lab rename / split paths
9. A4 roadmap as ordered stepper, kill third taxonomy
10. B4 real covers + OG PNGs
11. B5 lightbox + tables + lazy images
12. C2 shelf density + size budget
13. C3 ranked global search + excerpt jumps + file:// fallback
14. C4 progress v2 (section dots, history, completed)
15. C5 settings (line-height, font, reset, no-zoom)
16. A5 real per-book dates + changelog ribbons

### P2 (delight + scale)
17. Highlights/notes (local-only), "Was this useful?" per page (`mailto:` prefilled, local tally)
18. Popular-search hints from local query log
19. Cheatsheet filterable board (Jenkins/Docker/Git/Kubectl/Terraform) with per-row copy
20. Lab 09 proposal (GHA → ArgoCD GitOps end-to-end) to close vendor-neutral gap
21. Contrast/Dim-OLED themes, `prefers-color-scheme` default on first visit
22. PWA manifest (GitHub Pages HTTPS only, keep `file://` fallback documented)

---

## E. Build/QC changes (`website/scripts/build.py`, `scripts/qc-check.py`)
- Glossary render through `md_inline()`; assert no `[`…`](` literals in output; assert term counter > 0.
- `[ ]` → checkbox transform + `Reset checks` wiring test.
- Code-fence → `<pre><code class="lang-*">` + header bar; fail on bare-"Copy" text nodes.
- Token-only theming check: no hard dark colors inside `.readbody` overrides; screenshot diff 4 pages × 3 themes.
- Taxonomy check: every `path` in `books.json` exists in `paths.json`; no "Quick topics" unless defined; shelf hero count == path count.
- `loading=lazy` + `width/height` on content images; fonts `preconnect`; shelf size budget alert >200KB.
- Sitemap `lastmod` from per-book `updated`; OG PNG existence check; breadcrumb JSON-LD on readers.
- Rebuild rule stays: any `pdf/*`, `books.json`, `paths.json`, `GLOSSARY.md`, `build.py` change → rebuild + `qc-check.py` + republish `dist/`.

## F. Verification checklist (sign-off per fix batch)
- [ ] Map/shelf/reader Start-Here counts + minutes identical
- [ ] Glossary: 0 raw `[` links, counter correct, anchor per term, filter works
- [ ] Lab 01: checkboxes toggle + persist reload, Reset clears, copy-code-only 10/10
- [ ] 4 pages × 3 themes screenshot: no dark leaks, AA contrast spot-check
- [ ] Keyboard-only journey (library → book → reader → search → settings), axe 0 critical
- [ ] Lighthouse ≥95 perf/a11y on index/shelf/reader/glossary/roadmap
- [ ] `file://` double-click test of `dist/index.html` passes
- [ ] Link checker 0 broken; `zoom` fully removed
