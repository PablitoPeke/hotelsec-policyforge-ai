export function Sidebar() {
  return (
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
  )
}
