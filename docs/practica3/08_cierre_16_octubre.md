# Cierre de entrega: 16 de octubre de 2026

Revision 12/10/2026. Autor confirmado: Pablo Cortes. Trabajo individual; numero de grupo todavia desconocido. Consultar la hora exacta en el campus: no asumir que el plazo termina a medianoche.

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
| Hetzner | SSH responde en la IP indicada, pero rechaza autenticacion automatica; no se ha cambiado el VPS |
| IA real | Pendiente clave en instancia elegida y prueba consentida; no se ha consumido credito en tests |
| Video / envio | Pendientes; no hay MP4 ni envio al campus acreditado |

## 1. Entrar al servidor, sin cambiar nada todavia

En Windows abrir PowerShell y escribir:

```powershell
ssh root@178.105.149.202
```

Es la IP que el alumno cree conservar; confirmar que coincide con el servidor activo en Hetzner Console. Usar la contrasena del servidor, no la de GitHub, OpenAI o Windows. Al escribirla no aparecen caracteres: es normal. No enviarla por chat.

Si aparece un aviso de huella nuevo o cambiada, verificar con el servidor/console antes de aceptar. No borrar known_hosts ni desactivar esa verificacion a ciegas. Si aparece `Permission denied`, no repetir muchas veces: revisar usuario, clave y acceso desde Hetzner Console. Si PowerShell no reconoce ssh, instalar el cliente OpenSSH de Windows o usar la consola web de Hetzner con ayuda.

Una vez dentro, ejecutar solo esta consulta de lectura:

```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Compartir solo su salida sin secretos. No pegar `.env`, `docker inspect`, `docker compose config`, cookies, contrasenas o claves. Antes de actualizar, se revisaran puertos, configuracion y copias. No ejecutar `down -v`, no reemplazar la instalacion anterior ni eliminar volumenes.

## 2. Elegir nombre publico y publicar con HTTPS

No hay dominio contratado; no se compra nada automaticamente. Para la demostracion puede usarse un nombre de DNS publico basado en IP, o registrar un subdominio gratuito. sslip.io documenta esta asignacion: https://github.com/cunnie/sslip.io/blob/main/README.md. Es dependencia de un tercero, no un dominio propio ni una garantia de disponibilidad; no equivale a un certificado emitido o un despliegue ya realizado. Confirmar opcion y DNS antes de aplicarla. Para clientes reales es preferible un dominio controlado por el operador.

Despues seguir `05_despliegue.md`: copia del despliegue anterior, checkout separado, configuracion generada sin sobrescribir secretos, revision de puertos, firewall, Caddy, prueba HTTPS y comprobacion con dos cuentas. Mantener posibilidad de volver a la version anterior. Conservar evidencia del resultado real; no reutilizar capturas locales como prueba del VPS.

## 3. Configurar y probar IA

Introducir OPENAI_API_KEY solo en el archivo privado del servidor/instancia local. No es la clave del usuario root. Recrear la API y ejecutar la comprobacion con `--with-ai` solo al consentir el gasto de hasta tres llamadas ficticias. El indicador de respaldo por reglas no cuenta como exito OpenAI. El informe nunca contiene la API key.

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
