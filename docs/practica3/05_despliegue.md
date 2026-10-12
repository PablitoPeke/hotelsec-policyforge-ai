# Instalacion y operaciones

## Local probado

Ver README para comandos. Compose crea PostgreSQL privado, API con migraciones, frontend compilado y proxy en `localhost:8085`. Usar siempre `--env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml`. El nombre historico del archivo no significa que esta configuracion HTTP sea apta para publicar cuentas reales.

## Hetzner con HTTPS: preparacion, no despliegue acreditado

No se ha tocado el VPS anterior. Antes de actualizar: confirmar que el servidor sigue siendo del alumno, su IP actual, dominio/subdominio y acceso SSH. No enviar claves privadas ni OpenAI por chat. Preservar la version de Practica 1 hasta haber probado la nueva y poder volver a ella.

1. Hacer copia de configuracion y datos de la instancia anterior; no publicar `.env`.
2. Crear registro DNS A del dominio hacia la IP confirmada; revisar AAAA si se usa IPv6.
3. En firewall del proveedor permitir 443/80 y SSH solo desde IP del administrador. No permitir 8000/5432. UFW no sustituye el firewall del proveedor para puertos publicados por Docker.
4. Clonar o actualizar rama `practica3` en directorio de prueba independiente del anterior.
5. Desde el checkout nuevo, ejecutar `python3 scripts/setup_production.py --domain TU_DOMINIO_REAL` (sustituir TU_DOMINIO_REAL). Crea `.env.production` con clave PostgreSQL aleatoria y permisos 600 en Linux, sin mostrar secretos. Rechaza dominios de ejemplo, IPs, rutas y archivos ya existentes; no sobrescribe claves. No editar el password de una DB existente sin cambiar tambien el usuario PostgreSQL. Alternativa manual: copiar `.env.production.example` y reemplazar sus ejemplos.
6. Revisar puertos ya ocupados: no detener un servicio anterior a ciegas. Coordinar el cambio del proxy y conservar volumentes/backups.
7. Arrancar:

```bash
docker compose --env-file .env.production -p hotelsec-p3-prod -f docker-compose.production.yml up -d --build
docker compose --env-file .env.production -p hotelsec-p3-prod -f docker-compose.production.yml ps
docker compose --env-file .env.production -p hotelsec-p3-prod -f docker-compose.production.yml logs --tail 50 api caddy
curl --fail https://TU_DOMINIO/api/v1/health
```

8. Verificar certificado sin excepciones del navegador, redireccion HTTP a HTTPS, cookie Secure/HttpOnly/SameSite, registro/login/analisis/PDF y denegacion con segunda cuenta. Probar desde incognito y otra red. Anadir fecha y capturas al registro de evidencias.

Caddy necesita dominio DNS correcto, acceso 80/443 y volumen `/data` persistente. Configuracion basada en documentacion oficial: https://caddyserver.com/docs/automatic-https. No se demuestra disponibilidad remota con que `docker compose config` sea valido.

## Comprobacion automatizada despues de publicar

Desde el PC con las dependencias del backend instaladas, ejecutar (PowerShell):

```powershell
backend/.venv/Scripts/python.exe scripts/verify_deployment.py --url https://TU_DOMINIO_REAL --confirm-test-data --output docs/practica3/evidence/deployment-remote-check.json
```

Solo hacerlo contra una instancia propia. Crea dos cuentas ficticias temporales y comprueba salud, cookies, autenticacion, CSRF, guardado, historial, progreso tras login, PDF y denegacion de lectura/edicion/borrado desde otra cuenta. Intenta eliminar ambas cuentas incluso si un paso falla; si falla la limpieza, el resultado global es fallo. No guarda claves, contrasenas, tokens ni contenido de informes en el JSON. No acepta HTTP remoto ni desactiva validacion TLS; no sigue redirecciones. Si el servidor deja de responder, puede no completar el borrado: revisar las cuentas de prueba desde administracion, sin borrar clientes.

Para repetirlo en local, cambiar URL a `http://localhost:8085` y salida a `deployment-local-check.json`. El script necesita HTTPX, incluido en las dependencias existentes; no requiere otra libreria. Los tests simulan tambien el caso IA exitoso: esa evidencia automatizada NO demuestra llamadas reales al proveedor.

## IA

Agregar OPENAI_API_KEY al archivo privado de la instancia elegida y recrear `api` con `up -d --force-recreate api`. No la incluyas en capturas ni comandos que se graben. La clave de Render no se transfiere automaticamente a Hetzner. La UI requiere marcar el consentimiento. Si la clave/modelo fallan se etiqueta `rules-fallback`: no es una respuesta IA exitosa.

Limite por defecto: 20 solicitudes de flujo IA/contexto por usuario/hora. Cada flujo consentido puede hacer extraccion, politicas y resumen (hasta tres llamadas); no equivale a 20 llamadas individuales. Los reintentos consumen cuota. No es un presupuesto monetario duro; configurar limites/alertas del proveedor. Un solo proceso de API.

Tras configurar tu clave de forma privada, puedes repetir el script de comprobacion con `--with-ai`. Esta opcion autoriza envio de datos ficticios y hasta tres llamadas que pueden consumir credito. Exige que extraccion, politicas y resumen indiquen exito OpenAI: un fallback hace fallar la prueba, aunque el resto de la app siga funcionando. Sin `--with-ai` no solicita IA. Conservar el informe real separado, por ejemplo `live-ai-check.json`; no cambiar los mocks por una supuesta llamada real.

## Administracion

Promover solo una cuenta propia ya registrada; no hay credenciales admin de fabrica:

```bash
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml exec api python -m app.manage grant-admin TU_CORREO
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml exec api python -m app.manage cleanup --audit-days 180
```

El segundo comando es simulacion. Revisar el recuento y, solo al querer aplicar el borrado, anadir `--apply`. En produccion cambiar archivo/proyecto/Compose coherentemente. Programar ejecucion diaria queda a cargo del operador; no esta instalada automaticamente.

## Backup y restauracion

No usar redireccion binaria de PowerShell antiguo con `pg_dump -Fc`; puede corromper el archivo. Crear backup dentro del contenedor y copiarlo:

```bash
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml exec db pg_dump -U hotelsec -d hotelsec -Fc -f /tmp/hotelsec.backup
docker cp hotelsec-p3-db-1:/tmp/hotelsec.backup ./hotelsec.backup
```

Es datos sensibles: cifrar y guardar fuera del VPS con acceso restringido; no subir al repositorio. El nombre de contenedor depende del proyecto; confirmar con `ps`.

Ensayar restauracion en base independiente vacia, nunca sobre la base viva sin aprobacion. Copiar el archivo al contenedor de prueba y usar `pg_restore -U hotelsec -d BASE_DE_PRUEBA /tmp/hotelsec.backup`. No utilizar `--clean` contra produccion. Comparar usuarios, snapshots, estados y migracion; comprobar acceso/PDF. Se ha realizado un ensayo local en DB independiente: 10 snapshots y checksum de sus bundles/estados coincidentes. La base temporal y su backup se retiraron, sin alterar la original. No se ha probado restauracion fuera de esa instancia ni acceso/PDF por una API apuntando a la restaurada; ver evidence/restore-check.json.

Actualizacion: revisar diff, ejecutar pruebas, backup, `up -d --build`, verificar. No usar `down -v`. En cambio incompatible de esquema, restaurar backup en instancia aislada y version anterior; no suponer que revertir Git deshace migraciones.
