# Estado y trazabilidad del incremento

Revision de cierre: 13/10/2026. Version0.4.0 publica y codigo de aplicacion congelado en83d7b9b; los cambios de cierre son documentacion, evidencia y herramientas de entrega. Las figuras1-6 proceden del navegador local; figura7 de Hetzner. Todos los minutos de video siguen pendientes: no usar tiempos del guion como evidencia.

Actualizacion 16/10/2026: video definitivo confirmado por Pablo (`2026-10-16 19-41-38.mp4`), 18:54.066, 1920x1080, 60fps y pista de audio segun propiedades del archivo. Falta enlace accesible y revision completa con minutos reales; estos metadatos no prueban por si solos que el contenido cumpla. Carlos Cortes instalo el 15/10/2026 y todo funciono, segun declaracion de Pablo. Entrega individual sin numero, por indicacion del alumno. El registro anterior se conserva como estado historico.

Autor Pablo Cortes, individual; grupo omitido hasta confirmar por decision del alumno. Estimacion propia:40 horas (10 desarrollo,10 pruebas,10 documentacion,10 preparacion). El alumno confirma funcionamiento de la URL publica. Suite final99 tests (92 de aplicacion/operaciones y7 de validacion de entrega),5 escenarios en instalacion limpia y5 remotos, auditorias sin vulnerabilidades conocidas y Gitleaks sin hallazgos accionables tras revisar2 falsos positivos. CI no ejecutado por bloqueo de facturacion; no es obligatorio CI verde. Falta persona externa que instale el proyecto: no sustituirla por el asistente. Ver `evidence/closeout-verification.json`.

| ID | Implementacion | Prueba ejecutada / evidencia | Estado de cierre |
|---|---|---|---|
| RF-01 | frontend/src/components/AssessmentForm.tsx; utils/formAdapter.ts; backend/app/schemas/assessment.py | test_input_errors_and_progress_validation; product.spec.ts; figura1 | Cumplido; datos declarados |
| RF-02 | assessment_service | perfiles bajo/alto; reevaluacion navegador; figura 02 | Implementado; heuristico, no auditoria |
| RF-03 | schema RiskFinding, AssessmentResults | bundle/PDF y figura 02 | Implementado; estimaciones 1-5 |
| RF-04 | policy_service, enrich_policies | pack10, respuesta simulada/fallbacks y live-ai-check.json exitoso | Implementado; prueba OpenAI real 13/10 |
| RF-05 | product_service SOURCES | PDF AEPD, UI informe | Orientacion implementada; sin certificacion |
| RF-06 | bundle actions, records PATCH | test_full_flow, Playwright progreso; figura 04 | Implementado |
| RF-07 | App dashboard | Playwright escritorio/movil; figuras 02/07 | Implementado |
| RF-08 | backend/app/services/report_service.py; endpoints/records.py | test_full_flow_persistence_pdf_progress_and_delete; pypdf riesgos; descarga E2E | Cumplido; PDF cliente completo |
| RF-09 | backend/app/db.py; migrations0001-0004; records | test_migration_preserves_existing_user_and_session; instalacion limpia; reinicio historico4/4 | Cumplido; PostgreSQL conservado |
| RF-10 | history/filter, comparativa App | test_company_history y reevaluacion E2E; figura03 | Implementado; compara con anteriores de pagina cargada |
| RF-11 | endpoints/auth.py/account.py; core/security.py; owned_record | test_isolation_of_all_record_routes; test_password_change_rotates_session_and_revokes_all_previous; account.spec.ts; figura7 | Cumplido; no MFA/SSO |
| RF-12 | parse_description, dialogo App | conflicto409/manual-text, optout; figura06 | Implementado; comprension general no garantizada |
| RF-13 | generate_ai_executive_summary | timeout/success simulados y proveedor OpenAI real comprobado | Implementado; prueba real puntual |
| RNF-01 | Compose; scripts/setup_local.py; README | Clon GitHub limpio+config nueva+volumen nuevo8086; 5E2E y API pasan | Parcial: falta instalador humano ajeno al grupo |
| RNF-02 | Pydantic, errors, limites proxy | 422/413/404, error UI, proveedor malformado | Implementado y tests negativos |
| RNF-03 | Argon2; env privados; validator; Caddy | Hash/CSRF/rol/TLS/cookies; Gitleaks8.30.1 refs Git:0 accionables,2 falsos positivos exactos | Cumplido para alcance revisado; no garantia absoluta |
| RNF-04 | pip-audit/npm audit; workflow; Dependabot | Auditorias13/10:0 conocidas; revision de contratos y pruebas negativas | Con limites: CI0pasos por facturacion; imagen OS no escaneada |
| RNF-05 | Avisos; DELETE/export; manage cleanup | test_export_owns_all_rows_and_excludes_authentication_secrets; cascada; conservacion documentada | Con limites: sin retencion automatica/backup externo comercial |
| RNF-06 | usage_service; ai_quota; audit/timeout | test_quota_reservation_is_atomic_under_concurrency; test_global_quota_shared_between_users_and_persists_across_sessions | Cumplido:20 cuenta/h,50 global/dia; no techo monetario |
| RNF-07 | docker-compose.production.yml; Caddy |0.4.0 HTTPS,5E2E remotos,API y backup/restauracion aislada | Cumplido puntual13/10; no garantia de uptime |
| RE-01 | memoria_content.json; generate_practica3_report.py | PDF previo al video, cuerpo11, indice y evidencias; metadata/layout | Parcial: grupo, enlace/minutos y revision personal |
| RE-02 | MP4 local confirmado; guion07 | 18:54.066 y 1920x1080 comprobados en metadatos; contenido por revisar | Parcial: falta URL accesible y minutos reales |
| RE-03 | GitHub; README; MIT; .gitignore; commits | Rama practica3 y codigo editable; secretos revisados | Parcial: tag final tras incorporar video y revision |

## Comprobacion del alumno antes de cierre

Confirmar grupo, conseguir que otra persona siga README, grabar video >=10min, comprobar permisos en incognito, incorporar enlace/minutos reales, revisar PDF y crear tag v1.0-practica3 sobre el commit definitivo. Las40 horas quedan como estimacion comunicada, no tiempos auditados. El PDF previo al video ya incorpora0.4.0/Hetzner/cuenta/pruebas. `delivery_metadata.json` y `scripts/practice_delivery.py` enumeran lo que falta; `generate_practica3_report.py --final` rechaza datos incompletos. No se declara entrega al campus realizada.

La comparativa del dashboard solo utiliza la pagina de historial cargada (20 registros). No es consulta analitica de todo el historico. La agrupacion hotel usa propietario+nombre+municipio; renombrarlo puede crear otro grupo. Son limites conocidos que debe explicar el alumno.
