# Estado y trazabilidad del incremento

Las figuras son capturas locales reales de Chromium en `evidence`. Los minutos del video estan TODOS pendientes: no usar tiempos del guion como prueba real.

| ID | Implementacion | Prueba ejecutada / evidencia | Estado de cierre |
|---|---|---|---|
| RF-01 | AssessmentForm, formAdapter, schemas/assessment | test_input_errors; Playwright formulario; figura 01 | Implementado y probado localmente |
| RF-02 | assessment_service | perfiles bajo/alto; reevaluacion navegador; figura 02 | Implementado; heuristico, no auditoria |
| RF-03 | schema RiskFinding, AssessmentResults | bundle/PDF y figura 02 | Implementado; estimaciones 1-5 |
| RF-04 | policy_service, enrich_policies | pack10, respuesta simulada y fallbacks; figura 05 | Implementado; API real pendiente |
| RF-05 | product_service SOURCES | PDF AEPD, UI informe | Orientacion implementada; sin certificacion |
| RF-06 | bundle actions, records PATCH | test_full_flow, Playwright progreso; figura 04 | Implementado |
| RF-07 | App dashboard | Playwright escritorio/movil; figuras 02/07 | Implementado |
| RF-08 | report_service, records report.pdf | pypdf todos riesgos, descarga E2E; informe_ejemplo.pdf | Implementado; ver revision visual |
| RF-09 | db, migracion0001, records | SQLite sesion independiente, Compose DB nueva, reinicio4/4 | Implementado |
| RF-10 | history/filter, comparativa App | test_company_history y reevaluacion E2E; figura03 | Implementado; compara con anteriores de pagina cargada |
| RF-11 | auth, security, owned_record | isolation_of_all_record_routes; permisos rol/CSRF | Implementado; no MFA/SSO |
| RF-12 | parse_description, dialogo App | conflicto409/manual-text, optout; figura06 | Implementado; comprension general no garantizada |
| RF-13 | generate_ai_executive_summary | timeout/success simulados; proveedor mostrado | Implementado; API real pendiente |
| RNF-01 | Compose, setup_local, README | instalacion local volumen nuevo y Node24 build | Probado local; segundo entorno pendiente |
| RNF-02 | Pydantic, errors, limites proxy | 422/413/404, error UI, proveedor malformado | Implementado y tests negativos |
| RNF-03 | Argon2, env privados, production validator, Caddy | hash, CSRF, rol; config Caddy valida | HTTPS remoto/historial secretos pendientes |
| RNF-04 | pip-audit/npm audit, workflow, Dependabot | informes JSON0conocidas; CI comprobado sin arrancar | CI bloqueado por restriccion de cuenta; imagenes pendientes |
| RNF-05 | privacy notices, DELETE cuenta, manage cleanup | cascada probada; instrucciones conservacion | Parcial: politica backups/temporizador operador |
| RNF-06 | ai_quota, audit, timeout | rate auth, audit, failure/success proveedor | Parcial: cuota por proceso, sin presupuesto duro |
| RNF-07 | production Compose, guia Hetzner | Caddyvalidate; evidencia mayo no revalidada | Pendiente remoto |
| RE-01 | memoria fuente y generador | PDF borrador con figuras y pruebas | Pendiente datos portada/horas/minutos y revision alumno |
| RE-02 | guion07 | No hay MP4 nuevo | Pendiente grabacion >=10min y URL |
| RE-03 | commits, README, MIT, CI | rama practica3 subida; CI remoto sin ejecutar | Pendiente resolver bloqueo CI, cierre/revision/tag final |

## Comprobacion del alumno antes de cierre

Confirmar grupo/nombre, completar horas reales, comprender codigo, reproducir la demo, decidir dominio/despliegue, probar IA real sin divulgar clave, grabar video, comprobar permisos de enlaces en incognito, ajustar minutos exactos, revisar PDF y crear tag solo al terminar. El paquete actual no se etiqueta ni se presenta como entrega final.

La comparativa del dashboard solo utiliza la pagina de historial cargada (20 registros). No es consulta analitica de todo el historico. La agrupacion hotel usa propietario+nombre+municipio; renombrarlo puede crear otro grupo. Son limites conocidos que debe explicar el alumno.
