# 🚀 KULKID THEME REBUILD - MASTER ACTION PLAN

**Status:** Ready to Execute  
**Timeline:** ~5 hours total (spread over 1-2 days)  
**Goal:** Clean, working theme with functional variant switching, image galleries, and maintainable codebase

---

## **🛡️ SAFE DEPLOYMENT STRATEGY**

**Key Decision: DISCONNECT live theme from Git during rebuild**
- ✅ **Live theme stays untouched** during entire rebuild process
- ✅ **Build clean version in draft themes** only
- ✅ **Manual deployment** when everything perfect
- ✅ **Zero risk** to live site

**Git → Shopify Mapping:**
```bash
# During Rebuild:
"KULKID Live" (current)      →  [DISCONNECTED from Git - stays stable]
"KULKID Clean v2" (draft)    →  Our rebuild work (staging branch)
"Feature Tests" (draft)      →  Individual feature testing

# After Rebuild:
main (protected)             →  Manual deployment only
staging                     →  "KULKID Staging" theme
feature/*                   →  "Feature Tests" themes
```

---

## **PHASE 1: BACKUP & ASSESSMENT** ⏱️ 30 mins
**👤 Your Tasks**

### **A. Export Current Data & Disconnect**
```bash
# In Shopify Admin
1. Online Store → Themes → Live Theme → Actions → Export
2. Settings → Export theme settings to JSON  
3. Note down current app configurations
4. CRITICAL: Ensure live theme is NOT connected to GitHub/Git auto-deploy
```

### **B. Document What Works**
- ✅ **Brand styling** (colors, fonts, logos)
- ✅ **Working sections** (which custom sections actually work well?)
- ✅ **Essential pages** (which page templates are customized?)
- ✅ **Apps list** (Search & Discovery, Klaviyo, Printify, etc.)

### **C. Create Reference Screenshots**
- Homepage layout
- Product page (working vs broken parts)
- Collection page layout
- Key custom sections

**✅ COMPLETION CRITERIA:** 
- [ ] Theme exported and downloaded
- [ ] Settings JSON saved
- [ ] Working features documented
- [ ] Screenshots taken
- [ ] **CRITICAL:** Verified live theme is NOT auto-deploying from Git
- [ ] Current Git state tagged as "pre-rebuild-backup"

---

## **PHASE 2: CLEAN REPOSITORY SETUP** ⏱️ 45 mins
**🤖 My Tasks**

### **A. Repository Safety & Backup**
```bash
# I will execute:
# 1. First ensure current work is preserved
git add -A && git commit -m "FINAL BACKUP: Complete state before rebuild"
git tag "pre-rebuild-backup" # Tag for easy recovery

# 2. Create clean Dawn foundation
cd /tmp && git clone https://github.com/Shopify/dawn.git dawn-fresh
cd dawn-fresh && git checkout main
cd /home/ben/projects && mv kulkid kulkid-backup
mv /tmp/dawn-fresh kulkid && cd kulkid
```

### **B. Professional Git Structure**
```bash
# NEW Branch Strategy (Production-Safe):
main (protected)           # Stable code, manual deploy only
├── dawn-base             # Pristine Dawn reference
├── staging               # Pre-production testing ("KULKID Clean v2")
├── theme-custom          # Development branch
├── feature/*             # Individual features
└── hotfix/*              # Emergency fixes only

# Branch Protection Rules:
- main: Requires PR approval, no direct pushes
- staging: Automatic deployment to draft theme
- feature/*: Isolated testing environments
```

### **C. Development Tooling**
```bash
# Add proper .gitignore, Theme Check config
# Set up PR templates and development guidelines
# Configure branch protection rules
```

**✅ COMPLETION CRITERIA:**
- [ ] Clean Dawn repository created
- [ ] Proper branch structure established
- [ ] Development tooling configured
- [ ] Old chaotic repo backed up as kulkid-backup

---

## **PHASE 3: CONTENT PRESERVATION** ⏱️ 60 mins
**🤖 My Tasks**

### **A. Extract Valuable Assets**
```bash
# From kulkid-backup, extract:
- Brand CSS (colors, fonts, spacing)
- Working custom sections
- Essential snippets (non-broken ones)
- Brand assets (logos, icons)
- Translation files (locales/*.json)
```

### **B. Clean Migration List**
- ❌ **Remove**: debug-facets.js, custom global.js, broken facets.js
- ❌ **Remove**: Complex product-info.js modifications  
- ❌ **Remove**: Conflicting CSS overrides
- ✅ **Keep**: Brand styling, working sections, translations
- ✅ **Keep**: Essential integrations (Klaviyo setup, etc.)

### **C. Brand Integration Rules**
- **Typography**: "Luckiest Guy" for headings only
- **Colors**: Preserve brand color palette
- **Layout**: Keep working custom sections
- **Functionality**: Dawn defaults for all interactive elements

**✅ COMPLETION CRITERIA:**
- [ ] Essential assets extracted and catalogued
- [ ] Brand styling components identified
- [ ] Working sections documented
- [ ] Migration checklist created

---

## **PHASE 4: FRESH DAWN INTEGRATION** ⏱️ 90 mins
**👥 Collaborative**

### **A. Base Theme Setup** (My Task)
```bash
# Install fresh Dawn as DRAFT theme (NOT connected to live)
shopify theme push --unpublished --theme="KULKID Clean v2"
# This creates a completely separate draft theme for testing
```

### **B. Brand Styling Integration** (My Task)
```bash
# Apply ONLY essential branding:
- Colors and typography
- Logo and brand assets
- Basic layout adjustments
- "Luckiest Guy" font for headings
```

### **C. Section-by-Section Restoration** (Collaborative)
```bash
# Add custom sections ONE BY ONE:
1. Test homepage sections
2. Add product page customizations  
3. Test variant/image switching ✓
4. Add collection customizations
5. Test filtering ✓
6. Add footer/header mods
```

**✨ KEY PRINCIPLE: Test each addition immediately before moving to next**

**Testing Checklist per Section:**
- [ ] Section renders without errors
- [ ] No JavaScript console errors
- [ ] Mobile responsive
- [ ] Doesn't break existing functionality

**✅ COMPLETION CRITERIA:**
- [ ] Clean Dawn base theme deployed
- [ ] Brand styling applied and tested
- [ ] Each custom section added and verified
- [ ] Core functionality confirmed working

---

## **PHASE 5: APP & DATA RESTORATION** ⏱️ 45 mins
**👤 Your Tasks**

### **A. App Reconnections**
```bash
# In new clean theme:
1. Search & Discovery app → Configure filters
2. Klaviyo → Reconnect forms and flows
3. Printify → Verify product sync
4. Any other essential apps
```

### **B. Product Configuration**
```bash
# Verify in Shopify Admin:
1. Product variants have proper image assignments
2. Alt text follows consistent naming
3. Collection organization
4. SEO settings preserved
```

### **C. Settings Restoration**
```bash
# Apply theme settings from Phase 1 backup
1. Import theme settings JSON
2. Verify customizer options work
3. Test theme editor functionality
```

**✅ COMPLETION CRITERIA:**
- [ ] All essential apps reconnected and configured
- [ ] Product variants properly linked to images
- [ ] Theme settings restored from backup
- [ ] All integrations tested and working

---

## **PHASE 6: QUALITY ASSURANCE** ⏱️ 60 mins
**👥 Collaborative**

### **A. Functionality Testing**
- ✅ **Variant switching** (color/size selectors work)
- ✅ **Image galleries** (thumbnails clickable, zoom works)
- ✅ **Collection filtering** (Search & Discovery working)
- ✅ **Cart functionality** (add to cart, quantity updates)
- ✅ **Mobile responsiveness** (all features work on mobile)

### **B. Performance & SEO**
```bash
# Run audits:
shopify theme check --fail-level=error
# Lighthouse performance test
# Cross-browser testing
```

### **C. Launch Preparation**
```bash
# Final steps:
1. Theme settings comparison with backup
2. DNS/domain configuration check
3. Analytics verification
4. Launch checklist completion
```

**Testing Matrix:**
| Feature | Desktop | Mobile | Safari | Firefox | Chrome |
|---------|---------|---------|---------|----------|---------|
| Variant Selection | [ ] | [ ] | [ ] | [ ] | [ ] |
| Image Gallery | [ ] | [ ] | [ ] | [ ] | [ ] |
| Collection Filters | [ ] | [ ] | [ ] | [ ] | [ ] |
| Cart Functions | [ ] | [ ] | [ ] | [ ] | [ ] |
| Checkout Flow | [ ] | [ ] | [ ] | [ ] | [ ] |

**✅ COMPLETION CRITERIA:**
- [ ] All functionality tests passed
- [ ] Performance audit completed
- [ ] Cross-browser compatibility verified
- [ ] Ready for production deployment

---

## **🎯 SUCCESS CRITERIA**

**After this process, you will have:**
- ✅ **Working variant image switching** (Dawn default behavior)
- ✅ **Functional thumbnail gallery** (clickable, zoomable)  
- ✅ **Clean, maintainable codebase** (agents can understand)
- ✅ **Organized Git structure** (proper branching, no chaos)
- ✅ **Professional workflow** (Theme Check, PR templates, testing)
- ✅ **Preserved branding** (your design, but working functionality)

---

## **🚨 CRITICAL RULES**

1. **NO SHORTCUTS**: Each phase must be completed and tested before moving to next
2. **ONE CHANGE AT A TIME**: Add sections individually, test immediately  
3. **PRESERVE BACKUPS**: Never delete kulkid-backup until new theme is live
4. **DOCUMENT EVERYTHING**: Update this file with progress and findings
5. **TEST ON MOBILE**: Every change must work on mobile devices

---

## **📋 PROGRESS TRACKING**

### **Current Status:** [ ] Not Started

**Phase 1:** [ ] Not Started [ ] In Progress [ ] Complete  
**Phase 2:** [ ] Not Started [ ] In Progress [ ] Complete  
**Phase 3:** [ ] Not Started [ ] In Progress [ ] Complete  
**Phase 4:** [ ] Not Started [ ] In Progress [ ] Complete  
**Phase 5:** [ ] Not Started [ ] In Progress [ ] Complete  
**Phase 6:** [ ] Not Started [ ] In Progress [ ] Complete  

### **Notes & Findings:**
```
[Add progress updates, blockers, and key findings here as we work through each phase]
```

---

## **🆘 ROLLBACK PLAN**

If anything goes wrong:
1. **Immediate**: Switch back to current live theme
2. **Short-term**: Restore kulkid-backup repository  
3. **Long-term**: Continue with rebuild process, addressing identified issues

