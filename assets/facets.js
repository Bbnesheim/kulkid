function debounce(func, wait) {
  let timeout;
  return function (...args) {
    const later = () => {
      clearTimeout(timeout);
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

class FacetFiltersForm extends HTMLElement {
  constructor() {
    super();
    this.onActiveFilterClick = debounce(this.onActiveFilterClick.bind(this), 300);

    this.debouncedOnSubmit = debounce((event) => {
      this.onSubmitHandler(event);
    }, 800);

    const facetForm = this.querySelector('form');
    // Listen to both input and change to catch selects and checkboxes across browsers
    facetForm.addEventListener('input', this.debouncedOnSubmit.bind(this));
    facetForm.addEventListener('change', this.debouncedOnSubmit.bind(this));

    const facetWrapper = this.querySelector('#FacetsWrapperDesktop');
    if (facetWrapper) facetWrapper.addEventListener('keyup', onKeyUpEscape);
  }

  static setListeners() {
    const onHistoryChange = (event) => {
      const searchParams = event.state ? event.state.searchParams : FacetFiltersForm.searchParamsInitial;
      if (searchParams === FacetFiltersForm.searchParamsPrev) return;
      FacetFiltersForm.renderPage(searchParams, null, false);
    };
    window.addEventListener('popstate', onHistoryChange);
  }

  static toggleActiveFacets(disable = true) {
    document.querySelectorAll('.js-facet-remove').forEach((element) => {
      element.classList.toggle('disabled', disable);
    });
  }

  static getBaseUrl() {
    if (!FacetFiltersForm.baseUrl) {
      try {
        FacetFiltersForm.baseUrl = new URL(window.location.href);
      } catch (error) {
        FacetFiltersForm.baseUrl = { pathname: window.location.pathname || '/' };
      }
    }
    return FacetFiltersForm.baseUrl;
  }

  static getInitialQueryParams() {
    if (!FacetFiltersForm.initialQueryParams) {
      FacetFiltersForm.initialQueryParams = new URLSearchParams(window.location.search);
    }
    return new URLSearchParams(FacetFiltersForm.initialQueryParams.toString());
  }

  static normalizeSearchParams(searchParams) {
    if (searchParams instanceof URLSearchParams) return searchParams;
    return new URLSearchParams(searchParams || '');
  }

  static mergeSearchParams(searchParams, { includeSectionId = false, sectionId = '' } = {}) {
    const baseParams = FacetFiltersForm.getInitialQueryParams();
    const nextParams = FacetFiltersForm.normalizeSearchParams(searchParams);

    baseParams.delete('page');

    if (!includeSectionId) {
      baseParams.delete('section_id');
    }

    const seenKeys = new Set();
    nextParams.forEach((_, key) => {
      seenKeys.add(key);
    });

    seenKeys.forEach((key) => {
      baseParams.delete(key);
    });

    nextParams.forEach((value, key) => {
      baseParams.append(key, value);
    });

    if (includeSectionId && sectionId) {
      baseParams.set('section_id', sectionId);
    }

    return baseParams;
  }

  static buildSectionFetchUrl(sectionId, searchParams) {
    const base = FacetFiltersForm.getBaseUrl();
    const url = new URL(base.pathname || '/', window.location.origin);
    const mergedParams = FacetFiltersForm.mergeSearchParams(searchParams, { includeSectionId: true, sectionId });
    url.search = mergedParams.toString();
    return url.toString();
  }

  static buildHistoryTarget(searchParams) {
    const base = FacetFiltersForm.getBaseUrl();
    const mergedParams = FacetFiltersForm.mergeSearchParams(searchParams);
    const queryString = mergedParams.toString();
    return `${base.pathname || '/'}${queryString ? `?${queryString}` : ''}`;
  }

  static navigateToSearch(searchParams) {
    const target = FacetFiltersForm.buildHistoryTarget(searchParams);
    window.location.href = target;
  }

  static renderPage(searchParams, event, updateURLHash = true) {
    FacetFiltersForm.searchParamsPrev = searchParams;
    const sections = FacetFiltersForm.getSections();
    const countContainer = document.getElementById('ProductCount');
    const countContainerDesktop = document.getElementById('ProductCountDesktop');
    const loadingSpinners = document.querySelectorAll(
      '.facets-container .loading__spinner, facet-filters-form .loading__spinner'
    );
    loadingSpinners.forEach((spinner) => spinner.classList.remove('hidden'));
    const productGridContainer = document.getElementById('ProductGridContainer');
    const productGrid = productGridContainer ? productGridContainer.querySelector('.collection') : null;
    if (productGrid) {
      productGrid.classList.add('loading');
    }
    if (countContainer) {
      countContainer.classList.add('loading');
    }
    if (countContainerDesktop) {
      countContainerDesktop.classList.add('loading');
    }

    FacetFiltersForm.latestSearchParams = searchParams;

    sections.forEach((section) => {
      const url = FacetFiltersForm.buildSectionFetchUrl(section.section, searchParams);
      const filterDataUrl = (element) => element.url === url;

      FacetFiltersForm.filterData.some(filterDataUrl)
        ? FacetFiltersForm.renderSectionFromCache(filterDataUrl, event)
        : FacetFiltersForm.renderSectionFromFetch(url, event, searchParams);
    });

    if (updateURLHash) FacetFiltersForm.updateURLHash(searchParams);
  }

  static renderSectionFromFetch(url, event, searchParams) {
    fetch(url, { credentials: 'same-origin' })
      .then((response) => {
        if (!response.ok) {
          const error = new Error(`Facets request failed with status ${response.status}`);
          error.response = response;
          throw error;
        }
        return response.text();
      })
      .then((responseText) => {
        const html = responseText;
        FacetFiltersForm.filterData = [...FacetFiltersForm.filterData, { html, url }];
        FacetFiltersForm.renderFilters(html, event);
        FacetFiltersForm.renderProductGridContainer(html);
        FacetFiltersForm.renderProductCount(html);
      })
      .catch((error) => {
        console.error('FacetFiltersForm fetch failed, falling back to full page navigation.', error);
        FacetFiltersForm.navigateToSearch(searchParams || FacetFiltersForm.latestSearchParams || '');
      });
  }

  static renderSectionFromCache(filterDataUrl, event) {
    const html = FacetFiltersForm.filterData.find(filterDataUrl).html;
    FacetFiltersForm.renderFilters(html, event);
    FacetFiltersForm.renderProductGridContainer(html);
    FacetFiltersForm.renderProductCount(html);
  }

  static renderProductGridContainer(html) {
    const productGridContainer = document.getElementById('ProductGridContainer');
    if (!productGridContainer) return;

    productGridContainer.innerHTML = new DOMParser()
      .parseFromString(html, 'text/html')
      .getElementById('ProductGridContainer').innerHTML;

    productGridContainer.querySelectorAll('.scroll-trigger').forEach((element) => {
      element.classList.add('scroll-trigger--cancel');
    });

    if (typeof initializeScrollAnimationTrigger === 'function') {
      initializeScrollAnimationTrigger(productGridContainer);
    }

    FacetFiltersForm.observeLazyImages(productGridContainer);
    FacetFiltersForm.dispatchFacetsUpdated(productGridContainer);
  }

  static renderProductCount(html) {
    const count = new DOMParser().parseFromString(html, 'text/html').getElementById('ProductCount').innerHTML;
    const container = document.getElementById('ProductCount');
    const containerDesktop = document.getElementById('ProductCountDesktop');
    container.innerHTML = count;
    container.classList.remove('loading');
    if (containerDesktop) {
      containerDesktop.innerHTML = count;
      containerDesktop.classList.remove('loading');
    }
    const loadingSpinners = document.querySelectorAll(
      '.facets-container .loading__spinner, facet-filters-form .loading__spinner'
    );
    loadingSpinners.forEach((spinner) => spinner.classList.add('hidden'));
  }

  static renderFilters(html, event) {
    const parsedHTML = new DOMParser().parseFromString(html, 'text/html');
    const facetDetailsElementsFromFetch = parsedHTML.querySelectorAll(
      '#FacetFiltersForm .js-filter, #FacetFiltersFormMobile .js-filter, #FacetFiltersPillsForm .js-filter'
    );
    const facetDetailsElementsFromDom = document.querySelectorAll(
      '#FacetFiltersForm .js-filter, #FacetFiltersFormMobile .js-filter, #FacetFiltersPillsForm .js-filter'
    );

    // Remove facets that are no longer returned from the server
    Array.from(facetDetailsElementsFromDom).forEach((currentElement) => {
      if (!Array.from(facetDetailsElementsFromFetch).some(({ id }) => currentElement.id === id)) {
        currentElement.remove();
      }
    });

    const matchesId = (element) => {
      const jsFilter = event ? event.target.closest('.js-filter') : undefined;
      return jsFilter ? element.id === jsFilter.id : false;
    };

    const facetsToRender = Array.from(facetDetailsElementsFromFetch).filter((element) => !matchesId(element));
    const countsToRender = Array.from(facetDetailsElementsFromFetch).find(matchesId);

    facetsToRender.forEach((elementToRender, index) => {
      const currentElement = document.getElementById(elementToRender.id);
      // Element already rendered in the DOM so just update the innerHTML
      if (currentElement) {
        document.getElementById(elementToRender.id).innerHTML = elementToRender.innerHTML;
      } else {
        if (index > 0) {
          const { className: previousElementClassName, id: previousElementId } = facetsToRender[index - 1];
          // Same facet type (eg horizontal/vertical or drawer/mobile)
          if (elementToRender.className === previousElementClassName) {
            document.getElementById(previousElementId).after(elementToRender);
            return;
          }
        }

        if (elementToRender.parentElement) {
          document.querySelector(`#${elementToRender.parentElement.id} .js-filter`).before(elementToRender);
        }
      }
    });

    FacetFiltersForm.renderActiveFacets(parsedHTML);
    FacetFiltersForm.renderAdditionalElements(parsedHTML);
    FacetFiltersForm.normalizeDuplicateFilters();

    if (countsToRender) {
      const closestJSFilterID = event.target.closest('.js-filter').id;

      if (closestJSFilterID) {
        FacetFiltersForm.renderCounts(countsToRender, event.target.closest('.js-filter'));
        FacetFiltersForm.renderMobileCounts(countsToRender, document.getElementById(closestJSFilterID));

        const newFacetDetailsElement = document.getElementById(closestJSFilterID);
        const newElementSelector = newFacetDetailsElement.classList.contains('mobile-facets__details')
          ? `.mobile-facets__close-button`
          : `.facets__summary`;
        const newElementToActivate = newFacetDetailsElement.querySelector(newElementSelector);

        const isTextInput = event.target.getAttribute('type') === 'text';

        if (newElementToActivate && !isTextInput) newElementToActivate.focus();
      }
    }
  }

  static renderActiveFacets(html) {
    const activeFacetElementSelectors = ['.active-facets-mobile', '.active-facets-desktop'];

    activeFacetElementSelectors.forEach((selector) => {
      const activeFacetsElement = html.querySelector(selector);
      if (!activeFacetsElement) return;
      document.querySelector(selector).innerHTML = activeFacetsElement.innerHTML;
    });

    FacetFiltersForm.toggleActiveFacets(false);
  }

  static renderAdditionalElements(html) {
    const mobileElementSelectors = ['.mobile-facets__open', '.mobile-facets__count', '.sorting'];

    mobileElementSelectors.forEach((selector) => {
      if (!html.querySelector(selector)) return;
      document.querySelector(selector).innerHTML = html.querySelector(selector).innerHTML;
    });

    const mobileFacetForm = document.getElementById('FacetFiltersFormMobile');
    const mobileFacetDrawer = mobileFacetForm ? mobileFacetForm.closest('menu-drawer') : null;
    if (mobileFacetDrawer && typeof mobileFacetDrawer.bindEvents === 'function') {
      mobileFacetDrawer.bindEvents();
    }
  }

  static normalizeDuplicateFilters() {
    const contexts = [
      document.getElementById('FacetFiltersForm'),
      document.getElementById('FacetFiltersFormMobile'),
      document.getElementById('FacetFiltersPillsForm'),
    ].filter(Boolean);

    contexts.forEach((form) => {
      const detailsNodes = Array.from(form.querySelectorAll('[data-filter-key]')).filter(
        (node) =>
          node.dataset.filterKey &&
          node.dataset.filterKey !== '' &&
          node.matches('details')
      );

      const seen = new Map();
      detailsNodes.forEach((details) => {
        const key = details.dataset.filterKey;
        const scope = form.id || 'facets';
        const surface = details.closest('.mobile-facets__wrapper') ? 'mobile' : 'desktop';
        const mapKey = `${scope}-${surface}-${key}`;

        if (!seen.has(mapKey)) {
          seen.set(mapKey, details);
          return;
        }

        FacetFiltersForm.mergeFilterValues(seen.get(mapKey), details);
      });
    });
  }

  static ensureLazyImageObserver() {
    if (!('IntersectionObserver' in window)) return null;
    if (!window.KULKID_IMAGE_OBSERVER) {
      window.KULKID_IMAGE_OBSERVER = new IntersectionObserver((entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const img = entry.target;
          FacetFiltersForm.loadLazyImage(img);
          observer.unobserve(img);
        });
      }, { rootMargin: '200px 0px' });
    }
    return window.KULKID_IMAGE_OBSERVER;
  }

  static loadLazyImage(img) {
    if (!img) return;
    const { dataset } = img;
    const dataSrc = dataset.kulkidSrc || dataset.src;
    const dataSrcset = dataset.kulkidSrcset || dataset.srcset;
    if (dataSrc) {
      img.src = dataSrc;
      delete dataset.kulkidSrc;
      delete dataset.src;
    }
    if (dataSrcset) {
      img.srcset = dataSrcset;
      delete dataset.kulkidSrcset;
      delete dataset.srcset;
    }
    delete dataset.kulkidLazyObserved;
    dataset.kulkidLazyLoaded = 'true';
  }

  static observeLazyImages(root = document) {
    if (!root || typeof root.querySelectorAll !== 'function') return;
    const lazyImages = root.querySelectorAll(
      'img[data-kulkid-src], img[data-kulkid-srcset], img[data-src], img[data-srcset]'
    );
    if (!lazyImages.length) return;

    const observer = FacetFiltersForm.ensureLazyImageObserver();
    lazyImages.forEach((img) => {
      if (img.dataset.kulkidLazyLoaded === 'true') return;
      if (!observer) {
        FacetFiltersForm.loadLazyImage(img);
        return;
      }
      if (img.dataset.kulkidLazyObserved === 'true') return;
      observer.observe(img);
      img.dataset.kulkidLazyObserved = 'true';
    });
  }

  static dispatchFacetsUpdated(root) {
    if (typeof document === 'undefined' || !document.documentElement) return;
    const detail = { root };
    document.documentElement.dispatchEvent(new CustomEvent('kulkid:facets:updated', { detail }));
  }

  static mergeFilterValues(primary, duplicate) {
    if (!primary || !duplicate) return;
    if (duplicate.hasAttribute('open')) {
      primary.setAttribute('open', '');
    }

    const targetList = primary.querySelector('[data-filter-key][role="list"]');
    const duplicateList = duplicate.querySelector('[data-filter-key][role="list"]');

    if (!targetList || !duplicateList) {
      duplicate.remove();
      return;
    }

    const existingInputs = new Set();
    targetList.querySelectorAll('input[name][value]').forEach((input) => {
      existingInputs.add(`${input.name}::${input.value}`);
    });

    Array.from(duplicateList.children).forEach((item) => {
      const input = item.querySelector('input[name][value]');
      if (input) {
        const signature = `${input.name}::${input.value}`;
        if (existingInputs.has(signature)) return;
        existingInputs.add(signature);
      }
      targetList.appendChild(item);
    });

    const showMoreButton = duplicate.querySelector('show-more-button');
    if (showMoreButton) {
      const primaryShowMore = primary.querySelector('show-more-button');
      if (!primaryShowMore) {
        primary.appendChild(showMoreButton);
      } else {
        showMoreButton.remove();
      }
    }

    duplicate.remove();
  }

  static renderCounts(source, target) {
    const targetSummary = target.querySelector('.facets__summary');
    const sourceSummary = source.querySelector('.facets__summary');

    if (sourceSummary && targetSummary) {
      targetSummary.outerHTML = sourceSummary.outerHTML;
    }

    const targetHeaderElement = target.querySelector('.facets__header');
    const sourceHeaderElement = source.querySelector('.facets__header');

    if (sourceHeaderElement && targetHeaderElement) {
      targetHeaderElement.outerHTML = sourceHeaderElement.outerHTML;
    }

    const targetWrapElement = target.querySelector('.facets-wrap');
    const sourceWrapElement = source.querySelector('.facets-wrap');

    if (sourceWrapElement && targetWrapElement) {
      const isShowingMore = Boolean(target.querySelector('show-more-button .label-show-more.hidden'));
      if (isShowingMore) {
        sourceWrapElement
          .querySelectorAll('.facets__item.hidden')
          .forEach((hiddenItem) => hiddenItem.classList.replace('hidden', 'show-more-item'));
      }

      targetWrapElement.outerHTML = sourceWrapElement.outerHTML;
    }
  }

  static renderMobileCounts(source, target) {
    const targetFacetsList = target.querySelector('.mobile-facets__list');
    const sourceFacetsList = source.querySelector('.mobile-facets__list');

    if (sourceFacetsList && targetFacetsList) {
      targetFacetsList.outerHTML = sourceFacetsList.outerHTML;
    }
  }

  static updateURLHash(searchParams) {
    const target = FacetFiltersForm.buildHistoryTarget(searchParams);
    history.pushState({ searchParams }, '', target);
  }

  static getSections() {
    return [
      {
        section: document.getElementById('product-grid').dataset.id,
      },
    ];
  }

  createSearchParams(form) {
    const formData = new FormData(form);
    return new URLSearchParams(formData).toString();
  }

  onSubmitForm(searchParams, event) {
    FacetFiltersForm.renderPage(searchParams, event);
  }

  onSubmitHandler(event) {
    event.preventDefault();
    const sortFilterForms = document.querySelectorAll('facet-filters-form form');
    const srcEl = event.target || event.srcElement;
    if (srcEl && srcEl.classList && srcEl.classList.contains('mobile-facets__checkbox')) {
      const searchParams = this.createSearchParams(event.target.closest('form'));
      this.onSubmitForm(searchParams, event);
    } else {
      const forms = [];
      const isMobile = event.target.closest('form').id === 'FacetFiltersFormMobile';

      sortFilterForms.forEach((form) => {
        if (!isMobile) {
          if (form.id === 'FacetSortForm' || form.id === 'FacetFiltersForm' || form.id === 'FacetSortDrawerForm') {
            forms.push(this.createSearchParams(form));
          }
        } else if (form.id === 'FacetFiltersFormMobile') {
          forms.push(this.createSearchParams(form));
        }
      });
      this.onSubmitForm(forms.join('&'), event);
    }
  }

  onActiveFilterClick(event) {
    event.preventDefault();
    FacetFiltersForm.toggleActiveFacets();
    const url =
      event.currentTarget.href.indexOf('?') == -1
        ? ''
        : event.currentTarget.href.slice(event.currentTarget.href.indexOf('?') + 1);
    FacetFiltersForm.renderPage(url);
  }
}

FacetFiltersForm.filterData = [];
FacetFiltersForm.searchParamsInitial = window.location.search.slice(1);
FacetFiltersForm.searchParamsPrev = window.location.search.slice(1);
FacetFiltersForm.latestSearchParams = FacetFiltersForm.searchParamsInitial;
FacetFiltersForm.baseUrl = null;
FacetFiltersForm.initialQueryParams = null;
customElements.define('facet-filters-form', FacetFiltersForm);
FacetFiltersForm.setListeners();
FacetFiltersForm.normalizeDuplicateFilters();
if (typeof document !== 'undefined') {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      FacetFiltersForm.observeLazyImages(document);
    });
  } else {
    FacetFiltersForm.observeLazyImages(document);
  }
}

class PriceRange extends HTMLElement {
  constructor() {
    super();
    this.querySelectorAll('input').forEach((element) => {
      element.addEventListener('change', this.onRangeChange.bind(this));
      element.addEventListener('keydown', this.onKeyDown.bind(this));
    });
    this.setMinAndMaxValues();
  }

  onRangeChange(event) {
    this.adjustToValidValues(event.currentTarget);
    this.setMinAndMaxValues();
  }

  onKeyDown(event) {
    if (event.metaKey) return;

    const pattern = /[0-9]|\.|,|'| |Tab|Backspace|Enter|ArrowUp|ArrowDown|ArrowLeft|ArrowRight|Delete|Escape/;
    if (!event.key.match(pattern)) event.preventDefault();
  }

  setMinAndMaxValues() {
    const inputs = this.querySelectorAll('input');
    const minInput = inputs[0];
    const maxInput = inputs[1];
    if (maxInput.value) minInput.setAttribute('data-max', maxInput.value);
    if (minInput.value) maxInput.setAttribute('data-min', minInput.value);
    if (minInput.value === '') maxInput.setAttribute('data-min', 0);
    if (maxInput.value === '') minInput.setAttribute('data-max', maxInput.getAttribute('data-max'));
  }

  adjustToValidValues(input) {
    const value = Number(input.value);
    const min = Number(input.getAttribute('data-min'));
    const max = Number(input.getAttribute('data-max'));

    if (value < min) input.value = min;
    if (value > max) input.value = max;
  }
}

customElements.define('price-range', PriceRange);

class FacetRemove extends HTMLElement {
  constructor() {
    super();
    const facetLink = this.querySelector('a');
    if (!facetLink) return; // Safeguard against empty wrappers
    facetLink.setAttribute('role', 'button');
    facetLink.addEventListener('click', this.closeFilter.bind(this));
    facetLink.addEventListener('keyup', (event) => {
      event.preventDefault();
      if (event.code.toUpperCase() === 'SPACE') this.closeFilter(event);
    });
  }

  closeFilter(event) {
    event.preventDefault();
    const form = this.closest('facet-filters-form') || document.querySelector('facet-filters-form');
    form.onActiveFilterClick(event);
  }
}

customElements.define('facet-remove', FacetRemove);
