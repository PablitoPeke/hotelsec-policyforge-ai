# Registro real de verificacion

Fecha: 30/09/2026. Entorno local Windows, Docker Desktop Linux, Python de venv y Node 24 del runtime de desarrollo. Datos exclusivamente ficticios. Resultado final se completa con XML y resultados Playwright conservados en evidencias.

## Comprobaciones ejecutadas

| Comprobacion | Resultado comprobado | Limite de la evidencia |
|---|---|---|
| Backend pytest | 27 passed, 0 fallos; XML conservado | SQLite temporal, HTTPX simulado; no implica pentest ni acierto semantico IA |
| Migraciones | SQLite vacia, upgrade head dos veces: prueba superada | PostgreSQL tambien arranco desde volumen nuevo, pero no se ensayan todos los downgrade |
| Build frontend | TypeScript y Vite 8: compilacion correcta en Node 24 y en Docker Linux | No prueba todos los navegadores |
| Playwright | 2 passed, Chromium; escritorio 1440x1000, detalles 1000x900 y movil 390x844 | Son dos escenarios amplios, no dos unidades; no es dispositivo movil fisico |
| Instalacion Compose | Cuatro servicios arrancados, PostgreSQL healthy y API 0.3.0 ok | Local; no acreditacion Hetzner actual |
| Persistencia tras reiniciar DB y API | 4 snapshots antes y 4 despues; salud API ok | Datos de prueba; no ensayo de desastre ni restauracion backup |
| Backup/restauracion local | pg_dump -Fc y pg_restore en DB nueva: 10 snapshots y checksum de bundles/estados coincidentes | Misma instancia local; no recuperacion externa ni login/PDF separado en la restaurada |
| pip-audit runtime | 0 vulnerabilidades conocidas en dependencias resueltas | No escaneo de imagen OS ni garantia de ausencia de vulnerabilidades |
| npm audit | 0 conocidas tras actualizar Vite y dependencias | Informe a fecha de ejecucion; repetir antes de entregar |
| Caddy validate | Configuracion valida | Aviso de formato y encabezado redundante; no emision de certificado publico |
| GitHub Actions | Run36768106862: failure; backend y frontend ejecutaron 0 pasos | Jobs no iniciados por restriccion administrativa de cuenta; no es un test fallido ni CI superado |
| PDF cliente | Descargado por navegador; pypdf comprueba todos los riesgos y controles; etiquetas espanolas | No demuestra todas las combinaciones posibles de longitud |
| Memoria borrador | Renderizadas 27 paginas; 23 de contenido, cuerpo11, sin texto fuera de margenes | Faltan datos/horas/video y revision del alumno |

Backend cubre: perfiles iniciales, politicas, summary sin clave, fusion de texto, sesion, CSRF, rol, acceso cruzado de lectura/PDF/PATCH/DELETE, rate limit login, hashes, borrado de cuenta, guardado, acciones, entradas invalidas, timeout, estructura IA incorrecta, produccion insegura rechazada y no envio sin consentimiento. La respuesta OpenAI exitosa se simula con formato de Responses: extraccion, pack y resumen, tres llamadas; NO una prueba con clave real.

## Fallos encontrados durante desarrollo

1. Vite actualizado no construia con Node global 19 y faltaba binding nativo opcional. Solucion: Node 24 explicito e instalacion optional. Build posterior correcto; el alumno debe usar Node 24, no el global viejo.
2. Una prueba nueva importaba `test_product` en vez de `tests.test_product`: 1 fallo/21 passed. Se corrigio el import; ejecucion posterior 22 passed.
3. Dos primeras pruebas de navegador fallaron al localizar el campo contrasena: etiqueta agrupaba controles y ayuda. Se incorporo nombre accesible explicito. La siguiente pasada tuvo 1 fallo/1 passed por selector exacto de continuidad. Se corrigio el selector por rol; pasada posterior 2 passed.
4. Revision del contrato encontro respuesta del proveedor con output que no era objeto/lista; podia provocar AttributeError y 500. Se valida su estructura antes de extraer texto y se anaden casos negativos. Pasada posterior: 26 passed.

No se borran estos fallos del relato para aparentar una primera ejecucion perfecta. Los traces locales pueden contener cuentas y cookies de prueba: no publicarlos; guardar solo resultados sanitizados/capturas necesarias.

## Pendientes

Prueba OpenAI real consentida, recuperacion de backup fuera de la instancia, despliegue remoto HTTPS, instalacion por el alumno en segundo entorno, revision completa de secretos en historial, rendimiento/concurrencia, confirmacion de enlace de video y cierre de tag. GitHub Actions esta configurado y se comprobo por API: no inicia los jobs por restriccion de la cuenta; el titular debe resolverla y repetir la ejecucion. No puede acreditarse CI superado. Hay un aviso de deprecacion de TestClient/HTTPX; los tests locales pasan, pero debe revisarse esa compatibilidad al actualizar.
