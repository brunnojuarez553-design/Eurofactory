"""Información editorial única: editar aquí los servicios, sedes y textos."""
BRAND = "Euro Factory"
INSTAGRAM = "https://www.instagram.com/eurofactory_/"
# Revisar antes de publicar: los números y horarios se tomaron de historias/publicaciones aportadas.
LOCATIONS = {
    'maracay': {
        'city': 'Maracay', 'region': 'Aragua', 'label': 'Maracay · Aragua',
        'phone': '0424-3103283', 'wa': '584243103283',
        'address': 'Los Olivos Viejos, calle Rivas con Casanova Godoy, galpón #77, cerca del C.C. Hyper Jumbo',
        'shortAddress': 'Los Olivos Viejos, Maracay, Aragua',
        'map': 'https://www.google.com/maps/search/?api=1&query=Los+Olivos+Viejos+calle+Rivas+Casanova+Godoy+Maracay',
    },
    'valencia': {
        'city': 'Valencia', 'region': 'Carabobo', 'label': 'Valencia · Carabobo',
        'phone': '0414-4630453', 'wa': '584144630453',
        'address': 'El Viñedo, Valencia, Carabobo (ubicación exacta por confirmar)',
        'shortAddress': 'El Viñedo, Valencia, Carabobo',
        'map': 'https://www.google.com/maps/search/?api=1&query=El+Vinedo+Valencia+Carabobo',
    }
}
SERVICES = [
    {'slug':'diagnostico-computarizado','num':'01','name':'Diagnóstico computarizado','short':'Encontramos el origen, no solo el síntoma.','desc':'Evaluación electrónica con escáner, interpretación de códigos y revisión orientada a la falla reportada.','icon':'scan','tags':'Diagnóstico · Electrónica','details':'La lectura de códigos es el punto de partida, no un diagnóstico definitivo. Correlacionamos la información electrónica con los síntomas y las pruebas pertinentes para orientar la reparación.'},
    {'slug':'mantenimiento-preventivo','num':'02','name':'Mantenimiento preventivo','short':'El cuidado correcto, antes del problema.','desc':'Servicio periódico, revisión de fluidos, filtros y componentes según las necesidades del vehículo.','icon':'droplet','tags':'Mantenimiento · Lubricantes','details':'Un mantenimiento responsable considera el kilometraje, los intervalos del fabricante, el uso y el estado real del vehículo. Te ayudamos a priorizar las tareas necesarias.'},
    {'slug':'mecanica-especializada','num':'03','name':'Mecánica especializada','short':'Experiencia técnica en cada intervención.','desc':'Reparaciones de mecánica ligera y atención a sistemas del vehículo con evaluación previa.','icon':'tool','tags':'Mecánica · Reparación','details':'Realizamos una valoración técnica antes de recomendar trabajos. Cada reparación se define según el estado de la unidad, la disponibilidad de piezas y el alcance aprobado.'},
    {'slug':'suspension','num':'04','name':'Suspensión y dirección','short':'Estabilidad, precisión y confort.','desc':'Inspección y atención de componentes de suspensión y dirección.','icon':'route','tags':'Tren delantero · Seguridad','details':'Ruidos, vibraciones, desgaste irregular o pérdida de estabilidad merecen una revisión. El alcance de la intervención se confirma después de inspeccionar el vehículo.'},
    {'slug':'frenos','num':'05','name':'Sistema de frenos','short':'Confianza en lo que más importa.','desc':'Revisión de discos, pastillas y componentes del sistema de frenado.','icon':'shield','tags':'Frenos · Seguridad','details':'Evaluamos síntomas de desgaste y funcionamiento del sistema para indicar las intervenciones pertinentes. Si percibís pérdida de frenado, evitá conducir el vehículo.'},
    {'slug':'electronica-ecu','num':'06','name':'Electrónica y ECU','short':'Soluciones para sistemas complejos.','desc':'Evaluación electrónica, revisión de módulos y consultas sobre reprogramación según compatibilidad.','icon':'cpu','tags':'ECU · Sistemas electrónicos','details':'El diagnóstico y las intervenciones en módulos electrónicos requieren verificar modelo, año, arquitectura electrónica y naturaleza de la falla. Consultá disponibilidad antes de acercarte.'},
    {'slug':'repuestos-y-lubricantes','num':'07','name':'Repuestos y lubricantes','short':'Componentes adecuados para tu vehículo.','desc':'Asesoría en repuestos, consumibles y lubricantes conforme a especificaciones.','icon':'package','tags':'Repuestos · Consumibles','details':'Te orientamos para identificar componentes compatibles y alternativas disponibles, considerando las especificaciones aplicables al vehículo.'},
]
FAQS = [
    ('¿Atienden únicamente vehículos europeos?', 'Euro Factory se especializa en vehículos europeos, especialmente BMW, Mercedes-Benz, Audi y Volkswagen. Si tenés otro vehículo, podés enviar una consulta para evaluar disponibilidad y alcance del servicio.'),
    ('¿Puedo solicitar una cita desde la web?', 'Sí. Completá la solicitud digital y se abrirá WhatsApp con todos los datos para que el equipo confirme disponibilidad. La solicitud no constituye una reserva automática.'),
    ('¿Tienen atención en Maracay y Valencia?', 'Sí. Podés seleccionar la sede de Maracay o Valencia al iniciar tu consulta y contactar al equipo correspondiente.'),
    ('¿Pueden darme un precio sin revisar el vehículo?', 'Podemos orientar el proceso, pero los presupuestos técnicos dependen del diagnóstico, los repuestos y el alcance real del trabajo.'),
    ('¿Trabajan con repuestos originales?', 'La empresa comunica servicios de repuestos originales y asesoría. La disponibilidad y las especificaciones de cada pieza deben confirmarse para el modelo exacto.'),
    ('¿Cuáles son los horarios?', 'El material recibido informa atención de lunes a viernes de 8:00 a. m. a 6:00 p. m. Confirmá los horarios vigentes con la sede antes de trasladarte.'),
]
GUIDES = [
    {'slug':'cuando-hacer-diagnostico-computarizado','title':'¿Cuándo conviene hacer un diagnóstico computarizado?','excerpt':'Señales, límites del escáner y por qué leer códigos no equivale a identificar una falla.','date':'2026-10-27', 'body':[
        'Una luz de advertencia, pérdida de potencia, fallas intermitentes o consumo anormal pueden justificar una evaluación técnica. El escáner permite consultar información electrónica, pero un código por sí solo no determina qué componente debe reemplazarse.',
        'Un diagnóstico ordenado combina la información electrónica con los síntomas, el historial de mantenimiento y verificaciones específicas. Describir cuándo aparece la falla permite llegar mejor preparado a la revisión.',
        'Si el vehículo presenta una advertencia crítica o problemas de seguridad, evitá seguir conduciendo y consultá a un profesional.'
    ]},
    {'slug':'mantenimiento-preventivo-autos-europeos','title':'Mantenimiento preventivo en autos europeos: qué revisar','excerpt':'Cómo priorizar controles según el manual, el uso y el estado de la unidad.','date':'2026-10-27','body':[
        'No todos los vehículos necesitan las mismas intervenciones. Los intervalos de aceite, filtros, líquido de frenos y otros consumibles dependen del fabricante, el motor, el kilometraje y las condiciones de uso.',
        'Guardá un historial de servicios y consultá el manual del vehículo. Antes de reemplazar piezas, pedí una evaluación de su condición real. Esa información ayuda a mantener la confiabilidad y controlar costos.',
        'En Euro Factory podés solicitar una revisión orientativa indicando marca, modelo, año y el servicio que necesitás.'
    ]},
    {'slug':'ruidos-en-la-suspension','title':'Ruidos en la suspensión: señales que no conviene ignorar','excerpt':'Qué contar al taller cuando aparecen golpes, vibraciones o desgaste irregular.','date':'2026-10-27','body':[
        'Golpes en irregularidades, vibraciones en el volante, sensación de inestabilidad y desgaste irregular de los neumáticos son síntomas que merecen revisión.',
        'Anotá si el ruido aparece al frenar, doblar o circular a baja velocidad. Estas observaciones ayudan al técnico, aunque no sustituyen una inspección física.',
        'Cuando exista una pérdida marcada de control o un comportamiento peligroso, evitá circular y solicitá asistencia.'
    ]},
]
