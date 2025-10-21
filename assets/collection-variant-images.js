/**
 * Collection Variant Images - Responsive product images based on selected color variants
 * 
 * Handles updating product card images when color facets are selected in collection views.
 * Works with the existing facets and color grouping systems.
 */

(function() {
  'use strict';

  // Color normalization mapping (matches facets-color-groups.js)
  function normalizeColorName(colorName) {
    if (!colorName) return '';
    const normalized = colorName.toLowerCase()
      .replace(/[\\s-_]/g, '')
      .normalize('NFD')
      .replace(/\\p{Diacritic}/gu, '');
    return normalized;
  }

  // Base color mapping for fallback matching
  function getBaseColor(colorName) {
    if (!colorName) return null;
    const n = normalizeColorName(colorName);
    
    // Norwegian + English mappings (same as facets-color-groups.js)
    if (/(svart|sort|black)/.test(n)) return 'svart';
    if (/(hvit|white)/.test(n)) return 'hvit';
    if (/(gra|grå|gray|grey|koks)/.test(n)) return 'gra';
    if (/(bla|blå|blue|navy|royal|kongebla|kongeblå|himmelbla|marine|turkis|cyan)/.test(n)) return 'bla';
    if (/(rod|rød|red|burgunder|vin)/.test(n)) return 'rod';
    if (/(gronn|grønn|green|lime|oliven|khaki)/.test(n)) return 'gronn';
    if (/(gul|yellow|mustard)/.test(n)) return 'gul';
    if (/(oransj|orange)/.test(n)) return 'oransje';
    if (/(lilla|fiolett|purple|violet)/.test(n)) return 'lilla';
    if (/(rosa|pink)/.test(n)) return 'rosa';
    if (/(brun|brown|camel|tan)/.test(n)) return 'brun';
    if (/(beige|sand|cream|ivory|bone)/.test(n)) return 'beige';
    if (/(multi|flerfarg|flerfarget|multicolor)/.test(n)) return 'multi';
    
    return normalizeColorName(colorName);
  }

  /**
   * Find the best matching media for a product based on selected colors
   * @param {HTMLElement} productCard - The product card element
   * @param {Array} selectedColors - Array of currently selected color filter values
   * @returns {string|null} - URL of the best matching image or null
   */
  function findBestImageForColors(productCard, selectedColors) {
    if (!selectedColors || selectedColors.length === 0) {
      return null; // Use default image
    }

    // Get all product images from any secondary image sources or data attributes
    const productWrapper = productCard.closest('.card-wrapper');
    const productImages = [];
    
    // Look for data attributes that might contain variant images
    const productData = productWrapper?.dataset;
    if (productData) {
      // Check for product tags or media data
      const productTags = productData.productTags || '';
      const productId = productWrapper.querySelector('[href*="/products/"]')?.href?.split('/products/')[1]?.split('?')[0];
      
      // If we have product media data, parse it
      if (window.productMediaData && window.productMediaData[productId]) {
        productImages.push(...window.productMediaData[productId]);
      }
    }

    // Get media from secondary image if available
    const secondaryImage = productCard.querySelector('.media img + img');
    if (secondaryImage) {
      productImages.push({
        src: secondaryImage.src,
        alt: secondaryImage.alt || '',
        srcset: secondaryImage.srcset || ''
      });
    }

    // Find best match
    for (const color of selectedColors) {
      const normalizedColor = normalizeColorName(color);
      const baseColor = getBaseColor(color);
      
      for (const image of productImages) {
        const altNormalized = normalizeColorName(image.alt);
        const srcNormalized = normalizeColorName(image.src);
        
        // Direct color match
        if (altNormalized.includes(normalizedColor) || srcNormalized.includes(normalizedColor)) {
          return image;
        }
        
        // Base color fallback
        if (baseColor && (altNormalized.includes(baseColor) || srcNormalized.includes(baseColor))) {
          return image;
        }
      }
    }

    return null;
  }

  /**
   * Update product card image based on selected colors
   * @param {HTMLElement} productCard - The product card element
   * @param {Array} selectedColors - Array of currently selected color filter values
   */
  function updateProductCardImage(productCard, selectedColors) {
    const primaryImage = productCard.querySelector('.card__media .media img');
    if (!primaryImage) return;

    // Store original image data if not already stored
    if (!primaryImage.dataset.originalSrc) {
      primaryImage.dataset.originalSrc = primaryImage.src;
      primaryImage.dataset.originalSrcset = primaryImage.srcset || '';
      primaryImage.dataset.originalAlt = primaryImage.alt || '';
    }

    const bestMatch = findBestImageForColors(productCard, selectedColors);
    
    if (bestMatch && bestMatch.src !== primaryImage.dataset.originalSrc) {
      // Update to variant image
      primaryImage.src = bestMatch.src;
      if (bestMatch.srcset) {
        primaryImage.srcset = bestMatch.srcset;
      }
      if (bestMatch.alt) {
        primaryImage.alt = bestMatch.alt;
      }
      primaryImage.classList.add('variant-image');
    } else {
      // Reset to original image
      primaryImage.src = primaryImage.dataset.originalSrc;
      primaryImage.srcset = primaryImage.dataset.originalSrcset;
      primaryImage.alt = primaryImage.dataset.originalAlt;
      primaryImage.classList.remove('variant-image');
    }
  }

  /**
   * Get currently selected color filter values
   * @returns {Array} Array of selected color values
   */
  function getSelectedColors() {
    const selectedColors = [];
    const colorInputs = document.querySelectorAll('input[name*="color"]:checked, input[data-filter-key="color"]:checked');
    
    colorInputs.forEach(input => {
      const value = input.value;
      if (value) {
        selectedColors.push(value);
      }
    });

    return selectedColors;
  }

  /**
   * Update all product cards with variant images based on current selections
   */
  function updateAllProductCards() {
    const selectedColors = getSelectedColors();
    const productCards = document.querySelectorAll('.card-product, .card--media, .card[class*="product"]');
    
    productCards.forEach(card => {
      updateProductCardImage(card, selectedColors);
    });
  }

  /**
   * Handle color group button clicks (from facets-color-groups.js)
   */
  function handleColorGroupClick(event) {
    const button = event.target;
    if (!button.classList.contains('kulkid-color-group__btn')) return;
    
    // Wait for the color inputs to be updated, then update product images
    setTimeout(updateAllProductCards, 50);
  }

  /**
   * Handle individual color facet changes
   */
  function handleColorFacetChange(event) {
    const input = event.target;
    if (input.type !== 'checkbox') return;
    
    // Check if this is a color filter
    const isColorFilter = input.name?.includes('color') || 
                         input.dataset.filterKey === 'color' ||
                         input.closest('[data-filter-key="color"]');
    
    if (isColorFilter) {
      setTimeout(updateAllProductCards, 50);
    }
  }

  /**
   * Handle facet updates (when new products are loaded via AJAX)
   */
  function handleFacetUpdate(event) {
    // Re-scan for new product cards and update them
    setTimeout(updateAllProductCards, 100);
  }

  /**
   * Initialize the collection variant images system
   */
  function init() {
    // Handle color group clicks
    document.addEventListener('click', handleColorGroupClick);
    
    // Handle individual color facet changes
    document.addEventListener('change', handleColorFacetChange);
    
    // Handle facet updates
    document.addEventListener('kulkid:facets:updated', handleFacetUpdate);
    
    // Initial update
    updateAllProductCards();
    
    console.log('🎨 Collection variant images initialized');
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();