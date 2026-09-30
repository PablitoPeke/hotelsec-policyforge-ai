# Plan y registro de pruebas

## Base comprobada el 30/09/2026

Revision de codigo: `e7d1406`, sin cambios funcionales en este paso. Datos ficticios y clave OpenAI vacia en las pruebas; no se hicieron llamadas de pago ni conexiones al VPS.

| Comprobacion ejecutada | Resultado real | Alcance y limites |
|---|---|---|
| Pytest backend | 8 passed | Perfiles fuerte/debil, pack de politicas, health/raiz, fallback IA, texto y fusion. No demuestra todos los requisitos |
| TypeScript `npm run typecheck` | Superada | Tipado del frontend; no equivale a prueba visual ni de navegador |
| Entorno local backend | Restaurado | `.venv` no tenia pip/pytest; se instalo pip con ensurepip y dependencias existentes de `requirements.txt` |

Pytest emitio un aviso de deprecacion de AnyIO/Starlette y dos avisos de permisos para su cache. Los tests terminaron correctamente; la compatibilidad y los avisos se revisaran en el paso de dependencias.

Comando reproducible de backend desde la raiz en PowerShell:

```powershell
$env:PYTHONPATH="$PWD\backend"
$env:OPENAI_API_KEY=''
& .\backend\.venv\Scripts\python.exe -m pytest backend\tests -q
```

Comando de frontend desde `frontend/`: `npm run typecheck`.

## Casos a ejecutar durante el desarrollo

Todos los casos siguientes estan planificados, no superados. Cada ejecucion registrara fecha, version, entrada, resultado obtenido y evidencia; se documentaran tambien los fallos y su correccion.

| Prueba | Requisito | Accion | Resultado esperado |
|---|---|---|---|
| PR-01 | RF-01 | Completar perfil y todas las secciones con datos ficticios | Campos enviados, validados y recuperables sin perder respuestas |
| PR-02 | RF-02 | Perfiles fuerte, debil y limites; repetir misma entrada | Score 0-100 explicable, determinista y areas coherentes |
| PR-03 | RF-03 | Analizar controles ausentes y controles que no aplican | Riesgos con probabilidad/impacto/severidad y sin hallazgos inaplicables |
| PR-04 | RF-04 | Generar pack con y sin proveedor IA disponible | Politicas adaptadas, cobertura propuesta y origen/fallback identificado |
| PR-05 | RF-05 | Revisar recomendaciones y fuentes del resultado | Orientacion basica trazable sin afirmar cumplimiento certificado |
| PR-06 | RF-06 | Crear plan y cambiar estado de una accion | Plazos y campos completos; cambio persistente y limitado al propietario |
| PR-07 | RF-07 | Analizar y volver al dashboard | Metricas, tareas e historial coinciden con datos guardados |
| PR-08 | RF-08 | Exportar analisis extenso con acentos y todos los riesgos | PDF abre y es legible; incluye contenido completo, sin solapamientos ni cortes |
| PR-09 | RF-09 | Guardar analisis, reiniciar API/BD y recuperarlo | Entradas y resultados persistentes; migraciones aplicables desde cero |
| PR-10 | RF-10 | Guardar dos analisis fechados y abrir historial | Orden correcto y comparacion con resultados reales |
| PR-11 | RF-11 | Acceder sin sesion y con usuario ajeno a un analisis | Rechazo controlado y sin exposicion de datos del otro usuario |
| PR-12 | RF-12 | Texto complementario y texto que contradice MFA/backups manuales | Conserva datos no mencionados y pide/permite resolver contradicciones |
| PR-13 | RF-13 | Simular timeout, rechazo del proveedor y respuesta malformada | Resultado/estado controlado, origen claro y sin secretos ni traceback |
| PR-14 | RNF-01 | Instalar en entorno limpio solo siguiendo README | Flujo principal completo sin instrucciones externas al repositorio |
| PR-15 | RNF-02 | Numeros fuera de rango, JSON invalido, texto demasiado largo | 4xx controlado; el servicio sigue funcionando |
| PR-16 | RNF-03 | Revisar historial de Git, configuracion, hashes y acceso HTTPS | Sin secretos reales versionados; hashes seguros y transporte protegido |
| PR-17 | RNF-04 | Ejecutar auditorias de dependencias de frontend/backend | Informe fechado; hallazgos tratados o limitaciones justificadas |
| PR-18 | RNF-05 | Borrar datos de una cuenta y revisar politica de conservacion | Datos y accesos gestionados segun politica documentada |
| PR-19 | RNF-06 | Exceder limite de peticiones en laboratorio | 429 controlado y registro sin contenido sensible ni credenciales |
| PR-20 | RNF-07 | Verificar Compose y flujo completo en VPS propio | Version desplegada identificada; health, analisis e informe funcionan |
| PR-21 | RE-01 | Revisar PDF final pagina a pagina y contra matriz | 20-40 paginas de contenido, estructura completa y capturas reales |
| PR-22 | RE-02 | Revisar duracion, calidad y enlace del video en incognito | >=10 minutos, producto real y minutos exactos en matriz |
| PR-23 | RE-03 | Clonar version etiquetada y revisar accesibilidad | Tag final apunta a version entregada, README completo y licencia indicada |

## Registro de cada ejecucion

| Campo | Informacion que se registrara |
|---|---|
| ID y requisito | PR-XX y RF/RNF/RE relacionado |
| Version | Commit/tag y entorno |
| Pasos y entrada | Caso reproducible, datos ficticios |
| Esperado / obtenido | Comparacion concreta y mensaje/codigo de respuesta |
| Estado | Superada, fallida o superada con observacion |
| Evidencia | Test, log redactado sin secretos, captura y minuto real del video |
| Correccion | Commit de arreglo y nueva ejecucion si falla |
