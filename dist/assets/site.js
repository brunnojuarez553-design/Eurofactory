(function () {
  const toggle = document.querySelector('[data-menu-toggle]');
  const mobile = document.querySelector('[data-mobile-nav]');
  if (toggle && mobile) {
    const narrow = window.matchMedia("(max-width: 1180px)");
    function closeMenu(restoreFocus = false) {
      mobile.classList.remove("open"); document.body.classList.remove("menu-open");
      document.querySelector('.header')?.classList.remove('is-nav-hidden');
      toggle.setAttribute("aria-expanded", "false"); toggle.setAttribute("aria-label", "Abrir menú"); toggle.innerHTML = "<svg class=\"ui-icon\" aria-hidden=\"true\" focusable=\"false\"><use href=\"/assets/icons.svg#menu\"></use></svg>";
      mobile.inert = narrow.matches;
      if (restoreFocus) toggle.focus();
    }
    toggle.addEventListener("click", () => {
      if (mobile.classList.contains("open")) { closeMenu(); return; }
      mobile.inert = false; mobile.classList.add("open"); document.body.classList.add("menu-open");
      document.querySelector('.header')?.classList.remove('is-nav-hidden');
      toggle.setAttribute("aria-expanded", "true"); toggle.setAttribute("aria-label", "Cerrar menú"); toggle.innerHTML = "<svg class=\"ui-icon\" aria-hidden=\"true\" focusable=\"false\"><use href=\"/assets/icons.svg#close\"></use></svg>";
      mobile.querySelector("a")?.focus();
    });
    mobile.querySelectorAll("a").forEach(a => a.addEventListener("click", () => closeMenu()));
    document.addEventListener("keydown", e => {
      if (!mobile.classList.contains("open")) return;
      if (e.key === "Escape") { closeMenu(true); return; }
      if (e.key === "Tab") {
        const links = [...mobile.querySelectorAll("a")];
        if (e.shiftKey && document.activeElement === links[0]) { e.preventDefault(); toggle.focus(); }
        else if (!e.shiftKey && document.activeElement === links.at(-1)) { e.preventDefault(); toggle.focus(); }
        else if (document.activeElement === toggle) { e.preventDefault(); (e.shiftKey ? links.at(-1) : links[0]).focus(); }
      }
    });
    narrow.addEventListener("change", () => closeMenu()); closeMenu();
  }
  const floating = document.querySelector('.wa-float');
  if (floating && 'IntersectionObserver' in window) {
    const visible = new Set();
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? visible.add(entry.target) : visible.delete(entry.target));
      floating.hidden = visible.size > 0;
    });
    document.querySelectorAll('.hero, .tool-card, .cta-footer').forEach(el => observer.observe(el));
  }

  const header = document.querySelector('.header');
  const progressBar = document.querySelector('[data-reading-progress]');
  let scrollQueued = false;
  let lastScrollY = Math.max(0, window.scrollY);
  let directionStartY = lastScrollY;
  let scrollDirection = 0;
  function updateScroll() {
    const y = Math.max(0, window.scrollY);
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progressBar) progressBar.style.width = (max > 0 ? Math.min(100, y / max * 100) : 0) + '%';
    header?.classList.toggle('is-scrolled', y > 60);
    if (header) {
      if (y <= 80 || document.body.classList.contains('menu-open')) {
        // Always show at the top and while the mobile navigation is open.
        header.classList.remove('is-nav-hidden');
        directionStartY = y;
        scrollDirection = 0;
      } else {
        const delta = y - lastScrollY;
        if (Math.abs(delta) > 0) {
          const nextDirection = Math.sign(delta);
          if (nextDirection !== scrollDirection) {
            scrollDirection = nextDirection;
            directionStartY = lastScrollY;
          }
          // Ignore tiny touchpad/trackpad movements to avoid flickering.
          if (Math.abs(y - directionStartY) >= 14) {
            header.classList.toggle('is-nav-hidden', nextDirection > 0);
            directionStartY = y;
          }
        }
      }
    }
    lastScrollY = y;
    scrollQueued = false;
  }
  header?.addEventListener('focusin', () => header.classList.remove('is-nav-hidden'));
  window.addEventListener('scroll', () => {
    if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(updateScroll); }
  }, {passive:true});
  window.addEventListener('resize', updateScroll); updateScroll();

  const hero = document.querySelector('[data-hero-carousel]');
  if (hero) {
    const slides = [
      {image:'performance-hero.webp', alt:'Imagen de ambientación: deportivo europeo en un entorno de taller', kicker:'ESPECIALISTAS EN VEHÍCULOS EUROPEOS', line:'Tu auto merece', accent:'EURO FACTORY.', copy:'Diagnóstico, mantenimiento y mecánica especializada. Precisión técnica y atención personalizada en Maracay y Valencia.', note:'Imagen de ambientación'},
      {image:'bmw-detalle.webp', alt:'Detalle de un BMW compartido por Euro Factory', kicker:'DIAGNÓSTICO / MANTENIMIENTO / MECÁNICA', line:'Precisión técnica.', accent:'CUIDADO REAL.', copy:'Tu vehículo necesita criterio, atención y un proceso claro. Cuéntanos qué sucede y recibe orientación del equipo.', note:'Material de Euro Factory'},
      {image:'auto-audi.webp', alt:'Vehículo Audi del material compartido por Euro Factory', kicker:'MARACAY + VALENCIA', line:'Dos sedes.', accent:'UN MISMO ESTÁNDAR.', copy:'Elige la ubicación que te quede mejor. Prepara tu consulta y contacta directamente al equipo de tu sede.', note:'Material de Euro Factory'}
    ];
    let active = 0;
    function showSlide(index) {
      active = (index + slides.length) % slides.length;
      const slide = slides[active];
      const image = hero.querySelector('[data-hero-image]');
      image.src = '/assets/' + slide.image; image.alt = slide.alt;
      hero.querySelector('[data-hero-kicker]').textContent = slide.kicker;
      const title = hero.querySelector('[data-hero-title]');
      title.replaceChildren(document.createTextNode(slide.line), document.createElement('br'));
      const accent = document.createElement('em'); accent.textContent = slide.accent; title.append(accent);
      hero.querySelector('[data-hero-copy]').textContent = slide.copy;
      hero.querySelector('[data-hero-note]').textContent = slide.note;
      hero.querySelector('[data-hero-count]').textContent = String(active+1).padStart(2,'0') + ' / 03';
      hero.querySelectorAll('[data-hero-slide]').forEach((button, index) => button.setAttribute('aria-pressed', String(index === active)));
    }
    hero.querySelector('[data-hero-prev]').addEventListener('click', () => showSlide(active-1));
    hero.querySelector('[data-hero-next]').addEventListener('click', () => showSlide(active+1));
    hero.querySelectorAll('[data-hero-slide]').forEach(button => button.addEventListener('click', () => showSlide(Number(button.dataset.heroSlide))));
  }

  const dialog = document.querySelector('[data-gallery-dialog]');
  if (dialog && typeof dialog.showModal === 'function') {
    document.querySelectorAll('[data-gallery-image]').forEach(link => link.addEventListener('click', event => {
      event.preventDefault();
      const image = dialog.querySelector('[data-gallery-full]');
      image.src = link.href; image.alt = link.dataset.caption;
      dialog.querySelector('[data-gallery-caption]').textContent = link.dataset.caption;
      dialog.showModal();
    }));
    dialog.querySelector('[data-gallery-close]').addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', event => {
      const box = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
    });
  }

  // Datos enviados solo al WhatsApp elegido tras pulsar el enlace: no existe reserva ni almacenamiento local.
  document.querySelectorAll('[data-intake]').forEach(form => {
    const params = new URLSearchParams(location.search);
    const initialSede = params.get('sede');
    if (initialSede === 'maracay' || initialSede === 'valencia') form.elements.sede.value = initialSede;
    const initialBrand = params.get('marca');
    if (initialBrand && initialBrand.length <= 60) form.elements.marca.value = initialBrand;
    const progress = form.querySelector('[data-form-progress]');
    const required = [...form.querySelectorAll('[required]')];
    function updateProgress() {
      const complete = required.filter(el => el.type === 'checkbox' ? el.checked : el.value.trim() !== '').length;
      if (progress) progress.textContent = complete + ' de ' + required.length + ' campos completos. Revisa tu mensaje antes de enviarlo.';
    }
    updateProgress();
    const preview = form.querySelector('[data-preview]');
    const textEl = preview?.querySelector('[data-preview-text]');
    const link = preview?.querySelector('[data-send-wa]');
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const f = new FormData(form);
      const sede = f.get('sede');
      const phone = sede === 'valencia' ? '584144630453' : '584243103283';
      const sedeLabel = sede === 'valencia' ? 'Valencia' : 'Maracay';
      const pairs = [
        'Hola, equipo de Euro Factory. Quiero solicitar una evaluación técnica.',
        '', 'Sede: ' + sedeLabel,
        'Vehículo: ' + f.get('marca') + ' ' + f.get('modelo') + ' (' + f.get('anio') + ')',
        'Servicio: ' + f.get('servicio'),
        'Consulta: ' + f.get('consulta'),
        'Nombre: ' + f.get('nombre'),
        'Contacto: ' + f.get('telefono'),
        '', '¿Me pueden orientar con disponibilidad y próximos pasos?'
      ];
      const msg = pairs.join('\n');
      textEl.textContent = msg;
      link.href = 'https://wa.me/' + phone + '?text=' + encodeURIComponent(msg);
      link.setAttribute('aria-label', 'Abrir WhatsApp de Euro Factory ' + sedeLabel + ' con la consulta preparada');
      preview.classList.add('visible');
      preview.focus({preventScroll:true});
      preview.scrollIntoView({behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',block:'nearest'});
    });
    form.querySelectorAll('input,select,textarea').forEach(el=>el.addEventListener('input',()=>{ preview?.classList.remove('visible'); updateProgress(); }));
  });
})();
