import { riskLabels } from '../data/assessmentDefaults'
import type { PolicyPackState } from '../types/app'

type PolicyPackPanelProps = {
  policyPack: PolicyPackState
}

export function PolicyPackPanel({ policyPack }: PolicyPackPanelProps) {
  return (
    <article className="panel policy-panel" id="politicas">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Pack generado</p>
          <h2>Políticas recomendadas</h2>
        </div>
        {policyPack ? (
          <span className={`severity severity-${policyPack.risk_level}`}>
            {riskLabels[policyPack.risk_level]}
          </span>
        ) : null}
      </div>

      {policyPack ? (
        <>
          <div className="implementation-box">
            <h3>Orden de implantación</h3>
            <ol>
              {policyPack.implementation_order.map((step) => (
                <li key={step}>{step}</li>
              ))}
            </ol>
          </div>

          <div className="policy-list">
            {policyPack.policies.map((policy) => (
              <section className="policy-item" key={policy.name}>
                <header>
                  <h3>{policy.name}</h3>
                  <p>{policy.objective}</p>
                </header>
                <p>
                  <strong>Alcance:</strong> {policy.scope}
                </p>
                <div className="control-list">
                  {policy.controls.map((control) => (
                    <div className="control-item" key={`${policy.name}-${control.title}`}>
                      <span className={`severity severity-${control.priority}`}>
                        {riskLabels[control.priority]}
                      </span>
                      <div>
                        <strong>{control.title}</strong>
                        <p>{control.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
                <p>
                  <strong>Revisión:</strong> {policy.review_frequency}
                </p>
              </section>
            ))}
          </div>
        </>
      ) : (
        <p>Cuando ejecutes el análisis, el backend generará aquí el pack inicial de políticas.</p>
      )}
    </article>
  )
}
