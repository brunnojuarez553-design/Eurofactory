(function () {
  const toggle = document.querySelector('[data-menu-toggle]');
  const mobile = document.querySelector('[data-mobile-nav]');
  if (toggle && mobile) {
    const narrow = window.matchMedia("(max-width: 850px)");
    function closeMenu(restoreFocus = false) {
      mobile.classList.remove("open"); document.body.classList.remove("menu-open");
      toggle.setAttribute("aria-expanded", "false"); toggle.setAttribute("aria-label", "Abrir menú"); toggle.textContent = "☰";
      mobile.inert = narrow.matches;
      if (restoreFocus) toggle.focus();
    }
    toggle.addEventListener("click", () => {
      if (mobile.classList.contains("open")) { closeMenu(); return; }
      mobile.inert = false; mobile.classList.add("open"); document.body.classList.add("menu-open");
      toggle.setAttribute("aria-expanded", "true"); toggle.setAttribute("aria-label", "Cerrar menú"); toggle.textContent = "×";
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
  // Datos enviados solo al WhatsApp elegido tras pulsar el enlace: no existe reserva ni almacenamiento local.
  document.querySelectorAll('[data-intake]').forEach(form => {
    const params = new URLSearchParams(location.search);
    const initialSede = params.get('sede');
    if (initialSede === 'maracay' || initialSede === 'valencia') form.elements.sede.value = initialSede;
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
        '', '📍 Sede: ' + sedeLabel,
        '🚘 Vehículo: ' + f.get('marca') + ' ' + f.get('modelo') + ' (' + f.get('anio') + ')',
        '🛠️ Servicio: ' + f.get('servicio'),
        '📋 Consulta: ' + f.get('consulta'),
        '👤 Nombre: ' + f.get('nombre'),
        '📲 Contacto: ' + f.get('telefono'),
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
