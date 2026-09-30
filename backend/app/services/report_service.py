from html import escape
from io import BytesIO
from datetime import datetime
from app.services.report_labels import FIELDS, VALUES

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


def render_report(bundle: dict, created_at: str, record_id: str) -> bytes:
    output = BytesIO()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportBody", fontName="Helvetica", fontSize=10, leading=15, spaceAfter=7))
    styles.add(ParagraphStyle(name="SmallBody", fontSize=8, leading=11))
    def p(value, style="ReportBody"):
        return Paragraph(escape(str(value)).replace("\n", "<br/>"), styles[style])
    story = [p("HotelSec PolicyForge AI", "Title"), p("Informe de ciberseguridad hotelera", "Heading1")]
    profile = bundle["input"]["hotel_profile"]
    result = bundle["assessment"]
    readable_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%d/%m/%Y %H:%M UTC')
    story += [p(profile["business_name"], "Heading2"), p(f"Fecha: {readable_date}"), p(f"Referencia: {record_id}", "SmallBody"),
              p(f"Madurez: {result['overall_score']}/100 | Riesgo: {VALUES[result['risk_level']]}"),
              p(bundle["disclaimer"]), p("Resumen ejecutivo", "Heading2"), p(bundle["ai_summary"]["summary"]),
              p(f"Resumen: {VALUES.get(bundle['ai_summary']['provider'], bundle['ai_summary']['provider'])} | Politicas: {VALUES.get(bundle['policy_pack']['provider'], bundle['policy_pack']['provider'])}"),
              p(f"Version: {bundle['scoring_version']} / {bundle['prompt_version']}", "SmallBody"),
              p("Perfil y respuestas declaradas", "Heading2")]
    rows = [[p("Campo", "SmallBody"), p("Declaracion", "SmallBody")]]
    for section in ("hotel_profile", "security_controls"):
        for key, value in bundle["input"][section].items():
            if isinstance(value, bool): value = "Si" if value else "No"
            if value is None: value = "No evaluado"
            if isinstance(value, list): value = ", ".join(value) or "No declarado"
            if isinstance(value, str): value = VALUES.get(value, value)
            rows.append([p(FIELDS.get(key, key.replace("_", " ")), "SmallBody"), p(value, "SmallBody")])
    table = Table(rows, colWidths=[7 * cm, 9 * cm], repeatRows=1)
    table.setStyle(TableStyle([("BACKGROUND", (0,0),(-1,0), colors.HexColor("#dff7f3")),
                              ("VALIGN",(0,0),(-1,-1),"TOP"), ("LINEBELOW",(0,0),(-1,-1),0.3,colors.lightgrey),
                              ("TOPPADDING",(0,0),(-1,-1),5), ("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story += [table, Spacer(1, 10), p("Puntuaciones por area", "Heading2")]
    for area in result["area_scores"]:
        story.append(p(f"{area['area']}: {area['score']}/100"))
    story.append(p("Mapa de riesgos", "Heading2"))
    for risk in result["risks"]:
        story += [p(risk["title"], "Heading3"), p(f"Prioridad {VALUES[risk['severity']]} | Probabilidad {risk['probability']}/5 | Impacto {risk['impact']}/5"),
                  p(risk["description"]), p(risk["recommendation"]), p(risk["rationale"])]
    if not result["risks"]:
        story.append(p("No se detectan riesgos con las reglas y respuestas disponibles."))
    story.append(p("Plan de accion", "Heading2"))
    for action in bundle["actions"]:
        story += [p(action["title"], "Heading3"), p(f"Plazo: {action['deadline_days']} dias | Prioridad: {VALUES[action['priority']]} | Estado: {VALUES[action['status']]}"),
                  p(f"Responsable sugerido: {action['responsible']} | Dificultad: {action['difficulty']} | Impacto: {action['impact']}/5")]
    story += [PageBreak(), p("Politicas propuestas", "Heading1")]
    for policy in bundle["policy_pack"]["policies"]:
        story += [p(policy["name"], "Heading2"), p(policy["objective"]), p("Alcance: " + policy["scope"])]
        for control in policy["controls"]:
            story += [p(control["title"] + " - " + VALUES[control["priority"]], "Heading3"), p(control["description"])]
        story += [p("Evidencias: " + "; ".join(policy["evidence"])), p("Revision: " + policy["review_frequency"])]
    story.append(p("Orientacion y fuentes", "Heading2"))
    for source in bundle["regulatory"]:
        story += [p(source["name"], "Heading3"), p(source["topic"]), p(source["url"], "SmallBody")]
    if bundle.get("description"):
        story += [p("Contexto aportado", "Heading2"), p(bundle["description"])]
    def footer(canvas, doc):
        canvas.setFont("Helvetica", 8)
        canvas.drawString(2 * cm, 1.2 * cm, "HotelSec | Autodiagnostico y propuestas para revision humana")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page))
    SimpleDocTemplate(output, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm,
                      title="HotelSec - " + profile["business_name"]).build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue()
