import { useEffect, useState, type FormEvent } from 'react'
import {
  LayoutDashboard,
  ClipboardList,
  History,
  FileCheck,
  ListChecks,
  Download,
  LogOut,
  UserRound,
  Plus,
  Trash2,
  Eye,
  EyeOff,
  ArrowLeft,
  ArrowRight,
} from 'lucide-react'
import {
  ApiError,
  downloadReport,
  request,
  session,
  type User,
  type RecordDetail,
  type HistoryItem,
  type Conflict,
  type Action,
} from './api/product'
import { AssessmentForm } from './components/AssessmentForm'
import { AssessmentResults } from './components/AssessmentResults'
import { PolicyPackPanel } from './components/PolicyPackPanel'
import { AiSummaryPanel } from './components/AiSummaryPanel'
import { BrandLogo } from './components/BrandLogo'
import { initialFormState, riskLabels } from './data/assessmentDefaults'
import { extraControls, fromPayload, toPayload } from './utils/formAdapter'
import type { FormState } from './types/app'

const navigation = [
  ['dashboard', 'Dashboard', LayoutDashboard],
  ['analysis', 'Nuevo analisis', ClipboardList],
  ['history', 'Historial', History],
  ['policies', 'Politicas', FileCheck],
  ['actions', 'Plan de mejora', ListChecks],
  ['report', 'Informe', Download],
  ['account', 'Mi cuenta', UserRound],
] as const
const initialContext = {
  season: 'Todo el ano',
  inventory: '',
  categories: '',
  retention: 180,
  response: 24,
}
const emptyExtra = Object.fromEntries(
  Object.keys(extraControls).map((k) => [k, null]),
) as Record<string, boolean | null>
const date = (s: string) =>
  new Date(s.endsWith('Z') || /[+-]\d\d:\d\d$/.test(s) ? s : `${s}Z`).toLocaleString(
    'es-ES',
  )
const errorMessage = (e: unknown) =>
  e instanceof Error ? e.message : 'No se pudo completar la operacion.'

function Auth({ onAccess }: { onAccess: (u: User) => void }) {
  const [register, setRegister] = useState(false),
    [error, setError] = useState(''),
    [busy, setBusy] = useState(false),
    [show, setShow] = useState(false)
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setBusy(true)
    setError('')
    const values = Object.fromEntries(new FormData(event.currentTarget))
    try {
      onAccess(await session(register ? '/auth/register' : '/auth/login', values))
    } catch (e) {
      setError(errorMessage(e))
    } finally {
      setBusy(false)
    }
  }
  return (
    <main className="auth-page">
      <section className="auth-form">
        <div className="auth-brand">
          <BrandLogo />
          <div>
            <h1>HotelSec</h1>
            <p>PolicyForge AI · Lanzarote</p>
          </div>
        </div>
        <div className="mode-tabs">
          <button
            aria-pressed={!register}
            onClick={() => {
              setRegister(false)
              setError('')
            }}
          >
            Acceder
          </button>
          <button
            aria-pressed={register}
            onClick={() => {
              setRegister(true)
              setError('')
            }}
          >
            Crear cuenta
          </button>
        </div>
        <form onSubmit={submit} className="fields">
          {register && (
            <label>
              Nombre
              <input
                name="name"
                required
                minLength={2}
                maxLength={120}
                autoComplete="name"
              />
            </label>
          )}
          <label>
            Correo electronico
            <input name="email" required type="email" autoComplete="email" />
          </label>
          <label>
            Contrasena
            <div className="password-field">
              <input
                aria-label="Contrasena"
                name="password"
                required
                type={show ? 'text' : 'password'}
                minLength={12}
                maxLength={128}
                autoComplete={register ? 'new-password' : 'current-password'}
              />
              <button
                type="button"
                title={show ? 'Ocultar contrasena' : 'Mostrar contrasena'}
                aria-label={show ? 'Ocultar contrasena' : 'Mostrar contrasena'}
                onClick={() => setShow(!show)}
              >
                {show ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            </div>
            <small>Minimo 12 caracteres.</small>
          </label>
          {register && (
            <p className="notice">
              Tus analisis se guardaran en tu cuenta. No introduzcas datos de huespedes,
              documentos de identidad ni informacion de pago. Puedes borrar tu cuenta y
              sus datos.
            </p>
          )}
          {error && (
            <p role="alert" className="form-error">
              {error}
            </p>
          )}
          <button className="primary-button" disabled={busy}>
            {busy ? 'Conectando...' : register ? 'Crear cuenta' : 'Acceder'}
          </button>
        </form>
      </section>
    </main>
  )
}

function App() {
  const [user, setUser] = useState<User | null>(null),
    [booting, setBooting] = useState(true),
    [view, setView] = useState('dashboard')
  const [form, setForm] = useState(initialFormState),
    [context, setContext] = useState(initialContext),
    [extra, setExtra] = useState(emptyExtra)
  const [description, setDescription] = useState(''),
    [useAi, setUseAi] = useState(false),
    [busy, setBusy] = useState(false)
  const [error, setError] = useState(''),
    [record, setRecord] = useState<RecordDetail | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([]),
    [total, setTotal] = useState(0),
    [offset, setOffset] = useState(0),
    [filter, setFilter] = useState('')
  const [conflicts, setConflicts] = useState<Conflict[]>([]),
    [audit, setAudit] = useState<{ event: string; created_at: string }[]>([])
  const [deleting, setDeleting] = useState<string | null>(null),
    [accountPassword, setAccountPassword] = useState(''),
    [online, setOnline] = useState(false)
  useEffect(() => {
    session()
      .then(setUser)
      .catch((e) => {
        if (!(e instanceof ApiError && e.status === 401)) setError(errorMessage(e))
      })
      .finally(() => setBooting(false))
    request('/health')
      .then(() => setOnline(true))
      .catch(() => setOnline(false))
  }, [])
  async function refresh(page = offset, company = filter) {
    const data = await request<{ items: HistoryItem[]; total: number }>(
      `/records?limit=20&offset=${page}${company ? `&company_id=${encodeURIComponent(company)}` : ''}`,
    )
    setHistory(data.items)
    setTotal(data.total)
  }
  useEffect(() => {
    if (user) refresh().catch((e) => setError(errorMessage(e)))
  }, [user, offset, filter])
  async function run(operation: () => Promise<void>) {
    setBusy(true)
    setError('')
    try {
      await operation()
    } catch (e) {
      setError(errorMessage(e))
      if (e instanceof ApiError && e.status === 401) setUser(null)
    } finally {
      setBusy(false)
    }
  }
  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setForm((current) => ({ ...current, [key]: value }))
  }
  function newAnalysis() {
    setForm(initialFormState)
    setContext(initialContext)
    setExtra(emptyExtra)
    setDescription('')
    setRecord(null)
    setView('analysis')
    setError('')
  }
  function loadForm(r: RecordDetail) {
    setForm(fromPayload(r.input))
    setDescription(r.description)
    const profile = r.input.hotel_profile as typeof r.input.hotel_profile & {
      high_season: string
      technology_inventory: string[]
      personal_data_categories: string[]
      retention_days: number
      it_response_hours: number
    }
    setContext({
      season: profile.high_season,
      inventory: profile.technology_inventory.join(', '),
      categories: profile.personal_data_categories.join(', '),
      retention: profile.retention_days,
      response: profile.it_response_hours,
    })
    setExtra(
      Object.fromEntries(
        Object.keys(extraControls).map((k) => [
          k,
          (r.input.security_controls as unknown as Record<string, boolean | null>)[k] ??
            null,
        ]),
      ),
    )
  }
  async function analyze(resolution?: 'manual' | 'text') {
    setBusy(true)
    setError('')
    try {
      const result = await request<RecordDetail>('/records', 'POST', {
        assessment: toPayload(form, extra, context),
        description,
        use_ai: useAi,
        conflict_resolution: resolution,
      })
      setRecord(result)
      loadForm(result)
      setConflicts([])
      setView('dashboard')
      await refresh()
    } catch (e) {
      if (
        e instanceof ApiError &&
        e.status === 409 &&
        typeof e.detail === 'object' &&
        e.detail !== null &&
        'conflicts' in e.detail
      )
        setConflicts((e.detail as { conflicts: Conflict[] }).conflicts)
      else {
        setError(errorMessage(e))
        if (e instanceof ApiError && e.status === 401) setUser(null)
      }
    } finally {
      setBusy(false)
    }
  }
  async function open(id: string) {
    const r = await request<RecordDetail>(`/records/${id}`)
    setRecord(r)
    loadForm(r)
    setView('dashboard')
  }
  function navigate(next: string) {
    setView(next)
    setError('')
    if (next === 'account') run(async () => setAudit(await request('/auth/audit')))
  }
  if (booting)
    return (
      <main className="auth-page">
        <p role="status">Conectando con HotelSec...</p>
      </main>
    )
  if (!user)
    return (
      <>
        <Auth
          onAccess={(u) => {
            setError('')
            setHistory([])
            setTotal(0)
            setRecord(null)
            setAudit([])
            setDeleting(null)
            setAccountPassword('')
            setForm(initialFormState)
            setExtra(emptyExtra)
            setContext(initialContext)
            setDescription('')
            setUseAi(false)
            setView('dashboard')
            setUser(u)
          }}
        />
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
      </>
    )
  const previous = record
    ? history.filter(
        (r) =>
          r.company_id === record.company_id &&
          r.id !== record.id &&
          r.created_at < record.created_at,
      )[0]
    : undefined
  const completed = record?.actions.filter((a) => a.status === 'done').length ?? 0
  return (
    <main className="app-shell product-app">
      <aside className="sidebar">
        <div className="brand">
          <BrandLogo />
          <div>
            <strong>HotelSec</strong>
            <span>PolicyForge AI</span>
          </div>
        </div>
        <nav className="nav-list" aria-label="Principal">
          {navigation.map(([id, label, Icon]) => (
            <button
              key={id}
              aria-current={view === id ? 'page' : undefined}
              disabled={busy}
              onClick={() => navigate(id)}
            >
              <Icon size={18} />
              <span>{label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <strong>{user.name}</strong>
          <span>{user.email}</span>
          <button
            onClick={() =>
              run(async () => {
                await request('/auth/logout', 'POST')
                setUser(null)
                setRecord(null)
              })
            }
            disabled={busy}
          >
            <LogOut size={18} />
            Cerrar sesion
          </button>
        </div>
      </aside>
      <section className="workspace">
        <header className="topbar">
          <div>
            <p className="eyebrow">Lanzarote · Ciberseguridad hotelera</p>
            <h1>{navigation.find((n) => n[0] === view)?.[1]}</h1>
          </div>
          <span className={`status-pill status-${online ? 'online' : 'offline'}`}>
            {online ? 'API conectada' : 'API sin conexion'}
          </span>
        </header>
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        {busy && (
          <p role="status" className="notice">
            Procesando...
          </p>
        )}
        {view === 'analysis' && (
          <AssessmentForm
            formState={form}
            isAnalyzing={busy}
            error={null}
            onFieldChange={updateField}
            onSubmit={(e) => {
              e.preventDefault()
              analyze()
            }}
          >
            <fieldset>
              <legend>Contexto del alojamiento</legend>
              <div className="form-grid">
                <label>
                  Temporada alta
                  <input
                    maxLength={80}
                    value={context.season}
                    onChange={(e) => setContext({ ...context, season: e.target.value })}
                  />
                </label>
                <label>
                  Respuesta IT (horas)
                  <input
                    type="number"
                    min={0}
                    max={720}
                    value={context.response}
                    onChange={(e) =>
                      setContext({ ...context, response: Number(e.target.value) })
                    }
                  />
                </label>
                <label>
                  Sistemas (separados por comas)
                  <input
                    maxLength={1200}
                    value={context.inventory}
                    onChange={(e) =>
                      setContext({ ...context, inventory: e.target.value })
                    }
                  />
                </label>
                <label>
                  Categorias de datos
                  <input
                    maxLength={1000}
                    value={context.categories}
                    onChange={(e) =>
                      setContext({ ...context, categories: e.target.value })
                    }
                  />
                </label>
                <label>
                  Conservacion prevista (dias)
                  <input
                    min={0}
                    max={36500}
                    type="number"
                    value={context.retention}
                    onChange={(e) =>
                      setContext({ ...context, retention: Number(e.target.value) })
                    }
                  />
                </label>
              </div>
            </fieldset>
            <fieldset>
              <legend>Gobierno y continuidad</legend>
              <div className="form-grid">
                {Object.entries(extraControls).map(([key, label]) => (
                  <label key={key}>
                    {label}
                    <select
                      value={extra[key] === null ? '' : String(extra[key])}
                      onChange={(e) =>
                        setExtra({
                          ...extra,
                          [key]: e.target.value === '' ? null : e.target.value === 'true',
                        })
                      }
                    >
                      <option value="">Sin confirmar</option>
                      <option value="true">Si</option>
                      <option value="false">No</option>
                    </select>
                  </label>
                ))}
              </div>
            </fieldset>
            <label className="text-field">
              Contexto adicional
              <textarea
                aria-label="Contexto adicional"
                rows={6}
                maxLength={6000}
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
              <small>{description.length}/6000</small>
            </label>
            <label className="inline-check">
              <input
                type="checkbox"
                checked={useAi}
                onChange={(e) => setUseAi(e.target.checked)}
              />
              Autorizar el envio del perfil y el contexto a OpenAI para personalizar
              politicas y resumen
            </label>
            <p className="notice">
              No incluyas datos personales de huespedes, documentos ni pagos. Los
              resultados son orientativos y requieren revision humana. Sin IA se aplican
              reglas locales.
            </p>
          </AssessmentForm>
        )}
        {view === 'dashboard' && (
          <>
            <div className="toolbar">
              <strong>{record?.assessment.business_name ?? 'Mis alojamientos'}</strong>
              <button className="primary-button" disabled={busy} onClick={newAnalysis}>
                <Plus size={18} />
                Nuevo analisis
              </button>
            </div>
            <div className="metric-grid">
              {[
                ['Madurez', record ? `${record.assessment.overall_score}/100` : '-'],
                ['Riesgos', record?.assessment.risks.length ?? '-'],
                [
                  'Acciones completadas',
                  record ? `${completed}/${record.actions.length}` : '-',
                ],
                ['Analisis guardados', total],
              ].map(([label, value]) => (
                <article className="metric-card" key={label}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </article>
              ))}
            </div>
            {previous && record && (
              <p className="notice">
                Variacion respecto al {date(previous.created_at)}:{' '}
                <strong>
                  {record.assessment.overall_score - previous.overall_score > 0
                    ? '+'
                    : ''}
                  {record.assessment.overall_score - previous.overall_score} puntos
                </strong>
                . Comparacion de las declaraciones, no de una auditoria tecnica.
              </p>
            )}
            {record ? (
              <>
                <AiSummaryPanel aiSummary={record.ai_summary} isLoading={false} />
                <AssessmentResults assessment={record.assessment} />
                <p className="notice">{record.disclaimer}</p>
              </>
            ) : (
              <section className="empty-state">
                <h2>Aun no hay un analisis seleccionado</h2>
                <p>Crea uno o abre un resultado del historial.</p>
                {history.slice(0, 5).map((h) => (
                  <button
                    className="history-shortcut"
                    key={h.id}
                    disabled={busy}
                    onClick={() => run(() => open(h.id))}
                  >
                    {h.business_name}
                    <span>
                      {h.overall_score}/100 · {date(h.created_at)}
                    </span>
                  </button>
                ))}
              </section>
            )}
          </>
        )}
        {view === 'history' && (
          <>
            <div className="toolbar">
              <label>
                Alojamiento
                <select
                  value={filter}
                  onChange={(e) => {
                    setFilter(e.target.value)
                    setOffset(0)
                  }}
                >
                  <option value="">Todos</option>
                  {Array.from(
                    new Map(
                      history.map((h) => [h.company_id, h.business_name]),
                    ).entries(),
                  ).map(([id, name]) => (
                    <option key={id} value={id}>
                      {name}
                    </option>
                  ))}
                  {filter && !history.some((h) => h.company_id === filter) && (
                    <option value={filter}>Seleccionado</option>
                  )}
                </select>
              </label>
              <span>{total} analisis</span>
            </div>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Alojamiento</th>
                    <th>Fecha</th>
                    <th>Madurez</th>
                    <th>Riesgo</th>
                    <th>Pendientes</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((h) => (
                    <tr key={h.id}>
                      <td>{h.business_name}</td>
                      <td>{date(h.created_at)}</td>
                      <td>{h.overall_score}/100</td>
                      <td>
                        <span className={`severity severity-${h.risk_level}`}>
                          {riskLabels[h.risk_level]}
                        </span>
                      </td>
                      <td>{h.pending_actions}</td>
                      <td>
                        <div className="icon-actions">
                          <button
                            title="Abrir analisis"
                            aria-label={`Abrir ${h.business_name}`}
                            disabled={busy}
                            onClick={() => run(() => open(h.id))}
                          >
                            <Eye size={18} />
                          </button>
                          <button
                            title="Descargar PDF"
                            aria-label="Descargar PDF"
                            disabled={busy}
                            onClick={() => run(() => downloadReport(h.id))}
                          >
                            <Download size={18} />
                          </button>
                          <button
                            title="Borrar analisis"
                            aria-label="Borrar analisis"
                            disabled={busy}
                            onClick={() => setDeleting(h.id)}
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {!history.length && <p className="empty-state">No hay analisis guardados.</p>}
            <div className="toolbar">
              <button
                title="Pagina anterior"
                aria-label="Pagina anterior"
                disabled={!offset || busy}
                onClick={() => setOffset(Math.max(0, offset - 20))}
              >
                <ArrowLeft size={18} />
              </button>
              <span>
                {total
                  ? `${offset + 1}-${Math.min(offset + 20, total)} de ${total}`
                  : '0 resultados'}
              </span>
              <button
                title="Pagina siguiente"
                aria-label="Pagina siguiente"
                disabled={offset + 20 >= total || busy}
                onClick={() => setOffset(offset + 20)}
              >
                <ArrowRight size={18} />
              </button>
            </div>
          </>
        )}
        {['policies', 'actions', 'report'].includes(view) && !record && (
          <p className="empty-state">Selecciona un analisis en el historial.</p>
        )}
        {view === 'policies' && record && (
          <>
            <p className="notice">
              {record.policy_pack.business_name} ·{' '}
              {record.ai_summary.generated_by_ai
                ? 'Personalizacion IA disponible'
                : 'Generacion por reglas'}
            </p>
            <PolicyPackPanel policyPack={record.policy_pack} />
          </>
        )}
        {view === 'actions' && record && (
          <>
            <div className="toolbar">
              <strong>{record.assessment.business_name}</strong>
              <span>
                {completed} de {record.actions.length} completadas
              </span>
            </div>
            <div className="action-list">
              {record.actions.map((a) => (
                <article className="action-row" key={a.id}>
                  <div>
                    <span className={`severity severity-${a.priority}`}>
                      {a.deadline_days === 0 ? 'Inmediato' : `${a.deadline_days} dias`}
                    </span>
                    <h3>{a.title}</h3>
                    <p>
                      {a.risk} · Dificultad {a.difficulty} · {a.responsible}
                    </p>
                  </div>
                  <select
                    aria-label={`Estado de ${a.risk}`}
                    disabled={busy}
                    value={a.status}
                    onChange={(e) => {
                      const status = e.target.value as Action['status']
                      run(async () => {
                        setRecord(
                          await request(
                            `/records/${record.id}/actions/${a.id}`,
                            'PATCH',
                            { status },
                          ),
                        )
                        await refresh()
                      })
                    }}
                  >
                    <option value="pending">Pendiente</option>
                    <option value="in_progress">En curso</option>
                    <option value="done">Completada</option>
                  </select>
                </article>
              ))}
            </div>
          </>
        )}
        {view === 'report' && record && (
          <section className="report-section">
            <h2>{record.assessment.business_name}</h2>
            <p>
              {date(record.created_at)} · {record.scoring_version} ·{' '}
              {record.prompt_version}
            </p>
            <button
              className="primary-button"
              disabled={busy}
              onClick={() => run(() => downloadReport(record.id))}
            >
              <Download size={18} />
              Descargar informe PDF
            </button>
            <h2>Referencias de seguridad</h2>
            {record.regulatory.map((s) => (
              <div className="source-row" key={s.url}>
                <a href={s.url} target="_blank" rel="noopener noreferrer">
                  {s.name}
                </a>
                <p>{s.topic}</p>
              </div>
            ))}
            <p className="notice">{record.disclaimer}</p>
            <button
              className="secondary-button"
              disabled={busy}
              onClick={() => {
                loadForm(record)
                setView('analysis')
              }}
            >
              Reevaluar alojamiento
            </button>
          </section>
        )}
        {view === 'account' && (
          <section className="account-section">
            <h2>{user.name}</h2>
            <p>
              {user.email} · Rol: {user.role}
            </p>
            <h2>Actividad reciente</h2>
            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>Fecha</th>
                    <th>Evento</th>
                  </tr>
                </thead>
                <tbody>
                  {audit.map((a, i) => (
                    <tr key={i}>
                      <td>{date(a.created_at)}</td>
                      <td>{a.event}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <h2 className="danger-text">Borrar cuenta</h2>
            <p>
              Esta operacion elimina tus alojamientos, analisis, sesiones y registros de
              actividad. No se puede deshacer.
            </p>
            <label className="text-field">
              Confirma tu contrasena
              <input
                type="password"
                autoComplete="current-password"
                value={accountPassword}
                onChange={(e) => setAccountPassword(e.target.value)}
              />
            </label>
            <button
              className="danger-button"
              disabled={!accountPassword || busy}
              onClick={() => setDeleting('account')}
            >
              <Trash2 size={18} />
              Borrar mi cuenta
            </button>
          </section>
        )}
      </section>
      {conflicts.length > 0 && (
        <div className="modal-backdrop">
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="conflict-title"
          >
            <h2 id="conflict-title">Datos contradictorios</h2>
            <p>El texto y los controles seleccionados no coinciden.</p>
            <ul>
              {conflicts.map((c, i) => (
                <li key={i}>
                  {c.field}: formulario {String(c.manual)}, texto {String(c.text)}
                </li>
              ))}
            </ul>
            <div className="toolbar">
              <button
                disabled={busy}
                className="primary-button"
                onClick={() => analyze('manual')}
              >
                Conservar formulario
              </button>
              <button
                disabled={busy}
                className="secondary-button"
                onClick={() => analyze('text')}
              >
                Usar texto
              </button>
              <button disabled={busy} onClick={() => setConflicts([])}>
                Cancelar
              </button>
            </div>
          </section>
        </div>
      )}
      {deleting && (
        <div className="modal-backdrop">
          <section
            className="modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="delete-title"
          >
            <h2 id="delete-title">Confirmar borrado</h2>
            <p>
              {deleting === 'account'
                ? 'Se eliminara toda tu cuenta y sus datos.'
                : 'Se eliminara este analisis y su informe.'}
            </p>
            {error && (
              <p role="alert" className="form-error">
                {error}
              </p>
            )}
            <div className="toolbar">
              <button
                disabled={busy}
                className="danger-button"
                onClick={() =>
                  run(async () => {
                    if (deleting === 'account') {
                      await request('/auth/account', 'DELETE', {
                        password: accountPassword,
                      })
                      setUser(null)
                      setRecord(null)
                      setAccountPassword('')
                    } else {
                      await request(`/records/${deleting}`, 'DELETE')
                      if (record?.id === deleting) setRecord(null)
                      await refresh()
                    }
                    setDeleting(null)
                  })
                }
              >
                Borrar definitivamente
              </button>
              <button disabled={busy} onClick={() => setDeleting(null)}>
                Cancelar
              </button>
            </div>
          </section>
        </div>
      )}
    </main>
  )
}
export default App
