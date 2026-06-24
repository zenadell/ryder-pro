# Antigravity Kickoff — Ryder Pro Template Migration

## Your Two Governing Documents

Before you write a single line of code, read both of these files completely:

1. `plan and access/template-migration-prompt.md` — This is your **operating law**. Every decision you make during this project must be validated against it. You will re-read it before every phase and before every step within each phase. Not from memory — the actual file.

2. `plan and access/vehicle_financing_logistics_platform_spec_v2.md` — This is the **project specification**. It defines what this platform does, what it sells, what pages it needs, what the copy says, and what data models power everything. After the template is clean, this document tells you what to put inside it.

**Read both files right now before doing anything else. Come back to this prompt after you have read them.**

---

## Project Context

**Project name:** Ryder Pro
**What it is:** A vehicle financing, logistics, and marketplace platform. Customers browse vehicles, apply for financing, rent vehicles, track shipments, and apply for transport industry jobs.
**Template source:** Webflow (multi-file extraction)
**Template location:** `template-1/` folder in the project root
**Your working directory:** `ryder-pro/`

---

## Confirmed Tech Stack — Do Not Deviate From This

| Layer | Technology | Purpose |
|---|---|---|
| **Backend framework** | Django 5.x | API, routing, ORM, auth, file uploads, template serving |
| **Admin panel** | Django Admin (extended) | Full content management — vehicles, jobs, applications, users, copy, images |
| **Database** | PostgreSQL | Primary data store |
| **Real-time layer** | Django Channels + Redis | GPS/location tracking, live shipment status, live admin notifications via WebSocket |
| **File storage** | Cloudinary or AWS S3 | Vehicle photos, ID documents, resumes, proof of income — never stored locally |
| **Frontend** | Webflow template → Django templates (.html) | Template HTML becomes Django template files after migration |
| **API** | Django REST Framework | JSON API endpoints for any frontend/JS consumption |
| **Deployment** | Single Django server | No Node, no split backend, no second server |

### Critical architecture notes for Antigravity:

**Django templates are the frontend.** After migration is complete, every `pages/[name]/index.html` file becomes a Django template — extending a `base.html`, using `{% block %}`, `{% for %}`, `{% if %}`, `{{ variable }}` syntax. The migration phase keeps them as plain HTML first. The wiring phase converts them to Django templates.

**Django Channels handles all real-time.** GPS tracking for vehicles and live shipment status updates run over WebSocket connections managed by Django Channels. Redis is required as the channel layer. Do not use polling. Do not use third-party real-time services. Channels is the answer.

**Django Admin is the single source of truth for all content.** Every piece of text, every image, every vehicle listing, every job posting, every page copy block — managed through Django Admin. This means everything visible on the site that could ever change is a database field, not a hardcoded string. During migration this means every TYPE A section that could reasonably be edited by an admin becomes TYPE B with a `SiteContent` or `PageCopy` model backing it.

**The `SiteContent` model pattern:** Create a key-value model for admin-editable static copy:
```python
class SiteContent(models.Model):
    key = models.SlugField(unique=True)   # e.g. "hero_headline"
    value = models.TextField()             # e.g. "Move Your Business Forward"
    updated_at = models.DateTimeField(auto_now=True)
```
This lets the admin change any text on any page without a code deploy. Every heading, subheading, CTA label, trust indicator, and marketing line goes through this model.

---

## What You Are Looking At — Template Structure

The template has already been extracted from Webflow as separate HTML files per page. This means Phase 0 monolith splitting is partially done. However, CSS and JavaScript are almost certainly still embedded inside each HTML file as `<style>` and `<script>` blocks. Your job in Phase 0 is to complete the decomposition — extract CSS and JS out of every HTML file and into their own separate files, then organize everything into the correct folder structure defined in the migration prompt.

**Current template structure (what exists now):**
```
template-1/
├── blog/
│   ├── blog-page.html
│   └── blog.html
├── cars/
│   ├── car-details-p.../     (subfolder — inspect contents)
│   ├── adventure-ca....html
│   ├── all-car-page....html
│   ├── business-car....html
│   ├── famliy-cars.h....html
│   └── wedding-car....html
├── utilities/
│   ├── coming-soon.html
│   ├── error-404.html
│   └── protect-pass-4....html
├── about.html
├── contact.html
├── fqa.html
├── home.html
├── privacy.html
└── terms-conditions.html
```

**Target structure after Phase 0 (what you must build):**
```
template-1/
├── shared/
│   ├── base.css          ← CSS rules used across ALL pages
│   ├── base.js           ← JS used across ALL pages
│   └── fonts/            ← All font files (populated in Phase 2)
├── static/
│   ├── images/           ← All downloaded images (Phase 2)
│   ├── css/vendor/       ← Downloaded third-party CSS (Phase 2)
│   └── js/vendor/        ← Downloaded third-party JS (Phase 2)
├── pages/
│   ├── home/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── about/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── contact/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── faq/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── privacy/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── terms/
│   │   ├── index.html
│   │   ├── style.css
│   │   └── script.js
│   ├── blog/
│   │   ├── index.html
│   │   ├── style.css
│   │   ├── script.js
│   │   └── blog-page/
│   │       ├── index.html
│   │       ├── style.css
│   │       └── script.js
│   ├── cars/
│   │   ├── all-cars/
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   ├── car-details/
│   │   │   ├── index.html
│   │   │   ├── style.css
│   │   │   └── script.js
│   │   ├── adventure/
│   │   ├── business/
│   │   ├── family/
│   │   └── wedding/
│   └── utilities/
│       ├── coming-soon/
│       ├── 404/
│       └── access/
```

---

## Page → Project Mapping

As you migrate each template page, this is what each one becomes in the Ryder Pro platform. Read `vehicle_financing_logistics_platform_spec_v2.md` Section 3 for full details on each page's content requirements.

| Template Page | Becomes In Ryder Pro | Phase |
|---|---|---|
| `home.html` | Homepage — hero, vehicle showcase, financing highlight, jobs, stats, reviews | Phase 1 |
| `about.html` | About Page — company story, mission, team | Phase 1 |
| `contact.html` | Contact Page — form, phone, email, office info | Phase 1 |
| `fqa.html` | FAQ Page — financing FAQ, general FAQ | Phase 1 |
| `privacy.html` | Privacy Policy | Phase 1 |
| `terms-conditions.html` | Terms & Conditions | Phase 1 |
| `cars/all-car-page.html` | Vehicle Marketplace — browse all vehicles | Phase 1 |
| `cars/car-details-p.../` | Vehicle Details Page — gallery, specs, calculator, financing CTA | Phase 1 |
| `cars/adventure-ca....html` | Vehicle category page (repurpose for Trucks / Heavy Equipment) | Phase 1 |
| `cars/business-car....html` | Vehicle category page (repurpose for Fleet / Commercial) | Phase 1 |
| `cars/famliy-cars.h....html` | Vehicle category page (repurpose for Cars / SUVs / Vans) | Phase 1 |
| `cars/wedding-car....html` | Evaluate — may become Rental page or be cut | Flag for decision |
| `blog/blog.html` | Blog index | Phase 1 (skeleton only, no posts yet) |
| `blog/blog-page.html` | Single blog post | Phase 1 (skeleton only) |
| `utilities/coming-soon.html` | Coming Soon page | Keep as-is, rebrand only |
| `utilities/error-404.html` | 404 Error page | Keep as-is, rebrand only |
| `utilities/protect-pass-4....html` | Password protection / access page | Evaluate — may not be needed |

**Pages that need to be CREATED (not in template — build from scratch or adapt existing pages):**
- Financing page (overview, calculator, benefits, apply CTA)
- Financing Application page (full form with document uploads)
- Jobs Portal page (listings)
- Job Details page (single job + apply form)

Flag these to the user when you reach them. Do not build them during migration phase — migration first, then new page construction.

---

## The Copy — How It Works in This Project

**Important shift from standard migration:** The client has confirmed that ALL content — including text that would normally be hardcoded TYPE A — must be editable through Django Admin without a code deploy. This changes the classification rules for this specific project:

### Ryder Pro Content Classification Override

**Everything that displays text or images on the frontend is TYPE B** — backed by either a specific model (Vehicle, Job, BlogPost) or the generic `SiteContent` key-value model. There is no permanent hardcoded copy in this project except structural HTML tags and CSS class names.

| Content | Model | Admin control |
|---|---|---|
| Hero headline, subheading, CTA labels | `SiteContent` | ✅ Full |
| Nav labels | `SiteContent` | ✅ Full |
| Section headings across all pages | `SiteContent` | ✅ Full |
| Trust indicators, feature bullets | `SiteContent` | ✅ Full |
| Footer copy, copyright text | `SiteContent` | ✅ Full |
| Vehicle listings | `Vehicle` | ✅ Full |
| Job postings | `Job` | ✅ Full |
| Blog posts | `BlogPost` | ✅ Full |
| Team members | `TeamMember` | ✅ Full |
| Testimonials / reviews | `Testimonial` | ✅ Full |
| FAQ items | `FAQ` | ✅ Full |
| Page meta titles and descriptions | `PageMeta` | ✅ Full |
| Any image on any page | DB field or `SiteContent` | ✅ Full |

**The `SiteContent` model (add to Django models.py):**
```python
class SiteContent(models.Model):
    key = models.SlugField(unique=True)
    value = models.TextField()
    content_type = models.CharField(
        max_length=20,
        choices=[('text', 'Text'), ('image', 'Image URL'), ('html', 'Rich HTML')],
        default='text'
    )
    page = models.CharField(max_length=50, blank=True)  # e.g. 'home', 'about', 'global'
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name = 'Site Content'
        verbose_name_plural = 'Site Content'
        ordering = ['page', 'key']
```

**In Django templates, every text node becomes:**
```html
<!-- Instead of hardcoded: -->
<h1 class="hero-title">Move Your Business Forward</h1>

<!-- It becomes: -->
<h1 class="hero-title">{{ content.hero_headline }}</h1>
```

**In the Django view, the context is populated like:**
```python
def home_view(request):
    keys = ['hero_headline', 'hero_subheading', 'hero_cta_primary', ...]
    content = {
        obj.key: obj.value
        for obj in SiteContent.objects.filter(key__in=keys)
    }
    vehicles = Vehicle.objects.filter(is_active=True, featured=True)[:6]
    return render(request, 'pages/home/index.html', {
        'content': content,
        'vehicles': vehicles,
    })
```

**Seed data:** Every `SiteContent` key must have a fixture or management command that seeds default values so the site never renders empty keys. Antigravity must create `fixtures/site_content.json` with all default copy during the wiring phase.

**Confirmed seed values for homepage:**
- `hero_headline` → Move Your Business Forward
- `hero_subheading` → Trucks, trailers, vehicles, and equipment for every haul. Flexible financing. Fast delivery. Real support.
- `hero_cta_primary` → Browse Vehicles
- `hero_cta_secondary` → Explore Financing
- `hero_cta_tertiary` → Apply for Jobs
- `trust_1` → Secure Transactions
- `trust_2` → Nationwide & Global Shipping
- `trust_3` → Flexible Financing Plans
- `trust_4` → Trusted Support

For all other keys across all other pages — **ask the user before seeding any value.** Do not invent copy. Do not reuse template demo text.

---

## Brand Identity

**Colors:** Dark Navy + Deep Blue (primary), White + Light Gray (secondary), Bright Blue (accent)
**Style:** Professional, modern, corporate, premium. Enterprise logistics feel. Finance-company trust signals.
**Avoid:** Cartoon styling, overly colorful, playful tone
**Reference feel:** Ryder, Penske, Uber Freight, Schneider

For any CSS color replacement during migration — replace the template's color values with the above palette. If the template uses CSS custom properties (`:root { --color-primary: ... }`), update those variables. Do not hardcode colors into individual rules.

---

## What You Do NOT Build Yet

The following are in the project spec but are **Phase 2 and Phase 3 only.** Do not touch them during migration:
- Vehicle rental system
- Trade-in / swap system
- Shipment tracking system
- Customer dashboard
- Payment integration
- Email / SMS notifications
- Live chat / WhatsApp
- Real financing approval logic (Phase 1 only collects the application form — no automated decisioning)

If a template page maps to a Phase 2+ feature — migrate the HTML/CSS/JS structure cleanly, but leave all content as skeleton placeholders. Do not wire up data that doesn't exist yet.

---

## Execution Instructions

### PHASE A — TEMPLATE MIGRATION (Do this first. Entirely. Before any Django work.)

This phase follows `template-migration-prompt.md` exactly — Phases 0 through 7.
The output is clean, organized, fully-owned HTML/CSS/JS files. No Django yet.
No models. No views. No URLs. Just clean HTML that looks identical to the original.

**Why Django comes after:** You cannot wire a framework onto a dirty template. Mixing migration and wiring creates a state where you don't know if a bug is from the migration or the framework. Keep them separate. Finish one completely. Then start the other.

Order within Phase A:
1. Read both MD files fully
2. Confirm understanding out loud (5 questions from the kickoff prompt)
3. Phase 0 — decompose and organize all template files
4. Phase 1 — full asset audit (all pages)
5. Phase 2 — download everything to local
6. Phase 3 — strip all provider identity
7. Phase 4 through 7 — content plan, surgery, skeletons, verification per page
8. Wait for explicit user approval that ALL pages are clean before Phase B begins

---

### PHASE B — DJANGO WIRING (Only after Phase A is fully approved)

This phase converts the clean HTML files into a working Django application.

**Step B1 — Django project setup:**
```bash
django-admin startproject ryder_pro .
python manage.py startapp core        # SiteContent, PageMeta, homepage views
python manage.py startapp vehicles    # Vehicle model, listings, details
python manage.py startapp financing   # FinancingApplication model
python manage.py startapp jobs        # Job model, applications
python manage.py startapp blog        # BlogPost model
python manage.py startapp tracking    # GPS / shipment tracking (Channels)
python manage.py startapp accounts    # User auth, customer profiles
```

**Step B2 — Convert HTML to Django templates:**
- Every `pages/[name]/index.html` → Django template with `{% extends "base.html" %}`
- Every hardcoded text node → `{{ content.key_name }}`
- Every hardcoded image src → `{{ content.image_key }}` or `{{ object.image.url }}`
- Every list of items → `{% for item in items %}` with skeleton fallback

**Step B3 — Build models per the project spec:**
Read `vehicle_financing_logistics_platform_spec_v2.md` Section 2 for all model definitions.
Build every model. Run migrations. Register everything in Django Admin.

**Step B4 — Build views:**
Every page gets a view function that queries only what that page needs and passes it to the template. No view crashes on empty data. Every TYPE B section falls back to skeleton.

**Step B5 — Django Channels setup (real-time):**
```python
# Install: channels, channels-redis, daphne
# settings.py additions:
INSTALLED_APPS += ['channels', 'daphne']
ASGI_APPLICATION = 'ryder_pro.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]},
    }
}
```
GPS tracking consumer, shipment status consumer, and admin notification consumer are built in the `tracking` app. Do not build these until all other pages are wired and working.

**Step B6 — Seed data:**
Run `python manage.py loaddata fixtures/site_content.json` to populate all default copy.
The site must render correctly with real seeded data and with an empty database (skeletons).

---

### Decision Gates — Ask Before These

1. **Before Phase B begins** — confirm with user that all Phase A pages are approved
2. **Before building the Financing Application form** — confirm required fields with user
3. **Before building Jobs portal** — confirm job categories and application fields with user
4. **Before Django Channels / GPS tracking** — confirm tracking requirements in detail
5. **Before any payment integration** — stop. This is Phase 3 scope. Flag and wait.
6. **`wedding-car.html`** — ask user whether to repurpose as Rental page or cut it
7. **Any copy not in the confirmed seed list above** — ask. Never invent.

---

### Step 1 — Start Here Right Now

Read `plan and access/template-migration-prompt.md` completely.
Read `plan and access/vehicle_financing_logistics_platform_spec_v2.md` completely.

Then come back and state:
1. How many pages are in the template (list them)
2. What platform the template came from
3. What Phase 0 requires you to do first
4. What the three mandatory questions from the Operating Protocol are
5. Which pages need a user decision before you can map them

If you cannot state all five from memory — re-read. Then begin Phase 0.

---

## How to Use the Two MD Files Together

**During migration phases (0 through 7):** `template-migration-prompt.md` is your primary authority. Every technical decision is governed by it.

**During content planning (Phase 4):** Cross-reference `vehicle_financing_logistics_platform_spec_v2.md` Section 3 (Site Map), Section 6 (Copy), and Section 7 (Design) to understand what our content should be for each page section.

**During data surgery (Phase 5):** Cross-reference `vehicle_financing_logistics_platform_spec_v2.md` Section 2 (Data Models) to understand which DB fields map to which template elements. Every TYPE B section must map to a real model from the spec.

**When in doubt about which document applies:** If it's a question about HOW to do something — migration prompt. If it's a question about WHAT to put there — project spec. If neither document answers it — ask me.

---

## Final Reminder

You are not building the platform yet. You are cleaning and claiming ownership of the template. The platform gets built on top of a clean, fully-owned, properly structured template. A dirty migration produces a broken platform. Take your time. Follow the protocol. Show your work. Wait for approval at every gate.

**Begin with Step 1. Read both files. Then come back and confirm your understanding before touching anything.**
