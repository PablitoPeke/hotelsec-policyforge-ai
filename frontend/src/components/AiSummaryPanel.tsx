import type { AiSummaryState } from '../types/app'

type AiSummaryPanelProps = {
  aiSummary: AiSummaryState
  isLoading: boolean
}

export function AiSummaryPanel({ aiSummary, isLoading }: AiSummaryPanelProps) {
  return (
    <article className="panel ai-panel" id="ia">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Asistente IA</p>
          <h2>Resumen inteligente</h2>
        </div>
        {aiSummary ? (
          <span className={aiSummary.generated_by_ai ? 'ai-badge ai-badge-live' : 'ai-badge'}>
            {aiSummary.generated_by_ai ? aiSummary.model : 'Fallback reglas'}
          </span>
        ) : null}
      </div>

      {isLoading ? (
        <p>Generando resumen para dirección...</p>
      ) : aiSummary ? (
        <p className="ai-summary-text">{aiSummary.summary}</p>
      ) : (
        <p>
          Ejecuta el análisis para generar un resumen ejecutivo. Si Render tiene
          `OPENAI_API_KEY`, este bloque usará IA; si no, usará reglas de respaldo.
        </p>
      )}
    </article>
  )
}
