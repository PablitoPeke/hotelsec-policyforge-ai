import type { AssessmentResponse } from './assessment'
import type { PolicyPackResponse } from './policies'

export type AiExecutiveSummaryResponse = {
  summary: string
  generated_by_ai: boolean
  provider: string
  model: string | null
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
