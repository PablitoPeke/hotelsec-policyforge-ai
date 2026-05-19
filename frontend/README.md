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

La primera versión del frontend muestra un dashboard inicial con:

- Navegación lateral.
- Métricas de ejemplo.
- Estado del backend.
- Comprobación real del endpoint `GET /api/v1/health`.
- Tabla de riesgos de demostración.
- Referencia al endpoint `POST /api/v1/assessments/analyze`.

En la siguiente fase se conectará esta interfaz con el backend real.
