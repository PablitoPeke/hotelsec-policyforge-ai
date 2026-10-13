import { useId, useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'

export function PasswordInput({
  label,
  value,
  onChange,
  newPassword = false,
  disabled = false,
}: {
  label: string
  value: string
  onChange: (value: string) => void
  newPassword?: boolean
  disabled?: boolean
}) {
  const id = useId()
  const [visible, setVisible] = useState(false)
  return (
    <label className="text-field" htmlFor={id}>
      {label}
      <span className="password-field">
        <input
          id={id}
          aria-label={label}
          type={visible ? 'text' : 'password'}
          value={value}
          onChange={(event) => onChange(event.target.value)}
          required
          disabled={disabled}
          minLength={newPassword ? 12 : 1}
          maxLength={128}
          autoComplete={newPassword ? 'new-password' : 'current-password'}
        />
        <button
          type="button"
          disabled={disabled}
          onClick={() => setVisible(!visible)}
          aria-pressed={visible}
          aria-label={`${visible ? 'Ocultar' : 'Mostrar'} ${label.toLowerCase()}`}
          title={visible ? 'Ocultar contrasena' : 'Mostrar contrasena'}
        >
          {visible ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>
      </span>
    </label>
  )
}
