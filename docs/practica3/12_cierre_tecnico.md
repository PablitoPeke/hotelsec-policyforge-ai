# Cierre tecnico y pasos personales restantes

Revision:13/10/2026. No se compra dominio ni SMTP. Se mantiene https://178-105-149-202.sslip.io/. El enunciado permite local/contenedores; la publicacion Hetzner adicional ya funciona. No hace falta seguir ampliando funcionalidades antes de entregar.

## Comprobado

- Version0.4.0 publicada; cambios de aplicacion congelados en83d7b9b. Las herramientas/documentos posteriores no alteran esa app.
- 99 tests backend/herramientas superados. Son92 de app/operaciones mas7 del cierre de entrega. Cinco recorridos Chromium en instalacion limpia y cinco remotos, con datos ficticios y limpieza.
- Clon limpio desde GitHub, configuracion nueva y PostgreSQL nuevo en proyecto separado: build, migraciones, API, PDF, historial, progreso y aislamiento comprobados. No se borra ni reutiliza la DB habitual.
- pip-audit/npm audit repetidos sin vulnerabilidades conocidas. Gitleaks8.30.1 sobre refs Git: dos falsos positivos revisados, cero accionables. No se publica el reporte crudo ni traces.
- HTTPS publico, cookies seguras, backup/restauracion aislada y prueba OpenAI real anterior autorizada documentados. El cierre no consume IA de pago.
- Memoria actualizada con cuenta/perfil, correo desactivado, cuotas persistentes, fuentes de evidencia y40 horas estimadas por Pablo. Se conserva la declaracion de asistencia IA.

Esto no equivale a pentest ni producto certificado para clientes reales. CI sigue bloqueado por facturacion, con0pasos; no se oculta y no se cambia la facturacion. La practica valora pruebas automatizadas pero no impone CI exitoso. SMTP real, MFA, backups externos y mantenimiento comercial son limites futuros declarados, no servicios contratados.

## Lo que falta de verdad

1. Video real MP4 >=10min y >=720p. Seguir `07_video_entrega.md`; aportar enlace accesible en incognito y los minutos exactos de cada requisito. No son los tiempos previstos del guion.
2. Numero de grupo del campus para portada y nombre obligatorio `P3_GrupoXX_Memoria.pdf`. Por peticion de Pablo, el PDF actual no muestra grupo; no se asigna uno ficticio.
3. Una persona ajena al grupo debe instalar desde README. El alumno confirma que todavia no ha ocurrido. Facilitar `13_prueba_persona_externa.md` y registrar su resultado real.
4. Pablo debe revisar el PDF y entender codigo/seguridad. Comprobar acceso del profesor al repo. Si es privado, invitar las cuentas docentes del campus.
5. Incorporar esos datos, regenerar/revisar PDF, commit final, tag v1.0-practica3 y envio al campus antes del cierre del16/10. No se crea el tag final sobre un documento sin video.

## Como cerrar al volver con el video

Los datos se editan en `docs/practica3/delivery_metadata.json`: grupo, horas estimadas, video, resolucion/duracion reales, timestamps MM:SS, comprobaciones de acceso y prueba externa. Los valores false/null son pendientes, no errores de app. No marcarlos true sin hacer la comprobacion.

Al incorporar el video, revisar tambien los parrafos de estado de `memoria_content.json` para que describan lo realmente realizado, y solo entonces marcar `narrative_updated_for_submission`. No basta cambiar flags o renombrar un PDF previo al video. La matriz Markdown debe reflejar igualmente el cierre y los minutos reales.

Desde la raiz:

```powershell
backend/.venv/Scripts/python.exe scripts/practice_delivery.py
backend/.venv/Scripts/python.exe scripts/generate_practica3_report.py --final
```

El segundo comando falla deliberadamente si faltan datos. Una vez completos produce `output/pdf/P3_GrupoNN_Memoria.pdf` con NN real. Revisar paginas/margenes antes de guardar commit; no crear una segunda rama ni modificar main para cerrar esta entrega. El tag debe incluir codigo y documentacion definitivos.

```powershell
git status --short
git add docs/practica3/delivery_metadata.json output/pdf/P3_GrupoNN_Memoria.pdf docs/practica3/evidence/memory-layout.json
git commit -m "docs: finalize practice 3 submission with real video evidence"
git tag -a v1.0-practica3 -m "Practice 3 submission"
git push origin practica3
git push origin v1.0-practica3
```

Sustituir NN por el grupo. Antes de crear tag, comprobar si existe: no reemplazar ni forzar uno publicado. Estos comandos quedan preparados, no se afirman ejecutados. Despues adjuntar PDF y enlaces repo/tag+video en portada y comentario de la tarea. Abrir enlaces y adjuntos, pulsar Entregar y comprobar confirmacion. No hace falta adjuntar ZIP con dependencias o configuraciones privadas.

## Sobre las horas

Se consignan las40horas como estimacion aproximada del alumno,10 por bloque. No se auditan a partir de commits ni tiempos de IA. Como orientacion de planificacion, un proyecto de este alcance con ayuda puede ocupar40-80horas de aprendizaje/trabajo personal, y bastante mas desde cero; esa horquilla es criterio orientativo, no sustituye la declaracion personal ni acredita horas realizadas.
