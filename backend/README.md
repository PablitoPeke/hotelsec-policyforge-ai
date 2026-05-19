# Backend - HotelSec PolicyForge AI

API del proyecto HotelSec PolicyForge AI, desarrollada con FastAPI.

## Objetivo

El backend será responsable de:

- Exponer la API para el frontend.
- Gestionar usuarios y empresas.
- Recibir respuestas del analizador de hoteles.
- Calcular puntuaciones de madurez.
- Generar riesgos y recomendaciones.
- Integrar el motor de IA.
- Generar informes PDF.

## Stack

- Python 3.11+
- FastAPI
- Pydantic
- Pydantic Settings
- Uvicorn

## Instalación local

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

La API quedará disponible en:

```text
http://localhost:8000
```

Documentación automática:

```text
http://localhost:8000/docs
http://localhost:8000/redoc
```

## Endpoint inicial

```http
GET /api/v1/health
```

Devuelve el estado básico de la API.

## Analizador inicial

```http
POST /api/v1/assessments/analyze
```

Recibe el perfil de un hotel y sus controles de seguridad. El perfil ya contempla elementos propios del sector turístico, como PMS, WiFi de huéspedes, pagos con tarjeta, documentación de clientes, accesos de proveedores y dispositivos IoT/CCTV. Devuelve:

- Puntuación global de madurez.
- Nivel de riesgo.
- Puntuaciones por área.
- Riesgos detectados.
- Próximos pasos recomendados.
