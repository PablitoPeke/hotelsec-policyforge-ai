# 11. Road Map de mejora para la Práctica 2

## Objetivo

La Práctica 2 ampliará HotelSec PolicyForge AI para convertir el MVP en una herramienta más completa, persistente y preparada para uso real por hoteles y pymes turísticas.

## Diagrama de fases

```text
Fase 1 ─ Base de datos e histórico
   ↓
Fase 2 ─ Usuarios, empresas y autenticación
   ↓
Fase 3 ─ Informes PDF avanzados
   ↓
Fase 4 ─ IA mejorada y prompts versionados
   ↓
Fase 5 ─ Rendimiento, seguridad y despliegue escalable
```

## Mejoras planificadas

| Nº | Mejora | Descripción | Estimación |
|---|---|---|---|
| 1 | Persistencia en PostgreSQL | Guardar empresas, análisis, riesgos, políticas e informes generados. | 10-14 h |
| 2 | Autenticación y roles | Añadir login, usuarios de hotel, administrador y separación por empresa. | 12-16 h |
| 3 | Informes PDF avanzados | Generar PDF backend con plantilla profesional, logo, gráficos y anexos. | 8-12 h |
| 4 | IA con prompts versionados | Separar prompts, guardar versiones y permitir comparar resultados. | 8-10 h |
| 5 | Panel histórico | Consultar análisis anteriores y evolución de madurez por fechas. | 10-12 h |
| 6 | Recomendaciones ISO/RGPD ampliadas | Mapear riesgos a controles ISO 27001 y acciones RGPD. | 8-12 h |
| 7 | Mejoras de rendimiento | Cachear resultados, optimizar llamadas IA y reducir tiempos en Render/VPS. | 6-8 h |
| 8 | Seguridad del despliegue | HTTPS, cabeceras de seguridad, rate limiting y gestión de secretos. | 6-10 h |

## Mejoras de rendimiento o escalabilidad

- Separar frontend y backend en contenedores independientes.
- Añadir PostgreSQL gestionado o contenedor dedicado.
- Cachear respuestas IA repetidas.
- Añadir límites de tamaño a descripciones libres.
- Registrar errores y tiempos de respuesta.
- Preparar despliegue con HTTPS y dominio.

## Mejoras de seguridad

- Autenticación JWT.
- Gestión segura de claves en variables de entorno.
- Validación estricta de entradas.
- Rate limiting en endpoints de IA.
- Registro de auditoría de análisis generados.
- Revisión de CORS por dominio final.

## Integración con otras herramientas o APIs

- OpenAI para resúmenes y generación mejorada de políticas.
- Google Drive o almacenamiento S3 para guardar informes.
- API de correo para enviar informes al cliente.
- Integración futura con escáneres básicos de superficie externa.

## Estimación global

La evolución de la Práctica 2 se estima entre 70 y 95 horas de trabajo, priorizando primero persistencia, autenticación, PDF profesional y seguridad del despliegue.
