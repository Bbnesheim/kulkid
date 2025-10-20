// Debug helper for facets and variants
(function() {
  console.log('=== KULKID Debug Info ===');
  
  // Check facets
  const facetForms = document.querySelectorAll('facet-filters-form');
  console.log('Facet forms found:', facetForms.length);
  facetForms.forEach((form, i) => {
    console.log(`Form ${i}:`, {
      hasForm: !!form.querySelector('form'),
      formId: form.querySelector('form')?.id,
      inputs: form.querySelectorAll('input[type="checkbox"]').length,
      selects: form.querySelectorAll('select').length
    });
  });
  
  // Check variant selects
  const variantSelects = document.querySelectorAll('variant-selects');
  console.log('Variant selects found:', variantSelects.length);
  variantSelects.forEach((vs, i) => {
    console.log(`Variant Select ${i}:`, {
      selects: vs.querySelectorAll('select').length,
      radios: vs.querySelectorAll('input[type="radio"]').length,
      selectedVariant: vs.querySelector('[data-selected-variant]')?.textContent
    });
  });
  
  // Check media gallery
  const mediaGallery = document.querySelector('media-gallery');
  if (mediaGallery) {
    console.log('Media Gallery:', {
      exists: true,
      hasSetActiveMedia: typeof mediaGallery.setActiveMedia === 'function',
      thumbnails: mediaGallery.querySelectorAll('[data-target]').length,
      activeMedia: mediaGallery.querySelector('.is-active')?.dataset?.mediaId
    });
  }
  
  // Check product info
  const productInfo = document.querySelector('product-info');
  if (productInfo) {
    console.log('Product Info:', {
      exists: true,
      hasUpdateMedia: typeof productInfo.updateMedia === 'function',
      variantSelectors: !!productInfo.querySelector('variant-selects')
    });
  }
  
  // Check if FacetFiltersForm is customElement
  console.log('FacetFiltersForm defined:', customElements.get('facet-filters-form') ? 'YES' : 'NO');
  console.log('VariantSelects defined:', customElements.get('variant-selects') ? 'YES' : 'NO');
  console.log('MediaGallery defined:', customElements.get('media-gallery') ? 'YES' : 'NO');
  
  // Test facets manually
  const testCheckbox = document.querySelector('.facets__checkbox');
  if (testCheckbox) {
    console.log('Test checkbox found, triggering change...');
    testCheckbox.checked = !testCheckbox.checked;
    testCheckbox.dispatchEvent(new Event('change', {bubbles: true}));
  }
  
  // Listen for errors
  window.addEventListener('error', (e) => {
    if (e.filename && (e.filename.includes('facets') || e.filename.includes('product'))) {
      console.error('Script error:', e.message, 'at', e.filename, ':', e.lineno);
    }
  });
  
  console.log('=== End Debug Info ===');
})();