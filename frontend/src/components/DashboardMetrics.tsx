import { riskLabels } from '../data/assessmentDefaults'
import type { ApiConnectionState, AssessmentState } from '../types/app'

type DashboardMetricsProps = {
  apiConnection: ApiConnectionState
  assessment: AssessmentState
}

export function DashboardMetrics({ apiConnection, assessment }: DashboardMetricsProps) {
  const activeRisks = assessment?.risks ?? []
  const highOrCriticalRisks = activeRisks.filter(
    (risk) => risk.severity === 'high' || risk.severity === 'critical',
  ).length

  return (
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
  )
}
