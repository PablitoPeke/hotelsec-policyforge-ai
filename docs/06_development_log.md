# 06. Diario de desarrollo

Este archivo se usará para documentar el proceso de desarrollo fase a fase. Servirá como evidencia para el informe final.

## 2026-04-25

### Trabajo realizado

- Revisión de las especificaciones de la práctica.
- Elección de la línea de trabajo: Normativa y Cumplimiento.
- Definición de la idea: HotelSec PolicyForge AI.
- Creación de una propuesta inicial en PDF.
- Preparación de la estructura inicial del repositorio.

### Decisiones tomadas

- Enfocar la herramienta en hoteles y alojamientos turísticos de Lanzarote.
- Usar React en el frontend.
- Usar FastAPI en el backend.
- Usar PostgreSQL como base de datos.
- Usar IA para generar políticas, recomendaciones y resumen ejecutivo.
- Usar un motor de reglas propio para calcular puntuaciones y riesgos.

### Próximos pasos

- Inicializar Git.
- Crear repositorio en GitHub.
- Preparar backend base.
- Preparar frontend base.

## 2026-04-25 - Backend base

### Trabajo realizado

- Creación de la estructura inicial del backend con FastAPI.
- Separación de módulos por API, configuración, esquemas y servicios.
- Creación del endpoint `GET /api/v1/health`.
- Creación de `requirements.txt` con dependencias iniciales.
- Creación de prueba básica para comprobar el endpoint de salud.
- Actualización de variables de entorno de ejemplo.

### Decisiones tomadas

- Usar FastAPI porque ofrece una API moderna, documentación automática y buena integración con validación de datos.
- Usar Pydantic Settings para centralizar la configuración y evitar secretos dentro del código.
- Crear una estructura modular desde el principio para poder añadir scoring, riesgos, IA, base de datos y PDF sin reordenar el proyecto más adelante.
