import { useEffect, useState, type FormEvent, type KeyboardEvent } from 'react'
import {
  CheckCircle2,
  Download,
  KeyRound,
  LogOut,
  Mail,
  Monitor,
  RefreshCw,
  Save,
  ShieldCheck,
  Smartphone,
  Trash2,
  UserRound,
  X,
} from 'lucide-react'
import {
  ApiError,
  downloadAccountData,
  request,
  session,
  type AccountCapabilities,
  type AccountSession,
  type AuditEntry,
  type User,
} from '../api/product'
import { PasswordInput } from './PasswordInput'

const tabs = [
  ['profile', 'Perfil', UserRound],
  ['security', 'Seguridad', ShieldCheck],
  ['activity', 'Actividad', RefreshCw],
  ['data', 'Mis datos', Download],
] as const
type Tab = (typeof tabs)[number][0]
const eventLabels: Record<string, string> = {
  'session.created': 'Inicio de sesion',
  'session.revoked': 'Sesion cerrada',
  'sessions.others_revoked': 'Otras sesiones cerradas',
  'profile.updated': 'Perfil actualizado',
  'password.changed': 'Contrasena cambiada',
  'password.recovered': 'Contrasena recuperada',
  'password.recovery_requested': 'Recuperacion solicitada',
  'email.verification_requested': 'Verificacion solicitada',
  'email.verified': 'Correo verificado',
  'email.change_requested': 'Cambio de correo solicitado',
  'email.changed': 'Correo actualizado',
  'record.created': 'Analisis creado',
  'record.deleted': 'Analisis eliminado',
  'record.access_denied': 'Acceso a analisis denegado',
  'action.updated': 'Plan de mejora actualizado',
  'report.downloaded': 'Informe descargado',
  'account.exported': 'Datos exportados',
  'role.admin_granted': 'Permiso de administracion concedido',
}
const formatDate = (value: string | null) =>
  value
    ? new Date(/[Zz]$|[+-]\d\d:\d\d$/.test(value) ? value : value + 'Z').toLocaleString(
        'es-ES',
      )
    : 'Sesion anterior'
const profileOf = (user: User) => ({
  name: user.name,
  organization_name: user.organization_name,
  job_title: user.job_title,
})

async function fetchAccount() {
  const [sessions, activity, capabilities] = await Promise.all([
    request<AccountSession[]>('/auth/sessions'),
    request<AuditEntry[]>('/auth/audit'),
    request<AccountCapabilities>('/auth/capabilities'),
  ])
  return { sessions, activity, capabilities }
}

export function AccountPanel({
  user,
  onUserChange,
  onBusyChange,
  onSessionExpired,
  onDelete,
}: {
  user: User
  onUserChange: (user: User) => void
  onBusyChange: (value: boolean) => void
  onSessionExpired: () => void
  onDelete: (password: string) => void
}) {
  const [tab, setTab] = useState<Tab>('profile')
  const [profile, setProfile] = useState(profileOf(user))
  const [data, setData] = useState<Awaited<ReturnType<typeof fetchAccount>> | null>(null)
  const [loading, setLoading] = useState(true)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')
  const [password, setPassword] = useState({ current: '', next: '', confirmation: '' })
  const [sessionPassword, setSessionPassword] = useState('')
  const [exportPassword, setExportPassword] = useState('')
  const [deletePassword, setDeletePassword] = useState('')
  const [deleteConfirmation, setDeleteConfirmation] = useState('')
  const [changingEmail, setChangingEmail] = useState(false)
  const [email, setEmail] = useState({ next: '', password: '' })
  const dirty = Object.entries(profile).some(
    ([key, value]) => value !== user[key as keyof typeof profile],
  )
  const emailAvailable = data?.capabilities.email_delivery_configured ?? false

  useEffect(() => {
    setProfile(profileOf(user))
  }, [user.name, user.organization_name, user.job_title])
  useEffect(() => {
    let active = true
    setLoading(true)
    fetchAccount()
      .then((result) => {
        if (active) setData(result)
      })
      .catch((exception) => {
        if (!active) return
        setError(
          exception instanceof Error ? exception.message : 'No se pudo cargar la cuenta.',
        )
        if (exception instanceof ApiError && exception.status === 401) onSessionExpired()
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [user.id])

  async function perform(operation: () => Promise<void>) {
    setBusy(true)
    onBusyChange(true)
    setError('')
    setNotice('')
    try {
      await operation()
    } catch (exception) {
      setError(
        exception instanceof Error
          ? exception.message
          : 'No se pudo completar la operacion.',
      )
      if (exception instanceof ApiError && exception.status === 401) onSessionExpired()
    } finally {
      setBusy(false)
      onBusyChange(false)
    }
  }
  function selectTab(next: Tab) {
    setTab(next)
    setError('')
    setNotice('')
  }
  function tabKey(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const movement = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0
    if (!movement && event.key !== 'Home' && event.key !== 'End') return
    event.preventDefault()
    const next =
      event.key === 'Home'
        ? 0
        : event.key === 'End'
          ? tabs.length - 1
          : (index + movement + tabs.length) % tabs.length
    selectTab(tabs[next][0])
    document.getElementById(`account-tab-${tabs[next][0]}`)?.focus()
  }
  function saveProfile(event: FormEvent) {
    event.preventDefault()
    perform(async () => {
      const saved = await request<User>('/auth/profile', 'PATCH', profile)
      onUserChange(saved)
      setProfile(profileOf(saved))
      setNotice('Datos guardados correctamente.')
    })
  }
  function changePassword(event: FormEvent) {
    event.preventDefault()
    if (password.next !== password.confirmation) {
      setError('Las nuevas contrasenas no coinciden.')
      return
    }
    perform(async () => {
      const updated = await session('/auth/password', {
        current_password: password.current,
        new_password: password.next,
      })
      onUserChange(updated)
      setPassword({ current: '', next: '', confirmation: '' })
      setData(await fetchAccount())
      setNotice('Contrasena actualizada. Las sesiones anteriores se han cerrado.')
    })
  }

  return (
    <section className="account-center" aria-label="Configuracion de mi cuenta">
      <header className="account-summary">
        <span className="account-avatar" aria-hidden="true">
          {user.name
            .trim()
            .split(/\s+/)
            .slice(0, 2)
            .map((word) => word[0])
            .join('')
            .toUpperCase()}
        </span>
        <div className="account-identity">
          <h2>{user.name}</h2>
          <p>{user.email}</p>
          <div className="account-metadata">
            <span>
              {user.role === 'admin' ? 'Administrador' : 'Cuenta de alojamiento'}
            </span>
            <span
              className={user.email_verified ? 'account-verified' : 'account-unverified'}
            >
              {user.email_verified ? <ShieldCheck size={14} /> : <Mail size={14} />}
              {user.email_verified ? 'Correo verificado' : 'Correo sin verificar'}
            </span>
          </div>
        </div>
      </header>
      <nav className="account-tabs" role="tablist" aria-label="Configuracion de cuenta">
        {tabs.map(([id, label, Icon], index) => (
          <button
            key={id}
            id={`account-tab-${id}`}
            type="button"
            role="tab"
            aria-selected={tab === id}
            aria-controls={`account-panel-${id}`}
            tabIndex={tab === id ? 0 : -1}
            disabled={busy}
            onClick={() => selectTab(id)}
            onKeyDown={(event) => tabKey(event, index)}
          >
            <Icon size={17} />
            {label}
          </button>
        ))}
      </nav>
      {error && (
        <p role="alert" className="form-error">
          {error}
        </p>
      )}
      {notice && (
        <p role="status" className="account-success">
          <CheckCircle2 size={18} />
          {notice}
        </p>
      )}
      {loading && (
        <p role="status" className="account-muted">
          Cargando cuenta...
        </p>
      )}
      {!loading && !data && (
        <button
          type="button"
          onClick={() =>
            perform(async () => {
              setData(await fetchAccount())
            })
          }
        >
          <RefreshCw size={17} />
          Reintentar
        </button>
      )}
      <div
        id={`account-panel-${tab}`}
        role="tabpanel"
        aria-labelledby={`account-tab-${tab}`}
      >
        {tab === 'profile' && (
          <>
            <section className="account-block">
              <div className="account-block-heading">
                <h3>Datos personales</h3>
                <span className="account-muted">
                  Miembro desde {formatDate(user.created_at).split(',')[0]}
                </span>
              </div>
              <form onSubmit={saveProfile} className="account-form">
                <div className="form-grid">
                  <label className="text-field">
                    Nombre y apellidos
                    <input
                      autoComplete="name"
                      required
                      minLength={2}
                      maxLength={120}
                      disabled={busy}
                      value={profile.name}
                      onChange={(event) =>
                        setProfile({ ...profile, name: event.target.value })
                      }
                    />
                  </label>
                  <label className="text-field">
                    Organizacion
                    <input
                      autoComplete="organization"
                      maxLength={120}
                      disabled={busy}
                      value={profile.organization_name}
                      onChange={(event) =>
                        setProfile({ ...profile, organization_name: event.target.value })
                      }
                    />
                  </label>
                  <label className="text-field">
                    Cargo
                    <input
                      autoComplete="organization-title"
                      maxLength={120}
                      disabled={busy}
                      value={profile.job_title}
                      onChange={(event) =>
                        setProfile({ ...profile, job_title: event.target.value })
                      }
                    />
                  </label>
                  <label className="text-field">
                    Correo de acceso
                    <input
                      type="email"
                      autoComplete="email"
                      value={user.email}
                      readOnly
                    />
                  </label>
                </div>
                <div className="account-form-actions">
                  <button
                    type="submit"
                    className="primary-button"
                    disabled={!dirty || busy}
                  >
                    <Save size={17} />
                    Guardar cambios
                  </button>
                  <button
                    type="button"
                    disabled={!dirty || busy}
                    onClick={() => setProfile(profileOf(user))}
                  >
                    <X size={17} />
                    Cancelar
                  </button>
                </div>
              </form>
            </section>
            <section className="account-block">
              <div className="account-block-heading">
                <h3>Correo electronico</h3>
                <span className="account-muted">
                  {emailAvailable
                    ? 'Verificacion por enlace'
                    : loading
                      ? 'Comprobando disponibilidad'
                      : 'Servicio de correo sin configurar'}
                </span>
              </div>
              <div className="account-form-actions">
                {!user.email_verified && (
                  <button
                    type="button"
                    disabled={!emailAvailable || busy}
                    title={
                      emailAvailable
                        ? 'Enviar enlace de verificacion'
                        : 'Pendiente de configurar un proveedor de correo'
                    }
                    onClick={() =>
                      perform(async () => {
                        const result = await request<{ message: string }>(
                          '/auth/email/verify',
                          'POST',
                        )
                        setNotice(result.message)
                      })
                    }
                  >
                    <ShieldCheck size={17} />
                    Verificar correo
                  </button>
                )}
                <button
                  type="button"
                  disabled={!emailAvailable || busy}
                  title={
                    emailAvailable
                      ? 'Solicitar cambio de correo'
                      : 'Pendiente de configurar un proveedor de correo'
                  }
                  onClick={() => setChangingEmail(!changingEmail)}
                >
                  <Mail size={17} />
                  Cambiar correo
                </button>
              </div>
              {changingEmail && emailAvailable && (
                <form
                  className="account-form account-subform"
                  onSubmit={(event) => {
                    event.preventDefault()
                    perform(async () => {
                      const result = await request<{ message: string }>(
                        '/auth/email/change',
                        'POST',
                        { new_email: email.next, current_password: email.password },
                      )
                      setEmail({ next: '', password: '' })
                      setChangingEmail(false)
                      setNotice(result.message)
                    })
                  }}
                >
                  <div className="form-grid">
                    <label className="text-field">
                      Nuevo correo
                      <input
                        type="email"
                        required
                        maxLength={254}
                        autoComplete="email"
                        disabled={busy}
                        value={email.next}
                        onChange={(event) =>
                          setEmail({ ...email, next: event.target.value })
                        }
                      />
                    </label>
                    <PasswordInput
                      label="Contrasena para cambiar el correo"
                      disabled={busy}
                      value={email.password}
                      onChange={(value) => setEmail({ ...email, password: value })}
                    />
                  </div>
                  <button className="primary-button" disabled={busy}>
                    <Mail size={17} />
                    Solicitar confirmacion
                  </button>
                </form>
              )}
            </section>
          </>
        )}
        {tab === 'security' && (
          <>
            <section className="account-block">
              <div className="account-block-heading">
                <h3>Cambiar contrasena</h3>
                <KeyRound size={20} />
              </div>
              <form onSubmit={changePassword} className="account-form">
                <div className="form-grid">
                  <PasswordInput
                    label="Contrasena actual"
                    value={password.current}
                    disabled={busy}
                    onChange={(value) => setPassword({ ...password, current: value })}
                  />
                  <PasswordInput
                    label="Nueva contrasena"
                    newPassword
                    value={password.next}
                    disabled={busy}
                    onChange={(value) => setPassword({ ...password, next: value })}
                  />
                  <PasswordInput
                    label="Repetir nueva contrasena"
                    newPassword
                    value={password.confirmation}
                    disabled={busy}
                    onChange={(value) =>
                      setPassword({ ...password, confirmation: value })
                    }
                  />
                </div>
                <button
                  className="primary-button"
                  disabled={
                    busy || !password.current || !password.next || !password.confirmation
                  }
                >
                  <KeyRound size={17} />
                  Actualizar contrasena
                </button>
              </form>
            </section>
            <section className="account-block">
              <div className="account-block-heading">
                <h3>Sesiones activas</h3>
                <button
                  className="icon-button"
                  type="button"
                  disabled={busy}
                  title="Actualizar sesiones"
                  aria-label="Actualizar sesiones"
                  onClick={() =>
                    perform(async () => {
                      setData(await fetchAccount())
                    })
                  }
                >
                  <RefreshCw size={17} />
                </button>
              </div>
              <div className="account-session-list">
                {data?.sessions.map((item) => (
                  <div className="account-session" key={item.id}>
                    {/Android|iOS|iPadOS/.test(item.device) ? (
                      <Smartphone size={22} />
                    ) : (
                      <Monitor size={22} />
                    )}
                    <div>
                      <strong>{item.device}</strong>
                      <span>{formatDate(item.created_at)}</span>
                      <small>Caduca: {formatDate(item.expires_at)}</small>
                    </div>
                    {item.current ? (
                      <span className="account-current-session">Actual</span>
                    ) : (
                      <button
                        type="button"
                        className="icon-button"
                        title="Cerrar esta sesion"
                        aria-label={`Cerrar sesion de ${item.device}`}
                        disabled={busy}
                        onClick={() =>
                          perform(async () => {
                            await request(`/auth/sessions/${item.id}`, 'DELETE')
                            setData(await fetchAccount())
                            setNotice('Sesion cerrada.')
                          })
                        }
                      >
                        <LogOut size={17} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
              {data && data.sessions.length > 1 && (
                <form
                  className="account-form account-subform"
                  onSubmit={(event) => {
                    event.preventDefault()
                    perform(async () => {
                      await request('/auth/sessions/revoke-others', 'POST', {
                        current_password: sessionPassword,
                      })
                      setSessionPassword('')
                      setData(await fetchAccount())
                      setNotice('Las otras sesiones se han cerrado.')
                    })
                  }}
                >
                  <PasswordInput
                    label="Contrasena para cerrar otras sesiones"
                    value={sessionPassword}
                    disabled={busy}
                    onChange={setSessionPassword}
                  />
                  <button disabled={busy || !sessionPassword}>
                    <LogOut size={17} />
                    Cerrar otras sesiones
                  </button>
                </form>
              )}
            </section>
          </>
        )}
        {tab === 'activity' && (
          <section className="account-block">
            <div className="account-block-heading">
              <h3>Actividad reciente</h3>
              <span className="account-muted">{data?.activity.length ?? 0} eventos</span>
            </div>
            {data?.activity.length ? (
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Fecha</th>
                      <th>Actividad</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.activity.map((item, index) => (
                      <tr key={`${item.created_at}-${index}`}>
                        <td>
                          <time>{formatDate(item.created_at)}</time>
                        </td>
                        <td title={item.event}>
                          {eventLabels[item.event] ?? 'Evento registrado'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              !loading && <p className="account-muted">Sin actividad registrada.</p>
            )}
          </section>
        )}
        {tab === 'data' && (
          <>
            <section className="account-block">
              <div className="account-block-heading">
                <h3>Copia de mis datos</h3>
                <span className="account-muted">JSON</span>
              </div>
              <form
                className="account-form"
                onSubmit={(event) => {
                  event.preventDefault()
                  perform(async () => {
                    await downloadAccountData(exportPassword)
                    setExportPassword('')
                    setData(await fetchAccount())
                    setNotice('Descarga de datos preparada.')
                  })
                }}
              >
                <PasswordInput
                  label="Contrasena para exportar"
                  value={exportPassword}
                  disabled={busy}
                  onChange={setExportPassword}
                />
                <button disabled={busy || !exportPassword}>
                  <Download size={17} />
                  Descargar mis datos
                </button>
              </form>
            </section>
            <section className="account-block account-danger">
              <div className="account-block-heading">
                <h3>Eliminar cuenta</h3>
                <Trash2 size={20} />
              </div>
              <p>
                Los datos guardados se eliminaran de la aplicacion. Esta accion no se
                puede deshacer.
              </p>
              <form
                className="account-form"
                onSubmit={(event) => {
                  event.preventDefault()
                  if (deleteConfirmation === 'ELIMINAR') onDelete(deletePassword)
                }}
              >
                <div className="form-grid">
                  <PasswordInput
                    label="Contrasena para eliminar la cuenta"
                    value={deletePassword}
                    disabled={busy}
                    onChange={setDeletePassword}
                  />
                  <label className="text-field">
                    Confirmacion: ELIMINAR
                    <input
                      autoComplete="off"
                      value={deleteConfirmation}
                      disabled={busy}
                      onChange={(event) => setDeleteConfirmation(event.target.value)}
                      required
                    />
                  </label>
                </div>
                <button
                  className="danger-button"
                  disabled={busy || !deletePassword || deleteConfirmation !== 'ELIMINAR'}
                >
                  <Trash2 size={17} />
                  Eliminar mi cuenta
                </button>
              </form>
            </section>
          </>
        )}
      </div>
    </section>
  )
}
