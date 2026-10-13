# Preparacion remota comprobada: 13/10/2026

## Acceso sin debilitar SSH

El VPS del alumno responde en 178.105.149.202, nombre hotelsec. La configuracion efectiva de sshd permite claves y mantiene `PermitRootLogin without-password`: no se habilito contrasena de root para SSH. La clave Ed25519 que ya existia en el PC coincide con una clave del archivo correcto `authorized_keys`; se probo con IdentitiesOnly, BatchMode y verificacion estricta del host. El alumno confirma tambien acceso desde su PowerShell.

Durante los intentos manuales anteriores, la consola transformo caracteres y se creo un archivo `authorized-keys` con guion, no el archivo que SSH utiliza. No fue necesario sustituir claves ni eliminar ese archivo para entrar. No publicar claves privadas, passphrases ni contenidos de `.env`.

## Instalacion encontrada

- Directorio: `/opt/hotelsec-policyforge-ai`, rama main, commit `f11080acf00d61b3361d6fd57d809441bd1844b4`, sin cambios Git visibles.
- Tres contenedores del proyecto `hotelsec-policyforge-ai`: API, web y Nginx. Solo el proxy publica 80; API 8000 y web 80 son internos.
- Salud por proxy: 0.1.0, production, status ok. Esto acredita la instalacion antigua, no la version 0.3.0 de Practica 3.
- No se encontraron montajes persistentes ni DATABASE_URL en esos contenedores; el API no tiene cambios en su capa escribible. No se infiere por ello una garantia general de ausencia de datos o sistemas externos.
- UFW activo, permite 22/80/443 IPv4 e IPv6. No se ha inspeccionado el firewall del proveedor ni restringido SSH a la IP del administrador.
- Hay una clave OpenAI configurada en el API antiguo, pero no se mostro ni valido contra el proveedor. No se realizaron llamadas de pago.

## Copia privada creada

Ubicacion exclusiva de root:

```text
/root/hotelsec-backups/legacy-before-practica3-20261013T190017Z
```

Incluye el directorio del proyecto completo (con `.env` y Git), las tres imagenes Docker actuales, metadatos privados necesarios para identificar la configuracion efectiva y las configuraciones Nginx del web/proxy. La carpeta tiene permisos 0700 y todos sus archivos carecen de acceso para grupo/otros.

Se verificaron integridad gzip, lectura de los miembros tar, inclusion del entorno privado y Compose, y SHA256 de ambos archivos. La salud devolvio 0.1.0 ok antes y despues. No se detuvo, recreo ni actualizo ningun contenedor. Los cambios de Nginx se revisaron: configuracion generada, cache y PID; se guarda su configuracion efectiva y no se trata la cache como una base de datos.

Para comprobar de nuevo los hashes, en el servidor:

```bash
cd /root/hotelsec-backups/legacy-before-practica3-20261013T190017Z
sha256sum -c SHA256SUMS
```

Los archivos de copia y `containers.private.json` contienen configuracion sensible: no subirlos a GitHub, a capturas, al campus ni al video. El repositorio guarda solo `evidence/legacy-backup-check.json`, con metadatos sanitizados.

Limites: copia en el mismo VPS, no cifrada fuera de este, sin ensayo de restauracion. No se garantiza coherencia de una base externa ni captura de memoria volatil. No equivale a un plan completo de recuperacion de desastre.

## Siguiente fase autorizada

El alumno autoriza `178-105-149-202.sslip.io` como nombre para la practica. Depende de DNS de terceros; no se compra ni registra un dominio propio. Antes de publicar: revalidar DNS, crear checkout separado y volumen PostgreSQL nuevo, comprobar API/web internamente y coordinar la transferencia de 80/443 al proxy Caddy. Conservar el proyecto anterior y su proxy para rollback; no usar `down -v`, reemplazar el checkout antiguo o borrar volumenes.

Si el cambio publico falla, parar el Caddy nuevo y volver a arrancar el proxy Nginx anterior. No alterar las imagenes/configuracion antigua ni asumir que revertir Git deshace migraciones nuevas. La direccion autorizada no acredita todavia HTTPS emitido, publicacion de 0.3.0 ni exito real de OpenAI.

La memoria PDF sigue siendo el borrador del 12/10; esta fase se incorporara en su proxima regeneracion, sin cambiar las fechas de pruebas anteriores.
