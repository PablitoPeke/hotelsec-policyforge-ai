# 08. Ejemplos de uso del analizador

Este documento explica de forma sencilla cómo funciona el primer endpoint real del backend.

## Endpoint

```http
POST /api/v1/assessments/analyze
```

## Qué hace

Este endpoint recibe datos básicos de un hotel y una serie de controles de seguridad. Con esa información calcula:

- puntuación global de madurez,
- nivel de riesgo,
- puntuaciones por área,
- riesgos detectados,
- próximos pasos recomendados.

De momento no usa IA ni base de datos. Es una primera versión basada en reglas para que el proyecto tenga una lógica de ciberseguridad clara y comprobable.

## Por qué empezamos así

Antes de generar políticas con IA, necesitamos saber qué problemas tiene la empresa. Por eso este endpoint actúa como el primer motor de análisis.

Ejemplos de reglas:

- Si no hay doble factor de autenticación, aparece un riesgo alto.
- Si se comparten cuentas, aparece un riesgo alto.
- Si no hay copias de seguridad, aparece un riesgo crítico.
- Si la WiFi de huéspedes no está separada, aparece un riesgo alto.
- Si no existe protocolo de brechas RGPD, aparece un riesgo medio.
- Si el personal no recibe formación contra phishing, aparece un riesgo medio.

## Ejemplo de petición

```json
{
  "hotel_profile": {
    "business_name": "Hotel Demo Lanzarote",
    "municipality": "Tías",
    "business_type": "hotel",
    "rooms_count": 42,
    "permanent_employees": 12,
    "temporary_employees": 8,
    "has_external_it_provider": true
  },
  "security_controls": {
    "uses_mfa": false,
    "uses_password_manager": false,
    "shared_accounts": true,
    "backup_frequency": "none",
    "backups_tested": false,
    "has_antivirus": true,
    "systems_updated": false,
    "guest_wifi_separated": false,
    "has_incident_response_plan": false,
    "has_rgpd_breach_protocol": false,
    "staff_phishing_training": false
  }
}
```

## Ejemplo de respuesta

La respuesta exacta puede cambiar si se ajustan las reglas, pero tendrá esta estructura:

```json
{
  "business_name": "Hotel Demo Lanzarote",
  "overall_score": 18,
  "risk_level": "critical",
  "area_scores": [
    {
      "area": "Identidad y accesos",
      "score": 0
    },
    {
      "area": "Copias de seguridad",
      "score": 0
    },
    {
      "area": "Protección de dispositivos",
      "score": 50
    },
    {
      "area": "Seguridad de red",
      "score": 25
    },
    {
      "area": "Respuesta a incidentes",
      "score": 0
    },
    {
      "area": "Concienciación del personal",
      "score": 20
    }
  ],
  "risks": [
    {
      "title": "Falta de doble factor de autenticación",
      "description": "Las cuentas críticas del hotel podrían quedar expuestas si una contraseña se filtra o se reutiliza en otro servicio.",
      "severity": "high",
      "recommendation": "Activar MFA en correo, PMS, paneles de reservas y cuentas administrativas."
    },
    {
      "title": "Uso de cuentas compartidas",
      "description": "Compartir usuarios impide saber quién realizó una acción y dificulta revocar accesos cuando cambia el personal.",
      "severity": "high",
      "recommendation": "Crear usuarios individuales para recepción, administración y proveedores."
    },
    {
      "title": "Ausencia de copias de seguridad",
      "description": "Un incidente de ransomware, borrado accidental o fallo técnico podría provocar pérdida de reservas, facturación o documentación de clientes.",
      "severity": "critical",
      "recommendation": "Implantar copias de seguridad automáticas y mantener al menos una copia aislada."
    }
  ],
  "next_steps": [
    "Activar MFA en correo, PMS, paneles de reservas y cuentas administrativas.",
    "Crear usuarios individuales para recepción, administración y proveedores.",
    "Implantar copias de seguridad automáticas y mantener al menos una copia aislada."
  ]
}
```

## Cómo probarlo desde Swagger

Cuando el backend esté levantado, abrir:

```text
http://localhost:8000/docs
```

Después:

1. Buscar `POST /api/v1/assessments/analyze`.
2. Pulsar en `Try it out`.
3. Pegar el JSON de ejemplo.
4. Pulsar `Execute`.
5. Revisar la puntuación y los riesgos generados.

## Cómo probarlo con PowerShell

```powershell
$body = @{
  hotel_profile = @{
    business_name = "Hotel Demo Lanzarote"
    municipality = "Tías"
    business_type = "hotel"
    rooms_count = 42
    permanent_employees = 12
    temporary_employees = 8
    has_external_it_provider = $true
  }
  security_controls = @{
    uses_mfa = $false
    uses_password_manager = $false
    shared_accounts = $true
    backup_frequency = "none"
    backups_tested = $false
    has_antivirus = $true
    systems_updated = $false
    guest_wifi_separated = $false
    has_incident_response_plan = $false
    has_rgpd_breach_protocol = $false
    staff_phishing_training = $false
  }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod `
  -Method Post `
  -Uri "http://localhost:8000/api/v1/assessments/analyze" `
  -ContentType "application/json" `
  -Body $body
```

## Cómo explicar esto en la demo

Una explicación sencilla sería:

> Esta primera parte del backend analiza el perfil de seguridad de un hotel. Todavía no usa inteligencia artificial; primero aplica reglas claras de ciberseguridad para calcular madurez y riesgos. Después, en fases posteriores, la IA usará estos resultados para generar políticas, recomendaciones e informes.

