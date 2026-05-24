# 09. Guía de despliegue público

Esta guía deja el proyecto listo para publicarlo rápidamente con Render. Render permite desplegar un backend Python y un frontend estático desde GitHub usando el archivo `render.yaml`.

## Importante sobre Google

Para entregar la práctica lo importante es tener una URL pública. Que aparezca en Google Search puede tardar más que unas horas, porque Google decide cuándo indexa una página. Lo que sí podemos hacer es:

- publicar la aplicación,
- permitir indexación con `robots.txt`,
- añadir metadatos básicos en `index.html`,
- enviar la URL manualmente desde Google Search Console si se quiere acelerar.

## Servicios que se desplegarán

- `hotelsec-policyforge-api`: backend FastAPI.
- `hotelsec-policyforge-web`: frontend React/Vite.

## Variables principales

Backend:

```text
APP_ENV=production
APP_URL=https://hotelsec-policyforge-web.onrender.com
CORS_ORIGINS=https://hotelsec-policyforge-web.onrender.com
JWT_SECRET_KEY=<generada por Render>
OPENAI_API_KEY=<opcional en esta fase>
```

Frontend:

```text
VITE_API_URL=https://hotelsec-policyforge-api.onrender.com
```

## Pasos para publicar

1. Entrar en Render con GitHub.
2. Crear un nuevo `Blueprint`.
3. Seleccionar el repositorio `PablitoPeke/hotelsec-policyforge-ai`.
4. Render detectará `render.yaml`.
5. Confirmar la creación de los dos servicios.
6. Cuando terminen los despliegues, abrir:

```text
https://hotelsec-policyforge-web.onrender.com
```

7. Probar también:

```text
https://hotelsec-policyforge-api.onrender.com/docs
https://hotelsec-policyforge-api.onrender.com/api/v1/health
```

## Si Render cambia los nombres

Si Render añade sufijos al nombre porque la URL ya existe, hay que actualizar:

- `VITE_API_URL` en el frontend,
- `CORS_ORIGINS` en el backend,
- `APP_URL` en el backend.

Después se redeployan ambos servicios.

## Comprobación final para la entrega

- El dashboard carga.
- El estado de API aparece como `OK`.
- El formulario analiza un hotel.
- Se muestran riesgos y puntuaciones.
- Se genera el pack de políticas.
- `/docs` muestra la documentación automática de FastAPI.
