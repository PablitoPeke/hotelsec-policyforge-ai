import type { AssessmentRequest, RiskLevel } from './assessment'

export type PolicyControl = {
  title: string
  description: string
  priority: RiskLevel
}

export type GeneratedPolicy = {
  name: string
  objective: string
  scope: string
  controls: PolicyControl[]
  evidence: string[]
  review_frequency: string
}

export type PolicyPackResponse = {
  business_name: string
  municipality: string
  overall_score: number
  risk_level: RiskLevel
  policies: GeneratedPolicy[]
  implementation_order: string[]
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function generatePolicyPack(
  assessment: AssessmentRequest,
): Promise<PolicyPackResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/policies/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ assessment }),
  })

  if (!response.ok) {
    throw new Error(`Policy generation failed with status ${response.status}`)
  }

  return response.json() as Promise<PolicyPackResponse>
}
