# Live UX/UI Audit

Audit date: 2026-09-14. Scope: live site HTML plus responsive/theme checks
against the generated implementation. Page matrix: landing, map redirect,
Browse, glossary, roadmap, map detail hash, Foundations reader, Jenkins reader,
Jenkins Labs reader, and decision guide reader. Themes: sepia, dark, light.
Viewports: desktop, 768px, 414px, 375px, and 320px responsive rules.

| Page | Issue | Severity | Theme / viewport | Evidence and impact |
|---|---|---|---|---|
| Landing `/` | The map is the intended landing view, but `/map.html` is a tiny redirect document rather than a content-bearing page. | cosmetic | all / all | Live `/map.html` is 447 bytes and redirects to the canonical landing route. Correct behavior, but weak when inspected or shared as a standalone document. |
| Landing / Browse | Shared header controls rely on compact wrapping rules at narrow widths rather than a unified mobile menu. | moderate | sepia/dark/light / 320-414px | Reader has a compact menu, but non-reader pages retain the generic header/search arrangement. This creates inconsistent navigation chrome across page types. |
| Map detail | Map detail is hash-addressable and uses category accents, but the redirect route and canonical route are not visually distinguishable in browser history. | cosmetic | all / all | `/map.html#jenkins` resolves to the canonical landing page. No functional break found. |
| Reader pages | Reader mobile header is now compact and the Back control is in the primary nav. | no issue | all / 375-414px | Live reader HTML includes `mobilemenubtn`, one `backbtn`, and `topbtn`; no duplicate Back or feedback widget found. |
| Reader pages | Very small 320px widths leave little room for the wordmark plus TOC/menu controls. | moderate | all / 320px | The compact toolbar is structurally safe, but the wordmark is intentionally reduced/partially hidden; a visual pass should confirm touch-target spacing on physical devices. |
| Reader pages | Back-to-top fades after idle, so its temporary visibility is not discoverable without scrolling. | cosmetic | all / all | Intentional behavior from the prior request; could use a stronger focus/hover state or tooltip if user testing finds it missed. |
| Browse/shelf | Large shelf document is dense and long, especially on mobile. | moderate | all / 320-414px | Live shelf is about 258 KB before transfer compression and contains many repeated cards/rails; scanning requires repeated horizontal/vertical movement. |
| Glossary | Table is content-dense on narrow screens and depends on horizontal overflow behavior. | moderate | all / 320-414px | Existing mobile rule makes the table scrollable, but column context can be lost while scanning. |
| Roadmap | Timeline/cards use multiple density levels and can feel visually heavier than the map/path system. | cosmetic | sepia/light / 768px+ | No broken interaction found; consistency review recommended. |
| All pages | Google Fonts are imported from CSS and can delay the final typography when network access is slow. | moderate | all / first load | `@import` is render-path CSS; system fallback exists, but perceived layout can shift after font load. |

No critical live interaction failure was found in this pass. The most important
consistency issue is that the reader now has a dedicated compact mobile chrome
while the other page families still use the older generic header behavior.

