# Final Verification — 2026-09-15

## Verdict: READY TO DEPLOY

Rebuild clean, `qc-check` ALL GREEN, 0 dead anchors site-wide, all 44 readers 320px-clean.
Two trivial fixes found by this gate are applied and verified below; nothing else blocks.

## Commit reality-check

- `git log` shows every claimed stream landed: lab merges (`b963f12`–`d9d0970`), audit phases,
  fullscreen/mobile (`ee7ea7b`, `36b9421`, `3660db0`, `532dbc1`), TOC toggle (`9cec393`),
  md-fallback prefs (`0c132c1`), toc-head + island (`88bd0ae`), book analysis (`436d0cf`),
  P1 (`41dbb4b`), P2 (`2466c21`), report status (`7ced329`), drawer upgrade (`8665457`),
  insertion convention (`c8774b8`), governance section (`61506f3`). No claimed work is missing.
- Premise correction: the orchestration prompt assumed "nothing deployed" — in fact the user ordered
  `deploy everything` after `8665457` (source `88bd0ae..8665457`, gh-pages `22c057f→9320710`,
  live-verified 7/7). Consequence: live currently lacks `c8774b8` (docs-only, no render impact),
  `61506f3` (governance section — real content gap vs live), and this gate's 3 fixes.
  Next deploy carries all of it; no action beyond deploying.

## Confirmed working (with evidence)

- Fullscreen: enter/exit via button + Esc, theme/font/scroll preserved (`dark 20px 3000` intact,
  `22px` after A+×2, `light` after theme switch, all survive Esc). Mobile FS via menu works;
  `100dvh` in use (`.rlayout` rule). Preference per-session, not sticky — as designed.
- Drawer: opens as fixed overlay (`0,300` settled), closes via X, toggle, Esc, backdrop tap (new
  scrim `375x812`), swipe-left; body `overflow:hidden` while open; `aria-modal` true→false;
  Tab cycles inside (25 focusables); focus returns to Contents on every close path.
  Hide/show symmetric on desktop AND mobile; hide state correctly NOT persisted across reload.
- TOC X + toggle: `toc-head` flex, no overlap (measured), hide→restore both widths.
- Overflow: all 44 readers `320,320` (3 sweep batches); roadmap timeline wrapped at ≤480px;
  glossary `320/375/768` clean; shelf/index/book/roadmap/updates/labs/404 pages clean.
- Glossary: 49 terms, stacked cards, sticky 44px filter, 14 A–Z links; shelf search dropdown opens.
- Breadcrumbs: 4 cases (prereq lab-01, no-prereq foundations, mid git-branching, last cheatsheet)
  all render 3 separate lines.
- Contrast: related cards 15.6/18.6/10.2 (AA in dark/light/sepia); reader body 16.5/19.4/11.6.
- Lab theming: body/h2/steps/code change across all 3 themes (distinct computed colors each).
- Back: top-left cluster, 44px on mobile, navigates reader→overview (earlier "no-nav" alarm was
  `read/ci.html` vs `book/ci.html` filename confusion — verified on `book/ci.html`).
- Font-size: 18→22px visible growth on lab book, persists with theme across reload.
- Checkboxes: 7 steps on jenkins-setup, persist + `done` sync across reload, theme-aware.
- Content: all P1/P2 strings present in built `dist` (migration, capacity, doubles, acceptance,
  preflight/master/ratcheting, checklist, injection, integration callouts, skeleton desc,
  ROADMAP rows, handover convention note, governance section with 10 TOC entries).
- Terminology everywhere: no `never branches` left in `.md`; CD split + trunk softening applied.
- Audit-A leftovers: First-week strip, 44 books, 45 OG PNG + 45 SVG, 9 paths, 4 merged labs,
  updates dated, merge queues/SBOM/policy-gates content intact.
- Cross-stream: all UI-pass markers coexist in final `build.py` (36-line diff, no reverts);
  new `.kv` callouts inherit theme tokens (3 distinct colors); renumbered shell books have no
  numeric section cross-refs; no deep-anchor links exist anywhere in sources.

## Regressions found (fixed in this pass)

- Glossary duplication (P2 pass created 2nd Delivery/Deployment rows; old rows pointed Deployment
  at the wrong file). Fixed: old rows deleted, one row each. — `GLOSSARY.md`
- Lab checkboxes 13px native (CSS targeted `li.step`, markup is `div.step` — sizing never applied
  since the mobile pass). Fixed: selectors widened to `.step`; hit area 44×46 via label-wrap,
  22px visual preserved; real-tap toggle + persistence verified. — `build.py`
- Step-row mono text splitting mid-word at narrow widths (`.mono{overflow-wrap:anywhere}`).
  Fixed scoped: `.step .mono{overflow-wrap:break-word}`; step 4 now breaks at word boundaries,
  page still 375-clean. — `build.py`

## Still broken / never actually fixed

- None. Every item from Sections A–C and Parts A–F verified working with direct evidence.

## Cross-stream conflicts found

- None functional. One convention tension (callout mirrors vs renumbered sections) was already
  resolved and documented in `PROJECT_HANDOVER.md` before this gate; this pass confirmed the
  evidence cited (no deep anchors, hardcoded print footers) is accurate.

## New issues found (previously unreported)

- The 3 regressions above (all fixed + verified here). No other new issues.

## Recommendation

- Commit this gate's 3 fixes (single unit), then deploy: next deploy brings live up to HEAD
  (governance section + gate fixes). No further gate needed after that deploy.
- Live-vs-HEAD delta until deploy: live lacks governance section, 44px checkbox hit areas,
  step-mono fix, and glossary dedup. All else on live matches HEAD.
