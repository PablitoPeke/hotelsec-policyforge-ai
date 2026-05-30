# 10. Despliegue en Hetzner Cloud

Esta guía cubre el requisito de despliegue en un servidor Hetzner Cloud VPS usando Docker Compose.

## Arquitectura de despliegue

```text
Internet
  ↓
Dominio o subdominio
  ↓
VPS Hetzner
  ↓
Nginx reverse proxy
  ├─ Frontend React/Vite
  └─ Backend FastAPI
```

## Servicios Docker

- `api`: backend FastAPI.
- `web`: frontend compilado y servido con Nginx.
- `nginx`: reverse proxy público.

## Requisitos del VPS

- Ubuntu 22.04 o superior.
- Docker.
- Docker Compose plugin.
- Puerto 80 abierto.
- Dominio o subdominio apuntando a la IP pública del VPS.

## Pasos de despliegue

1. Crear un VPS en Hetzner Cloud.
2. Apuntar un dominio/subdominio a la IP del VPS.
3. Instalar Docker:

```bash
sudo apt update
sudo apt install -y ca-certificates curl gnupg git
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
```

4. Clonar el repositorio:

```bash
git clone https://github.com/PablitoPeke/hotelsec-policyforge-ai.git
cd hotelsec-policyforge-ai
```

5. Crear el archivo `.env` de producción:

```bash
cp infra/.env.hetzner.example .env
nano .env
```

Valores importantes:

```text
APP_URL=https://tu-dominio.com
CORS_ORIGINS=https://tu-dominio.com
JWT_SECRET_KEY=clave_larga_y_segura
OPENAI_API_KEY=tu_clave_openai
OPENAI_MODEL=gpt-4o-mini
```

6. Levantar contenedores:

```bash
docker compose -f docker-compose.hetzner.yml --env-file .env up -d --build
```

7. Comprobar estado:

```bash
docker compose -f docker-compose.hetzner.yml ps
curl http://localhost/api/v1/health
```

## HTTPS

Para una entrega real se recomienda añadir HTTPS con Certbot o colocar Cloudflare delante del dominio. El proyecto queda preparado con Nginx como reverse proxy para incorporar certificados.

## Actualización de versión

```bash
git pull
docker compose -f docker-compose.hetzner.yml --env-file .env up -d --build
```

## URLs esperadas

- Panel web: `https://tu-dominio.com`
- API health: `https://tu-dominio.com/api/v1/health`
- Swagger: `https://tu-dominio.com/docs`
