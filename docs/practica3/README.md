# Practica 3: del prototipo al producto

## Referencia de esta entrega

Fuente: `Practica_3_Evolve (1).pdf`, enunciado de Evolve Academy de 12 paginas facilitado por el alumno. Se conserva fuera del repositorio.

- Fecha limite: 16 de octubre de 2026; la hora de cierre se consultara en el campus.
- Producto: HotelSec PolicyForge AI, continuacion de la Practica 1.
- Nota anterior: 9/10, comunicada por el alumno.
- Feedback docente: el alumno indica que no recibio comentarios.
- Equipo: una persona, Pablo; numero de grupo y nombre para portada pendientes de confirmar.
- Inicio de revision: 30 de septiembre de 2026.
- Commit inicial revisado: `e7d140600f3d6be9517effe73c68a1e578cfc575`.

El enunciado denomina esta entrega Practica 3. El roadmap anterior la llamaba Practica 2: se mantiene como antecedente, sin cambiar retroactivamente la entrega anterior.

## Entregables que exige el enunciado

1. Memoria PDF de 20 a 40 paginas de contenido, sin contar portada, indice ni anexos. Cuerpo de 11 o 12 puntos, paginas numeradas y capturas legibles con requisito y pie. Nombre: `P3_GrupoXX_Memoria.pdf`.
2. Video MP4 de al menos 10 minutos, 720p como minimo (1080p recomendado). Demostracion real, incluyendo errores y seguridad; enlace accesible para el docente y probado en incognito.
3. Repositorio GitHub con instalacion reproducible, configuracion ficticia, pruebas, licencia si es publico y etiqueta final `v1.0-practica3`.

La memoria debe contener, en el orden indicado: portada; resumen ejecutivo (maximo una pagina); punto de partida; requisitos; arquitectura y decisiones; funcionalidades; seguridad; pruebas y evidencias; matriz de trazabilidad; limitaciones; reparto del trabajo; uso de IA; anexos. Se incluira tambien indice.

La matriz relacionara cada requisito con codigo, prueba, figura/apartado de memoria y minuto exacto del video. Se cumplimentaran minutos y resultados cuando existan; no se inventaran.

La entrega sera un unico envio en la tarea Practica 3 del campus, con PDF y enlaces al video y GitHub en portada y comentario. El despliegue publico no es obligatorio en esta nueva practica, pero se revisara el compromiso previo de Hetzner. Su disponibilidad actual no se ha comprobado en esta fase.

## Revision inicial

Material leido: memoria PDF final de la Practica 1, propuesta inicial, documentos de funcionalidades/modelo de datos/roadmap y codigo actual.

| Area | Situacion encontrada | Consecuencia |
|---|---|---|
| Formulario y scoring | API con validacion Pydantic, puntuacion global, areas y riesgos | Conservar la base y ampliar cobertura de campos/casos de error |
| Dashboard | Muestra el resultado de la sesion actual | Faltan historial persistente y seguimiento de acciones |
| Politicas | Generacion por reglas en `policy_service.py` | La IA no redacta actualmente el pack de politicas, pese a la propuesta |
| IA | Interpreta texto y redacta resumen; dispone de alternativa por reglas | Probar errores del proveedor, contradicciones y distinguir inferencias de hechos |
| Fusion manual/texto | Combina muchos booleanos con OR y conserva la frecuencia de backup mas alta | Una negacion en el texto puede no corregir un control marcado; requiere resolucion explicita |
| Datos | Resultados en estado React; no hay capa de persistencia | Los analisis se pierden al recargar y no hay comparativa temporal |
| Usuarios | Configuracion de JWT prevista, sin login ni permisos implementados | Hace falta autenticar y aislar los analisis por propietario |
| PDF cliente | Generador propio en navegador con contenido resumido | Falta incluir todo el perfil, resumen IA y contenido completo prometido |
| Despliegue | Dockerfiles, Compose Hetzner y Nginx HTTP | Revalidar desde cero y revisar HTTPS antes de usar datos reales |
| Memoria anterior | PDF de 5 paginas | Nueva memoria con evidencias reales y estructura/extension del enunciado |
| README | Mezcla tecnologias previstas con presentes | Documentar stack real e instalacion completa |

Estos hallazgos son una revision del codigo, no una auditoria completa de seguridad. No hay requisitos descartados en este punto.

## Orden de trabajo

| Paso | Trabajo | Evidencia para cerrarlo |
|---|---|---|
| 1 | Revision, requisitos numerados y pruebas iniciales | Estos documentos y commit separado |
| 2 | PostgreSQL, modelos y migraciones | Datos que sobreviven a un reinicio y pruebas de persistencia |
| 3 | Usuarios, sesiones y permisos | Login funcional y pruebas de acceso cruzado denegado |
| 4 | Guardado, consulta e historial desde frontend | Flujo completo autenticado con comparativa de analisis |
| 5 | Completar campos, riesgos, politicas y plan de accion | Requisitos originales cubiertos y cambios justificados |
| 6 | IA y PDF completos | Pruebas de fallos/contradicciones y PDF legible con datos coherentes |
| 7 | Seguridad e instalacion limpia | Amenazas, auditorias de dependencias, secretos y pruebas negativas |
| 8 | Memoria, video y entrega | Evidencias finales, minutos reales, enlaces y tag |

Cada paso tendra explicacion, codigo/documentacion editable, comprobaciones y commits pequenos. La persistencia se prepara primero; no se publicaran endpoints de historial con datos de clientes antes de incorporar permisos.

Calendario orientativo, sujeto a disponibilidad del alumno: hasta el 2/10, persistencia y usuarios; del 3 al 9/10, flujos completos y requisitos pendientes; del 10 al 12/10, seguridad y pruebas; del 13 al 15/10, congelar version, grabar y cerrar memoria; 16/10, entrega antes del cierre del campus. La carga se revisara tras cada paso.

## Documentos de seguimiento

- [Matriz de requisitos](01_matriz_requisitos.md).
- [Plan y registro de pruebas](02_plan_pruebas.md).
- Antecedente: [roadmap anterior](../11_practica2_roadmap.md).

## Incremento implementado

Usuarios/sesiones, DB/migracion, snapshots, historial, acciones y PDF completo estan implementados en `practica3`. La instalacion local con PostgreSQL esta en http://localhost:8085. Los tests locales cubren 27 casos de backend y 2 escenarios de navegador; auditorias npm/pip-audit: cero vulnerabilidades conocidas a fecha de ejecucion. Ver resultados estructurados, no asumir equivalencia con un pentest.

- [Arquitectura y STRIDE](03_arquitectura_seguridad.md).
- [Verificacion, fallos y limites](04_verificacion.md).
- [Despliegue y operaciones](05_despliegue.md).
- [Estado de entrega y trazabilidad actual](06_estado_entrega.md).
- [Guion de video y envio al campus](07_video_entrega.md).
- [Memoria borrador](../../output/pdf/HotelSec_P3_Memoria_borrador.pdf): 23 paginas de contenido, 27 totales, cuerpo11. Fuente editable `memoria_content.json`; generador `scripts/generate_practica3_report.py`.

No esta cerrada la entrega: grupo/nombre, horas reales, revision personal, video/minutos, IA real, segundo entorno y revalidacion remota pendientes. No se ha creado el tag final ni publicado esta version en Hetzner. Las decisiones sobre tecnologias alternativas estan documentadas; los documentos de revision inicial se mantienen como evidencia del punto de partida.

## Informacion pendiente

- Numero de grupo y nombre completo que debe aparecer en portada.
- Enlace del video, cuando se grabe, y minutos de demostracion.
- Horas reales del alumno: registrarlas por sesion, no sustituirlas por estimaciones ficticias.
- Confirmar al cerrar que la memoria final de Practica 1 del repositorio es la misma que se subio al campus.

## Uso de IA

Codex se utiliza como asistente para revisar, planificar, implementar, probar y redactar documentacion. OpenAI se integra en el producto para texto libre y resumen. El alumno revisara los cambios y debera poder explicar codigo, decisiones y limitaciones. Esta declaracion se ampliara con las tareas efectivamente realizadas.
