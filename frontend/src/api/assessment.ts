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
  }
  security_controls: {
    uses_mfa: boolean
    uses_password_manager: boolean
    shared_accounts: boolean
    backup_frequency: BackupFrequency
    backups_tested: boolean
    has_antivirus: boolean
    systems_updated: boolean
    guest_wifi_separated: boolean
    has_incident_response_plan: boolean
    has_rgpd_breach_protocol: boolean
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
