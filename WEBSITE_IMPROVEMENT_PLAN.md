# Website Improvement Plan — CICD BY Nabawy
**Date:** 2026-09-13
**Scope:** `website/dist/` (library, reader, roadmap, glossary) + `website/content/books.json` + `website/scripts/build.py` + source Markdown/PDF in `CI-CD/`
**Goal:** Turn solid static library into premium technical reading platform. Better UI, better UX, stronger content.

---

## 1. Executive Summary

The site already does a lot right:

- 39 books, data-driven via `books.json`, no-build static output works from `file://`
- Dark / Light themes with CSS tokens, localStorage prefs + progress, resume
- Reader with TOC scroll-spy, in-book search (Ctrl+K), copy buttons, prev/next, print stylesheet, SEO tags + sitemap + JSON-LD
- Library with shelves, rails, jump nav, glossary, roadmap

Main gaps fall in 3 buckets:

1. **UI:** strong dark engineering identity, but visual system incomplete. No real covers, category color only, typography scale flat, code/terminal/callout styles inherit from PDF CSS and clash with site tokens, light theme is afterthought, mobile header wraps awkwardly.
2. **UX:** discovery weak (title-only search, no filters, no difficulty/category filter, no learning paths), reader flow weak (no book landing page, no reading-time, no bookmarks, no history, no related content, TOC generated from `<h3>` only, progress is scroll % not real read state), no onboarding for beginners.
3. **Content:** good depth (CI/CD + Jenkins + labs), but inconsistent. Descriptions 1-line, no prerequisites, no outcomes, no estimated time, glossary has duplicate Canary entry and dead links, no version/date/author metadata on cards, labs not visually distinct, no cross-links between related books.

This plan fixes that in 4 phases. P0 first for max impact with minimal build.py changes.

---

## 2. Method

Inspected:

- `website/README.md`, `WEBSITE_BUILD_SPEC.md` (spec = library + reader + themes + search + TOC + progress)
- `website/content/books.json` (39 entries: id/title/file/category/difficulty/description)
- `website/scripts/build.py` (705 lines: BASE_CSS, INDEX_JS, READER_JS, PageGrabber, toc_of, roadmap, index, reader, glossary, sitemap)
- `website/dist/index.html`, `dist/read/foundations.html`, `dist/roadmap/index.html`, `dist/glossary.html`
- `GLOSSARY.md`, `CONTENT_MAP.md`, `PROJECT_PLAN.md`, sample Jenkins PDFs

Checked against: readability first, navigation second, comprehension third (per spec §57), plus a11y, responsive, performance, SEO.

---

## 3. Current-State Audit

### 3.1 UI — What Works
- Token system (`--bg, --ink, --mut, --acc, --cat`) shared across pages. Good.
- Card top-border in category color. Cheap, effective wayfinding.
- Hero restrained, no SaaS bloat. Matches spec §44.
- Sticky blurred header, pill search, pill buttons. Consistent radius.

### 3.2 UI — Issues

| # | Issue | Evidence | Impact |
|---|-------|----------|--------|
| U1 | No covers. All cards text-only | `card()` in build.py emits num/title/desc/difficulty only | Library looks like index, not library. Low click desire. No visual memory. |
| U2 | Typography flat | Body 1.5 line-height, headings 19-24px, reader inherits PDF CSS + `zoom` for font size | Long reads fatigue. `zoom` breaks layout, non-standard. Headings don't scale with setting. |
| U3 | Code style collision | `scope_css()` scopes PDF CSS to `.readbody` but PDF variables (`--paper, --ink, --line`) override site tokens in dark mode via overrides block | Code blocks look different per book. Copy bar injected via JS, inconsistent spacing. No language label, no line numbers, no wrap toggle. |
| U4 | Light theme incomplete | `BASE_CSS` light overrides only top-level tokens. PDF-embedded tables/diagrams/callouts keep dark backgrounds | Half-themed pages. Contrast failures. |
| U5 | Callouts/labs not distinct | Labs are same `.page` as concepts. No Objective/Prereq/Verify/Cleanup treatment in reader despite spec §31 | Labs blend in. Users can't scan steps vs explanation vs expected output. |
| U6 | Tables/diagrams fragile on mobile | `display:block; overflow-x:auto` fallback only. No zoom viewer, no caption style | Architecture diagrams unreadable on 360px. Tables scroll blind. |
| U7 | Header wraps on mobile | `@media 900px` forces `.search{flex-basis:100%; order:5}` → 2-row header + TOC button + crumbs crowd | Loses 120px vertical space. Search pushed down. |
| U8 | No design tokens for spacing/type | Spacing ad-hoc (22px, 24px, 32px). No `--space-*`, `--font-*`, `--radius-*` scale | Future edits drift. Light/dark diverge. |
| U9 | Focus + reduced-motion partial | `:focus-visible` exists, but TOC drawer has no focus trap, no `prefers-reduced-motion` guard despite spec §58 | Keyboard/screen-reader users stuck. Motion-sensitive users get rail smooth-scroll. |
| U10 | Print CSS thin | Hides nav but doesn't expand rails, doesn't force light ink, doesn't add page breaks per `.page` | Printouts waste ink, cut code blocks. |

### 3.3 UX — What Works
- Continue Reading rail + floating Resume pill. Good retention hook.
- Scroll-spy TOC (`tocUpdate`), Ctrl+K, T / ← / → / Esc shortcuts. Power-user friendly.
- Progress bar top + per-card `%`. Local, no login.

### 3.4 UX — Issues

| # | Issue | Evidence | Impact |
|---|-------|----------|--------|
| X1 | Search title-only | `filter(q)` matches `dataset.title + dataset.desc`. Reader `findBook` walks text nodes, no ranking, no global search | Can't find "merge queue" unless in title. No cross-book search. Spec §24 unmet. |
| X2 | No filter/sort | No category pills, no difficulty filter, no sort (A-Z, level, pages). Jumpnav is anchor list only | 39 books unsortable. New user overwhelmed. Jenkins 12-book rail endless. |
| X3 | No book landing page | `reader_url = read/{id}.html` goes straight to content. Spec §9 (Start/Continue/TOC/Prereqs/Related) missing | No commitment step. No time estimate. No prereqs. Bounce risk. |
| X4 | No learning paths | Roadmap is category-grouped zigzag timeline (`START·01 → FINISH`). Not ordered by dependency. `Quick topics` + `Core practices` + `Series edition` sorted by count, confusing | Beginner doesn't know Foundations → Git → Pipelines → Jenkins Setup order. Roadmap ≠ path. |
| X5 | TOC shallow + brittle | `toc_of()` grabs `<h3>` only, falls back to `Cover — label`. No h2/h4 nesting, no numbers | 3-page books show 5-7 flat links. No chapter/section hierarchy. Long books unnavigable. |
| X6 | Progress = scroll % | `scrollTop / (scrollHeight-clientHeight)` saved on scroll. 100% = bottom reached, even if skimmed | False completion. No per-section check, no time-spent, no lab done state. |
| X7 | No bookmarks/history | No bookmark button, no history list, only in-progress (<100%) shown. Completed books vanish | Return users lose place. No "read again" path. |
| X8 | No related content | `chapnav` only prev/next in manifest order (alphabetical-ish, not pedagogical). No Related Topics/Books per spec §33 | Siloed reading. Git → CI → Jenkins link opportunity lost. |
| X9 | Onboarding zero | Hero says "39 concise books" + stats. No "Start here", no 5-min tour, no role selector (Dev / QA / Ops / Beginner) | First visit = shelf wall. High pogo. |
| X10 | Empty states + errors thin | `#empty` suggests Foundations only. No 404 page, no broken-asset fallback (spec §63 wants Retry/Back-to-Library) | Dead ends on GitHub Pages deep links. |
| X11 | Settings limited | Theme (Light/Dark), fs via `zoom` (0.9/1/1.2/1.4), width (680/820/1020). No line-height, no font family (sans/serif/mono), no reset button despite spec §23 | Accessibility gap. Dyslexia / serif preference ignored. |
| X12 | Copy UX incomplete | Terminal copy grabs `innerText` (includes `$` + output). Code blocks from PDF have no copy button, only `.terminal` gets one | Copy-paste breaks. Users copy expected output as command. |

### 3.5 Content — What Works
- Coverage strong: foundations → pipelines → artifacts → delivery/deployment → security → observability → Jenkins deep (12) → GitLab/Argo/IaC → 8 labs → cheatsheet.
- Descriptions punchy, consistent voice ("Build once, promote digest everywhere").
- Glossary 50+ terms with related-topic links.

### 3.6 Content — Issues

| # | Issue | Evidence | Impact |
|---|-------|----------|--------|
| C1 | Descriptions too short, no metadata | books.json: 1 sentence, no `time`, `prereqs`, `outcomes`, `version`, `updated` | Can't show "25 min · Beginner · No prereqs". SEO thin. Cards undifferentiated. |
| C2 | Glossary defects | Duplicate "Canary Deployment" rows (lines 10/16), "Floci" typo?, "Planned: Deployment Strategies" dead ref, pipe-table regex fragile | Trust hit. Glossary page renders dupes. |
| C3 | No reading time / difficulty rubric | Difficulty assigned but undefined. No word-count → time calc in build.py | Users can't plan. "Advanced" means what? |
| C4 | Labs same voice as concepts | Lab descriptions ("Break prod, redeploy digest") fun but no Objective/Verify/Cleanup preview on card | Users can't tell lab duration, risk, env needs (Docker? Jenkins? AWS?). |
| C5 | Missing bridges | Jenkins books link generic concepts weakly. No "If you read X, read Y next" map. `CONTENT_CONNECTIVITY_PROMPT` applied but not surfaced in UI | Knowledge graph exists on disk, invisible on site. |
| C6 | No "What's new / Changelog" | Footer "v2.0 Sep 2026" static. No per-book Updated date, no recent-updates shelf | Returning users see no reason to revisit. |
| C7 | Images/diagrams undescribed | PDF assets copied verbatim. No alt-text audit, no captions in reader | A11y + SEO loss. Diagrams unsearchable. |
| C8 | Tone + ESL friction | Long sentences, idioms ("kill criteria", "ride train"), no summaries/TL;DR per chapter | Non-native readers struggle. Skim readers bounce. |
| C9 | No assessments | Spec mentions Quiz (§48) but zero quizzes/checks in reader | No comprehension loop. Labs verify manually only. |
| C10 | Series vs Books confusion | Library mixes 39 books + 9 Series omnibus editions + "Quick topics" + "Core practices" in same shelf sort (`sort by -n`) | Users don't know whether to read `Pipelines` or `S04 Pipelines`. Duplicate paths. |

### 3.7 SEO / A11y / Performance
- Good: canonical, OG, Twitter, JSON-LD TechArticle/CollectionPage, sitemap.xml + robots.txt, semantic `<main>/<aside>`, `lang=en`.
- Gaps: no `meta theme-color`, no OG image, no `aria-label` on rails/arrows/search, TOC links have no `aria-current`, images lack `loading=lazy` + `width/height` (CLS), Google Fonts `@import` blocks render (no `preconnect`), no `prefetch` for next book, `zoom` breaks text scaling for AT, contrast of `--mut #a0a0a0` on `#12151a` ~5.2:1 OK but `--cat` yellows (#EAB308) on dark fail for small text.

---

## 4. Improvement Plan

Principles: readability > navigation > comprehension > a11y > performance > polish. No framework migration. Stay static, no-build, `file://`-compatible. Every change = manifest + Markdown + `build.py` + rebuild + QC.

### Phase 0 — Foundation (1–2 days, P0, no visual break)

**0.1 Content model upgrade**
Extend `books.json` schema (backward compatible):

```json
{
  "id": "jenkins-pipelines",
  "title": "Jenkins Pipelines",
  "file": "pdf-10-jenkins-pipelines.html",
  "category": "Jenkins",
  "difficulty": "Intermediate",
  "description": "Jenkinsfiles: Declarative vs Scripted...",
  "time_minutes": 35,
  "prereqs": ["jenkins-setup", "pipelines"],
  "outcomes": ["Write Declarative Jenkinsfile", "Gate staging with approval"],
  "updated": "2026-09-01",
  "version": "2.0",
  "tags": ["jenkinsfile", "declarative", "multibranch"],
  "path": "jenkins-core",
  "lab_env": null
}
```

- Add `paths.json`: `foundations → ci-core → delivery → jenkins-core → jenkins-advanced → platforms → labs`
- Fix glossary: dedupe Canary, fix Floci → LocalStack? verify, replace "Planned:" with real links, add 10 missing terms (Trunk, Merge Queue already, Hermetic, JCasC, ARC, Review App OK, add Promotion, Rollback, Game Day OK... audit full list).
- Add `time_minutes` via word-count script (`words/200 + labs*15`).

**0.2 Build pipeline hardening**
- Split `BASE_CSS` → `styles/tokens.css`, `styles/library.css`, `styles/reader.css`, inlined at build (keep single-file output for `file://`).
- Replace `style.zoom` with `font-size: calc(18px * var(--fs))` + `--fs` on `.readbody`. Headings scale via `em`.
- Add build-time QC: broken internal links, missing alt, duplicate IDs, contrast spot-check, glossary dupes. Fail build on error. Reuse `scripts/qc-check.py`.
- Add `sitemap` lastmod from `updated` field, add `robots` + `404.html`.

Acceptance: `python scripts/build.py` green, `dist/` byte-similar, no visual regression.

### Phase 1 — UI Refresh (3–5 days, P0 — biggest perceived lift)

**1.1 Covers + card system**
- Generate CSS/SVG covers per book at build: category hue band + big initial + pipeline glyph + difficulty dots. No external images. Example: `Jenkins / PIPELINES / ●●○ / S→B→T→A→D strip`.
- Card layout: cover (4:3) → category + time → title → desc (2-line clamp) → outcomes on hover → Read + Bookmark buttons + progress.
- Keep `--cat` accent, add `--cat-ink` for text-on-accent AA compliance.

**1.2 Typography + reading scale**
- Adopt editorial scale: Display 40/48, H1 32, H2 24, H3 20, Body 18/1.7, Small 14, Mono 15/1.6 (JetBrains Mono fallback to Geist Mono).
- Reader settings: Theme [Dark|Light|Sepia], Size [S/M/L/XL → 16/18/20/22px], Width [Narrow 680 / Comfortable 760 / Wide 960], Line [1.6/1.75/1.9], Font [Sans/Serif]. Persist all. Add Reset.
- Fix light theme: scope PDF remnants — force `.readbody table, pre, .callout, .terminal` to use site tokens in both themes. Add Sepia `#faf6ed / #2b2620` for long reads.

**1.3 Code / terminal / callouts**
- Unify: every `pre` gets header bar (language dot + filename + Copy + Wrap toggle). Terminal gets `$` prompt styling, output in dim, copy-code-only (strip output via `data-cmd` attr at build).
- Syntax highlight lightweight: build-time Pygments → inline spans, no JS lib (keeps `file://`). Fallback to mono if no lexer.
- Callouts: NOTE/TIP/WARNING/IMPORTANT/BEST PRACTICE/COMMON MISTAKE with icon + tinted left border, collapsible on mobile.
- Labs: distinct template — Objective box, Prereqs chips, Steps numbered with checkboxes (localStorage), Command vs Expected Output split, Verify checklist, Troubleshooting accordion, Cleanup warning, "What This Proved" recap.

**1.4 Diagrams + tables**
- Diagram viewer: click → lightbox with zoom/pan (CSS only + 30-line JS), caption + alt always rendered, `loading=lazy`.
- Tables: sticky header, zebra, horizontal scroll with shadow hint, min cell 120px.

**1.5 Header / mobile**
- Single-row mobile header: logo mark only + search icon expanding to overlay + theme dot + menu. No wrap. TOC drawer + Settings drawer separate, focus-trapped, Esc closes, `aria-modal`.
- Add `prefers-reduced-motion: reduce` → disable smooth scroll, hover lift, rail snap.

Acceptance: Lighthouse ≥95 perf/a11y, cards recognizable at 320px, code copy correct 10/10 trials, light+sepia fully themed (no dark leaks via screenshot diff).

### Phase 2 — UX Overhaul (4–6 days, P1 — retention + discovery)

**2.1 Library discovery**
- Filter bar: Search + Category pills (All + 11) + Difficulty [Beginner/Intermediate/Advanced] + Type [Guide/Lab/Reference] + Sort [Path order / A-Z / Shortest / Newest]. Result count live. URL hash sync (`#q=jenkins&d=beginner`) for share.
- Shelves → Paths: replace count-sorted shelves with ordered paths: `Start Here (5) → CI Core (6) → Delivery & Deployment (6) → Jenkins Core (5) → Jenkins Advanced (7) → Platforms (3) → Labs (8) → Reference (1)`. Keep category rails as secondary view toggle [Paths|Topics].
- Hero v2: "New to CI/CD? Start with Foundations — 25 min" primary CTA + "I know Jenkins, take me to labs" secondary + role chips. Remove generic stats wall or move below.
- Continue Reading v2: show cover thumb + % + "Page 3/12 · Jenkins Agents" + Dismiss. History row (last 6 visited) + Bookmarks row. Completed → "Read again / Review cheatsheet".

**2.2 Book landing pages (`read/{id}.html` → `book/{id}.html` + reader)**
New `book/{id}.html` per spec §9:
Cover, title, desc, meta (time, pages, sections, level, updated, version), Start/Continue/Download PDF/Open print HTML, TOC preview, What you'll learn (outcomes), Prerequisites (linked chips), Related books (same path + tags), Author + changelog (last 3 updates).
- Keeps reader clean. Improves SEO (one URL per intent: overview vs content).

**2.3 Reader upgrades**
- TOC v2: nested h2/h3/h4 with numbers (1, 1.1, 1.1.1), collapsible sections, progress dots per section (read = seen 3s in viewport), "Mark complete" per chapter.
- Right rail (desktop ≥1200px): On this page mini-TOC + Copy page link + Bookmark + Print + Font quick (A−/A+). Collapses to toolbar on smaller.
- In-book search v2: match count, prev/next jumps, excerpt list, highlight all, Esc clears. Add global search index (`search.json` built from text + headings + glossary, 50KB, client-side Fuse-lite, no dep — simple ranked substring + tag boost).
- Related footer: Prev/Next in *path order* (not manifest order) + "Up next in Jenkins Core" + 3 Related (shared tags) + Back to Path.
- Bookmarks: per-section `🔖` toggle, stored `cicdlib:marks:{book}`. Bookmarks page/section in library.
- Lab mode: step checkboxes persist, "Copy all commands" button, reset lab progress.

**2.4 Empty / error / offline**
- `404.html` styled + search box + 3 suggested books.
- Broken image fallback: hide + log + show caption placeholder, never broken icon.
- Add manifest-less offline note: "Static files — works offline if saved. Add to Home Screen prompt copy." (No SW to keep `file://` compat; document PWA as future.)

Acceptance: find any concept <3 keystrokes + Enter, filter to Beginner Jenkins in 2 clicks, start-to-first-lab <4 clicks, bookmarks survive reload, TOC reflects real hierarchy on 5 sampled books.

### Phase 3 — Content Enhancement (ongoing, P1/P2 — authority + comprehension)

**3.1 Card + landing content pass (all 39)**
- Rewrite descriptions: 2 sentences (what + why) + 3 outcomes + time + prereqs. Example: Foundations → "Automate commit-to-prod with confidence. Learn CI vs delivery vs deployment and where pipelines, artifacts, and approvals fit." Outcomes: [Draw full lifecycle, Choose delivery vs deployment, Name 5 pipeline stages].
- Add per-book `TL;DR` box (4 bullets) at top of reader + `Key takeaways` at end (auto from outcomes).
- Standardize difficulty rubric: Beginner = no prior CI/CD, Intermediate = built a pipeline, Advanced = runs prod + owns security/recovery. Publish rubric on library.

**3.2 Cross-links + paths**
- Insert "Bridges" callout at end of each book: `← Prereq: X · Up next: Y · See also: Z`. Source from `prereqs` + `path` order + manual `related` field. Build validates targets exist.
- Roadmap rewrite: linear vertical stepper with mile numbers in path order, each stop shows time + level + done check (from progress). Keep category color dot, drop zigzag on desktop? Keep zigzag aesthetic but order by path, not category size.
- Glossary v2: table → cards with anchor URLs (`glossary.html#merge-queue`), "Mentioned in" book chips, autocomplete filter, link glossary terms inline in reader (first occurrence dotted underline + tooltip, toggleable).

**3.3 Labs upgrade**
- Each lab gets: Environment box (Docker 24+, 4GB, ports), Time (30/45/60 min), Risk (Safe/Destructive — rollback lab warns), Deliverable checklist, Solution hints collapsed, Cleanup mandatory.
- Add Lab 09 proposal: "GitHub Actions → ArgoCD GitOps end-to-end" to close vendor-neutral gap (GHA + Argo exist but no joint lab).
- Cheatsheet split: one page → filterable command board by tool (Jenkins/Docker/Git/Kubectl/Terraform) with copy per row.

**3.4 Freshness + trust**
- Per-book Updated + Version badge on card + landing. "New/Updated in Sep 2026" ribbon if <60 days.
- Changelog page (`updates.html`) from git log or manual `CHANGELOG.md`. Footer links: About, How to use this library, Difficulty guide, Updates, Glossary, Roadmap, Source.
- Author block: "By Nabawy — CI/CD engineer" + contact/GitHub link. Adds E-E-A-T for SEO.

**3.5 Media + a11y content**
- Alt-text sprint: every diagram gets 1-line alt + longer caption. Decorative icons `aria-hidden`.
- Add 1 hero diagram per core book (lifecycle, pipeline DAG, artifact promotion, Jenkins controller/agent) as inline SVG with `<title>/<desc>`.
- ESL pass: short sentences (<22 words), expand acronyms first use, add summaries. No idiom removal — add glossary links instead.

Acceptance: 0 glossary dupes/dead links, 39/39 have time/prereqs/outcomes/updated, labs all have env+verify+cleanup, link checker 0 broken, readability grade ≤10 (Flesch-Kincaid) on rewritten intros.

### Phase 4 — Polish + Growth (P2, after P0/P1 live)

- Themes: add Contrast (AAA) + Dim OLED. Theme respects `prefers-color-scheme` on first visit.
- Search analytics (privacy-local): log top queries in localStorage, surface "Popular: jenkins agents, canary, sbom" hints.
- Notes/highlights extension point: implement local-only highlight (selection → save → list on bookmarks page). No backend.
- SEO: OG images per book (build-time SVG → PNG), `theme-color`, canonical + prev/next link tags in reader, breadcrumb JSON-LD.
- Perf: fonts `preconnect + display=swap + subset`, images `avif/webp` with fallback, `prefetch` next-in-path, inline critical CSS already — add `defer` audit, total index <250KB HTML+CSS (excl. PDF embeds).
- Feedback loop: per-page "Was this useful? 👍/👎" → local tally + `mailto:` with prefilled book/section. No server.
- Versioning: keep `v2.x` footer + per-book history accordion (future: `?v=` snapshots).

---

## 5. Prioritized Backlog

### P0 — Ship first (week 1)
- [ ] Fix `zoom` → CSS var font-size, fix light-theme leaks, add sepia
- [ ] Covers via CSS/SVG, card time + level + progress
- [ ] Category + difficulty filters + sort + result count
- [ ] TOC nesting (h2/h3/h4) + section numbers
- [ ] Code header (lang + copy-code-only + wrap) + terminal split cmd/output
- [ ] Glossary dedupe + dead-link fix + anchor links
- [ ] books.json: add `time_minutes, prereqs, outcomes, updated` for top 10 trafficked books (Foundations, Pipelines, Jenkins Setup/Pipelines/Agents, Delivery, Security, Labs 01/06, Cheatsheet)
- [ ] Mobile header single-row + drawer focus trap + reduced-motion
- [ ] 404.html + image fallback + print CSS fix

### P1 — Path to premium (weeks 2–3)
- [ ] Book landing pages (`book/{id}.html`) + Start/Continue + Related
- [ ] Paths view (ordered) + Hero with Start-Here CTA + role chips
- [ ] Global `search.json` + ranked results + excerpt jump
- [ ] Bookmarks + History + Completed states
- [ ] Lab template (Objective→Proved with checkboxes + Verify + Cleanup)
- [ ] Related footer in path order + Bridges callouts
- [ ] Reading time for all 39 + difficulty rubric page
- [ ] Updates/Changelog page + per-book Updated badges
- [ ] Diagram lightbox + table sticky headers + captions/alt pass

### P2 — Delight + scale (month 2)
- [ ] Highlights/notes local-only, rating widget, popular searches
- [ ] OG images, breadcrumb JSON-LD, theme-color, prefetch
- [ ] Contrast/Dim themes, font family choice, line-height setting
- [ ] Lab 09 (GHA→ArgoCD), cheatsheet board, quiz/checks per chapter
- [ ] Series vs Books disambiguation (hide Series from main shelves → separate "Print editions" shelf)
- [ ] PWA manifest (optional, GitHub Pages HTTPS only, keep `file://` fallback)

---

## 6. File / Build Changes

| Area | Change | File |
|------|--------|------|
| Model | Add fields, add `paths.json`, `related` | `website/content/books.json`, `website/content/paths.json` |
| Styles | Split tokens/library/reader/print, add covers, callouts, labs, lightbox | `website/styles/*.css` → inlined by `scripts/build.py` |
| Library | Filters, sort, paths toggle, hero CTA, history/bookmarks rows | `build()` index template |
| Reader | Nested TOC, right rail, search v2, related footer, lab steps, bookmarks | `build()` reader template + `READER_JS` |
| Book pages | New template | `build_book_pages()` new func |
| Search | Build `dist/search.json` (id/title/headings/text/tags, stripped) | `build_search()` new func |
| Glossary | Cards, anchors, mentioned-in, inline term linking | glossary template + reader post-process |
| SEO | OG images, theme-color, 404, breadcrumb LD | templates + `scripts/make_og.py` |
| QC | Link/alt/ID/dupe/contrast checks, fail-fast | `scripts/qc-check.py` extended |

No new runtime deps. Python stdlib only. Output stays static, `file://`-safe (no fetch — inline `search.json` as `<script>` on library page if needed for file protocol, else fetch with fallback).

---

## 7. Metrics — How We Know It Worked

- Discovery: search-to-open <15s median (manual test 5 queries), filter use covers 80% of visits (local log sample), bounce from library −20%.
- Reading: avg scroll depth +15%, lab checkbox completion logged, bookmarks created ≥1 per return visitor, "Up next" click-through ≥30%.
- Content: 0 broken links, 0 glossary dupes, 39/39 complete metadata, Lighthouse 95+ across index/reader/glossary/roadmap, print-to-PDF readable without cuts.
- Accessibility: keyboard-only full journey (library → book → reader → search → settings), axe 0 critical, contrast AA 100% text.

---

## 8. Risks + Guards

- **Scope creep (framework rewrite):** Guard — stay static. No React/Vue. CSS+vanilla only.
- **PDF drift:** Guard — readers embed at build. Any `pdf/*`, `books.json`, `GLOSSARY.md`, `build.py` change → rebuild + QC + republish. Already documented, enforce in CI.
- **Theme QA explosion:** Guard — screenshot 4 pages × 3 themes × 2 widths per PR. Token-only theming, no per-component colors.
- **`file://` breakage (fetch, SW, modules):** Guard — no `fetch()` for critical path, no ES modules, no SW. Test by double-clicking `dist/index.html`.
- **Content dilution:** Guard — no summarization to fit UI. UI adapts to content (spec §66). Long books get paged TOC, not trimmed text.

---

## 9. Next Step

1. Approve P0 list (or cut to 5 items for 2-day sprint).
2. Run Phase 0 model upgrade (books.json + glossary fix + font-size fix).
3. Rebuild + QC + deploy to Pages, then start Phase 1 covers + filters.

*Source: full audit of `website/dist`, `website/scripts/build.py`, `books.json`, spec, glossary, content map. No content deleted, no URLs broken — all changes additive or in-place.*

---

## 10. Execution Log — 2026-09-13 (P0 shipped)

- Installed Python 3.12.10 via winget (was missing; build needs it).
- `books.json`: all 39 enriched (time_minutes, prereqs, outcomes, tags, path, updated 2026-09-01, version 2.0). New `website/content/paths.json` (8 learning paths).
- `GLOSSARY.md`: removed duplicate Canary row.
- `website/scripts/build.py`: sepia theme + light/sepia leak guards, px font-size (zoom removed), nested TOC h2/h3/h4 with numbers, covers + time/version/path on cards, category/difficulty filter + sort + count + hash share, theme cycle dark→light→sepia, code headers copy/wrap, terminal copy fix, image lazy+fallback, print CSS, reduced-motion, glossary dedupe+anchors, 404.html, search.json.
- Rebuild: `BUILT roadmap: 39 books in 5 sections` + `BUILT 39 books + index + glossary`. Note: must run with `PYTHONUTF8=1` on Windows (console `→` char).
- QC: `scripts/qc-check.py` ALL GREEN. Verify script 15/15 PASS (filters, covers, TOC, sepia, codehead, glossary anchors, search.json, 404, reduced-motion).
- Remaining: commit + push to republish Pages. P1 still open (book landing pages, paths view, global search UI, bookmarks/history, lab template, related footer, changelog).

## 11. Execution Log — 2026-09-13 (P1 shipped)

- `dist/book/{id}.html`: 39 landing pages (cover, time/level/version/updated, Start/Continue auto-label from progress, prereq chips, outcomes, contents preview, up-next-in-path, related). Cards link title → Overview, Read → reader.
- Library: Learning Paths grid (8 paths, ordered, per-book time/level, totals), Levels rubric strip, search dropdown (ranked title>tag>text, top 8 → book pages, file:// safe via inlined SEARCH_IDX), Saved row (bookmarks), Completed chips + Recently Viewed, Updates footer link.
- Reader: ☆ Save bookmark btn (cicdlib:marks), lab banner (time/env/overview/reset) on lab books, `.step` checkboxes persisted (cicdlib:lab:{id}), Up-next-in-path box, Related box (tag/category scored), diagram lightbox, sticky table headers, Overview header link.
- `dist/updates.html`: full book table (category/level/ver/updated/time). Sitemap adds 39 book URLs + updates.
- Rebuild + QC green. P1 verify 18/18 PASS. P0 re-verify 14/15 (1 stale check string — time meta confirmed present as "20 min · Updated 2026-09-01").
- Remaining: commit + push. P2 still open (highlights/notes, OG images, extra themes, Lab 09, quizzes, Series-vs-Books split, PWA).

## 12. Execution Log — 2026-09-13 (P2 shipped)

- Themes: Dim (OLED) + Contrast (AAA, yellow links, 2px borders). 5-state cycle dark→light→sepia→dim→contrast synced across library, reader, book pages, roadmap.
- Reader settings: Font Sans/Serif + Line height Tight/Comfort/Roomy (`--lh` var, persisted). Serif keeps mono for code.
- Engagement: per-book 👍/👎 rating (local, thanks state), Popular searches (local query log, top 5 clickable), copy-section-link via `C` key (copies URL + current `#pN`).
- SEO/perf: 40 OG SVGs (`dist/og/{id}.svg` + `library.svg`, category color), og:image on index/reader/book, theme-color everywhere, BreadcrumbList LD on reader + book, prefetch up-next/next in reader + book→reader, Series edition shelf pinned last.
- Rebuild + QC green. P2 verify 20/20 PASS. P1 re-verify still green.
- Deferred (need content pipeline or bigger builds): full text highlights/notes, Lab 09 joint GHA→ArgoCD lab, cheatsheet tool board, per-chapter quizzes, PWA manifest.
- Remaining: commit + push to republish Pages.
