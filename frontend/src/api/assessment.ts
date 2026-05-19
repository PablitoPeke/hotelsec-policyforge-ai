export type BusinessType =
  | 'hotel'
  | 'apartahotel'
  | 'villa'
  | 'hostal'
  | 'alquiler_vacacional'
  | 'agencia_turistica'

export type BackupFrequency = 'none' | 'monthly' | 'weekly' | 'daily'

export type RiskLevel = 'low' | 'medium' | 'high' | 'critical'

export type AssessmentRequest = {
  hotel_profile: {
    business_name: string
    municipality: string
    business_type: BusinessType
    rooms_count: number
    permanent_employees: number
    temporary_employees: number
    has_external_it_provider: boolean
    uses_pms: boolean
    offers_guest_wifi: boolean
    handles_card_payments: boolean
    stores_guest_documents: boolean
  }
  security_controls: {
    uses_mfa: boolean
    uses_password_manager: boolean
    shared_accounts: boolean
    pms_individual_users: boolean
    employee_offboarding_process: boolean
    backup_frequency: BackupFrequency
    backups_tested: boolean
    has_antivirus: boolean
    systems_updated: boolean
    guest_wifi_separated: boolean
    payment_terminal_isolated: boolean
    cctv_or_iot_devices: boolean
    iot_network_separated: boolean
    supplier_remote_access: boolean
    supplier_access_controlled: boolean
    has_incident_response_plan: boolean
    has_rgpd_breach_protocol: boolean
    rgpd_processing_register: boolean
    staff_phishing_training: boolean
  }
}

export type AreaScore = {
  area: string
  score: number
}

export type RiskFinding = {
  title: string
  description: string
  severity: RiskLevel
  recommendation: string
}

export type AssessmentResponse = {
  business_name: string
  overall_score: number
  risk_level: RiskLevel
  area_scores: AreaScore[]
  risks: RiskFinding[]
  next_steps: string[]
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function analyzeHotelAssessment(
  payload: AssessmentRequest,
): Promise<AssessmentResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/assessments/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`Assessment failed with status ${response.status}`)
  }

  return response.json() as Promise<AssessmentResponse>
}
