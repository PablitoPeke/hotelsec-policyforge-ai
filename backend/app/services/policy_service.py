from app.schemas.assessment import AssessmentRequest, RiskLevel
from app.schemas.policy import GeneratedPolicy, PolicyControl, PolicyPackResponse
from app.services.assessment_service import analyze_assessment


def generate_policy_pack(payload: AssessmentRequest) -> PolicyPackResponse:
    assessment = analyze_assessment(payload)
    profile = payload.hotel_profile
    controls = payload.security_controls

    policies = [
        _password_policy(controls.uses_mfa, controls.uses_password_manager),
        _backup_policy(controls.backup_frequency, controls.backups_tested),
        _device_policy(controls.systems_updated, controls.has_antivirus),
        _network_policy(
            profile.offers_guest_wifi,
            controls.guest_wifi_separated,
            profile.handles_card_payments,
            controls.payment_terminal_isolated,
            controls.cctv_or_iot_devices,
            controls.iot_network_separated,
        ),
        _incident_policy(
            controls.has_incident_response_plan,
            controls.has_rgpd_breach_protocol,
            controls.rgpd_processing_register,
        ),
        _supplier_policy(
            controls.supplier_remote_access,
            controls.supplier_access_controlled,
        ),
    ]

    return PolicyPackResponse(
        business_name=profile.business_name,
        municipality=profile.municipality,
        overall_score=assessment.overall_score,
        risk_level=assessment.risk_level,
        policies=policies,
        implementation_order=_build_implementation_order(assessment.risk_level),
    )


def _control(title: str, description: str, priority: RiskLevel) -> PolicyControl:
    return PolicyControl(title=title, description=description, priority=priority)


def _password_policy(uses_mfa: bool, uses_password_manager: bool) -> GeneratedPolicy:
    controls = [
        _control(
            "Usuarios individuales",
            "Cada empleado debe usar una cuenta propia para correo, PMS, reservas y herramientas internas.",
            "high",
        ),
        _control(
            "Contraseñas robustas",
            "Las contraseñas deben tener longitud suficiente, no reutilizarse y cambiarse si existe sospecha de filtración.",
            "medium",
        ),
    ]

    if not uses_mfa:
        controls.append(
            _control(
                "Doble factor obligatorio",
                "Activar MFA en correo, PMS, paneles de reservas, administración y cuentas de proveedores.",
                "high",
            )
        )

    if not uses_password_manager:
        controls.append(
            _control(
                "Gestor de contraseñas",
                "Implantar un gestor de contraseñas para evitar documentos compartidos o claves apuntadas en papel.",
                "medium",
            )
        )

    return GeneratedPolicy(
        name="Política de contraseñas y accesos",
        objective="Reducir accesos no autorizados a sistemas críticos del alojamiento.",
        scope="Personal interno, dirección, recepción, administración y proveedores con acceso a sistemas.",
        controls=controls,
        evidence=[
            "Listado de usuarios activos por sistema.",
            "Capturas o exportación de MFA activado.",
            "Registro de altas, bajas y cambios de permisos.",
        ],
        review_frequency="Trimestral o cuando cambie personal/proveedores.",
    )


def _backup_policy(frequency: str, backups_tested: bool) -> GeneratedPolicy:
    priority: RiskLevel = "critical" if frequency == "none" else "medium"
    controls = [
        _control(
            "Copias automáticas",
            "Configurar copias de seguridad de reservas, facturación, documentación y ficheros operativos.",
            priority,
        ),
        _control(
            "Copia aislada",
            "Mantener al menos una copia separada del sistema principal para reducir impacto de ransomware.",
            "high",
        ),
    ]

    if frequency in {"none", "monthly"}:
        controls.append(
            _control(
                "Mejorar frecuencia",
                "Pasar a copias semanales como mínimo, y diarias para información de reservas y facturación.",
                "high",
            )
        )

    if not backups_tested:
        controls.append(
            _control(
                "Pruebas de restauración",
                "Realizar pruebas documentadas para comprobar que los datos pueden recuperarse.",
                "medium",
            )
        )

    return GeneratedPolicy(
        name="Política de copias de seguridad",
        objective="Garantizar recuperación ante ransomware, fallo técnico o borrado accidental.",
        scope="PMS, channel manager, facturación, documentos de huéspedes y ficheros de gestión.",
        controls=controls,
        evidence=[
            "Plan de copias.",
            "Registro de ejecuciones.",
            "Actas de prueba de restauración.",
        ],
        review_frequency="Mensual, con prueba de restauración al menos trimestral.",
    )


def _device_policy(systems_updated: bool, has_antivirus: bool) -> GeneratedPolicy:
    controls = [
        _control(
            "Inventario de equipos",
            "Mantener un listado de ordenadores, móviles, tablets, TPV y equipos usados por el alojamiento.",
            "medium",
        ),
        _control(
            "Bloqueo de pantalla",
            "Activar bloqueo automático en equipos de recepción y administración.",
            "medium",
        ),
    ]

    if not has_antivirus:
        controls.append(
            _control(
                "Antivirus o EDR",
                "Instalar protección antimalware en equipos que acceden a correo, reservas y documentación.",
                "high",
            )
        )

    if not systems_updated:
        controls.append(
            _control(
                "Actualizaciones",
                "Aplicar actualizaciones de sistema operativo, navegador y aplicaciones críticas.",
                "high",
            )
        )

    return GeneratedPolicy(
        name="Política de uso de dispositivos",
        objective="Proteger equipos que tratan datos de clientes y operación del hotel.",
        scope="Equipos corporativos, dispositivos de recepción, administración, TPV y dispositivos móviles.",
        controls=controls,
        evidence=[
            "Inventario de activos.",
            "Registro de actualizaciones.",
            "Estado de protección antivirus/EDR.",
        ],
        review_frequency="Mensual.",
    )


def _network_policy(
    offers_guest_wifi: bool,
    guest_wifi_separated: bool,
    handles_card_payments: bool,
    payment_terminal_isolated: bool,
    cctv_or_iot_devices: bool,
    iot_network_separated: bool,
) -> GeneratedPolicy:
    controls = [
        _control(
            "Red interna protegida",
            "Limitar la red interna a equipos necesarios para la gestión del alojamiento.",
            "medium",
        )
    ]

    if offers_guest_wifi and not guest_wifi_separated:
        controls.append(
            _control(
                "Separación de WiFi de huéspedes",
                "Separar la WiFi de clientes de la red interna mediante VLAN o red independiente.",
                "high",
            )
        )

    if handles_card_payments and not payment_terminal_isolated:
        controls.append(
            _control(
                "Aislamiento de TPV",
                "Mantener terminales de pago y equipos relacionados en segmento restringido.",
                "high",
            )
        )

    if cctv_or_iot_devices and not iot_network_separated:
        controls.append(
            _control(
                "Red separada para IoT/CCTV",
                "Separar cámaras, cerraduras inteligentes y domótica de los equipos administrativos.",
                "medium",
            )
        )

    return GeneratedPolicy(
        name="Política de red, WiFi e IoT",
        objective="Reducir exposición entre clientes, dispositivos inteligentes y sistemas internos.",
        scope="Red interna, WiFi de huéspedes, TPV, CCTV, cerraduras inteligentes y domótica.",
        controls=controls,
        evidence=[
            "Diagrama simple de red.",
            "Configuración de WiFi/VLAN.",
            "Listado de dispositivos IoT/CCTV.",
        ],
        review_frequency="Semestral o al instalar nuevos dispositivos.",
    )


def _incident_policy(
    has_incident_response_plan: bool,
    has_rgpd_breach_protocol: bool,
    rgpd_processing_register: bool,
) -> GeneratedPolicy:
    controls = [
        _control(
            "Canal de aviso interno",
            "Definir a quién avisar ante phishing, pérdida de dispositivo, ransomware o fuga de datos.",
            "high",
        )
    ]

    if not has_incident_response_plan:
        controls.append(
            _control(
                "Plan de respuesta",
                "Documentar pasos básicos: contener, avisar, preservar evidencias, recuperar y aprender.",
                "high",
            )
        )

    if not has_rgpd_breach_protocol:
        controls.append(
            _control(
                "Protocolo de brechas RGPD",
                "Evaluar impacto, documentar hechos y preparar notificación si aplica.",
                "medium",
            )
        )

    if not rgpd_processing_register:
        controls.append(
            _control(
                "Registro de tratamientos",
                "Documentar datos tratados, finalidad, base legal, conservación y encargados.",
                "medium",
            )
        )

    return GeneratedPolicy(
        name="Política de respuesta a incidentes y RGPD",
        objective="Responder de forma ordenada ante incidentes técnicos o brechas de datos personales.",
        scope="Dirección, recepción, administración, soporte IT y proveedores críticos.",
        controls=controls,
        evidence=[
            "Plan de respuesta a incidentes.",
            "Registro de incidentes.",
            "Registro RGPD de tratamientos y brechas.",
        ],
        review_frequency="Semestral y después de cada incidente.",
    )


def _supplier_policy(
    supplier_remote_access: bool,
    supplier_access_controlled: bool,
) -> GeneratedPolicy:
    controls = [
        _control(
            "Listado de proveedores",
            "Mantener una lista de proveedores con acceso a sistemas, datos o soporte técnico.",
            "medium",
        )
    ]

    if supplier_remote_access and not supplier_access_controlled:
        controls.append(
            _control(
                "Control de acceso remoto",
                "Limitar accesos remotos por usuario, horario, MFA y registro de actividad.",
                "high",
            )
        )

    return GeneratedPolicy(
        name="Política de proveedores y accesos remotos",
        objective="Controlar accesos externos a sistemas del alojamiento.",
        scope="Proveedores de PMS, channel manager, mantenimiento, soporte IT, marketing y sistemas de pago.",
        controls=controls,
        evidence=[
            "Listado de proveedores autorizados.",
            "Contratos o acuerdos de tratamiento de datos.",
            "Registro de accesos remotos.",
        ],
        review_frequency="Trimestral y al cambiar de proveedor.",
    )


def _build_implementation_order(risk_level: RiskLevel) -> list[str]:
    first_steps = [
        "Activar MFA y eliminar cuentas compartidas en sistemas críticos.",
        "Asegurar copias de seguridad y probar restauración.",
        "Separar WiFi de huéspedes, TPV e IoT/CCTV cuando aplique.",
    ]

    if risk_level in {"critical", "high"}:
        return [
            *first_steps,
            "Crear plan de respuesta a incidentes y protocolo RGPD.",
            "Revisar accesos remotos de proveedores.",
        ]

    return [
        "Revisar evidencias de controles ya implantados.",
        "Formalizar políticas internas y calendario de revisión.",
        "Preparar formación básica para el personal.",
    ]
