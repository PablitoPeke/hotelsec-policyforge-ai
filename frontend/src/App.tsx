import { useEffect, useState, type FormEvent } from 'react'

import {
  analyzeHotelAssessment,
  type AssessmentRequest,
  type AssessmentResponse,
} from './api/assessment'
import { fetchHealthStatus } from './api/health'
import { AssessmentForm } from './components/AssessmentForm'
import { AssessmentResults } from './components/AssessmentResults'
import { DashboardMetrics } from './components/DashboardMetrics'
import { Sidebar } from './components/Sidebar'
import { StatusPill } from './components/StatusPill'
import { initialFormState } from './data/assessmentDefaults'
import type { ApiConnectionState, FormState } from './types/app'

function App() {
  const [apiConnection, setApiConnection] = useState<ApiConnectionState>({
    status: 'checking',
  })
  const [formState, setFormState] = useState<FormState>(initialFormState)
  const [assessment, setAssessment] = useState<AssessmentResponse | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [assessmentError, setAssessmentError] = useState<string | null>(null)

  useEffect(() => {
    let ignore = false

    fetchHealthStatus()
      .then((data) => {
        if (!ignore) {
          setApiConnection({ status: 'online', data })
        }
      })
      .catch((error: unknown) => {
        if (!ignore) {
          setApiConnection({
            status: 'offline',
            message: error instanceof Error ? error.message : 'No se pudo conectar con la API',
          })
        }
      })

    return () => {
      ignore = true
    }
  }, [])

  function updateField<K extends keyof FormState>(key: K, value: FormState[K]) {
    setFormState((current) => ({
      ...current,
      [key]: value,
    }))
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsAnalyzing(true)
    setAssessmentError(null)

    const payload: AssessmentRequest = {
      hotel_profile: {
        business_name: formState.businessName,
        municipality: formState.municipality,
        business_type: formState.businessType,
        rooms_count: formState.roomsCount,
        permanent_employees: formState.permanentEmployees,
        temporary_employees: formState.temporaryEmployees,
        has_external_it_provider: formState.hasExternalItProvider,
        uses_pms: formState.usesPms,
        offers_guest_wifi: formState.offersGuestWifi,
        handles_card_payments: formState.handlesCardPayments,
        stores_guest_documents: formState.storesGuestDocuments,
      },
      security_controls: {
        uses_mfa: formState.usesMfa,
        uses_password_manager: formState.usesPasswordManager,
        shared_accounts: formState.sharedAccounts,
        pms_individual_users: formState.pmsIndividualUsers,
        employee_offboarding_process: formState.employeeOffboardingProcess,
        backup_frequency: formState.backupFrequency,
        backups_tested: formState.backupsTested,
        has_antivirus: formState.hasAntivirus,
        systems_updated: formState.systemsUpdated,
        guest_wifi_separated: formState.guestWifiSeparated,
        payment_terminal_isolated: formState.paymentTerminalIsolated,
        cctv_or_iot_devices: formState.cctvOrIotDevices,
        iot_network_separated: formState.iotNetworkSeparated,
        supplier_remote_access: formState.supplierRemoteAccess,
        supplier_access_controlled: formState.supplierAccessControlled,
        has_incident_response_plan: formState.hasIncidentResponsePlan,
        has_rgpd_breach_protocol: formState.hasRgpdBreachProtocol,
        rgpd_processing_register: formState.rgpdProcessingRegister,
        staff_phishing_training: formState.staffPhishingTraining,
      },
    }

    try {
      const result = await analyzeHotelAssessment(payload)
      setAssessment(result)
    } catch (error) {
      setAssessmentError(
        error instanceof Error ? error.message : 'No se pudo completar el análisis',
      )
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="workspace" id="dashboard">
        <header className="topbar">
          <div>
            <p className="eyebrow">MVP Práctica 1</p>
            <h1>Panel inicial de madurez hotelera</h1>
          </div>
          <StatusPill connection={apiConnection} />
        </header>

        <DashboardMetrics apiConnection={apiConnection} assessment={assessment} />

        <section className="content-grid content-grid-wide">
          <AssessmentForm
            error={assessmentError}
            formState={formState}
            isAnalyzing={isAnalyzing}
            onFieldChange={updateField}
            onSubmit={handleSubmit}
          />
          <AssessmentResults assessment={assessment} />
        </section>
      </section>
    </main>
  )
}

export default App
