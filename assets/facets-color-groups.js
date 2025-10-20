(function(){
  function labelToBaseColor(label){
    if(!label) return null;
    const l = label.toString().toLowerCase();
    // Normalize diacritics
    const n = l.normalize('NFD').replace(/\p{Diacritic}/gu,'');
    // Norwegian + English mappings
    if(/(svart|sort|black)/.test(n)) return 'Svart';
    if(/(hvit|hvit|white)/.test(n)) return 'Hvit';
    if(/(gra|grå|gray|grey|koks)/.test(n)) return 'Gra';
    if(/(bla|blå|blue|navy|royal|kongebla|kongeblå|himmelbla|marine|turkis|cyan)/.test(n)) return 'Bla';
    if(/(rod|rød|red|burgunder|vin)/.test(n)) return 'Rod';
    if(/(gronn|grønn|green|lime|oliven|khaki)/.test(n)) return 'Gronn';
    if(/(gul|yellow|mustard)/.test(n)) return 'Gul';
    if(/(oransj|orange)/.test(n)) return 'Oransje';
    if(/(lilla|fiolett|purple|violet)/.test(n)) return 'Lilla';
    if(/(rosa|pink)/.test(n)) return 'Rosa';
    if(/(brun|brown|camel|tan)/.test(n)) return 'Brun';
    if(/(beige|sand|cream|ivory|bone)/.test(n)) return 'Beige';
    if(/(multi|flerfarg|flerfarget|multicolor)/.test(n)) return 'Flerfarget';
    return label; // fallback
  }

  function buildGroups(root){
    const lists = (root || document).querySelectorAll('ul[role="list"][data-filter-key="color"]');
    lists.forEach((ul)=>{
      if(ul.dataset.kulkidGrouped === 'true') return;
      const items = Array.from(ul.querySelectorAll('li')); 
      const groups = new Map();
      items.forEach((li)=>{
        const labelEl = li.querySelector('.facet-checkbox__text-label') || li;
        const name = labelEl.textContent.trim();
        const base = labelToBaseColor(name);
        li.dataset.baseColor = base;
        const input = li.querySelector('input[type="checkbox"]');
        const disabled = input?.disabled;
        const countText = li.querySelector('.facet-checkbox__text')?.textContent || '';
        if(!groups.has(base)) groups.set(base,{inputs:[], count:0});
        const g = groups.get(base);
        if (input) g.inputs.push(input);
        // derive count
        const m = countText.match(/\((\d+)\)/);
        if(m) g.count += parseInt(m[1],10);
      });

      // Create UI only if it meaningfully consolidates
      if(groups.size === 0 || groups.size === items.length) { ul.dataset.kulkidGrouped='true'; return; }

      const container = document.createElement('div');
      container.className = 'kulkid-color-groups';
      container.setAttribute('aria-label','Hovedfarger');

      groups.forEach((g,base)=>{
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'button button--tertiary kulkid-color-group__btn';
        btn.textContent = `${base}${g.count?` (${g.count})`:''}`;
        btn.addEventListener('click', () => {
          let changed = false;
          g.inputs.forEach((input)=>{
            if (input.disabled) return;
            if (!input.checked) {
              input.checked = true;
              input.dispatchEvent(new Event('change',{bubbles:true}));
              changed = true;
            }
          });
          if(!changed){
            // toggle off if all already checked
            g.inputs.forEach((input)=>{
              if (input.disabled) return;
              input.checked = false;
              input.dispatchEvent(new Event('change',{bubbles:true}));
            });
          }
        });
        container.appendChild(btn);
      });

      ul.parentElement.insertBefore(container, ul);
      ul.dataset.kulkidGrouped = 'true';
    });
  }

  function init(){
    buildGroups(document);
    document.documentElement.addEventListener('kulkid:facets:updated', (e)=>{
      try { buildGroups(e.detail?.root || document); } catch(err) { console.error(err); }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
