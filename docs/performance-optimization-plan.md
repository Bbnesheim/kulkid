# Performance Optimization Action Plan

Based on Lighthouse audit results (Performance Score: 46/100)

## Critical Issues Identified

### 🔴 **High Priority** (Immediate Impact)
1. **Unused JavaScript: 263KB** - Major savings opportunity
2. **Unused CSS: 142KB** - Significant reduction possible  
3. **Server Response Time: 1,080ms** - Far above optimal (<200ms)
4. **First Contentful Paint: 7.5s** - Should be <1.8s
5. **Largest Contentful Paint: 15.2s** - Should be <2.5s

### 🟡 **Medium Priority** (Performance Gains)
6. **Total Blocking Time: 380ms** - Should be <200ms
7. **Unminified CSS: 33KB** - Easy compression wins
8. **Unminified JS: 21KB** - Quick optimization

## Action Plan by Priority

### Phase 1: Quick Wins (1-2 days)

#### 1. Asset Optimization
- **Minify CSS/JS**: Use Shopify's built-in asset pipeline
- **Remove unused CSS**: Audit and clean up unused styles (142KB savings)
- **Remove unused JS**: Clean up unused JavaScript (263KB savings)

#### 2. Script Loading Optimization
- **Defer non-critical JS**: Add `defer` attributes to scripts
- **Async load secondary features**: Cart, search, product variants
- **Move scripts to bottom**: Ensure CSS loads first

#### 3. CSS Delivery Optimization
- **Inline critical CSS**: Extract above-the-fold styles
- **Defer non-critical CSS**: Load remaining styles asynchronously
- **Optimize base.css**: Split 80KB base.css into critical/non-critical

### Phase 2: Core Performance (3-5 days)

#### 4. Lazy Loading Implementation
- **Images**: Implement native lazy loading for all images
- **Below-fold sections**: Lazy load non-critical sections
- **Product grids**: Progressive loading for collection pages

#### 5. Resource Preloading
- **Critical fonts**: Preload used fonts
- **Hero images**: Preload above-the-fold images
- **Key resources**: DNS prefetch for external services

#### 6. JavaScript Optimization
- **Code splitting**: Break large JS files into modules
- **Module loading**: Use ES6 modules where possible
- **Remove unused features**: Audit global.js (56KB) and product-info.js (24KB)

### Phase 3: Server Optimization (5-7 days)

#### 7. Liquid Template Optimization
- **Reduce API calls**: Minimize product/collection queries
- **Cache expensive operations**: Use Liquid variables effectively
- **Optimize loops**: Review collection/product iteration logic
- **Remove unused includes**: Clean up snippet usage

#### 8. Image Optimization
- **WebP format**: Convert images to WebP where supported
- **Responsive images**: Implement srcset for different screen sizes
- **Compression**: Optimize existing images without quality loss

### Phase 4: Advanced Optimization (Ongoing)

#### 9. Caching Strategy
- **Browser caching**: Optimize cache headers
- **CDN optimization**: Leverage Shopify's CDN effectively
- **Service worker**: Consider for repeat visitors

#### 10. Third-party Scripts
- **Audit external scripts**: Review analytics, chat widgets, etc.
- **Load timing**: Defer non-essential third-party content

## Implementation Commands

### Minification Check
```bash
# Check for minified assets
find assets -name "*.min.css" -o -name "*.min.js"
```

### Theme Check (Before/After)
```bash
# Run theme check to catch issues
shopify theme check --fail-level=warning
```

### Performance Testing
```bash
# Re-run Lighthouse after each phase
lighthouse http://127.0.0.1:9292 --only-categories=performance --chrome-flags="--headless --no-sandbox"
```

## Success Metrics

### Target Performance Goals
- **Performance Score**: 46 → 80+ (75% improvement)
- **FCP**: 7.5s → <1.8s (76% improvement)
- **LCP**: 15.2s → <2.5s (84% improvement)  
- **TBT**: 380ms → <200ms (47% improvement)
- **Server Response**: 1,080ms → <500ms (54% improvement)

### Phase Targets
- **Phase 1**: Score 46 → 60 (Asset optimization)
- **Phase 2**: Score 60 → 75 (Loading optimization) 
- **Phase 3**: Score 75 → 80+ (Server optimization)

## File Priority List

### High Impact Files (Optimize First)
1. `assets/base.css` (80KB) - Split critical/non-critical
2. `assets/global.js` (56KB) - Remove unused code
3. `assets/section-main-product.css` (32KB) - Product page critical
4. `assets/product-info.js` (24KB) - Defer if not above-fold

### Medium Impact Files  
5. `assets/facets.js` (24KB) - Collection page specific
6. `assets/component-facets.css` (28KB) - Collection page specific
7. `assets/quick-order-list.js` (20KB) - Feature-specific, can defer

## Next Steps
1. ✅ Run initial audit
2. ✅ Create optimization plan
3. 🔄 Begin Phase 1 implementation
4. 📊 Test after each phase
5. 📈 Monitor ongoing performance

---
*Last updated: $(date)*
*Lighthouse report: docs/perf/lighthouse-performance-20251021_021037.json*