import { riskLabels } from '../data/assessmentDefaults'
import type { AssessmentState, PolicyPackState } from '../types/app'
import { buildExecutiveReportPdf } from '../utils/pdfReport'

type ExecutiveReportPanelProps = {
  assessment: AssessmentState
  policyPack: PolicyPackState
}

export function ExecutiveReportPanel({
  assessment,
  policyPack,
}: ExecutiveReportPanelProps) {
  const topRisks = assessment?.risks.slice(0, 4) ?? []
  const evidenceItems = Array.from(
    new Set(policyPack?.policies.flatMap((policy) => policy.evidence) ?? []),
  ).slice(0, 8)

  function downloadReport() {
    if (!assessment || !policyPack) {
      return
    }

    const blob = buildExecutiveReportPdf(assessment, policyPack)
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `hotelsec-informe-${assessment.business_name
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')}.pdf`
    link.click()
    URL.revokeObjectURL(url)
  }

  return (
    <article className="panel report-panel" id="informe">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Resumen ejecutivo</p>
          <h2>Informe listo para presentar</h2>
        </div>
        <button
          className="secondary-button"
          disabled={!assessment || !policyPack}
          type="button"
          onClick={downloadReport}
        >
          Descargar PDF
        </button>
      </div>

      {assessment && policyPack ? (
        <div className="report-grid">
          <section className="report-card report-card-strong">
            <span>Nivel de riesgo</span>
            <strong>{riskLabels[assessment.risk_level]}</strong>
            <p>
              Puntuación {assessment.overall_score}/100 con {assessment.risks.length}{' '}
              riesgos activos y {policyPack.policies.length} políticas generadas.
            </p>
          </section>

          <section className="report-card">
            <h3>Prioridades inmediatas</h3>
            <ul>
              {policyPack.implementation_order.slice(0, 4).map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ul>
          </section>

          <section className="report-card">
            <h3>Riesgos clave</h3>
            {topRisks.length > 0 ? (
              <ul>
                {topRisks.map((risk) => (
                  <li key={risk.title}>{risk.title}</li>
                ))}
              </ul>
            ) : (
              <p>No hay riesgos prioritarios con las reglas actuales.</p>
            )}
          </section>

          <section className="report-card">
            <h3>Evidencias a recopilar</h3>
            <ul>
              {evidenceItems.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </section>
        </div>
      ) : (
        <p>
          Ejecuta el análisis para generar un resumen ejecutivo con prioridades,
          evidencias y exportación del resultado en PDF.
        </p>
      )}
    </article>
  )
}
