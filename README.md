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
