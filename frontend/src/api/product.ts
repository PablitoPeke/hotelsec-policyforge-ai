import type { AssessmentRequest, AssessmentResponse } from './assessment'
import type { PolicyPackResponse } from './policies'
import type { AiExecutiveSummaryResponse } from './ai'

export type User = { id: string; name: string; email: string; role: string }
export type Action = {
  id: string
  title: string
  risk: string
  priority: string
  deadline_days: number
  difficulty: string
  responsible: string
  status: 'pending' | 'in_progress' | 'done'
}
export type Conflict = { field: string; manual: unknown; text: unknown }
export type RecordDetail = {
  id: string
  company_id: string
  created_at: string
  input: AssessmentRequest
  description: string
  assessment: AssessmentResponse
  policy_pack: PolicyPackResponse
  ai_summary: AiExecutiveSummaryResponse
  actions: Action[]
  conflicts: Conflict[]
  regulatory: { name: string; url: string; topic: string }[]
  disclaimer: string
  scoring_version: string
  prompt_version: string
}
export type HistoryItem = {
  id: string
  company_id: string
  created_at: string
  business_name: string
  overall_score: number
  risk_level: AssessmentResponse['risk_level']
  risk_count: number
  pending_actions: number
}
export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: unknown,
    message: string,
  ) {
    super(message)
  }
}
const base = (import.meta.env.VITE_API_URL ?? '').replace(/\/$/, '')
let csrf = ''
export async function request<T>(
  path: string,
  method = 'GET',
  body?: unknown,
): Promise<T> {
  let response: Response
  try {
    response = await fetch(`${base}/api/v1${path}`, {
      method,
      credentials: 'include',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': csrf },
      body: body === undefined ? undefined : JSON.stringify(body),
    })
  } catch {
    throw new Error(
      'No se pudo conectar con el servidor. Comprueba la conexion y reintenta.',
    )
  }
  if (!response.ok) {
    const data = await response
      .json()
      .catch(() => ({ detail: 'No se pudo conectar con el servidor.' }))
    const message =
      typeof data.detail === 'string'
        ? data.detail
        : response.status === 422
          ? 'Revisa los campos y sus limites.'
          : (data.detail?.message ?? `Operacion rechazada (${response.status}).`)
    throw new ApiError(response.status, data.detail, message)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}
export async function session(path = '/auth/me', body?: unknown) {
  const data = await request<{ user: User; csrf_token: string }>(
    path,
    body ? 'POST' : 'GET',
    body,
  )
  csrf = data.csrf_token
  return data.user
}
export async function downloadReport(id: string) {
  const response = await fetch(`${base}/api/v1/records/${id}/report.pdf`, {
    credentials: 'include',
  })
  if (!response.ok)
    throw new Error('No se pudo descargar el informe. Comprueba tu sesion.')
  const url = URL.createObjectURL(await response.blob())
  const link = document.createElement('a')
  link.href = url
  link.download = `HotelSec-${id}.pdf`
  link.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}
