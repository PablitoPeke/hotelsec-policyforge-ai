# 07. Guía inicial de GitHub

## Objetivo

Subir el proyecto a GitHub desde el principio para que quede evidencia del proceso de desarrollo.

## Pasos recomendados

### 1. Inicializar Git en local

```bash
git init
```

### 2. Revisar archivos

```bash
git status
```

### 3. Añadir archivos

```bash
git add .
```

### 4. Crear primer commit

```bash
git commit -m "Initial project documentation and structure"
```

### 5. Crear repositorio en GitHub

Nombre recomendado:

```text
hotelsec-policyforge-ai
```

Puede ser público o privado, siempre que el profesor tenga acceso.

### 6. Conectar repositorio local con GitHub

```bash
git remote add origin https://github.com/USUARIO/hotelsec-policyforge-ai.git
git branch -M main
git push -u origin main
```

## Recomendación de commits

Usar commits frecuentes y descriptivos:

```text
docs: add initial project brief
feat: create FastAPI base project
feat: add assessment form
feat: implement scoring engine
feat: generate AI policies
feat: add PDF report export
chore: add Docker deployment files
```
