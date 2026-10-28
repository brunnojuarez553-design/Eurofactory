(function () {
  const toggle = document.querySelector('[data-menu-toggle]');
  const mobile = document.querySelector('[data-mobile-nav]');
  if (toggle && mobile) {
    function closeMenu() { mobile.classList.remove('open'); document.body.classList.remove('menu-open'); toggle.setAttribute('aria-expanded','false'); toggle.textContent='☰'; }
    toggle.addEventListener('click', () => {
      const open = mobile.classList.toggle('open');
      document.body.classList.toggle('menu-open',open);
      toggle.setAttribute('aria-expanded', String(open)); toggle.textContent = open ? '×' : '☰';
    });
    mobile.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
    document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });
  }
  // Datos enviados solo al WhatsApp elegido tras pulsar el enlace: no existe reserva ni almacenamiento local.
  document.querySelectorAll('[data-intake]').forEach(form => {
    const params = new URLSearchParams(location.search);
    const initialSede = params.get('sede');
    if (initialSede === 'maracay' || initialSede === 'valencia') form.elements.sede.value = initialSede;
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
      preview.scrollIntoView({behavior:'smooth',block:'nearest'});
    });
    form.querySelectorAll('input,select,textarea').forEach(el=>el.addEventListener('input',()=>preview?.classList.remove('visible')));
  });
})();
