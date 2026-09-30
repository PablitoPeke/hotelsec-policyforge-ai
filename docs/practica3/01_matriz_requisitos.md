# Matriz de requisitos y trazabilidad inicial

Revision: 30/09/2026. Los IDs se asignan ahora a los compromisos del material de Practica 1; no son IDs suministrados por Evolve. RF indica funcionalidad y RNF una condicion de calidad/seguridad. Los RE son entregables de Practica 3.

Fuentes: propuesta inicial (`propuesta_hotelsec_policyforge_ai.md`), `docs/01_project_brief.md`, `docs/03_features.md`, `docs/04_data_model.md`, memoria final PDF y roadmap anterior. El roadmap contiene mejoras futuras: se distingue de los compromisos del MVP. En esta fase no se descarta nada; cualquier cambio de alcance requerira version original, nueva version y motivo escrito.

Cumplido = existe implementacion y evidencia suficiente para ese alcance. Parcial = existe, pero falta parte o verificacion. Pendiente = no implementado. A revisar = necesita reformulacion o correccion. La columna final no acredita la entrega: se actualizara tras ejecutar pruebas y grabar el video.

| ID | Requisito original y origen | Estado inicial | Implementacion actual / carencia | Prueba prevista | Estado final / evidencia |
|---|---|---|---|---|---|
| RF-01 | Recoger perfil y controles hoteleros (funcionalidades y propuesta) | Parcial | `frontend/src/components/AssessmentForm.tsx`, `backend/app/schemas/assessment.py`; faltan campos propuestos de temporada, sistemas cloud, datos, continuidad y BYOD | PR-01 | Pendiente de cierre |
| RF-02 | Calcular puntuacion global 0-100 y por areas (MVP) | Parcial | `backend/app/services/assessment_service.py`; base probada, revisar cobertura de proteccion de datos y continuidad propuestas | PR-02 | 2 tests actuales de perfiles; pendiente cobertura ampliada |
| RF-03 | Mostrar mapa de riesgos con probabilidad, impacto, severidad y recomendacion (propuesta/funcionalidades) | Parcial | `backend/app/schemas/assessment.py`, `AssessmentResults.tsx`; faltan probabilidad e impacto explicitos | PR-03 | Pendiente de cierre |
| RF-04 | Generar politicas adaptadas con IA (propuesta/MVP) | Parcial | `backend/app/services/policy_service.py` usa reglas; faltan redaccion IA y politicas de teletrabajo/correo propuestas | PR-04 | Test actual del pack por reglas; pendiente ampliar |
| RF-05 | Ofrecer orientacion RGPD/ISO sin afirmar certificacion (propuesta) | Parcial | Politicas contienen controles y recomendaciones; falta seccion normativa explicita con fuentes | PR-05 | Pendiente de cierre |
| RF-06 | Plan de accion inmediato/30/90 dias con prioridad, dificultad, impacto y responsable (propuesta) | Parcial | `next_steps` e `implementation_order` son listas; sin estructura ni seguimiento | PR-06 | Pendiente de cierre |
| RF-07 | Dashboard con puntuacion, riesgo, politicas, ultimos analisis y estado de acciones (propuesta) | Parcial | `frontend/src/App.tsx`, `DashboardMetrics.tsx`; solo sesion actual | PR-07 | Pendiente de cierre |
| RF-08 | Exportar PDF con perfil, resumen, riesgos, politicas, normativa y plan (propuesta/MVP) | Parcial | `frontend/src/utils/pdfReport.ts`; resumen local, maximo 8 riesgos y fichas resumidas de politicas | PR-08 | Pendiente verificacion visual y contenido completo |
| RF-09 | Guardar empresas, respuestas, analisis, riesgos, politicas e informes (modelo/MVP) | Pendiente | No hay modelos ni migraciones; solo configuracion `DATABASE_URL` | PR-09 | Pendiente de cierre |
| RF-10 | Consultar historial por empresa y comparar madurez en el tiempo (propuesta) | Pendiente | No existen endpoints ni vista de historial | PR-10 | Pendiente de cierre |
| RF-11 | Usuarios y autenticacion con aislamiento de datos (seguridad propuesta; roles en roadmap) | Pendiente | `JWT_SECRET_KEY` configurado, sin autenticar peticiones | PR-11 | Pendiente de cierre |
| RF-12 | Analisis por descripcion que complementa el formulario (funcion entregada) | A revisar | `backend/app/services/ai_service.py`; fusion OR no resuelve negaciones/contradicciones | PR-12 | Test actual conserva datos manuales; falta prueba de contradiccion |
| RF-13 | Resumen ejecutivo por IA con alternativa declarada por reglas (funcion entregada) | Parcial | `ai_service.py`, `AiSummaryPanel.tsx`; existe indicador del proveedor, falta probar respuestas malformadas/timeout | PR-13 | Test actual sin clave; API real no comprobada en esta fase |
| RNF-01 | Instalacion reproducible desde cero (P3; despliegue original) | Parcial | Docker y Compose existen; README raiz no explica ejecucion completa | PR-14 | Pendiente instalacion limpia |
| RNF-02 | Validacion de entradas y errores controlados (seguridad original/P3) | Parcial | Pydantic y estados de error; falta cobertura negativa y consistencia en respuestas | PR-15 | Pendiente de cierre |
| RNF-03 | Secretos fuera del codigo, hash seguro y comunicaciones protegidas (seguridad propuesta) | Parcial | `.gitignore`, env de ejemplo; falta auditar historial, implementar hashes y HTTPS | PR-16 | Pendiente de cierre |
| RNF-04 | Revision de dependencias y codigo (P3) | Pendiente | Sin auditoria actual ni automatizacion comprobada | PR-17 | Pendiente auditoria y tratamiento de hallazgos |
| RNF-05 | Datos personales: finalidad, acceso, conservacion y borrado (P3) | Pendiente | Debe documentarse e implementarse junto a persistencia; usar datos ficticios en pruebas | PR-18 | Pendiente de cierre |
| RNF-06 | Limitar consumo de IA y registrar incidencias (roadmap/seguridad P3) | Pendiente | Timeout existente; no hay cuotas/rate limiting ni auditoria funcional | PR-19 | Pendiente de cierre |
| RNF-07 | Despliegue Hetzner por Docker (compromiso de P1) | Parcial | `docker-compose.hetzner.yml`, Nginx; evidencia historica de mayo, no comprobada hoy | PR-20 | Pendiente revalidacion |
| RE-01 | Memoria 20-40 paginas con 13 apartados, indice, capturas y declaracion IA (P3) | Pendiente | Memoria anterior es de 5 paginas; no sirve como memoria final de P3 | PR-21 | Pendiente PDF final |
| RE-02 | Video real >=10 minutos y enlace accesible (P3) | Pendiente | Falta guion, grabacion y minutos exactos de esta version | PR-22 | Pendiente video |
| RE-03 | GitHub, licencia si publico y tag `v1.0-practica3` (P3) | Parcial | Historial previo disponible; faltan licencia y tag final | PR-23 | Pendiente cierre de version |

## Fuera del MVP y decisiones futuras

RAG avanzado, simulador de incidentes, escaneo externo, PMS real, envio de informes por correo y multiidioma aparecen como ampliaciones. No se convierten automaticamente en obligacion de esta entrega; primero se cierran los compromisos originales. Certificacion ISO y auditoria juridica completa siguen fuera del alcance definido.

## Registro de cambios de requisitos

No hay modificaciones aprobadas en esta revision inicial. Cada cambio futuro registrara ID, texto original, texto nuevo, motivo, impacto y fecha. No se eliminara una fila para ocultar un incumplimiento.

## Evidencias finales

Para cada fila: ruta de implementacion real, ID de prueba ejecutada, resultado, figura o apartado de memoria y minuto exacto del video. Una prueba planificada no equivale a una prueba superada.
