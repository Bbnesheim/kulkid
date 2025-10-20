# Launch Action Plan (Kulkid)

This plan focuses on footer (main-footer.liquid), the “Nyhetsbrev” signup, Klaviyo integrations, and collection filtering/sorting. It includes preflight checks, implementation steps, and QA.

## 0) Preflight and backups
- Create live backup (production):
  ```sh path=null start=null
  shopify theme pull --environment=production --theme Live --path snapshot/live-theme-backup
  ```
- Verify working branch is up to date and clean:
  ```sh path=null start=null
  git --no-pager status -sb
  ```
- Lint with Theme Check (fix CLI issue if present):
  ```sh path=null start=null
  shopify theme check --fail-level=warning
  ```
  - If the CLI errors about a missing module in theme-check config extends, resolve the extends entry (e.g., install missing pack, or change extends to a local preset).

## 1) Footer (main-footer.liquid) – newsletter and SVG icons
- Newsletter
  - Current behavior: footer newsletter uses `{% form 'customer' %}` (Shopify Customer Marketing list). It now properly renders success/error states (updated).
  - Decision: use Shopify list or Klaviyo? If Klaviyo is required, implement one of:
    - Option A: Klaviyo embedded form (recommended for lowest risk). Add Klaviyo’s embed script and container into the footer newsletter block, styled to match.
    - Option B: Post to Klaviyo Subscribe API (requires public key, list ID; show localized success/error).
  - Copy/Locales: ensure placeholders and messages are translated in `locales/en.default.json` and `locales/nb.json`.
- SVG social icons
  - Verify required icon snippets exist: `snippets/icon-instagram.liquid`, `icon-facebook.liquid`, `icon-tiktok.liquid`, `icon-spotify.liquid`, `icon-youtube.liquid`.
  - If using custom image icons, confirm assets resolve and have alt text. Confirm brand colors via CSS vars in the footer.

## 2) Map all newsletter/email signups to Klaviyo
Identify and standardize all signup points:
- Sections:
  - `sections/main-footer.liquid` (Nyhetsbrev block)
  - `sections/newsletter.liquid`
  - `sections/email-signup-banner.liquid`
- For each, choose integration (embed vs API). Required data:
  - {{KLAVIYO_PUBLIC_KEY}} and target list ID(s)
  - Double opt-in preference
  - Success message copy and redirect behavior
Implementation checklist:
- Add Klaviyo script/embed or API post for each section’s form.
- Ensure success/error messages render inline, accessible, and localized.
- Tag contacts (e.g., `newsletter`) for segmentation.
- QA with test emails and confirm profiles appear in Klaviyo list, flows trigger.

## 3) Collection filtering and sorting audit
- Files:
  - `sections/main-collection-product-grid.liquid` (wires filters)
  - `snippets/facets.liquid` (+ `assets/facets.js`)
- Tests (desktop/mobile):
  - Filtering by size/color/category and removing filters
  - Price range filter
  - Sorting via select (vertical, horizontal, and drawer modes)
  - URL param persistence and back/forward navigation
  - Product count updates and loading states
- Accessibility
  - Focus order within filter drawer
  - ARIA attributes on summary/details and facet pills
- Performance
  - Ensure facets.js only loads once, no console errors

## 4) UX polish (key items)
- Footer newsletter card: responsive spacing, button label casing, and consistent typography.
- Success/error state announcements: ensure screen readers receive feedback via `aria-describedby` and focus management.
- Social links: open in new tab with `rel="noopener noreferrer"`.
- Cookie, contact, and legal links: verify targets and labels in `footer-group.json`/Theme Editor.

## 5) QA scenarios (staging/preview)
- Newsletter signup
  - Valid email signup → success message visible; appears in Klaviyo (if Klaviyo chosen)
  - Invalid email → inline error, input `aria-invalid=true`
  - Duplicate email → friendly message (no crash)
- Collection filters/sort
  - Combine multiple filters, paginate, then clear all
  - Mobile drawer apply/close cycles
- Visuals
  - Footer gradient on/off toggle
  - Social icons brand coloring and hover behavior

## 6) Launch execution
- Final Theme Check and quick visual pass
- Push theme draft:
  ```sh path=null start=null
  shopify theme push --assume-yes
  ```
- Open preview and run smoke tests:
  ```sh path=null start=null
  shopify theme open
  ```
- Publish when approved:
  ```sh path=null start=null
  shopify theme push --publish --assume-yes
  ```

## 7) Post-launch
- Real-time monitoring of checkout, error logs, and analytics (GA4/Meta/TikTok)
- Verify Klaviyo signups and flows in production
- Capture issues into a Day 2 backlog

## Open items to confirm with stakeholders
- Klaviyo vs Shopify list as the system of record for newsletter
- Final copy for success/error messages (NB + EN)
- Target lists, tags, and double opt-in configuration
- Any gated collections needing custom facet labels
