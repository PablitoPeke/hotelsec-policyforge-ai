import type { FormEvent } from 'react'

import type { BackupFrequency, BusinessType } from '../api/assessment'
import type { FormState } from '../types/app'

type AssessmentFormProps = {
  formState: FormState
  isAnalyzing: boolean
  error: string | null
  onSubmit: (event: FormEvent<HTMLFormElement>) => void
  onFieldChange: <K extends keyof FormState>(key: K, value: FormState[K]) => void
}

const checkboxFields: Array<{
  key: keyof Pick<
    FormState,
    | 'hasExternalItProvider'
    | 'usesPms'
    | 'offersGuestWifi'
    | 'handlesCardPayments'
    | 'storesGuestDocuments'
    | 'usesMfa'
    | 'usesPasswordManager'
    | 'sharedAccounts'
    | 'pmsIndividualUsers'
    | 'employeeOffboardingProcess'
    | 'backupsTested'
    | 'hasAntivirus'
    | 'systemsUpdated'
    | 'guestWifiSeparated'
    | 'paymentTerminalIsolated'
    | 'cctvOrIotDevices'
    | 'iotNetworkSeparated'
    | 'supplierRemoteAccess'
    | 'supplierAccessControlled'
    | 'hasIncidentResponsePlan'
    | 'hasRgpdBreachProtocol'
    | 'rgpdProcessingRegister'
    | 'staffPhishingTraining'
  >
  label: string
}> = [
  { key: 'hasExternalItProvider', label: 'Proveedor IT externo' },
  { key: 'usesPms', label: 'Usa PMS o channel manager' },
  { key: 'offersGuestWifi', label: 'Ofrece WiFi a huéspedes' },
  { key: 'handlesCardPayments', label: 'Acepta pagos con tarjeta' },
  { key: 'storesGuestDocuments', label: 'Guarda documentación de huéspedes' },
  { key: 'usesMfa', label: 'Usa doble factor' },
  { key: 'usesPasswordManager', label: 'Usa gestor de contraseñas' },
  { key: 'sharedAccounts', label: 'Comparte cuentas' },
  { key: 'pmsIndividualUsers', label: 'PMS con usuarios individuales' },
  { key: 'employeeOffboardingProcess', label: 'Proceso de baja de empleados' },
  { key: 'backupsTested', label: 'Prueba restauración de backups' },
  { key: 'hasAntivirus', label: 'Tiene antivirus/EDR' },
  { key: 'systemsUpdated', label: 'Sistemas actualizados' },
  { key: 'guestWifiSeparated', label: 'WiFi de huéspedes separada' },
  { key: 'paymentTerminalIsolated', label: 'TPV/red de pagos aislada' },
  { key: 'cctvOrIotDevices', label: 'Usa cámaras, domótica o IoT' },
  { key: 'iotNetworkSeparated', label: 'IoT/CCTV en red separada' },
  { key: 'supplierRemoteAccess', label: 'Proveedores con acceso remoto' },
  { key: 'supplierAccessControlled', label: 'Acceso remoto de proveedores controlado' },
  { key: 'hasIncidentResponsePlan', label: 'Plan de respuesta a incidentes' },
  { key: 'hasRgpdBreachProtocol', label: 'Protocolo de brechas RGPD' },
  { key: 'rgpdProcessingRegister', label: 'Registro RGPD de tratamientos' },
  { key: 'staffPhishingTraining', label: 'Formación contra phishing' },
]

export function AssessmentForm({
  formState,
  isAnalyzing,
  error,
  onSubmit,
  onFieldChange,
}: AssessmentFormProps) {
  return (
    <article className="panel" id="analisis">
      <div className="panel-header">
        <div>
          <p className="eyebrow">Formulario inicial</p>
          <h2>Analizador de hoteles</h2>
        </div>
        <code>POST /api/v1/assessments/analyze</code>
      </div>

      <form className="assessment-form" onSubmit={onSubmit}>
        <div className="form-grid">
          <label>
            Nombre del alojamiento
            <input
              value={formState.businessName}
              onChange={(event) => onFieldChange('businessName', event.target.value)}
            />
          </label>
          <label>
            Municipio
            <input
              value={formState.municipality}
              onChange={(event) => onFieldChange('municipality', event.target.value)}
            />
          </label>
          <label>
            Tipo
            <select
              value={formState.businessType}
              onChange={(event) =>
                onFieldChange('businessType', event.target.value as BusinessType)
              }
            >
              <option value="hotel">Hotel</option>
              <option value="apartahotel">Apartahotel</option>
              <option value="villa">Villa</option>
              <option value="hostal">Hostal</option>
              <option value="alquiler_vacacional">Alquiler vacacional</option>
              <option value="agencia_turistica">Agencia turística</option>
            </select>
          </label>
          <label>
            Habitaciones
            <input
              min="1"
              type="number"
              value={formState.roomsCount}
              onChange={(event) => onFieldChange('roomsCount', Number(event.target.value))}
            />
          </label>
          <label>
            Empleados fijos
            <input
              min="0"
              type="number"
              value={formState.permanentEmployees}
              onChange={(event) =>
                onFieldChange('permanentEmployees', Number(event.target.value))
              }
            />
          </label>
          <label>
            Empleados temporales
            <input
              min="0"
              type="number"
              value={formState.temporaryEmployees}
              onChange={(event) =>
                onFieldChange('temporaryEmployees', Number(event.target.value))
              }
            />
          </label>
          <label>
            Frecuencia de backups
            <select
              value={formState.backupFrequency}
              onChange={(event) =>
                onFieldChange('backupFrequency', event.target.value as BackupFrequency)
              }
            >
              <option value="none">No se realizan</option>
              <option value="monthly">Mensual</option>
              <option value="weekly">Semanal</option>
              <option value="daily">Diaria</option>
            </select>
          </label>
        </div>

        <div className="checkbox-grid">
          {checkboxFields.map((field) => (
            <label key={field.key}>
              <input
                type="checkbox"
                checked={Boolean(formState[field.key])}
                onChange={(event) => onFieldChange(field.key, event.target.checked)}
              />
              {field.label}
            </label>
          ))}
        </div>

        <button className="primary-button" disabled={isAnalyzing} type="submit">
          {isAnalyzing ? 'Analizando...' : 'Analizar hotel'}
        </button>
        {error ? <p className="form-error">{error}</p> : null}
      </form>
    </article>
  )
}
