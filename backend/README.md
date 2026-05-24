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

## Generador de políticas

```http
POST /api/v1/policies/generate
```

Recibe el mismo perfil de evaluación y genera un pack inicial de políticas:

- Política de contraseñas y accesos.
- Política de copias de seguridad.
- Política de uso de dispositivos.
- Política de red, WiFi e IoT.
- Política de respuesta a incidentes y RGPD.
- Política de proveedores y accesos remotos.

En esta fase se genera con reglas propias para que el resultado sea estable y explicable en la demostración.

## Resumen ejecutivo con IA

```http
POST /api/v1/ai/executive-summary
```

Recibe el resultado del análisis y el pack de políticas. Si existe `OPENAI_API_KEY`, genera un resumen ejecutivo usando OpenAI. Si no existe, devuelve un resumen de respaldo basado en reglas para que la demo siga funcionando.

```http
POST /api/v1/ai/analyze-description
```

Recibe una descripción libre escrita por el cliente y la convierte en un análisis completo: controles normalizados, puntuación de madurez, riesgos, políticas y resumen ejecutivo.
