# Instalacion y operaciones

## Local probado

Ver README para comandos. Compose crea PostgreSQL privado, API con migraciones, frontend compilado y proxy en `localhost:8085`. Usar siempre `--env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml`. El nombre historico del archivo no significa que esta configuracion HTTP sea apta para publicar cuentas reales.

## Hetzner con HTTPS: preparacion, no despliegue acreditado

No se ha tocado el VPS anterior. Antes de actualizar: confirmar que el servidor sigue siendo del alumno, su IP actual, dominio/subdominio y acceso SSH. No enviar claves privadas ni OpenAI por chat. Preservar la version de Practica 1 hasta haber probado la nueva y poder volver a ella.

1. Hacer copia de configuracion y datos de la instancia anterior; no publicar `.env`.
2. Crear registro DNS A del dominio hacia la IP confirmada; revisar AAAA si se usa IPv6.
3. En firewall del proveedor permitir 443/80 y SSH solo desde IP del administrador. No permitir 8000/5432. UFW no sustituye el firewall del proveedor para puertos publicados por Docker.
4. Clonar o actualizar rama `codex/practica3` en directorio de prueba independiente del anterior.
5. Crear `.env.production` a partir de `.env.production.example`. Reemplazar DOMAIN y clave PostgreSQL por secreto aleatorio hexadecimal. Permisos `chmod 600 .env.production`. No editar el password de una DB existente sin cambiar tambien el usuario PostgreSQL.
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

## IA

Agregar OPENAI_API_KEY al archivo privado de la instancia elegida y recrear `api` con `up -d --force-recreate api`. No la incluyas en capturas ni comandos que se graben. La clave de Render no se transfiere automaticamente a Hetzner. La UI requiere marcar el consentimiento. Si la clave/modelo fallan se etiqueta `rules-fallback`: no es una respuesta IA exitosa.

Limite por defecto: 20 solicitudes de flujo IA/contexto por usuario/hora. Cada flujo consentido puede hacer extraccion, politicas y resumen (hasta tres llamadas); no equivale a 20 llamadas individuales. Los reintentos consumen cuota. No es un presupuesto monetario duro; configurar limites/alertas del proveedor. Un solo proceso de API.

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
