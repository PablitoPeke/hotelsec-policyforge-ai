import { riskLabels } from '../data/assessmentDefaults'
import type { ApiConnectionState, AssessmentState, PolicyPackState } from '../types/app'

type HeroPanelProps = {
  apiConnection: ApiConnectionState
  assessment: AssessmentState
  policyPack: PolicyPackState
}

export function HeroPanel({ apiConnection, assessment, policyPack }: HeroPanelProps) {
  const apiText =
    apiConnection.status === 'online'
      ? 'API conectada'
      : apiConnection.status === 'offline'
        ? 'API pendiente'
        : 'Comprobando API'

  return (
    <section className="hero-panel" aria-label="Resumen del proyecto">
      <div className="hero-copy">
        <p className="eyebrow">MVP Práctica 1 · Lanzarote</p>
        <h1>Panel de madurez y políticas para alojamientos turísticos</h1>
        <p>
          Analiza controles clave de ciberseguridad, prioriza riesgos y genera un
          primer pack de políticas adaptado a hoteles, villas y pymes turísticas.
        </p>
        <div className="hero-actions" aria-label="Estado del flujo">
          <span>{apiText}</span>
          <span>{assessment ? `Riesgo ${riskLabels[assessment.risk_level]}` : 'Demo lista'}</span>
          <span>{policyPack ? `${policyPack.policies.length} políticas` : 'Pack pendiente'}</span>
        </div>
      </div>

      <div className="hero-summary-card">
        <span>Preparado para demo</span>
        <strong>{assessment ? `${assessment.overall_score}/100` : 'MVP'}</strong>
        <p>
          {assessment
            ? `${assessment.risks.length} riesgos detectados y ${policyPack?.policies.length ?? 0} políticas generadas.`
            : 'Completa el formulario o usa los datos demo para generar el análisis.'}
        </p>
      </div>
    </section>
  )
}
