import { useEffect, useState, type FormEvent } from 'react'

import {
  analyzeHotelAssessment,
  type AssessmentRequest,
  type AssessmentResponse,
} from './api/assessment'
import {
  analyzeDescriptionWithAi,
  generateAiExecutiveSummary,
  type AiExecutiveSummaryResponse,
} from './api/ai'
import { fetchHealthStatus } from './api/health'
import { generatePolicyPack, type PolicyPackResponse } from './api/policies'
import { AiSummaryPanel } from './components/AiSummaryPanel'
import { AssessmentForm } from './components/AssessmentForm'
import { AssessmentResults } from './components/AssessmentResults'
import { DashboardMetrics } from './components/DashboardMetrics'
import { DescriptionAnalysisPanel } from './components/DescriptionAnalysisPanel'
import { ExecutiveReportPanel } from './components/ExecutiveReportPanel'
import { HeroPanel } from './components/HeroPanel'
import { PolicyPackPanel } from './components/PolicyPackPanel'
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
  const [policyPack, setPolicyPack] = useState<PolicyPackResponse | null>(null)
  const [aiSummary, setAiSummary] = useState<AiExecutiveSummaryResponse | null>(null)
  const [freeTextDescription, setFreeTextDescription] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [isAnalyzingDescription, setIsAnalyzingDescription] = useState(false)
  const [isGeneratingAiSummary, setIsGeneratingAiSummary] = useState(false)
  const [assessmentError, setAssessmentError] = useState<string | null>(null)
  const [descriptionError, setDescriptionError] = useState<string | null>(null)

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
    setPolicyPack(null)
    setAiSummary(null)

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
      const [result, generatedPolicies] = await Promise.all([
        analyzeHotelAssessment(payload),
        generatePolicyPack(payload),
      ])
      setAssessment(result)
      setPolicyPack(generatedPolicies)
      setIsGeneratingAiSummary(true)
      const generatedSummary = await generateAiExecutiveSummary(result, generatedPolicies)
      setAiSummary(generatedSummary)
    } catch (error) {
      setAssessmentError(
        error instanceof Error ? error.message : 'No se pudo completar el análisis',
      )
    } finally {
      setIsAnalyzing(false)
      setIsGeneratingAiSummary(false)
    }
  }

  async function handleDescriptionSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsAnalyzingDescription(true)
    setDescriptionError(null)
    setAssessmentError(null)
    setAssessment(null)
    setPolicyPack(null)
    setAiSummary(null)

    try {
      const result = await analyzeDescriptionWithAi({
        business_name: formState.businessName,
        municipality: formState.municipality,
        business_type: formState.businessType,
        rooms_count: formState.roomsCount,
        permanent_employees: formState.permanentEmployees,
        temporary_employees: formState.temporaryEmployees,
        description: freeTextDescription,
      })
      setAssessment(result.assessment)
      setPolicyPack(result.policy_pack)
      setAiSummary(result.ai_summary)
    } catch (error) {
      setDescriptionError(
        error instanceof Error ? error.message : 'No se pudo analizar la descripción',
      )
    } finally {
      setIsAnalyzingDescription(false)
    }
  }

  return (
    <main className="app-shell">
      <Sidebar />

      <section className="workspace" id="dashboard">
        <header className="topbar">
          <span>HotelSec PolicyForge AI</span>
          <StatusPill connection={apiConnection} />
        </header>

        <HeroPanel
          apiConnection={apiConnection}
          assessment={assessment}
          policyPack={policyPack}
        />

        <DashboardMetrics
          apiConnection={apiConnection}
          assessment={assessment}
          policyPack={policyPack}
        />

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

        <DescriptionAnalysisPanel
          description={freeTextDescription}
          error={descriptionError}
          isAnalyzing={isAnalyzingDescription}
          onDescriptionChange={setFreeTextDescription}
          onSubmit={handleDescriptionSubmit}
        />

        <PolicyPackPanel policyPack={policyPack} />
        <AiSummaryPanel aiSummary={aiSummary} isLoading={isGeneratingAiSummary} />
        <ExecutiveReportPanel assessment={assessment} policyPack={policyPack} />
      </section>
    </main>
  )
}

export default App
