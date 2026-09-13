# CI/CD TECHNICAL BOOKS WEBSITE

## Design, Architecture, Content Integration & Reading Experience Specification

---

# 1. ROLE

You are a senior frontend architect, UI/UX designer, and documentation-platform engineer.

Your task is to build a **premium technical documentation and digital-book website** for a structured CI/CD knowledge base.

The website will contain technical books generated from Markdown and HTML/PDF documents.

The website must not behave like a simple documentation folder viewer.

It should feel like a:

> **Modern technical library + interactive documentation platform + digital reading application.**

The system must be designed so that new books, chapters, topics, diagrams, labs, and tools can be added later without restructuring the application.

---

# 2. PRIMARY OBJECTIVES

The website must allow users to:

* Browse all available technical books
* Open and read books directly in the browser
* Navigate chapters and sections
* Search across books
* Search inside the currently opened book
* Change font size
* Change reading width
* Change theme
* Switch between two visual themes
* Preserve reading preferences
* Continue reading from the previous position
* Navigate using a table of contents
* Jump between chapters
* View diagrams
* View code examples
* Copy code
* View labs and practical exercises
* View technical references
* Download the original PDF
* Access the original HTML when appropriate
* Open related books/topics
* Share/bookmark specific content where practical
* Use the website comfortably on desktop, tablet, and mobile

The experience must prioritize **reading and learning**, not visual effects.

---

# 3. CORE ARCHITECTURE

The application must separate:

```text
CONTENT
    ↓
CONTENT PROCESSING
    ↓
CONTENT MODEL
    ↓
UI COMPONENTS
    ↓
READING EXPERIENCE
```

Do NOT hardcode individual books directly into page components.

Use a content-driven architecture.

Recommended structure:

```text
website/
├── public/
│   ├── books/
│   │   ├── ci-cd-foundations/
│   │   ├── jenkins/
│   │   └── ...
│   │
│   ├── assets/
│   │   ├── icons/
│   │   ├── diagrams/
│   │   └── images/
│   │
│   └── favicon/
│
├── src/
│   ├── components/
│   │   ├── layout/
│   │   ├── navigation/
│   │   ├── books/
│   │   ├── reader/
│   │   ├── chapters/
│   │   ├── code/
│   │   ├── diagrams/
│   │   ├── search/
│   │   ├── settings/
│   │   └── common/
│   │
│   ├── content/
│   │   ├── books/
│   │   ├── chapters/
│   │   └── index/
│   │
│   ├── data/
│   │   ├── books.json
│   │   ├── topics.json
│   │   └── navigation.json
│   │
│   ├── pages/
│   ├── routes/
│   ├── services/
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   │   ├── themes/
│   │   ├── tokens/
│   │   └── global.css
│   └── app/
│
└── README.md
```

Adapt the structure to the selected framework, but preserve the architectural separation.

---

# 4. CONTENT MUST BE DATA-DRIVEN

A book should be represented as structured metadata.

Example:

```json
{
  "id": "ci-cd-foundations",
  "title": "CI/CD Foundations",
  "description": "Understanding modern continuous integration and delivery.",
  "category": "CI/CD",
  "difficulty": "Beginner",
  "version": "1.0",
  "cover": "/books/ci-cd-foundations/cover.webp",
  "content": "/books/ci-cd-foundations/book.html",
  "pdf": "/books/ci-cd-foundations/book.pdf",
  "chapters": [
    {
      "id": "introduction",
      "title": "Introduction",
      "href": "#introduction"
    },
    {
      "id": "continuous-integration",
      "title": "Continuous Integration",
      "href": "#continuous-integration"
    }
  ]
}
```

Do not create a unique page component for every book.

Use one reusable book-reader architecture.

---

# 5. HTML/PDF CONTENT INTEGRATION

The existing technical books may exist as:

```text
Markdown
HTML
PDF
SVG
Images
Diagrams
Code examples
```

The website must support these assets as part of the same content ecosystem.

Preferred content pipeline:

```text
Markdown
   ↓
Structured HTML
   ↓
PDF
   ↓
Website Reader
```

The Markdown remains the canonical knowledge source whenever available.

The generated HTML is the primary browser-renderable representation.

The PDF is the downloadable/printable representation.

Do NOT treat the PDF as the only source of truth if structured Markdown or HTML exists.

---

# 6. IMPORTING EXISTING HTML BOOKS

When adding an existing HTML book:

1. Inspect its structure.
2. Identify:

   * Title
   * Chapters
   * Sections
   * Headings
   * Images
   * SVGs
   * Diagrams
   * Code blocks
   * Tables
   * Links
3. Preserve the technical content.
4. Extract or map the content into the website's reader structure.
5. Remove unnecessary standalone HTML document chrome.
6. Do not duplicate the website's global navigation inside the imported book.
7. Preserve semantic HTML.
8. Generate a table of contents from headings where possible.
9. Ensure internal links work.
10. Ensure local assets resolve correctly.

Do not simply display an entire PDF screenshot as the reading experience.

---

# 7. PDF SUPPORT

Every book should have a visible:

```text
Read Online
Download PDF
```

actions.

The PDF should remain available as the authoritative printable artifact.

Where technically appropriate, also provide:

```text
Open PDF
Print
Download
```

Do not force users to read PDFs inside a tiny embedded viewer.

The primary experience should be the responsive web reader.

---

# 8. BOOK LIBRARY

Create a dedicated library page.

Example:

```text
┌─────────────────────────────────────────────┐
│ Technical Library                           │
│                                             │
│ Search books...                             │
│                                             │
│ [All] [CI/CD] [Jenkins] [Cloud] [DevOps]   │
│                                             │
│ ┌─────────────────┐ ┌─────────────────┐     │
│ │ Book Cover      │ │ Book Cover      │     │
│ │                 │ │                 │     │
│ │ CI/CD           │ │ Jenkins         │     │
│ │ Foundations     │ │ Deep Dive       │     │
│ │                 │ │                 │     │
│ │ Beginner        │ │ Intermediate    │     │
│ │ [Read]          │ │ [Read]          │     │
│ └─────────────────┘ └─────────────────┘     │
└─────────────────────────────────────────────┘
```

Each book card should provide:

* Cover
* Title
* Description
* Category
* Difficulty
* Estimated reading time when available
* Chapter count
* Progress if the user has started reading
* Read button

---

# 9. BOOK DETAILS PAGE

Each book should have a dedicated landing page.

Include:

```text
Book Cover

Title

Description

Difficulty
Category
Estimated reading time

[Start Reading]
[Continue Reading]
[Download PDF]

Table of Contents

About This Book

Prerequisites

Related Books

Related Topics
```

Do not overwhelm the page with unnecessary metadata.

---

# 10. DIGITAL READER

The reader is the most important part of the application.

It should contain:

```text
┌───────────────────────────────────────────────────────┐
│ Logo     Book Title                    Search  ⚙      │
├──────────────┬────────────────────────────────────────┤
│              │                                        │
│ TABLE OF     │            CONTENT                     │
│ CONTENTS     │                                        │
│              │                                        │
│ Introduction │       Chapter Heading                 │
│              │                                        │
│ CI           │       Paragraph...                    │
│              │                                        │
│ Pipelines    │       Diagram                          │
│              │                                        │
│ Jenkins      │       Code                             │
│              │                                        │
│ Deployment   │       Explanation                     │
│              │                                        │
├──────────────┴────────────────────────────────────────┤
│ Previous Chapter                    Next Chapter       │
└───────────────────────────────────────────────────────┘
```

---

# 11. READER LAYOUT

Use a three-zone architecture where appropriate:

```text
LEFT
Navigation / TOC

CENTER
Reading content

RIGHT
Context / tools / page controls
```

However, do not force all three columns on small screens.

Desktop:

```text
TOC | READER | TOOLS
```

Tablet:

```text
TOC | READER
```

Mobile:

```text
READER
+
TOC drawer
+
Settings drawer
```

---

# 12. READING WIDTH

Provide adjustable reading width.

Recommended options:

```text
Narrow
Comfortable
Wide
```

Default:

```text
Comfortable
```

Do not allow unlimited width.

Long technical paragraphs become unpleasant when stretched across the entire monitor.

---

# 13. FONT SIZE CUSTOMIZATION

The user must be able to change reading font size.

Provide:

```text
A−
A
A+
```

or:

```text
Small
Medium
Large
Extra Large
```

Recommended default:

```text
18px approximately
```

for browser reading, adjusted based on the chosen font.

The font-size preference should affect:

* Paragraphs
* Lists
* Notes
* Tables where appropriate
* Code text where appropriate

Headings should scale proportionally.

Do not scale UI navigation controls with the reading font.

---

# 14. LINE HEIGHT

Provide comfortable line spacing.

Default:

```text
1.6–1.8
```

The reader must never feel compressed.

Technical documentation benefits from breathing room.

---

# 15. TWO THEMES

Implement exactly two primary reading themes initially.

## THEME 1: ORIGINAL

The primary design should preserve the original technical-book identity.

Characteristics:

```text
Technical
Premium
Dark / deep engineering aesthetic
Strong contrast
Controlled accent colors
Modern
Editorial
```

Use the established visual identity of the PDF series.

The website should feel like the digital continuation of the books.

---

## THEME 2: LIGHT READING

Provide a dedicated light theme optimized for long reading sessions.

Characteristics:

```text
Warm/off-white background
Dark text
Soft borders
Subtle shadows
Low visual noise
Comfortable contrast
```

Avoid pure:

```text
#FFFFFF
```

for the entire reading surface when a softer background improves readability.

---

# 16. THEME SYSTEM

Do not implement themes by rewriting individual components.

Use design tokens.

Example:

```css
:root {
    --bg-primary: ...;
    --bg-secondary: ...;
    --text-primary: ...;
    --text-secondary: ...;
    --border: ...;
    --accent: ...;
    --code-bg: ...;
}
```

Then:

```css
[data-theme="original"] {
    ...
}

[data-theme="light"] {
    ...
}
```

Components should consume tokens instead of hardcoded colors.

This makes future themes possible without architectural changes.

---

# 17. THEME APPLICATION

Theme changes must affect the entire reading experience:

* Background
* Text
* Headings
* Links
* Cards
* Code blocks
* Tables
* Diagrams where appropriate
* Borders
* Navigation
* Reader controls

Do not leave half the application in the previous theme.

---

# 18. USER READING PREFERENCES

Persist reading preferences locally.

Store:

```text
Theme
Font size
Reading width
Line height if configurable
Last opened book
Last reading position
TOC state
```

Use appropriate browser storage.

The user should be able to close the browser and return without losing their reading configuration.

---

# 19. READING PROGRESS

Track reading progress locally.

Example:

```text
Jenkins
████████████░░░░ 72%
```

Store progress per:

```text
Book
Chapter
```

Do not require account authentication for basic progress tracking.

Anonymous/local progress should work.

---

# 20. CONTINUE READING

If the user previously opened a book:

```text
Continue Reading
```

should return them to the last meaningful reading position.

Example:

```text
Jenkins Deep Dive
Chapter 5 · Jenkins Agents

[Continue Reading]
```

Do not always send users back to the beginning.

---

# 21. TABLE OF CONTENTS

Generate a dynamic TOC from document headings.

Support:

```text
Chapter
  Section
    Subsection
```

The current section should be visually highlighted.

As the user scrolls, the TOC should update to show their current location.

Do not highlight every heading simultaneously.

---

# 22. MOBILE TOC

On mobile, the TOC becomes a drawer/sheet.

Example:

```text
☰ Contents
```

Opening it displays the chapter hierarchy.

After selecting a section, close the drawer automatically where appropriate.

---

# 23. READER SETTINGS PANEL

Create a clean settings panel.

Example:

```text
READING SETTINGS

Theme
[ Original ] [ Light ]

Text Size
A−   A   A+

Reading Width
[ Narrow ] [ Comfortable ] [ Wide ]

Line Spacing
[ Comfortable ]

Reset
```

Settings must update immediately.

Do not require page reloads.

---

# 24. SEARCH

Implement global search.

Search should cover:

* Book titles
* Chapters
* Sections
* Concepts
* Glossary terms
* Technical tools
* Jenkins
* CI/CD topics

Search results should show:

```text
Title
Book
Section
Short context
```

Example:

```text
Jenkins Agents
Jenkins Deep Dive
Chapter 4

"...Jenkins agents execute pipeline workloads..."
```

Clicking a result should open the exact relevant location.

---

# 25. IN-BOOK SEARCH

The reader must support searching inside the current book.

Provide:

```text
Ctrl + K
```

or another sensible shortcut for search.

Search results should allow jumping directly to matches.

Highlight the matching text where technically practical.

---

# 26. KEYBOARD NAVIGATION

Support useful shortcuts.

Examples:

```text
Ctrl/Cmd + K
Search

Esc
Close panel

←
Previous chapter

→
Next chapter

T
Toggle TOC

F
Focus search where appropriate
```

Do not introduce shortcuts that conflict with standard browser behavior.

Document available shortcuts in the settings/help interface.

---

# 27. CODE BLOCKS

Code is a first-class part of technical documentation.

Every code block should provide:

```text
Language label
Copy button
Syntax highlighting
Readable font
```

Example:

```text
┌────────────────────────────────────────────┐
│ Jenkinsfile                         Copy   │
├────────────────────────────────────────────┤
│ pipeline {                                 │
│     agent any                              │
│     stages {                               │
│         ...                                │
│     }                                      │
│ }                                          │
└────────────────────────────────────────────┘
```

Copy must copy only the code.

---

# 28. DIAGRAMS

Diagrams should remain readable and responsive.

Support:

* SVG
* Mermaid where appropriate
* Images
* Architecture diagrams
* Pipeline diagrams
* Flow diagrams

Clicking a complex diagram may open a larger viewing mode.

Do not destroy diagram readability by forcing every image into a tiny fixed container.

---

# 29. IMAGES AND ICONS

Use the centralized asset system.

```text
assets/
└── icons/
```

Do not use:

* Emoji as technical icons
* Random icon sources
* Broken external image URLs
* Unlicensed assets

Prefer local SVG assets.

The same icon system should be shared between:

```text
PDF
Website
Book cards
Reader
Diagrams
```

where appropriate.

---

# 30. TECHNICAL BRANDING

Technology logos such as:

```text
Jenkins
Git
GitHub
Docker
Kubernetes
AWS
Terraform
Prometheus
Grafana
```

should use legitimate, appropriately licensed assets.

Do not create fake logos.

Do not distort official logos.

---

# 31. LAB EXPERIENCE

Labs should receive special visual treatment.

Each lab should expose:

```text
Objective
Prerequisites
Architecture
Environment
Steps
Commands
Expected Output
What Happened Internally
Verification
Troubleshooting
Cleanup
What This Proved
```

Provide:

```text
Copy Command
```

for commands.

Make expected results visually distinguishable from commands.

---

# 32. COMMAND TERMINAL DESIGN

Technical commands should use a terminal-style component.

Example:

```text
┌─────────────────────────────────────────────┐
│ Terminal                              Copy  │
├─────────────────────────────────────────────┤
│ $ kubectl get pods                          │
│                                             │
│ NAME             READY   STATUS              │
│ nginx-7d...      1/1     Running             │
└─────────────────────────────────────────────┘
```

Commands must remain selectable and copyable.

---

# 33. RELATED CONTENT

At the end of a chapter provide useful navigation:

```text
Previous
Next

Related Topics
Related Chapters
Related Books
```

Example:

```text
Related Topics

→ Continuous Integration
→ Build Systems
→ Jenkins Pipelines
→ Deployment Strategies
```

These relationships should come from the knowledge-base metadata whenever possible.

---

# 34. BOOK NAVIGATION

Support:

```text
Previous Chapter
Next Chapter
Chapter selector
TOC navigation
Breadcrumbs
```

Example:

```text
CI/CD Library
  /
Jenkins
  /
Jenkins Pipelines
```

Navigation should make the user's location obvious.

---

# 35. HEADER

The global header should contain:

```text
Logo / Library
Books
Topics
Search
Theme
Reader Settings
```

Do not overload the header.

The reader header may be simplified to prioritize the book.

---

# 36. SIDEBAR

Desktop sidebar should provide:

```text
Book Contents
```

Optionally:

```text
Book Progress
```

The sidebar should remain usable for large books.

If the TOC is long:

* Make it independently scrollable
* Keep current section visible
* Do not allow it to consume the entire screen

---

# 37. FOOTER

The global footer should contain:

```text
About
Documentation
Repository / Source
Version
Last Updated
License
```

Only display information that actually exists.

Do not invent metadata.

---

# 38. ACCESSIBILITY

Accessibility is mandatory.

Support:

* Keyboard navigation
* Visible focus states
* Semantic headings
* Semantic buttons
* Accessible labels
* Sufficient contrast
* Screen-reader-friendly navigation
* Reduced motion preference
* Proper alt text
* No color-only meaning

The site should remain usable without a mouse.

---

# 39. RESPONSIVE DESIGN

Desktop:

```text
Full reader
Persistent TOC
Full navigation
```

Tablet:

```text
Reduced sidebar
Comfortable reading width
Collapsible navigation
```

Mobile:

```text
Single-column reader
Drawer TOC
Compact header
Bottom/inline navigation
Responsive tables
Responsive diagrams
```

Never simply shrink the desktop layout onto mobile.

---

# 40. PERFORMANCE

Optimize for fast reading.

Avoid unnecessary:

* Large JavaScript bundles
* Huge background images
* Repeated assets
* External requests
* Blocking scripts
* Heavy animation

Prefer:

```text
Static content
Lazy-loaded images
Local assets
Code splitting where appropriate
Caching
Optimized SVG
```

Books should load quickly even when they contain many chapters.

---

# 41. OFFLINE-FRIENDLY DESIGN

Where practical, architect the application so content can eventually support offline reading.

The system should not depend on a remote API for every paragraph.

Static technical content should remain accessible even if external services are unavailable.

---

# 42. VERSIONING

Books may evolve.

Support metadata such as:

```text
Version
Published
Last Updated
Status
```

Example:

```text
Version 1.2
Updated September 2026
```

Do not silently overwrite version information if the content system later requires historical versions.

---

# 43. BOOK COVER DESIGN

Every major book should have a consistent cover system.

Cover should communicate:

```text
Book title
Topic
Category
Difficulty
Series identity
```

For example:

```text
┌────────────────────────────┐
│                            │
│ CI/CD                      │
│                            │
│ FOUNDATIONS                │
│                            │
│ Source → Build → Test      │
│ → Artifact → Deploy        │
│                            │
│ TECHNICAL BOOK             │
└────────────────────────────┘
```

Use the same visual language across the entire series.

---

# 44. VISUAL DESIGN LANGUAGE

The website should feel:

```text
Technical
Editorial
Premium
Modern
Focused
Structured
Engineering-oriented
```

Avoid:

```text
Generic SaaS dashboard
Excessive gradients
Excessive glassmorphism
Random rounded cards
Huge animated hero sections
Overly colorful UI
Excessive shadows
Unnecessary animations
```

This is a technical library, not a startup landing page desperately trying to explain why its button is revolutionary.

---

# 45. TYPOGRAPHY

Use a strong technical/editorial typography system.

Recommended structure:

```text
Display
→ Book titles

Heading
→ Chapters

Subheading
→ Sections

Body
→ Reading content

Monospace
→ Code / commands
```

Body text must prioritize readability.

Recommended browser reading baseline:

```text
16px–20px
```

Default around:

```text
18px
```

Adjust based on viewport and selected font.

Use generous line-height.

---

# 46. SPACING SYSTEM

Use a consistent spacing scale.

Example:

```text
4
8
12
16
24
32
48
64
```

Do not invent random values throughout components.

Create spacing tokens.

---

# 47. COMPONENT SYSTEM

Build reusable components such as:

```text
BookCard
BookGrid
BookHero
ChapterHeader
TableOfContents
ReaderLayout
ReaderSettings
ThemeSwitcher
FontSizeControl
CodeBlock
TerminalBlock
DiagramViewer
Callout
Warning
Tip
InfoCard
ComparisonTable
LabStep
Breadcrumbs
ChapterNavigation
SearchDialog
ProgressIndicator
```

Do not duplicate component implementations for different books.

---

# 48. CONTENT COMPONENTS

The content renderer should recognize semantic structures.

For example:

```text
Heading
Paragraph
List
Code
Terminal
Table
Diagram
Callout
Warning
Tip
Lab
Quiz
Glossary
Reference
```

Render each appropriately.

Do not flatten everything into generic paragraphs.

---

# 49. SPECIAL CALLOUTS

Support semantic callouts:

```text
NOTE
TIP
WARNING
IMPORTANT
EXAMPLE
BEST PRACTICE
COMMON MISTAKE
```

Example:

```text
┌────────────────────────────────────┐
│ IMPORTANT                          │
│                                    │
│ Jenkins agents execute workloads. │
└────────────────────────────────────┘
```

Use icons from the managed icon system.

Do not use emoji.

---

# 50. GLOSSARY

Provide a global glossary.

Example:

```text
Artifact
Agent
Build
Deployment
Pipeline
Runner
Registry
Release
Stage
Webhook
```

Each term should link to its explanation.

Glossary terms may be searchable.

---

# 51. TOPIC EXPLORER

Provide a topic-oriented view in addition to books.

Example:

```text
CI/CD
├── Continuous Integration
├── Pipelines
├── Build
├── Testing
├── Artifacts
├── Deployment
├── Security
└── Observability

Jenkins
├── Architecture
├── Pipeline
├── Agents
├── Plugins
├── Credentials
└── Webhooks
```

This allows users to learn by concept rather than only by book.

---

# 52. CROSS-BOOK RELATIONSHIPS

A concept can appear in multiple books.

The website should support relationships such as:

```text
Git
 ↓
CI
 ↓
Jenkins
 ↓
Docker
 ↓
Deployment
 ↓
Kubernetes
```

Do not duplicate the same content merely to create navigation.

Link to the canonical topic.

---

# 53. URL ARCHITECTURE

Use clean, stable routes.

Example:

```text
/
 /books
 /books/ci-cd-foundations
 /books/ci-cd-foundations/continuous-integration
 /books/jenkins
 /books/jenkins/pipelines
 /topics
 /topics/continuous-integration
 /topics/jenkins
 /glossary
 /search
 /about
```

URLs should be:

* Human-readable
* Stable
* Predictable
* SEO-friendly
* Independent of implementation details

Do not use meaningless IDs in public URLs when slugs are available.

---

# 54. SEO

Each book/chapter should have appropriate:

```text
Title
Description
Canonical URL
Open Graph metadata
```

Use semantic HTML.

Technical content should be indexable where appropriate.

Do not sacrifice application performance for unnecessary SEO machinery.

---

# 55. PRINT SUPPORT

The website should support printing the reader content cleanly.

Create a dedicated print stylesheet.

When printing:

```text
Hide navigation
Hide settings
Hide interactive controls
Preserve headings
Preserve code
Preserve diagrams
Preserve tables
Use readable typography
```

The printed result should resemble a clean technical document.

---

# 56. PDF / HTML CONSISTENCY

The website and PDF should share:

```text
Terminology
Icons
Visual identity
Chapter naming
Book metadata
Content hierarchy
```

But do not force the web layout to imitate the A4 PDF exactly.

PDF:

```text
Fixed page
Print-oriented
Pagination-aware
```

Website:

```text
Responsive
Scrollable
Interactive
Customizable
```

They share the content and design language, not necessarily the exact layout.

---

# 57. READING EXPERIENCE PRIORITY

When making design decisions, use this priority:

```text
1. Readability
2. Navigation
3. Content comprehension
4. Accessibility
5. Performance
6. Visual polish
7. Animation
```

Never sacrifice readability for visual effects.

---

# 58. ANIMATION

Use subtle animation only when it improves usability.

Allowed:

```text
Drawer transitions
Theme transition
Search opening
Hover states
Progress updates
```

Avoid:

```text
Constant floating elements
Large entrance animations
Parallax
Scrolling gimmicks
Animated backgrounds
```

Respect:

```text
prefers-reduced-motion
```

---

# 59. STATE MANAGEMENT

Keep application state organized.

Separate:

```text
Content state
UI state
Reading preferences
Reading progress
Search state
Navigation state
```

Do not place everything into one global state object.

---

# 60. FUTURE BACKEND COMPATIBILITY

The initial system may use static/local content.

However, architecture should allow future migration to:

```text
Static files
        ↓
Content API
        ↓
Database
```

without rewriting the entire reader.

Possible future capabilities:

```text
User accounts
Cloud reading progress
Bookmarks
Notes
Highlights
Comments
Analytics
Recommendations
```

Do not implement these prematurely.

Design extension points without overengineering.

---

# 61. BOOKMARKS

If practical, support local bookmarks.

Users should be able to bookmark a section or reading location.

Example:

```text
🔖 Jenkins Agents
Chapter 4
```

Store locally initially.

Do not require authentication.

---

# 62. NOTES AND HIGHLIGHTS

Architect the reader so future support for:

```text
Highlights
Personal notes
Annotations
```

is possible.

Do not implement a complex backend unless required.

The current system can expose clean extension points.

---

# 63. ERROR HANDLING

If a book cannot load:

Display:

```text
Unable to load this book.

The content may be missing or unavailable.

[Retry]
[Back to Library]
```

Do not show raw stack traces to users.

For missing assets:

* Log the problem
* Show a graceful fallback
* Never leave broken image icons throughout the page

---

# 64. CONTENT VALIDATION

Before publishing a book, validate:

```text
[ ] Book metadata exists
[ ] Cover exists
[ ] HTML exists
[ ] PDF exists
[ ] Chapters resolve
[ ] TOC links work
[ ] Images load
[ ] SVGs load
[ ] Code blocks render
[ ] Internal links work
[ ] External links work
[ ] No broken assets
[ ] No duplicate IDs
[ ] No missing headings
```

---

# 65. DESIGN VALIDATION

Check every major screen:

```text
Library
Book Details
Reader
Search
Topics
Glossary
Settings
Mobile Reader
```

Verify:

```text
[ ] Original theme
[ ] Light theme
[ ] Font size controls
[ ] Reading width
[ ] Responsive layout
[ ] Keyboard navigation
[ ] Accessibility
[ ] Code copying
[ ] TOC navigation
[ ] Progress tracking
```

---

# 66. NO CONTENT LOSS

When importing existing books:

> Never modify, simplify, summarize, or remove technical content merely to make the website easier to implement.

Preserve:

* Explanations
* Commands
* Code
* Tables
* Diagrams
* Examples
* Labs
* Warnings
* References

The website is a reader for the knowledge base, not a rewriting engine.

---

# 67. ARCHITECTURE FOR FUTURE BOOKS

Adding a new book should require approximately:

```text
1. Add book metadata
2. Add HTML/content
3. Add PDF
4. Add assets
5. Add chapter metadata if needed
6. Register the book
```

It should NOT require:

```text
Creating a new React/Vue component
Creating a new page layout
Duplicating navigation
Writing new reader logic
Creating custom CSS
```

If adding a book requires modifying many unrelated files, the architecture is wrong.

---

# 68. AUTOMATIC BOOK DISCOVERY

Where practical, design the system so books can eventually be discovered from a content manifest.

Example:

```text
/books/
    ci-cd-foundations/
    jenkins/
    docker/
    kubernetes/
```

The application should read metadata rather than relying on manually duplicated routes.

---

# 69. CONTENT MANIFEST

Maintain a central manifest:

```text
content/
└── books.json
```

Example:

```json
[
  {
    "id": "ci-cd-foundations",
    "title": "CI/CD Foundations",
    "slug": "ci-cd-foundations",
    "category": "CI/CD",
    "status": "published"
  },
  {
    "id": "jenkins",
    "title": "Jenkins",
    "slug": "jenkins",
    "category": "CI/CD Tools",
    "status": "published"
  }
]
```

This becomes the central registry for the library.

---

# 70. ORIGINAL THEME + LIGHT THEME RULE

The original theme is the **identity theme**.

The light theme is the **reading comfort theme**.

Do not make them two completely unrelated designs.

They must share:

```text
Typography
Layout
Spacing
Component structure
Iconography
Brand identity
```

Only visual tokens change.

The user should immediately recognize that both themes belong to the same technical library.

---

# 71. USER EXPERIENCE FLOW

The intended journey:

```text
HOME
  ↓
LIBRARY
  ↓
BOOK
  ↓
BOOK DETAILS
  ↓
START READING
  ↓
READER
  ↓
CHAPTER
  ↓
SECTION
  ↓
NEXT CHAPTER
  ↓
CONTINUE READING
```

Alternative:

```text
SEARCH
  ↓
TOPIC
  ↓
BOOK / CHAPTER
  ↓
EXACT SECTION
```

Both flows must feel natural.

---

# 72. PLATFORM ROADMAPS & DECISION GUIDE

This section defines **platform roadmaps** as a first-class content type for forward-looking, decision-oriented books. It integrates the three canonical research documents — **Jenkins Platform Roadmap 2026**, **GitHub Actions 2026 Security Roadmap**, and **Combined Decision Framework (Jenkins vs. GitHub Actions)** — as the authoritative source for all roadmap content on the website. No roadmap content may be invented, summarized from memory, or sourced from secondary blogs; all claims must be traceable to these three research docs and verified against official sources (jenkins.io, jenkins-infra changelogs/roadmap, docs.github.com, GitHub Blog/Changelog, GitHub Docs REST/GraphQL release notes, and linked advisories/CVEs).

## 72.1 Purpose & Scope

Platform roadmaps are not feature wishlists. They answer:

```text
What is coming?
When is it expected?
What should teams adopt, postpone, or avoid?
Which platform fits which context?
How to migrate or run both?
```

Roadmap books cover:

* **Jenkins 2026** — controller/agent, remoting, JCasC, plugin ecosystem, security hardening, cloud-native agents, performance.
* **GitHub Actions 2026 (Security Roadmap)** — runner security, OIDC, attestation, secrets, enterprise controls, supply-chain hardening.
* **Decision Guide** — human-readable synthesis: when to choose Jenkins, when to choose Actions, when to run both (coexistence/migration).

All roadmap content lives under `/roadmap/` (see §72.6 URL Scheme) and is presented both as readable books (reader experience) and as structured decision tools (comparison, timeline, decision tree).

## 72.2 Content Model for Roadmap Books

Roadmap books extend — but do not replace — the standard book model defined in §4. They are data-driven entries in `content/books.json` with additional fields:

```json
{
  "id": "roadmap-jenkins-2026",
  "slug": "roadmap-jenkins-2026",
  "title": "Jenkins Platform Roadmap 2026",
  "kind": "roadmap",
  "platform": "jenkins",
  "description": "Forward-looking roadmap for Jenkins core, agents, plugins, and security — Q1 2026 → Q1 2027 horizon.",
  "category": "Platform Roadmap",
  "difficulty": "Intermediate",
  "version": "1.0",
  "status": "published",
  "cover": "/books/roadmap-jenkins-2026/cover.webp",
  "content": "/books/roadmap-jenkins-2026/book.html",
  "pdf": "/books/roadmap-jenkins-2026/book.pdf",
  "sourceDocs": [
    "research/jenkins-2026-roadmap.md",
    "research/github-actions-2026-security-roadmap.md",
    "research/combined-decision-framework.md"
  ],
  "freshness": {
    "lastVerified": "2026-09-01",
    "verifyCadence": "quarterly",
    "officialSources": [
      "https://www.jenkins.io/changelog/",
      "https://www.jenkins.io/doc/book/",
      "https://docs.github.com/en/actions",
      "https://github.blog/changelog/"
    ]
  },
  "roadmapMeta": {
    "horizon": "2026-Q1 → 2027-Q1",
    "buckets": ["Now", "Next", "Later"],
    "decisionRelevant": true
  },
  "chapters": [
    { "id": "executive-summary", "title": "Executive Summary", "href": "#executive-summary" },
    { "id": "timeline", "title": "Timeline", "href": "#timeline" },
    { "id": "comparison", "title": "Comparison", "href": "#comparison" },
    { "id": "decision-tree", "title": "Decision Tree", "href": "#decision-tree" },
    { "id": "sources", "title": "Sources & Freshness", "href": "#sources" }
  ],
  "relatedBooks": ["jenkins-architecture", "jenkins-security", "github-actions"],
  "relatedTopics": ["Platform Choice", "CI/CD Security", "Migration"]
}
```

Required sibling entries:

```text
roadmap-jenkins-2026       → platform: jenkins
roadmap-github-actions-2026 → platform: github-actions
roadmap-decision-guide      → platform: both  (synthesis)
```

Rules:

* `kind: "roadmap"` distinguishes roadmaps from standard books; the renderer and library must handle both.
* `sourceDocs` MUST list all three canonical research docs. Only these three are canonical for roadmap content; additional docs may be cited as supplementary verification but never as the primary source.
* `officialSources` + `lastVerified` + `verifyCadence` are mandatory (see §72.5).
* `roadmapMeta.buckets` governs timeline rendering.
* Adding a new platform roadmap (e.g., GitLab 2027) requires only a new entry + HTML/PDF + assets — no new component (cf. §67).

Storage layout mirrors existing books:

```text
public/books/roadmap-jenkins-2026/
  book.html
  book.pdf
  cover.webp
  data/timeline.json      // optional structured timeline source
  data/comparison.json    // optional structured comparison source
```

## 72.3 Comparison View — Side-by-Side Table (Jenkins vs. GitHub Actions)

Every roadmap book that evaluates platforms MUST render a shared **ComparisonTable** component. The decision-guide book is the primary host; the Jenkins and Actions roadmap books embed a scoped variant.

### Component: `ComparisonTable`

```text
Props:
  title: string                      // "Jenkins vs. GitHub Actions — 2026 Lens"
  caption: string                    // "Synthesized from the three canonical research docs; see Sources."
  rows: ComparisonRow[]
  footnote: string                   // "Verify against official sources before planning (§72.5)."
  sourceRef: "canonical-three"

ComparisonRow:
  dimension: string                  // e.g. "Runner & Executor Model"
  jenkins: Cell                      // { text, status: "Now"|"Next"|"Later"|"Caution", icon }
  actions: Cell
  verdict: "Jenkins" | "Actions" | "Contextual" | "Both"
  evidenceIds: string[]              // anchors into Sources section
```

Canonical dimensions (rows) — minimum set derived from the three research docs; do not omit without explicit source justification:

```text
Runner & Executor Model
Scalability & Cost Model
Security Posture (2026 delta)
Secrets & OIDC
Supply-Chain & Attestation
Pipeline Authoring (Declarative vs. YAML)
Plugin / Action Ecosystem
Observability & Audit
Governance / Enterprise Controls
Migration & Coexistence
```

Rendering rules:

* Desktop: true side-by-side table with sticky header, `Jenkins | Dimension | GitHub Actions` and a `Verdict` chip. Responsive fallback per §86: horizontal scroll with sticky first column; do not collapse into cards on tablet — keep table semantics.
* Mobile: stacked cards per row with dimension as card header, Jenkins/Actions as labeled sections, verdict as badge.
* Each cell shows a compact `status` badge (Now/Next/Later/Caution) sourced from `roadmapMeta.buckets`; colors come from design tokens, not hardcoded.
* Verdict values: `Jenkins` / `Actions` / `Contextual` / `Both` — never a numeric score.
* Every row exposes `evidenceIds` that deep-link to §72.5 Sources entries. Clicking a cell scrolls to and highlights the source.
* Accessibility: `<table>` with `<caption>`, `scope="col"`/`scope="row"`, and `aria-describedby` pointing to the footnote. Never use div-only tables.
* Reuse existing `ComparisonTable` from §47; extend props if needed — do not duplicate the component.

Verification requirement: The footnote and caption MUST state that the table is synthesized from the three canonical research docs and that official sources must be checked before acting. No cell may claim a ship date or SLA without an official source anchor.

## 72.4 Timeline Visualization

Roadmap books MUST render a **Timeline** component that visualizes Now / Next / Later horizons plus explicit dates when official sources provide them.

### Component: `RoadmapTimeline`

```text
Props:
  horizon: string                    // "2026-Q1 → 2027-Q1"
  lanes: Lane[]                      // one per platform or shared
  buckets: ["Now", "Next", "Later"]
  items: TimelineItem[]

Lane: { id: "jenkins" | "github-actions" | "shared", label: string }
TimelineItem:
  id: string
  lane: Lane["id"]
  title: string
  bucket: "Now" | "Next" | "Later"
  window: string                     // e.g. "2026-Q3" or "H2 2026"
  confidence: "Committed" | "Planned" | "Exploratory"
  description: string                // ≤ 280 chars in timeline; full text in reader
  anchors: string[]                  // heading IDs in book HTML
  evidenceIds: string[]              // links to Sources
  relatedBooks: string[]             // deep-links into library
```

Visual spec:

```text
Desktop: horizontal swimlanes (Jenkins · GitHub Actions · Shared) with bucket zones as background bands.
         Now | Next | Later as vertical region labels. Items as cards on the lane. Connectors show dependencies where declared in source docs.
Tablet:  horizontal scroll, lanes preserved.
Mobile:  vertical stacked lanes, bucket as section headers.
```

Behavior:

* Clicking an item scrolls the reader to its `anchors` location and highlights the source evidence.
* `confidence` is visually distinct (solid border = Committed, dashed = Planned, dotted = Exploratory). Never imply commitment without official source wording.
* Timeline data SHOULD be generated from `data/timeline.json` if present, else parsed from HTML headings with `data-roadmap-item` attributes. Keep the HTML as the readable truth; JSON is a derived convenience.
* The timeline and the chapter order MUST agree — no timeline item that has no section in the book.
* Colors and spacing via tokens; no custom CSS per roadmap.

## 72.5 Decision-Tree Component

The decision guide (`/roadmap/decision-guide`) MUST render an interactive **DecisionTree** that operationalizes the Combined Decision Framework. It is the only component that outputs a recommendation.

### Component: `DecisionTree`

```text
Props:
  title: "Choose Your CI Platform"
  nodes: DecisionNode[]
  outcomes: Outcome[]
  disclaimer: string

DecisionNode:
  id: string
  question: string                   // e.g. "Do you require self-hosted, air-gapped runners with custom kernels?"
  help: string                       // ≤ 160 chars
  yes: string  // next node id or outcome id
  no: string
  evidenceIds: string[]              // why this question matters per research docs

Outcome:
  id: string                         // "jenkins" | "actions" | "hybrid" | "either"
  label: string                      // "Jenkins is the better fit"
  summary: string                    // 1–2 sentences, no marketing language
  nextSteps: string[]                // linked checklists: e.g. "Review §6 Agents", "Read lab 06"
  evidenceIds: string[]
```

Flow (canonical 5–7 questions synthesized from the Combined Decision Framework; wording must match the framework, not paraphrase away nuance):

```text
Q1. Self-hosted / air-gapped / custom kernel or hardware?
Q2. Enterprise governance: required SAML/SCIM, audit, policy-as-code at org scale?
Q3. Supply-chain hardening: attestations, artifact signing, SLSA/reproducible builds?
Q4. Team topology: platform team owns infra vs. product teams own YAML?
Q5. Existing investment: deep Jenkins Shared Libraries / plugins to preserve?
Q6. Cost sensitivity to per-minute billing vs. self-hosted capacity planning?
  → Outcomes: Jenkins | GitHub Actions | Hybrid (both, with boundary) | Either (start with Actions)
```

Rules:

* Deterministic, no scoring tricks: the tree is a directed acyclic graph; the path is explainable. Every outcome MUST list the exact questions/decisions that produced it (breadcrumb).
* Each question and outcome links to its Sources evidence and to related books/labs (e.g., Jenkins Agents, GitHub Actions, Secrets, Labs 06–08).
* UI: single question per view with `Yes / No` (and `Why this matters?` expander). Undo/back is mandatory. Final outcome shows: label, summary, breadcrumb, next-steps links, and `Copy share link` that encodes the path as query params (`?path=q1-y,q2-n,...`) for bookmarking.
* Accessibility: radio group or button group with `aria-describedby` for help text; focus moves to next question on advance; full keyboard support.
* No outcome may recommend a platform without citing at least one evidence item from the canonical three docs.
* Print: decision tree prints as a static flowchart (all nodes visible) with outcomes highlighted.

## 72.6 Sources & Freshness Model

Every roadmap book MUST end with a `Sources & Freshness` chapter/section that makes its provenance auditable.

### Required block per source

```text
Source
  Title / Document:  Jenkins Platform Roadmap 2026 — Research Brief
  File:              research/jenkins-2026-roadmap.md  (canonical id)
  Role:              Primary — do not omit or substitute
  Official verification: jenkins.io/changelog, jenkins.io/doc, plugin release notes
  Last verified:     2026-09-01  (ISO date, kept current)
  Verify cadence:    Quarterly
  Owner:             Docs / Platform team
```

The three canonical entries (exact titles required):

1. `research/jenkins-2026-roadmap.md` — **Jenkins 2026 Platform Roadmap**
2. `research/github-actions-2026-security-roadmap.md` — **GitHub Actions 2026 Security Roadmap**
3. `research/combined-decision-framework.md` — **Combined Decision Framework (Jenkins vs. GitHub Actions)**

Additional official sources are supplementary, never replacement:

```text
Canonical (required, exactly these three):
  research/jenkins-2026-roadmap.md
  research/github-actions-2026-security-roadmap.md
  research/combined-decision-framework.md

Supplementary official verification (at least one per non-trivial claim):
  jenkins.io/changelog, jenkins.io/doc/book, jenkins.io/security/advisory,
  docs.github.com/en/actions, github.blog/changelog, GitHub Docs → Actions release notes,
  linked CVEs/advisories where cited.
```

Freshness contract:

* `lastVerified` MUST be an ISO date no older than `verifyCadence` ago. Build (`scripts/qc-check.py`) MUST flag stale roadmaps (`now - lastVerified > cadence`) as a warning and stale > 2× cadence as an error.
* The reader header for roadmap books shows a `Freshness` badge: `Verified 2026-09-01 · quarterly` with color: green (current), amber (due within 30 days), red (overdue). Do not show a badge if metadata is missing — show `Unverified` and log a build warning.
* Every timeline item, comparison row, and decision-tree node/outcome that makes a factual claim MUST carry `evidenceIds` pointing to at least one canonical source entry or a supplementary official source. Un-evidenced claims are a build error.
* Verification rule (hard requirement): **Before any roadmap edit is merged or published, the author MUST re-verify each affected claim against its listed official source and update `lastVerified`.** If an official source contradicts the research doc, the official source prevails and the research doc is annotated as `superseded` for that claim. Never publish an unverified delta.
* The `Sources` section MUST contain a `Verification checklist` callout with the exact wording:

> Verified against official sources on <date>. Jenkins claims checked against jenkins.io/changelog and plugin release notes; GitHub Actions claims checked against docs.github.com and the GitHub Changelog. Canonical research docs remain the synthesis source; official sources are the truth.

Security advisory for readers: if a roadmap claim involves a CVE, secret handling, or supply-chain control, add an explicit `Security note` callout linking to the advisory.

## 72.7 URL Scheme

Roadmap URLs are distinct from book URLs and from the legacy `/roadmap/` visual overview. The legacy overview (existing `dist/roadmap/index.html` — the 39-book visual map) is retained at `/roadmap/` for backward compatibility and cross-linked.

New canonical routes:

```text
/roadmap/                        → legacy visual overview (39-book map) — retained, not replaced
/roadmap/jenkins                 → Jenkins Platform Roadmap 2026 (reader + timeline + comparison subset)
/roadmap/github-actions          → GitHub Actions 2026 Security Roadmap (reader + timeline + comparison subset)
/roadmap/decision-guide          → Combined Decision Framework (reader + full comparison + decision tree)
/roadmap/jenkins#timeline        → deep link: timeline section of Jenkins roadmap
/roadmap/decision-guide#compare  → deep link: comparison table
/roadmap/decision-guide#tree     → deep link: decision tree
```

Implementation mapping (adapt to framework):

```text
/src/pages/roadmap/jenkins.tsx        (or route file)
/src/pages/roadmap/github-actions.tsx
/src/pages/roadmap/decision-guide.tsx
/src/content/books roadmap entries with slug matching route param
```

Rules:

* All three new routes are **first-class pages** with SEO tags (title, description, canonical URL, OG metadata per §54).
* `/roadmap/*` pages reuse the same `ReaderLayout` + `TableOfContents` + `ReaderSettings` as standard books — same typography, same theme tokens, same progress handling. No bespoke layout.
* Breadcrumbs: `Library / Roadmaps / Jenkins` etc., plus `Roadmaps` as a global nav item alongside Library/Topics/Glossary.
* Share/bookmark: every roadmap page supports fragment + query deep links (timeline item id, decision-tree path) suitable for `Copy Link`.
* Redirects: no redirect from `/roadmap/` → any sub-page; the overview stays at `/roadmap/`.

## 72.8 Integration with Library / Reader / Search

Roadmap books are not isolated microsites; they are integrated into the existing platform:

**Library (§8, §69):**
* Roadmaps appear in the library as a distinct shelf/rail labeled `Platform Roadmaps` pinned near the top (above Recently Updated when present). Filter chip `Roadmaps` alongside All/CI/CD/Jenkins/etc.
* Each roadmap card shows: platform badge (Jenkins / GitHub Actions / Decision Guide), horizon (e.g. `2026–2027`), freshness badge (Verified/Unverified), and chapter count.
* Card actions: `[Read]` → `/roadmap/jenkins` (or mapped reader), `[PDF]` preserved.

**Reader (§10–§13, §21, §47):**
* Roadmap books render in the same reader as standard books: left TOC, center content, right tools. The TOC includes `Timeline`, `Comparison`, `Decision Tree` (where applicable), and `Sources & Freshness`.
* Wide content handling (§86–§87) applies: ComparisonTable and RoadmapTimeline use expanded width; body text stays at readable width.
* Right context panel adds roadmap-specific tools when `kind === "roadmap"`: `Timeline minimap`, `Comparison jump`, `Decision tree` launcher — implemented as extensions, not forks, of the standard reader.

**Search (§24–§25):**
* Global search indexes roadmap books with a `type: roadmap` facet. Result snippet shows `Roadmap · Jenkins · 2026` plus evidence excerpt.
* In-book search (`Ctrl/Cmd+K`) indexes roadmap-specific anchors: timeline items, comparison rows, decision-tree questions/outcomes. Matches highlight within the table/timeline where practical.
* Search index generation (`scripts/build.py` / `generate search index` per §80) MUST include roadmap HTML and the derived `data/*.json` if present.

**Topics & Glossary (§50–§51):**
* Roadmaps cross-link to Topic Explorer (`Platform Choice`, `CI/CD Security`, `Migration`) and to Glossary terms (`Runner`, `OIDC`, `Attestation`) via `relatedBooks` / `relatedTopics`.

## 72.9 Validation & Build Gates (extends §64, §80)

Extend `scripts/qc-check.py` and `scripts/build.py` checks for roadmaps:

```text
[ ] All three canonical research docs exist at research/*.md
[ ] Every roadmap entry in books.json has kind=roadmap, platform, sourceDocs (all three), freshness, roadmapMeta
[ ] lastVerified is ISO date and within verifyCadence (quarterly default)
[ ] No roadmap claim (comparison row / timeline item / decision node) without evidenceIds
[ ] Every evidenceId resolves to an entry in Sources & Freshness
[ ] Supplementary official sources are live (HTTP check) or flagged
[ ] /roadmap/jenkins, /roadmap/github-actions, /roadmap/decision-guide routes build and link-check
[ ] ComparisonTable renders on desktop and mobile without overflow
[ ] Timeline buckets cover horizon without gaps/overlaps
[ ] DecisionTree paths are exhaustive (every yes/no leads to an outcome) and every outcome has nextSteps
[ ] Search index includes roadmap anchors
[ ] Print stylesheet renders comparison + timeline + decision tree without cuts
```

Failure mode: if any gate fails, the build MUST warn (stale) or error (missing canonical doc, un-evidenced claim, broken route) — never silently publish.

## 72.10 Design Constraints (extends §44, §84)

* Roadmap components (ComparisonTable, RoadmapTimeline, DecisionTree) use existing design tokens (§16, §84) and the two-theme system (§15–§17). No new palette; status/confidence badges derive from `--accent`, `--warning`, `--success`, `--border`.
* Do not introduce emoji for status; use managed icons (cf. §29).
* Do not add persistent floating CTA or newsletter upsell to roadmap pages — reading remains the priority (§57).

---

# 73. HOME PAGE

The homepage should focus on the library rather than marketing.

Recommended structure:

```text
Hero
────

CI/CD Technical Library

Learn CI/CD from fundamentals
to real-world Jenkins pipelines,
deployment, security and reliability.

[Explore Books]

Featured Books
──────────────

Continue Reading
──────────────

Topics
──────

Recently Updated
────────────────
```

Do not turn it into a generic SaaS landing page.

---

# 74. RECENTLY UPDATED

Show recently updated books/topics when metadata exists.

Example:

```text
Recently Updated

Jenkins Pipelines
Updated Sep 2026

CI/CD Foundations
Updated Sep 2026
```

Use actual metadata only.

---

# 75. CONTINUE READING CARD

If reading progress exists:

```text
Continue Reading

Jenkins
Chapter 5 · Agents

████████████░░░░ 72%
```

If no progress exists, do not show an empty progress component.

---

# 76. EMPTY STATES

Design intentional empty states.

Example:

```text
No books found.

Try another search or browse all categories.
```

Do not leave blank screens.

---

# 77. SECURITY

Do not trust imported HTML blindly.

Sanitize externally sourced HTML before rendering where appropriate.

Prevent:

* Script injection
* Dangerous HTML
* Unsafe embeds

Only allow intentionally supported content.

---

# 78. EXTERNAL LINKS

External links should:

* Be visually identifiable
* Work correctly
* Not break reader navigation
* Open in a new tab where appropriate

Do not create external dependencies for core book functionality.

---

# 79. SOURCE ATTRIBUTION

Where an asset or technical source requires attribution, maintain attribution metadata.

Do not hide licensing information.

Provide a suitable:

```text
Credits / Licenses
```

page or section when required.

---

# 80. REPOSITORY STRUCTURE

Keep the website repository clean.

Recommended:

```text
website/
├── src/
├── public/
├── content/
├── assets/
├── scripts/
├── tests/
├── README.md
└── package.json
```

Do not commit generated junk.

Avoid:

```text
temp/
backup/
old/
final/
final2/
final-real/
```

The filesystem is not a historical record of every bad decision.

---

# 81. AUTOMATION

Create scripts where useful for:

```text
Validate books
Validate links
Generate book index
Generate search index
Check missing assets
Check duplicate IDs
Check PDF availability
Check HTML availability
```

A future content update should not require manually checking hundreds of files.

---

# 82. TESTING

At minimum test:

```text
Library rendering
Book loading
Chapter navigation
TOC
Search
Font size
Theme switching
Reading width
Progress tracking
PDF links
Code copying
Responsive behavior
Broken-content handling
```

Test both themes.

Test desktop and mobile.

---

# 83. VISUAL QUALITY CONTROL

After implementation, inspect the website visually.

Check for:

```text
❌ Empty awkward layouts
❌ Excessive whitespace
❌ Tiny reading text
❌ Excessive rounded cards
❌ Poor contrast
❌ Broken diagrams
❌ Misaligned icons
❌ Inconsistent spacing
❌ Overflowing tables
❌ Horizontal scrolling on normal content
❌ Clipped code
❌ Broken mobile navigation
```

Fix the underlying layout rather than adding random CSS patches.

---

# 84. DESIGN TOKENS

Centralize:

```text
Colors
Typography
Spacing
Radius
Shadows
Borders
Breakpoints
Content widths
Reader widths
```

Example:

```text
tokens/
├── colors
├── typography
├── spacing
├── layout
└── effects
```

Components must consume tokens.

---

# 85. READER CONTENT WIDTH

The reader should have a controlled maximum width.

Example:

```text
max-width:
720px–900px
```

depending on content type.

Long-form paragraphs should remain comfortable.

Diagrams and wide tables may use a wider content container.

Use:

```text
Normal Content
    ↓
Readable Width

Wide Content
    ↓
Expanded Width
```

Do not force every content type into the same width.

---

# 86. WIDE CONTENT HANDLING

For:

* Tables
* Architecture diagrams
* Pipeline diagrams
* Large code examples

allow controlled expansion.

Example:

```text
Normal:
        [ readable content ]

Wide:
[           diagram / table           ]
```

Do not make normal paragraphs equally wide.

---

# 87. CONTENT-AWARE COMPONENTS

The renderer should recognize when content needs more space.

For example:

```text
Paragraph
→ normal width

Code
→ wider

Diagram
→ wider

Table
→ wider

Lab terminal
→ wider
```

This improves readability without making the entire reader unnecessarily wide.

---

# 88. FINAL IMPLEMENTATION PRINCIPLE

The website must be built around this architecture:

```text
                    KNOWLEDGE BASE
                         │
                         ▼
                  ┌───────────────┐
                  │ Markdown / MD │
                  └───────┬───────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          HTML BOOK                PDF BOOK
              │                       │
              ▼                       ▼
       ┌──────────────┐        Download / Print
       │ WEB READER   │
       └──────┬───────┘
              │
     ┌────────┼───────────────┐
     ▼        ▼               ▼
  Themes   Preferences    Navigation
     │        │               │
     ▼        ▼               ▼
 Original   Font Size       TOC
 Light      Width           Search
            Progress        Chapters
            Bookmarks       Related Topics
```

The **knowledge base is the source**.

The **PDF is the printable artifact**.

The **HTML is the web-readable artifact**.

The **website is the interactive reading platform**.

Do not allow one layer to become unnecessarily dependent on another.

---

# 89. FINAL SUCCESS CRITERIA

The implementation is complete only when:

```text
[ ] Books can be browsed
[ ] Books can be opened
[ ] HTML content renders correctly
[ ] PDF can be downloaded
[ ] Chapters are navigable
[ ] TOC works
[ ] Search works
[ ] In-book search works
[ ] Original theme works
[ ] Light theme works
[ ] Font size can be increased
[ ] Font size can be decreased
[ ] Reading width can change
[ ] Preferences persist
[ ] Reading progress persists
[ ] Continue Reading works
[ ] Code blocks have copy buttons
[ ] Diagrams are readable
[ ] Labs are usable
[ ] Glossary works
[ ] Related topics work
[ ] Mobile layout works
[ ] Keyboard navigation works
[ ] Accessibility requirements are addressed
[ ] Print layout works
[ ] Broken content has graceful errors
[ ] Assets are managed centrally
[ ] No emoji are used as technical icons
[ ] No unnecessary duplicate components exist
[ ] New books can be added without architectural changes
[ ] Website remains compatible with future content growth
```

---

# 90. GOLDEN RULE

The platform must be designed around one fundamental principle:

> **The content is the product. The website is the reading environment.**

Do not let UI components, animations, frameworks, or visual effects dominate the technical material.

The user should be able to forget that they are using a website and simply feel like they are reading a very well-designed technical book.

The system must therefore optimize for:

```text
CONTENT
   ↓
READABILITY
   ↓
UNDERSTANDING
   ↓
NAVIGATION
   ↓
CUSTOMIZATION
   ↓
DISCOVERY
```

while remaining:

```text
Fast
Accessible
Responsive
Maintainable
Extensible
Content-driven
```

Build the architecture so that when the knowledge base grows from 2 books to 20 or 100 books, the application remains structurally sane.
