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

## 2026-05-05 - Analizador inicial de hoteles

### Trabajo realizado

- Creación de schemas para el perfil del hotel y los controles de seguridad.
- Creación del primer motor de scoring de madurez.
- Detección inicial de riesgos de ciberseguridad frecuentes en hoteles.
- Creación del endpoint `POST /api/v1/assessments/analyze`.
- Creación de tests para perfiles con seguridad débil y fuerte.

### Decisiones tomadas

- Empezar sin base de datos para validar primero la lógica del análisis.
- Mantener el scoring separado del endpoint para facilitar pruebas y futuras mejoras.
- Usar reglas deterministas antes de incorporar IA, evitando que la puntuación dependa solo de un modelo generativo.

## 2026-05-19 - Documentación del endpoint de análisis

### Trabajo realizado

- Creación de documentación específica para el endpoint `POST /api/v1/assessments/analyze`.
- Inclusión de un ejemplo completo de petición JSON.
- Inclusión de un ejemplo de respuesta con puntuación, riesgos y próximos pasos.
- Inclusión de instrucciones para probar el endpoint desde Swagger y PowerShell.

### Decisiones tomadas

- Documentar cada funcionalidad pequeña antes de pasar al frontend.
- Mantener ejemplos claros para poder usarlos después en la presentación oral y en el informe final.

## 2026-05-19 - Frontend base

### Trabajo realizado

- Creación del proyecto frontend con React, Vite y TypeScript.
- Ajuste de versiones para mantener compatibilidad con el entorno local.
- Sustitución de la pantalla inicial de Vite por un dashboard propio de HotelSec PolicyForge AI.
- Creación de una primera navegación lateral.
- Creación de métricas visuales de ejemplo.
- Creación de una tabla de riesgos de demostración.
- Verificación con `npm run typecheck` y `npm run build`.

### Decisiones tomadas

- Empezar con un dashboard funcional en vez de una landing page.
- No conectar todavía el backend para mantener este commit pequeño y fácil de revisar.
- Usar CSS propio en esta primera fase para evitar añadir más dependencias antes de tener clara la estructura visual.

## 2026-05-19 - Conexión frontend-backend inicial

### Trabajo realizado

- Creación de un cliente API mínimo en el frontend usando `fetch`.
- Conexión del frontend con el endpoint `GET /api/v1/health`.
- Visualización del estado del backend en el dashboard.
- Creación de `frontend/.env.example` con la variable `VITE_API_URL`.
- Actualización de documentación del frontend.

### Decisiones tomadas

- Usar `fetch` nativo para evitar añadir una dependencia extra antes de necesitar un cliente HTTP más completo.
- Conectar primero un endpoint simple antes de construir el formulario de análisis.
- Mantener la URL del backend en variable de entorno para facilitar local, Docker y despliegue.

## 2026-05-19 - Formulario inicial de análisis

### Trabajo realizado

- Creación del cliente API para `POST /api/v1/assessments/analyze`.
- Creación del primer formulario funcional de análisis hotelero.
- Envío de datos reales desde React al backend FastAPI.
- Visualización de puntuación global, puntuaciones por área y riesgos detectados.
- Gestión de estados de carga y error en el frontend.

### Decisiones tomadas

- Mantener el formulario en una sola pantalla para validar primero el flujo completo.
- Usar estado local de React antes de introducir librerías como React Hook Form o Zod.
- No añadir nuevas dependencias en esta fase para que el commit sea fácil de revisar.

## 2026-05-19 - Refactor del frontend en componentes

### Trabajo realizado

- Separación de la pantalla principal en componentes reutilizables.
- Creación de componentes para la barra lateral, estado de API, métricas, formulario y resultados.
- Creación de una carpeta `data` para valores iniciales y etiquetas compartidas.
- Creación de una carpeta `types` para tipos internos de la aplicación.
- Simplificación de `App.tsx` para que se encargue principalmente de coordinar estado, llamadas API y renderizado.
- Verificación con `npm run typecheck` y `npm run build`.

### Decisiones tomadas

- Dividir el frontend antes de añadir más campos para que el proyecto sea más fácil de mantener.
- Mantener los componentes en archivos pequeños para que se puedan explicar mejor en la defensa de la práctica.
- No añadir librerías nuevas todavía porque React, TypeScript y CSS propio siguen siendo suficientes para esta fase.

## 2026-05-19 - Ampliación del analizador hotelero

### Trabajo realizado

- Añadidos campos específicos para hoteles y pymes turísticas: PMS, WiFi de huéspedes, pagos con tarjeta, documentación de clientes, proveedores, TPV e IoT/CCTV.
- Ampliado el motor de scoring del backend para tener en cuenta esos nuevos campos.
- Añadidos nuevos riesgos: PMS sin usuarios individuales, TPV no aislados, IoT/CCTV en red principal, accesos remotos de proveedores y registro RGPD incompleto.
- Actualizados los tests del backend con un perfil débil y un perfil fuerte.
- Actualizado el formulario del frontend para enviar los nuevos campos al backend.
- Actualizada la documentación de uso del endpoint.

### Decisiones tomadas

- Mantener el análisis basado en reglas para que sea explicable y verificable antes de integrar IA.
- Separar campos de perfil del hotel y controles de seguridad para que el análisis entienda cuándo aplica cada riesgo.
- Priorizar riesgos reales del sector hotelero frente a una lista genérica de controles de ciberseguridad.

## 2026-05-24 - Generador backend de políticas

### Trabajo realizado

- Creación del endpoint `POST /api/v1/policies/generate`.
- Creación de schemas específicos para políticas, controles y pack generado.
- Creación del servicio backend que genera políticas a partir del perfil del hotel y los controles de seguridad.
- Inclusión de políticas de accesos, backups, dispositivos, red/IoT, incidentes/RGPD y proveedores.
- Creación de test automático para validar que el endpoint devuelve un pack completo.

### Decisiones tomadas

- Generar las políticas con reglas propias en esta fase para que la demo sea estable aunque no haya API externa de IA configurada.
- Reutilizar el analizador de madurez para que las políticas estén alineadas con el nivel de riesgo.
- Mantener el diseño preparado para sustituir o complementar las reglas con IA en una fase posterior.

## 2026-05-24 - Conexión del generador de políticas al frontend

### Trabajo realizado

- Creación del cliente frontend para `POST /api/v1/policies/generate`.
- Ejecución en paralelo del análisis de madurez y la generación del pack de políticas.
- Creación del componente visual `PolicyPackPanel`.
- Actualización de las métricas del dashboard para mostrar cuántas políticas se han generado.
- Añadido del bloque de orden de implantación para explicar qué debería hacer primero el hotel.

### Decisiones tomadas

- Mostrar las políticas en la misma pantalla del análisis para que la demo sea directa.
- Ejecutar análisis y generación de políticas en paralelo para que la respuesta sea más rápida.
- Mantener textos generados por reglas para que la entrega no dependa de claves externas.
