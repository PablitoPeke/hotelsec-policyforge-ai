import { useEffect, useMemo, useState, type FormEvent } from 'react'

import {
  analyzeHotelAssessment,
  type AssessmentRequest,
  type AssessmentResponse,
  type BackupFrequency,
  type BusinessType,
  type RiskLevel,
} from './api/assessment'
import { fetchHealthStatus, type HealthStatus } from './api/health'

type ApiConnectionState =
  | { status: 'checking' }
  | { status: 'online'; data: HealthStatus }
  | { status: 'offline'; message: string }

type FormState = {
  businessName: string
  municipality: string
  businessType: BusinessType
  roomsCount: number
  permanentEmployees: number
  temporaryEmployees: number
  hasExternalItProvider: boolean
  usesMfa: boolean
  usesPasswordManager: boolean
  sharedAccounts: boolean
  backupFrequency: BackupFrequency
  backupsTested: boolean
  hasAntivirus: boolean
  systemsUpdated: boolean
  guestWifiSeparated: boolean
  hasIncidentResponsePlan: boolean
  hasRgpdBreachProtocol: boolean
  staffPhishingTraining: boolean
}

const initialFormState: FormState = {
  businessName: 'Hotel Demo Lanzarote',
  municipality: 'Tías',
  businessType: 'hotel',
  roomsCount: 42,
  permanentEmployees: 12,
  temporaryEmployees: 8,
  hasExternalItProvider: true,
  usesMfa: false,
  usesPasswordManager: false,
  sharedAccounts: true,
  backupFrequency: 'none',
  backupsTested: false,
  hasAntivirus: true,
  systemsUpdated: false,
  guestWifiSeparated: false,
  hasIncidentResponsePlan: false,
  hasRgpdBreachProtocol: false,
  staffPhishingTraining: false,
}

const riskLabels: Record<RiskLevel, string> = {
  low: 'Bajo',
  medium: 'Medio',
  high: 'Alto',
  critical: 'Crítico',
}

function App() {
  const [apiConnection, setApiConnection] = useState<ApiConnectionState>({
    status: 'checking',
  })
  const [formState, setFormState] = useState<FormState>(initialFormState)
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [assessmentError, setAssessmentError] = useState<string | null>(null)

  useEffect(() => {
    let ignore = false

    fetchHealthStatus()
      .then((data) => {
        if (!ignore) {
          setApiConnection({ status: 'online', data })
        }
      })
      .catch((error: unknown) => {
        if (!ignore) {
          setApiConnection({
            status: 'offline',
            message: error instanceof Error ? error.message : 'No se pudo conectar con la API',
          })
        }
      })

    return () => {
      ignore = true
    }
  }, [])

  const apiStatusText =
    apiConnection.status === 'online'
      ? `Backend online · ${apiConnection.data.version}`
      : apiConnection.status === 'offline'
        ? 'Backend offline'
        : 'Comprobando backend'

  const activeRisks = assessment?.risks ?? []
  const highOrCriticalRisks = activeRisks.filter(
    (risk) => risk.severity === 'high' || risk.severity === 'critical',
  ).length

  const areaScores = useMemo(() => assessment?.area_scores ?? [], [assessment])

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setFormState((current) => ({
      ...current,
      [key]: value,
    }))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsAnalyzing(true)
    setAssessmentError(null)

    const payload: AssessmentRequest = {
      hotel_profile: {
        business_name: formState.businessName,
        municipality: formState.municipality,
        business_type: formState.businessType,
        rooms_count: formState.roomsCount,
        permanent_employees: formState.permanentEmployees,
        temporary_employees: formState.temporaryEmployees,
        has_external_it_provider: formState.hasExternalItProvider,
      },
      security_controls: {
        uses_mfa: formState.usesMfa,
        uses_password_manager: formState.usesPasswordManager,
        shared_accounts: formState.sharedAccounts,
        backup_frequency: formState.backupFrequency,
        backups_tested: formState.backupsTested,
        has_antivirus: formState.hasAntivirus,
        systems_updated: formState.systemsUpdated,
        guest_wifi_separated: formState.guestWifiSeparated,
        has_incident_response_plan: formState.hasIncidentResponsePlan,
        has_rgpd_breach_protocol: formState.hasRgpdBreachProtocol,
        staff_phishing_training: formState.staffPhishingTraining,
      },
    }

    try {
      const result = await analyzeHotelAssessment(payload)
      setAssessment(result)
    } catch (error) {
      setAssessmentError(
        error instanceof Error ? error.message : 'No se pudo completar el análisis',
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <main className="app-shell">
      <aside className="sidebar" aria-label="Navegación principal">
        <div className="brand">
          <span className="brand-mark">H</span>
          <div>
            <strong>HotelSec</strong>
            <span>PolicyForge AI</span>
          </div>
        </div>
        <nav className="nav-list">
          <a href="#dashboard" aria-current="page">Dashboard</a>
          <a href="#analisis">Análisis</a>
          <a href="#riesgos">Riesgos</a>
          <a href="#politicas">Políticas</a>
        </nav>
      </aside>

      <section className="workspace" id="dashboard">
        <header className="topbar">
          <div>
            <p className="eyebrow">MVP Práctica 1</p>
            <h1>Panel inicial de madurez hotelera</h1>
          </div>
          <span className={`status-pill status-${apiConnection.status}`}>
            {apiStatusText}
          </span>
        </header>

        <section className="metric-grid" aria-label="Indicadores principales">
          <article className="metric-card">
            <span>Puntuación</span>
            <strong>{assessment ? `${assessment.overall_score}/100` : '-'}</strong>
            <p>{assessment ? `Riesgo ${riskLabels[assessment.risk_level]}` : 'Sin análisis'}</p>
          </article>
          <article className="metric-card">
            <span>Riesgos activos</span>
            <strong>{activeRisks.length}</strong>
            <p>{assessment ? `${highOrCriticalRisks} altos/críticos` : 'Esperando formulario'}</p>
          </article>
          <article className="metric-card">
            <span>Políticas</span>
            <strong>0</strong>
            <p>Pendiente de IA</p>
          </article>
          <article className="metric-card">
            <span>API</span>
            <strong>{apiConnection.status === 'online' ? 'OK' : 'No'}</strong>
            <p>
              {apiConnection.status === 'online'
                ? apiConnection.data.service
                : apiConnection.status === 'offline'
                  ? apiConnection.message
                  : 'Esperando respuesta'}
            </p>
          </article>
        </section>

        <section className="content-grid content-grid-wide">
          <article className="panel" id="analisis">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Formulario inicial</p>
                <h2>Analizador de hoteles</h2>
              </div>
              <code>POST /api/v1/assessments/analyze</code>
            </div>

            <form className="assessment-form" onSubmit={handleSubmit}>
              <div className="form-grid">
                <label>
                  Nombre del alojamiento
                  <input
                    value={formState.businessName}
                    onChange={(event) => updateField('businessName', event.target.value)}
                  />
                </label>
                <label>
                  Municipio
                  <input
                    value={formState.municipality}
                    onChange={(event) => updateField('municipality', event.target.value)}
                  />
                </label>
                <label>
                  Tipo
                  <select
                    value={formState.businessType}
                    onChange={(event) =>
                      updateField('businessType', event.target.value as BusinessType)
                    }
                  >
                    <option value="hotel">Hotel</option>
                    <option value="apartahotel">Apartahotel</option>
                    <option value="villa">Villa</option>
                    <option value="hostal">Hostal</option>
                    <option value="alquiler_vacacional">Alquiler vacacional</option>
                    <option value="agencia_turistica">Agencia turística</option>
                  </select>
                </label>
                <label>
                  Habitaciones
                  <input
                    min="1"
                    type="number"
                    value={formState.roomsCount}
                    onChange={(event) => updateField('roomsCount', Number(event.target.value))}
                  />
                </label>
                <label>
                  Empleados fijos
                  <input
                    min="0"
                    type="number"
                    value={formState.permanentEmployees}
                    onChange={(event) =>
                      updateField('permanentEmployees', Number(event.target.value))
                    }
                  />
                </label>
                <label>
                  Empleados temporales
                  <input
                    min="0"
                    type="number"
                    value={formState.temporaryEmployees}
                    onChange={(event) =>
                      updateField('temporaryEmployees', Number(event.target.value))
                    }
                  />
                </label>
                <label>
                  Frecuencia de backups
                  <select
                    value={formState.backupFrequency}
                    onChange={(event) =>
                      updateField('backupFrequency', event.target.value as BackupFrequency)
                    }
                  >
                    <option value="none">No se realizan</option>
                    <option value="monthly">Mensual</option>
                    <option value="weekly">Semanal</option>
                    <option value="daily">Diaria</option>
                  </select>
                </label>
              </div>

              <div className="checkbox-grid">
                <label><input type="checkbox" checked={formState.hasExternalItProvider} onChange={(event) => updateField('hasExternalItProvider', event.target.checked)} />Proveedor IT externo</label>
                <label><input type="checkbox" checked={formState.usesMfa} onChange={(event) => updateField('usesMfa', event.target.checked)} />Usa doble factor</label>
                <label><input type="checkbox" checked={formState.usesPasswordManager} onChange={(event) => updateField('usesPasswordManager', event.target.checked)} />Usa gestor de contraseñas</label>
                <label><input type="checkbox" checked={formState.sharedAccounts} onChange={(event) => updateField('sharedAccounts', event.target.checked)} />Comparte cuentas</label>
                <label><input type="checkbox" checked={formState.backupsTested} onChange={(event) => updateField('backupsTested', event.target.checked)} />Prueba restauración de backups</label>
                <label><input type="checkbox" checked={formState.hasAntivirus} onChange={(event) => updateField('hasAntivirus', event.target.checked)} />Tiene antivirus/EDR</label>
                <label><input type="checkbox" checked={formState.systemsUpdated} onChange={(event) => updateField('systemsUpdated', event.target.checked)} />Sistemas actualizados</label>
                <label><input type="checkbox" checked={formState.guestWifiSeparated} onChange={(event) => updateField('guestWifiSeparated', event.target.checked)} />WiFi de huéspedes separada</label>
                <label><input type="checkbox" checked={formState.hasIncidentResponsePlan} onChange={(event) => updateField('hasIncidentResponsePlan', event.target.checked)} />Plan de respuesta a incidentes</label>
                <label><input type="checkbox" checked={formState.hasRgpdBreachProtocol} onChange={(event) => updateField('hasRgpdBreachProtocol', event.target.checked)} />Protocolo de brechas RGPD</label>
                <label><input type="checkbox" checked={formState.staffPhishingTraining} onChange={(event) => updateField('staffPhishingTraining', event.target.checked)} />Formación contra phishing</label>
              </div>

              <button className="primary-button" disabled={isAnalyzing} type="submit">
                {isAnalyzing ? 'Analizando...' : 'Analizar hotel'}
              </button>
              {assessmentError ? <p className="form-error">{assessmentError}</p> : null}
            </form>
          </article>

          <article className="panel" id="riesgos">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Resultado</p>
                <h2>{assessment ? assessment.business_name : 'Sin análisis todavía'}</h2>
              </div>
            </div>

            {assessment ? (
              <>
                {areaScores.map((area) => (
                  <div className="score-strip" key={area.area}>
                    <span>{area.area}</span>
                    <div><span style={{ width: `${area.score}%` }} /></div>
                    <strong>{area.score}%</strong>
                  </div>
                ))}

                <div className="risk-table" role="table" aria-label="Riesgos detectados">
                  <div className="risk-row risk-head" role="row">
                    <span>Riesgo</span>
                    <span>Nivel</span>
                    <span>Recomendación</span>
                  </div>
                  {assessment.risks.length > 0 ? (
                    assessment.risks.map((risk) => (
                      <div className="risk-row risk-row-result" role="row" key={risk.title}>
                        <span>{risk.title}</span>
                        <span className={`severity severity-${risk.severity}`}>
                          {riskLabels[risk.severity]}
                        </span>
                        <span>{risk.recommendation}</span>
                      </div>
                    ))
                  ) : (
                    <div className="empty-state">
                      No se han detectado riesgos prioritarios con las reglas actuales.
                    </div>
                  )}
                </div>
              </>
            ) : (
              <p>
                Completa o ajusta el formulario y pulsa analizar. El resultado vendrá
                directamente del backend FastAPI.
              </p>
            )}
          </article>
        </section>
      </section>
    </main>
  )
}

export default App
