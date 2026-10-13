import { useEffect, useState, type FormEvent } from 'react'
import { ArrowLeft, CheckCircle2, KeyRound, Mail } from 'lucide-react'
import { request, type AccountCapabilities } from '../api/product'
import { BrandLogo } from './BrandLogo'
import { PasswordInput } from './PasswordInput'

export type AccountLink = { token: string; purpose: string }
export function readAccountLink(): AccountLink | null {
  const values = new URLSearchParams(window.location.hash.slice(1))
  const token = values.get('account_token')
  return token
    ? { token: token.slice(0, 256), purpose: values.get('purpose') ?? '' }
    : null
}

export function RecoveryForm({ onBack }: { onBack: () => void }) {
  const [email, setEmail] = useState('')
  const [available, setAvailable] = useState<boolean | null>(null)
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  useEffect(() => {
    let active = true
    request<AccountCapabilities>('/auth/capabilities')
      .then((value) => {
        if (active) setAvailable(value.email_delivery_configured)
      })
      .catch(() => {
        if (active) setError('No se pudo consultar el servicio de correo.')
      })
    return () => {
      active = false
    }
  }, [])
  async function submit(event: FormEvent) {
    event.preventDefault()
    setBusy(true)
    setError('')
    try {
      const result = await request<{ message: string }>(
        '/auth/password/reset/request',
        'POST',
        { email },
      )
      setMessage(result.message)
    } catch (exception) {
      setError(
        exception instanceof Error
          ? exception.message
          : 'No se pudo solicitar la recuperacion.',
      )
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
            <p>Recuperar acceso</p>
          </div>
        </div>
        {available === false && (
          <p className="notice">La recuperacion por correo no esta disponible.</p>
        )}
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        {available === null && !error && (
          <p role="status" className="notice">
            Consultando servicio de correo...
          </p>
        )}
        {message ? (
          <p role="status" className="account-success">
            <CheckCircle2 size={18} />
            {message}
          </p>
        ) : (
          <form className="fields" onSubmit={submit}>
            <label>
              Correo electronico
              <input
                type="email"
                autoComplete="email"
                maxLength={254}
                required
                disabled={busy || !available}
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </label>
            <button className="primary-button" disabled={busy || !available}>
              <Mail size={17} />
              Solicitar enlace
            </button>
          </form>
        )}
        <button className="auth-back" type="button" disabled={busy} onClick={onBack}>
          <ArrowLeft size={17} />
          Volver al acceso
        </button>
      </section>
    </main>
  )
}

export function AccountLinkForm({
  link,
  onClose,
}: {
  link: AccountLink
  onClose: () => void
}) {
  const reset = link.purpose === 'reset_password'
  const [password, setPassword] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  async function submit(event: FormEvent) {
    event.preventDefault()
    if (reset && password !== confirmation) {
      setError('Las contrasenas no coinciden.')
      return
    }
    setBusy(true)
    setError('')
    try {
      const result = await request<{ message: string }>(
        '/auth/account-token/confirm',
        'POST',
        { token: link.token, ...(reset ? { new_password: password } : {}) },
      )
      setPassword('')
      setConfirmation('')
      setMessage(result.message)
    } catch (exception) {
      setError(
        exception instanceof Error
          ? exception.message
          : 'No se pudo confirmar el enlace.',
      )
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
            <p>{reset ? 'Restablecer contrasena' : 'Confirmar correo'}</p>
          </div>
        </div>
        {error && (
          <p role="alert" className="form-error">
            {error}
          </p>
        )}
        {message ? (
          <p role="status" className="account-success">
            <CheckCircle2 size={18} />
            {message}
          </p>
        ) : (
          <form className="fields" onSubmit={submit}>
            {reset && (
              <>
                <PasswordInput
                  label="Nueva contrasena"
                  value={password}
                  onChange={setPassword}
                  newPassword
                  disabled={busy}
                />
                <PasswordInput
                  label="Repetir nueva contrasena"
                  value={confirmation}
                  onChange={setConfirmation}
                  newPassword
                  disabled={busy}
                />
              </>
            )}
            <button className="primary-button" disabled={busy}>
              {reset ? <KeyRound size={17} /> : <Mail size={17} />}
              {reset ? 'Restablecer contrasena' : 'Confirmar correo'}
            </button>
          </form>
        )}
        <button className="auth-back" type="button" disabled={busy} onClick={onClose}>
          <ArrowLeft size={17} />
          Volver a HotelSec
        </button>
      </section>
    </main>
  )
}
