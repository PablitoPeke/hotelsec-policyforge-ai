"""Build the pre-video or validated final Practice 3 report from structured evidence."""
import argparse
import json
from io import BytesIO
from html import escape
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, Preformatted, Flowable
from pypdf import PdfReader
from practice_delivery import submission_filename, validate_delivery

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/practica3'
SOURCE = json.loads((DOCS / 'memoria_content.json').read_text(encoding='utf-8'))
RESULTS = json.loads((DOCS / 'evidence/verification.json').read_text(encoding='utf-8'))
CURRENT = json.loads((DOCS / 'evidence/account-center-verification.json').read_text(encoding='utf-8'))
CLOSEOUT = json.loads((DOCS / 'evidence/closeout-verification.json').read_text(encoding='utf-8'))
DELIVERY = json.loads((DOCS / 'delivery_metadata.json').read_text(encoding='utf-8'))
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--final', action='store_true', help='Requires complete real group, video and manual verification metadata')
args = parser.parse_args()
if args.final:
    pending = validate_delivery(DELIVERY)
    if pending:
        parser.error('No generar final: ' + '; '.join(pending))
OUTPUT = ROOT / 'output/pdf' / (submission_filename(DELIVERY) if args.final else 'P3_Pablo_Cortes_Memoria_prevideo.pdf')
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
WIDTH = A4[0] - 4 * cm
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Body11', fontName='Helvetica', fontSize=11, leading=15.5, spaceAfter=12))
styles.add(ParagraphStyle(name='Cell11', fontName='Helvetica', fontSize=11, leading=14))
styles.add(ParagraphStyle(name='Caption9', fontName='Helvetica', fontSize=9, leading=12, textColor=colors.HexColor('#50606b'), spaceAfter=16))
styles.add(ParagraphStyle(name='Kicker', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=colors.HexColor('#08776f'), spaceAfter=8))
styles.add(ParagraphStyle(name='PageTitle', fontName='Helvetica-Bold', fontSize=21, leading=26, textColor=colors.HexColor('#23353b'), spaceAfter=20))
styles.add(ParagraphStyle(name='Code11', fontName='Courier', fontSize=11, leading=15, backColor=colors.HexColor('#eff3f4'), borderPadding=10, spaceAfter=15))


def p(text, style='Body11'):
    return Paragraph(escape(str(text)), styles[style])


class Heading(Paragraph):
    def __init__(self, text, section, kind='content'):
        super().__init__(escape(text), styles['PageTitle'])
        self.section, self.kind, self.label = section, kind, text


class Report(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.locations = []

    def afterFlowable(self, flowable):
        if isinstance(flowable, Heading):
            self.locations.append({'title': flowable.label, 'section': flowable.section, 'kind': flowable.kind, 'page': self.page})


class Architecture(Flowable):
    def __init__(self):
        super().__init__()
        self.width, self.height = WIDTH, 265

    def draw(self):
        canvas = self.canv
        boxes = [('Navegador / React', 224), ('Proxy de mismo origen', 182), ('FastAPI: sesion, CSRF, validacion', 140), ('Reglas y bundle de resultados', 98), ('PostgreSQL: snapshots y progreso', 56), ('Dashboard / PDF ReportLab', 14)]
        for label, y in boxes:
            canvas.setStrokeColor(colors.HexColor('#9aadb3'))
            canvas.setFillColor(colors.HexColor('#f1f6f5'))
            canvas.rect(4, y, 295, 30, fill=1)
            canvas.setFillColor(colors.HexColor('#22373d'))
            canvas.setFont('Helvetica', 11)
            canvas.drawCentredString(151, y + 11, label)
            if y > 14:
                canvas.line(151, y, 151, y - 12)
                canvas.line(151, y - 12, 147, y - 7)
                canvas.line(151, y - 12, 155, y - 7)
        canvas.setFillColor(colors.HexColor('#fff5dd'))
        canvas.rect(323, 126, 149, 48, fill=1)
        canvas.setFillColor(colors.HexColor('#22373d'))
        canvas.setFont('Helvetica-Bold', 11)
        canvas.drawCentredString(397, 153, 'OpenAI opcional')
        canvas.setFont('Helvetica', 10)
        canvas.drawCentredString(397, 138, 'Consentimiento + fallback')
        canvas.setDash(3, 3)
        canvas.line(299, 155, 323, 155)
        canvas.line(397, 126, 397, 113)
        canvas.line(397, 113, 299, 113)
        canvas.setDash()


def table(rows, widths=None):
    if widths is None:
        n = len(rows[0])
        widths = [WIDTH / n] * n
        if n == 2: widths = [WIDTH * .28, WIDTH * .72]
    values = [[p(str(cell), 'Cell11') for cell in row] for row in rows]
    result = Table(values, colWidths=widths, repeatRows=1, hAlign='LEFT')
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dfedeb')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), .4, colors.HexColor('#d5dfe1')),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    return result


def trace(kind):
    rows = [['ID', 'Estado', 'Implementacion', 'Prueba / evidencia', 'Video']]
    if kind.startswith('functional'):
        entries = [
            ('RF-01', 'AssessmentForm / schema', 'Entradas invalidas; fig.1'),
            ('RF-02', 'assessment_service', 'Perfiles y reevaluacion; fig.2'),
            ('RF-03', 'RiskFinding / Results', 'Bundle y PDF; fig.2'),
            ('RF-04', 'policy_service / IA', 'Pack10; mocks y OpenAI real13/10; fig.5'),
            ('RF-05', 'product_service sources', 'PDF AEPD; vista informe'),
            ('RF-06', 'records PATCH / actions', 'full_flow; progreso E2E; fig.4'),
            ('RF-07', 'App dashboard', 'E2E escritorio/movil; fig.2'),
            ('RF-08', 'report_service', 'pypdf todos riesgos; descarga'),
            ('RF-09', 'db / migraciones', 'Persistencia; 0004 PostgreSQL'),
            ('RF-10', 'history / App', 'company_history; fig.3'),
            ('RF-11', 'auth / owned_record', 'isolation de todas las rutas'),
            ('RF-12', 'parse_description', 'conflicts409, optout; fig.6'),
            ('RF-13', 'summary / fallback', 'Mocks y OpenAI real13/10'),
        ]
    else:
        entries = [
            ('RNF-01', 'Compose / README', 'Local limpio y VPS; externo humano pendiente'),
            ('RNF-02', 'Pydantic / errores', '422/413/404; entrada negativa'),
            ('RNF-03', 'Argon2 / Caddy / env', 'Hashes, TLS; Gitleaks historial'),
            ('RNF-04', 'Auditorias / CI', '0 conocidas; CI sin iniciar por restriccion de cuenta'),
            ('RNF-05', 'DELETE / export / cleanup', 'Cascada/export; retencion documentada'),
            ('RNF-06', 'quota / audit / timeout', 'DB:20 cuenta/h;50 global/dia'),
            ('RNF-07', 'Produccion / guia', '0.4.0 HTTPS; backup/restore aislado'),
            ('RE-01', 'Fuente memoria / PDF', 'Prevideo; grupo/enlace/minutos pendientes'),
            ('RE-02', 'Guion / MP4', 'Sin grabacion ni enlace'),
            ('RE-03', 'GitHub / MIT / README', 'Rama y commits; tag final pendiente'),
        ]
    if kind == 'functional_a':
        entries = entries[:7]
    elif kind == 'functional_b':
        entries = entries[7:]
    states = {'RNF-01': 'Parcial', 'RNF-04': 'Con limites', 'RNF-05': 'Con limites',
              'RE-01': 'Parcial', 'RE-02': 'Pendiente', 'RE-03': 'Parcial'}
    rows += [[identifier, states.get(identifier, 'Cumplido'), code, test,
              DELIVERY['video']['timestamps'].get(identifier, 'Pendiente')] for identifier, code, test in entries]
    return table(rows, [48, 65, 113, WIDTH - 290, 64])


def footer(canvas, doc):
    canvas.setStrokeColor(colors.HexColor('#cad6d9'))
    canvas.line(2 * cm, 1.65 * cm, A4[0] - 2 * cm, 1.65 * cm)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#50606b'))
    canvas.drawString(2 * cm, 1.2 * cm, 'HotelSec | Practica 3 | ' + ('Version de entrega' if args.final else 'Version previa al video'))
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, str(doc.page))


def build(locations=None):
    story = [Spacer(1, 3 * cm), p('EVOLVE ACADEMY · CIBERSEGURIDAD CON IA', 'Kicker'),
             Heading('HotelSec PolicyForge AI', 'Portada', 'front'), p('Practica 3: del prototipo al producto', 'Heading2'),
             Spacer(1, cm), p('MEMORIA TECNICA' + ('' if args.final else ' · VERSION PREVIA AL VIDEO'), 'Kicker'),
             p('Autor: ' + SOURCE['author']),
             *([p('Grupo: ' + str(DELIVERY['group_number']))] if DELIVERY['group_number'] is not None else []),
             p('Revision: ' + SOURCE['date']),
             p('GitHub: https://github.com/PablitoPeke/hotelsec-policyforge-ai'), p('Rama: practica3'),
             p('Aplicacion: https://178-105-149-202.sslip.io/'),
             p('Version del producto: 0.4.0; codigo verificado 83d7b9b'),
             p('Video: ' + (DELIVERY['video']['url'] or SOURCE['video'])), Spacer(1, cm),
             p('La version anterior obtuvo 9/10; el alumno indica que no hubo comentarios del docente. Trabajo individual con asistencia IA declarada.'),
             p('Fecha limite: 16/10/2026; confirmar hora en campus.' if args.final else 'Pendientes para entregar: grupo real, video/enlace/minutos, prueba de instalacion por persona externa y revision personal. Horas estimadas por el alumno: 40. No se fabrica evidencia ni se marca esta version como entrega final.'),
             PageBreak(), Heading('Indice de contenidos', 'Indice', 'front')]
    groups = list(dict.fromkeys(page['section'] for page in SOURCE['pages'])) + ['Anexo A. Instalacion y uso', 'Anexo B. Glosario y referencias']
    pages = {}
    for location in locations or []:
        pages.setdefault(location['section'], location['page'])
    story.append(table([['Apartado', 'Pagina']] + [[s, str(pages.get(s, '-'))] for s in groups], [WIDTH - 60, 60]))
    story += [Spacer(1, 20), p('Cuerpo: 11 puntos. Portada, indice y anexos no cuentan como paginas de contenido. Capturas reales con datos ficticios. Evidencias locales y remotas diferenciadas.'), PageBreak()]
    for index, page in enumerate(SOURCE['pages']):
        if index: story.append(PageBreak())
        story += [p(page['section'].upper(), 'Kicker'), Heading(page['title'], page['section'])]
        if page.get('diagram'): story += [Architecture(), p('Figura 0. Arquitectura implementada. El proveedor es opcional; el scoring sigue siendo local.', 'Caption9')]
        if page.get('figure'):
            path = DOCS / 'evidence' / page['figure']
            if not path.exists(): raise FileNotFoundError(f'Real figure missing: {path}')
            figure = Image(str(path))
            scale = min(WIDTH / figure.imageWidth, 8.4 * cm / figure.imageHeight)
            figure.drawWidth, figure.drawHeight = figure.imageWidth * scale, figure.imageHeight * scale
            figure.hAlign = 'LEFT'
            story += [figure, Spacer(1, 8), p(page['caption'], 'Caption9')]
        if page.get('results'):
            b, browser = CLOSEOUT['backend'], CURRENT['browser_hetzner']
            story += [table([['Comprobacion', 'Resultado'], ['Backend pytest', f"{b['tests']} tests; {b['failures']} fallos; {b['errors']} errores"],
                ['Chromium remoto y local', f"{browser['expected']} escenarios correctos en cada entorno; {browser['unexpected']} inesperados"],
                ['pip-audit', f"{CLOSEOUT['python_known_vulnerabilities']} vulnerabilidades conocidas"],
                ['npm audit', f"{CLOSEOUT['npm_vulnerabilities']['total']} vulnerabilidades conocidas"], ['Backup Hetzner13/10', 'pg_restore aislado correcto; DB en uso conservada'], ['Gitleaks historial', '0 hallazgos accionables; 2 falsos positivos revisados']]), Spacer(1, 15)]
        for paragraph in page.get('paragraphs', []): story.append(p(paragraph))
        if page.get('table'):
            widths = [WIDTH * ratio for ratio in page['widths']] if page.get('widths') else None
            story += [table(page['table'], widths), Spacer(1, 15)]
        if page.get('trace'): story += [trace(page['trace']), Spacer(1, 15)]
        if page.get('code'): story.append(Preformatted(page['code'], styles['Code11']))
        if page.get('closing'): story.append(p(page['closing']))
    story += [PageBreak(), Heading('Instalacion y manual de uso', 'Anexo A. Instalacion y uso', 'annex'),
        p('La guia completa reproducible esta en README.md y docs/practica3/05_despliegue.md. El codigo se puede editar en VS Code; seleccionar el interprete del venv de backend. Requisitos locales: Git, Docker Desktop Linux/Compose v2 y Python para setup_local.'),
        Preformatted('python scripts/setup_local.py --port 8085\n# Desde raiz, conservar nombre de proyecto:\ndocker compose --env-file .env.local -p hotelsec-p3\n  -f docker-compose.hetzner.yml up -d --build', styles['Code11']),
        p('La ultima orden se escribe como una sola linea en terminal. Abrir http://localhost:8085. No hay usuarios de fabrica: crear cuenta ficticia, minimo 12 caracteres de contrasena. Las cuentas del navegador automatizado no son cuentas de clientes ni administradores.'),
        table([['Paso de uso', 'Comprobacion'], ['Acceder o crear cuenta', 'Ver Dashboard sin hashes ni secretos'], ['Nuevo analisis', 'Responder controles/contexto y elegir consentimiento IA'], ['Analizar y guardar', 'Resolver conflictos si existen; ver puntuacion'], ['Plan de mejora', 'Cambiar estado y recargar para verificar'], ['Historial', 'Abrir un resultado propio o reevaluarlo'], ['Informe', 'Descargar PDF y comprobar todas sus secciones'], ['Mi cuenta', 'Editar perfil, contrasena y sesiones; exportar datos; borrado confirmado']]),
        Spacer(1, 15), p('No publicar la configuracion HTTP local en Internet. Produccion usa Compose separado con dominio, cookies Secure y Caddy. No usar down -v para actualizar: elimina el volumen. La instalacion asistida no reemplaza probar personalmente desde cero.'),
        PageBreak(), Heading('Glosario y fuentes', 'Anexo B. Glosario y referencias', 'annex'),
        table([['Termino', 'Significado en este proyecto'], ['API', 'Contrato HTTP entre interfaz y backend'], ['Migracion', 'Cambio versionado de tablas e indices'], ['Snapshot', 'Evaluacion guardada con entradas y resultados'], ['CSRF', 'Proteccion ante mutaciones inducidas por otro sitio'], ['HttpOnly', 'Cookie no accesible al JavaScript de la pagina'], ['Fallback', 'Resultado alternativo por reglas cuando no se usa o falla IA'], ['MFA', 'Mas de un factor para autenticar'], ['PMS', 'Sistema de gestion del alojamiento'], ['STRIDE', 'Categorias de amenazas para estructurar la revision']]), Spacer(1, 15)]
    references = [
        'Enunciado: Practica_3_Evolve (1).pdf, 12 paginas, proporcionado por el alumno; no publicado en GitHub.',
        'Documentos previos: propuesta_hotelsec_policyforge_ai.md y docs de Practica 1 del repositorio.',
        'OWASP Session Management: https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html',
        'Caddy Automatic HTTPS: https://caddyserver.com/docs/automatic-https',
        'Alembic: https://alembic.sqlalchemy.org/en/latest/tutorial.html',
        'SQLAlchemy: https://docs.sqlalchemy.org/en/20/orm/session_basics.html',
        'AEPD Facilita RGPD: https://www.aepd.es/guias-y-herramientas/herramientas/facilita-rgpd',
        'INCIBE politicas: https://www.incibe.es/empresas/herramientas/politicas',
        'ISO familia 27000: https://www.iso.org/standard/iso-iec-27000-family',
        'Evidencias: docs/practica3/evidence; revision13/10/2026. Capturas locales/remotas separadas, pruebas con su fecha real, restauracion aislada y revisiones sanitizadas; no traces privados.',
    ]
    story.extend(p(reference) for reference in references)
    output = BytesIO()
    document = Report(output, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=1.8*cm, bottomMargin=2*cm,
                      title='HotelSec - Practica 3 - ' + ('Entrega' if args.final else 'Prevideo'), author=SOURCE['author'])
    document.build(story, onFirstPage=footer, onLaterPages=footer)
    return output.getvalue(), document.locations


_, locations = build()
pdf, locations = build(locations)
OUTPUT.write_bytes(pdf)
reader = PdfReader(BytesIO(pdf))
content_start = min(x['page'] for x in locations if x['kind'] == 'content')
annex_start = min(x['page'] for x in locations if x['kind'] == 'annex')
count = annex_start - content_start
if not 20 <= count <= 40:
    raise ValueError(f'Content page count outside rubric: {count}')
metadata = {'pdf': str(OUTPUT.relative_to(ROOT)), 'total_pages': len(reader.pages), 'content_pages': count,
            'content_start': content_start, 'annex_start': annex_start, 'body_font_size': 11, 'draft': not args.final, 'sections': locations}
(DOCS / 'evidence/memory-layout.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({k: v for k, v in metadata.items() if k != 'sections'}, indent=2))
