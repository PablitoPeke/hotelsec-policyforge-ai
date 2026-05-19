const riskRows = [
  {
    name: 'Doble factor desactivado',
    severity: 'Alto',
    area: 'Identidad',
    status: 'Pendiente',
  },
  {
    name: 'Backups sin verificar',
    severity: 'Medio',
    area: 'Continuidad',
    status: 'Pendiente',
  },
  {
    name: 'WiFi de huéspedes no separada',
    severity: 'Alto',
    area: 'Red',
    status: 'Pendiente',
  },
]

function App() {
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
          <span className="status-pill">Backend preparado</span>
        </header>

        <section className="metric-grid" aria-label="Indicadores principales">
          <article className="metric-card">
            <span>Puntuación demo</span>
            <strong>42/100</strong>
            <p>Madurez media-baja</p>
          </article>
          <article className="metric-card">
            <span>Riesgos activos</span>
            <strong>3</strong>
            <p>2 altos, 1 medio</p>
          </article>
          <article className="metric-card">
            <span>Políticas</span>
            <strong>0</strong>
            <p>Pendiente de IA</p>
          </article>
          <article className="metric-card">
            <span>Informe PDF</span>
            <strong>No</strong>
            <p>Módulo futuro</p>
          </article>
        </section>

        <section className="content-grid">
          <article className="panel" id="analisis">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Endpoint actual</p>
                <h2>Analizador de hoteles</h2>
              </div>
              <code>POST /api/v1/assessments/analyze</code>
            </div>
            <p>
              El backend ya recibe un perfil de hotel, calcula madurez de seguridad
              y devuelve riesgos priorizados mediante reglas controladas.
            </p>
            <div className="score-strip">
              <span>Identidad</span>
              <div><span style={{ width: '33%' }} /></div>
              <strong>33%</strong>
            </div>
            <div className="score-strip">
              <span>Backups</span>
              <div><span style={{ width: '30%' }} /></div>
              <strong>30%</strong>
            </div>
            <div className="score-strip">
              <span>Red</span>
              <div><span style={{ width: '25%' }} /></div>
              <strong>25%</strong>
            </div>
          </article>

          <article className="panel" id="riesgos">
            <div className="panel-header">
              <div>
                <p className="eyebrow">Vista previa</p>
                <h2>Riesgos detectados</h2>
              </div>
            </div>
            <div className="risk-table" role="table" aria-label="Riesgos detectados">
              <div className="risk-row risk-head" role="row">
                <span>Riesgo</span>
                <span>Área</span>
                <span>Nivel</span>
                <span>Estado</span>
              </div>
              {riskRows.map((risk) => (
                <div className="risk-row" role="row" key={risk.name}>
                  <span>{risk.name}</span>
                  <span>{risk.area}</span>
                  <span className={`severity severity-${risk.severity.toLowerCase()}`}>
                    {risk.severity}
                  </span>
                  <span>{risk.status}</span>
                </div>
              ))}
            </div>
          </article>
        </section>
      </section>
    </main>
  )
}

export default App
