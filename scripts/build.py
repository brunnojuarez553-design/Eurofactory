#!/usr/bin/env python3
"""Generador estático sin dependencias para Euro Factory.
Uso: python3 scripts/build.py (SITE_URL=https://dominio-real.com)
"""
from pathlib import Path
import sys, os, re, json, html, shutil, datetime
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from content import BRAND,INSTAGRAM,LOCATIONS,SERVICES,FAQS,GUIDES
DEST=ROOT/'dist'
URL=os.environ.get('SITE_URL','https://eurofactory.example').rstrip('/')
if not re.match(r'^https://[^/]+$',URL): raise ValueError('SITE_URL debe ser https://dominio.com sin ruta')
E=lambda s: html.escape(str(s),quote=True)

# Los simbolos de interfaz se sustituyen por SVG (sin glifos Unicode/emoji).
ICON_SYMBOLS = {"↗":"arrow-up-right","→":"arrow-right","☰":"menu","×":"close","‹":"chevron-left","›":"chevron-right"}
def render_icons(markup):
    for char, symbol in ICON_SYMBOLS.items():
        markup = markup.replace(char, f'<svg class="ui-icon" aria-hidden="true" focusable="false"><use href="/assets/icons.svg#{symbol}"></use></svg>')
    return markup
SERVE={s['slug']:s for s in SERVICES}
ROUTES=[]

def btn(label,href,cls='btn-light'):
    return f'<a class="btn {cls}" href="{E(href)}">{E(label)} <span class="arrow" aria-hidden="true">↗</span></a>'

def breadcrumb(*items):
    return '<nav class="crumb" aria-label="Ruta de navegación"><a href="/">Inicio</a> / '+ ' / '.join(E(it) for it in items) + '</nav>'

def brand():
    return '''<a class="logo" href="/" aria-label="Euro Factory, volver al inicio"><img class="logo-official" src="/assets/eurofactory-logo.webp" width="540" height="211" alt="Euro Factory · Garage Premium Automotriz" decoding="async"></a>'''

def layout(path,title,description,body,schema=None,ogtype='website'):
    canonical=URL+path
    if path=='/':canonical=URL+'/'
    navs=[('Inicio','/'),('Servicios','/servicios/'),('Nosotros','/nosotros/'),('Galería','/galeria/'),('Sedes','/sedes/'),('Guías','/guias/'),('Contacto','/contacto/')]
    navhtml=''.join(f'<a href="{u}" '+('aria-current="page"' if (path==u or path.startswith(u) and u!='/') else '')+f'>{E(t)}</a>' for t,u in navs)
    schema_script=f'<script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(",",":"))}</script>' if schema else ''
    html_text=f'''<!doctype html><html lang="es-VE"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#090a0b">
<title>{E(title)}</title><meta name="description" content="{E(description)}"><meta name="author" content="Euro Factory">
<link rel="canonical" href="{E(canonical)}"><link rel="icon" type="image/webp" href="/assets/eurofactory-icon.webp">
<meta property="og:type" content="{ogtype}"><meta property="og:locale" content="es_VE"><meta property="og:site_name" content="Euro Factory"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(description)}"><meta property="og:url" content="{E(canonical)}"><meta property="og:image" content="{E(URL)}/assets/bmw-detalle.webp">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(description)}">
<link rel="preload" href="/assets/barlow-condensed-bold.ttf" as="font" type="font/ttf" crossorigin><link rel="stylesheet" href="/assets/styles.css?v=6"><link rel="stylesheet" href="/assets/refinement.css?v=6"><link rel="stylesheet" href="/assets/locations.css?v=1"><link rel="stylesheet" href="/assets/premium.css?v=2">{schema_script}</head><body class="{'home-page' if path=='/' else 'inner-page'}{' intake-page' if path in ('/evaluacion/', '/contacto/') else ''}"><a class="skip-link" href="#contenido">Saltar al contenido</a>
<div class="reading-progress" aria-hidden="true" data-reading-progress></div>
<header class="header"><div class="wrap header-in">{brand()}<nav class="nav" aria-label="Navegación principal">{navhtml}</nav><div class="nav-cta">{btn('Agenda tu evaluación','/evaluacion/','btn-accent')}<button type="button" class="mobile-toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="mobile-nav" data-menu-toggle>☰</button></div></div>
<nav id="mobile-nav" class="mobile-nav" aria-label="Navegación móvil" data-mobile-nav>{navhtml}<a href="/evaluacion/">Solicitar evaluación ↗</a></nav></header>
<main id="contenido" tabindex="-1">{body}</main>
<section class="cta-footer"><div class="wrap"><span class="eyebrow">07 / DA EL SIGUIENTE PASO</span><h2>Tu vehículo,<br><span class="outline-text">en buenas manos.</span></h2><p>Cuéntanos qué necesitas. El equipo de tu sede te orienta.</p>{btn('Agenda tu evaluación','/evaluacion/','btn-accent')+btn('Elegir sede','/sedes/','btn-outline')}</div></section>
<footer class="footer"><div class="wrap"><div class="foot-grid"><div class="foot-identity">{brand()}<p>Taller independiente de servicio automotriz. Especialistas en vehículos europeos, con atención en Maracay y Valencia, Venezuela.</p><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram @eurofactory_ ↗</a></div><div><h4>Explorar</h4><a href="/servicios/">Servicios</a><a href="/nosotros/">Quiénes somos</a><a href="/galeria/">Galería</a><a href="/evaluacion/">Evaluación digital</a><a href="/guias/">Guías técnicas</a></div><div><h4>Nuestras sedes</h4><a href="/sedes/maracay/">Maracay · Aragua</a><a href="tel:+584243103283">0424-3103283</a><a href="/sedes/valencia/">Valencia · Carabobo</a><a href="tel:+584144630453">0414-4630453</a><a href="/contacto/">Más información</a></div><div><h4>Información</h4><p>Lunes a viernes<br>8:00 a. m. – 6:00 p. m.<br><small>(horario sujeto a confirmación)</small></p><a href="/preguntas-frecuentes/">Preguntas frecuentes</a><a href="/contacto/">Contacto</a></div></div>
<div class="foot-bottom"><span>© {datetime.date.today().year} EURO FACTORY. TODOS LOS DERECHOS RESERVADOS.</span><span>Taller independiente. Las marcas automotrices mencionadas son de sus respectivos titulares.</span></div></div></footer>
<dialog class="gallery-dialog" data-gallery-dialog aria-label="Imagen de la galería"><button type="button" data-gallery-close aria-label="Cerrar imagen">×</button><img data-gallery-full alt=""><p data-gallery-caption></p></dialog><a class="wa-float" href="/evaluacion/" aria-label="Iniciar solicitud de servicio"><span aria-hidden="true">↗</span> Solicitar evaluación</a>
<script src="/assets/site.js?v=6" defer></script></body></html>'''
    dest=DEST/path.lstrip('/')/'index.html' if path!='/' else DEST/'index.html'
    dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(render_icons(html_text),encoding='utf-8')
    ROUTES.append(path)

def pagehead(label,title,description,trail):
    return f'''<section class="page-top"><div class="wrap">{breadcrumb(*trail)}<div class="eyebrow" style="margin-top:45px">{E(label)}</div><h1>{title}</h1><p>{E(description)}</p></div></section>'''

def organization_schema():
    return {'@context':'https://schema.org','@type':'Organization','@id':URL+'/#organization','name':'Euro Factory','url':URL+'/','logo':URL+'/assets/eurofactory-logo.webp','sameAs':[INSTAGRAM], 'description':'Taller automotriz especializado en vehículos europeos con sedes en Maracay y Valencia, Venezuela.', 'areaServed':[{'@type':'City','name':'Maracay'},{'@type':'City','name':'Valencia, Carabobo'}]}

def local_schema(key):
    L=LOCATIONS[key];return {'@context':'https://schema.org','@type':'AutoRepair','@id':URL+'/sedes/'+key+'/#localbusiness','name':'Euro Factory '+L['city'],'url':URL+'/sedes/'+key+'/','logo':URL+'/assets/eurofactory-logo.webp','image':URL+'/assets/bmw-detalle.webp', 'telephone':'+'+L['wa'],'address':{'@type':'PostalAddress','streetAddress':L['address'] if key=='maracay' else 'El Viñedo','addressLocality':L['city'],'addressRegion':L['region'],'addressCountry':'VE'},'areaServed':{'@type':'City','name':L['city']},'sameAs':[INSTAGRAM],'parentOrganization':{'@id':URL+'/#organization'}}

def service_icon(index):
    paths = ["<path d=\"M4 9V4h5m6 0h5v5m0 6v5h-5m-6 0H4v-5\"/><path d=\"M8 12h2l2-4 2 8 2-4h2\"/>","<path d=\"M12 3C9 8 5 11 5 15a7 7 0 0 0 14 0c0-4-4-7-7-12Z\"/><path d=\"M8 15a4 4 0 0 0 4 4\"/>","<path d=\"M14 6a5 5 0 0 0-6 6l-5 5a2 2 0 0 0 4 4l5-5a5 5 0 0 0 6-6l-4 4-4-4 4-4Z\"/>","<path d=\"M9 3h6M9 21h6M12 3v3l-4 2 8 3-8 3 8 3-4 2v2\"/>","<circle cx=\"12\" cy=\"12\" r=\"9\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/><path d=\"M12 3v3m9 6h-3m-6 9v-3m-9-6h3\"/>","<rect x=\"6\" y=\"6\" width=\"12\" height=\"12\" rx=\"2\"/><path d=\"M9 2v4m6-4v4m7 3h-4m4 6h-4M9 18v4m6-4v4M2 9h4m-4 6h4\"/><path d=\"M10 10h4v4h-4z\"/>","<path d=\"m12 3 9 5v9l-9 5-9-5V8l9-5Zm-9 5 9 5 9-5M12 13v9M7 5.8l9 5\"/>"]
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+paths[index]+'</svg>'

def service_card(s):
    images=['bmw-detalle.webp','vehiculo-europeo.webp','taller-fragmento.webp','auto-audi.webp','bmw-detalle.webp','performance-hero.webp','vehiculo-europeo.webp']
    image=images[int(s['num'])-1]
    return f"""<a class="service-card" href="/servicios/{E(s['slug'])}/"><img class="service-bg" src="/assets/{image}" alt="" loading="lazy"><span class="svc-num">{s['num']}</span><div class="service-copy"><span class="service-rule" aria-hidden="true"></span><h3>{E(s['name'])}</h3><p>{E(s['short'])}</p><span class="svc-go">SABER MÁS <span aria-hidden="true">→</span></span></div></a>"""

def services_section(limit=7):
    selected=[SERVICES[5],SERVICES[1],SERVICES[0],SERVICES[2]] if limit==4 else SERVICES[:limit]
    cards=''.join(service_card(s) for s in selected)
    return f"""<section class="section dark-panel" id="servicios"><div class="wrap"><div class="section-head"><div><div class="eyebrow">02 / SERVICIOS ESPECIALIZADOS</div><h2 class="title">Nuestros servicios</h2></div><p class="lead">Diagnóstico, mantenimiento y soluciones técnicas para tu vehículo.</p></div><div class="service-grid {'full-catalog' if limit==7 else ''}">{cards}</div><div class="wide-cta"><span>El cuidado correcto empieza por conocer tu vehículo.</span><a class="line-link" href="/servicios/">VER TODOS LOS SERVICIOS →</a></div></div></section>"""

def evidence_section():
    return '''<section class="section evidence"><div class="wrap evidence-layout"><div><div class="eyebrow">02 / NUESTRA ESENCIA</div><h2 class="title">La precisión<br>es nuestra <span class="serif">actitud.</span></h2><p class="lead">Euro Factory es un taller automotriz con sedes en Maracay y Valencia. Nos enfocamos en el cuidado de vehículos europeos con diagnóstico, mantenimiento y asesoría personalizada.</p><div class="evidence-notes"><div class="evidence-note"><b>Atención especializada</b><span>Vehículos europeos</span></div><div class="evidence-note"><b>Dos sedes</b><span>Maracay y Valencia</span></div><div class="evidence-note"><b>Proceso orientado al cliente</b><span>Evaluación + contacto</span></div></div><a class="line-link" href="/nosotros/">Conoce Euro Factory ↗</a></div><div class="evidence-photo"><img src="/assets/bmw-detalle.webp" width="1170" height="730" alt="Detalle de vehículo BMW compartido por Euro Factory" loading="lazy"><span class="evidence-index">EURO / 02</span><span class="evidence-overlay">AUTOMOTIVE CARE · MARACAY / VALENCIA</span></div></div></section>'''

def gallery_section():
    items=[('bmw-detalle.webp','BMW · Detalle automotriz'),('auto-audi.webp','Audi · Especialización europea'),('apertura-valencia.webp','Sede Valencia'),('vehiculo-europeo.webp','Vehículos europeos'),('taller-fragmento.webp','Comunidad Euro Factory')]
    cards=''.join(f'<a class="gallery-item" href="/assets/{name}" data-gallery-image data-caption="{E(label)}"><img src="/assets/{name}" alt="{E(label)} — material compartido por Euro Factory" loading="lazy"><span class="gallery-label">{E(label)}<small>AMPLIAR IMAGEN <span aria-hidden="true">↗</span></small></span></a>' for name,label in items)
    return f"""<section class="section gallery-section" id="galeria"><div class="wrap"><div class="section-head"><div><div class="eyebrow">03 / DENTRO DE EURO FACTORY</div><h2 class="title">Pasión por los autos.<br>Atención al detalle.</h2></div><a class="line-link" href="/galeria/">VER GALERÍA →</a></div><div class="gallery-grid">{cards}<a class="gallery-social" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><span class="eyebrow">EURO FACTORY / EN INSTAGRAM</span><strong>El taller.<br>Los autos.<br>El día a día.</strong><span>SEGUIR @EUROFACTORY_ ↗</span></a></div><p class="gallery-disclaimer">Imágenes del material compartido por Euro Factory.</p></div></section>"""

def tool_form():
    options=''.join(f'<option value="{E(s["name"])}">{E(s["name"])}</option>' for s in SERVICES)
    return f'''<form class="tool-form" data-intake aria-label="Solicitud de evaluación técnica"><div class="field"><label for="sede">Sede preferida *</label><select id="sede" name="sede" required><option value="maracay">Maracay</option><option value="valencia">Valencia</option></select></div><div class="field"><label for="servicio">Tipo de servicio *</label><select id="servicio" name="servicio" required><option value="No estoy seguro / necesito orientación">No estoy seguro</option>{options}</select></div><div class="field"><label for="marca">Marca *</label><input id="marca" name="marca" placeholder="Ej. BMW" maxlength="60" required></div><div class="field"><label for="modelo">Modelo *</label><input id="modelo" name="modelo" placeholder="Ej. 320i" maxlength="65" required></div><div class="field"><label for="anio">Año *</label><input type="number" id="anio" name="anio" placeholder="Ej. 2018" min="1960" max="{datetime.date.today().year+1}" required></div><div class="field"><label for="nombre">Tu nombre *</label><input id="nombre" name="nombre" placeholder="Nombre y apellido" autocomplete="name" maxlength="90" required></div><div class="field full"><label for="consulta">¿Qué necesita tu vehículo? *</label><textarea id="consulta" name="consulta" placeholder="Describe los síntomas, la falla o el mantenimiento que quieres realizar..." maxlength="1200" required></textarea></div><div class="field full"><label for="telefono">Teléfono de contacto *</label><input id="telefono" name="telefono" type="tel" placeholder="Ej. 0412-0000000" autocomplete="tel" maxlength="35" required></div><div class="form-note"><label><input type="checkbox" name="consentimiento" required> Acepto que mis datos se utilicen para preparar la consulta que enviaré voluntariamente por WhatsApp. La web no los almacena.</label></div><div class="form-progress" aria-live="polite" data-form-progress>Completa los datos para preparar tu consulta.</div><div class="tool-submit"><button type="submit" class="btn btn-dark">Preparar solicitud <span class="arrow" aria-hidden="true">↗</span></button></div><div class="form-preview" data-preview role="region" aria-label="Revisión de tu consulta" tabindex="-1"><div class="eyebrow">REVISA TU CONSULTA</div><p data-preview-text></p><a data-send-wa class="btn btn-accent" target="_blank" rel="noopener noreferrer" href="#">Enviar consulta por WhatsApp ↗</a><p style="font-size:11px;margin:15px 0 0">Tu consulta se enviará únicamente cuando confirmes desde WhatsApp. La cita queda sujeta a confirmación del taller.</p></div></form>'''

def tool_section():
    return f'''<section class="section tool-section" id="evaluacion"><div class="wrap"><div class="section-head"><div><div class="eyebrow">04 / HERRAMIENTA DIGITAL</div><h2 class="title">Tu próxima<br><span class="serif">evaluación.</span></h2></div><p class="lead">Una solicitud ordenada ayuda al taller a entender tu caso desde el primer contacto.</p></div><div class="tool-card"><div class="tool-intro"><div class="eyebrow">EURO FACTORY / SERVICE INTAKE</div><h3 class="title">Cuéntanos qué <span class="serif">necesitas.</span></h3><p>Elige una sede, cuéntanos qué vehículo tienes y qué está pasando. Preparamos tu mensaje para el equipo adecuado.</p><div class="step-list"><div><span>01 / IDENTIFICACIÓN</span><b>Vehículo y servicio</b></div><div><span>02 / CONTEXTO</span><b>Descripción de la consulta</b></div><div><span>03 / CONTACTO</span><b>WhatsApp de la sede elegida</b></div></div></div>{tool_form()}</div></div></section>'''

def branch_icon(name):
    """Íconos SVG inline para que el contacto funcione sin librerías externas."""
    paths = {
        'pin': '<path d="M20 10c0 5.5-8 11-8 11S4 15.5 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.6"/>',
        'phone': '<path d="M22 16.5v3a2.5 2.5 0 0 1-2.7 2.5A18.4 18.4 0 0 1 3 5.7 2.5 2.5 0 0 1 5.5 3h3a2 2 0 0 1 2 1.7l.5 3a2 2 0 0 1-.6 1.8L8.6 11a14 14 0 0 0 4.4 4.4l1.5-1.8a2 2 0 0 1 1.8-.6l3 .5a2 2 0 0 1 1.7 2Z"/>',
        'message': '<path d="M20 11.5a8 8 0 0 1-8 8 9 9 0 0 1-4-.9L3 20l1.4-4.6A8 8 0 1 1 20 11.5Z"/><path d="M8.5 11.5h7"/>',
        'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4m10-4v4M3 10h18"/>',
        'navigation': '<path d="m3 11 18-8-8 18-2.5-7.5L3 11Z"/>',
        'arrow': '<path d="M7 17 17 7M7 7h10v10"/>',
    }
    return '<svg class="branch-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">' + paths[name] + '</svg>'

def locations_section():
    cards = []
    for index, (key, L) in enumerate(LOCATIONS.items(), start=1):
        exact_address = key == 'maracay'
        address = L['address'] if exact_address else L['shortAddress']
        query = (L['address'] + ', ' + L['city'] + ', Venezuela') if exact_address else 'El Viñedo, Valencia, Carabobo, Venezuela'
        embed_url = 'https://maps.google.com/maps?q=' + quote(query, safe='') + '&z=15&output=embed'
        wa_message = 'Hola, Euro Factory ' + L['city'] + '. Me gustaría solicitar información para mi vehículo.'
        wa_url = 'https://wa.me/' + L['wa'] + '?text=' + quote(wa_message, safe='')
        map_notice = ('Mapa de la zona de Los Olivos Viejos. Confirma el acceso al galpón con el taller.' if exact_address else
                      'Mapa referencial de El Viñedo. Confirma la dirección exacta con la sede antes de ir.')
        map_label = 'Ver ubicación en Google Maps' if exact_address else 'Explorar zona en Google Maps'
        location_status = 'Dirección publicada' if exact_address else 'Ubicación exacta por confirmar'
        cards.append(f'''<article class="branch-card" aria-labelledby="branch-{key}-title">
<div class="branch-card__top">
  <div class="branch-card__eyebrow"><span class="branch-card__index">SEDE {index:02d}</span><span class="branch-card__region">{E(L['region']).upper()} / VENEZUELA</span></div>
  <h3 id="branch-{key}-title">{E(L['city'])}<span>.</span></h3>
  <p class="branch-card__intro">Contacto directo con el equipo de Euro Factory {E(L['city'])}.</p>
  <div class="branch-contact-detail">
    <div class="branch-contact-detail__icon">{branch_icon('pin')}</div>
    <div class="branch-contact-detail__body"><span class="branch-contact-detail__label">DIRECCIÓN</span><address>{E(address)}</address><small class="branch-location-status">{E(location_status)}</small></div>
  </div>
  <a class="branch-contact-detail branch-contact-detail--link" href="tel:+{E(L['wa'])}" aria-label="Llamar a Euro Factory {E(L['city'])} al {E(L['phone'])}">
    <span class="branch-contact-detail__icon">{branch_icon('phone')}</span>
    <span class="branch-contact-detail__body"><span class="branch-contact-detail__label">TELÉFONO / CONTACTO</span><strong>{E(L['phone'])}</strong></span>
    <span class="branch-contact-detail__trail">{branch_icon('arrow')}</span>
  </a>
</div>
<div class="branch-map" aria-label="Mapa de referencia de Euro Factory {E(L['city'])}">
  <iframe title="Mapa de referencia: Euro Factory {E(L['city'])}" src="{E(embed_url)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
</div>
<div class="branch-card__bottom">
  <p class="branch-map-note">{branch_icon('pin')}<span>{E(map_notice)}</span></p>
  <a class="branch-map-link" href="{E(L['map'])}" target="_blank" rel="noopener noreferrer">{E(map_label)} {branch_icon('arrow')}</a>
  <div class="branch-actions">
    <a class="branch-action branch-action--primary" href="{E(wa_url)}" target="_blank" rel="noopener noreferrer" aria-label="Escribir por WhatsApp a la sede Euro Factory {E(L['city'])}">{branch_icon('message')}<span>WhatsApp de la sede</span>{branch_icon('arrow')}</a>
    <a class="branch-action branch-action--secondary" href="/evaluacion/?sede={E(key)}">{branch_icon('calendar')}<span>Solicitar evaluación</span>{branch_icon('arrow')}</a>
  </div>
  <a class="branch-detail-link" href="/sedes/{E(key)}/">Conocer más sobre esta sede {branch_icon('arrow')}</a>
</div>
</article>''')
    return f'''<section class="section branches-section" id="sedes" aria-labelledby="branches-title"><div class="wrap">
<div class="section-head branches-head"><div><div class="eyebrow">05 / DÓNDE ESTAMOS</div><h2 class="title" id="branches-title">Dos sedes.<br><span class="serif">Un estándar.</span></h2></div>
<p class="lead">Elige tu sede. Encuentra su dirección, contacto directo y mapa, y prepara tu evaluación en pocos pasos.</p></div>
<div class="branch-grid">{''.join(cards)}</div>
</div></section>'''

def faq_section():
    return '<section class="section dark-panel"><div class="wrap"><div class="section-head"><div><div class="eyebrow">06 / PREGUNTAS FRECUENTES</div><h2 class="title">Resolvemos <span class="serif">tus dudas.</span></h2></div><a class="line-link" href="/preguntas-frecuentes/">Ver todas las respuestas ↗</a></div><div class="faq">'+''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in FAQS)+'</div></div></section>'

def process_section():
    return """<section class="section process-section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">04 / NUESTRA FORMA DE TRABAJAR</div><h2 class="title">Tu confianza<br>se gana en cada detalle.</h2></div><p class="lead">Un proceso claro, desde la primera consulta hasta la evaluación técnica.</p></div><div class="process-grid"><article><span>01</span><h3>Primero, escuchamos.</h3><p>Nos compartes el vehículo, los síntomas y el servicio que necesitas.</p></article><article><span>02</span><h3>Evaluamos con criterio.</h3><p>El diagnóstico y el alcance se definen según el estado real de tu vehículo.</p></article><article><span>03</span><h3>Hablamos claro.</h3><p>El equipo de tu sede te orienta sobre disponibilidad y próximos pasos.</p></article></div></div></section>"""

def home():
    hero="""<section class="hero" data-hero-carousel aria-roledescription="carrusel" aria-label="Euro Factory: especialización automotriz"><img class="hero-background" data-hero-image src="/assets/performance-hero.webp" alt="Imagen de ambientación: deportivo europeo en un entorno de taller" width="1672" height="941" fetchpriority="high"><div class="hero-shade"></div><div class="wrap hero-content"><span class="hero-kicker" data-hero-kicker>ESPECIALISTAS EN VEHÍCULOS EUROPEOS</span><h1 class="hero-heading" data-hero-title>Tu auto merece<br><em>EURO FACTORY.</em></h1><p data-hero-copy>Diagnóstico, mantenimiento y mecánica especializada. Precisión técnica y atención personalizada en Maracay y Valencia.</p><div class="hero-actions">"""+btn('Solicitar evaluación','/evaluacion/','btn-accent')+btn('Conoce nuestros servicios','/servicios/','btn-outline')+"""</div><div class="hero-meta"><span>MARACAY / ARAGUA</span><span>VALENCIA / CARABOBO</span></div></div><button class="hero-arrow prev" data-hero-prev aria-label="Ver imagen anterior">‹</button><button class="hero-arrow next" data-hero-next aria-label="Ver imagen siguiente">›</button><div class="hero-pagination"><span data-hero-count aria-live="polite">01 / 03</span><div class="hero-dots"><button data-hero-slide="0" aria-label="Ver portada" aria-pressed="true"></button><button data-hero-slide="1" aria-label="Ver especialización" aria-pressed="false"></button><button data-hero-slide="2" aria-label="Ver atención" aria-pressed="false"></button></div></div><small class="hero-image-note" data-hero-note>Imagen de ambientación</small></section>"""
    brands="""<div class="brandbar"><div class="wrap brandbar-in"><small>ESPECIALIZACIÓN EUROPEA</small><span>BMW</span><span>MERCEDES-BENZ</span><span>AUDI</span><span>VOLKSWAGEN</span><span>SEAT</span></div></div>"""
    selector="""<section class="consult-strip"><div class="wrap consult-strip-in"><div><span class="eyebrow">01 / EMPIEZA AQUÍ</span><h2>Prepara tu visita.</h2></div><form action="/evaluacion/" class="visit-selector"><label>Tu sede<select name="sede"><option value="maracay">Maracay · Aragua</option><option value="valencia">Valencia · Carabobo</option></select></label><label>Tu vehículo<select name="marca"><option value="">Selecciona la marca</option><option>BMW</option><option>Mercedes-Benz</option><option>Audi</option><option>Volkswagen</option><option>SEAT</option><option>Otra marca</option></select></label><button type="submit" class="btn btn-accent">CONTINUAR <span aria-hidden="true">→</span></button></form></div></section>"""
    return hero+brands+selector+services_section(4)+gallery_section()+evidence_section()+process_section()+tool_section()+locations_section()+faq_section()



layout('/','Euro Factory | Taller automotriz premium en Maracay y Valencia','Taller automotriz especializado en BMW, Audi, Mercedes-Benz y Volkswagen. Diagnóstico, mantenimiento, frenos y mecánica en Maracay y Valencia, Venezuela.',home(),organization_schema())
layout('/servicios/','Servicios de mecánica y diagnóstico | Euro Factory','Conoce nuestros servicios automotrices: diagnóstico, mantenimiento, electrónica, frenos, suspensión, repuestos y mecánica en Venezuela.',pagehead('SERVICIOS / EURO FACTORY','Mecánica de<br><span class="serif">precisión.</span>','Diagnóstico, mantenimiento y reparaciones orientadas a cada necesidad. Atención en Maracay y Valencia.',['Servicios'])+services_section()+tool_section(),organization_schema())
layout('/nosotros/','Sobre Euro Factory | Taller especializado en vehículos europeos','Conoce Euro Factory, taller independiente especializado en vehículos europeos con sedes en Maracay y Valencia, Venezuela.',pagehead('NUESTRA IDENTIDAD','Donde la técnica<br>se une al <span class="serif">cuidado.</span>','La confianza se construye con criterios claros, atención cercana y respeto por cada vehículo.',['Quiénes somos'])+evidence_section()+'''<section class="section"><div class="wrap"><div class="section-head"><div><div class="eyebrow">NUESTRO COMPROMISO</div><h2 class="title">Diagnosticar.<br>Explicar.<br><span class="serif">Resolver.</span></h2></div><p class="lead">Euro Factory comunica una propuesta enfocada en asesoría honesta, trato personalizado y soluciones confiables. Nuestro objetivo digital es hacer visible ese mismo estándar.</p></div><div class="stats"><div class="stat"><strong>01.</strong><span>ESCUCHAMOS TU CONSULTA</span></div><div class="stat"><strong>02.</strong><span>EVALUAMOS LA NECESIDAD</span></div><div class="stat"><strong>03.</strong><span>ACORDAMOS LOS PRÓXIMOS PASOS</span></div></div></div></section>'''+locations_section(),organization_schema())
layout('/galeria/','Galería del taller | Euro Factory Maracay y Valencia','Conoce imágenes y momentos compartidos por Euro Factory, taller automotriz especializado en vehículos europeos en Venezuela.',pagehead('EURO FACTORY / EN IMÁGENES','Una mirada<br><span class="serif">al taller.</span>','Conoce algunos momentos de Euro Factory.',['Galería'])+gallery_section()+'''<section class="section" style="padding-top:0"><div class="wrap note-banner">Esta es una selección de referencia extraída de las capturas aportadas. Para el lanzamiento final recomendamos una sesión fotográfica de ambas sedes, equipos, técnicos y vehículos, con las autorizaciones correspondientes.</div></div></section>''',organization_schema())
layout('/evaluacion/','Solicitar evaluación o cita | Euro Factory','Enviá una consulta técnica organizada a la sede de Euro Factory en Maracay o Valencia. Identificá tu vehículo y contacta directamente por WhatsApp.',pagehead('CONTACTO / SERVICE INTAKE','Tu consulta,<br><span class="serif">bien encaminada.</span>','No necesitas describir tu vehículo varias veces. Prepara toda la información y contacta al equipo correspondiente.',['Solicitar evaluación'])+tool_section()+'''<section class="section"><div class="wrap note-banner">Importante: este formulario no almacena datos ni reserva automáticamente una cita. El equipo confirma disponibilidad por WhatsApp. En situaciones de seguridad crítica, no conduzcas el vehículo hasta recibir evaluación profesional.</div></div></section>''',organization_schema())
layout('/sedes/','Nuestras sedes en Maracay y Valencia | Euro Factory','Ubicaciones, contacto y solicitud de servicio de Euro Factory en Maracay, Aragua y Valencia, Carabobo, Venezuela.',pagehead('SEDES / VENEZUELA','Más cerca de<br><span class="serif">tu vehículo.</span>','Encuentra la sede ideal para tu servicio y enviá tu consulta directamente.',['Sedes'])+locations_section(),organization_schema())
for key,L in LOCATIONS.items():
    details=pagehead('EURO FACTORY / '+L['region'].upper(),f'Taller automotriz<br>en <span class="serif">{E(L["city"])}.</span>',f'Atención especializada para vehículos europeos en {L["city"]}, {L["region"]}. Diagnóstico, mecánica y mantenimiento.',['Sedes',L['city']])
    details+=f'''<section class="section"><div class="wrap contact-columns"><div><div class="eyebrow">VISÍTANOS / {E(L['city']).upper()}</div><h2>Tu sede en {E(L['city'])}.</h2><p class="lead">{E(L['address'])}</p><p class="small-bullet">Teléfono / WhatsApp: <a href="tel:+{L['wa']}"><strong>{E(L['phone'])}</strong></a></p><p class="small-bullet">Horario comunicado: lunes a viernes de 8:00 a. m. a 6:00 p. m. (por confirmar)</p><p class="small-bullet">Servicios: diagnóstico, mantenimiento, mecánica, frenos y otros, sujetos a disponibilidad.</p><div style="display:flex;flex-wrap:wrap;gap:13px;margin-top:30px">{btn('Enviar consulta',f'/evaluacion/?sede={key}')}<a href="{E(L['map'])}" class="btn btn-outline" target="_blank" rel="noopener noreferrer">Buscar ubicación ↗</a></div></div><aside class="sidebar"><div class="eyebrow">ATENCIÓN PERSONALIZADA</div><h3>Antes de visitarnos</h3><p>Comparte marca, modelo, año, síntomas y el motivo de tu visita. Así el equipo podrá orientarte y confirmar la disponibilidad de atención.</p>{btn('Preparar solicitud',f'/evaluacion/?sede={key}','btn-accent')}</aside></div></section>'''
    details+=services_section(6)+faq_section()
    layout(f'/sedes/{key}/',f'Taller automotriz en {L["city"]} | Euro Factory',f'Euro Factory {L["city"]}: diagnóstico, mantenimiento y mecánica especializada en vehículos europeos. Contacto {L["phone"]}.',details,local_schema(key))
for s in SERVICES:
    body=pagehead('SERVICIOS / '+s['num'],E(s['name'])+'<span class="serif">.</span>',s['desc'],['Servicios',s['name']])
    body+=f'''<section class="section"><div class="wrap service-detail"><article><div class="eyebrow">{E(s['tags'])}</div><h2>{E(s['short'])}</h2><div class="prose"><p>{E(s['details'])}</p><p>Atendemos consultas en nuestras sedes de Maracay y Valencia. Para orientarte, necesitamos los datos de tu vehículo y una descripción breve del problema o del servicio solicitado.</p></div><h2 style="margin-top:65px">¿Cómo solicitar este servicio?</h2><div class="evidence-notes"><div class="evidence-note"><b>01. Describe tu vehículo</b><span>Marca, modelo y año</span></div><div class="evidence-note"><b>02. Explicá lo que necesitas</b><span>Síntomas o consulta</span></div><div class="evidence-note"><b>03. Elige la sede</b><span>Maracay o Valencia</span></div></div>{btn('Iniciar solicitud','/evaluacion/','btn-light')}</article><aside class="sidebar"><div class="eyebrow">SERVICIOS / EURO FACTORY</div><h3>Atención en dos sedes.</h3><p>No indicamos presupuestos cerrados sin conocer las condiciones del vehículo. Contáctanos y te orientamos sobre los próximos pasos.</p>{btn('Consultar disponibilidad','/evaluacion/','btn-accent')}<p class="micro">* La consulta no representa una cita confirmada.</p></aside></div></section>'''
    body+=f'''<section class="section dark-panel"><div class="wrap"><div class="section-head"><div><div class="eyebrow">EXPLORÁ MÁS</div><h2 class="title">Otros <span class="serif">servicios.</span></h2></div></div><div class="list-services">{''.join(f'<a href="/servicios/{v["slug"]}/">{E(v["name"])} <span>↗</span></a>' for v in SERVICES if v!=s)}</div></div></section>'''
    layout(f'/servicios/{s["slug"]}/',f'{s["name"]} en Maracay y Valencia | Euro Factory',f'{s["desc"]} Consulta en Euro Factory, taller especializado en Maracay y Valencia, Venezuela.',body,organization_schema())
layout('/preguntas-frecuentes/','Preguntas frecuentes sobre el taller | Euro Factory','Preguntas frecuentes sobre turnos, sedes, precios orientativos, mantenimiento, diagnóstico y vehículos europeos en Euro Factory.',pagehead('AYUDA / PREGUNTAS FRECUENTES','Todo lo que<br>quieres <span class="serif">saber.</span>','Respuestas claras antes de consultar o visitar una sede.',['Preguntas frecuentes'])+faq_section(),organization_schema())
layout('/contacto/','Contacto y teléfonos de Euro Factory | Maracay y Valencia','Contactá a Euro Factory en Maracay al 0424-3103283 o Valencia al 0414-4630453. Enviá una consulta técnica por WhatsApp desde nuestro sitio.',pagehead('CONTACTO / MARACAY + VALENCIA','Hablemos de<br><span class="serif">tu vehículo.</span>','Elige la sede y el canal de contacto. Podés preparar una solicitud digital para agilizar la conversación.',['Contacto'])+locations_section()+tool_section(),organization_schema())
layout('/guias/','Guías de cuidado automotriz | Euro Factory','Consejos de mantenimiento, diagnóstico computarizado y seguridad para el cuidado de vehículos europeos.',pagehead('CONTENIDOS / INFORMACIÓN ÚTIL','Conocimiento<br>que <span class="serif">acompaña.</span>','Guías generales para entender mejor el cuidado de tu vehículo. No sustituyen el diagnóstico de un profesional.',['Guías'])+'<section class="section"><div class="wrap"><div class="guides-grid">'+''.join(f'''<a class="guide-card" href="/guias/{g['slug']}/"><span class="guide-tag">GUÍA / AUTOMOTRIZ</span><h3>{E(g['title'])}</h3><p>{E(g['excerpt'])}</p><span>Leer artículo ↗</span></a>''' for g in GUIDES)+'</div></div></section>',organization_schema())
for g in GUIDES:
    article=pagehead('GUÍAS / EURO FACTORY',E(g['title']),g['excerpt'],['Guías',g['title']])
    article+='<article class="section"><div class="wrap editorial"><div class="eyebrow">INFORMACIÓN GENERAL · '+g['date']+'</div>'+''.join('<p>'+E(par)+'</p>' for par in g['body'])+'<div class="note-banner">Esta nota es informativa. Ante una falla, el servicio adecuado depende de una evaluación técnica individual.</div><div style="margin-top:38px">'+btn('Solicitar evaluación','/evaluacion/')+'</div></div></article>'
    sch={'@context':'https://schema.org','@type':'BlogPosting','headline':g['title'],'datePublished':g['date'],'dateModified':g['date'],'author':{'@type':'Organization','name':'Euro Factory'},'publisher':{'@id':URL+'/#organization'},'mainEntityOfPage':URL+'/guias/'+g['slug']+'/'}
    layout('/guias/'+g['slug']+'/',g['title']+' | Euro Factory',g['excerpt'],article,sch,ogtype='article')
# Assets and crawlability.
shutil.copytree(ROOT/'public'/'assets',DEST/'assets',dirs_exist_ok=True)
(DEST/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{E(URL+p)}</loc></url>\n' for p in ROUTES)+'</urlset>\n',encoding='utf-8')
(DEST/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: '+URL+'/sitemap.xml\n',encoding='utf-8')
(DEST/'404.html').write_text(render_icons('<!doctype html><html lang="es-VE"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>No encontramos esa página | Euro Factory</title><style>body{font-family:Arial;background:#090a0b;color:#fff;margin:15vh auto;width:min(90%,650px)}a{color:#f2b32e}.ui-icon{display:inline-block;width:17px;height:17px;vertical-align:-3px;fill:none;stroke:currentColor}</style><h1>404 — No encontramos esta página.</h1><p>Podés volver al inicio para seguir explorando.</p><a href="/">Volver a Euro Factory →</a></html>'),encoding='utf-8')
print('Built:',len(ROUTES),'pages | SITE_URL:',URL)
