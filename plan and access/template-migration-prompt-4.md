# Template Ownership Migration Prompt

> You are performing **surgical data ownership surgery** on a web template sourced from Webflow, Framer, ThemeForest, HTML5UP, or any similar platform.
>
> Your mission is NOT to redesign the template. The template must look, behave, animate, and feel **100% identical** to the original after you are done.
>
> Your only job is to **replace every piece of data that belongs to the template provider** — every word, image, badge, icon, color value baked into content, and external dependency — with data that belongs to us. Either our own written copy, our own assets, or live data from our database.
>
> **READ THIS ENTIRE PROMPT BEFORE TOUCHING A SINGLE FILE.**
> **DO NOT redesign. DO NOT restructure. DO NOT touch animation logic.**
> **DO NOT batch pages. DO NOT assume. Ask when uncertain.**

**FRAMEWORK:** Django 5.x + Django Channels + PostgreSQL + Redis

**PROJECT:** `[BRIEFLY DESCRIBE WHAT THIS APP DOES]`

---

## PHASE 0 — FILE DECOMPOSITION *(Always first. No exceptions.)*

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Phase 0 requires me to decompose files only — I must not modify any content yet."
> - "I will detect the platform type first before deciding how to split."
> - "I will not begin Phase 1 until the folder structure is built and confirmed."
> If uncertain about any page boundary — ask the user. Do not guess.

Every template from every platform arrives as one or more monolithic files. Before any audit, stripping, or surgery can happen, the codebase must be decomposed into a clean, organized folder structure — one folder per page, with HTML, CSS, and JS fully separated inside each.

This phase runs first regardless of platform. Do not skip it. Do not merge it with Phase 1.

---

### STEP 0A — DETECT THE PLATFORM AND FILE STRUCTURE

Before writing a single folder, examine what you have been given.

**Run this first:**

```bash
# Count total lines in each file provided
wc -l *.html index.html 2>/dev/null

# Check for Framer signatures
grep -n "data-framer\|framer-motion\|FramerBadge\|chunks/\|__framer" index.html | head -20

# Check for Webflow signatures  
grep -n "data-wf-\|data-w-id\|webflow\.js\|w-webflow-badge\|Webflow\.push" index.html | head -20

# Check for other platform signatures
grep -n "themeforest\|elementor\|divi\|squarespace\|wix" index.html | head -20

# Detect page section markers (common patterns across platforms)
grep -n 'id="[^"]*page\|class="[^"]*page-wrapper\|data-page\|<!-- Page\|section id=' index.html | head -40
```

Show me the output. Based on results, classify the situation as one of these:

| Situation | Description | Decomposition Method |
|---|---|---|
| **FRAMER — MONOLITH** | All pages in one `index.html`, 1000+ lines, Framer signatures present | Method A |
| **WEBFLOW — MULTI-FILE** | Separate HTML file per page, Webflow signatures present | Method B |
| **OTHER — MONOLITH** | All pages in one file, unknown or other platform | Method A |
| **OTHER — MULTI-FILE** | Separate files per page, unknown or other platform | Method B |

State your classification out loud before proceeding.

---

### STEP 0B — IDENTIFY ALL PAGE BOUNDARIES

This is the most precise step in Phase 0. Take your time.

**For FRAMER MONOLITH (Method A):**

Framer renders all pages into one HTML file as stacked full-page containers. They are typically wrapped like this:

```html
<!-- Common Framer page wrapper patterns -->
<div id="page-home" ...>...</div>
<div id="page-about" ...>...</div>

<!-- Or hidden/shown via display none -->
<div data-framer-name="Home" style="display:block">...</div>
<div data-framer-name="About" style="display:none">...</div>

<!-- Or as route-based sections -->
<section data-route="/" ...>...</section>
<section data-route="/about" ...>...</section>
```

Run this to find all page containers:

```bash
# Find Framer page wrappers by common patterns
grep -n "data-framer-name\|data-route\|id=\"page-\|class=\"page-\|framer-page\|__framer_page" index.html

# Find display:none blocks (hidden pages)
grep -n 'display:\s*none\|display:none\|visibility:\s*hidden' index.html | head -30

# Find large top-level divs that could be page roots
grep -n '^<div\|^  <div' index.html | head -50
```

List every page you find with its:
- Page name (from `data-framer-name`, route, or ID)
- Starting line number
- Ending line number
- Approximate line count

**For WEBFLOW MULTI-FILE (Method B):**

List every HTML file provided:

```bash
ls -la *.html
wc -l *.html
```

For each file, identify which page it represents (usually clear from filename or `<title>` tag).

**Present the complete page list to the user before building any folders.**

Example output format:

```
PAGES DETECTED:
1. Home          → lines 1–340      (340 lines)
2. About         → lines 341–589    (249 lines)
3. Services      → lines 590–820    (231 lines)
4. Contact       → lines 821–1045   (225 lines)

SHARED ASSETS DETECTED:
- <head> block   → lines 1–42
- Base CSS       → lines 43–180 (embedded <style>)
- Base JS        → lines 1020–1044 (embedded <script>)
```

Wait for my confirmation that the page list is correct before building anything.

---

### STEP 0C — BUILD THE FOLDER STRUCTURE

Only after page boundaries are confirmed, create the folder structure.

**Required structure:**

```
project-root/
│
├── shared/
│   ├── base.css          ← CSS rules used across ALL pages
│   ├── base.js           ← JS used across ALL pages (animation engine, utils)
│   └── fonts/            ← All font files (populated in Phase 2)
│
├── pages/
│   ├── home/
│   │   ├── index.html    ← Home page HTML only
│   │   ├── style.css     ← CSS rules specific to home page only
│   │   └── script.js     ← JS specific to home page only
│   │
│   ├── about/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   ├── [page-name]/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   │
│   └── ... (one folder per page)
│
├── static/
│   ├── images/           ← All downloaded images (populated in Phase 2)
│   ├── css/vendor/       ← Downloaded third-party CSS (populated in Phase 2)
│   └── js/vendor/        ← Downloaded third-party JS (populated in Phase 2)
│
└── [your framework files]
```

Create every folder and empty file before populating anything.

```bash
# Create the structure (adjust page names to match what was detected)
mkdir -p shared/fonts
mkdir -p static/images static/css/vendor static/js/vendor
mkdir -p pages/home pages/about pages/contact
# ... repeat for every detected page

# Create empty files
touch shared/base.css shared/base.js
touch pages/home/index.html pages/home/style.css pages/home/script.js
# ... repeat for every page
```

Show me the folder tree after creation:

```bash
find . -type f | grep -v ".git" | sort
```

---

### STEP 0D — EXTRACTION RULES

This is the most important part of Phase 0. Read carefully.

#### HTML Extraction

For each page, extract only the HTML that belongs to that page's content area. Do not extract shared structure — that goes in the base template.

```
EXTRACT INTO pages/[name]/index.html:
✅ The page's root container div and everything inside it
✅ Page-specific <section>, <div>, <main> content
✅ A reference to shared/base.css
✅ A reference to pages/[name]/style.css
✅ A reference to shared/base.js
✅ A reference to pages/[name]/script.js

DO NOT EXTRACT:
❌ The <head> block (goes in base template)
❌ <script> tags that initialize global animation engines
❌ CSS that applies to multiple pages
❌ The <body> opening/closing tags (base template handles this)
```

#### CSS Extraction — The Hard Part

CSS in monolithic files is almost never cleanly separated by page. You must sort it manually:

**Rule 1 — Shared CSS** goes in `shared/base.css`:
- CSS resets and normalizations (`*, body, html` rules)
- Typography base rules (font-family, font-size on body)
- Color variables and CSS custom properties (`:root { --color: ... }`)
- Utility classes used on more than one page
- Animation `@keyframes` blocks used across pages
- Navigation and footer styles

**Rule 2 — Page-specific CSS** goes in `pages/[name]/style.css`:
- Classes that only appear in that page's HTML
- Section-specific layout rules
- Page-specific animation overrides

**How to determine which is which:**

```bash
# For each CSS class, check which pages use it
# Example: check if .hero-section appears in multiple pages
grep -n "hero-section" pages/*/index.html
# If it appears in only one page → page-specific CSS
# If it appears in multiple pages → shared/base.css
```

When in doubt — put it in `shared/base.css`. Shared is always safe. Missing a shared style breaks multiple pages. Over-including in shared only wastes a few bytes.

#### JS Extraction — The Most Dangerous Part

**Do not split JS without reading this first.**

Animation JS in Framer and Webflow initializes globally. It registers event listeners, sets up scroll watchers, and boots the entire interaction system for all pages at once. Splitting it carelessly will break animations silently — they will appear to work on first load but fail on certain scroll positions or interactions.

**Rule 1 — Everything in `shared/base.js`:**
- The animation engine initialization (Webflow.push, GSAP init, Framer runtime)
- Scroll event listeners
- Any function definitions used across pages
- Third-party library initializations (Swiper, Lottie, etc.)
- **When in doubt — put it in shared/base.js**

**Rule 2 — Only truly isolated code in `pages/[name]/script.js`:**
- Code wrapped in a condition that checks for a page-specific element before running
- Form submission handlers unique to one page
- Page-specific counter or timer logic

```javascript
// Example of safely page-specific JS:
const contactForm = document.getElementById('contact-form');
if (contactForm) {
  // This only runs on the contact page — safe to isolate
  contactForm.addEventListener('submit', handleSubmit);
}

// Example of SHARED JS — never isolate this:
Webflow.push(function() {
  // This initializes the entire animation engine — must stay in shared/base.js
});
```

**If you are unsure whether a JS block is page-specific or shared — put it in shared/base.js.** The cost of over-sharing is zero. The cost of under-sharing is broken animations.

---

### STEP 0E — POPULATE THE FILES

Now fill the empty files with the extracted content.

**Order of operations:**
1. Populate `shared/base.css` first
2. Populate `shared/base.js` first
3. Then populate each page folder, one page at a time
4. After each page is populated, verify it renders correctly before moving to the next

**Verification after each page extraction:**

```bash
# Confirm the page HTML references shared files correctly
grep -n "base.css\|base.js\|style.css\|script.js" pages/[name]/index.html

# Confirm no content from other pages leaked into this file
# (check for identifiers from other pages)
grep -n "[other-page-specific-class]" pages/[name]/index.html
```

Open each extracted page in a browser and confirm:
- Visual appearance is identical to the original monolith
- Animations trigger correctly
- No console errors

---

### STEP 0F — PHASE 0 COMPLETION VERIFICATION

Run all of these before moving to Phase 1:

```bash
# Confirm all pages have all three files
find pages/ -name "*.html" -o -name "*.css" -o -name "*.js" | sort

# Confirm shared files exist and are not empty
wc -l shared/base.css shared/base.js

# Confirm no page HTML file is empty
for f in pages/*/index.html; do echo "$f: $(wc -l < $f) lines"; done

# Confirm each page HTML references the shared files
grep -l "base.css" pages/*/index.html
grep -l "base.js" pages/*/index.html
```

Show me this output. Then open every page in the browser and confirm visual parity with the original.

**State explicitly:**
- How many pages were extracted
- How many lines are in shared/base.css and shared/base.js
- Whether every page renders visually identical to the original

**Wait for my explicit approval before moving to Phase 1.**

---

## ⚠️ MANDATORY OPERATING PROTOCOL — READ BEFORE EVERY SINGLE STEP

This prompt is your law. Not your memory of it — the actual file.

**Before you begin ANY step, you must:**

1. **Re-read this entire MD file from the top.** Not skim it. Read it. Every phase you are about to enter has rules that are easy to misremember and catastrophic to get wrong.
2. **State out loud which step you are about to begin** and quote the exact rule from this file that governs it.
3. **Answer these three questions before writing a single line of code or making any change:**
   - *"What does this prompt explicitly say I must do in this step?"*
   - *"What does this prompt explicitly say I must NOT do in this step?"*
   - *"Do I need approval from the user before I proceed, or can I continue?"*
4. **If your answer to any question is uncertain — stop. Ask. Do not guess. Do not proceed.**

You are not allowed to operate from memory. IDEs drift. Context windows compress. Rules blur. The file does not drift. Re-read it every time.

**This is not optional. This is not bureaucratic overhead. Every major mistake in template migration happens because the agent trusted its memory over the document. You will not do that.**

---

## THE PRIME DIRECTIVE

### What you are NOT doing
- You are NOT redesigning the template
- You are NOT changing layout, spacing, or structure
- You are NOT modifying animation timing, easing, triggers, or sequences
- You are NOT touching JavaScript animation logic under any circumstances
- You are NOT changing DOM hierarchy or class names used by animations

### What you ARE doing
- You ARE replacing every piece of **data** inside the animation containers
- You ARE replacing every hardcoded text string with our copy or a DB-driven variable
- You ARE replacing every hardcoded image `src` with our asset or a DB-driven field
- You ARE removing every badge, watermark, and attribution that belongs to the provider
- You ARE downloading every external asset (CSS, JS, fonts, images) to local storage
- You ARE ensuring zero content arrives from any external platform at runtime
- You ARE ensuring the page reaches the browser with our data already rendered — never the provider's

### The flash problem you are solving
Previous approach used client-side hydration (JavaScript injecting our data after load). This was broken: on slow networks, users saw the provider's original content for 1–3 seconds before our data replaced it. That is unacceptable.

**The solution:** Every piece of our data must be rendered **server-side**, baked into the HTML before it leaves the server. The browser receives a page that has never contained the provider's data. JavaScript only handles animation behavior — never data injection.

---

## UNDERSTANDING ANIMATION-SAFE DATA SURGERY

This is the most critical concept in this entire prompt. Read it twice.

Animation systems (Webflow Interactions, Framer Motion, GSAP, CSS keyframes) work by targeting **DOM elements** — their class names, IDs, positions, and structure. They do not care about the **content inside** those elements.

This means you can freely replace:
- The `src` of an `<img>` inside an animated container
- The text inside a `<span>`, `<h1>`, `<p>`, or `<div>` that gets animated
- The `background-image` CSS value of an animated div
- Color values inside animated elements (where color is content, not animation logic)
- Badge or watermark elements that are overlaid on top of animated sections

You must NEVER touch:
- The class names on animated elements (animation targets)
- The IDs on animated elements
- The DOM structure (nesting order) of animated containers
- Inline `style` attributes that control animation start/end states
- `data-*` attributes consumed by the animation engine
- JavaScript files that contain animation definitions
- CSS `@keyframes` blocks and animation properties

**Rule of thumb:** If removing or changing it would break a visual effect, it is animation logic — leave it. If removing or changing it only changes what you see (the content), not how it moves — replace it.

---

## TWO CONTENT TYPES — CLASSIFY BEFORE YOU TOUCH ANYTHING

Every element on every page belongs to exactly one of these two types.

---

### TYPE A — STATIC CONTENT
Content that is permanently ours and belongs hardcoded in the template. Never comes from a database. Never needs a skeleton loader.

**Examples:**
- Navigation labels
- Section headings and subheadings
- Feature descriptions and bullet points
- How-it-works steps
- CTA button labels
- Footer copy and copyright text
- Marketing taglines and mission statements
- Error and empty state messages
- Legal text

**How to handle:** Replace the provider's text with our exact approved copy, written directly into the HTML. If I have not given you the copy yet, **ask me** — do not invent it.

---

### TYPE B — DYNAMIC CONTENT
Content that comes from our database and changes without a code deploy. Always requires a server-side query. Always needs a skeleton loader for empty states.

**Examples:**
- Any list managed through an admin panel
- User profiles and avatars
- Blog posts, articles, case studies
- Product listings, prices, availability
- Testimonials and reviews
- Team members and bios
- Statistics from live counts
- Any image uploaded through the application

**How to handle:** Remove the provider's hardcoded fake data entirely. Wire the correct database query. Render server-side. Add skeleton loader for empty state. Never let the provider's fake data reach the browser.

---

## PHASE 1 — FULL ASSET AUDIT

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Phase 1 requires me to audit and document only — I must not modify any file."
> - "I will show the user every grep result before moving to Phase 2."
> - "I need the user's review before proceeding past this phase."
> If you cannot answer those confidently from memory, re-read again.

Before touching any file, audit and document everything. Do not modify anything yet.

### 1A — External Dependency Audit

Run these commands and show me the full output:

```bash
# All external script sources
grep -rn "<script" templates/ src/ | grep "src=" | grep -v "localhost"

# All external CSS links
grep -rn "<link" templates/ src/ | grep "href=" | grep -v "localhost"

# All external image references in HTML
grep -rn "src=" templates/ src/ | grep -E "https?://"

# All external URLs in CSS files
grep -rn "url(" static/ assets/ css/ | grep -E "https?://"

# All external URLs buried in JavaScript files
grep -rn "https://" static/ assets/ js/ | grep -v "localhost" | grep -v "//.*comment"

# Provider-specific platform references
grep -rn "webflow\.com\|website-files\.com\|framer\.com\|themeforest\|netlify\|squarespace" templates/ src/ static/ assets/

# Google Fonts (flag for local download decision)
grep -rn "fonts\.googleapis\.com\|fonts\.gstatic\.com" templates/ src/ static/

# Provider badges and attribution links
grep -rni "webflow\|made with\|powered by\|built with\|framer badge\|badge" templates/ src/
```

Show me every result. I will decide what to download locally and what (if anything) stays external.

### 1B — Animation Inventory

Before touching any JS, list every animation system in use:

```bash
# Detect animation libraries
grep -rn "gsap\|ScrollTrigger\|anime\.js\|motion\|framer-motion\|AOS\|Lottie\|swiper\|splide" templates/ src/ static/

# Detect Webflow-native interactions
grep -rn "Webflow\.push\|ix2\|data-w-id\|data-animation\|data-ix" templates/ src/

# Detect CSS animation usage
grep -rn "@keyframes\|animation:\|transition:" static/ assets/ css/

# Detect scroll-triggered or intersection observer animations
grep -rn "IntersectionObserver\|ScrollObserver\|data-aos\|data-scroll" templates/ src/ static/
```

Document every animation found. For each one, note:
- What library or system drives it
- What DOM elements it targets (class names / IDs)
- Whether any of those elements contain content we need to replace

This inventory protects us from accidentally breaking animations during data surgery.

### 1C — Content Inventory

List every hardcoded piece of content that needs to be replaced:

```bash
# Find all text content (scan HTML files)
grep -rn "Lorem\|ipsum\|placeholder\|sample\|dummy\|demo\|example\|fake\|test@\|info@\|hello@" templates/ src/

# Find all hardcoded image srcs pointing externally
grep -rn '<img' templates/ src/ | grep -E 'src="https?://'

# Find all hardcoded background images
grep -rn "background-image\|background:" templates/ src/ static/ | grep -E "url\(.https?://"

# Find all video sources pointing externally  
grep -rn "<video\|<source" templates/ src/ | grep -E "https?://"

# Find all fake contact data patterns
grep -rni "555-\|@example\|@demo\|123 main\|anytown\|12345" templates/ src/
```

Present the complete inventory before any surgery begins.

---

## PHASE 2 — DOWNLOAD EVERYTHING TO LOCAL

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Phase 2 requires me to download assets — I must not modify template content yet."
> - "I must not touch JS file contents — only the path references."
> - "Fonts must be self-hosted with @font-face — no external CDN calls survive."
> - "After Phase 2 I must run the 2F grep verification and show all output before Phase 3."
> If you cannot answer those confidently, re-read again.

Nothing external survives. Everything the template needs must live in our codebase.

### 2A — JavaScript Files

For every external JS file identified in Phase 1:

1. Download to `static/js/vendor/[filename]`
2. Update the `<script src="">` to point to the local path
3. Do NOT modify the JS file contents — animation logic is sacred
4. Exception: if the JS file contains hardcoded provider domain strings (API endpoints, CDN URLs), flag them for me — do not edit without instruction

### 2B — CSS Files

For every external CSS file:

1. Download to `static/css/vendor/[filename]`
2. Update the `<link href="">` to point to the local path
3. Open the downloaded CSS and scan for any `url()` references pointing externally
4. Download those secondary assets too (fonts, images referenced in CSS)
5. Update the `url()` references in the CSS to local paths

### 2C — Fonts

**No font may be loaded from Google Fonts, Adobe Fonts, or any external CDN at runtime.**

For every font in use:

1. Identify the font family and weights needed
2. Download the font files (woff2 preferred, woff as fallback) to `static/fonts/`
3. Create `@font-face` declarations in our main CSS file
4. Remove the external `<link>` or `@import` that loaded them
5. Verify the font renders identically after switching to local

### 2D — Images and Icons (Layout Assets)

For every decorative image, background, icon, or illustration that is part of the design (not content):

1. Download to `static/images/[descriptive-name].[ext]`
2. Update every reference (HTML `src`, CSS `url()`, `srcset`) to the local path
3. Verify dimensions and format match what the animation system expects

### 2E — Lottie / SVG Animations / JSON Assets

If the template uses Lottie animations, SVG sprite sheets, or JSON animation data:

1. Download all `.json`, `.svg`, and animation asset files to `static/animations/`
2. Update all references to local paths
3. Do NOT modify the animation data — only the path reference

### 2F — Verification After Phase 2

Run these — all must return zero external references:

```bash
# No remaining external scripts
grep -rn "src=\"https\?://" templates/ src/ | grep "<script"

# No remaining external stylesheets
grep -rn "href=\"https\?://" templates/ src/ | grep "<link.*stylesheet"

# No remaining external images in HTML
grep -rn "src=\"https\?://" templates/ src/ | grep "<img"

# No remaining external URLs in CSS
grep -rn "url(\"https\?://" static/ assets/ css/

# No remaining font CDN calls
grep -rn "fonts\.googleapis\|fonts\.gstatic\|typekit\|use\.fontawesome" templates/ src/ static/
```

Show me the output. All must return zero. Do not proceed to Phase 3 until confirmed.

---

## PHASE 3 — STRIP ALL PROVIDER IDENTITY

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Phase 3 is identity stripping only — badges, meta tags, analytics, attribution."
> - "I must cross-reference Phase 1B animation inventory before removing ANY data-* attribute."
> - "If a data-* attribute appears in the animation inventory, I must NOT remove it."
> - "I do not need user approval to start Phase 3, but I must show results before Phase 4."
> If uncertain on any attribute — stop and ask the user before removing it.

Now remove everything that identifies this template as belonging to someone else.

### 3A — Platform Badges and Watermarks

These are injected by the platform and must be completely removed:

```bash
# Webflow badge
grep -rn "w-webflow-badge\|webflow\.com/badge\|Made in Webflow" templates/ src/

# Framer badge  
grep -rn "framer\.com\|FramerBadge\|Made with Framer\|framer-badge" templates/ src/

# ThemeForest / Envato attribution
grep -rn "themeforest\|envato\|codecanyon" templates/ src/

# Any "powered by" or "built with" attribution
grep -rni "powered by\|built with\|made with\|created with" templates/ src/
```

Remove every match entirely — the element, its parent wrapper if it exists solely for the badge, and any associated CSS. Confirm the visual output is unaffected (these are usually absolutely positioned overlays).

### 3B — Provider-Specific Data Attributes

**CRITICAL: Read the animation inventory from Phase 1B before doing this step.**

Only remove provider data attributes that are NOT consumed by the animation engine.

```bash
# Webflow CMS and configuration attributes (NOT animation attributes)
grep -rn "data-wf-domain\|data-wf-site\|data-wf-page\|data-wf-collection" templates/ src/

# Framer publish and site attributes (NOT animation/motion attributes)
grep -rn "data-framer-site\|data-framer-hydrate\|data-framer-appear-id" templates/ src/
```

For each match, cross-reference against the animation inventory. If the attribute is in the animation inventory — leave it. If it is not — remove it.

**Never remove:** `data-w-id`, `data-animation`, `data-framer-component`, `data-framer-name`, or any attribute that appears in animation targeting code.

### 3C — Provider Meta Tags and SEO Data

```bash
grep -rn "og:site_name\|twitter:site\|generator\|webflow\|framer" templates/ src/ | grep "<meta"
```

Replace every provider meta value with our own. Example:
- `<meta name="generator" content="Webflow">` → remove entirely or replace with our stack name
- `og:site_name` → our brand name
- `twitter:site` → our Twitter handle

### 3D — Provider Analytics and Tracking

```bash
# Any tracking scripts
grep -rn "gtag\|ga\(\|fbq\|_hsq\|intercom\|hotjar\|mixpanel\|segment\|amplitude" templates/ src/ static/

# Webflow analytics
grep -rn "d3e54v103j8qbb\.cloudfront\|webflow\.js\|w\.webflow" templates/ src/ static/
```

Remove every tracking script that belongs to the provider. We will add our own analytics separately.

### 3D — Favicon and Web Manifest

```bash
grep -rn "favicon\|apple-touch-icon\|manifest\.json\|site\.webmanifest" templates/ src/
```

Replace every provider favicon with our own assets. Update `manifest.json` with our app name, colors, and icons. Never ship with the provider's branding in the browser tab.

---

## PHASE 4 — CONTENT PLAN *(Required before any data replacement)*

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Phase 4 is planning only — I write zero code, I change zero files."
> - "Every animated section must list the animation system and confirm the elements I plan to modify are content containers, not animation targets."
> - "I must present this plan ONE PAGE AT A TIME."
> - "I cannot begin Phase 5 without the user's explicit written approval of this plan."
> If you do not have the user's copy for a TYPE A section — ask now, before presenting the plan.

Map every section of every page before touching a line of content.

```
PAGE: [page name]

  SECTION: [section name]
  Animation: [yes / no — list animation system if yes]
  Type: TYPE A or TYPE B

  If TYPE A:
    Current provider text: [what's there now]
    Our replacement text: [exact copy — ask me if not provided]
    Images in this section: [list each one]
    Our replacement images: [our asset path or ask me]
    Animation containers affected: [list class names / IDs]
    Safe to replace content: [confirm animation inventory check]

  If TYPE B:
    Current provider fake data: [describe what's there]
    Model/Source: [database model or API]
    Query: [server-side query]
    Fields shown: [which fields map to which elements]
    Images: [which field provides image src]
    Empty state skeleton: [describe shape]
    Count: [expected number of items]
    Animation containers affected: [list class names / IDs]
    Safe to replace content: [confirm animation inventory check]
```

**Animated sections require extra documentation.** For any section where animations are present, explicitly confirm that the elements you plan to modify are content containers, not animation targets. If you are not certain — ask me. Never guess.

Present the plan page by page. Wait for my written approval before building anything.

---

## PHASE 5 — PERFORMING DATA SURGERY

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top. Re-read the QUICK REFERENCE TABLE at the bottom.
> Then answer out loud:
> - "I have the user's explicit written approval of the Phase 4 content plan."
> - "I will work element by element — not file by file, not section by section."
> - "I will never change class names, IDs, data-* animation attributes, or inline styles on animated elements."
> - "I will never use client-side fetch or JavaScript to inject content — all data is server-side rendered."
> - "For every element I am about to change, I can confirm it is content (safe) not animation logic (forbidden)."
> If you cannot confirm all five — re-read. Do not proceed until you can.

Only begin after the content plan is approved.

### The Surgery Rules

**Rule 1: Work element by element, not file by file.**
Go line by line through every template file. Evaluate each element. Do not batch-replace across files.

**Rule 2: Never change the element — only its content.**

```html
<!-- CORRECT: Changed only the src and alt, kept everything else identical -->
<img 
  class="hero-image animate-fade-in" 
  data-w-id="abc123"
  src="/static/images/our-hero.jpg"
  alt="Our product in action"
  style="opacity:0; transform:translateY(20px)"
/>

<!-- WRONG: Removed the data attribute and style that the animation needs -->
<img src="/static/images/our-hero.jpg" alt="Our product" />
```

**Rule 3: Never change animation-adjacent attributes.**
If an element has `style` attributes controlling its initial animation state (opacity: 0, transform, visibility), leave them exactly as they are. Only change `src`, text content, and `alt`.

**Rule 4: Background images inside animated divs.**
When a div has both a `background-image` and animation classes:

```css
/* CORRECT: Only change the image URL, keep all animation properties */
.hero-bg {
  background-image: url('/static/images/our-background.jpg'); /* ← changed */
  animation: fadeIn 0.8s ease forwards;                        /* ← untouched */
  opacity: 0;                                                   /* ← untouched */
  transform: scale(1.05);                                       /* ← untouched */
}
```

**Rule 5: TYPE B sections — remove fake data completely.**
Never leave provider fake data as a fallback. The template engine must render either real data or skeletons. No third option exists.

### Server-Side Rendering Requirement

All TYPE B content must be rendered before the HTML leaves the server.

```
FORBIDDEN — client-side hydration (old approach):
Page loads → browser receives provider's fake data →
JavaScript runs → data replaced → user may see original

REQUIRED — server-side rendering:
Server queries DB → data injected into template →
Browser receives HTML with our data already present →
JavaScript only handles animation behavior
```

Your framework's template engine handles this. Examples:

**Django:**
```html
{% if products %}
  {% for product in products %}
    <div class="product-card animate-slide-up" data-w-id="{{ product.id }}">
      <img class="product-img" src="{{ product.image.url }}" alt="{{ product.name }}">
      <h3 class="product-title">{{ product.name }}</h3>
    </div>
  {% endfor %}
{% else %}
  {% include "skeletons/product-card.html" with count=6 %}
{% endif %}
```

**Next.js (getServerSideProps):**
```jsx
export async function getServerSideProps() {
  const products = await db.product.findMany({ where: { active: true } });
  return { props: { products } };
}

// In component — no useEffect, no fetch, no hydration
{products.length > 0 
  ? products.map(p => <ProductCard key={p.id} {...p} />)
  : <SkeletonGrid count={6} />
}
```

---

## PHASE 6 — SKELETON LOADERS

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "Every TYPE B section I built in Phase 5 needs a skeleton loader — I have a list of them."
> - "Each skeleton must mirror the DOM structure and dimensions of the real content."
> - "Skeleton CSS is added once to the global stylesheet — not duplicated per component."
> - "The skeleton renders server-side when the DB query returns empty — it is NOT JavaScript-injected."
> List every TYPE B section from Phase 5. Confirm each one has a skeleton before moving to Phase 7.

Every TYPE B section must have a skeleton that matches the shape of the real content.

### Skeleton CSS

Add once to the global stylesheet:

```css
.skeleton {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  display: block;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Size utilities */
.skeleton-image    { height: 200px; width: 100%; margin-bottom: 12px; }
.skeleton-title    { height: 24px;  width: 70%; margin-bottom: 10px; }
.skeleton-text     { height: 16px;  width: 100%; margin-bottom: 8px; }
.skeleton-text.short { width: 50%; }
.skeleton-avatar   { height: 48px;  width: 48px; border-radius: 50%; }
.skeleton-badge    { height: 20px;  width: 80px; border-radius: 20px; }
.skeleton-button   { height: 40px;  width: 120px; border-radius: 6px; }
.skeleton-full-card { height: 320px; width: 100%; }
```

### Skeleton Structure Rule

The skeleton must mirror the DOM structure of the real content exactly — same number of elements, same approximate dimensions. This prevents layout shift when real data loads.

```html
<!-- Real card structure -->
<div class="team-card animate-fade-up" data-w-id="team-1">
  <img class="team-photo" src="..." alt="...">
  <h3 class="team-name">...</h3>
  <p class="team-role">...</p>
</div>

<!-- Skeleton must mirror same structure -->
<div class="team-card"> <!-- Same class for layout, no animation class needed -->
  <span class="skeleton skeleton-image"></span>
  <span class="skeleton skeleton-title"></span>
  <span class="skeleton skeleton-text short"></span>
</div>
```

---

## PHASE 7 — VERIFICATION

> 🔁 **STOP. Before proceeding:**
> Re-read this MD file from the top.
> Then answer out loud:
> - "I will run every grep command in 7A and show the user every result — not just the ones that pass."
> - "I will verify animations visually in the browser — not just assume they still work."
> - "I will test the page with an empty database to confirm skeletons render — not just with real data."
> - "I cannot mark this page complete or move to the next page without the user's explicit written approval."
> Do not shortcut verification. A page is not done because you think it is done. It is done when the user says it is done.

Run every check before declaring a page complete.

### 7A — Zero Provider Content

```bash
# No provider platform references remain
grep -rn "webflow\.com\|framer\.com\|website-files\.com\|themeforest\|netlify\.app" templates/ src/ static/

# No placeholder or fake text
grep -ri "lorem\|ipsum\|placeholder\|dummy\|fake\|sample text\|test data" templates/ src/

# No external image sources
grep -rn 'src="https\?://' templates/ src/ | grep "<img"

# No external background images in CSS
grep -rn 'url("https\?://' static/ assets/ css/

# No provider badges
grep -rni "webflow-badge\|framer-badge\|made with\|powered by\|built with" templates/ src/

# No external fonts
grep -rn "fonts\.googleapis\|fonts\.gstatic\|use\.typekit\|use\.fontawesome\.com" templates/ src/ static/

# No provider meta or generator tags
grep -rn "webflow\|framer" templates/ src/ | grep "<meta"
```

**All must return zero.** Show me the output.

### 7B — Animation Integrity

For every animation identified in Phase 1B:

- [ ] All targeted class names are still present on their elements
- [ ] All targeted IDs are still present on their elements
- [ ] DOM structure (nesting) of animated containers is unchanged
- [ ] Inline style attributes on animated elements are unchanged
- [ ] All `data-*` attributes consumed by the animation engine are unchanged
- [ ] All JS animation files are loaded from their new local paths and unchanged in content
- [ ] Animation runs identically to the original — verify visually in browser

### 7C — Data Surgery Verification

- [ ] No provider text is visible anywhere on the page
- [ ] No provider images are visible or referenced
- [ ] All TYPE A sections contain our exact approved copy
- [ ] All TYPE B sections render from our database (verified with test data)
- [ ] All TYPE B sections show skeleton loaders when database is empty
- [ ] No JS is injecting content after page load (check Network tab — no fetch calls populating visible content)
- [ ] Page source code (View Source) contains our data, not provider data

### 7D — Asset Independence

Test with all external requests blocked:

1. Open browser DevTools → Network tab
2. Right-click any external request → Block request URL
3. Block every domain except our own server
4. Hard refresh the page
5. Page must still render correctly — layout intact, fonts correct, animations running
6. The only things allowed to fail are optional third-party embeds (maps, video players)

### 7E — SEO and Structure

- [ ] One unique H1 per page
- [ ] Unique `<title>` tag — our brand, not provider's demo
- [ ] `<meta name="description">` — our copy
- [ ] `og:title`, `og:description`, `og:image` — all ours
- [ ] All images have descriptive `alt` text
- [ ] Heading hierarchy: H1 → H2 → H3 (no skipped levels)
- [ ] Favicon is ours — verify in browser tab

### 7F — What to Show Me Before Marking a Page Complete

1. Screenshot of page with real data in the database — must look identical to original template
2. Screenshot of page with empty database — skeleton loaders visible, no layout collapse
3. Browser DevTools Network tab — no requests to external provider domains
4. Page source (Ctrl+U) — our data present in raw HTML, no provider content visible
5. Console tab — zero errors
6. All grep commands from 7A — all return zero

**Wait for my explicit written approval before proceeding to the next page.**

---

## EXECUTION ORDER — DO NOT DEVIATE

Every step begins the same way: **re-read this MD file. Answer the three questions. Then proceed.**

| Step | Phase | Action | Re-read Required | Gate |
|---|---|---|---|---|
| **1** | 0A | Detect platform and file structure. Show grep output. | ✅ Yes | My classification confirmation |
| **2** | 0B | Identify all page boundaries. Show page list with line numbers. | ✅ Yes | My confirmation of page list |
| **3** | 0C | Build folder structure. Show file tree. | ✅ Yes | — |
| **4** | 0D–0E | Extract and populate files. One page at a time. | ✅ Yes — per page | Visual parity check per page |
| **5** | 0F | Phase 0 verification. Show all output. | ✅ Yes | My explicit written approval |
| **6** | 1 | Full asset audit. Show all grep output. | ✅ Yes | My review of all output |
| **7** | — | Ask me for all missing TYPE A copy. | ✅ Yes | My supply of copy |
| **8** | 2 | Download all assets to local. | ✅ Yes | Run 2F grep — all zero — show output |
| **9** | 3 | Strip provider identity. | ✅ Yes | Cross-check animation inventory first |
| **10** | 4 | Present content plan for page 1. | ✅ Yes | My explicit written approval |
| **11** | 5 | Perform data surgery on page 1. | ✅ Yes | Approved content plan in hand |
| **12** | 6 | Add skeleton loaders for all TYPE B sections. | ✅ Yes | TYPE B list confirmed |
| **13** | 7 | Run full verification — show all output. | ✅ Yes | My explicit written approval |
| **14** | — | Repeat steps 10–13 for every remaining page. | ✅ Yes — per page | Approval per page, every time |

**ONE PAGE AT A TIME. ONE STEP AT A TIME. RE-READ THE FILE EVERY TIME.**

If you find yourself about to work on step N+1 without having shown me the output of step N — you have broken protocol. Stop. Show me the output. Wait for approval.

---

## QUICK REFERENCE — WHAT TO REPLACE vs. WHAT TO NEVER TOUCH

| Element | Replace? | Notes |
|---|---|---|
| Text content inside animated element | ✅ Yes | Change text only, not the element or its attributes |
| `src` of `<img>` inside animated container | ✅ Yes | Keep all other attributes untouched |
| `background-image` URL in CSS | ✅ Yes | Keep all other CSS properties on that rule |
| `alt` text on images | ✅ Yes | Always replace with descriptive copy |
| Provider badge / watermark element | ✅ Yes — Remove | Remove entire element |
| Provider `<meta>` tags | ✅ Yes — Replace | Replace values with ours |
| External script `src` URLs | ✅ Yes — Localize | Download file, update path |
| External CSS `href` URLs | ✅ Yes — Localize | Download file, update path |
| External font imports | ✅ Yes — Localize | Self-host with @font-face |
| Class names on animated elements | ❌ Never | Animation targets these |
| IDs on animated elements | ❌ Never | Animation targets these |
| `data-w-id`, `data-animation` | ❌ Never | Webflow animation engine |
| `data-framer-component` | ❌ Never | Framer animation engine |
| Inline `style` on animated elements | ❌ Never | Animation start states |
| DOM nesting of animated containers | ❌ Never | Animation structure |
| JS animation files (content) | ❌ Never | Only update the path reference |
| `@keyframes` blocks | ❌ Never | Core animation logic |
| CSS `animation:` and `transition:` properties | ❌ Never | Core animation logic |

---

---

## IF YOU EVER FEEL UNCERTAIN, LOST, OR LIKE YOU'RE DRIFTING

Stop immediately. Do not continue. Do the following:

1. **Re-read this entire MD file from the top.**
2. Identify exactly which step in the execution order you are on.
3. Read the self-check gate for that phase out loud.
4. Answer the three mandatory questions.
5. If you still feel uncertain — **tell the user where you are and what you're unsure about.** Do not guess your way through it. Do not fill the gap with assumptions. Ask.

The template will survive you pausing. It will not survive you assuming.

---

*I will now provide the template files.*
