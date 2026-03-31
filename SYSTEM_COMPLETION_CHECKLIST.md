# System Completion Checklist (WordPress + React)

This repo provides:

- A WordPress theme shell (`wordpress/wp-content/themes/wellness-solutions`) that mounts the React app.
- A Vite React app (`frontend/`) that can run standalone or build into the theme.
- A local Docker stack (`docker-compose.local.yml`) + scripts to boot WordPress locally.

What’s missing for a “complete system” is primarily **plugin + external-service configuration** and **API wiring**.

## Platform pages (WordPress)

These pages are created/updated by `scripts/local-wordpress-bootstrap.php` and all use the `Wellness App Shell` template (`page-app-shell.php`) so React can handle routing:

- `/wellness-app/` (main shell)
- `/login/`
- `/join/`
- `/dashboard/`
- `/programmes/`
- `/membership/`
- `/book/`
- `/movement-diagnostic/`

If you want traditional SEO marketing pages (non-app), create standard WP pages normally (no special template needed).

## Required plugin stack (from proposal)

### Must-have (WP plugins)

- **WooCommerce**
- **Paystack for WooCommerce** (for M-Pesa + card checkout; ensure it supports your desired settlement and webhook flow)
- **LifterLMS** (memberships + programmes + progress + gated content)

### Optional / depending on UX

- **Caching/security**: Cloudflare + a WP security plugin (your preference), plus backups.
- **Email deliverability**: SMTP plugin if you need reliable transactional email from WP.

### External services (not WP plugins)

- **Paystack**: configure products/pricing approach and **split payments** (15% CES / 85% WSK, then 10% after month 13).
- **Cal.com Cloud**: booking event types, availability, timezone settings, Google Calendar sync.
- **Google Meet**: Cal.com integration to auto-generate meeting links.
- **Bunny Stream**: host videos; embed inside LifterLMS lessons.
- **Pabbly Connect**: workflows Paystack → QuickBooks (and optionally WooCommerce → Brevo, etc.).
- **QuickBooks**: destination accounting system.
- **Google Workspace**: mailboxes + calendars.

## Data model templates (what to standardize)

You can implement these either via:

- LifterLMS entities (preferred for programmes + progress), and/or
- custom WordPress meta/options for app-specific fields.

### Roles (minimum)

- **ws_client**: end user/member
- **ws_trainer**: staff who can view client progress and notes
- **ws_admin**: operational admin (can manage content, members, bookings)
- *(optional)* **ws_corporate_contact**: corporate account/contact (B2B portal later)

### User profile fields (user meta)

Store as `user_meta` keys (examples):

- `ws_phone_e164`
- `ws_whatsapp_e164`
- `ws_timezone` (IANA string, e.g. `Africa/Nairobi`)
- `ws_country`
- `ws_city`
- `ws_last_assessment_at` (timestamp)
- `ws_calcom_email` / `ws_calcom_attendee_email` (if different)
- `ws_paystack_customer_code` (if you standardize it)

### Membership tier template

Define tiers as a canonical enum across WP + frontend:

- `basic_virtual`
- `hybrid`
- `premium`
- `elite_concierge`

The source of truth can be:

- LifterLMS “Memberships”, mapped to these tier IDs, OR
- WooCommerce subscription products, mapped to these tier IDs, OR
- a small WP option (`ws_membership_map`) that maps product IDs → tier IDs.

### Programmes template

Suggested programme IDs:

- `posture_reset`
- `pain_relief`
- `strong_feet_movement`

Each programme needs:

- duration (weeks), sessions count, deliverables
- included assessments (foot scan, posture assessment)
- content plan (lessons/videos/exercises)

Use LifterLMS courses/lessons to represent the structure and progress tracking.

### Booking template (Cal.com)

Standardize event type slugs:

- `movement-diagnostic`
- `virtual-session`
- `in-person-session`

Then store mapping in WP options:

- `ws_calcom_event_type_map = { "movement-diagnostic": "<cal_event_type_id>", ... }`

### Payments template (WooCommerce/Paystack)

Pick the “system of record” for payment status:

- WooCommerce order/subscription status (recommended if using Paystack gateway via WooCommerce)
- Paystack webhook events (used to validate/repair order status)

## API contract (what React expects)

The theme injects runtime config and points `apiBaseUrl` to:

- `/wp-json/wellness-solutions/v1`

### Implemented now (minimal)

- `GET /wp-json/wellness-solutions/v1/health` → `{ ok, service, timestamp }`
- `GET /wp-json/wellness-solutions/v1/config` → `{ restNamespace, restBaseUrl, siteUrl, themeUrl }`
- `GET /wp-json/wellness-solutions/v1/me` (auth required) → `{ id, email, displayName, roles }`

### Next endpoints to implement (recommended order)

- **Membership & access**
  - `GET /membership/status` → tier + entitlements + renewal dates
- **Programmes**
  - `GET /programmes` → list programmes available for current tier
  - `GET /programmes/{id}` → lessons/exercises/progress summary
- **Bookings**
  - `GET /bookings/links` → Cal.com booking URLs per event type
  - *(optional)* `POST /bookings/webhook` → receive booking events (if you want WP to be the central log)
- **Payments**
  - `POST /payments/webhook/paystack` → verify signature, update WooCommerce/LifterLMS access
- **Progress**
  - `POST /progress/checkin` → lightweight “check-in” outside LifterLMS, if needed

## Setup checklist (step-by-step)

### A) Local development preview (this repo)

- [ ] `cp .env.wordpress.example .env.wordpress`
- [ ] `bash scripts/local-wordpress-up.sh`
- [ ] Open:
  - [ ] `http://127.0.0.1:8090/`
  - [ ] `http://127.0.0.1:8090/wp-admin/`
  - [ ] `http://127.0.0.1:8090/wellness-app/`
  - [ ] `http://127.0.0.1:8090/programmes/` *(shell page)*

### B) WordPress plugin install/config (core)

- [ ] Install + activate **WooCommerce**
  - [ ] configure base currency (KES), taxes, checkout
- [ ] Install + activate **Paystack for WooCommerce**
  - [ ] set Paystack keys (test + live)
  - [ ] enable M-Pesa where applicable
  - [ ] confirm webhook endpoint and events
  - [ ] confirm split payments feasibility (Paystack subaccounts / splits) and settlement rules
- [ ] Install + activate **LifterLMS**
  - [ ] define memberships (tiers)
  - [ ] define courses/programmes and drip rules (if any)
  - [ ] gate video lessons by membership/course access

### C) External services

- [ ] **Paystack**
  - [ ] create/configure subaccount for CES
  - [ ] configure split to CES (15% year 1, 10% after month 13)
  - [ ] document exact Paystack split configuration used
- [ ] **Cal.com**
  - [ ] connect Google Calendar
  - [ ] connect Google Meet
  - [ ] create event types (diagnostic, virtual, in-person)
  - [ ] set reminders + timezone behaviour
- [ ] **Bunny Stream**
  - [ ] upload first batch videos
  - [ ] create embedding approach (iframe/player) used in LifterLMS lessons
- [ ] **Pabbly Connect → QuickBooks**
  - [ ] workflow: Paystack payment succeeded → QuickBooks sale/receipt
  - [ ] workflow: refunds/chargebacks handling (if needed)

### D) App wiring tasks (to complete)

- [ ] Decide the **source of truth** for access: WooCommerce vs LifterLMS (or hybrid)
- [ ] Implement the missing REST endpoints listed above
- [ ] Update React to call those endpoints and render:
  - [ ] membership tier + billing status
  - [ ] programmes + progress
  - [ ] booking links/widgets
- [ ] Add admin dashboards (WP admin pages or React admin routes) for staff workflows

