from __future__ import annotations

import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "HotelSec_PolicyForge_AI_propuesta_proyecto.pdf"


def clean(text: str) -> str:
    replacements = {
        "Practica": "Práctica",
        "practica": "práctica",
        "Presentacion": "Presentación",
        "presentacion": "presentación",
        "Justificacion": "Justificación",
        "justificacion": "justificación",
        "Linea": "Línea",
        "linea": "línea",
        "situacion": "situación",
        "Situacion": "Situación",
        "diagnostico": "diagnóstico",
        "Diagnostico": "Diagnóstico",
        "Descripcion": "Descripción",
        "descripcion": "descripción",
        "Funcionamiento": "Funcionamiento",
        "Analizador": "Analizador",
        "analizador": "analizador",
        "politicas": "políticas",
        "Politicas": "Políticas",
        "Politica": "Política",
        "politica": "política",
        "turistico": "turístico",
        "turistica": "turística",
        "turisticos": "turísticos",
        "turisticas": "turísticas",
        "pequenas": "pequeñas",
        "Pequenas": "Pequeñas",
        "contrasenas": "contraseñas",
        "Contrasenas": "Contraseñas",
        "informacion": "información",
        "Informacion": "Información",
        "solucion": "solución",
        "Solucion": "Solución",
        "gestion": "gestión",
        "Gestion": "Gestión",
        "cumplimiento": "cumplimiento",
        "normativa": "normativa",
        "automaticamente": "automáticamente",
        "Automaticamente": "Automáticamente",
        "tecnologicos": "tecnológicos",
        "Tecnologicos": "Tecnológicos",
        "electronico": "electrónico",
        "electronicas": "electrónicas",
        "Electronicas": "Electrónicas",
        "facturacion": "facturación",
        "Facturacion": "Facturación",
        "aplicaciones": "aplicaciones",
        "estan": "están",
        "esten": "estén",
        "basicos": "básicos",
        "Basicos": "Básicos",
        "autenticacion": "autenticación",
        "Autenticacion": "Autenticación",
        "puntuacion": "puntuación",
        "Puntuacion": "Puntuación",
        "accion": "acción",
        "Accion": "Acción",
        "evaluacion": "evaluación",
        "Evaluacion": "Evaluación",
        "generacion": "generación",
        "Generacion": "Generación",
        "recomendacion": "recomendación",
        "Recomendacion": "Recomendación",
        "recomendaciones": "recomendaciones",
        "integracion": "integración",
        "Integracion": "Integración",
        "modulo": "módulo",
        "Modulo": "Módulo",
        "modulos": "módulos",
        "vision": "visión",
        "decision": "decisión",
        "rapida": "rápida",
        "rapido": "rápido",
        "facil": "fácil",
        "criticos": "críticos",
        "Criticos": "Críticos",
        "ultimos": "últimos",
        "Ultimos": "Últimos",
        "identidad": "identidad",
        "proteccion": "protección",
        "Proteccion": "Protección",
        "concienciacion": "concienciación",
        "Concienciacion": "Concienciación",
        "descripcion": "descripción",
        "probabilidad": "probabilidad",
        "huespedes": "huéspedes",
        "Huespedes": "Huéspedes",
        "basica": "básica",
        "basicas": "básicas",
        "Basica": "Básica",
        "Basicas": "Básicas",
        "periodicamente": "periódicamente",
        "inmediatas": "inmediatas",
        "incluira": "incluirá",
        "Incluira": "Incluirá",
        "permitira": "permitirá",
        "Permitira": "Permitirá",
        "seria": "sería",
        "podria": "podría",
        "podrian": "podrían",
        "sera": "será",
        "Sera": "Será",
        "usara": "usará",
        "usaran": "usarán",
        "guardara": "guardará",
        "anadir": "añadir",
        "Anadir": "Añadir",
        "Espanol": "Español",
        "espanol": "español",
        "ingles": "inglés",
        "aleman": "alemán",
        "codigo": "código",
        "Codigo": "Código",
        "tambien": "también",
        "Tambien": "También",
        "mas": "más",
        "Mas": "Más",
        "dia": "día",
        "dias": "días",
        "migraciones": "migraciones",
        "imagenes": "imágenes",
        "camara": "cámara",
        "camaras": "cámaras",
        "Camaras": "Cámaras",
        "operacion": "operación",
        "operacion": "operación",
    }
    for src, dst in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        text = re.sub(rf"\b{re.escape(src)}\b", dst, text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(clean(text), style)


def bullets(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, styles["Body"]), leftIndent=10) for item in items],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontName="Helvetica",
        bulletFontSize=7,
        bulletIndent=0,
    )


def numbered(items: list[str], styles) -> ListFlowable:
    return ListFlowable(
        [ListItem(p(item, styles["Body"]), leftIndent=10) for item in items],
        bulletType="1",
        leftIndent=18,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=8,
        bulletIndent=0,
    )


def section(title: str, styles) -> list:
    return [Spacer(1, 0.22 * cm), p(title, styles["H2"]), Spacer(1, 0.08 * cm)]


def draw_header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(colors.HexColor("#12303F"))
    canvas.rect(0, height - 1.05 * cm, width, 1.05 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(1.6 * cm, height - 0.67 * cm, "HotelSec PolicyForge AI")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 1.6 * cm, height - 0.67 * cm, "Práctica 1 - Ciberseguridad con IA")
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(width / 2, 0.85 * cm, f"Página {doc.page}")
    canvas.restoreState()


def build_pdf():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="CoverTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=26,
            leading=31,
            textColor=colors.HexColor("#0F2D3A"),
            alignment=TA_CENTER,
            spaceAfter=18,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CoverSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=18,
            textColor=colors.HexColor("#334155"),
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#12303F"),
            spaceBefore=8,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H2",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12.5,
            leading=16,
            textColor=colors.HexColor("#0F766E"),
            spaceBefore=6,
            spaceAfter=4,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=13.2,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1F2937"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=11.2,
            textColor=colors.HexColor("#374151"),
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHead",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.4,
            leading=10.5,
            alignment=TA_LEFT,
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableCell",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.0,
            leading=10.3,
            textColor=colors.HexColor("#1F2937"),
        )
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.7 * cm,
        bottomMargin=1.35 * cm,
        title="HotelSec PolicyForge AI - Propuesta de proyecto",
        author="Proyecto Master Ciberseguridad",
    )

    story = []

    # Cover
    story.append(Spacer(1, 2.3 * cm))
    story.append(p("HotelSec PolicyForge AI", styles["CoverTitle"]))
    story.append(p("Analizador de madurez, riesgos y politicas de ciberseguridad para hoteles de Lanzarote", styles["CoverSubtitle"]))
    story.append(Spacer(1, 0.6 * cm))
    cover_table = Table(
        [
            [p("Practica", styles["TableHead"]), p("Practica 1 - Desarrollo de herramienta de ciberseguridad con Inteligencia Artificial", styles["TableCell"])],
            [p("Linea", styles["TableHead"]), p("Normativa y Cumplimiento", styles["TableCell"])],
            [p("Enfoque", styles["TableHead"]), p("Hoteles, alojamientos turisticos y pymes del sector turistico de Lanzarote", styles["TableCell"])],
            [p("Resultado", styles["TableHead"]), p("Dashboard web, evaluador de madurez, generador IA de politicas e informe PDF", styles["TableCell"])],
        ],
        colWidths=[3.1 * cm, 12.1 * cm],
    )
    cover_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#12303F")),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#F8FAFC")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CBD5E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(cover_table)
    story.append(Spacer(1, 1.1 * cm))
    story.append(p("Documento redactado en primera persona para presentar la idea inicial del proyecto, justificar su encaje con la practica y explicar las funcionalidades y herramientas previstas.", styles["CoverSubtitle"]))
    story.append(PageBreak())

    story += section("1. Presentacion del proyecto", styles)
    story.append(p("Mi proyecto se llama HotelSec PolicyForge AI. La idea consiste en desarrollar una plataforma web de ciberseguridad orientada a hoteles, alojamientos turisticos y pequenas empresas del sector turistico de Lanzarote.", styles["Body"]))
    story.append(p("El objetivo principal es que una empresa pueda introducir informacion sobre su situacion actual, sus sistemas tecnologicos, sus procesos con datos personales y sus medidas de seguridad, y que la plataforma genere automaticamente un diagnostico inicial de madurez, un mapa de riesgos, recomendaciones priorizadas y un paquete de politicas de seguridad adaptadas al negocio.", styles["Body"]))
    story.append(p("No quiero que sea simplemente una herramienta que genere documentos con IA. Mi objetivo es crear una solucion funcional que ayude a una pyme turistica a entender sus riesgos reales y a empezar a organizar su seguridad de una forma practica, visual y comprensible.", styles["Body"]))

    story += section("2. Justificacion", styles)
    story.append(p("He elegido este proyecto porque el sector turistico depende cada vez mas de sistemas digitales: reservas online, plataformas externas, TPV, correo electronico, redes WiFi para clientes, sistemas de facturacion, camaras, cerraduras inteligentes y aplicaciones en la nube.", styles["Body"]))
    story.append(p("En el caso de hoteles y alojamientos de Lanzarote, muchos negocios son pequenas o medianas empresas que no siempre tienen un departamento interno de ciberseguridad. Sin embargo, tratan datos personales de clientes, documentos de identidad, datos de pago, informacion de reservas y comunicaciones con proveedores.", styles["Body"]))
    story.append(p("Esto hace que esten expuestos a riesgos como phishing, ransomware, robo de credenciales, fuga de datos personales, mala gestion de copias de seguridad, accesos compartidos, WiFi mal segmentada o incumplimientos basicos del RGPD.", styles["Body"]))

    story += section("3. Encaje con la practica", styles)
    story.append(p("El proyecto encaja dentro de la linea de Normativa y Cumplimiento de la practica. Concretamente, combina varias ideas del enunciado:", styles["Body"]))
    story.append(bullets([
        "Generador de politicas de seguridad con IA.",
        "Simulador de auditoria de ciberseguridad.",
        "Gestor de riesgos de seguridad con IA.",
        "Generador de planes de continuidad y respuesta a incidentes.",
        "Recomendador basico de medidas alineadas con RGPD e ISO 27001.",
    ], styles))

    story += section("4. Problema que resuelve", styles)
    story.append(p("El problema principal es que muchas pymes turisticas no saben por donde empezar en ciberseguridad. Pueden tener antivirus o copias de seguridad, pero no disponen de politicas internas, no conocen su nivel de madurez, no tienen un plan de respuesta ante incidentes y no saben priorizar que medidas implantar primero.", styles["Body"]))
    story.append(numbered([
        "La empresa completa un analizador de perfil.",
        "La herramienta calcula una puntuacion de madurez.",
        "Se identifican riesgos tecnicos, organizativos y normativos.",
        "La IA genera politicas adaptadas al caso concreto.",
        "El sistema crea un plan de accion priorizado.",
        "Se genera un informe PDF profesional.",
        "El dashboard permite consultar el historial y la evolucion.",
    ], styles))

    story += section("5. Usuarios objetivo", styles)
    story.append(bullets([
        "Hoteles pequenos y medianos.",
        "Apartahoteles.",
        "Villas turisticas.",
        "Hostales y pensiones.",
        "Empresas de alquiler vacacional.",
        "Pequenas agencias turisticas.",
        "Consultores o proveedores IT que dan soporte a este tipo de empresas.",
    ], styles))

    story.append(PageBreak())

    story += section("6. Analizador de empresa", styles)
    story.append(p("El analizador no se limita a preguntar el sector y el numero de empleados. Incluye campos especificos para el contexto hotelero, lo que permite que la IA genere resultados mucho mas concretos.", styles["Body"]))

    analyzer_rows = [
        ["Area", "Campos principales"],
        ["Perfil del negocio", "Nombre, municipio, tipo de alojamiento, habitaciones, empleados fijos, empleados temporales, temporada alta/baja, proveedor IT."],
        ["Sistemas tecnologicos", "PMS, channel manager, motor de reservas, Booking/Airbnb/Expedia, TPV, pagos online, facturacion, correo, nube, web propia, CRM."],
        ["Seguridad actual", "MFA, gestor de contrasenas, cuentas compartidas, backups, pruebas de restauracion, antivirus/EDR, firewall, actualizaciones, WiFi separada."],
        ["Datos personales y RGPD", "Pasaportes, DNI, datos de pago, menores, conservacion, proveedores, contratos, registro de actividades y protocolo de brechas."],
        ["Riesgo operativo", "Caida de reservas, perdida de correo, ransomware, operacion sin internet, check-in manual, responsable de incidentes, tiempo de respuesta IT."],
        ["Personal", "Formacion en phishing, empleados temporales, revocacion de accesos, dispositivos personales, WhatsApp o mensajeria con datos de clientes."],
        ["IoT e instalaciones", "CCTV, cerraduras electronicas, domotica, tablets, kioscos de check-in y control horario."],
    ]
    analyzer_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(analyzer_rows)],
        colWidths=[4.0 * cm, 11.2 * cm],
        repeatRows=1,
    )
    analyzer_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12303F")),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(analyzer_table)

    story += section("7. Funcionalidades principales", styles)
    functionality_rows = [
        ["Funcionalidad", "Descripcion"],
        ["Dashboard principal", "Muestra puntuacion global, nivel de riesgo, riesgos criticos, politicas generadas, tareas pendientes, ultimos analisis y estado del plan de accion."],
        ["Evaluador de madurez", "Calcula una puntuacion de 0 a 100 y la divide por areas: identidad, datos, backups, red, dispositivos, personal, incidentes y continuidad."],
        ["Mapa de riesgos", "Identifica riesgos con descripcion, causa probable, impacto, probabilidad, prioridad y medida recomendada."],
        ["Generador de politicas con IA", "Crea politicas adaptadas sobre contrasenas, backups, dispositivos, teletrabajo, WiFi, PMS, proveedores, incidentes y proteccion de datos."],
        ["Recomendaciones RGPD e ISO 27001", "Ofrece recomendaciones iniciales de cumplimiento, dejando claro que no sustituye una auditoria ni una certificacion oficial."],
        ["Plan de accion", "Divide las medidas en acciones inmediatas, 30 dias, 90 dias y mejoras a medio plazo, con prioridad, dificultad, impacto y responsable sugerido."],
        ["Informe PDF", "Genera un documento profesional con resumen ejecutivo, perfil del hotel, puntuacion, riesgos, politicas, recomendaciones y conclusiones."],
        ["Historial", "Guarda los analisis de cada empresa para comparar la evolucion de su madurez de seguridad."],
    ]
    functionality_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(functionality_rows)],
        colWidths=[4.4 * cm, 10.8 * cm],
        repeatRows=1,
    )
    functionality_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(functionality_table)

    story.append(PageBreak())

    story += section("8. Arquitectura propuesta", styles)
    architecture_rows = [
        ["Capa", "Responsabilidad"],
        ["Usuario / hotel", "Introduce informacion de la empresa y consulta resultados."],
        ["Frontend web", "Formulario por pasos, dashboard, tablas de riesgos, historial y descarga de informes."],
        ["Backend API", "Gestiona usuarios, empresas, analisis, reglas, llamadas a IA y generacion de informes."],
        ["Motor de reglas", "Calcula puntuaciones, severidades y prioridades con criterios controlados."],
        ["Motor IA", "Genera politicas, recomendaciones, resumen ejecutivo y texto del informe."],
        ["Base de datos", "Almacena usuarios, perfiles, respuestas, puntuaciones, riesgos, politicas e informes."],
        ["PDF / dashboard", "Presenta los resultados de forma visual y descargable."],
    ]
    arch_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(architecture_rows)],
        colWidths=[4.0 * cm, 11.2 * cm],
        repeatRows=1,
    )
    arch_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12303F")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(arch_table)

    story += section("9. Stack tecnico propuesto", styles)
    stack_rows = [
        ["Area", "Herramientas que voy a utilizar", "Motivo"],
        ["Frontend", "React, Vite, TypeScript, Tailwind CSS, React Router, React Hook Form, Zod, Recharts, Lucide React, Axios o TanStack Query.", "Permite crear una interfaz moderna, rapida y mantenible, con formularios robustos y dashboard visual."],
        ["Backend", "Python, FastAPI, Pydantic, SQLAlchemy, Alembic, JWT, bcrypt o Passlib.", "FastAPI es ligero, rapido, documenta la API automaticamente y encaja bien con servicios de IA."],
        ["Base de datos", "PostgreSQL.", "Es robusta, profesional y adecuada para guardar usuarios, empresas, analisis, riesgos, politicas e informes."],
        ["IA", "OpenAI API o modelo local con Ollama, prompts estructurados, plantillas y motor de reglas.", "La IA genera textos adaptados, mientras que las reglas aportan consistencia a puntuaciones y riesgos."],
        ["PDF", "ReportLab o WeasyPrint.", "Permite generar informes profesionales descargables desde la propia herramienta."],
        ["Despliegue", "Hetzner Cloud VPS, Docker, Docker Compose, Nginx, Let's Encrypt.", "Cumple el requisito de despliegue real y permite publicar la aplicacion con HTTPS."],
        ["Repositorio", "GitHub, README, ramas, commits por fases y .env.example.", "Facilita la evaluacion del historial de desarrollo y la organizacion del proyecto."],
        ["Seguridad", "HTTPS, JWT, hash de contrasenas, validacion de entrada, variables de entorno, rate limiting, logs y backups.", "Protege la propia herramienta y demuestra buenas practicas de desarrollo seguro."],
    ]
    stack_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(stack_rows)],
        colWidths=[2.75 * cm, 6.25 * cm, 6.2 * cm],
        repeatRows=1,
    )
    stack_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(stack_table)

    story.append(PageBreak())

    story += section("10. Estructura del repositorio", styles)
    story.append(p("La estructura inicial del repositorio podria ser la siguiente:", styles["Body"]))
    repo_rows = [
        ["Ruta", "Contenido"],
        ["frontend/", "Aplicacion React con Vite y TypeScript."],
        ["backend/", "API FastAPI, modelos, rutas, servicios, motor de scoring e integracion IA."],
        ["docs/", "Documentacion, capturas, diagramas y evidencias del desarrollo."],
        ["docker-compose.yml", "Orquestacion de frontend, backend, base de datos y proxy."],
        [".env.example", "Variables necesarias sin exponer secretos reales."],
        ["README.md", "Descripcion del proyecto, instalacion, uso y despliegue."],
    ]
    repo_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(repo_rows)],
        colWidths=[4.2 * cm, 11.0 * cm],
        repeatRows=1,
    )
    repo_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12303F")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#F8FAFC"), colors.white]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(repo_table)

    story += section("11. Seguridad de la propia herramienta", styles)
    story.append(p("Ademas de analizar la seguridad de hoteles, la propia plataforma debe estar protegida. Por eso incorporare medidas de desarrollo seguro desde el inicio:", styles["Body"]))
    story.append(bullets([
        "HTTPS obligatorio en produccion.",
        "Autenticacion mediante JWT.",
        "Hash seguro de contrasenas.",
        "Variables de entorno para claves y secretos.",
        "Validacion de datos en frontend y backend.",
        "Control basico de roles.",
        "Rate limiting en endpoints sensibles.",
        "Logs de actividad.",
        "Copias de seguridad de la base de datos.",
    ], styles))

    story += section("12. Roadmap para la Practica 2", styles)
    roadmap_rows = [
        ["Mejora", "Descripcion"],
        ["RAG con fuentes oficiales", "Integrar documentacion de INCIBE, AEPD, ISO 27001 o NIST para enriquecer respuestas."],
        ["Simulador de incidentes", "Escenarios como ransomware, phishing, caida de reservas o fuga de pasaportes."],
        ["Evaluacion de proveedores", "Cuestionarios y scorecards para proveedores IT, PMS, marketing o mantenimiento."],
        ["Comparativa mensual", "Evolucion historica de madurez y reduccion de riesgos."],
        ["Modulo de formacion", "Contenido adaptado para recepcion, direccion, administracion y personal temporal."],
        ["Multiidioma", "Espanol, ingles y aleman para hacerlo mas util en el contexto turistico de Lanzarote."],
        ["Escaneo externo basico", "Revision inicial de dominio, HTTPS, cabeceras y exposicion publica."],
    ]
    roadmap_table = Table(
        [[p(cell, styles["TableHead"] if i == 0 else styles["TableCell"]) for cell in row] for i, row in enumerate(roadmap_rows)],
        colWidths=[4.3 * cm, 10.9 * cm],
        repeatRows=1,
    )
    roadmap_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F766E")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(roadmap_table)

    story += section("13. Conclusion", styles)
    story.append(p("HotelSec PolicyForge AI es una propuesta realista y alineada con los requisitos de la practica. Combina desarrollo web, inteligencia artificial, ciberseguridad, normativa, gestion de riesgos, generacion documental y despliegue real.", styles["Body"]))
    story.append(p("La herramienta tiene un caso de uso concreto: ayudar a hoteles y pymes turisticas de Lanzarote a conocer su nivel inicial de ciberseguridad y obtener politicas y recomendaciones adaptadas a su situacion.", styles["Body"]))
    story.append(p("Considero que es un proyecto adecuado para la Practica 1 porque permite construir una version funcional en el plazo disponible y, al mismo tiempo, deja margen para ampliar la herramienta en una Practica 2 con funcionalidades mas avanzadas.", styles["Body"]))

    doc.build(story, onFirstPage=draw_header_footer, onLaterPages=draw_header_footer)


if __name__ == "__main__":
    build_pdf()
    print(OUTPUT)
