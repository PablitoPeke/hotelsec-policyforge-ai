# Despliegue publico comprobado: 13/10/2026

## Direccion y alcance

https://178-105-149-202.sslip.io/ sirve HotelSec PolicyForge AI 0.3.0 en modo production, en el VPS Hetzner del alumno. El alumno autoriza este hostname basado en su IP, la reutilizacion privada de su clave OpenAI existente y una prueba real con datos ficticios. No se compro dominio ni se modifico facturacion.

El DNS se comprobo desde Windows y desde el VPS. Caddy obtuvo certificado publico Let's Encrypt, verificado desde Windows con TLS 1.3 y sin desactivar validacion. Su caducidad observada es 11/01/2027; Caddy configura renovacion automatica con volumen persistente, pero aun no se ha observado una renovacion. HTTP redirige a HTTPS; la IP HTTP antigua redirige al hostname correcto preservando ruta y query.

sslip.io depende de un tercero y de que la IP siga asignada al alumno. No es dominio propio ni garantia de disponibilidad. Documentacion de base: https://github.com/cunnie/sslip.io/blob/main/README.md y https://caddyserver.com/docs/automatic-https.

## Que se ha cambiado y por que

1. Backup privado de la version anterior, verificado sin pararla; ver `09_preparacion_hetzner.md`.
2. Checkout independiente en `/opt/hotelsec-policyforge-ai-practica3`, rama practica3; la carpeta antigua no se reemplaza.
3. `.env.production` generado con password PostgreSQL aleatorio y permisos 0600. La clave OpenAI se transfiere entre configuraciones dentro del VPS sin aparecer en chat, comandos publicos, frontend o GitHub.
4. Proyecto Compose `hotelsec-p3-prod`: DB, API y web solo en la red interna; PostgreSQL nuevo en volumen separado. Se comprueban migracion, salud y HTML antes de exponer puertos.
5. Se valida Caddy y se transfiere el trafico: se detiene solo el Nginx antiguo y arranca Caddy. Comprobacion HTTPS exitosa en unos segundos; no hizo falta ejecutar rollback. API y web anteriores siguen conservados.
6. Las pruebas remotas encuentran una carrera de navegacion y scroll heredado; correcciones pequenas, compilacion y actualizacion solo del frontend. La redireccion HTTP por IP se corrige y valida antes de recrear el proxy. DB y API no se recrean durante esas correcciones.

Codigo de interfaz final comprobado: `55ef12a887d099763c8035624488c949b966b40f`. Los commits posteriores solo de documentacion no cambian las imagenes en ejecucion. No se fusiono main ni se creo tag final.

## Pruebas y evidencia

| Comprobacion | Resultado | Archivo sanitizado |
|---|---|---|
| API publica sin IA | Salud, cookies Secure/HttpOnly/SameSite, CSRF, logout, historial/progreso, PDF y propiedad | evidence/deployment-remote-check.json |
| IA real autorizada | Extraccion, personalizacion de 10 politicas y resumen OpenAI, sin fallback; dos cuentas eliminadas | evidence/live-ai-check.json |
| Transporte | Certificado publico, redirecciones, assets y cabeceras; 8000/5432 no accesibles desde este cliente | evidence/transport-remote-check.json |
| Navegador final | 2 passed, 0 fallos/flaky/skips; escritorio y movil, persistencia/PDF, contradicciones y respuesta retenida | evidence/browser-remote-check.json |
| Primer intento de navegador | 1 fallo y 1 passed; fallo de navegacion reproducido y corregido, no ocultado | evidence/browser-remote-first-attempt.json |
| Estado del VPS | Cuatro contenedores nuevos, DB healthy, migracion 0001, proxy anterior detenido y preservado | evidence/runtime-remote-check.json |

Las capturas remotas estan en `evidence/hetzner`, separadas de las locales del 12/10. Las pruebas Chromium no solicitan IA: su indicador de reglas es correcto; la prueba real IA esta en su JSON separado. Los escenarios de navegador eliminan sus propias cuentas en afterEach, incluso si falla un paso; un fallo de limpieza hace fallar la prueba. Tras las comprobaciones, PostgreSQL tenia cero usuarios, analisis, companias y sesiones, sin borrar cuentas ajenas por consultas masivas.

No se registran contrasenas, cookies, tokens, contenido de proveedor ni claves en los JSON. No publicar traces completos de Playwright: pueden contener secretos de las cuentas ficticias.

## Uso y administracion

Crear una cuenta propia en la nueva URL, con contrasena de al menos 12 caracteres y datos de hotel ficticios. Las cuentas locales/Render no se migran automaticamente y no hay administrador de fabrica. El consentimiento IA es opcional y cada uso puede consumir credito. La cuota por usuario/hora no es limite monetario global; revisar alertas/presupuesto del proveedor antes de un uso real amplio.

Comandos de lectura en el VPS:

```bash
cd /opt/hotelsec-policyforge-ai-practica3
docker compose --env-file .env.production -p hotelsec-p3-prod -f docker-compose.production.yml ps
curl --fail https://178-105-149-202.sslip.io/api/v1/health
```

Para actualizaciones, revisar diff y hacer backup PostgreSQL, conservar nombre de proyecto/volumen y usar esta carpeta nueva. No arrancar el Compose antiguo sobre el puerto 80 ni usar `down -v`. No volver a generar o rotar el password de un volumen existente sin un procedimiento de cambio de credenciales en DB.

## Recuperacion y limites

El backup anterior permanece privado en `/root/hotelsec-backups/legacy-before-practica3-20261013T190017Z`. Es copia en el mismo VPS y no sustituye backup externo cifrado ni prueba de restauracion. PostgreSQL nuevo necesita su propia politica de backup; el backup de Practica 1 no contiene los futuros datos de Practica 3.

El procedimiento previsto si falla el cambio publico es detener Caddy nuevo y arrancar `hotelsec-policyforge-ai-nginx-1`, conservando ambos proyectos. Devuelve la app antigua HTTP, no restaura ni migra PostgreSQL nuevo. No se ejecuto como ensayo para evitar interrupcion innecesaria, ni se declara restauracion comprobada. Las imagenes anteriores del frontend nuevo tambien se etiquetaron antes de corregirlo.

Pendientes operativos: backup cifrado fuera del VPS y ensayo, mantenimiento del sistema, revision del firewall del proveedor y restriccion de SSH, monitorizacion, pruebas de rendimiento y revision integral de secretos/historial. No se ha reiniciado el VPS ni aplicado actualizaciones del sistema en esta fase. Esto es demostracion academica, no certificacion de seguridad ni despliegue listo para datos reales de clientes.

## Antes de entregar

El alumno debe revisar la nueva URL, comprender las correcciones, confirmar grupo/horas reales y grabar video/minutos. El borrador PDF actual es del 12/10 y aun no incorpora este despliegue: regenerarlo y revisarlo antes de entregar. Revisar el aviso de GitHub Actions, crear tag solo al cerrar, y comprobar enlaces/adjuntos en el campus. Publicar la app no equivale a haber entregado la practica.
