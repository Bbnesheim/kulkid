# Phase 1 Audit Checklist – KUL KID v1.0

Use this doc as you validate the Phase 1 rollout (Search & Discovery, Klaviyo hooks, normalization). Tick each box in VS Code once verified.

## 1. Theme & Frontend Behavior
- [ ] `/collections/all` and representative category collection opened.
- [ ] Facet filters (Size, Color, Category, Price) render once per page load.
- [ ] Applying multiple filters updates the product grid dynamically without full-page reloads.
- [ ] Clearing filters restores the full product lineup.
- [ ] Mobile filter drawer shows the same facets and retains selections.
- [ ] `snippets/main-collection-product-grid.liquid` includes `data-dynamic-facets` attribute when filters bind correctly.

## 2. Related-Products Widget
- [ ] Product page shows “You might also like” (or equivalent) populated when API returns results.
- [ ] Empty API response triggers the localized fallback text from `locales/en.default.json` and `locales/nb.json`.
- [ ] Recommendation list contains no duplicate products.

## 3. Klaviyo Hooks & Metadata
- [ ] Product card DOM includes `data-product-tags` and related attributes.
- [ ] Newsletter/footer signup form includes `data-klaviyo`.
- [ ] Triggering signup dispatches `klaviyo_signup` event in DevTools.
- [ ] Add-to-cart interaction fires `klaviyo_purchase` (or equivalent) hooks.

## 4. Localization Audit
- [ ] Switching to Norwegian renders translated facet labels (“Størrelse”, “Farge”, “Pris”).
- [ ] `locales/en.default.json` and `locales/nb.json` contain the new strings (lines 23–40).

## 5. SEO & Structure
- [ ] Lighthouse SEO score is **≥ 95**.
- [ ] Collection templates render a single `<h1>` per view; product pages use product title as `<h1>`.
- [ ] View source confirms JSON-LD for `Product`, `BreadcrumbList`, and `Organization`.
- [ ] `<img>` elements include descriptive `alt` text.
- [ ] `robots.txt` blocks cart/checkout while allowing `/collections` and `/products`.

## 6. File Consistency
- [ ] `snapshot/test.txt` and `sync_kulkid_docs.py` removed from repo.
- [ ] New files present: `config/search_schema.json`, `docs/codex_launch_prompt.md`.
- [ ] `/assets/facets.js` (lines 156–275) contains normalization helpers.
- [ ] `/snippets/facets.liquid` and `/snippets/card-product.liquid` include data attributes and localization updates.

## 7. QA Outcome
- [ ] Phase 1 marked complete after all items pass.
- [ ] Release tagged: `git tag -a v1.0-phase1 -m "Phase 1 verified – Search & Discovery, Klaviyo hooks"` followed by `git push origin v1.0-phase1`.
