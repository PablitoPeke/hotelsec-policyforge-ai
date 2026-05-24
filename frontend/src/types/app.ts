import type { AssessmentResponse, BackupFrequency, BusinessType } from '../api/assessment'
import type { HealthStatus } from '../api/health'
import type { PolicyPackResponse } from '../api/policies'

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
  usesPms: boolean
  offersGuestWifi: boolean
  handlesCardPayments: boolean
  storesGuestDocuments: boolean
  usesMfa: boolean
  usesPasswordManager: boolean
  sharedAccounts: boolean
  pmsIndividualUsers: boolean
  employeeOffboardingProcess: boolean
  backupFrequency: BackupFrequency
  backupsTested: boolean
  hasAntivirus: boolean
  systemsUpdated: boolean
  guestWifiSeparated: boolean
  paymentTerminalIsolated: boolean
  cctvOrIotDevices: boolean
  iotNetworkSeparated: boolean
  supplierRemoteAccess: boolean
  supplierAccessControlled: boolean
  hasIncidentResponsePlan: boolean
  hasRgpdBreachProtocol: boolean
  rgpdProcessingRegister: boolean
  staffPhishingTraining: boolean
}

export type AssessmentState = AssessmentResponse | null

export type PolicyPackState = PolicyPackResponse | null
