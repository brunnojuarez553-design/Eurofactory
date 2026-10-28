# EURO FACTORY · web premium (versión conceptual funcional)

Sitio multipágina estático, **sin dependencias**, pensado para producción en Vercel. Diseño editorial responsive, páginas prerenderizadas para indexación, datos estructurados, metadata diferenciada por página, 2 sedes, 7 fichas de servicios, blog educativo, galería, sitemap y herramienta de solicitud por WhatsApp.

## Estructura

- `src/content.py`: fuente central de servicios, sedes, teléfonos, preguntas y contenidos.  
- `scripts/build.py`: generador estático Python 3 (sin paquetes externos).  
- `public/assets/styles.css`: diseño, responsive, accesibilidad.  
- `public/assets/site.js`: menú móvil y herramienta de consulta.  
- `public/assets/*.webp`: material de referencia proporcionado, recortado para la demo.  
- `dist/`: sitio completo **ya compilado**, desplegable como está, sin entorno Python en el hosting.

## Ver localmente

```bash
python3 -m http.server 8000 --directory dist
```

Abrir http://localhost:8000 (nunca abrir `index.html` como `file://`, por rutas absolutas).

## Cambios de contenido y compilación

```bash
SITE_URL=https://TU-DOMINIO-REAL.com python3 scripts/build.py
```

> **Importante**: El sitio inicial se genera con `https://eurofactory.example` como dominio de muestra en canonicals, OG y sitemap. Recompilar con el dominio final antes de desplegar. No usar `.example` públicamente.

## Vercel

Importar el repositorio con Framework Preset **Other**, salida `dist` y comando `node scripts/vercel-build.mjs`. La configuración está incluida en `vercel.json`. El build adapta el dominio de SEO al despliegue. Si cambias el contenido, regenera `dist/` con Python localmente y sube el resultado.

## Herramienta digital

Formulario accesible para sede, vehículo, servicio, síntomas y datos personales. `site.js` prepara un mensaje que se muestra para revisar. El usuario **debe pulsar** el botón de envío y confirmar en WhatsApp. No almacena datos, no agenda turnos ni genera presupuestos. Rutas: Maracay `584243103283` y Valencia `584144630453` según capturas de Instagram.

## Pendientes de validación antes del lanzamiento

1. Dominio oficial y logo vectorial original del cliente: el monograma **EF** es una propuesta, no el logo definitivo.
2. Teléfonos actuales: capturas publicadas muestran Valencia **0414-4630453** y otra publicación menciona **0422-7170855**. Corroborar sede y número activo; Maracay figura como **0424-3103283**.
3. Dirección precisa y Google Maps/Perfil de Empresa de Valencia; confirmar dirección exacta de Maracay.
4. Horario actual por sede (historias muestran L-V de 8:00 a 18:00, datos del 2025).
5. Texto de servicios reales: verificar mecánica electrónica, ECU, repuestos, reprogramación y disponibilidad en cada sede.
6. Material real: pedir fotos/videos originales de taller, equipo, trabajos, autoridades de uso y permisos; las imágenes actuales son recortes limitados de las capturas del cliente **solo para demo**. Reemplazar por originales, optimizados a WebP/AVIF.
7. Marca `+400 vehículos`: procede de bio compartida por usuario; verificar si se mantiene vigente antes de publicarlo.
8. Obtener testimonios reales publicados/autorizados y reseñas reales de Google Business Profile. No hay opiniones ficticias, puntuaciones falsas ni ratings inventados.
9. Integrar GA4 y Search Console del cliente, perfiles Google Business individuales, OG original y términos/privacidad para Venezuela, si luego se almacena o comparte datos con un CRM.
10. Probar Lighthouse mobile, enlazado, Search Console, Rich Results Test y perfiles Google Business luego de implementar dominio real.

## SEO/GEO realizado

- 22+ rutas prerenderizadas (no SPA con contenido oculto en JS), titles y metas únicas, canonical, OG, `lang=es-VE`, headings semánticos, alt texts, enlaces internos, sitemap XML, robots.txt.
- Una página exclusiva para cada sede, nombre, dirección, teléfono, servicios y un `AutoRepair` JSON-LD específico para cada ubicación (no fake ratings).
- Guías originales que responden preguntas relevantes de los usuarios, preguntas frecuentes visibles, copy local natural, marca y diferenciación explícitas.
- **GEO (AI discoverability)**: claridad de entidad, servicios, ubicaciones, contenido relevante y datos estructurados. **No garantiza** aparecer o posicionar en ChatGPT/Gemini ni Google; se complementa con reputación externa, citas verificables y autoridad real.

## Consideraciones de seguridad

La herramienta no guarda información personal; el mensaje sale por WhatsApp solo por decisión del usuario. Si luego se conecta a Supabase/CRM, agregá aviso de privacidad, consentimiento, validación de servidor, control de spam, acceso con RLS, logs mínimos y protección de secretos. No uses tokens en JS público.

## Despliegue desde este repositorio

Importar en Vercel con Framework Preset **Other**, Root Directory **.**, Build Command **node scripts/vercel-build.mjs** y Output Directory **dist**. No requiere instalación de dependencias. La configuración está incluida en vercel.json.

El build adapta canonical, Open Graph, JSON-LD, robots.txt y sitemap al dominio de producción provisto por Vercel. Si se conecta un dominio propio, definir SITE_URL=https://dominio-real.com y volver a desplegar. SITE_URL tiene prioridad sobre VERCEL_PROJECT_PRODUCTION_URL y VERCEL_URL. No se requiere Python en Vercel: dist está versionado. Para cambios de contenido, ejecutar el generador Python localmente y subir dist actualizado.

## Refinamiento UI/UX

Sistema de negro obsidiana, marfil cálido y champán; tokens de tres capas en public/assets/refinement.css y guía en docs/brand-guidelines.md. Incluye SVGs de servicios, portada con accesos a sedes, enlace para saltar al contenido, menú con foco y Escape, progreso del formulario y revisión enfocada antes de WhatsApp. El botón flotante se oculta al mostrar las llamadas a la acción principales.

Verificación: 375, 768, 1024 y 1440 px sin desbordamiento horizontal; menú por teclado; mensajes WhatsApp de ambas sedes; invalidación de vista previa al editar; movimiento reducido; 22 HTML y 21 JSON-LD sin enlaces internos rotos.

## Dirección premium

Portada editorial asimétrica con fotografía enmarcada, tipografía serif de gran escala, acentos champán, servicios en dos columnas y formulario oscuro. La misma dirección se aplica a sedes, guías, contacto y páginas de servicio. Fotografías y funciones existentes conservadas.

Verificado en 320, 375, 768, 1024 y 1440 px; 30 combinaciones de páginas y tamaños sin desbordamiento horizontal. JSON-LD, enlaces internos, menú por teclado, reducción de movimiento y WhatsApp de ambas sedes verificados.
