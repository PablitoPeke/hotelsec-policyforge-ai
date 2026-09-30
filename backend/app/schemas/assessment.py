from typing import Literal, Annotated

from pydantic import BaseModel, Field, ConfigDict


RiskLevel = Literal["low", "medium", "high", "critical"]


class HotelProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
    high_season: str = Field(default="Todo el ano", max_length=80)
    technology_inventory: list[Annotated[str, Field(min_length=1, max_length=120)]] = Field(default_factory=list, max_length=20)
    personal_data_categories: list[Annotated[str, Field(min_length=1, max_length=120)]] = Field(default_factory=list, max_length=12)
    retention_days: int = Field(default=180, ge=0, le=36500)
    it_response_hours: int = Field(default=24, ge=0, le=720)


class SecurityControls(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
    password_policy: bool | None = None
    firewall_enabled: bool | None = None
    supplier_contracts: bool | None = None
    data_retention_defined: bool | None = None
    byod_policy: bool | None = None
    remote_work_policy: bool | None = None
    secure_messaging: bool | None = None
    business_continuity_plan: bool | None = None
    manual_checkin_procedure: bool | None = None
    incident_responsible_assigned: bool | None = None
    temporary_staff_onboarding: bool | None = None
    can_operate_offline: bool | None = None


class AssessmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
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
    probability: int = Field(default=3, ge=1, le=5)
    impact: int = Field(default=3, ge=1, le=5)
    rationale: str = "Estimacion orientativa por reglas; no es una medicion de incidentes."


class AssessmentResponse(BaseModel):
    business_name: str
    overall_score: int = Field(ge=0, le=100)
    risk_level: RiskLevel
    area_scores: list[AreaScore]
    risks: list[RiskFinding]
    next_steps: list[str]
