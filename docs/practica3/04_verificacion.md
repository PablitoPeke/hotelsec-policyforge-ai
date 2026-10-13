# Registro real de verificacion

Revision documental: 13/10/2026. Las pruebas locales son del 12/10: Windows, Docker Desktop Linux, Python de venv y Node 24 del runtime de desarrollo, con datos ficticios. No se repitieron al documentar la preparacion remota del 13/10. Se conservan las fechas originales de los ensayos de reinicio y restauracion del 30/09.

## Comprobaciones ejecutadas

| Comprobacion | Resultado comprobado | Limite de la evidencia |
|---|---|---|
| Backend y operaciones pytest | 50 passed, 0 fallos; XML conservado | SQLite temporal, HTTPX simulado; no implica pentest ni acierto semantico IA |
| Migraciones | SQLite vacia, upgrade head dos veces: prueba superada | PostgreSQL tambien arranco desde volumen nuevo, pero no se ensayan todos los downgrade |
| Build frontend | TypeScript y Vite 8: compilacion correcta en Node 24 y en Docker Linux | No prueba todos los navegadores |
| Playwright | 2 passed, Chromium; escritorio 1440x1000, detalles 1000x900 y movil 390x844 | Son dos escenarios amplios, no dos unidades; no es dispositivo movil fisico |
| Instalacion Compose | Cuatro servicios arrancados, PostgreSQL healthy y API 0.3.0 ok | Local; no acreditacion Hetzner actual |
| Persistencia tras reiniciar DB y API | 4 snapshots antes y 4 despues; salud API ok | Datos de prueba; no ensayo de desastre ni restauracion backup |
| Backup/restauracion local | pg_dump -Fc y pg_restore en DB nueva: 10 snapshots y checksum de bundles/estados coincidentes | Misma instancia local; no recuperacion externa ni login/PDF separado en la restaurada |
| pip-audit runtime | 0 vulnerabilidades conocidas en dependencias resueltas | No escaneo de imagen OS ni garantia de ausencia de vulnerabilidades |
| npm audit | 0 conocidas tras actualizar Vite y dependencias | Informe a fecha de ejecucion; repetir antes de entregar |
| Caddy validate | Configuracion valida | Aviso de formato y encabezado redundante; no emision de certificado publico |
| GitHub Actions | Ultimo run inspeccionado36773073650: failure; backend y frontend ejecutaron 0 pasos | Reconsultado el 12/10: restriccion administrativa de cuenta; no es un test fallido ni CI superado |
| Script de despliegue local | Salud, cookies, CSRF, historial/progreso tras login, PDF y aislamiento correctos; dos cuentas temporales eliminadas | API HTTP local; no acredita HTTPS remoto ni IA real |
| Configuracion produccion | Tests de DNS valido, rechazo de IP/ejemplos/rutas, secreto aleatorio y no sobrescritura | No se genero configuracion real de VPS ni certificado |
| Prueba manual del alumno | Pablo confirma el 12/10 que los pasos propuestos funcionan | Declaracion del alumno, no observacion independiente ni revision de cada linea |
| Acceso SSH remoto | El 13/10 entra con clave Ed25519 ya autorizada; el alumno tambien confirma acceso | La denegacion del 12/10 queda como antecedente; no se habilito password de root por SSH |
| Instancia anterior en Hetzner | Tres contenedores activos; salud 0.1.0 production antes y despues de la copia | No acredita publicacion de 0.3.0, HTTPS ni llamadas OpenAI reales |
| Backup previo en Hetzner | Codigo/configuracion, imagenes Docker y configuracion efectiva Nginx; gzip/tar/SHA256 correctos; permisos privados | Misma maquina, sin copia externa cifrada ni ensayo de restauracion |
| PDF cliente | Descargado por navegador; pypdf comprueba todos los riesgos y controles; etiquetas espanolas | No demuestra todas las combinaciones posibles de longitud |
| Memoria borrador | Renderizadas 27 paginas; 23 de contenido, cuerpo11, sin texto fuera de margenes | Faltan datos/horas/video y revision del alumno |

Backend cubre: perfiles iniciales, politicas, summary sin clave, fusion de texto, sesion, CSRF, rol, acceso cruzado de lectura/PDF/PATCH/DELETE, rate limit login, hashes, borrado de cuenta, guardado, acciones, entradas invalidas, timeout, estructura IA incorrecta, produccion insegura rechazada y no envio sin consentimiento. La respuesta OpenAI exitosa se simula con formato de Responses: extraccion, pack y resumen, tres llamadas; NO una prueba con clave real.

## Fallos encontrados durante desarrollo

1. Vite actualizado no construia con Node global 19 y faltaba binding nativo opcional. Solucion: Node 24 explicito e instalacion optional. Build posterior correcto; el alumno debe usar Node 24, no el global viejo.
2. Una prueba nueva importaba `test_product` en vez de `tests.test_product`: 1 fallo/21 passed. Se corrigio el import; ejecucion posterior 22 passed.
3. Dos primeras pruebas de navegador fallaron al localizar el campo contrasena: etiqueta agrupaba controles y ayuda. Se incorporo nombre accesible explicito. La siguiente pasada tuvo 1 fallo/1 passed por selector exacto de continuidad. Se corrigio el selector por rol; pasada posterior 2 passed.
4. Revision del contrato encontro respuesta del proveedor con output que no era objeto/lista; podia provocar AttributeError y 500. Se valida su estructura antes de extraer texto y se anaden casos negativos. Pasada posterior: 26 passed.

No se borran estos fallos del relato para aparentar una primera ejecucion perfecta. Los traces locales pueden contener cuentas y cookies de prueba: no publicarlos; guardar solo resultados sanitizados/capturas necesarias.

El 12/10 Docker Desktop estaba parado; se arranco sin reinstalar ni borrar volumenes. El primer build local fallo por permisos de escritura en la cache global de npm del entorno restringido; se uso una cache temporal y el build posterior paso. No fue un error TypeScript ni una prueba de usuario fallida. Los 23 tests nuevos verifican herramientas operativas, limpieza tras errores, origen HTTPS y exito/fallback simulado de IA. La prueba operativa real se ejecuto sin IA y paso.

El 13/10 se detecto que la consola habia transformado caracteres de una clave nueva y creado `authorized-keys`, distinto de `authorized_keys`. La clave previamente autorizada ya existia en el PC y su huella coincidio con el servidor. Se accedio con esa identidad, sin reemplazar claves ni cambiar sshd. El primer intento de backup se detuvo antes de escribir por cambios de Nginx; se inspeccionaron, eran configuracion/cache/PID, y se incluyo la configuracion efectiva en la copia posterior. La API no tenia cambios en su capa escribible. Ver `09_preparacion_hetzner.md` y los JSON sanitizados; no se publican secretos ni archivos de backup.

## Pendientes

Prueba OpenAI real consentida, recuperacion de backup fuera de la instancia, despliegue remoto HTTPS, instalacion por el alumno en segundo entorno, revision completa de secretos en historial, rendimiento/concurrencia, confirmacion de enlace de video y cierre de tag. GitHub Actions esta configurado y se comprobo por API: no inicia los jobs por restriccion de la cuenta; el titular debe resolverla y repetir la ejecucion. No puede acreditarse CI superado. Hay un aviso de deprecacion de TestClient/HTTPX; los tests locales pasan, pero debe revisarse esa compatibilidad al actualizar.
