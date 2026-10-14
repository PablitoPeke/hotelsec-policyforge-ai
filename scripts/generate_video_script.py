"""Generate an editable recording script and readable PDF from the same source."""
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path

from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs/practica3'
SOURCE = DOCS / 'video_script.json'
MARKDOWN = DOCS / '14_guion_lectura.md'
PDF = ROOT / 'output/pdf/P3_Guion_lectura_y_grabacion.pdf'
data = json.loads(SOURCE.read_text(encoding='utf-8'))
width = A4[0] - 100
styles = {
    'title': ParagraphStyle('title', fontName='Helvetica-Bold', fontSize=24, leading=29, spaceAfter=20, textColor=colors.HexColor('#173c40')),
    'heading': ParagraphStyle('heading', fontName='Helvetica-Bold', fontSize=19, leading=24, spaceAfter=15, textColor=colors.HexColor('#173c40')),
    'label': ParagraphStyle('label', fontName='Helvetica-Bold', fontSize=10, leading=14, spaceBefore=9, spaceAfter=7, textColor=colors.HexColor('#08776f')),
    'body': ParagraphStyle('body', fontName='Helvetica', fontSize=11, leading=15.5, spaceAfter=10),
    'speech': ParagraphStyle('speech', fontName='Helvetica', fontSize=13, leading=18.5, spaceAfter=14),
    'action': ParagraphStyle('action', fontName='Helvetica', fontSize=10.5, leading=14.5, spaceAfter=7, textColor=colors.HexColor('#425b63')),
    'cell': ParagraphStyle('cell', fontName='Helvetica', fontSize=10, leading=13),
    'code': ParagraphStyle('code', fontName='Courier', fontSize=9, leading=13, spaceAfter=12),
}


def p(text, style='body'):
    return Paragraph(escape(str(text)).replace('\n', '<br/>'), styles[style])


def table(rows, widths):
    result = Table([[p(cell, 'cell') for cell in row] for row in rows], colWidths=widths, repeatRows=1)
    result.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e1eeec')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -1), .4, colors.HexColor('#cfdbdf')),
        ('TOPPADDING', (0, 0), (-1, -1), 7), ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return result


def speech_count(block):
    common = block['speech'] + block.get('closing_speech', [])
    count = sum(len(text.split()) for text in common)
    alternatives = [sum(len(text.split()) for text in alt['speech']) for alt in block.get('alternatives', [])]
    return count + (max(alternatives) if alternatives else 0)


required = [f'RF-{i:02}' for i in range(1, 14)] + [f'RNF-{i:02}' for i in range(1, 8)] + [f'RE-{i:02}' for i in range(1, 4)]
coverage = {key: [block['id'] for block in data['blocks'] if key in block['requirements']] for key in required}
assert all(coverage.values()), 'A requirement is missing from the recording script.'
assert len(set(block['id'] for block in data['blocks'])) == len(data['blocks'])
for command in data['commands']:
    assert '--with-ai' not in command['code'], 'Never prepare an automatic paid check in the default commands.'

md = [f"# {data['title']}", '', f"Autor: {data['author']}. Version: {data['version']}. Revision: {data['date']}.",
      '', 'Lee solo LEER. PANTALLA son acciones silenciosas. En las alternativas, lee solamente la que describa el resultado real.',
      '', f"Duracion prevista: {data['target_duration']}. No acredita duracion del archivo ni minutos reales.", '', '## Requisitos del video']
md += ['- ' + text for text in data['requirements']]
md += ['', '## Preparacion antes de REC'] + ['- ' + text for text in data['preflight']]
md += ['', '## Datos exactos de la demostracion', '', '| Campo | Valor |', '|---|---|']
md += [f'| {key} | {value} |' for key, value in data['demo_fields']]
md += ['', '**Casillas marcadas al empezar:**'] + ['- ' + text for text in data['initial_checked']]
md += ['', '**Casillas desmarcadas al empezar:**'] + ['- ' + text for text in data['initial_unchecked']]
story = [Spacer(1, 60), p('GUION DE LECTURA Y DEMOSTRACION', 'label'), p('HotelSec PolicyForge AI', 'title'),
         p('Practica 3 - Pablo Cortes', 'heading'), p(f"Version {data['version']} | {data['date']}"),
         p(data['target_duration']), p('Texto literal + acciones de pantalla + respuestas alternativas.'),
         p('No leer las instrucciones ni todas las alternativas. Ensayar antes; explicar con tus palabras si el docente pregunta. No se han grabado video ni minutos reales.'),
         p(data['url']), PageBreak(), p('Lo que exige el enunciado', 'heading')]
story += [p('- ' + text) for text in data['requirements']]
story += [p('Fuente: enunciado Practica_3_Evolve (1).pdf, paginas6-8 y11-12, proporcionado por el alumno. No es necesario comprar un dominio ni una webcam.', 'action'),
          PageBreak(), p('Antes de pulsar REC', 'heading')]
story += [p(f'{i}. {text}') for i, text in enumerate(data['preflight'], 1)]
story += [PageBreak(), p('Ficha del hotel ficticio', 'heading'), table([['Campo', 'Valor']] + data['demo_fields'], [150, width - 150]),
          Spacer(1, 15), p('Estas cifras son datos ficticios, no resultados calculados ni recomendaciones legales.', 'action'),
          PageBreak(), p('Casillas del primer analisis', 'heading'), p('MARCADAS', 'label')]
story += [p('- ' + text, 'action') for text in data['initial_checked']]
story += [p('DESMARCADAS', 'label')] + [p('- ' + text, 'action') for text in data['initial_unchecked']]

for block in data['blocks']:
    md += ['', '---', '', f"## {block['id']} | {block['time']} previsto | {block['title']}",
           '', 'Requisitos: ' + ', '.join(block['requirements']), '', '### PANTALLA - NO LEER']
    md += ['- ' + text for text in block['actions']]
    md += ['', '### LEER', '']
    for text in block['speech']:
        md += [text, '']
    story += [PageBreak(), p(f"{block['id']} | {block['time']} PREVISTO", 'label'), p(block['title'], 'heading'),
              p('Requisitos: ' + ', '.join(block['requirements']), 'action'), p('PANTALLA - NO LEER', 'label')]
    story += [p('- ' + text, 'action') for text in block['actions']]
    story += [p('LEER', 'label')] + [p(text, 'speech') for text in block['speech']]
    for alternative in block.get('alternatives', []):
        md += ['', '### ' + alternative['condition'], '']
        for text in alternative['speech']:
            md += [text, '']
        story += [p(alternative['condition'], 'label')] + [p(text, 'speech') for text in alternative['speech']]
    if block.get('closing_speech'):
        md += ['', '### LEER AL FINAL DEL BLOQUE', '']
        for text in block['closing_speech']:
            md += [text, '']
        story += [KeepTogether([p('LEER AL FINAL DEL BLOQUE', 'label')]
                               + [p(text, 'speech') for text in block['closing_speech']])]

md += ['', '---', '', '## Comandos preparados']
story += [PageBreak(), p('Comandos preparados', 'heading'), p('Solo sistemas propios. Sin llamadas IA de pago en estos comandos. No capturar secretos.')]
for command in data['commands']:
    md += ['', '### ' + command['title'], '', command['where'], '', '```powershell', command['code'], '```']
    story += [KeepTogether([p(command['title'], 'label'), p(command['where']), p(command['code'], 'code')])]
md += ['', '## Frases ante incidencias']
story += [PageBreak(), p('Si algo no sale como esperabas', 'heading')]
for title, phrase in data['incident_phrases']:
    md += ['', '### ' + title, '', phrase]
    story += [p(title, 'label'), p(phrase)]
md += ['', '## Despues de grabar'] + [f'{i}. {text}' for i, text in enumerate(data['after_recording'], 1)]
story += [PageBreak(), p('Despues de grabar', 'heading')]
story += [p(f'{i}. {text}') for i, text in enumerate(data['after_recording'], 1)]
md += ['', '## Minutos REALES para la matriz', '', 'No rellenado: falta el MP4. Copiar el minuto observado, no el previsto.', '', '| Requisito | Bloques orientativos | MM:SS real |', '|---|---|---|']
md += [f"| {key} | {', '.join(coverage[key])} | Pendiente |" for key in required]
story += [PageBreak(), p('Minutos REALES de tu video', 'heading'), p('Completar despues de revisar el MP4. Los bloques sirven para localizar el momento, no sustituyen el segundo real.'),
          table([['Requisito', 'Bloques orientativos', 'MM:SS real']] + [[key, ', '.join(coverage[key]), 'Pendiente'] for key in required], [80, width - 165, 85])]
md += ['', '## Mini glosario para entender lo que dices', '', '| Concepto | Explicacion |', '|---|---|']
md += [f'| {key} | {value} |' for key, value in data['mini_glossary']]
story += [PageBreak(), p('Entiende lo que estas explicando', 'heading'), table([['Concepto', 'Explicacion']] + data['mini_glossary'], [100, width - 100])]
words = sum(speech_count(block) for block in data['blocks'])
md += ['', f'Lectura aproximada: {words} palabras, eligiendo una alternativa por bloque. El tiempo real depende de ritmo, acciones y esperas.',
       '', 'Fuente editable: docs/practica3/video_script.json. Regenerar MD/PDF con python scripts/generate_video_script.py.', '']
MARKDOWN.write_text('\n'.join(md), encoding='utf-8')


def footer(canvas, doc):
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.HexColor('#526871'))
    canvas.drawString(50, 28, 'HotelSec | Guion: tiempos previstos, no evidencia grabada')
    canvas.drawRightString(A4[0] - 50, 28, str(doc.page))


PDF.parent.mkdir(parents=True, exist_ok=True)
SimpleDocTemplate(str(PDF), pagesize=A4, rightMargin=50, leftMargin=50, topMargin=45, bottomMargin=47,
                  title='HotelSec - Guion literal de grabacion', author=data['author']).build(story, onFirstPage=footer, onLaterPages=footer)
reader = PdfReader(PDF)
text = '\n'.join(page.extract_text() for page in reader.pages)
assert all(block['title'] in text for block in data['blocks'])
assert all(key in text for key in required)
assert words >= 1600, 'Script unexpectedly short for the requested demonstration.'
metadata = {'generated_at': datetime.now(timezone.utc).isoformat(), 'pdf': PDF.relative_to(ROOT).as_posix(),
            'markdown': MARKDOWN.relative_to(ROOT).as_posix(), 'pages': len(reader.pages), 'spoken_words_longest_path': words,
            'blocks': len(data['blocks']), 'requirements_covered': required,
            'actual_video_recorded': False, 'actual_duration_verified': False,
            'paid_ai_calls_during_preparation': 0, 'limits': 'Word count/planned timings do not prove MP4 duration or successful demo.'}
(DOCS / 'evidence/video-script-layout.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
print(json.dumps(metadata, indent=2))
