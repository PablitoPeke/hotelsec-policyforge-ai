import { riskLabels } from '../data/assessmentDefaults'
import type { AssessmentResponse } from '../api/assessment'
import type { PolicyPackResponse } from '../api/policies'

type PdfLine = {
  text: string
  size?: number
  bold?: boolean
  gap?: number
}

const pageWidth = 595
const pageHeight = 842
const marginX = 46
const startY = 790
const lineHeight = 16

export function buildExecutiveReportPdf(
  assessment: AssessmentResponse,
  policyPack: PolicyPackResponse,
): Blob {
  const lines = buildReportLines(assessment, policyPack)
  const pages = paginate(lines)
  const objects: string[] = []

  objects.push('<< /Type /Catalog /Pages 2 0 R >>')
  objects.push(`<< /Type /Pages /Kids [${pages.map((_, index) => `${3 + index * 2} 0 R`).join(' ')}] /Count ${pages.length} >>`)

  pages.forEach((pageLines, pageIndex) => {
    const pageObjectNumber = 3 + pageIndex * 2
    const contentObjectNumber = pageObjectNumber + 1
    objects.push(
      `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight}] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> /F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> >> >> /Contents ${contentObjectNumber} 0 R >>`,
    )
    const content = buildPageContent(pageLines)
    objects.push(`<< /Length ${content.length} >>\nstream\n${content}\nendstream`)
  })

  return createPdfBlob(objects)
}

function buildReportLines(
  assessment: AssessmentResponse,
  policyPack: PolicyPackResponse,
): PdfLine[] {
  const risks = assessment.risks.slice(0, 6)
  const evidence = Array.from(
    new Set(policyPack.policies.flatMap((policy) => policy.evidence)),
  ).slice(0, 8)

  return [
    { text: 'HotelSec PolicyForge AI', size: 20, bold: true, gap: 10 },
    { text: 'Informe ejecutivo de ciberseguridad hotelera', size: 16, bold: true, gap: 18 },
    { text: `Alojamiento: ${assessment.business_name}` },
    { text: `Fecha: ${new Date().toLocaleDateString('es-ES')}` },
    { text: `Puntuacion global: ${assessment.overall_score}/100` },
    { text: `Nivel de riesgo: ${riskLabels[assessment.risk_level]}`, gap: 18 },
    { text: 'Resumen', size: 14, bold: true, gap: 8 },
    {
      text: `El analisis ha detectado ${assessment.risks.length} riesgos activos y ha generado ${policyPack.policies.length} politicas iniciales para mejorar la postura de seguridad.`,
      gap: 18,
    },
    { text: 'Puntuaciones por area', size: 14, bold: true, gap: 8 },
    ...assessment.area_scores.map((area) => ({
      text: `- ${area.area}: ${area.score}/100`,
    })),
    { text: 'Riesgos principales', size: 14, bold: true, gap: 8 },
    ...(risks.length > 0
      ? risks.map((risk) => ({
          text: `- ${risk.title} (${riskLabels[risk.severity]}): ${risk.recommendation}`,
        }))
      : [{ text: '- No se han detectado riesgos prioritarios.' }]),
    { text: 'Orden de implantacion', size: 14, bold: true, gap: 8 },
    ...policyPack.implementation_order.map((step, index) => ({
      text: `${index + 1}. ${step}`,
    })),
    { text: 'Politicas generadas', size: 14, bold: true, gap: 8 },
    ...policyPack.policies.flatMap((policy) => [
      { text: policy.name, bold: true, gap: 4 },
      { text: `Objetivo: ${policy.objective}` },
      { text: `Revision: ${policy.review_frequency}` },
    ]),
    { text: 'Evidencias recomendadas', size: 14, bold: true, gap: 8 },
    ...evidence.map((item) => ({ text: `- ${item}` })),
  ]
}

function paginate(lines: PdfLine[]): PdfLine[][] {
  const pages: PdfLine[][] = [[]]
  let y = startY

  lines.flatMap(wrapLine).forEach((line) => {
    const gap = line.gap ?? 0
    if (y - gap < 54) {
      pages.push([])
      y = startY
    }

    y -= gap
    pages[pages.length - 1].push(line)
    y -= lineHeight
  })

  return pages
}

function wrapLine(line: PdfLine): PdfLine[] {
  const maxLength = line.size && line.size >= 16 ? 58 : 86
  if (line.text.length <= maxLength) {
    return [line]
  }

  const words = line.text.split(' ')
  const lines: PdfLine[] = []
  let current = ''

  words.forEach((word) => {
    const next = current ? `${current} ${word}` : word
    if (next.length > maxLength && current) {
      lines.push({ ...line, text: current })
      current = word
    } else {
      current = next
    }
  })

  if (current) {
    lines.push({ ...line, text: current, gap: lines.length === 0 ? line.gap : 0 })
  }

  return lines
}

function buildPageContent(lines: PdfLine[]): string {
  let y = startY
  const commands: string[] = [
    'BT',
    '1 0 0 1 46 790 Tm',
    '0.12 0.16 0.22 rg',
  ]

  lines.forEach((line, index) => {
    y -= line.gap ?? 0
    const x = marginX
    const size = line.size ?? 10
    const font = line.bold ? 'F2' : 'F1'
    if (index > 0 || line.gap) {
      commands.push(`1 0 0 1 ${x} ${y} Tm`)
    }
    commands.push(`/${font} ${size} Tf`)
    commands.push(`${toPdfHexString(line.text)} Tj`)
    y -= lineHeight
  })

  commands.push('ET')
  return commands.join('\n')
}

function createPdfBlob(objects: string[]): Blob {
  const chunks = ['%PDF-1.7\n']
  const offsets = [0]

  objects.forEach((object, index) => {
    offsets.push(chunks.join('').length)
    chunks.push(`${index + 1} 0 obj\n${object}\nendobj\n`)
  })

  const xrefOffset = chunks.join('').length
  chunks.push(`xref\n0 ${objects.length + 1}\n`)
  chunks.push('0000000000 65535 f \n')
  offsets.slice(1).forEach((offset) => {
    chunks.push(`${offset.toString().padStart(10, '0')} 00000 n \n`)
  })
  chunks.push(
    `trailer\n<< /Size ${objects.length + 1} /Root 1 0 R >>\nstartxref\n${xrefOffset}\n%%EOF`,
  )

  return new Blob(chunks, { type: 'application/pdf' })
}

function toPdfHexString(value: string): string {
  const bytes = [0xfe, 0xff]
  for (const char of value) {
    const code = char.codePointAt(0) ?? 32
    bytes.push((code >> 8) & 0xff, code & 0xff)
  }

  return `<${bytes.map((byte) => byte.toString(16).padStart(2, '0')).join('')}>`
}
