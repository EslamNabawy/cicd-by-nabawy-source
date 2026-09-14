# P1.2 UX Heuristic Audit — CICD BY Nabawy (live + dist)

**Date:** 2026-09-14 · **Scope:** 3 live URLs + local `website/dist/*.html` · **Method:** Nielsen heuristics + information-scent / scan-ability pass
**Live checked:** `https://eslamnabawy.github.io/cicd-by-nabawy/` · `/read/foundations.html` · `/glossary.html`
**Dist checked:** `dist/index.html` (380 lines), `dist/read/foundations.html` (751 lines), `dist/book/foundations.html`, `dist/glossary.html`, `website/scripts/build.py` (1012 lines), `content/books.json` (42 books), `content/paths.json` (9 paths)

---

## 1. Method

Walked three personas: (A) stranger on homepage deciding what to read first, (B) scanner browsing the shelf grid, (C) deep-link visitor landing on a single reader page from Google with zero site context. Each friction point below cites the exact DOM/CSS/JS that causes it.

---

## 2. Information Scent — "Can a stranger tell what to read first?"

### What works
- **Learning Paths grid** (`div.pathgrid` → `.pathcard`) is the only ordered guidance. Evidence `dist/index.html:298-299`:
  ```html
  <div class="collectlabel">LEARNING PATHS</div>
  <p class="sub">Ordered end to end — follow a path, don't wander shelves.</p>
  <div class="pathgrid"><div class="pathcard"><h3>Start Here</h3>…1. Foundations · 25 min … 2. Git, Branching → 50 min</div>
  ```
  Paths map cleanly to `paths.json:order = start-here → ci-core → delivery → jenkins-core → …`.

### Friction

| # | Heuristic | Friction | Evidence |
|---|-----------|----------|----------|
| S1 | Visibility of system status | **Hero gives no single next step.** `hero h1: "From commit to production, explained end to end"` + stats `42 books / 12 topics / 8 labs` tells *scale*, not sequence. The actual CTA is ambiguous: `★ Start here: Foundations` (filterbar), `Start Here` path card, `BROWSE EVERYTHING`, and `Roadmap`. Newcomer must infer order. | `dist/index.html:292-294`, `304` |
| S2 | Recognition vs recall | **Paths title is 11px mono, below hero.** ` .collectlabel { font-size:11px; letter-spacing:.6px; margin:56px 0 20px }` renders as a faint label, easy to scroll past. The path grid sits ~600px below hero on desktop; on mobile, hero + stats + continue/marks rows push it further. | `build.py:109`, `dist/index.html:297` |
| S3 | Consistency | **Count drift erodes trust.** Live hero says `42 books` (correct per `books.json` length), but `SITE_DESC` in `build.py:19` still says `39 concise technical books` and OG description inherited that. Live `web_extract` hero snippet returned `39 books`. A first-time visitor seeing mismatched counts questions freshness. | `build.py:19`, `books.json` (42 entries), `web_extract` homepage content |
| S4 | Help & documentation | **LEVELS rubric is decorative, not actionable.** `<div class="rubric"><div><b>Beginner</b> No prior CI/CD. Start with Foundations → Git → Pipelines.</div>…` looks clickable but is static text. No link from rubric to the actual path. | `dist/index.html:301` |

---

## 3. Scan-ability of the Shelf Grid

### What works
- `filterbar` (`#fcat`, `#fdif`, `#fsort`) updates `n shown` and hides empty shelves. `jumpnav` pills let you anchor-jump to a shelf.
- `.card::before { height:3px; background:var(--cat) }` gives a thin category accent. Cards show `difficulty · path` inline (e.g. `Beginner · jenkins-core`).

### Friction

| # | Heuristic | Friction | Evidence |
|---|-----------|----------|----------|
| G1 | Aesthetic & minimalist / Flexibility | **Horizontal rails hide 70% of inventory.** `.rail { display:flex; overflow-x:auto; scroll-snap-type:x mandatory } .rail .card { flex:0 0 272px }` — each shelf is a side-scrolling carousel, not a scannable grid. On a 1200px viewport only ~4 of 12 Jenkins cards are visible. Arrows scroll `320px` per click (`rail.scrollBy({left:320})` in `build.py:370`). No scrollbar affordance on macOS/Windows. Scan-ability drops because comparison requires horizontal scrubbing, not vertical scan. | `build.py:128-129`, `build.py:369` |
| G2 | Visibility | **5 shelves visible; rest hidden behind a button.** `SHOW_FIRST = 5` (`build.py:858`) → `Browse all topics ↓` + `<div id="morecats" style="display:none">`. `jumpnav` clicks reveal it (`build.py:371`), but a user filtering or scrolling never sees 3 hidden shelves. Web-extract homepage lists 8 shelves collapsed into an ellipsis — proof truncation. | `build.py:858-863` |
| G3 | Recognition | **Cover art carries zero information.** `<div class="coverart"><b>JD</b></div>` — two-letter initials on a gradient. Every card looks identical except 3px top rule. At 272px card width, initials `28px` (`build.py:202`) are illegible as cues vs full iconography available in `assets/icons/*` (used inside reader pages but not on cards). | `build.py:774-779`, `dist/index.html:307` |
| G4 | Consistency | **Two competing organizations: shelves vs paths vs filters.** Shelves grouped by `category` ("Jenkins · 12 books"), paths grouped by `path` ("Start Here", "CI Core"). A book like `pipelines` appears in `CI/CD` shelf but belongs to path `ci-core`. Filter `All categories` dropdown is category-based, `Sort: Path order` is path-based — mental model clash. Evidence: card footer says `Beginner · jenkins-core` (path slug leaked as UX). | `build.py:810-845`, `books.json:path` vs `category` |
| G5 | Error prevention | **Filter wipes shelves silently.** `filter() { $$('.shelf').forEach(s=> s.style.display = vis?'':'none') }` — if you type `q=lab` only `Labs` shelf remains; no summary ("4 shelves hidden"). `#empty` shows only when `n===0`. Partial match (e.g. `q=jenkins` → 1 shelf left) looks like the site only has 1 shelf. | `build.py:339-355` |
| G6 | Minimalism | **Jumpnav + filterbar + sort = 3 ways to do one job.** `jumpnav` (8 pills) + `filterbar` (3 selects + count) + `popsearch` row compete for attention directly above shelves. `popsearch` (`Popular: …`) renders from `cicdlib:qlog` localStorage — empty on first visit, showing blank space. | `dist/index.html:303-306` |
| G7 | Accessibility | **Rail snap + hidden overflow breaks keyboard nav.** Cards are `scroll-snap-align:start` but focus order still tab-through offscreen cards without visible indicator. No `aria-label` on rail; arrow buttons are `<button data-dir="-1">←</button>` with only `aria-label="Scroll left"` — screen reader gets no shelf name. | `build.py:96-98`, `build.py:813` |

---

## 4. Reader-Page Navigation — Deep-link visitor (search → single book, no context)

Tested persona: user Googles "CI CD artifact management" → lands on `read/artifacts.html`.

| # | Heuristic | Friction | Evidence |
|---|-----------|----------|----------|
| R1 | Visibility / Recognition | **Header breadcrumb shows nowhere.** `<nav class="crumbs"><a class="logo">CICD BY Nabawy</a><span class="here">CI/CD Foundations</span></nav>` — only logo + current title. No `Library / CI Core / Artifact Management` path. No path badge. A Googler cannot answer "where does this book sit?" without scrolling to bottom `Up next` or opening the TOC. | `dist/read/foundations.html:712-714`, `build.py:710-714` |
| R2 | Navigation / User control | **"Up next" and path context are bottom-only.** `<div class="upnext">Up next in Start Here → <a>Git, Branching…</a></div>` rendered via `path_next()` (`build.py:657`) appears after all pages + related box. Top of document has no orientation header (e.g. `1 of 2 in Start Here`). | `build.py:730`, `dist/read/foundations.html:657` |
| R3 | Consistency | **Prev/Next follows manifest order, not path order.** `prevb = books[idx-1]; nextb = books[idx+1]` (`build.py:663-664`). For `foundations` (idx 0) prev is empty, next is `git-branching` (coincidentally both manifest and path order). For `ci` (manifest idx 6) next is `build`, but path `ci-core` order is `pipelines → artifacts → ci → build → testing` — manifest and path diverge. Arrow keys `←/→ prev/next book` (`build.py:425-426`) therefore jump out of path. | `build.py:663-665`, `paths.json:order` |
| R4 | Discoverability | **TOC and settings share one tiny button row; TOC hidden on mobile.** `aside.toc { width:300px; position:sticky }` becomes `position:fixed; transform:translateX(-105%)` below 900px (`build.py:193`). Opened by `#tocbtn: ☰ Contents` and `#setbtn: ⚙ A⁺`. On the live extract the header collapsed to `☰ Contents / CI/CD Foundations / ⌘K` — crumbs truncated to `110px` (`build.py:214`). Deep-link mobile visitor sees title only, not the book's 10 sections. | `build.py:193-194`, `build.py:712-719` |
| R5 | Match with real world | **Book search placebo.** Header input `placeholder="Search in book…"` + `FindBook(q)` highlights `mark` on Enter (`build.py:419`), but homepage `placeholder="Search books…"` does global filter + dropdown to `book/<id>.html`. Same iconography (`⌘K` hint), different semantics, same box. First-time user types once, expects global results inside reader, gets silent local mark. | `build.py:715`, `build.py:411-418`, `build.py:361-362` |
| R6 | Help / Error recovery | **No escape hatch visible.** Logo links to `../index.html` but is styled as brand mark, not `← Library`. `Overview` button (`href="../book/<id>.html"`) is a 14px pill alongside `⚙ A⁺`, easy to miss. No persistent `Back to Library` or `View this book in its path` affordance. Breadcrumb `Library` appears only in JSON-LD, not in UI. | `build.py:718` |
| R7 | Visibility | **Progress + settings are invisible affordances.** `#pbar` is `height:3px` on brand color (`build.py:721`). Reading progress stored as `cicdlib:prog:<id> {pct, ts}` in `scroll` handler (`build.py:408-410`) — but never surfaced inline (only via hidden `#resume` pill and homepage `PICK UP WHERE YOU LEFT OFF` rail). Settings (theme/font/width) live behind `#drawer` (`.drawer{display:none}`) — discoverable only by clicking `⚙ A⁺`. | `build.py:408-410`, `build.py:664-689` |
| R8 | Consistency | **Two artifacts per book confuse "where to read".** Reader header has `⭳ Open print HTML` (`../pdf/<file>`) linking to a paginated print edition vs the long-scrolling reader. `Overview` page (`book/<id>.html`) also links both. No guidance which to use; deep-link visitor may bounce to print HTML and lose TOC/related nav. | `build.py:725`, `book/foundations.html:card` |

---

## 5. Glossary & Peripheral Pages

| # | Finding | Evidence |
|---|---------|----------|
| Gl1 | Glossary table is dense but functional. Filter input `placeholder="Filter terms…"` works (`$('#q').addEventListener('input',…)` per row). However table has no sticky header on long scroll, no letter nav, duplicate rows existed (`Canary Deployment` appears twice in web_extract before dedupe via `seen` set in `build.py:933-934`). | `web_extract glossary content`, `build.py:938` |
| Gl2 | Glossary is unlinked from reader. No glossary tooltip or `Glossary` pill inside book pages — only via homepage `Glossary` btn and footer. A term-heavy sentence like `Build once, promote the digest` cannot jump to definition. | `build.py:710-719` (header has no Glossary link in reader) |

---

## 6. Other Concrete Nits Flagged

- **Duplicate description field truncated mid-sentence in `build.py:772` + library cards `p` clamped to 3 lines** — some cards show clipped sentence (e.g. `Testing Strategy: Pyramid, placement, flaky policy.` loses nuance).
- **Dark-theme-optimized icons leak:** `.coverart b { color:#fff; text-shadow:0 1px 8px rgba(0,0,0,.5)}` is white-on-dark; on sepia/light `card` background contrast still poor for `--card:#fffdf7`.
- **`search.json` (= global index) and `SEARCH_IDX` (inline script) duplicate** — same 42 entries shipped twice; not a UX bug but impacts first-paint weight.
- **Resume pill `position:fixed; right:20px; bottom:20px`** obscures footer content on short pages; no dismiss.

---

## 7. Ranked Friction List (likely user impact, highest first)

| Rank | ID | Surface | Heuristic | One-line impact | Effort to fix |
|------|----|---------|-----------|-----------------|---------------|
| 1 | **R1** | Reader header | Visibility | Search visitor cannot orient — no path/site breadcrumb | S |
| 2 | **G1** | Shelf rails | Scan-ability | Inventory appears smaller than it is; horizontal scroll hides books | M |
| 3 | **S1** | Homepage hero | Scent | No single "read this first" — choice overload on cold start | S |
| 4 | **R3** | Reader chapnav | Navigation | Next/Prev jumps out of the Learning Path you just chose | S |
| 5 | **R5** | Reader search | Consistency | In-book search looks like global search but behaves differently | S |
| 6 | **G2** | Homepage shelves | Visibility | 3 shelves permanently hidden behind collapse | S |
| 7 | **R2** | Reader bottom | Orientation | "Up next" only at bottom — top of long book gives no next step | S |
| 8 | **G3** | Card | Recognition | Initials covers carry no scent; all cards look alike | M |
| 9 | **R4** | Reader TOC | Discoverability | TOC hidden on mobile behind hamburger; 10-section book looks like 1 page | S |
| 10 | **S3** | Counts | Trust | 39 vs 42 drift signals stale site | XS |
| 11 | **G4** | Taxonomy | Mental model | Category vs Path mismatch confuses filters | M |
| 12 | **R7** | Progress | Feedback | Progress exists but only visible after leaving | S |

---

## 8. Top 5 to Fix — Phase 2 Scope

> These five are the Phase 2 build list. Each is actionable against `website/scripts/build.py` + `dist/*.html` and verifiable with one acceptance check.

### 1) Reader orientation header (fixes R1 + R2)
**What:** Add a persistent strip above the book title showing `Library › {Path.label} › {Book}  ·  {idx} of {n} in path` with links, plus duplicate `Up next →` cue at **top** of reader (below cover, not only bottom). Breadcrumb also replaces the bare `<span class="here">`.
**File:** `build.py: define path_pos(b)=f"{n} of {len(seq)}"`, inject into `reader_url` template `build.py:687-732` header + just under `readbody` open.
**Accept:** Deep-link `read/artifacts.html` shows `Library › CI Core › 2 of 5` in header; top `Up next` visible without scrolling.

### 2) Make shelves vertically scannable (fixes G1 + G2)
**What:** Default shelves to CSS grid (not rail) on desktop; keep rail only as opt-in. Remove `SHOW_FIRST=5` collapse — render all shelves. Preserve rails only where justified (add `data-rail="true"`). Remove or de-emphasize `popsearch` when empty.
**File:** `build.py:128-130 (.rail/.grid), 858-864 (SHOW_FIRST logic), 855-857 (rendered)`.
**Accept:** `index.html` renders 0 `.rail` by default on 1200px; all shelves visible without clicking `Browse all topics`; `dist/index.html` has no `#morecats[display:none]`.

### 3) Single cold-start CTA on homepage (fixes S1)
**What:** Hero action row: one primary button `★ Start with Foundations — 25 min` (path 1/1) + secondary `Explore full map` linking to `roadmap/`. Move `BROWSE EVERYTHING` filterbar **below** paths, not competing above shelves. Promote `collectlabel LEARNING PATHS` to real heading.
**File:** `build.py:898-905 (hero + pathgrid)`.
**Accept:** First viewport on `index.html` (no scroll) shows exactly one primary CTA whose href is `read/foundations.html`.

### 4) Reader navigation = path order, not manifest order (fixes R3 + R2)
**What:** `prevb/nextb` derived from `bypath[book.path]` sequence, not `books[idx±1]`. Chapnav labels show path label (`CI Core · 1 → 2`). Arrow keys follow same order. `prefetch` points to path next.
**File:** `build.py:653-666, 684-685, 694`.
**Accept:** On `read/ci.html` (ci-core position 3), Next = `Build Systems`, not whatever manifest had; `←/→` matches displayed chapnav.

### 5) Disambiguate the two searches (fixes R5 + R4)
**What:** Reader search input relabeled `Find in this book` (aria-label + placeholder) with inline hint `↵ highlights · Esc clears`; dropdown not shown. Homepage search placeholder `Search all 42 books…` with hint `Goes to overview`. Add `T Contents` hint as a visible link next to reader search, not only in settings panel. On mobile, keep TOC button label `Contents — 10 sections` so depth is visible at entry.
**File:** `build.py:715-716 (#q), 731-735 (drawer), 413-420 (findBook)`.
**Accept:** Reader `#q` placeholder contains `in this book`; homepage `#q` placeholder contains `all 42 books`; TOC button text includes section count.

---

## Appendix — Evidence Snippets Index

- Homepage live + dist: `web_extract:https://eslamnabawy.github.io/cicd-by-nabawy/` § hero/stats/pathgrid/rails; `dist/index.html:291-313`
- Reader live + dist: `web_extract:/read/foundations.html` § lifecycle table + pipeline diagram; `dist/read/foundations.html:1-751` (cover at `p1`, system map at `p10`, `upnext/related/ratebox/chapnav` at 657-661, JS prefs at 695-748)
- Glossary live + dist: `web_extract:/glossary.html` (50 terms, canary duplicate), `dist/glossary.html:1-289`
- Build logic: `build.py:19 SITE_DESC`, `128-130 rail`, `340-355 filter`, `360-372 drop/render`, `653-666 related/path_next`, `774-785 card()`, `810-863 shelf()`, `858 SHOW_FIRST`, `933-953 glossary dedupe`
- Content truth: `content/books.json` 42 entries; `content/paths.json` 9 path labels
