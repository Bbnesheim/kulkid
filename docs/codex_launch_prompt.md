# KUL KID Fast GO LIVE – Codex Prompt

## How to Use
- Open Codex (VS Code, CLI, or web workspace) and paste the full prompt below.
- Keep Shopify CLI authenticated with production access; all commands assume the local repo `Bbnesheim/kulkid`.
- Focus work on the root theme files (outside `/kulkid/` subdirectory); that nested repo is a historical snapshot only.

## @prompt – Fast GO LIVE Execution (for Codex)

**Context**  
Store: `kulkid.no` (production)  
Theme target: current `main` branch → publish as Live  
Integrations: Vipps, Klarna, Klaviyo, GA4, Meta Pixel, TikTok Pixel, Printful  
Launch window: `2025-10-16 21:00 CET`  
Objective: finalize the storefront, remove password, and verify checkout/analytics within the go-live window.

**Ground Rules**  
- Treat `/sections`, `/snippets`, `/assets`, `/templates`, `/config`, `/locales`, `/docs/AGENTS.md` as protected; edit only when needed for launch fixes.  
- Avoid touching the archived `/kulkid/*` tree.  
- No new heavy automation runs (Lighthouse etc.) unless expressly requested; time is limited.  
- Log every theme or settings change in `docs/post_launch_notes.md` once created.

### Phase 0 – Theme Freeze & QA (T-3h → T-90m)
- Ensure `git status --short` is clean and synced with `origin/main`; flag if anything unexpected appears.
- Run `shopify theme check --fail-level=warning`; resolve blocking errors immediately.
- Perform smoke tests on key templates (`/`, `/collections/nyheter`, `/products/<launch-hero>`, `/cart`, `/pages/personvern`) across:
  - iPhone 13 Safari
  - Pixel 7 Chrome
  - MacBook Safari + Chrome
- Scrub console warnings/`console.log` leftovers in `assets/global.js`, `assets/cart*.js`, and critical sections/snippets.
- Confirm launch content:
  - Announcement bar copy references launch offer.
  - Homepage hero CTA points to an in-stock collection.
  - Localized strings exist in both `locales/en.default.json` and `locales/nb.json`.
- Create a fresh live backup: `shopify theme pull --environment=production --theme Live --path snapshot/live-theme-backup`.

### Phase 1 – Checkout & Integrations (T-90m → T-30m)
- Run three test checkouts (Vipps, Klarna, Card) using Shopify test modes, then cancel/refund.
- Validate shipping matrix for Norway + EU at price breaks `<500`, `500-1500`, `>1500` NOK.
- Export an inventory snapshot (CSV) for rollback.
- Confirm analytics instrumentation:
  - GA4 debug view shows page_view + add_to_cart exactly once.
  - Meta Pixel helper shows PageView + InitiateCheckout.
  - TikTok Pixel helper shows PageView.
- Verify Klaviyo:
  - Public key set in the onsite script.
  - Flows (Welcome, Post-Purchase, Winback) active and pointing to production lists.
- Spot-check legal copy (Privacy, Terms, Shipping & Returns) for up-to-date policies.

### Phase 2 – Launch Execution & Monitoring (T-15m → T+2h)
- Publish the `main` theme as Live (keep previous live theme duplicated as rollback option).
- Disable storefront password; confirm incognito session reaches homepage.
- Force-refresh hero assets with `?launch` query to bust CDN cache.
- Place a low-value live order (hidden 1 NOK product); check:
  - Order emails/SMS trigger correctly.
  - Payment providers capture and can refund.
- Watch analytics dashboards for spikes or errors (GA4 real-time, Meta Events Manager, Shopify Live View).
- Post launch announcement copy to newsletter + social queue (template ready in marketing drive).
- Set monitoring reminders at T+15m, T+60m, and T+120m to review support inbox, error logs, payment dashboards.

### Phase 3 – Post-Launch Follow-up (T+2h → T+24h)
- Create `/docs/post_launch_notes.md` with sections: traffic_summary, conversion_metrics, customer_feedback, follow_up_actions.
- Document any hotfixes applied and tag tasks in the backlog as `launch-followup`.
- Update KPI tracker with launch-day metrics.

**Output Expectations**
- Theme live without password, checkout verified, analytics firing once.
- `snapshot/live-theme-backup` contains latest pre-launch export.
- `docs/post_launch_notes.md` created and filled during monitoring window.
- Repo remains clean (`git status` empty) after each major step.

---

## Commit Message Template
```
chore(launch): fast go-live readiness

- freeze theme and resolve pre-launch blockers
- verify payments, shipping, and analytics instrumentation
- publish theme and document monitoring actions
```

## Definition of Done Checklist
- [ ] Live theme published from `main`; previous live theme duplicated as rollback.
- [ ] Password page disabled and storefront accessible in incognito.
- [ ] Vipps, Klarna, and Card test orders placed and refunded; shipping matrix verified.
- [ ] GA4, Meta, and TikTok pixels fire once per event post-launch.
- [ ] Launch announcement copy dispatched; support/montoring schedule logged.
- [ ] `/docs/post_launch_notes.md` created with initial entries.
- [ ] Working tree clean (`git status` empty) and pushed to `origin/main`.
