export type HealthStatus = {
  status: string
  service: string
  version: string
  environment: string
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function fetchHealthStatus(): Promise<HealthStatus> {
  const response = await fetch(`${API_BASE_URL}/api/v1/health`)

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`)
  }

  return response.json() as Promise<HealthStatus>
}
