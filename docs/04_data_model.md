# 04. Modelo de datos inicial

## Entidades principales

### User

Representa a una persona que accede a la plataforma.

Campos previstos:

- id
- name
- email
- password_hash
- role
- created_at

### Company

Representa al hotel o pyme turística analizada.

Campos previstos:

- id
- user_id
- name
- municipality
- business_type
- rooms_count
- permanent_employees
- temporary_employees
- has_external_it_provider
- created_at

### Assessment

Representa un análisis realizado a una empresa.

Campos previstos:

- id
- company_id
- status
- overall_score
- risk_level
- created_at
- completed_at

### AssessmentAnswer

Guarda las respuestas del formulario.

Campos previstos:

- id
- assessment_id
- section
- question_key
- answer_value

### Risk

Riesgo detectado durante el análisis.

Campos previstos:

- id
- assessment_id
- title
- description
- probability
- impact
- severity
- recommendation

### Policy

Política generada por IA.

Campos previstos:

- id
- assessment_id
- policy_type
- title
- content
- created_at

### Report

Informe PDF generado.

Campos previstos:

- id
- assessment_id
- file_path
- created_at

## Nota

Este modelo puede cambiar durante el desarrollo, pero sirve como base para diseñar la API y la base de datos.
