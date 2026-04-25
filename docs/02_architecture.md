# 02. Arquitectura técnica

## Visión general

```text
Usuario / Hotel
   ↓
Frontend Web
   ↓
Formulario de análisis
   ↓
Backend API
   ↓
Motor de reglas + Motor IA
   ↓
Base de datos
   ↓
Dashboard + Informe PDF
```

## Componentes

### Frontend

Aplicación web desarrollada con React y TypeScript. Será la interfaz principal del usuario.

Responsabilidades:

- Registro e inicio de sesión.
- Formulario de análisis por pasos.
- Visualización del dashboard.
- Consulta de políticas generadas.
- Descarga del informe PDF.

### Backend

API desarrollada con FastAPI.

Responsabilidades:

- Autenticación.
- Gestión de empresas.
- Recepción de respuestas del formulario.
- Cálculo de puntuaciones.
- Clasificación de riesgos.
- Integración con IA.
- Generación del informe PDF.

### Base de datos

PostgreSQL almacenará:

- Usuarios.
- Empresas.
- Análisis realizados.
- Respuestas del formulario.
- Puntuaciones.
- Riesgos.
- Políticas generadas.
- Metadatos de informes.

### Motor de scoring

El motor de scoring calculará una puntuación de madurez entre 0 y 100.

Áreas previstas:

- Identidad y accesos.
- Copias de seguridad.
- Seguridad de red.
- Seguridad de dispositivos.
- Protección de datos.
- Concienciación del personal.
- Respuesta a incidentes.
- Continuidad del negocio.

### Motor IA

La IA se utilizará para generar:

- Políticas internas.
- Recomendaciones explicadas.
- Resumen ejecutivo.
- Plan de acción.
- Texto del informe PDF.

La IA no decidirá sola la puntuación final. Esa parte se apoyará en reglas controladas para mantener resultados consistentes.

## Despliegue previsto

```text
Internet
   ↓
Nginx + HTTPS
   ↓
Frontend React
   ↓
Backend FastAPI
   ↓
PostgreSQL
```

El despliegue se realizará en Hetzner Cloud usando Docker y Docker Compose.
