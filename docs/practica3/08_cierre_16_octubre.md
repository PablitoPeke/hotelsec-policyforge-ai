# Cierre de entrega: 16 de octubre de 2026

Revision 13/10/2026. Autor confirmado: Pablo Cortes. Trabajo individual; numero de grupo todavia desconocido. Consultar la hora exacta en el campus: no asumir que el plazo termina a medianoche.

## Estado actual

| Bloque | Situacion real |
|---|---|
| App y codigo editable | Rama practica3, version 0.3.0; main conserva Practica 1 |
| Prueba manual | Pablo confirma el 12/10 que los pasos propuestos funcionaron; declaracion, no observacion independiente |
| Pruebas locales repetidas | 50 tests backend/operaciones, 2 escenarios Chromium, build frontend correcto |
| Dependencias | npm/pip-audit: cero vulnerabilidades conocidas en la revision actual |
| Comprobacion operativa | Script local superado; dos cuentas temporales eliminadas |
| Memoria | Borrador con nombre confirmado; pendientes grupo, horas, video/minutos y revision final |
| GitHub Actions | Jobs sin arrancar por bloqueo de facturacion; requiere accion del titular |
| Hetzner | 0.3.0 publicada por HTTPS en sslip.io; API y navegador remoto comprobados; backup anterior conservado |
| IA real | Clave reutilizada privadamente con autorizacion; tres etapas exitosas con datos ficticios; esta prueba si puede consumir credito |
| Video / envio | Pendientes; no hay MP4 ni envio al campus acreditado |

## 1. Entrar al servidor, sin cambiar nada todavia

En Windows abrir PowerShell y escribir:

```powershell
ssh -i "$env:USERPROFILE\.ssh\hotelsec_hetzner" -o IdentitiesOnly=yes root@178.105.149.202
```

La IP y la clave publica existente se confirmaron el 13/10; el alumno tambien probo este acceso desde PowerShell. Root usa `PermitRootLogin without-password`: no acepta su contrasena por SSH. La consola web de Hetzner sigue siendo acceso de respaldo. No enviar la clave privada ni contrasenas por chat. Si se protegio una clave con passphrase, esa frase desbloquea la clave local, no es la contrasena de root. El archivo nuevo `authorized-keys` creado durante el diagnostico no es el archivo utilizado por SSH y no se necesita para este acceso.

Si aparece un aviso de huella nuevo o cambiada, verificar con el servidor/console antes de aceptar. No borrar known_hosts ni desactivar esa verificacion a ciegas. Si aparece `Permission denied`, no repetir muchas veces: revisar usuario, clave y acceso desde Hetzner Console. Si PowerShell no reconoce ssh, instalar el cliente OpenSSH de Windows o usar la consola web de Hetzner con ayuda.

Una vez dentro, ejecutar solo esta consulta de lectura:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Compartir solo su salida sin secretos. No pegar `.env`, `docker inspect`, `docker compose config`, cookies, contrasenas o claves. Antes de actualizar, se revisaran puertos, configuracion y copias. No ejecutar `down -v`, no reemplazar la instalacion anterior ni eliminar volumenes.

## 2. Elegir nombre publico y publicar con HTTPS

No hay dominio contratado; no se compra nada automaticamente. El 13/10 el alumno autoriza `178-105-149-202.sslip.io` para la demostracion. sslip.io documenta esta asignacion: https://github.com/cunnie/sslip.io/blob/main/README.md. Es dependencia de un tercero, no un dominio propio ni una garantia de disponibilidad; la autorizacion no equivale a un certificado emitido o un despliegue ya realizado. Verificar DNS antes de aplicarlo. Para clientes reales es preferible un dominio controlado por el operador.

Fase realizada el 13/10: https://178-105-149-202.sslip.io responde 0.3.0 production con certificado Let's Encrypt valido, cookies seguras y datos separados. La IP antigua HTTP redirige al hostname. Se conservan backup, checkout y contenedores anteriores para recuperacion. Revisar pruebas/limites reales en `10_despliegue_publico.md`; el alumno debe crear una cuenta propia y repetir su demostracion en esa URL.

Despues seguir `05_despliegue.md`: copia del despliegue anterior, checkout separado, configuracion generada sin sobrescribir secretos, revision de puertos, firewall, Caddy, prueba HTTPS y comprobacion con dos cuentas. Mantener posibilidad de volver a la version anterior. Conservar evidencia del resultado real; no reutilizar capturas locales como prueba del VPS.

## 3. Configurar y probar IA

Introducir OPENAI_API_KEY solo en el archivo privado del servidor/instancia local. No es la clave del usuario root. Recrear la API y ejecutar la comprobacion con `--with-ai` solo al consentir el gasto de hasta tres llamadas ficticias. El indicador de respaldo por reglas no cuenta como exito OpenAI. El informe nunca contiene la API key.

Fase realizada el 13/10 con autorizacion explicita: reutilizacion privada de la clave existente y prueba con datos ficticios exitosa en las tres etapas. Ver `evidence/live-ai-check.json`. No repetir llamadas de pago solo para regenerar documentos; el resultado no garantiza semantica ni presupuesto duro. Configurar presupuesto/alertas del proveedor antes de abrir uso real amplio.

## 4. Preparar video y PDF

- Confirmar numero de grupo en campus o con el profesor; trabajar solo no implica automaticamente grupo 01.
- Anotar horas personales reales por actividad; no inventarlas a partir de commits o tiempos del asistente.
- Ensayar el guion `07_video_entrega.md`, comprender el codigo y grabar MP4 de al menos 10 minutos y 720p, preferiblemente 1080p.
- Probar permisos del enlace del video en incognito; anadir URL y minutos reales a portada y matriz.
- Actualizar `memoria_content.json` y regenerar con `python scripts/generate_practica3_report.py` desde un entorno con las dependencias de documentos.
- Renderizar y revisar el PDF completo; mantener 20-40 paginas de contenido, cuerpo 11/12 y anexos separados. No renombrar un borrador como final sin revisarlo.

La declaracion de asistencia IA se mantiene. No crear un video ficticio ni presentar minutos del guion como minutos grabados.

## 5. Cerrar GitHub y entregar

Resolver el aviso de facturacion desde la cuenta propia de GitHub y volver a ejecutar el workflow. No se ha contratado otro plan ni modificado facturacion. Si no se resuelve a tiempo, declarar la limitacion y aportar los resultados locales sin afirmar CI superado.

Solo tras revisar la version definitiva: commit final, tag `v1.0-practica3`, subida del tag y comprobacion de acceso. No fusionar a main sin decidirlo: conserva la Practica 1. Adjuntar PDF con numero de grupo real y enlaces al repo/tag y MP4 en la tarea del campus. Abrir adjuntos, pulsar Entregar y comprobar confirmacion.

Plan recomendado: acceso/despliegue/IA cuanto antes; video y memoria antes del dia 15; revision final y subida con margen respecto a la hora del dia 16. Este plan no constituye una automatizacion ni una entrega realizada.
