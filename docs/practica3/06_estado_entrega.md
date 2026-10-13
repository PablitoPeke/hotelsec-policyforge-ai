# Estado y trazabilidad del incremento

Las figuras son capturas locales reales de Chromium en `evidence`. Los minutos del video estan TODOS pendientes: no usar tiempos del guion como prueba real.

Revision 13/10/2026: nombre confirmado Pablo Cortes, trabajo individual; grupo y horas pendientes. El alumno comunica prueba manual local correcta. Las pruebas del 12/10 suman 50 tests backend/operaciones y 2 escenarios locales. El 13/10 se publica 0.3.0 en Hetzner con HTTPS, PostgreSQL nuevo y backup de la anterior. Pasan API remota, tres etapas OpenAI reales y dos escenarios Chromium remotos, tras corregir navegacion/scroll. La revision manual del alumno en la nueva URL sigue pendiente. Ver `10_despliegue_publico.md`.

| ID | Implementacion | Prueba ejecutada / evidencia | Estado de cierre |
|---|---|---|---|
| RF-01 | AssessmentForm, formAdapter, schemas/assessment | test_input_errors; Playwright formulario; figura 01 | Implementado y probado localmente |
| RF-02 | assessment_service | perfiles bajo/alto; reevaluacion navegador; figura 02 | Implementado; heuristico, no auditoria |
| RF-03 | schema RiskFinding, AssessmentResults | bundle/PDF y figura 02 | Implementado; estimaciones 1-5 |
| RF-04 | policy_service, enrich_policies | pack10, respuesta simulada/fallbacks y live-ai-check.json exitoso | Implementado; prueba OpenAI real 13/10 |
| RF-05 | product_service SOURCES | PDF AEPD, UI informe | Orientacion implementada; sin certificacion |
| RF-06 | bundle actions, records PATCH | test_full_flow, Playwright progreso; figura 04 | Implementado |
| RF-07 | App dashboard | Playwright escritorio/movil; figuras 02/07 | Implementado |
| RF-08 | report_service, records report.pdf | pypdf todos riesgos, descarga E2E; informe_ejemplo.pdf | Implementado; ver revision visual |
| RF-09 | db, migracion0001, records | SQLite sesion independiente, Compose DB nueva, reinicio4/4 | Implementado |
| RF-10 | history/filter, comparativa App | test_company_history y reevaluacion E2E; figura03 | Implementado; compara con anteriores de pagina cargada |
| RF-11 | auth, security, owned_record | isolation_of_all_record_routes; permisos rol/CSRF | Implementado; no MFA/SSO |
| RF-12 | parse_description, dialogo App | conflicto409/manual-text, optout; figura06 | Implementado; comprension general no garantizada |
| RF-13 | generate_ai_executive_summary | timeout/success simulados y proveedor OpenAI real comprobado | Implementado; prueba real puntual |
| RNF-01 | Compose, setup_local, README | local y segundo entorno Hetzner instalado; build Node24 | Probado automatizado; revision manual remota pendiente |
| RNF-02 | Pydantic, errors, limites proxy | 422/413/404, error UI, proveedor malformado | Implementado y tests negativos |
| RNF-03 | Argon2, env privados, production validator, Caddy | hash, CSRF, rol, certificado publico y cookies Secure comprobados | Revision completa de secretos en historial pendiente |
| RNF-04 | pip-audit/npm audit, workflow, Dependabot | informes JSON0conocidas; CI comprobado sin arrancar | CI bloqueado por restriccion de cuenta; imagenes pendientes |
| RNF-05 | privacy notices, DELETE cuenta, manage cleanup | cascada probada; instrucciones conservacion | Parcial: politica backups/temporizador operador |
| RNF-06 | ai_quota, audit, timeout | rate auth, audit, failure/success proveedor | Parcial: cuota por proceso, sin presupuesto duro |
| RNF-07 | production Compose, guia Hetzner | 0.3.0 HTTPS, transporte/API/Chromium remotos y backup anterior | Publicado y comprobado 13/10; no garantia de uptime |
| RE-01 | memoria fuente y generador | PDF borrador con nombre confirmado, figuras y pruebas | Pendiente grupo/horas/minutos y revision final |
| RE-02 | guion07 | No hay MP4 nuevo | Pendiente grabacion >=10min y URL |
| RE-03 | commits, README, MIT, CI | rama practica3 subida; CI remoto sin ejecutar | Pendiente resolver bloqueo CI, cierre/revision/tag final |

## Comprobacion del alumno antes de cierre

Confirmar grupo, completar horas reales, comprender codigo, probar personalmente la nueva URL, ensayar/grabar video, comprobar permisos de enlaces en incognito, ajustar minutos exactos, regenerar/revisar PDF y crear tag solo al terminar. Despliegue e IA ya tienen evidencia automatizada real del 13/10, no sustituyen la revision del alumno ni el video. El PDF del 12/10 aun no los incorpora. El paquete actual no se etiqueta ni se presenta como entrega final.

La comparativa del dashboard solo utiliza la pagina de historial cargada (20 registros). No es consulta analitica de todo el historico. La agrupacion hotel usa propietario+nombre+municipio; renombrarlo puede crear otro grupo. Son limites conocidos que debe explicar el alumno.
