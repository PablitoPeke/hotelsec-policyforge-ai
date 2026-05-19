# HotelSec PolicyForge AI

Plataforma web de ciberseguridad con inteligencia artificial orientada a hoteles, alojamientos turísticos y pymes del sector turístico de Lanzarote.

El objetivo del proyecto es analizar el perfil de seguridad de una empresa hotelera, calcular su nivel de madurez, identificar riesgos prioritarios y generar políticas básicas de seguridad adaptadas al negocio.

## Línea de trabajo

Este proyecto pertenece a la línea de **Normativa y Cumplimiento** de la práctica de Ciberseguridad con Inteligencia Artificial.

Combina varias funcionalidades:

- Generador de políticas de seguridad con IA.
- Evaluador de madurez de ciberseguridad.
- Mapa de riesgos.
- Recomendaciones básicas de RGPD e ISO 27001.
- Generador de informe PDF.
- Dashboard web con histórico de análisis.

## Funcionalidades previstas para la Práctica 1

- Formulario avanzado para analizar el perfil de un hotel o alojamiento turístico.
- Cálculo de una puntuación de madurez de 0 a 100.
- Clasificación de riesgos por nivel: bajo, medio, alto y crítico.
- Generación de políticas de seguridad mediante IA.
- Generación de recomendaciones priorizadas.
- Dashboard con métricas visuales.
- Exportación de informe PDF.
- Despliegue en un VPS de Hetzner mediante Docker.

## Stack técnico previsto

### Frontend

- React
- Vite
- TypeScript
- CSS propio en la primera fase
- Tailwind CSS previsto para fases posteriores si compensa
- React Router previsto para navegación real
- React Hook Form y Zod previstos para el formulario de análisis
- Recharts previsto para gráficas del dashboard
- Lucide React previsto para iconos de acciones

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- JWT
- bcrypt / Passlib

### Base de datos

- PostgreSQL

### IA

- OpenAI API o modelo local mediante Ollama
- Prompts estructurados
- Motor de reglas para scoring
- Posible RAG en la Práctica 2

### Despliegue

- Hetzner Cloud VPS
- Docker
- Docker Compose
- Nginx
- Let's Encrypt

## Estructura del repositorio

```text
.
├── backend/              # API FastAPI
├── frontend/             # Aplicación React
├── infra/                # Docker, Nginx y despliegue
├── docs/                 # Documentación del proyecto
├── README.md
└── .gitignore
```

## Estado actual

Fase inicial del proyecto:

- Idea definida.
- Propuesta PDF creada.
- Estructura base del repositorio preparada.
- Documentación inicial creada.
- Backend base con FastAPI creado.
- Endpoint de análisis inicial creado.
- Frontend base con React/Vite creado.

## Entregables finales

- URL de la herramienta desplegada en Hetzner.
- URL del repositorio GitHub.
- Informe profesional en PDF.
- Presentación oral de 10 minutos con demostración en vivo.
