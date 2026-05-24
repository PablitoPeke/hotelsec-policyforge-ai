import { BrandLogo } from './BrandLogo'

export function Sidebar() {
  return (
    <aside className="sidebar" aria-label="Navegación principal">
      <div className="brand">
        <BrandLogo />
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
        <a href="#informe">Informe</a>
      </nav>
      <div className="sidebar-footer">
        <span>Entrega pública</span>
        <strong>Render · FastAPI · React</strong>
      </div>
    </aside>
  )
}
