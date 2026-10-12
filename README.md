# HotelSec PolicyForge AI

Autodiagnostico de ciberseguridad para alojamientos de Lanzarote. Continuacion de la Practica 1 (9/10, sin comentarios del docente) para la Practica 3 de Evolve Academy.

## Funciones actuales

- Registro, acceso y cierre de sesiones; aislamiento de datos por propietario.
- Cuestionario hotelero ampliado, texto libre integrado y confirmacion de contradicciones.
- Madurez global y por areas; riesgos con prioridad, probabilidad e impacto orientativos.
- Diez politicas por reglas, con personalizacion opcional mediante OpenAI.
- Analisis persistentes, historial por hotel, comparativa y seguimiento de acciones.
- PDF completo generado en servidor, fuentes de orientacion y registro de actividad.
- Borrado de analisis o de cuenta con sus datos asociados.

No es una auditoria tecnica ni una certificacion RGPD/ISO. No analiza redes de terceros ni necesita datos de huespedes. La IA es opcional y se identifica cuando se aplica el respaldo por reglas.

## Probar desde cero con Docker

Requisitos: Git, Docker con Compose v2 y Python 3.12+ para generar la configuracion. Windows: iniciar Docker Desktop en modo contenedores Linux.

```powershell
git clone https://github.com/PablitoPeke/hotelsec-policyforge-ai.git
cd hotelsec-policyforge-ai
git switch practica3
python scripts/setup_local.py --port 8085
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml up -d --build
```

Abrir http://localhost:8085 y crear una cuenta con datos ficticios y contrasena de al menos 12 caracteres. No existen usuarios ni contrasenas predeterminados. El script genera una clave de base de datos privada; no sobrescribe un `.env.local` existente. Alembic aplica las migraciones al arrancar. No publicar esta configuracion HTTP local en Internet.

```powershell
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml ps
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml logs --tail 50 api
docker compose --env-file .env.local -p hotelsec-p3 -f docker-compose.hetzner.yml stop
```

Para volver a arrancar, repetir `up -d`. El volumen conserva los datos. `down -v` destruye la base de datos: no usarlo como actualizacion. El proyecto Compose debe conservar el mismo nombre.

## Desarrollo editable en VS Code

Todo el codigo esta en este repositorio: `backend/app`, `frontend/src`, `backend/migrations`, `infra`, `scripts` y `docs/practica3`. No hay un servicio de generacion de codigo cerrado necesario para ejecutar el producto.

Alternativa ligera de desarrollo con SQLite (PowerShell, desde la raiz):

```powershell
py -3.12 -m venv backend/.venv
backend/.venv/Scripts/python.exe -m pip install -r backend/requirements-dev.txt
$env:PYTHONPATH="$PWD/backend"
$env:DATABASE_URL="sqlite:///./local.sqlite3"
$env:APP_ENV="development"
$env:CORS_ORIGINS="http://localhost:5173"
backend/.venv/Scripts/python.exe -m alembic -c backend/alembic.ini upgrade head
backend/.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

En otra terminal con Node 24 LTS:

```powershell
cd frontend
npm ci
npm run dev -- --host 127.0.0.1
```

Abrir http://localhost:5173. Vite redirige `/api` al backend local. En VS Code seleccionar `backend/.venv/Scripts/python.exe` como interprete Python. SQLite es una alternativa para desarrollo y pruebas, no la base del despliegue con Docker.

## Pruebas

```powershell
$env:PYTHONPATH="$PWD/backend"
backend/.venv/Scripts/python.exe -m pytest backend/tests -q
backend/.venv/Scripts/python.exe -m pip_audit -r backend/requirements.txt
cd frontend
npm ci
npm run build
npm audit --audit-level=moderate
npx playwright install chromium
npx playwright test
```

Playwright necesita la instalacion Docker local en el puerto 8085. Para otra URL: `$env:E2E_URL="http://localhost:OTRO_PUERTO"`. Utiliza cuentas ficticias nuevas; sus datos quedan en la base local. Las capturas se guardan en `docs/practica3/evidence` y los resultados en `frontend/test-results`. Las pruebas del backend utilizan bases temporales aisladas. Ver [resultados y limites](docs/practica3/04_verificacion.md).

## Stack y motivos

| Capa | Herramientas | Motivo |
|---|---|---|
| Interfaz | React 18, TypeScript, Vite 8, CSS, Lucide | Conservar la base y separar estados/vistas; tipos e iconos accesibles |
| API | Python 3.12, FastAPI, Pydantic, HTTPX | Contratos validados y API documentada; tiempo limite al proveedor |
| Datos | PostgreSQL 17, SQLAlchemy 2, Alembic | Persistencia, propiedad y cambios de esquema versionados |
| Sesiones | Argon2, tokens opacos, cookies HttpOnly, CSRF | Hash probado y revocacion inmediata; sin tokens en localStorage |
| IA | OpenAI Responses API, reglas locales | Personalizacion opcional; scoring reproducible no delegado al modelo |
| PDF | ReportLab | Texto paginado y todos los resultados, no un resumen truncado |
| Pruebas | pytest, Playwright, pip-audit, npm audit | Casos funcionales, negativos, navegador y dependencias |
| Formato de codigo | Prettier (solo desarrollo) | Mantener el codigo nuevo legible y editable |
| Despliegue | Docker Compose; Nginx local; Caddy en produccion | Mismo origen y TLS automatizado con dominio configurado |

JWT/bcrypt, Tailwind, Router, Zod y Recharts eran opciones iniciales, no dependencias obligatorias. Se registra la decision de mantener CSS/estado React y usar sesiones revocables con Argon2 en [arquitectura y seguridad](docs/practica3/03_arquitectura_seguridad.md). Ollama y RAG no estan implementados.

## Configuracion de IA y produccion

OpenAI: anadir `OPENAI_API_KEY` solo al archivo privado del servidor, nunca al frontend ni a GitHub. Con Docker, recrear el servicio `api` tras cambiarlo. La casilla de consentimiento del formulario controla el envio en el flujo principal; sin ella no se llama al proveedor. No hay clave incorporada ni costes incluidos. La prueba real con la cuenta del alumno queda pendiente; las pruebas automatizadas simulan errores/respuestas.

Produccion HTTPS: [guia de despliegue y operaciones](docs/practica3/05_despliegue.md). `python scripts/setup_production.py --domain TU_DOMINIO_REAL` crea configuracion privada sin sobrescribir secretos ni arrancar servicios. El archivo `docker-compose.production.yml` exige dominio y clave privada de PostgreSQL. `APP_ENV=production` impide arrancar con cookies inseguras o URL HTTP. La IP de Hetzner de Practica 1 es un antecedente: esta nueva version no se ha publicado ni revalidado alli.

Comprobacion de instancia propia (crea y elimina dos cuentas ficticias):

```powershell
backend/.venv/Scripts/python.exe scripts/verify_deployment.py --url http://localhost:8085 --confirm-test-data
```

Para remoto usar origen HTTPS. Anadir `--output RUTA.json` para conservar evidencia sanitizada. La opcion explicita `--with-ai` envia datos ficticios al proveedor y puede consumir credito; sin ella no solicita IA. Un fallback no cuenta como prueba IA superada. Revisar el resultado de limpieza si el servidor deja de responder.

## Entrega

[Seguimiento de Practica 3](docs/practica3/README.md), [matriz inicial](docs/practica3/01_matriz_requisitos.md), [cierre y trazabilidad](docs/practica3/06_estado_entrega.md), [guion del video](docs/practica3/07_video_entrega.md). La memoria marcada como borrador no sustituye la entrega final mientras falten datos de portada, horas reales, video y comprobaciones indicadas. No se crea `v1.0-practica3` hasta cerrar esos pendientes.

Revision del 12/10: 50 tests backend/operaciones y 2 escenarios de navegador superados; build correcto, auditorias sin vulnerabilidades conocidas. [Pasos de cierre para el 16 de octubre](docs/practica3/08_cierre_16_octubre.md). Pablo Cortes confirma la prueba manual; el grupo sigue pendiente. La conexion SSH automatica fue rechazada, sin cambiar el VPS.

Licencia MIT. Documentos de Practica 1 conservados como antecedentes; las guias actuales estan en `docs/practica3`.

Estado CI: el primer run de GitHub Actions de esta fase no pudo iniciar backend/frontend por una restriccion administrativa de la cuenta. No equivale a un test fallido del codigo ni a CI superado. El titular debe resolver el bloqueo y repetirlo; las pruebas locales y su evidencia son independientes.
