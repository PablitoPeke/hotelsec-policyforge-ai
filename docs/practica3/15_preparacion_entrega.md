# Preparacion de entrega individual

Revision: 16/10/2026. Autor: Pablo Cortes. Sin numero de grupo por indicacion
explicita del alumno; no se inventa uno. Confirmar que el campus acepta el
nombre individual `P3_Pablo_Cortes_Memoria.pdf`.

## Confirmado

- GitHub tiene `main` y `practica3`. No hay una rama llamada Codex.
- Lectura HTTPS del repositorio comprobada sin credenciales el 16/10.
- La ruta que empieza por `PS C:\...` es una carpeta de PowerShell, no una rama.
- El alumno confirma el MP4 `2026-10-16 19-41-38.mp4` como definitivo.
  Sus propiedades locales indican 1134.066 segundos (18:54), 1920x1080,
  60fps y dos canales de audio. Se conservan sin modificar el archivo.
- Carlos Cortes instalo el 15/10/2026 siguiendo el README y todo funciono,
  segun declaracion de Pablo. Los detalles no comunicados no se inventan.
- La prueba de seguridad del 16/10 esta en
  `evidence/recording-security-check.json`: `passed: true`, sin IA y con
  eliminacion confirmada de las dos cuentas temporales.

## Falta para la entrega definitiva

AVISO: el muestreo visual del video detecta contrasenas visibles cerca de
15:30 en el formulario de Seguridad. No subir el original. Ocultar esas
zonas en una copia con aviso de proteccion, o volver a grabar el fragmento.
Cambiar cualquier contrasena expuesta que se haya utilizado. No se
transcriben ni se guardan sus valores en la documentacion.

Se ha creado `HotelSec_Practica3_Demo_segura.mp4` en la carpeta Videos.
Oculta los campos identificados de 15:22 a 15:36, con aviso visible de
edicion. Conserva audio y resultados, sin cortes; la salida es 1080p/30fps,
18:54.134. El hash del original se conserva intacto. La salida tiene revision
visual muestreada; falta que Pablo reproduzca el archivo completo antes de
publicarlo. Ver `evidence/video-redaction.json` y la herramienta editable
`scripts/protect_practice_video.py` (requiere FFmpeg local con drawtext).

1. Revisar el contenido del MP4, audio, legibilidad y ausencia de secretos.
2. Subirlo a Drive/YouTube u otro servicio equivalente, permitir acceso por
   enlace y comprobarlo sin iniciar sesion. Incorporar el enlace a portada.
3. Registrar los minutos observados de cada requisito, no los del guion.
4. Actualizar los parrafos de la memoria, generar y revisar el PDF definitivo.
5. Comprobar acceso del profesor al repo y crear el tag `v1.0-practica3`
   sobre el commit que contenga la entrega real. No crear un tag final antes.
6. Adjuntar PDF y enlaces a video y GitHub en el campus; comprobar que la
   tarea quede entregada. Confirmar la hora de cierre real en el campus.

## Nombres y autoria

Se permiten nombres profesionales para carpetas, ventanas y ramas. Se
mantienen la declaracion de asistencia IA, la integracion OpenAI del producto
y el historial real. No se reescriben commits para aparentar otra autoria.

La copia de entrega no debe incluir `.env`, claves, entornos Python,
`node_modules`, bases de datos privadas ni cuentas del VPS. El codigo
versionado y las instrucciones de instalacion permanecen en GitHub.

Se ha creado una copia limpia de la rama `practica3` en
`C:\Users\ironm\Documents\hotelsec-policyforge-ai`. La carpeta anterior se
conserva para no romper el entorno local ni rutas ya utilizadas. La copia
limpia contiene los archivos versionados, no dependencias ni configuracion
privada; seguir el README si se quiere ejecutarla localmente desde cero.
