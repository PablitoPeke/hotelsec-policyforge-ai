import type { AssessmentResponse } from '../api/assessment'
import type { PolicyPackResponse } from '../api/policies'
import { riskLabels } from '../data/assessmentDefaults'

type PdfPage = {
  commands: string[]
}

type TextOptions = {
  bold?: boolean
  color?: string
  size?: number
}

const pageWidth = 595
const pageHeight = 842
const margin = 44
const contentWidth = pageWidth - margin * 2
const bottomLimit = 62

export function buildExecutiveReportPdf(
  assessment: AssessmentResponse,
  policyPack: PolicyPackResponse,
): Blob {
  const pages: PdfPage[] = []
  let page = createPage()
  pages.push(page)

  drawCoverHeader(page, assessment)
  let y = 676
  y = drawScoreCards(page, assessment, policyPack, y)
  y = drawSection(page, y, 'Resumen ejecutivo')
  y = drawParagraph(
    pages,
    page,
    y,
    `El alojamiento ${assessment.business_name} obtiene una puntuacion global de ${assessment.overall_score}/100 y un nivel de riesgo ${riskLabels[assessment.risk_level]}. El analisis ha detectado ${assessment.risks.length} riesgos activos y ha generado ${policyPack.policies.length} politicas iniciales para priorizar la mejora de seguridad.`,
  ).y
  page = pages[pages.length - 1]

  y = drawSection(page, y - 8, 'Puntuaciones por area')
  assessment.area_scores.forEach((area) => {
    const result = ensureSpace(pages, page, y, 34)
    page = result.page
    y = result.y
    drawText(page, `${area.area}`, margin, y, { bold: true, size: 10 })
    drawProgressBar(page, margin + 210, y - 7, 230, area.score)
    drawText(page, `${area.score}/100`, margin + 455, y, { bold: true, size: 10 })
    y -= 24
  })

  y = drawSection(page, y - 8, 'Riesgos principales')
  const risks = assessment.risks.slice(0, 8)
  if (risks.length === 0) {
    const result = drawParagraph(
      pages,
      page,
      y,
      'No se han detectado riesgos prioritarios con las reglas actuales.',
    )
    page = result.page
    y = result.y
  } else {
    risks.forEach((risk) => {
      const result = drawBullet(
        pages,
        page,
        y,
        `${risk.title} (${riskLabels[risk.severity]}): ${risk.recommendation}`,
      )
      page = result.page
      y = result.y
    })
  }

  y = drawSection(page, y - 8, 'Orden de implantacion recomendado')
  policyPack.implementation_order.forEach((step, index) => {
    const result = drawBullet(pages, page, y, `${index + 1}. ${step}`)
    page = result.page
    y = result.y
  })

  y = drawSection(page, y - 8, 'Politicas generadas')
  policyPack.policies.forEach((policy) => {
    let result = ensureSpace(pages, page, y, 78)
    page = result.page
    y = result.y
    drawRoundedCard(page, margin, y - 58, contentWidth, 64)
    drawText(page, policy.name, margin + 14, y - 12, {
      bold: true,
      color: '0.06 0.35 0.32',
      size: 11,
    })
    drawText(page, `Objetivo: ${policy.objective}`, margin + 14, y - 30, { size: 9 })
    drawText(page, `Revision: ${policy.review_frequency}`, margin + 14, y - 46, {
      color: '0.39 0.45 0.55',
      size: 9,
    })
    y -= 78
  })

  y = drawSection(page, y - 8, 'Evidencias recomendadas')
  const evidence = Array.from(
    new Set(policyPack.policies.flatMap((policy) => policy.evidence)),
  ).slice(0, 10)
  evidence.forEach((item) => {
    const result = drawBullet(pages, page, y, item)
    page = result.page
    y = result.y
  })

  pages.forEach((pdfPage, index) => drawFooter(pdfPage, index + 1, pages.length))

  return createPdfBlob(pages)
}

function createPage(): PdfPage {
  return { commands: [] }
}

function drawCoverHeader(page: PdfPage, assessment: AssessmentResponse) {
  drawRect(page, 0, 742, pageWidth, 100, '0.06 0.16 0.26')
  drawRect(page, 0, 742, pageWidth, 6, '0.08 0.72 0.65')
  drawText(page, 'HotelSec PolicyForge AI', margin, 800, {
    bold: true,
    color: '1 1 1',
    size: 21,
  })
  drawText(page, 'Informe ejecutivo de ciberseguridad hotelera', margin, 774, {
    color: '0.86 0.95 0.98',
    size: 13,
  })
  drawText(page, `Cliente: ${assessment.business_name}`, margin, 724, {
    bold: true,
    color: '0.12 0.16 0.22',
    size: 12,
  })
  drawText(page, `Fecha: ${new Date().toLocaleDateString('es-ES')}`, margin, 706, {
    color: '0.39 0.45 0.55',
    size: 10,
  })
}

function drawScoreCards(
  page: PdfPage,
  assessment: AssessmentResponse,
  policyPack: PolicyPackResponse,
  y: number,
) {
  const cardWidth = (contentWidth - 24) / 3
  const cards = [
    ['Puntuacion global', `${assessment.overall_score}/100`],
    ['Nivel de riesgo', riskLabels[assessment.risk_level]],
    ['Politicas generadas', `${policyPack.policies.length}`],
  ]

  cards.forEach(([label, value], index) => {
    const x = margin + index * (cardWidth + 12)
    drawRect(page, x, y - 62, cardWidth, 62, '0.96 0.98 0.99', '0.83 0.88 0.93')
    drawText(page, label, x + 14, y - 22, { color: '0.39 0.45 0.55', size: 9 })
    drawText(page, value, x + 14, y - 45, { bold: true, size: 18 })
  })

  return y - 92
}

function drawSection(page: PdfPage, y: number, title: string) {
  drawRect(page, margin, y - 3, 30, 3, '0.08 0.72 0.65')
  drawText(page, title, margin, y - 22, {
    bold: true,
    color: '0.12 0.16 0.22',
    size: 14,
  })
  return y - 44
}

function drawParagraph(
  pages: PdfPage[],
  currentPage: PdfPage,
  startY: number,
  text: string,
) {
  let page = currentPage
  let y = startY
  wrapText(text, 94).forEach((line) => {
    const result = ensureSpace(pages, page, y, 16)
    page = result.page
    y = result.y
    drawText(page, line, margin, y, { color: '0.26 0.32 0.41', size: 10 })
    y -= 15
  })

  return { page, y: y - 8 }
}

function drawBullet(
  pages: PdfPage[],
  currentPage: PdfPage,
  startY: number,
  text: string,
) {
  let page = currentPage
  let y = startY
  const lines = wrapText(text, 88)
  lines.forEach((line, index) => {
    const result = ensureSpace(pages, page, y, 16)
    page = result.page
    y = result.y
    drawText(page, index === 0 ? '-' : ' ', margin, y, { bold: true, size: 10 })
    drawText(page, line, margin + 14, y, { color: '0.26 0.32 0.41', size: 10 })
    y -= 15
  })
  return { page, y: y - 3 }
}

function ensureSpace(
  pages: PdfPage[],
  currentPage: PdfPage,
  y: number,
  requiredHeight: number,
) {
  if (y - requiredHeight > bottomLimit) {
    return { page: currentPage, y }
  }

  const page = createPage()
  pages.push(page)
  drawRect(page, 0, 808, pageWidth, 34, '0.06 0.16 0.26')
  drawText(page, 'HotelSec PolicyForge AI', margin, 822, {
    bold: true,
    color: '1 1 1',
    size: 12,
  })
  return { page, y: 770 }
}

function drawProgressBar(page: PdfPage, x: number, y: number, width: number, score: number) {
  drawRect(page, x, y, width, 8, '0.88 0.92 0.95')
  drawRect(page, x, y, Math.max(4, (width * score) / 100), 8, progressColor(score))
}

function drawRoundedCard(page: PdfPage, x: number, y: number, width: number, height: number) {
  drawRect(page, x, y, width, height, '0.97 0.99 0.99', '0.83 0.88 0.93')
}

function drawFooter(page: PdfPage, pageNumber: number, totalPages: number) {
  drawRect(page, margin, 42, contentWidth, 1, '0.83 0.88 0.93')
  drawText(page, 'Informe generado automaticamente por HotelSec PolicyForge AI', margin, 26, {
    color: '0.39 0.45 0.55',
    size: 8,
  })
  drawText(page, `Pagina ${pageNumber} de ${totalPages}`, pageWidth - 112, 26, {
    color: '0.39 0.45 0.55',
    size: 8,
  })
}

function drawText(page: PdfPage, text: string, x: number, y: number, options: TextOptions = {}) {
  const font = options.bold ? 'F2' : 'F1'
  const size = options.size ?? 10
  const color = options.color ?? '0.12 0.16 0.22'
  page.commands.push('BT')
  page.commands.push(`${color} rg`)
  page.commands.push(`/${font} ${size} Tf`)
  page.commands.push(`1 0 0 1 ${x} ${y} Tm`)
  page.commands.push(`(${escapePdfText(normalizeText(text))}) Tj`)
  page.commands.push('ET')
}

function drawRect(
  page: PdfPage,
  x: number,
  y: number,
  width: number,
  height: number,
  fillColor: string,
  strokeColor?: string,
) {
  page.commands.push('q')
  page.commands.push(`${fillColor} rg`)
  if (strokeColor) {
    page.commands.push(`${strokeColor} RG`)
    page.commands.push(`${x} ${y} ${width} ${height} re B`)
  } else {
    page.commands.push(`${x} ${y} ${width} ${height} re f`)
  }
  page.commands.push('Q')
}

function wrapText(text: string, maxLength: number) {
  const words = normalizeText(text).split(' ')
  const lines: string[] = []
  let current = ''

  words.forEach((word) => {
    const next = current ? `${current} ${word}` : word
    if (next.length > maxLength && current) {
      lines.push(current)
      current = word
    } else {
      current = next
    }
  })

  if (current) {
    lines.push(current)
  }

  return lines
}

function progressColor(score: number) {
  if (score >= 80) {
    return '0.08 0.72 0.65'
  }
  if (score >= 50) {
    return '0.96 0.62 0.04'
  }
  return '0.70 0.13 0.09'
}

function createPdfBlob(pages: PdfPage[]): Blob {
  const objects: string[] = []
  objects.push('<< /Type /Catalog /Pages 2 0 R >>')
  objects.push(`<< /Type /Pages /Kids [${pages.map((_, index) => `${3 + index * 2} 0 R`).join(' ')}] /Count ${pages.length} >>`)

  pages.forEach((page, index) => {
    const pageObjectNumber = 3 + index * 2
    const contentObjectNumber = pageObjectNumber + 1
    const content = page.commands.join('\n')
    objects.push(
      `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${pageWidth} ${pageHeight}] /Resources << /Font << /F1 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica >> /F2 << /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >> >> >> /Contents ${contentObjectNumber} 0 R >>`,
    )
    objects.push(`<< /Length ${content.length} >>\nstream\n${content}\nendstream`)
  })

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

function normalizeText(text: string) {
  return text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^\x20-\x7E]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
}

function escapePdfText(text: string) {
  return text.replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)')
}
