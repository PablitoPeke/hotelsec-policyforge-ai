# Guion y cierre de entrega

Guion literal listo para leer, con acciones y alternativas: [14_guion_lectura.md](14_guion_lectura.md). Version de lectura en PDF: [P3_Guion_lectura_y_grabacion.pdf](../../output/pdf/P3_Guion_lectura_y_grabacion.pdf). Incluye16 bloques, datos ficticios exactos, comandos sin IA de pago, incidencias y hoja de minutos reales. La duracion prevista completa es17-20minutos; medir el MP4. La tabla breve inferior es antecedente orientativo, no un video ni evidencia temporal.

Este guion actualizado a0.4.0 propone14-16 minutos, NO es un video producido ni minutos reales de evidencia. Grabar la version probada, con datos ficticios y sin `.env`, API keys ni contrasenas. La URL publica puede mostrarse; no mostrar credenciales del VPS.

| Tiempo previsto | Demostracion real | Requisitos |
|---|---|---|
| 00:00-01:00 | Nombre del producto, objetivo hotelero, autor individual, 9/10 sin feedback, limites | Punto de partida |
| 01:00-02:00 | GitHub, rama/commits, README, Compose y salud del backend | RNF-01, RE-03 |
| 02:00-03:00 | Crear cuenta ficticia y explicar datos/rol hotel | RF-11, RNF-05 |
| 03:00-04:30 | Perfil, controles, temporada, sistemas, continuidad y texto propio | RF-01, RF-12 |
| 04:30-05:30 | Provocar contradiccion MFA; confirmar fuente; unico resultado | RF-12, RNF-02 |
| 05:30-06:30 | Madurez por areas, probabilidad/impacto estimados, limites del scoring | RF-02, RF-03 |
| 06:30-07:30 | Politicas, evidencia necesaria, fuentes RGPD/ISO, indicador reglas/IA | RF-04, RF-05, RF-13 |
| 07:30-08:30 | Cambiar accion a completada, recargar, volver al historial | RF-06, RF-07, RF-09 |
| 08:30-09:30 | Reevaluar mismo hotel y comparar; descargar/abrir PDF completo | RF-08, RF-10 |
| 09:30-11:00 | Mi cuenta: editar nombre/cargo y recargar; sesiones, actividad/exportacion y correo desactivado | RF-11, RNF-05 |
| 11:00-12:00 | Segunda cuenta sin historial ajeno; caso de error; explicar tests permisos/CSRF | RF-11, RNF-02, RNF-03 |
| 12:00-13:00 | 99 tests, auditorias, Gitleaks y limites IA20/50; CI bloqueado sin fingir exito | RNF-04, RNF-06 |
| 13:00-14:30 | Codigo editable, arquitectura, HTTPS/backup, limites y declaracion IA | RE-01, RE-03, RNF-07 |

Explicar con tus palabras: frontend es la pantalla; API valida y calcula; base guarda; proxy publica; migracion crea las tablas; sesion identifica la cuenta; CSRF comprueba que la peticion fue iniciada por ella. No memorizar afirmaciones de seguridad que no puedas demostrar.

## Antes de grabar

- Revisar cada cambio y poder ubicarlo en VS Code.
- Probar microfono y texto legible a 1080p; MP4 >=10 minutos, minimo 720p.
- Probar instalacion en otra maquina o un entorno limpio distinto; la prueba local asistida no sustituye revision del alumno.
- Si demuestras IA real, probarla antes y verificar etiqueta openai. Sin clave, explicar reglas; no llamar IA a una respuesta fallback.
- No grabar el borrado de la cuenta utilizada para el resto de la demo; crear una cuenta descartable para ese ejemplo.

## Finalizar memoria

Autor Pablo Cortes, individual. Grupo omitido por ahora a su peticion; confirmar antes de entregar. Las40horas son su estimacion aproximada. Incorporar URL y minutos reales a delivery_metadata.json; el generador final valida pendientes. La memoria previa al video ya incorpora0.4.0, evidencia remota diferenciada y cuenta. Mantener20-40paginas de contenido y revisar el PDF regenerado. El alumno confirma la web publica, no grabacion ni revision de cada linea. Ver12_cierre_tecnico.md y13_prueba_persona_externa.md.

Crear tag `v1.0-practica3` sobre el commit realmente final, con repo/video/enlaces accesibles. La rama actual no se ha fusionado automaticamente a main para preservar la entrega anterior.

## Subir al campus

1. Abrir la tarea Practica 3 del campus utilizado por Evolve. Confirmar hora limite del 16/10/2026 y si se usa Classroom u otra plataforma.
2. Adjuntar `P3_GrupoXX_Memoria.pdf` (XX debe ser tu grupo real, no literal).
3. Subir el MP4 donde permita acceso al docente y comprobar el enlace en incognito. No dejarlo restringido solo a tu usuario.
4. Anadir en comentario los enlaces al repositorio con tag y al video; ambos deben estar tambien en portada.
5. Revisar los adjuntos abriendolos; pulsar Entregar/Enviar y comprobar el estado de entrega y confirmacion.

No esta entregado por generar archivos localmente. No se ha subido nada al campus en esta fase.
