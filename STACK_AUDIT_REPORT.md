# Stack Audit Report (WordPress-centric, 3-year reliability, 2-month delivery)

This report captures the technical due diligence and architecture assessment performed for the proposed platform stack (content-heavy corrective wellness platform with memberships, programmes, booking, video delivery, payments, and accounting automation).

## 1) Executive verdict

### Is the proposal technically sound as-is?

**Directionally sound for MVP**, but **under-specified** in the areas that determine long-term reliability:

- payment truth + reconciliation
- entitlement truth (membership access rules)
- webhook correctness and replay
- plugin boundaries and operational support

### Best stack for 3 years with minimal maintenance (and within ~2 months)

**WordPress + managed plugins + minimal custom code** is the lowest maintenance option, provided you enforce:

- **one source-of-truth** for access/entitlements
- **minimal plugin surface area**
- **staging + update policy**
- **CDN and caching**

If revenue split auditing and reliable accounting sync are contractual requirements, introduce a **thin custom integration layer** (small Laravel service) only for webhooks/ledger/retries. Everything else stays WordPress.

## 2) Core risks found (and their practical impact)

### Risk: No source-of-truth per domain

If payments, memberships, and access rules are split across WooCommerce + LifterLMS + Paystack, the system will drift under refunds, failed webhooks, manual order edits, and plugin updates.

- **Risk level**: High
- **Mitigation**: Declare one source-of-truth and make other systems read/derive from it.

### Risk: Split payments assumption (Paystack)

The proposal depends on Paystack splitting revenue (15%/10%) reliably.

- **Risk level**: High (financial integrity)
- **Mitigation**:
  - run an early “payment spike” in week 1
  - document exactly how split is configured
  - define refund/chargeback handling and reconciliation reporting

### Risk: Automation brittleness (Pabbly → QuickBooks)

No-code automation without event logs and retries becomes a support burden and can silently fail.

- **Risk level**: Medium–High
- **Mitigation**: treat as MVP-only; migrate to a small integration service or at least enforce audit logging + reconciliation checks.

### Risk: Security posture not specified

WordPress + plugins + admin accounts + payments on a VPS requires explicit hardening.

- **Risk level**: High
- **Mitigation**: WAF, least privilege, strong auth, backups, staging, monitoring, controlled updates.

## 3) Recommended 3-year architecture (low complexity)

### Preferred: WordPress (classic) + minimal glue

- **WordPress**: marketing, content, SEO, admin
- **Membership/programmes**: choose ONE:
  - **WooCommerce-first** (lowest commerce maintenance), OR
  - **LifterLMS-first** (best programme/progress delivery)
- **Cal.com**: bookings (embed/links; optional webhook ingestion later)
- **Bunny Stream**: video hosting/delivery (embed into lessons/pages)
- **Paystack**: payments via WooCommerce gateway plugin

### When to add a thin Laravel service (still low maintenance)

Add only if you need:

- auditable payment event ledger
- robust webhook replay and anomaly handling
- reliable QuickBooks sync with idempotent retries
- consistent entitlements under refunds/chargebacks

The Laravel service should be intentionally small: webhook receiver + event store + entitlement calculator + queue worker + admin view.

## 4) Plugin/dependency risk register (proposal items)

Legend:

- **Status**: Safe / Caution / Replace / Custom-build instead

| Item | Purpose | Status | Key risks | Recommended action |
|---|---|---|---|---|
| WordPress | CMS/admin/content | Safe | Plugin attack surface | Managed hosting + hardening + staged updates |
| WooCommerce | Orders/checkout | Caution | Complexity if overextended | Keep scope tight; use as payments truth if chosen |
| Paystack for WooCommerce | Paystack payments | Caution (sometimes Replace) | Plugin quality variance; webhook fragility | Validate plugin maturity; add custom webhook verifier if needed |
| LifterLMS | Programmes/progress/gating | Caution | Lock-in; customization limits | Use for LMS only; avoid making it integration hub |
| Cal.com Cloud | Booking | Safe | Vendor dependency | Keep as scheduling truth; embed + optional webhooks |
| Google Meet | Meeting links | Safe | OAuth/security if custom | Use Cal.com integration; avoid custom OAuth in WP |
| Bunny Stream | Video delivery | Safe | Vendor lock-in | Accept lock-in; it buys performance and reliability |
| Pabbly Connect | Automation to QuickBooks | Caution | Brittle; limited audit/retry | MVP-only; replace with custom integration layer if reliability required |
| QuickBooks | Accounting | Safe | Integration reliability | Prefer idempotent sync + reconciliation reports |
| Elementor | Page builder | Caution | Lock-in + performance | Optional; confine to marketing pages only |

## 5) Data strategy (source-of-truth)

Define one system as truth for each domain:

- **Content**: WordPress
- **Programme structure/content**: LifterLMS (if chosen)
- **Payments**: WooCommerce orders/subscriptions + Paystack as processor (or Paystack ledger if hybrid)
- **Bookings**: Cal.com
- **Entitlements**:
  - WooCommerce-first: membership derived from WC subscription/order states
  - LifterLMS-first: membership derived from LifterLMS access rules, with payment confirmation driving access grants

Avoid storing operational records in WP `postmeta` (payments/events/logs) beyond MVP.

## 6) Scaling strategy (3-year horizon)

- **CDN + Bunny** for video
- **Page caching** for public pages
- **Object cache (Redis)** if logged-in traffic grows
- **DB hygiene**: avoid unbounded meta growth; prefer structured tables for operational logs
- **Background jobs**:
  - if hybrid: queue worker for webhooks and accounting sync
  - if WP-only: minimize cron-heavy plugins; consider real cron and external monitoring
- **Observability**: webhook logs, payment anomaly alerts, basic operational dashboards

## 7) Timeline realism (2 months)

### Most realistic 2-month path (low maintenance)

Deliver an MVP that:

- sells memberships/programmes
- gates content
- supports booking
- has stable video delivery
- has a basic operational runbook

Cut/phase:

- real-time trainer dashboards
- deep analytics/reporting
- “fully automated accounting” beyond simple sync

## 8) Required proposal changes (before client-facing)

- Explicitly define sources-of-truth and failure modes
- Specify Paystack split feasibility and exact approach
- Replace “no developer needed” language with an honest ops model
- Add security/operations commitments (staging, backups, updates, WAF)
- Add Phase 2 roadmap for reliability + reporting upgrades

