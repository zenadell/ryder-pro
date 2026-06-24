# Vehicle Financing, Logistics & Marketplace Platform
### Developer Specification — v2

> **How to use this document:** Section 0 and Section 11 come first because they're the decisions that change everything else. Read those before estimating. Sections 1–10 describe the full long-term vision; Section 0 tells you what to actually build first.

---

## 0. Build Phasing (Read This First)

The original plan describes a complete platform — marketplace, financing, rentals, trade-ins, shipment tracking, and a jobs board — as one build. That's a multi-month, multi-developer scope if built all at once, and several pieces (live financing approvals, real payment processing, trade-in valuation) can't be built correctly until business-side decisions are made (see Section 11).

Recommended phasing:

### Phase 1 — MVP (launch-ready core)
- Vehicle marketplace (browse, search, filter, vehicle details)
- Financing calculator (client-side estimate only, no real approval logic)
- Financing **application** submission (collects data, stores it, notifies admin — no automated approval/decision engine)
- Jobs portal (listings + application submission)
- Basic admin dashboard (manage vehicles, manage jobs, view submitted applications)
- Authentication (signup/login/password reset)
- Contact + About pages
- Core design system applied site-wide

### Phase 2 — Transactional features
- Real payment integration (once a provider is chosen — see Section 11)
- Customer dashboard (track own applications, payments, rentals)
- Trade-in submission + admin valuation workflow
- Vehicle rental requests
- Shipment tracking (manual status updates by admin first; provider API integration later)
- Email/SMS notifications

### Phase 3 — Scale & polish
- Lease-to-own workflows
- Reviews/testimonials system
- Live chat / WhatsApp integration
- Admin analytics & reporting
- Multi-language / multi-currency (if confirmed needed)

**Why this matters for estimation:** Phase 1 is a buildable, fixed-scope project. Phases 2–3 depend on answers in Section 11 and should be scoped separately once those are confirmed. Don't quote the whole platform as one number.

---

## 1. Project Overview

### Business Purpose
A transportation ecosystem platform combining vehicle sales, installment financing, rentals, lease-to-own, trade-ins, shipment tracking, and transport-industry recruitment. Positioned as a trusted logistics/finance brand, not a basic listings site.

### Target Audience
Individuals buying vehicles; customers seeking installment financing; businesses sourcing fleet vehicles; truck owner-operators; logistics companies; truck drivers, dispatch riders, tractor operators; fleet managers; vehicle sellers and traders; equipment operators; transport recruiters.

### Core Business Goals
1. Sell vehicles
2. Offer installment financing
3. Offer vehicle rentals
4. Support lease-to-own programs
5. Support trade-ins and upgrades
6. Provide shipment tracking
7. Operate a transport job marketplace
8. Connect customers with financing
9. Multi-channel revenue generation
10. Build trust through transparency and professional presentation

---

## 2. Data Model (New)

This is the minimum entity structure the build relies on. Field lists are not exhaustive — they cover what's needed to support the flows in Section 4.

**User**
`id, name, email, phone, password_hash, role (customer/admin), email_verified, created_at`

**Vehicle**
`id, category (car/suv/pickup/cargo_van/semi_truck/box_truck/flatbed/dispatch_bike/tractor/forklift/heavy_equipment), make, model, year, price, mileage, condition, financing_eligible (bool), status (available/reserved/sold), photos[], specs (JSON), created_at`

**FinancingApplication**
`id, user_id, vehicle_id, full_name, email, phone, country, address, government_id_file, drivers_license_file, proof_of_income_file, employment_details, business_details (nullable), status (submitted/under_review/approved/rejected), submitted_at`

**TradeIn**
`id, user_id, make, model, year, mileage, vin, condition, photos[], admin_valuation (nullable), status (submitted/valued/offer_made/accepted/rejected), target_vehicle_id (nullable)`

**Rental**
`id, user_id, vehicle_id, duration_type (daily/weekly/monthly/lease_to_own), start_date, end_date, status (requested/approved/active/completed), payment_status`

**Job**
`id, title, category, description, requirements, salary_range, location, status (open/closed), created_at`

**JobApplication**
`id, job_id, user_id, resume_file, status (submitted/reviewed/accepted/rejected), submitted_at`

**Shipment**
`id, financing_application_id (or order reference), tracking_number, status (order_confirmed/processing/financing_approved/ready_for_shipment/in_transit/customs_clearance/out_for_delivery/delivered), status_history[]`

**Review**
`id, user_id, vehicle_id (nullable), content, rating, status (pending/published), created_at`

> Note for developer: exact field types/constraints should be finalized against whichever stack is chosen (Section 9).

---

## 3. Site Map / Pages

### Home Page
Hero banner, slogan, primary CTAs (Browse Vehicles / Apply for Financing / Apply for Jobs), trust indicators, vehicle showcase, financing highlight, shipment tracking widget, featured jobs, customer reviews, stats section, "Why Choose Us," footer.

### Vehicle Marketplace
Categories: Cars, SUVs, Pickup Trucks, Cargo Vans, Semi Trucks, Box Trucks, Flatbed Trucks, Dispatch Bikes, Tractors, Forklifts, Heavy Equipment.
Features: search, filters, sort, financing-eligibility filter, compare vehicles (Phase 2+ if compare adds complexity — flag during build).

### Vehicle Details Page
Gallery, specs, pricing, financing calculator, availability, trade-in option, apply-for-financing CTA, contact sales.

### Financing Page
Overview, benefits, calculator, eligibility, FAQ, apply button.

### Financing Application Page
Fields: full name, email, phone, country, address, government ID upload, driver's license upload, proof of income upload, business details, employment details.

### Vehicle Rental Page (Phase 2)
Daily / weekly / monthly / lease-to-own options across cars, trucks, vans, bikes, tractors.

### Trade-In / Swap Page (Phase 2)
Submit vehicle (make, model, year, mileage, VIN, condition, photos) → admin valuation → offer → apply toward upgrade.

### Sell Your Vehicle Page (Phase 2)
Create listing, upload photos, receive offers, request valuation.

### Shipment Tracking Page (Phase 2)
Statuses: Order Confirmed → Processing → Financing Approved → Ready for Shipment → In Transit → Customs Clearance → Out for Delivery → Delivered.

### Jobs Portal
Categories: Truck Driver, CDL Driver, Dispatch Rider, Bike Courier, Tractor Operator, Forklift Operator, Fleet Manager, Logistics Coordinator, Warehouse Staff, Mechanic.

### Job Details Page
Description, requirements, salary range, location, apply form.

### Customer Dashboard (Phase 2)
Profile, financing status, payments, shipment tracking, rentals, trade-in requests, invoices, notifications.

### Admin Dashboard
Phase 1: manage vehicles, manage jobs, view applications.
Phase 2+: manage payments, financing approval workflow, trade-ins, shipments, analytics.

### About Page
Company story, mission, team, leadership, trust info.

### Contact Page
Contact form, phone, email, office info, support channels.

---

## 4. Features & Functionality

**Authentication:** signup, login, password reset, email verification.

**Vehicle Search:** keyword, category filter, price filter, financing-eligibility filter.

**Financing Calculator:** inputs — vehicle price, down payment, term. Outputs — amount financed, monthly payment, total repayment. *(Phase 1: estimate only, not tied to a real approval decision.)*

**Financing System:** application submission, document upload, status tracking, approval workflow. *(Phase 1 = manual admin review; automated approval logic is Phase 2+ and depends on Section 11 answers.)*

**Trade-In System (Phase 2):** submission, admin valuation, offer generation, apply to upgrade.

**Rental System (Phase 2):** availability check, rental request, lease-to-own request.

**Shipment Tracking (Phase 2):** tracking lookup, delivery timeline, status updates (manual admin-driven first, provider-API-driven later).

**Job System:** listings, resume upload, application tracking.

**Reviews (Phase 3):** customer reviews, testimonials, success stories.

**Notifications (Phase 2):** email, SMS, in-dashboard.

**Live Chat (Phase 3):** support chat, WhatsApp integration.

---

## 5. User Flows

### Vehicle Financing Flow
Browse vehicles → view details → use calculator → click Apply → create account → upload documents → submit application → admin review → approval/rejection → (if approved) payments → progress tracking → shipment begins → track shipment → delivered.

### Trade-In Flow (Phase 2)
Open Trade-In page → submit vehicle info → upload photos → admin valuation → receive offer → select replacement vehicle → pay or finance the difference → complete transaction.

### Rental Flow (Phase 2)
Browse rentals → select vehicle → choose duration → submit request → approval → payment → vehicle release.

### Job Application Flow
Browse jobs → open job → click Apply → upload resume → submit → track status.

---

## 6. Content & Copy

**Hero headline:** Move Your Business Forward

**Supporting copy:** Trucks, trailers, vehicles, and equipment for every haul. Flexible financing. Fast delivery. Real support.

**Primary buttons:** Browse Vehicles · Explore Financing · Apply for Jobs

**Trust messaging:** Secure Transactions · Nationwide & Global Shipping · Flexible Financing Plans · Trusted Support

**Why Choose Us:** Wide Vehicle Selection · Flexible Financing · Reliable Shipping · Secure Payments · Customer Support

---

## 7. Design & Branding Notes

**Visual style:** Professional, modern, corporate, premium.

**Colors:** Primary — Dark Navy, Deep Blue. Secondary — White, Light Gray. Accent — Bright Blue.

**Avoid:** overly colorful layouts, cartoon styling.
**Prefer:** enterprise logistics look, finance-company feel, clean UI, trust-focused design.

**Reference brands:** Ryder, Penske, Uber Freight, Schneider.

**Homepage feel:** Active, busy, established — never empty. Use fleet imagery, vehicle cards, dashboard previews, tracking widgets, stats, testimonials.

---

## 8. Admin / Backend Needs

**Vehicles:** add / edit / remove.
**Financing:** review applications, approve, reject, track status.
**Jobs:** create, edit, review applications.
**Trade-Ins (Phase 2):** review submissions, assign valuations.
**Shipments (Phase 2):** create tracking numbers, update statuses.
**Content:** edit homepage content, manage testimonials, manage banners.
**Analytics (Phase 3):** sales reports, application reports, customer reports.

---

## 9. Technical Requirements

### Stack
*Not yet specified in the original plan — needs a decision before Phase 1 starts.* Developer should propose a stack (e.g. for a solo build: a framework like Next.js/Django/Laravel + PostgreSQL + cloud storage for uploads) and confirm with the business owner before kickoff.

### Integrations (by phase)
- Phase 1: none required beyond file storage and email (e.g. transactional email for application confirmations).
- Phase 2: payment gateway, SMS service, shipment tracking provider API, identity verification (if doing real KYC).
- Phase 3: WhatsApp Business API, analytics tooling.

### File Uploads
Required for: government ID, driver's license, resumes, proof of income, vehicle photos, trade-in photos. All uploads need size/type limits, virus scanning consideration, and secure storage (not public-read by default — IDs and income docs are sensitive).

### Security
SSL, secure auth (hashed passwords, session/token management), basic fraud-prevention checks on financing submissions, data protection for uploaded documents (this platform will hold government IDs and income proof — treat as sensitive PII regardless of jurisdiction).

---

## 10. Out of Scope (Phase 1–2)

Not included unless explicitly approved later:
- Native mobile apps
- AI recommendation engine
- Dealer portal
- Full fleet management software
- Affiliate system
- Insurance marketplace
- Advanced owner-operator program

---

## 11. Decisions Required Before Development Starts

These aren't "nice to have later" — several of them change the architecture, so they're split by urgency.

### 🔴 Blocking — needed before Phase 1 can be scoped or quoted
1. **Is this platform originating loans itself, or collecting applications on behalf of a third-party lender?** This is a compliance question, not just a feature question — installment lending is regulated in most jurisdictions. If the business is acting as a lender, that likely requires licensing review independent of the software. Flag this to the client directly; don't let "we'll figure it out later" slide into Phase 1 scope.
2. Will inventory be owned by the business, brokered, or supplied by partners? (Affects how vehicle data is managed and who confirms availability.)
3. Which countries will the platform serve at launch? (Affects currency, language, shipping logic, and the legal question above.)
4. Tech stack — confirm before any code is written (see Section 9).
5. Final company name and logo (needed for design system and copy).

### 🟡 Needed before Phase 2 (transactional features)
6. Payment provider(s) to integrate.
7. Shipping/logistics partners (for real tracking integration vs. manual status updates).
8. Minimum down payment and financing term options.
9. Interest rate structure (flat, amortized, etc.) — tied directly to question 1.
10. Rental pricing model.
11. Trade-in valuation process — manual admin judgment, a fixed formula, or a third-party valuation API?
12. Do customers receive the vehicle before or after final payment clears? (Major operational/risk decision.)

### 🟢 Can decide during or after Phase 1
13. Customer support hours.
14. Multi-language support — needed at launch or later?
15. Multi-currency support — needed at launch or later?
16. Launch as marketplace-only first, then layer in financing? (Worth revisiting once Phase 1 is live — may be the safer sequencing given question 1.)

---

## Summary for the Developer

Build Phase 1 only against this spec initially: marketplace, financing applications (no automated decisioning), jobs portal, basic admin, auth, core pages. Everything involving real money movement, real lending decisions, or third-party shipment APIs should wait until the Section 11 blocking questions are answered by the business owner — building those before the answers exist risks throwaway work.
