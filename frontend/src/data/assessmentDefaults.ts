import type { RiskLevel } from '../api/assessment'
import type { FormState } from '../types/app'

export const initialFormState: FormState = {
  businessName: 'Hotel Demo Lanzarote',
  municipality: 'Tías',
  businessType: 'hotel',
  roomsCount: 42,
  permanentEmployees: 12,
  temporaryEmployees: 8,
  hasExternalItProvider: true,
  usesPms: true,
  offersGuestWifi: true,
  handlesCardPayments: true,
  storesGuestDocuments: true,
  usesMfa: false,
  usesPasswordManager: false,
  sharedAccounts: true,
  pmsIndividualUsers: false,
  employeeOffboardingProcess: false,
  backupFrequency: 'none',
  backupsTested: false,
  hasAntivirus: true,
  systemsUpdated: false,
  guestWifiSeparated: false,
  paymentTerminalIsolated: false,
  cctvOrIotDevices: true,
  iotNetworkSeparated: false,
  supplierRemoteAccess: true,
  supplierAccessControlled: false,
  hasIncidentResponsePlan: false,
  hasRgpdBreachProtocol: false,
  rgpdProcessingRegister: false,
  staffPhishingTraining: false,
}

export const riskLabels: Record<RiskLevel, string> = {
  low: 'Bajo',
  medium: 'Medio',
  high: 'Alto',
  critical: 'Crítico',
}
