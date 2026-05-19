from app.schemas.assessment import (
    AreaScore,
    AssessmentRequest,
    AssessmentResponse,
    HotelProfile,
    RiskFinding,
    RiskLevel,
    SecurityControls,
)


def analyze_assessment(payload: AssessmentRequest) -> AssessmentResponse:
    controls = payload.security_controls
    profile = payload.hotel_profile
    area_scores = _calculate_area_scores(profile, controls)
    overall_score = round(sum(area.score for area in area_scores) / len(area_scores))
    risks = _detect_risks(profile, controls)

    return AssessmentResponse(
        business_name=payload.hotel_profile.business_name,
        overall_score=overall_score,
        risk_level=_calculate_risk_level(overall_score, risks),
        area_scores=area_scores,
        risks=risks,
        next_steps=_build_next_steps(risks),
    )


def _calculate_area_scores(
    profile: HotelProfile, controls: SecurityControls
) -> list[AreaScore]:
    backup_score = 0
    if controls.backup_frequency == "daily":
        backup_score += 70
    elif controls.backup_frequency == "weekly":
        backup_score += 55
    elif controls.backup_frequency == "monthly":
        backup_score += 30
    if controls.backups_tested:
        backup_score += 30

    return [
        AreaScore(
            area="Identidad y accesos",
            score=_score_booleans(
                [
                    controls.uses_mfa,
                    controls.uses_password_manager,
                    not controls.shared_accounts,
                    controls.employee_offboarding_process,
                    *(
                        [controls.pms_individual_users]
                        if profile.uses_pms
                        else []
                    ),
                ]
            ),
        ),
        AreaScore(area="Copias de seguridad", score=min(backup_score, 100)),
        AreaScore(
            area="Protección de dispositivos",
            score=_score_booleans([controls.has_antivirus, controls.systems_updated]),
        ),
        AreaScore(
            area="Seguridad de red y sistemas hoteleros",
            score=_score_booleans(
                [
                    *(
                        [controls.guest_wifi_separated]
                        if profile.offers_guest_wifi
                        else []
                    ),
                    *(
                        [controls.payment_terminal_isolated]
                        if profile.handles_card_payments
                        else []
                    ),
                    *(
                        [controls.iot_network_separated]
                        if controls.cctv_or_iot_devices
                        else []
                    ),
                ],
            ),
        ),
        AreaScore(
            area="Proveedores y accesos remotos",
            score=_score_booleans(
                [
                    (
                        controls.supplier_access_controlled
                        if controls.supplier_remote_access
                        else True
                    )
                ]
            ),
        ),
        AreaScore(
            area="Respuesta a incidentes",
            score=_score_booleans(
                [
                    controls.has_incident_response_plan,
                    controls.has_rgpd_breach_protocol,
                    *(
                        [controls.rgpd_processing_register]
                        if profile.stores_guest_documents
                        else []
                    ),
                ]
            ),
        ),
        AreaScore(
            area="Concienciación del personal",
            score=100 if controls.staff_phishing_training else 20,
        ),
    ]


def _score_booleans(values: list[bool]) -> int:
    if not values:
        return 100

    return round((sum(1 for value in values if value) / len(values)) * 100)


def _detect_risks(profile: HotelProfile, controls: SecurityControls) -> list[RiskFinding]:
    risks: list[RiskFinding] = []

    if not controls.uses_mfa:
        risks.append(
            RiskFinding(
                title="Falta de doble factor de autenticación",
                description=(
                    "Las cuentas críticas del hotel podrían quedar expuestas si una "
                    "contraseña se filtra o se reutiliza en otro servicio."
                ),
                severity="high",
                recommendation="Activar MFA en correo, PMS, paneles de reservas y cuentas administrativas.",
            )
        )

    if controls.shared_accounts:
        risks.append(
            RiskFinding(
                title="Uso de cuentas compartidas",
                description=(
                    "Compartir usuarios impide saber quién realizó una acción y dificulta "
                    "revocar accesos cuando cambia el personal."
                ),
                severity="high",
                recommendation="Crear usuarios individuales para recepción, administración y proveedores.",
            )
        )

    if profile.uses_pms and not controls.pms_individual_users:
        risks.append(
            RiskFinding(
                title="PMS sin usuarios individuales",
                description=(
                    "El sistema de gestión hotelera concentra reservas, datos de clientes "
                    "y facturación. Si se usa con cuentas genéricas, se pierde trazabilidad."
                ),
                severity="high",
                recommendation="Configurar usuarios individuales y perfiles por rol en el PMS.",
            )
        )

    if not controls.employee_offboarding_process:
        risks.append(
            RiskFinding(
                title="Baja de empleados sin proceso de retirada de accesos",
                description=(
                    "En negocios con personal temporal, un acceso olvidado puede seguir "
                    "activo después de finalizar la relación laboral."
                ),
                severity="medium",
                recommendation="Crear una lista de baja para correo, PMS, llaves digitales y aplicaciones internas.",
            )
        )

    if controls.backup_frequency == "none":
        risks.append(
            RiskFinding(
                title="Ausencia de copias de seguridad",
                description=(
                    "Un incidente de ransomware, borrado accidental o fallo técnico podría "
                    "provocar pérdida de reservas, facturación o documentación de clientes."
                ),
                severity="critical",
                recommendation="Implantar copias de seguridad automáticas y mantener al menos una copia aislada.",
            )
        )
    elif not controls.backups_tested:
        risks.append(
            RiskFinding(
                title="Copias de seguridad no verificadas",
                description=(
                    "Tener backups no garantiza la recuperación si nunca se ha probado que "
                    "pueden restaurarse correctamente."
                ),
                severity="medium",
                recommendation="Programar pruebas de restauración periódicas y documentar el resultado.",
            )
        )

    if profile.offers_guest_wifi and not controls.guest_wifi_separated:
        risks.append(
            RiskFinding(
                title="WiFi de huéspedes no separada",
                description=(
                    "Los dispositivos de clientes podrían compartir red con sistemas internos "
                    "del hotel, aumentando la superficie de ataque."
                ),
                severity="high",
                recommendation="Separar la red de huéspedes de la red interna mediante VLAN o red independiente.",
            )
        )

    if profile.handles_card_payments and not controls.payment_terminal_isolated:
        risks.append(
            RiskFinding(
                title="Terminales de pago no aislados",
                description=(
                    "Los TPV y sistemas de pago deben estar separados de redes de clientes "
                    "y de equipos no necesarios para reducir el riesgo sobre datos de pago."
                ),
                severity="high",
                recommendation="Separar TPV y equipos de pago en una red propia o segmento restringido.",
            )
        )

    if controls.cctv_or_iot_devices and not controls.iot_network_separated:
        risks.append(
            RiskFinding(
                title="Cámaras o dispositivos IoT en la red principal",
                description=(
                    "Cámaras, cerraduras inteligentes o domótica pueden tener vulnerabilidades "
                    "y conviene aislarlos de recepción, administración y sistemas críticos."
                ),
                severity="medium",
                recommendation="Crear una red separada para CCTV, cerraduras, domótica y otros dispositivos IoT.",
            )
        )

    if controls.supplier_remote_access and not controls.supplier_access_controlled:
        risks.append(
            RiskFinding(
                title="Acceso remoto de proveedores sin control suficiente",
                description=(
                    "Los proveedores de PMS, mantenimiento o soporte pueden convertirse en "
                    "una vía de entrada si sus accesos no se revisan ni se limitan."
                ),
                severity="high",
                recommendation="Limitar accesos remotos por proveedor, horario, MFA y registro de actividad.",
            )
        )

    if not controls.has_rgpd_breach_protocol:
        risks.append(
            RiskFinding(
                title="No existe protocolo de brechas RGPD",
                description=(
                    "Ante una fuga de datos personales, el hotel podría no reaccionar dentro "
                    "de los plazos y obligaciones exigidos por el RGPD."
                ),
                severity="medium",
                recommendation="Definir un procedimiento de detección, evaluación y notificación de brechas.",
            )
        )

    if profile.stores_guest_documents and not controls.rgpd_processing_register:
        risks.append(
            RiskFinding(
                title="Registro RGPD de tratamientos incompleto",
                description=(
                    "Los alojamientos suelen tratar documentos de identidad, reservas y datos "
                    "de contacto. Sin registro, es más difícil demostrar cumplimiento."
                ),
                severity="medium",
                recommendation="Documentar tratamientos, finalidades, bases legales, plazos de conservación y encargados.",
            )
        )

    if not controls.staff_phishing_training:
        risks.append(
            RiskFinding(
                title="Falta de formación frente a phishing",
                description=(
                    "El personal de recepción y administración es un objetivo habitual para "
                    "correos fraudulentos relacionados con reservas, pagos o proveedores."
                ),
                severity="medium",
                recommendation="Realizar formación básica y simulaciones periódicas de phishing.",
            )
        )

    return risks


def _calculate_risk_level(score: int, risks: list[RiskFinding]) -> RiskLevel:
    if any(risk.severity == "critical" for risk in risks) or score < 35:
        return "critical"
    if any(risk.severity == "high" for risk in risks) or score < 60:
        return "high"
    if any(risk.severity == "medium" for risk in risks) or score < 80:
        return "medium"
    return "low"


def _build_next_steps(risks: list[RiskFinding]) -> list[str]:
    if not risks:
        return [
            "Mantener revisiones periódicas de controles de seguridad.",
            "Actualizar políticas internas cuando cambien sistemas o proveedores.",
        ]

    return [risk.recommendation for risk in risks[:5]]
