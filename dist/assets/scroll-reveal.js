/* Euro Factory — cinematic, scroll-triggered reveal on every page.
   IntersectionObserver + compositor-only translate/scale/opacity.
   Never changes layout, scroll position, interactive state or carousel transforms. */
(() => {
  'use strict';
  if (!('IntersectionObserver' in window) ||
      !('CSS' in window) || !CSS.supports('translate', '1px 0') ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const selectors = [
    // Section headings: independent typographic entrance.
    '.section-head .eyebrow',
    '.section-head .title',
    '.section-head .lead',
    '.section-head > .line-link',
    '.section-head > p',
    // Brand heading, service finder and intake.
    '.brandbar-copy',
    '.consult-strip .eyebrow',
    '.consult-strip h2',
    '.consult-strip .visit-selector',
    // Editorial blocks and proof.
    '.evidence .eyebrow',
    '.evidence .title',
    '.evidence .lead',
    '.evidence .evidence-story',
    '.evidence .evidence-note',
    '.evidence .evidence-photo',
    '.evidence .evidence-discover-cta',
    // Services, gallery, process and locations.
    '.service-grid > .service-card',
    '.gallery-grid > .gallery-item',
    '.gallery-grid > .gallery-social',
    '.process-grid > article',
    '.branch-grid > .branch-card',
    '.guides-grid > .guide-card',
    // Other page content: select only blocks, never a scroll rail or sticky parent.
    '.tool-card > .tool-intro',
    '.tool-card > .tool-form',
    '.tool-section .section-head',
    '.service-detail > *',
    '.stats > .stat',
    '.faq details',
    '.page-top + .section > .wrap > .eyebrow',
    '.page-top + .section > .wrap > .title',
    '.page-top + .section > .wrap > .lead',
    '.cta-footer .eyebrow',
    '.cta-footer h2',
    '.cta-footer .btn',
    '.footer-topline',
    '.footer-luxe-grid > .foot-identity',
    '.footer-luxe-grid > .footer-nav-group',
    '.footer-luxe-grid > .footer-locations',
    '.footer-luxe-grid > .footer-information'
  ];

  // No animation for the hero (LCP), marquee logo track, nav, maps, modal,
  // chat, input controls or any item inside already animated descendants.
  const excluded = '.hero, .header, .mobile-nav, .brandbar-track, .gallery-dialog, .ef-concierge, dialog';
  const items = [...new Set(
    selectors.flatMap(sel => [...document.querySelectorAll(sel)])
  )].filter(el => !el.closest(excluded) && !el.matches('[hidden]'));
  if (!items.length) return;

  const prefersNarrow = window.matchMedia('(max-width: 700px)').matches;
  const visibleHeight = window.innerHeight || document.documentElement.clientHeight;
  // Preserve existing stagger but keep any group below ~250 ms for responsiveness.
  const staggerGroup = new WeakMap();
  function groupKey(el) {
    return el.closest('.service-grid, .gallery-grid, .process-grid, .branch-grid, .guides-grid, .evidence-notes, .stats, .faq, .footer-luxe-grid, .section-head') || el.closest('section') || el.parentElement;
  }
  let sectionCounter = 0;
  const sectionIndexes = new WeakMap();
  function sectionIndex(el) {
    const section = el.closest('section') || el.parentElement;
    if (!sectionIndexes.has(section)) sectionIndexes.set(section, sectionCounter++);
    return sectionIndexes.get(section);
  }
  const directionCycle = ['up', 'left', 'right', 'in', 'down', 'out'];
  const cardSelectors = '.service-card, .gallery-item, .gallery-social, .branch-card, .guide-card, .evidence-note, .stat, .faq details, .process-grid > article';
  const cardGroupIndexes = new WeakMap();

  for (const el of items) {
    const isCard = el.matches(cardSelectors);
    const group = groupKey(el);
    const next = (staggerGroup.get(group) || 0);
    staggerGroup.set(group, next + 1);

    let direction;
    if (isCard) {
      const cardIndex = cardGroupIndexes.get(group) || 0;
      cardGroupIndexes.set(group, cardIndex + 1);
      // Side-to-side, inward and upward patterns alternate naturally.
      direction = ['left', 'right', 'in', 'up', 'out', 'down'][cardIndex % 6];
    } else if (el.matches('.evidence-photo, .tool-card > .tool-form')) {
      direction = 'right';
    } else if (el.matches('.evidence-story, .evidence .lead, .tool-card > .tool-intro')) {
      direction = 'left';
    } else if (el.matches('.section-head .title, .cta-footer h2')) {
      direction = 'up';
    } else {
      direction = directionCycle[sectionIndex(el) % directionCycle.length];
    }
    el.dataset.reveal = direction;
    el.style.setProperty('--reveal-delay', Math.min(next % 5, 4) * (prefersNarrow ? 45 : 75) + 'ms');
    const rect = el.getBoundingClientRect();
    // Content visible at initialization must never disappear for a transition.
    if (rect.bottom > 0 && rect.top < visibleHeight * 0.91 &&
        rect.right > 0 && rect.left < window.innerWidth) {
      el.classList.add('is-revealed');
    }
  }
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add('is-revealed');
      observer.unobserve(entry.target);
    }
  }, { root: null, rootMargin: '0px 0px -7% 0px', threshold: 0.065 });

  for (const el of items) if (!el.classList.contains('is-revealed')) observer.observe(el);
  // Gating class only after IntersectionObserver and visible targets are ready:
  // pages stay 100% visible when JS is unavailable or fails.
  document.documentElement.classList.add('scroll-reveal-ready');
  document.addEventListener('focusin', event => {
    const target = event.target.closest?.('[data-reveal]');
    if (target && !target.classList.contains('is-revealed')) {
      target.classList.add('is-revealed');
      observer.unobserve(target);
    }
  }, { passive: true });
})();
