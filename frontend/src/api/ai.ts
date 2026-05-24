import type { AssessmentResponse } from './assessment'
import type { AssessmentRequest, BusinessType } from './assessment'
import type { PolicyPackResponse } from './policies'

export type AiExecutiveSummaryResponse = {
  summary: string
  generated_by_ai: boolean
  provider: string
  model: string | null
}

export type AiDescriptionAnalysisRequest = {
  business_name: string
  municipality: string
  business_type: BusinessType
  rooms_count: number
  permanent_employees: number
  temporary_employees: number
  description: string
}

export type AiDescriptionAnalysisResponse = {
  normalized_assessment: AssessmentRequest
  assessment: AssessmentResponse
  policy_pack: PolicyPackResponse
  ai_summary: AiExecutiveSummaryResponse
  generated_by_ai: boolean
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function generateAiExecutiveSummary(
  assessment: AssessmentResponse,
  policyPack: PolicyPackResponse,
): Promise<AiExecutiveSummaryResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ai/executive-summary`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      assessment,
      policy_pack: policyPack,
    }),
  })

  if (!response.ok) {
    throw new Error(`AI summary failed with status ${response.status}`)
  }

  return response.json() as Promise<AiExecutiveSummaryResponse>
}

export async function analyzeDescriptionWithAi(
  payload: AiDescriptionAnalysisRequest,
): Promise<AiDescriptionAnalysisResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ai/analyze-description`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(`AI description analysis failed with status ${response.status}`)
  }

  return response.json() as Promise<AiDescriptionAnalysisResponse>
}
