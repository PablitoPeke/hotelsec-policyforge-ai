import type { AssessmentResponse, BackupFrequency, BusinessType } from '../api/assessment'
import type { HealthStatus } from '../api/health'

export type ApiConnectionState =
  | { status: 'checking' }
  | { status: 'online'; data: HealthStatus }
  | { status: 'offline'; message: string }

export type FormState = {
  businessName: string
  municipality: string
  businessType: BusinessType
  roomsCount: number
  permanentEmployees: number
  temporaryEmployees: number
  hasExternalItProvider: boolean
  usesMfa: boolean
  usesPasswordManager: boolean
  sharedAccounts: boolean
  backupFrequency: BackupFrequency
  backupsTested: boolean
  hasAntivirus: boolean
  systemsUpdated: boolean
  guestWifiSeparated: boolean
  hasIncidentResponsePlan: boolean
  hasRgpdBreachProtocol: boolean
  staffPhishingTraining: boolean
}

export type AssessmentState = AssessmentResponse | null
