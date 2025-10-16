# Phase 2 Audit Checklist – Klaviyo Integration

Use this list to validate the Klaviyo rollout once implementation work lands. Tick each item as you confirm behaviour in the live theme or preview.

## 1. Onsite Script & Config
- [ ] `layout/theme.liquid` injects Klaviyo onsite script before `</body>` with the production `company_id`.
- [ ] `config/klaviyo.json` exists with the correct public key plus the documented flows (Welcome Series, First Purchase, Winback).
- [ ] Shopify theme settings (`config/settings_data.json`) reference any Klaviyo sections/blocks that should render in the storefront.

## 2. Form Instrumentation
- [ ] Newsletter, footer, popup, and checkout intercept forms include `data-klaviyo` attributes and per-form identifiers.
- [ ] Each form posts to the expected endpoint (Shopify customer endpoint for sync or Klaviyo hosted endpoint) without throwing browser console errors.
- [ ] Successful submits display localized success copy and track the subscriber status (Shopify customer tag or Klaviyo list membership).

## 3. Event Hooks & Tracking
- [ ] `assets/global.js` (or dedicated modules) dispatch `window.dispatchEvent(new CustomEvent('klaviyo_signup', {...}))` on signup success.
- [ ] Cart and checkout triggers dispatch purchase-intent events (`klaviyo_add_to_cart`, `klaviyo_purchase`, etc.) with product metadata (handle, variant, price).
- [ ] DevTools → Network confirms payloads to Klaviyo (`collect`, `identify`, or `events`) fire when events dispatch.
- [ ] Events respect localization (no hard-coded English strings in payload labels).

## 4. Data Layer & Metadata
- [ ] Product cards and cart lines expose `data-product-*` attributes for tags, collections, price, and inventory that Klaviyo scripts can consume.
- [ ] Customer data hydration (email, name) is available to Klaviyo onsite script for logged-in users (`_learnq` identify call present).
- [ ] Product detail pages include Klaviyo view tracking (e.g., `_learnq.push(['track', 'Viewed Product', {...}])`).

## 5. Flow Verification
- [ ] Test signup (`contact@nesheimvatten.no`) appears in the Klaviyo list/segment within 5 minutes.
- [ ] Welcome Series email triggers with correct branding and unsubscribe footer.
- [ ] First Purchase automation captures order metadata from Shopify (total, items) and enters customer into the proper flow.
- [ ] Winback flow exits correctly when a customer repurchases.

## 6. Analytics & Reporting
- [ ] Klaviyo dashboard event timelines show the new onsite events with accurate timestamps.
- [ ] No duplicate profiles or unidentified events appear in Klaviyo (check Profiles → Recent Activity).
- [ ] UTM parameters persist from signup to checkout so Klaviyo attribution matches Shopify analytics.

## 7. QA Outcome
- [ ] Document screenshots/logs of script tag, Network captures, and Klaviyo flows in `/docs/qa/phase2`.
- [ ] Mark Phase 2 complete and prepare changelog entry summarizing Klaviyo integration.
- [ ] Tag release `v1.0-phase2` once all items pass.
