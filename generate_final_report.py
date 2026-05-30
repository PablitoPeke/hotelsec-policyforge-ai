from __future__ import annotations

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "HotelSec_PolicyForge_AI_informe_final.pdf"


def style_sheet():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#102a43"),
            spaceAfter=16,
        ),
        "subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["Normal"],
            fontSize=12,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#486581"),
            spaceAfter=14,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=21,
            textColor=colors.HexColor("#0f766e"),
            spaceBefore=12,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#102a43"),
            spaceBefore=8,
            spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontSize=9.5,
            leading=14,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor("#1f2937"),
            spaceAfter=7,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#52606d"),
        ),
        "code": ParagraphStyle(
            "Code",
            parent=base["Code"],
            fontName="Courier",
            fontSize=7.6,
            leading=10,
            textColor=colors.HexColor("#1f2937"),
        ),
    }


def p(text: str, style: ParagraphStyle):
    return Paragraph(text, style)


def table(data, widths=None):
    t = Table(data, colWidths=widths, hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#102a43")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("LEADING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#bcccdc")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f7fb")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    return t


def figure_box(title: str, text: str):
    data = [[Paragraph(f"<b>{title}</b><br/>{text}", style_sheet()["small"])]]
    t = Table(data, colWidths=[16.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef3f8")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#9fb3c8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return t


def build_story():
    s = style_sheet()
    story = []

    story.append(Spacer(1, 2.5 * cm))
    story.append(p("HotelSec PolicyForge AI", s["title"]))
    story.append(
        p(
            "Informe final de la Practica 1 | Ciberseguridad con Inteligencia Artificial",
            s["subtitle"],
        )
    )
    story.append(Spacer(1, 1 * cm))
    story.append(
        table(
            [
                ["Campo", "Contenido"],
                ["Proyecto", "HotelSec PolicyForge AI"],
                ["Linea", "Normativa, cumplimiento y analisis de madurez"],
                ["Autor", "Pablo / PablitoPeke"],
                ["Fecha", "30/05/2026"],
                ["Repositorio", "https://github.com/PablitoPeke/hotelsec-policyforge-ai"],
                ["URL publica Hetzner", "http://178.105.149.202"],
                ["URL publica Render", "https://hotelsec-policyforge-ai-1.onrender.com/"],
            ],
            [4 * cm, 12 * cm],
        )
    )
    story.append(PageBreak())

    story.append(p("1. Indice de contenidos", s["h1"]))
    index_items = [
        "Resumen ejecutivo",
        "Descripcion del problema y justificacion",
        "Arquitectura tecnica",
        "Proceso de desarrollo con evidencias",
        "Guia de despliegue paso a paso",
        "Manual de uso de la herramienta",
        "Conclusiones y lecciones aprendidas",
        "Road map de mejora para la Practica 2",
    ]
    story.extend([p(f"{i + 1}. {item}", s["body"]) for i, item in enumerate(index_items)])

    story.append(p("2. Resumen ejecutivo", s["h1"]))
    story.append(
        p(
            "HotelSec PolicyForge AI es una plataforma web orientada a hoteles, villas y pymes turisticas de Lanzarote. La herramienta permite evaluar la madurez de ciberseguridad, detectar riesgos, generar politicas basicas, crear un resumen asistido por IA y descargar un informe PDF para cliente.",
            s["body"],
        )
    )
    story.append(
        p(
            "El MVP cumple una funcion practica: transformar respuestas tecnicas y descripciones libres del cliente en un diagnostico entendible. La IA no sustituye al motor de reglas, sino que ayuda a interpretar texto libre y redactar resumenes ejecutivos.",
            s["body"],
        )
    )

    story.append(p("3. Descripcion del problema y justificacion", s["h1"]))
    story.append(
        p(
            "Muchas pequenas empresas turisticas no disponen de politicas internas, inventario claro de riesgos ni procedimientos basicos ante incidentes. En hoteles y alojamientos, los sistemas de reservas, pagos, documentos de huespedes, WiFi, PMS y proveedores externos aumentan la superficie de ataque.",
            s["body"],
        )
    )
    story.append(
        p(
            "La solucion propuesta reduce esa barrera mediante un panel web sencillo que pregunta por controles concretos y permite describir la situacion en lenguaje natural. A partir de ello genera puntuaciones, riesgos priorizados, politicas y recomendaciones.",
            s["body"],
        )
    )

    story.append(p("4. Arquitectura tecnica con diagrama", s["h1"]))
    story.append(
        Preformatted(
            """Usuario / Hotel
   |
   v
Frontend React + Vite
   |
   v
Backend FastAPI
   |-- Motor de scoring por reglas
   |-- Generador de politicas
   |-- Integracion IA opcional
   |-- Generador PDF frontend
   v
Dashboard + Riesgos + Politicas + Informe PDF""",
            s["code"],
        )
    )
    story.append(
        table(
            [
                ["Componente", "Tecnologia", "Funcion"],
                ["Frontend", "React, Vite, TypeScript", "Interfaz, formulario, dashboard, descarga PDF"],
                ["Backend", "FastAPI, Pydantic", "API, validacion, scoring, politicas e IA"],
                ["IA", "OpenAI Responses API", "Resumen ejecutivo y analisis de descripcion libre"],
                ["Despliegue", "Render / Docker Compose Hetzner", "Publicacion de la herramienta"],
                ["Repositorio", "GitHub", "Control de versiones y trazabilidad"],
            ],
            [3.2 * cm, 4.4 * cm, 8.4 * cm],
        )
    )

    story.append(p("5. Proceso de desarrollo con evidencias", s["h1"]))
    story.append(
        p(
            "El desarrollo se realizo por fases: documentacion inicial, backend FastAPI, analizador de madurez, frontend React, conexion API, generador de politicas, informe PDF, integracion IA, despliegue y mejoras visuales.",
            s["body"],
        )
    )
    story.append(
        table(
            [
                ["Fase", "Evidencia"],
                ["Backend base", "Endpoint GET /api/v1/health y tests automaticos"],
                ["Analizador", "Endpoint POST /api/v1/assessments/analyze"],
                ["Politicas", "Endpoint POST /api/v1/policies/generate"],
                ["IA", "Endpoints POST /api/v1/ai/executive-summary y /ai/analyze-description"],
                ["Frontend", "Dashboard publico con formulario, riesgos, politicas, IA e informe"],
                ["Despliegue", "URL publica en Hetzner y despliegue adicional en Render"],
            ],
            [4.2 * cm, 11.8 * cm],
        )
    )
    story.append(Spacer(1, 0.3 * cm))
    story.append(
        figure_box(
            "Captura 1: Dashboard publico",
            "Panel principal con cabecera, metricas, formulario de analisis, riesgos y estado de API.",
        )
    )
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        figure_box(
            "Captura 2: Analisis por descripcion libre",
            "Bloque donde el cliente escribe su situacion y la IA complementa el formulario.",
        )
    )

    story.append(p("Fragmento de codigo representativo", s["h2"]))
    story.append(
        Preformatted(
            """@router.post("/analyze-description", response_model=AiDescriptionAnalysisResponse)
def analyze_free_text_description(payload: AiDescriptionAnalysisRequest):
    return analyze_description_with_ai(payload)""",
            s["code"],
        )
    )

    story.append(PageBreak())
    story.append(p("6. Guia de despliegue paso a paso", s["h1"]))
    story.append(
        p(
            "La aplicacion se encuentra desplegada publicamente en Hetzner Cloud VPS mediante Docker Compose y Nginx. Durante el desarrollo tambien se preparo un despliegue adicional en Render para pruebas rapidas y disponibilidad alternativa.",
            s["body"],
        )
    )
    story.append(
        Preformatted(
            """git clone https://github.com/PablitoPeke/hotelsec-policyforge-ai.git
cd hotelsec-policyforge-ai
cp infra/.env.hetzner.example .env
docker compose -f docker-compose.hetzner.yml --env-file .env up -d --build
curl http://178.105.149.202/api/v1/health""",
            s["code"],
        )
    )
    story.append(
        p(
            "El dominio o subdominio debe apuntar a la IP publica del VPS. Nginx actua como reverse proxy y redirige /api hacia FastAPI y el resto hacia el frontend.",
            s["body"],
        )
    )

    story.append(p("7. Manual de uso de la herramienta", s["h1"]))
    steps = [
        "Abrir la URL publica del panel web.",
        "Comprobar que la API aparece como OK.",
        "Rellenar o ajustar el formulario del alojamiento.",
        "Opcionalmente, escribir una descripcion libre para complementar el formulario.",
        "Pulsar Analizar hotel o Combinar formulario + descripcion.",
        "Revisar puntuacion, areas, riesgos y politicas.",
        "Leer el resumen IA y descargar el informe PDF.",
    ]
    story.extend([p(f"{i + 1}. {step}", s["body"]) for i, step in enumerate(steps)])

    story.append(p("8. Conclusiones y lecciones aprendidas", s["h1"]))
    story.append(
        p(
            "El proyecto demuestra como combinar un motor de reglas explicable con IA generativa. La parte determinista aporta consistencia en la puntuacion, mientras que la IA mejora la experiencia al interpretar texto libre y redactar resumenes ejecutivos.",
            s["body"],
        )
    )
    story.append(
        p(
            "Una leccion importante ha sido separar la logica critica de scoring de la generacion de texto. Esto evita que una respuesta generativa cambie de forma impredecible la madurez calculada.",
            s["body"],
        )
    )

    story.append(p("9. Road map de mejora para la Practica 2", s["h1"]))
    roadmap = [
        ["Mejora", "Objetivo", "Estimacion"],
        ["PostgreSQL", "Guardar empresas, analisis e informes", "10-14 h"],
        ["Usuarios y roles", "Login, empresas y permisos", "12-16 h"],
        ["PDF backend avanzado", "Plantilla profesional con graficas", "8-12 h"],
        ["Prompts versionados", "Controlar cambios de IA", "8-10 h"],
        ["Historico", "Evolucion temporal de madurez", "10-12 h"],
        ["Seguridad despliegue", "HTTPS, rate limiting y cabeceras", "6-10 h"],
    ]
    story.append(table(roadmap, [4.5 * cm, 8 * cm, 3 * cm]))

    story.append(p("10. Anexos", s["h1"]))
    story.append(p("Documentos relevantes del repositorio:", s["body"]))
    for item in [
        "docs/08_assessment_api_examples.md",
        "docs/09_deployment_guide.md",
        "docs/10_hetzner_deployment.md",
        "docs/11_practica2_roadmap.md",
        "docker-compose.hetzner.yml",
    ]:
        story.append(p(f"- {item}", s["body"]))

    return story


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d9e2ec"))
    canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#52606d"))
    canvas.drawString(2 * cm, 1.1 * cm, "HotelSec PolicyForge AI | Practica 1")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Pagina {doc.page}")
    canvas.restoreState()


def main():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="HotelSec PolicyForge AI - Informe final",
    )
    doc.build(build_story(), onFirstPage=header_footer, onLaterPages=header_footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
