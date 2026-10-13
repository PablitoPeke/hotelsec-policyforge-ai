# Centro de cuenta y preparacion para un piloto: 13/10/2026

## Objetivo y alcance

La version 0.4.0 incorpora autogestion de cuenta, una interfaz de ajustes por pestanas y controles adicionales de consumo de IA. Publicada en https://178-105-149-202.sslip.io/ desde el commit de despliegue `97cc81f`. Es un piloto academico mejorado, no una certificacion de seguridad ni una declaracion de producto comercial listo para datos reales.

## Uso de Mi cuenta

1. Entrar con la cuenta habitual y abrir **Mi cuenta**. Si aparece la interfaz anterior, recargar con Ctrl+F5.
2. En **Perfil**, modificar nombre y apellidos, organizacion y cargo; guardar o cancelar. Los cambios persisten y actualizan la identidad de la barra lateral. No cambian la titularidad ni el contenido historico de los analisis.
3. En **Seguridad**, introducir contrasena actual, nueva y confirmacion. La nueva debe tener entre 12 y 128 caracteres y ser diferente. Se revocan las sesiones anteriores y se emite una nueva para el navegador actual. No se guardan contrasenas en el navegador ni se devuelven en errores de validacion.
4. La lista de sesiones muestra navegador/sistema aproximado, fecha conocida y caducidad. No almacena IP ni el user-agent completo. Se puede cerrar una sesion ajena individual o todas las demas con contrasena. Las sesiones anteriores a la migracion muestran "Sesion anterior": no se inventa una fecha de creacion.
5. **Actividad** presenta nombres comprensibles de los eventos propios. **Mis datos** descarga perfil, alojamientos, snapshots, progreso y actividad en JSON con reautenticacion. Es portabilidad de datos, no el informe comercial: los informes del alojamiento siguen descargandose como PDF en **Informe**.
6. El borrado exige contrasena, escribir ELIMINAR y confirmar en un dialogo modal. Escape cancela, el foco permanece en el dialogo y vuelve al control anterior. El borrado afecta a la aplicacion; una copia privada anterior conserva su contenido hasta que se aplique la politica de retencion de backups.

La exportacion automatica admite hasta 1000 analisis y 10000 eventos de actividad; indica este ultimo limite. Para volumenes superiores hace falta un procedimiento administrativo. Las claves, hashes de contrasenas, sesiones y tokens CSRF no forman parte de la exportacion. Los campos personales son opcionales salvo el nombre; no se solicitan DNI, telefono ni datos de huespedes.

## Correo preparado, no contratado ni activado

Por decision del alumno, no se contrata proveedor. Sin SMTP, verificar/cambiar correo y recuperar acceso aparecen desactivados y el backend devuelve indisponibilidad, no simula envios. Nombre, organizacion, cargo, contrasena, sesiones y exportacion funcionan sin SMTP.

La integracion utiliza `smtplib`, `ssl` y `email` de la biblioteca estandar de Python, sin nuevas dependencias runtime. Variables privadas del servidor:

| Variable | Configuracion |
|---|---|
| SMTP_HOST | Host facilitado por el proveedor, sin URL ni credenciales |
| SMTP_PORT | Puerto del proveedor; normalmente 587 con STARTTLS o 465 con SSL |
| SMTP_MODE | `starttls` o `ssl`; sin modo de texto plano |
| SMTP_USERNAME / SMTP_PASSWORD | Credenciales privadas, ambas o ninguna si el relay lo permite |
| SMTP_FROM | Remitente autorizado y verificado con el proveedor |

No subir estos valores a GitHub ni enviarlos por chat. Antes de activarlo, revisar contrato, dominio, SPF/DKIM/DMARC y politica de tratamiento del proveedor. Recrear solo API con el mismo Compose/volumen y comprobar envio real con cuentas propias. El flag de capacidad indica configuracion presente, no garantiza que el proveedor acepte o entregue mensajes.

Los enlaces tienen secretos aleatorios, persistidos solo como SHA-256, un unico uso y expiracion: 15 minutos para recuperacion y 30 para verificacion/cambio. La URL se construye desde APP_URL, no desde Host. El secreto viaja en el fragmento, se retira de la barra del navegador y requiere confirmacion POST; un GET de un escaner de correo no consume el enlace. El cambio de correo requiere contrasena actual y confirmacion en **ambas** direcciones. Al completar cambio de correo o recuperacion se cierran todas las sesiones y se exige nuevo login. La solicitud de recuperacion ofrece la misma respuesta para una direccion existente o desconocida.

El envio se ejecuta en tareas de fondo del proceso: no hay cola persistente, reintentos ni garantia de entrega. Un fallo se registra sin destinatario, enlace, credencial ni contenido sensible. Los tests simulan SMTP; **no se ha probado entrega real**. La verificacion aun no es obligatoria para registrarse o usar la herramienta.

## Limites persistentes de IA

- `AI_REQUESTS_PER_HOUR=20`: peticiones de IA por cuenta y hora UTC fija.
- `AI_GLOBAL_DAILY_LIMIT=50`: peticiones compartidas entre todas las cuentas por dia UTC fijo; `0` desactiva las llamadas de pago. El analisis por reglas sigue disponible.
- Los contadores viven en PostgreSQL, con incremento condicional atomico y transaccion para ambos limites. Sobreviven al reinicio de API. Una peticion no valida no consume cuota; un intento reservado que falla o acaba en fallback si la consume.
- Una peticion de analisis completo puede realizar hasta tres llamadas al proveedor. Por tanto, **50 peticiones no significan 50 llamadas ni un techo monetario**. Configurar alertas y controles de gasto en el proveedor; esta version no implementa facturacion ni limites por tokens/dolares.
- La cuenta global no se borra al eliminar una cuenta. La limpieza administrativa elimina buckets caducados, no snapshots. Los limites de login y correo siguen en memoria por proceso: requieren un sistema compartido antes de escalar horizontalmente.

## Arquitectura y codigo editable

Frontend: React/TypeScript, componentes `AccountPanel`, `AccountAccess`, `PasswordInput` y `Modal`; CSS propio y Lucide. API: FastAPI/Pydantic; SQLAlchemy y Alembic para perfil, identificadores publicos de sesiones, tokens de correo y contadores. Argon2 conserva el hashing de contrasenas. No se usa un generador cerrado ni hace falta contratar software para editarlo en VS Code.

La migracion 0002 rellena identificadores de sesiones existentes y conserva hashes/CSRF. Tiene default de servidor para que una API anterior pueda seguir insertando sesiones al revertir una imagen. 0003 y 0004 crean tablas nuevas. El login y los cambios de credenciales se serializan con bloqueo de usuario en PostgreSQL. Las migraciones se aplican al iniciar API; no se borran volumenes ni se recrean cuentas.

## Backup y actualizacion

Se ejecuto `bash scripts/backup_production.sh` en el VPS antes de actualizar: pg_dump consistente, archivo de codigo, configuracion privada e imagenes API/web. Copia root-only en `/root/hotelsec-backups/p3-before-update-20261013T203952Z`, con SHA256 y comprobacion gzip. pg_restore termino correctamente en una base temporal distinta, que se elimino al terminar. La base en uso nunca fue sustituida. Es una copia en el mismo VPS, no cifrada ni externa; no protege frente a perdida total del servidor.

Antes y despues del upgrade se conservaron 1 usuario y 0 analisis; esquema 0001 paso a 0004. Las comprobaciones posteriores crean y borran solo sus cuentas ficticias. No se cambia la contrasena del alumno, su clave OpenAI, el volumen PostgreSQL ni el proxy Caddy. El cambio de contenedor tuvo una respuesta 502 transitoria, seguida de salud correcta; no se promete despliegue sin interrupcion.

## Verificacion de esta fase

Resultados detallados y fechas en `evidence/account-center-verification.json`, separados de la evidencia anterior 0.3.0. Backend: 92 tests superados, incluidos casos negativos, propiedad, tokens caducados/reutilizados, confirmacion doble, SMTP desactivado, cuotas concurrentes y compatibilidad de sesiones. Un aviso de deprecacion HTTPX/TestClient no invalida la pasada; conviene resolverlo en una actualizacion controlada. Build Docker TypeScript/Vite correcto.

Las pruebas de navegador cubren cinco escenarios: cuenta completa, movil/teclado, recuperacion desactivada/enlace invalido y dos recorridos completos previos con PDF/contradicciones. Pasadas finales: 5/5 local y 5/5 contra Hetzner, sin fallos, skips ni flaky. Capturas separadas en `evidence/account-center-local` y `evidence/account-center-hetzner`; las cuentas ficticias se eliminaron al terminar. Durante desarrollo hubo fallos: temp del sandbox inaccesible, proxy local conservando IP de contenedor anterior, enlace en pestana ya cargada no atendido y rate limit 429 al repetir demasiado pronto. Se corrigieron entorno/proxy/enlace y se respetaron los limites; no se desactivaron para aprobar. No publicar traces completos: pueden contener secretos de las cuentas de prueba.

No se han hecho llamadas de pago adicionales ni envio SMTP real. La prueba IA real de 0.3.0 se conserva como evidencia historica, no se atribuye como nueva prueba 0.4.0. GitHub Actions no se declara superado: la restriccion de facturacion administrativa observada anteriormente requiere revision de la cuenta.

## Antes de vender a un hotel

1. Configurar correo real y dominio controlado; probar verificacion, recuperacion y entrega. Introducir MFA/SSO y gestion de equipos/roles antes de ampliar acceso.
2. Definir responsable, avisos, terminos, retencion y acuerdos de tratamiento/subencargados con datos reales del operador. No declarar cumplimiento RGPD/ISO automatico ni usar datos de huespedes en esta demo.
3. Copias externas cifradas y programadas, retencion, alertas y simulacro de recuperacion de servicio completo, no solo pg_restore.
4. Mantenimiento del VPS, revision de firewall/SSH, monitorizacion, gestion de vulnerabilidades, logs y respuesta a incidentes.
5. Revision de seguridad independiente, pruebas de carga, accesibilidad y varios navegadores; cuotas compartidas de autenticacion y cola persistente de correo.
6. Acotar consumo/coste de IA y soporte al cliente. Revisar humanamente los informes antes de tratarlos como politicas aprobadas.

Referencias de diseno: [OWASP Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html), [OWASP Forgot Password](https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html) y [Python smtplib](https://docs.python.org/3/library/smtplib.html). Usarlas como guia no acredita conformidad integral.
