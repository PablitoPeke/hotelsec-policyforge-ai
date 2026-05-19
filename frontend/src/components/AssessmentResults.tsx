import { riskLabels } from '../data/assessmentDefaults'
import type { AssessmentState } from '../types/app'

type AssessmentResultsProps = {
  assessment: AssessmentState
}

export function AssessmentResults({ assessment }: AssessmentResultsProps) {
  return (
    <article className="panel" id="riesgos">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Resultado</p>
          <h2>{assessment ? assessment.business_name : 'Sin análisis todavía'}</h2>
        </div>
      </div>

      {assessment ? (
        <>
          {assessment.area_scores.map((area) => (
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
  )
}
