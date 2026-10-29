# Asistente virtual Euro Factory

## Activación obligatoria
1. Abrir el proyecto Eurofactory en Vercel > Settings > Environment Variables.
2. Crear GROQ_API_KEY como variable de servidor, asignada a Production (y Preview para pruebas), con la clave de Groq Console.
3. Modelo por defecto (Groq producción 2026): openai/gpt-oss-120b con Structured Outputs estrictos. Opcional GROQ_MODEL=openai/gpt-oss-20b o qwen/qwen3.8-27b. Si GROQ_MODEL apunta al antiguo llama-3.3-70b-versatile (retirado en Free/Developer el 16/08/2026) el servidor usa automáticamente openai/gpt-oss-120b. No utilizar prefijos públicos ni subir claves a GitHub.
4. Hacer Redeploy para que la función de servidor reciba la variable.
5. Probar conversaciones en producción. Un deploy exitoso no confirma por sí solo que la clave esté configurada ni que Groq responda.

## Arquitectura y experiencia
- Frontend: public/assets/assistant.js y assistant.css, iniciados desde site.js en las 21 páginas.
- Backend: api/assistant.js, función Node serverless que llama Groq. Clave solo en process.env.GROQ_API_KEY.
- El botón flotante es circular con el emblema original. A los 45 segundos sin interacción aparece una viñeta de ayuda.
- Respuestas naturales en español de Venezuela sobre servicios, sedes, horarios y dudas generales; sin inventar precios, diagnósticos ni disponibilidad.
- Para pedir cita, reúne conversacionalmente sede, nombre, marca/modelo de vehículo, servicio o problema, fecha estimada y, opcionalmente, teléfono.
- Solo cuando los campos principales estén completos aparece el enlace WhatsApp preparado para la sede correcta.
- Maracay: 584243103283. Valencia: 584144630453. El personal confirma los turnos manualmente; jamás se promete una reserva.
- La dirección de Valencia es solo la zona de El Viñedo; se debe confirmar la dirección exacta con el taller.

## Privacidad y límites
- Las conversaciones están en memoria de la pestaña y se envían a Groq para generar respuestas. No hay base de datos de leads ni agenda conectada.
- El usuario debe abrir y enviar el mensaje en WhatsApp; preparar el enlace no envía los datos por sí solo.
- El endpoint valida los tamaños, evita roles arbitrarios y usa controles de origen y limitación básica de solicitudes por instancia.
- Para tráfico alto complementar con protección WAF y rate limiting distribuido; no guardar ni registrar mensajes con datos personales.
- No se debe mostrar GROQ_API_KEY en JavaScript público ni añadirla al repositorio.

## Pruebas recomendadas
- Servicios y preguntas sobre las dos sedes sin solicitud de turno.
- Cita Maracay con destino wa.me/584243103283 y cita Valencia con wa.me/584144630453.
- Preguntar por detalles, corregir datos y comprobar botón de WhatsApp con nombre, vehículo, problema y fecha estimada.
- Fallos de Groq y falta de clave: mensaje comprensible y contactos de ambas sedes.
- Vista móvil de 375px/430px, teclado, Escape, sugerencia a los 45 segundos y animación reducida.
## Saludo único
El cliente ve una bienvenida en el chat, antes de escribir. El servidor añade ese turno al contexto, evita nuevos saludos y responde de forma directa si la consulta contiene solamente «hola». Se evita una segunda bienvenida sin impedir preguntas sobre servicios y solicitudes de turno.
