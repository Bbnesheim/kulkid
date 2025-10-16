# KUL KID Launch Optimization – Codex Prompt

## How to Use
- Open your Codex session (VS Code, Codex CLI, or web workspace).
- Copy the full prompt below and paste it into the assistant to kick off the automation.
- Keep Shopify theme access ready; Codex will operate against the local repo cloned from `Bbnesheim/kulkid`.

## @prompt – KUL KID Launch Optimization (for Codex)

**Context**  
Shopify store: `kulkid.no`  
Theme: `Dawn (customized)`  
Repo: `Bbnesheim/kulkid`  
Apps: Shopify Search & Discovery, Klaviyo, Printful, Klarna, Vipps

**Theme Snapshot**  
- JSON templates drive pages (`templates/product.json`, collection-specific JSON templates) with core sections in `sections/main-product.liquid`, `sections/main-collection-product-grid.liquid`, `sections/main-search.liquid`, and `sections/related-products.liquid`.  
- Variant option naming mixes Norwegian and English (`Str.`, `Str`, `Size`, `Farge`, `Color`, `Farge:`); harmonize to power consistent filters.  
- Fonts: body `Quicksand`, headings `Nunito Sans`, plus Google `Luckiest Guy` load in `layout/theme.liquid`.  
- Primary newsletter touchpoints live in `sections/footer.liquid` (`ContactFooter` form), `sections/newsletter.liquid`, and `sections/email-signup-banner.liquid`.  
- Core scripts/CSS for filters and product data live in `assets/facets.js`, `assets/main-search.js`, `assets/global.js`, `assets/base.css`, and `assets/section-related-products.css`.
- Repository contains a legacy snapshot under `/kulkid/*`; run Codex tasks against the root theme files (outside the nested directory) to avoid editing stale copies.
- High-level automation phases already live in `codex_launch_plan.yaml`; keep this prompt in sync if that roadmap evolves.

**Goal**  
Prepare kulkid.no for public launch by implementing SEO-optimal structure, Search & Discovery app integration, and technical improvements that enhance speed, discoverability, and data readiness for Klaviyo and analytics tools.

### 1. Shopify Search & Discovery Integration
- Enable full integration of Shopify Search & Discovery with custom filters, sorting, and product recommendations (update `sections/main-collection-product-grid.liquid`, `sections/main-search.liquid`, `templates/search.json`, and `snippets/facets.liquid`).
- Normalize option and facet labels (map `Str.`, `Str`, `Sizes (Kids)` ➝ Size; `Farge`, `Farge:` ➝ Color) before surfacing them with the `facets` API; expose Size, Color, Category, and Price filters, plus high-value tags such as `baby`, `nyhet`, and personalization flags.
- Hook app-powered recommendations into `sections/related-products.liquid` using `routes.product_recommendations_url` with fallback messaging when the API has no results.
- Surface metafield-filtered data (theme motifs, print type, age range) in filter UI and product cards once metafields are published; validate against `snapshot/kulkid_live_dump.json`.

### 2. SEO & Code Optimization
- Audit JSON templates (`templates/product.json`, `templates/index.json`, all `templates/collection.*.json`, `templates/search.json`) and their referenced sections (`sections/main-product.liquid`, `sections/main-collection-product-grid.liquid`, `sections/main-search.liquid`, landing page sections) for semantic heading hierarchy (`<h1>` per template, descriptive `<h2>` blocks).
- Inject JSON-LD snippets via `snippets/meta-tags.liquid` and/or new dedicated schema snippets for Product (name, description, price, availability, SKU, brand), BreadcrumbList, and Organization; ensure PDP schema reflects Norwegian locale currency and inventory.
- Guarantee all Liquid `image_tag` helpers populate `alt` text (`product.featured_image.alt`, fall back to `product.title` + option); sweep `sections/` and `snippets/` to cover placeholders.
- Create meta title/description fallbacks in `layout/theme.liquid` + `snippets/meta-tags.liquid` (use collection description, page excerpts, or sensible defaults when admin fields are blank).
- Defer or conditionally load non-critical scripts (`animations.js`, `main-search.js`, `quick-add*.js`) and apply `loading="lazy"`/`fetchpriority` tweaks where safe; remove unused snippets or duplicate stylesheet tags discovered in `sections/`.

### 3. Performance Optimization
- Extract and inline critical CSS for the fold (hero + header) from `assets/base.css`/`assets/section-image-banner.css`; lazy-load the remaining bundle.
- Preload `Nunito Sans`, `Quicksand`, and Google `Luckiest Guy` (add `<link rel="preload" as="font">` in `layout/theme.liquid`, ensure `font-display: swap/fallback` config prevents FOUT).
- Add/pre-verify `preconnect`/`dns-prefetch` for `cdn.shopify.com`, `fonts.shopifycdn.com`, `fonts.googleapis.com`, `cdn.jsdelivr.net`, and any image CDN used by Printful mockups.
- Run Lighthouse and Shopify Theme Inspector; target Performance > 90 and SEO > 95 with evidence captured in `/docs/perf/`.

### 4. Klaviyo Signup & First-Purchase Hooks
- Add `data-klaviyo` instrumentation to `sections/footer.liquid` (form `ContactFooter`), `sections/newsletter.liquid` (form `NewsletterForm`), `sections/email-signup-banner.liquid`, and any popup snippet; include cart CTA hooks in `sections/cart-drawer.liquid`, `sections/main-cart-items.liquid`, and dynamic checkout buttons.
- Dispatch `window.dispatchEvent(new CustomEvent("klaviyo_signup", {...}))` on AJAX success paths in `assets/global.js` (newsletter) and `assets/cart.js`/`assets/cart-drawer.js` for cart actions; fire `klaviyo_purchase` post-order (confirmation template or additional script).
- Convert any full-page form submits to AJAX (use Shopify `fetch` endpoints or `Shopify.postLink` replacement) and surface localized success/error messaging without reloads.
- Ensure newsletter forms create/update customers (`contact[tags]=newsletter`) so Klaviyo sync automatically ingests profiles.

### 5. Analytics & Meta Pixel QA
- Audit `layout/theme.liquid` and any custom analytics snippets for GA4, Meta Pixel, TikTok Pixel, Vipps/Klarna scripts; document IDs in `/docs/analytics.md`.
- Validate event coverage (page view, view_item, add_to_cart, begin_checkout, purchase) using browser dev tools + Pixel Helper; ensure server-side Conversions API (if enabled via Shopify) mirrors browser events exactly once.
- Inspect post-purchase/thank-you templates for redundant script inclusions; consolidate into a single snippet to avoid double fires.

### 6. General Cleanup
- Minify/compress custom assets (focus on `assets/global.js`, `assets/main-search.js`, `assets/section-related-products.css`) and remove unused SVGs/icons.
- Purge test snippets, console logs, and commented code across `sections/`, `snippets/`, and `assets/`.
- Confirm `robots.txt` rules allow product/collection crawling but block `cart`, `checkout`, `account`; update sitemap references and submit to Google Search Console.


**Expected Outcome**  
- Search & Discovery integration live with filters, recommendations, and dynamic facets.  
- SEO and schema enhancements across primary templates.  
- Lighthouse SEO score ≥95 and Performance ≥90.  
- Klaviyo event hooks functioning for signup and purchase tracking.  
- Theme cleaned and optimized, ready for launch and pushed to `main`.

---

## Commit Message Template
```
feat: launch optimizations for KUL KID theme

- integrate Shopify Search & Discovery facets and recommendations
- add JSON-LD, meta fallbacks, and semantic HTML updates
- optimize performance assets and analytics/Klaviyo hooks

Refs: kulkid-launch
```

## Definition of Done Checklist
- [ ] Search & Discovery facets expose Size/Color/Category/Price with normalized option labels (`Str.`/`Farge` mapped) and recommendations render on PDPs with fallbacks.
- [ ] JSON-LD (`Product`, `BreadcrumbList`, `Organization`) validated via Rich Results Test; product schema reflects NOK prices and availability.
- [ ] Primary templates (`templates/*.json` + sections) have single `<h1>`, logical `<h2>`, and populated `alt` attributes across key images.
- [ ] Meta title/description fallbacks verified in theme preview when admin values are empty; `meta-tags` outputs localized descriptions.
- [ ] Critical CSS + font preloads applied in `layout/theme.liquid`; Lighthouse Performance ≥90 and SEO ≥95 with evidence in `/docs/perf/`.
- [ ] Klaviyo `klaviyo_signup` and `klaviyo_purchase` events observed in browser dev tools; newsletter/cart forms carry `data-klaviyo` attributes and submit via AJAX.
- [ ] GA4, Meta Pixel, TikTok Pixel, and Conversions API audited (IDs documented in `/docs/analytics.md`) with no duplicate purchase events.
- [ ] Asset cleanup complete (`assets/global.js`, `assets/main-search.js`, `sections/*`) with no console logs or dead code; new bundles minified.
- [ ] Robots.txt + sitemap meet launch requirements; Google Search Console test passes.
- [ ] Changes reviewed and merged to `main` in `Bbnesheim/kulkid`.
