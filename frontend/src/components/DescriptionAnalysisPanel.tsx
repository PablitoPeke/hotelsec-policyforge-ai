import type { FormEvent } from 'react'

type DescriptionAnalysisPanelProps = {
  description: string
  error: string | null
  isAnalyzing: boolean
  onDescriptionChange: (value: string) => void
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
}

export function DescriptionAnalysisPanel({
  description,
  error,
  isAnalyzing,
  onDescriptionChange,
  onSubmit,
}: DescriptionAnalysisPanelProps) {
  return (
    <article className="panel description-panel">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Análisis por descripción</p>
          <h2>Cuéntalo con tus palabras</h2>
        </div>
        <code>POST /api/v1/ai/analyze-description</code>
      </div>

      <form className="description-form" onSubmit={onSubmit}>
        <label>
          Descripción libre del alojamiento
          <textarea
            minLength={20}
            placeholder="Ejemplo: usamos PMS externo, la WiFi de clientes comparte router con recepción, los proveedores entran por AnyDesk, hacemos copias semanales pero nunca hemos probado restaurarlas..."
            rows={7}
            value={description}
            onChange={(event) => onDescriptionChange(event.target.value)}
          />
        </label>
        <button className="secondary-button" disabled={isAnalyzing} type="submit">
          {isAnalyzing ? 'Analizando descripción...' : 'Analizar descripción con IA'}
        </button>
        {error ? <p className="form-error">{error}</p> : null}
      </form>
    </article>
  )
}
