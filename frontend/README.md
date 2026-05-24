# Frontend - HotelSec PolicyForge AI

Aplicación web del proyecto HotelSec PolicyForge AI.

## Objetivo

El frontend será la interfaz principal para que un hotel pueda:

- Completar el formulario de análisis.
- Consultar la puntuación de madurez.
- Revisar riesgos detectados.
- Ver políticas generadas.
- Descargar informes PDF.

## Stack actual

- React.
- Vite.
- TypeScript.
- CSS propio en `src/index.css`.

## Estructura principal

- `src/App.tsx`: coordina el estado de la pantalla, llama a la API y une los componentes.
- `src/api`: contiene las funciones que hablan con el backend FastAPI.
- `src/components`: contiene las piezas visuales reutilizables del dashboard.
- `src/data`: contiene datos iniciales y etiquetas compartidas.
- `src/types`: contiene tipos internos del frontend.

## Por qué usamos estas herramientas

- **React** permite construir una interfaz por componentes.
- **Vite** permite arrancar y compilar el frontend de forma rápida.
- **TypeScript** ayuda a detectar errores antes de ejecutar la aplicación.
- **CSS propio** permite empezar con una interfaz clara sin añadir más dependencias en esta fase.

## Instalación

```bash
cd frontend
npm install
```

## Ejecución local

```bash
npm run dev
```

La aplicación se abrirá en:

```text
http://localhost:5173
```

## Configuración

El frontend lee la URL del backend desde la variable:

```text
VITE_API_URL=http://localhost:8000
```

Puedes copiar `frontend/.env.example` a `frontend/.env` si necesitas cambiarla en local.

En esta fase la pantalla principal llama a:

```http
GET /api/v1/health
```

Con eso muestra si el backend está online u offline.

## Comprobaciones

```bash
npm run typecheck
npm run build
```

## Estado actual

La versión actual del frontend muestra un dashboard inicial con:

- Navegación lateral.
- Métricas de ejemplo.
- Estado del backend.
- Comprobación real del endpoint `GET /api/v1/health`.
- Formulario inicial de análisis hotelero.
- Campos específicos de hoteles: PMS, WiFi de huéspedes, pagos, RGPD, proveedores, TPV e IoT/CCTV.
- Conexión real con el endpoint `POST /api/v1/assessments/analyze`.
- Visualización de puntuación, áreas de madurez y riesgos detectados.
- Estructura modular separada en componentes, API, datos y tipos.
- Generación de un pack de políticas desde el endpoint `POST /api/v1/policies/generate`.
- Resumen ejecutivo con prioridades, evidencias y descarga de informe PDF.
- Resumen inteligente desde `POST /api/v1/ai/executive-summary`, con OpenAI opcional y fallback por reglas.

En la siguiente fase se preparará el despliegue público del frontend y backend.
