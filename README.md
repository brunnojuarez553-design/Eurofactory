# Euro Factory · Web automotriz

Sitio estático multipágina para Maracay y Valencia. Diseño premium negro grafito y amarillo ámbar (según carteles reales del taller), con portada fotográfica, carrusel manual, tipografía condensada local, servicios con imagen, galería ampliable y solicitud por WhatsApp.

## Vercel

- Framework: Other
- Root Directory: .
- Build Command: node scripts/vercel-build.mjs
- Output Directory: dist
- Sin instalación de dependencias.

La configuración está incluida en vercel.json. El build adapta canonical, Open Graph, JSON-LD, sitemap y robots al dominio de producción de Vercel. Para dominio propio, definir SITE_URL=https://dominio-real.com y volver a desplegar. SITE_URL prevalece sobre VERCEL_PROJECT_PRODUCTION_URL y VERCEL_URL.

## Editar

Contenido: src/content.py. Plantillas: scripts/build.py. Estilos: public/assets/styles.css y public/assets/refinement.css. Interacciones: public/assets/site.js.

Regenerar con Python 3: python scripts/build.py. Subir dist actualizado junto con las fuentes. El servidor de Vercel usa el dist versionado y no necesita Python.

## Funciones

El selector inicial preselecciona sede y marca. El formulario valida datos, prepara una vista previa y abre WhatsApp solo al pulsar el enlace. No almacena datos ni confirma reservas. Teléfonos incluidos: Maracay 584243103283 y Valencia 584144630453.

Carrusel con flechas y selectores; galería en diálogo con cierre por Escape; menú móvil con foco controlado; enlace para saltar al contenido; preferencias de movimiento reducido; tipografía Barlow Condensed local con licencia OFL en assets/FONT-LICENSE.txt.

## SEO/GEO

21 rutas de contenido y 404, HTML prerenderizado, metadatos por página, canonical, Open Graph, sitemap, robots y datos estructurados. Páginas AutoRepair específicas para cada sede.

## Verificación

45 combinaciones de páginas y tamaños (320, 375, 768, 1024 y 1440 px), sin desbordamiento horizontal. Carrusel en cinco tamaños, menú, galería por teclado, selector de visita y consultas WhatsApp de ambas sedes verificados. 22 HTML y 21 bloques JSON-LD válidos, sin enlaces internos rotos.

## Imágenes y datos

La portada utiliza una imagen de ambientación generada e identificada como tal. Galería con el material original compartido. Procedencia y prompt en docs/image-provenance.md. Guía visual y paleta de señalética en docs/brand-guidelines.md.

Confirmar con el taller teléfonos, horarios y direcciones antes de la publicación comercial definitiva. El material original contiene capturas: reemplazarlas por fotografías originales de mayor resolución cuando estén disponibles. El monograma EF es provisional. No se incorporan reseñas ni resultados de potencia ficticios.

## Logo oficial
`public/assets/eurofactory-logo.webp` reproduce el logotipo original plateado facilitado por el cliente, optimizado a WebP y aplicado en navbar y footer, también en `dist/assets/`. Evitar reemplazarlo por el marcador `EF`. La estética general mantiene el ámbar del cartel ECUS Motors y el grafito.

## Iconografia SVG
Toda la iconografia de accion (flechas, botones, navegacion, controles de galeria/carrusel) usa SVG desde `/assets/icons.svg` en lugar de caracteres Unicode o emojis. El generador `scripts/build.py` aplica estos iconos a las 21 paginas estaticas. El menu movil alterna iconos SVG desde `site.js`. Los mensajes preparados para WhatsApp usan etiquetas de texto sin emojis, porque un mensaje no admite SVG.

## Sección de contacto por sede (mapas)
La sección de sedes de Inicio, Contacto y Sedes presenta tarjetas independientes con teléfono, WhatsApp de cada sede, acceso al formulario con sede preseleccionada, enlace a la página individual y Google Maps integrado mediante una búsqueda sin clave API. Diseño: `public/assets/locations.css`. Generación: `locations_section()` en `scripts/build.py`.

**Ubicaciones:** Maracay usa la dirección publicada en Los Olivos Viejos, calle Rivas con Casanova Godoy, galpón 77. Valencia solo tiene confirmada la zona de El Viñedo; por eso el mapa es referencial y se pide confirmar la dirección exacta con el taller. Los mapas son búsquedas, no pines GPS verificados. Confirmar ubicación y horarios con el cliente antes de declarar una dirección definitiva.

## Corrección de layout / regresiones
El diseño premium carga `premium.css?v=2`. **Nunca** centrar un encabezado `position:sticky` con `left:50%` + `transform:translateX(-50%)`: en escritorio se desplaza hacia la izquierda y oculta el logotipo original. Las páginas internas centran el header con `margin-inline:auto` y `left:auto; transform:none`; Inicio puede conservar el centrado de su header `absolute/fixed`. A partir de 1180px se utiliza el menú responsive. Las páginas con formulario de consulta ocultan el CTA flotante redundante. Los encabezados internos tienen alto contenido, sin espacio excesivo. Mantener la metaetiqueta `theme-color` bien formada en los HTML prerenderizados y comprobarlo antes de cada deploy.

## Hero full screen y navegación integrada
Inicio: hero **full-bleed** (`width:100%`, altura inicial `100svh`) sin bordes ni márgenes; la foto conserva `object-fit:cover`. La barra superior ocupa todo el ancho y se superpone a la imagen al inicio; al desplazarse queda fija. En las páginas internas la barra es sticky, también a ancho completo y sin transformación horizontal. El menú móvil se activa a 1180px tanto en CSS como en JS y se despliega justo debajo del header. Fuentes en `public/assets/premium.css` (v3) y `public/assets/site.js` (v7); sincronizar las versiones de `dist/assets/` y los HTML prerenderizados para evitar caché de Vercel.

## Fotografías de galería actualizadas (octubre de 2026)
Las tarjetas de **BMW**, **Audi** y **Vehículos europeos** usan las fotografías originales alojadas en Cloudinary, provistas por el cliente. Los enlaces se mantienen exactamente en `gallery_section()` de `scripts/build.py`; tanto la imagen como el enlace de ampliación apuntan a la misma foto. Los cambios están reflejados también en `dist/index.html` y `dist/galeria/index.html`.

- BMW: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200966/IMG_2829.jpg
- Audi: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200959/IMG_2832.jpg
- Vehículos europeos: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200961/IMG_2841.jpg

Las otras fotografías permanecen locales. El navegador del visitante debe tener acceso a Cloudinary; verificar la disponibilidad remota tras desplegar.

## Carrusel de marcas europeas (2026-10)
La banda debajo del hero muestra logotipos SVG transparentes de BMW, Mercedes-Benz, Audi, Volkswagen y SEAT, guardados localmente en `public/assets/brands/` y `dist/assets/brands/`. La secuencia duplicada solo visualmente (`aria-hidden="true"` en la segunda lista) garantiza desplazamiento CSS continuo (`translateX(-50%)`), pausa con hover y respeta `prefers-reduced-motion`. El marcado original se genera mediante `brand_carousel()` en `scripts/build.py`, con CSS dedicado `brand-marquee.css` solo en inicio, sin JS ni dependencia de terceros durante la navegación.

**Procedencia:** vectores de [Sim1Who/CarBrands](https://github.com/Sim1Who/CarBrands); las marcas son propiedad de sus titulares y su presencia solo expresa especialización técnica del taller independiente, sin atribuir relación comercial ni autorización de fabricante.

## Banner fotográfico de servicios
La página `/servicios/` utiliza una portada exclusiva con la imagen compartida por el cliente alojada en Cloudinary: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200964/IMG_2838.jpg. La foto se aplica como `background-image` con doble degradado oscuro para asegurar la legibilidad del título y la descripción. Implementación en `public/assets/services-banner.css` (y copia en `dist/assets/`) y en `pagehead(..., extra_class='services-banner')`. La hoja de estilos se carga únicamente en la ruta `/servicios/` con precarga de imagen; no modifica banners de otras páginas.

## Footer premium (2026-10)
Pie de página rediseñado mediante `footer()` en `scripts/build.py` y hoja `footer-luxe.css?v=1`, con logotipo oficial, redes sociales y mensajería con iconos SVG de Instagram y WhatsApp, enlaces propios, teléfonos por sede, horario sujeto a confirmación, notas legales y enlace accesible para volver arriba. SVG de redes desde Simple Icons (simbolos añadidos a `icons.svg`). Solo se incorporaron Instagram y WhatsApp reales; sin inventar redes adicionales. Su estética conserva grafito, plata y detalles ámbar, adaptándose a escritorio, tablet y móvil.

## Banner fotográfico de Nosotros (2026-10)
La portada de `/nosotros/` usa una fotografía BMW facilitada por el cliente desde Cloudinary (https://res.cloudinary.com/pcuis0hp/image/upload/v1793200966/IMG_2829.jpg), con degradados grafito para preservar legibilidad, tamaños responsive y precarga. La clase específica `about-banner` se añade en la llamada a `pagehead()` en `scripts/build.py`; el estilo dedicado `about-banner.css?v=1` solo se sirve en `/nosotros/`. Otras portadas no se modifican.

## Fotografía de tarjetas de servicios (octubre 2026)
El generador `scripts/build.py` utiliza `SERVICE_CARD_IMAGE_OVERRIDES` para las tarjetas de **Frenos**, **Suspensión y dirección**, **Mantenimiento preventivo** y **Repuestos y lubricantes** en Inicio y Servicios.
- Frenos y Suspensión: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200963/IMG_2834.jpg
- Mantenimiento preventivo (tarjeta, última foto indicada por el cliente): https://res.cloudinary.com/pcuis0hp/image/upload/v1793200965/IMG_2831.jpg
- Repuestos y lubricantes: https://res.cloudinary.com/pcuis0hp/image/upload/v1793200960/IMG_2840.jpg
- Mantenimiento preventivo (fotografía complementaria en la página de detalle): https://res.cloudinary.com/pcuis0hp/image/upload/v1793200960/IMG_2836.jpg
Las imágenes de servicios no solicitados permanecen sin cambios. CSS fotográfico de detalle: `maintenance-detail.css`.

## Mobile Studio — rediseño mobile-first
La hoja `mobile-studio.css?v=1` se carga **al final** después de todos los estilos, solo modifica presentación en pantallas <=900px y deja intacto escritorio. Servicios, pasos y sedes son carruseles táctiles nativos con scroll snap horizontal, sin librería JS; se mantienen sus enlaces y contenido y se añade `tabindex=0` + descripción accesible para navegación con teclado. Galería en patrón bento de dos columnas, formulario compacto y accesible, sedes con mapas, iconos SVG, CTA con safe-area y footer organizado en dos columnas. Respetar `prefers-reduced-motion` y evitar transformaciones en hover táctil. Los cambios también están integrados en `scripts/build.py` para persistir en reconstrucciones de Vercel.

## Corrección del footer en celulares
`mobile-studio.css?v=2` define áreas de CSS Grid explícitas para el pie de página: identidad (ancho total), Explorar e Información en dos tarjetas paralelas y Sedes en dos tarjetas de contacto. Reemplaza los conflictos de `grid-column` de reglas a 480/700px y reduce el espacio vertical. El enlace flotante de evaluación se oculta cuando cualquier parte del footer entra en pantalla gracias a la observación de `.footer-luxe` en `site.js?v=11`, recuperándose al salir del footer. Se conservan logo, enlaces, SVG y datos reales.

## Asistente conversacional Groq (2026-10)
Botón animado con logo y viñeta a los 45 segundos; chat de consultas, dos sedes y solicitud de cita por WhatsApp con datos completos. La clave debe configurarse como GROQ_API_KEY en Vercel (variable privada) y se debe redeplegar. Guía: docs/assistant.md. No existe agenda automática ni confirmación de turnos.
