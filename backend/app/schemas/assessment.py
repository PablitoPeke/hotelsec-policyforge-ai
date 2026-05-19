from typing import Literal

from pydantic import BaseModel, Field


RiskLevel = Literal["low", "medium", "high", "critical"]


class HotelProfile(BaseModel):
    business_name: str = Field(min_length=2, max_length=120)
    municipality: str = Field(min_length=2, max_length=80)
    business_type: Literal[
        "hotel",
        "apartahotel",
        "villa",
        "hostal",
        "alquiler_vacacional",
        "agencia_turistica",
    ]
    rooms_count: int = Field(ge=1, le=1000)
    permanent_employees: int = Field(ge=0, le=500)
    temporary_employees: int = Field(ge=0, le=500)
    has_external_it_provider: bool
    uses_pms: bool
    offers_guest_wifi: bool
    handles_card_payments: bool
    stores_guest_documents: bool


class SecurityControls(BaseModel):
    uses_mfa: bool
    uses_password_manager: bool
    shared_accounts: bool
    pms_individual_users: bool
    employee_offboarding_process: bool
    backup_frequency: Literal["none", "monthly", "weekly", "daily"]
    backups_tested: bool
    has_antivirus: bool
    systems_updated: bool
    guest_wifi_separated: bool
    payment_terminal_isolated: bool
    cctv_or_iot_devices: bool
    iot_network_separated: bool
    supplier_remote_access: bool
    supplier_access_controlled: bool
    has_incident_response_plan: bool
    has_rgpd_breach_protocol: bool
    rgpd_processing_register: bool
    staff_phishing_training: bool


class AssessmentRequest(BaseModel):
    hotel_profile: HotelProfile
    security_controls: SecurityControls


class AreaScore(BaseModel):
    area: str
    score: int = Field(ge=0, le=100)


class RiskFinding(BaseModel):
    title: str
    description: str
    severity: RiskLevel
    recommendation: str


class AssessmentResponse(BaseModel):
    business_name: str
    overall_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    area_scores: list[AreaScore]
    risks: list[RiskFinding]
    next_steps: list[str]
