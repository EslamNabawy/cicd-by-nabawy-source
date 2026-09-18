# STRUCTURE MAP — Concept & Data-Mapping Proposal

Branch: `feature/structure-map-view` · Route proposed: `map.html` (`/map.html`)
Source of truth: `books.json` (42 books) — no second manifest.
Status: **D.1 — design only, no code written. Needs your sign-off (D.gate) before any build.**

---

## 1. What each block maps to

**Recommendation: one block per `books.json` `category`, derived at build time.**

- There are 12 distinct `category` values today: `CI/CD (9), Jenkins (12), Labs (8), Platforms (3), Roadmap (3), Build (1), Testing (1), Delivery (1), Security (1), Reliability (1), Reference (1), GitHub (1)`. That's unbalanced — some 1-book singletons look thin if taken literally.
- Alternative groupings were considered:
  - *By `difficulty`* (Beginner/Intermediate/Advanced) — would mix unrelated topics (e.g. `jenkins-setup` next to `foundations`) and lose the category storytelling.
  - *By dependency order* (a layered floor/dependency stack) — interesting, but invents a new taxonomy not present in `books.json` and would need hand-maintained layer metadata.
- Why category wins: it **already is the site's contract**. `build.py`'s `[data-cat]` accent map and `[--cat]` per-card color, plus `books.json` itself, already treat `category` as the grouping key. Deriving blocks from `category` at build time means adding a book or changing its category automatically adds/resizes a block — no parallel manifest to keep in sync.

**What about the singletons?** They render as intentionally small, secondary blocks (like narrow service blocks around a building), not as a broken sparse layout. B3.3 explicitly checks that a 1-book group still looks intentional.

---

## 2. What each block face shows (zoomed-out view)

Each block is an angled card (≈ isometric via `transform` + `box-shadow` for depth — see §4) showing, top-to-bottom:

- A thin `3px` top accent in the existing per-category color (`--cat`, already used on cards via `.card::before`).
- The category's representative icon (the same glyph already associated with perhaps the Jenkins/Git icons — reuse the existing per-category icon choice; monochrome icons use `currentColor` so they already obey the theme).
- **Category name** (e.g. "Jenkins", "Labs", "Platforms") — the `category` string verbatim.
- **Count** — e.g. "12 books", "1 book" — derived from the grouped data, not hard-coded.
- **Difficulty spread** as a compact pill row — tiny dots in category color with labels: e.g. "3 Beg · 5 Int · 1 Adv" (counts derived from `difficulty` per group; omitted if a group is uniform).
- Subtle depth via `box-shadow: var(--shadow-lift)` and a slight `transform: perspective(600px) rotateX(6deg) rotateY(-10deg)` on hover — cheap, no extra assets.

---

## 3. What "zoom in" reveals

**Reuse the existing book-card component, filtered to the clicked group.**

- Clicking a block transitions to a detail view that renders the same `.card` markup already used on the homepage shelves (same padding, radius, accent, Read/Overview buttons, `Read →` link to `read/<id>.html`). The detail view is just that category's books in a flat grid (not another 3D layout) with a clear **"← Back to map"** affordance plus browser back support.
- Why not a new renderer: the homepage card is the site's canonical book presentation. A second renderer would duplicate styling, link logic, and `books.json` → card mapping. Filtering the existing cards by `data-cat` keeps one source of truth.
- URL is meaningfully addressable: `/map.html#platforms` (or `#jenkins`) — each group gets an anchor. Back/forward cycle between `#` and bare `map.html` (zoomed-out) without a full page reload.

---

## 4. Visual approach — trade-offs and recommendation

**Option (a) — Pseudo-3D / isometric CSS (recommended)**

- Implementation: each block is a regular flat card, given depth only through `box-shadow` + a modest `perspective`/`rotateX`/`rotateY` on the container. Keyboard focus ring and borders remain straightforward to theme because the underlying element is still a flat card.
- Theming: reuses the existing `--bg/--card/--ink/--line/--brand` tokens — no new hex values. The per-category `--cat` color continues to come from `books.json`.
- Mobile + reduced-motion fallback: the angled transforms are removed via a media query (`@media (max-width: 600px)` stacks blocks as a plain tappable list/grid) and `prefers-reduced-motion` skips the scale/transition entirely and jumps directly. Keyboard nav stays as normal tab order over the flat list.

**Option (b) — True CSS 3D (`transform-style: preserve-3d`, `perspective`, cube faces)**

- More literal "building" with side faces and depth, but every face needs its own background/border/shadow handling per theme, focus rings become 3D-projected, and touch targets become tricky on narrow viewports. The current site has no 3D precedent; this would be the first, and it would need to be re-tested for every theme/mobile/reduced-motion combo.
- Verdict: **not recommended for a solo-maintained static site**. The visual payoff over (a) is modest relative to the ongoing maintenance cost, and a wrong 3D implementation is much harder to unwind.

**Recommendation: (a) — lightweight pseudo-3D.** It reads as "structure" at a glance, degrades trivially on mobile, and is provably correct across themes because it reuses the existing card styling that your last contrast fix already made robust.

---

## 5. Route & nav

- **Proposed URL:** `map.html` at the site root (same level as `index.html` and `glossary.html`), accessible as `/map.html` and `/map.html#<category>`.
- **Nav placement:** new link **Map** alongside **Roadmap** and **Glossary** in `header.top .wrap` (after Search, before theme toggle — same row as the other top-level views). This keeps the map as a first-class view rather than a buried footer link, and it mirrors the Roadmap entry point.
- **Chrome inheritance:** the new page reuses the existing header/footer chrome and theme toggle verbatim (same sticky header, same brand mark, same pills). It is not a standalone unstyled page.

---

## 6. Accessibility & reduced-motion fallback

- **Keyboard-only:** every block is a focusable, activatable element (`<a>` with `href="#<category>"` or `<button>` with `aria-label="<Category>, 12 books"`). Tab reaches blocks in visual order; Enter/Space activates the same detail view as a click; visible focus styling reuses the site's existing `focus-visible` outline.
- **Reduced motion** (`prefers-reduced-motion: reduce`): zoom animation disabled — the transition becomes an instant jump to the detail anchor. Detail view is still reached and back navigation still works; nothing is "gracefully missing."
- **No-JS / degraded JS:** blocks are real links to their fragment (`#platforms` etc.) and the detail views are anchor targets in the same document, so the map is still a usable categorized index even if the zoom JS never runs.
- **Screen readers:** each block carries an `aria-label` like `"Jenkins — 12 books, 2 Beginner 6 Intermediate 4 Advanced"` plus the per-category icon with `alt=""` (decorative).

---

## 7. What does NOT change

This is **strictly additive**:

- `index.html` (homepage / shelf view), every `read/<id>.html` reader page, `glossary.html`, `roadmap/`, and the existing header theme toggle are **not modified** by this feature except to add one nav link (`Map`) to the header's link row. No existing CSS for cards/shelves/readers is removed or overwritten.
- The existing `books.json` → card pipeline is reused, not replaced. The map's data is a build-time-derived view of the same 42 entries — there is exactly one source of truth.
- Adding a book (new `category`, new `difficulty` spread) or renaming a category automatically flows into the map without hand-editing a second manifest — derived counts/labels are computed in `build.py`.

---

## Questions for D.gate (your sign-off)

1. **Grouping:** one block per `category` as above — approved, or would you prefer a different grouping (difficulty layers, or a merged topology like Foundations → Core → Delivery → Platforms)?
2. **Visual approach:** (a) pseudo-3D as recommended — approved?
3. **Route & nav:** `/map.html` with a Map link next to Roadmap/Glossary — confirmed?
4. **Anything to change or explicitly exclude before build starts?**

Reply with your answers to 1–3 (e.g. `category / a / /map.html + header ok`) plus any edits, and I'll build the rest autonomously.


---

## Addendum — Rev 2026-09-14: Sepia default + Exterior & Interior overhaul (feat/sepia-map-polish)

This addendum reflects the UI as actually shipped after the combined sepia + structure-map polish. The original proposal (above) described the initial weak version; this section is the accurate record.

### Sepia theme (now default)

- **Tokens:** `--bg:#F6F1E7` (warm cream, within #F4ECD8–#F8F1E3 range), `--bg2:#EDE3CC`, `--card:#FFFBF0`, `--ink:#3B2F1E` (warm dark brown), `--mut:#6F665A` (warm muted, 5.01:1 on bg — passes AA), `--line:rgba(59,47,30,.16)`, warm `shadow` tints. Checked: ink 11.58:1 on bg (AAA), mut 5.01:1 (AA).
- **Brand accent decision:** `#18E299` (original brand) on sepia `#F6F1E7` is 1.51:1 — fails even large-text AA, reads too cool against warm palette. Warmed variant **`#0B9B68`** used consistently for sepia (`--acc`/`--brand`): 3.16:1 on bg (passes large-text AA, sufficient for borders/buttons/accents) and 3.44:1 on card. Dark and light keep `#18E299` unchanged. Reader `--acc-soft` is `rgba(11,155,104,.11)` (warm-transparent) instead of cool `#d4fae8`.
- **Default & cycle:** First paint is `sepia` when no saved preference exists (synchronous `<script>` in `<head>` before any paint, respecting `localStorage['cicdlib:pref']` — returning visitors keep their choice). Toggle cycles `sepia → dark → light → dim → contrast → sepia` (sepia first). All 5 theme placements (`THEMES`/`RTHEMES`/`THS`/`THX`) updated.
- **Icon audit vs sepia:** All 20 registered icons audited. Lucide line glyphs use `stroke="currentColor"` and render via `filter:brightness(0)` (black) on light/sepia, `filter:invert(1)` on dark — correct on `#F6F1E7`. Official brand SVGs (Docker blue `#2496ED`, Argo orange `#EF7B4D`, Jenkins etc.) keep official fills untouched by any filter (scoped only to dark-surface line glyphs). No hardcoded white/black fills remain.

### Map exterior — before → after

- **Before:** Flat `var(--card)` blocks with thin `3px` top line in `--cat`, `1px solid var(--line-soft)` border, `var(--shadow)` — blended into page, no depth cues beyond a subtle lift, small 40×40 icon box, pill row `3 Beg · 1 Int` only, no preview.
- **After:** Distinct objects — `1.5px solid color-mix(var(--cat) 28%, var(--line-soft))` border **visible in all 3 themes** (verified: sepia warm border on `#F6F1E7`, light neutral on white, dark bright on `#0B0D10`), tinted `linear-gradient(135deg, color-mix(var(--cat) 7%, var(--card)), var(--card))` background (category presence without overwhelming), 5px top accent + 1px top highlight (light source top-left consistent: shadow bottom-right `0 8px 24px -8px color-mix(var(--cat) 18%)`), `scale(1.015) rotateX(3deg) rotateY(-5deg) translateY(-6px)` hover with matching `shadow-lift`, `face vs side` via highlight vs shadow. Info scent per face: **large 52×52 icon** (28px glyph, `12% cat` bg), **name (18px/800)**, **count (mono + 6px cat dot)**, **difficulty bar** (proportional segments `beg:#2ECC71 int:#F5A524 adv:#E5484D` + matching dots + mono count), **pills**. Hover/focus shows **2–3 title preview popover** (`→ Title` list, `"Inside — N books"` header, `+N more`). Touch equivalent: `…` preview button (`data-preview-btn`) toggles `.preview-open` on mobile where hover doesn't exist (375px: preview is inline dashed box, stacked 1fr grid, no perspective).
- **Contrast/visual-separation check:** Verified blocks separate from bg in sepia (`#FFFBF0` card tinted with cat vs `#F6F1E7` bg + 1.5px cat border + shadow), light (`#fff` + cat border + shadow), dark (`#12151a` + cat border + shadow). Single light source top-left across all themes (highlight top, shadow bottom-right).

### Map interior — before → after

- **Before (two bugs, now fixed):** (a) Hero used a `16% cat / 6% bg2` gradient with `4px` top bar, `56×56` icon, and pill-style count — close to but NOT the same tokens as `.map-block` (which uses `7% cat` tint, `5px` bar, `52×52` chip, dot-count). (b) Book cards used the legacy `.coverart` block — a large solid `linear-gradient(135deg, var(--cat), transparent 140%)` header with oversized 28px bleeding initials (`<b>CF/CP/CI</b>`) — clashing blue block on sepia, no icon chip, `1.5px cat 14%` border (vs map's `28%`).
- **After (current — interior reuses the exact exterior card system):** Hero `.map-detail-hero` === `.map-block` tokens: `linear-gradient(135deg, color-mix(cat 7%, card), card 55%)`, `1.5px solid color-mix(cat 28%, line-soft)`, `16px` radius, `5px` top cat bar + 1px top highlight, `52×52` `.map-icon` chip (`12% cat` bg, `18% cat` border, 28px `currentColor` glyph), dot-count (`6px cat dot + mono`), same `map-difficulty` bar/dots/pills. Book cards `.map-cards .card` === same chrome at smaller scale: `3px` slim top bar (vs map's `5px`, same `var(--cat)` logic), `42×42` `.map-icon` chip (22px glyph, same `12%/18%` treatment), same gradient/border/shadow tokens, difficulty **badge** (`Beg/Int/Adv` colored `10% cat` bg, `22% cat` border), time+path mono, title 17px/700, 2-line clamped desc, **footer** with version/date meta + `Read` on `3% cat` tinted `bg2` strip. **No `.coverart`, no bleeding initials anywhere in `map.html` (0 occurrences).** Per-category `--cat` from the same `CAT_COLORS_MAP` as the exterior (CI/CD `#5B8DEF`, Jenkins `#22B8CF`, Platforms `#F97316`, Labs `#EAB308`, …) — verified distinct across 12 details. **Back transition matches entry:** `mapZoomIn .32s cubic-bezier(.2,.8,.2,1)` in, `mapZoomOut .24s` + `.exiting` class on back (history pushState + scroll to top), both disabled under `prefers-reduced-motion: reduce` (instant). Header/backdrop uses same `--cat` as exterior, so entry feels like spatial transition.
- **A11y kept:** `tabindex 0` + `aria-label` with counts, `Enter/Space` activation, `focus-visible` in `var(--cat)`, `prefers-reduced-motion` disables all transform/animation/preview transitions.
- **Themes:** all interior chrome uses theme tokens (`var(--card)/--bg2/--line-soft`) + `color-mix(var(--cat)…)` + `currentColor` icons — no hardcoded hex, no flat blue-gray panel. Correct on sepia (`#F6F1E7` bg / `#FFFBF0` card), light, and dark.

### Verification

- Rendered `map.html` + one detail (`#jenkins`) in **sepia/dark/light** (state color pairs checked above, not "looks fine").
- **375px:** blocks stack `1fr`, perspective none, preview via tap button (verified hidden until `.preview-open`, dashed cat border), cards `1fr`, hero `20px` padding — all functional without hover.
- **Blocks stand out:** as per separation check above, bold cat accent applied via `CAT_COLORS` map (`data-cat`/`--cat`) more boldly than homepage thin-border treatment.
- **Build+QC:** `python website/scripts/build.py` green, `python scripts/qc-check.py` 33 FAILs — **identical to main** (stub PDFs), zero new. `12 blocks × 42 cards` verified. Interior spot-checks: CI/CD (`--cat:#5B8DEF`), Jenkins (`#22B8CF`), Platforms (`#F97316`) — distinct per-category accents, shared card chrome, sepia/dark/light via tokens.

## Addendum — Rev 2026-09-14: Map becomes landing, paths redesigned, related enriched (feat/paths-map-landing-related)

### Route swap (option (a) from the level-up spec)
- `/` now serves the Structure Map (12 blocks, same `#slug` detail anchors) + Learning Paths section below it.
- Old shelf/grid homepage moved intact to `/shelf.html` (hero, recstrip, paths, rubric, filters, shelves); nav gains `Browse`.
- `map.html` kept as a redirect (canonical `/`, meta-refresh + `location.replace('./'+hash)` so old `#slug` links survive).
- Reader contextbar now reads `Browse › <Path> › <Book>` pointing at `shelf.html#path-<id>`; header `Map` points at `/`, plus `Browse`.
- Map detail `← Back to map` keeps its wording (it returns to the zoomed-out grid above on the same page); back transition made robust (hash cleared via pushState guarded by `if(location.hash)`, `.exiting` removed, 500ms fallback timer in case `animationend` never fires).
- Learning Paths live on BOTH `/` (under the map) and `/shelf.html` — discoverable from the landing, still with the shelves.

### Learning Paths redesign (visual data in `website/content/paths.json`, grouping derived from `books.json`)
- Accent: dominant-category rule — each path card takes `--cat`/icon from the category holding the most of its books (CI/CD `#5B8DEF` for Start Here/CI Core, Delivery `#F472B6`, Jenkins `#22B8CF`, Labs `#EAB308`, Reference `#64748B`, Roadmap `#18E299`). No neutral fallback was needed: every path has a strict majority.
- Steps: connected journey — `data-n` numbered circles (`1.5px cat` ring) joined by a `2px 32%-cat` vertical connector, difficulty as `Beg/Int/Adv` badges in the site's level colors (`#2ECC71/#F5A524/#E5484D`), step title (600wt, links to reader) primary vs mono time meta secondary, final step filled cat circle + `🏁 Finish` pill.
- Long paths (≥6 steps: delivery×7, labs×8, jenkins-advanced×7) get `.long` compact spacing (9px vs 16px gaps); short paths (start-here×2) keep airy spacing.
- Footer stats restyled to map `map-pill` chips (`N books`, `~M min`, `Level Beg→Int` span). All theme-token colors, `currentColor` icons.
- QC: `python website/scripts/build.py` + `python scripts/qc-check.py` → 33 FAILs identical to main (stub PDFs), zero new.

### Related Books (still build-time static, richer signals)
- Scoring per reader: adjacent path steps (next +12 / prev +10, same-path +4) > prereq/follow-up (+8) > same category (+3) > shared tags (+2 each); reason label rendered (`Next/Previous in path`, `Prerequisite`, `Follow-up`, `Same topic`, `Shared tags`).
- Treatment: compact `.relcard` rows reusing card tokens (`bg2`, cat left bar, 30px `currentColor` icon chip, `Beg/Int/Adv` badge, time, `→ reason`); 4 items (was 3 pills). Spot-checks: pipelines→artifacts(next)/git-branching(prereq), security→rollback(next)/envs(prev), jenkins-pipelines→jenkins-agents(next)/jenkins-setup(prev).
