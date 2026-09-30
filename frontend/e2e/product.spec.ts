import { test, expect } from '@playwright/test'
import { mkdirSync } from 'node:fs'
import { resolve } from 'node:path'

const evidence = resolve('../docs/practica3/evidence')
mkdirSync(evidence, { recursive: true })
async function register(page: import('@playwright/test').Page, label: string) {
  await page.goto('/')
  await page.getByRole('button', { name: 'Crear cuenta', exact: true }).click()
  await page.getByLabel('Nombre', { exact: true }).fill(label)
  await page
    .getByLabel('Correo electronico')
    .fill(`e2e-${Date.now()}-${label.toLowerCase()}@example.org`)
  await page.getByLabel('Contrasena', { exact: true }).fill('Demostracion-2026!')
  await page.getByRole('button', { name: 'Crear cuenta', exact: true }).last().click()
  await expect(
    page.getByRole('heading', { name: 'Dashboard', exact: true }),
  ).toBeVisible()
}
async function detailFigure(
  page: import('@playwright/test').Page,
  selector: string,
  name: string,
) {
  await page.setViewportSize({ width: 1000, height: 900 })
  await page
    .locator(selector)
    .first()
    .screenshot({ path: resolve(evidence, name) })
  await page.setViewportSize({ width: 1440, height: 1000 })
}
test('registro, analisis, historial persistente, plan y PDF', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 1000 })
  await register(page, 'Demostracion')
  await page.getByRole('button', { name: 'Nuevo analisis', exact: true }).last().click()
  await page.getByLabel('Nombre del alojamiento').fill('Hotel Prueba Lanzarote')
  await page
    .getByLabel('Sistemas (separados por comas)')
    .fill('PMS cloud, Microsoft 365, TPV')
  await page.getByLabel('Categorias de datos').fill('Reservas, facturacion')
  await page.getByRole('combobox', { name: /Plan de continuidad/ }).selectOption('false')
  await page.screenshot({ path: resolve(evidence, '01_formulario.png'), fullPage: true })
  await page.screenshot({ path: resolve(evidence, '01_formulario_vista.png') })
  await detailFigure(page, '.assessment-form > .form-grid', '01_formulario_detalle.png')
  await page.getByRole('button', { name: 'Analizar y guardar', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Dashboard', exact: true }),
  ).toBeVisible()
  await expect(page.getByText('Hotel Prueba Lanzarote').first()).toBeVisible()
  await page.screenshot({ path: resolve(evidence, '02_dashboard.png'), fullPage: true })
  await page.screenshot({ path: resolve(evidence, '02_dashboard_vista.png') })
  await detailFigure(page, '.metric-grid', '02_dashboard_detalle.png')
  await page.getByRole('button', { name: 'Plan de mejora', exact: true }).click()
  await page.locator('.action-row select').first().selectOption('done')
  await expect(page.locator('.action-row select').first()).toHaveValue('done')
  await expect(page.getByText(/1 de .* completadas/)).toBeVisible()
  await page.reload()
  await page.getByRole('button', { name: 'Historial', exact: true }).click()
  await expect(
    page.getByRole('cell', { name: 'Hotel Prueba Lanzarote', exact: true }),
  ).toBeVisible()
  await page.screenshot({ path: resolve(evidence, '03_historial.png'), fullPage: true })
  await detailFigure(page, '.table-scroll', '03_historial_detalle.png')
  await page
    .getByRole('button', { name: 'Abrir Hotel Prueba Lanzarote', exact: true })
    .click()
  await page.getByRole('button', { name: 'Plan de mejora', exact: true }).click()
  await expect(page.locator('.action-row select').first()).toHaveValue('done')
  await page.screenshot({ path: resolve(evidence, '04_plan.png'), fullPage: true })
  await page.screenshot({ path: resolve(evidence, '04_plan_vista.png') })
  await detailFigure(page, '.action-row', '04_plan_detalle.png')
  await page.getByRole('button', { name: 'Informe', exact: true }).click()
  const download = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Descargar informe PDF', exact: true }).click()
  const file = await download
  expect(file.suggestedFilename()).toMatch(/\.pdf$/)
  await file.saveAs(resolve(evidence, 'informe_ejemplo.pdf'))
  await page.getByRole('button', { name: 'Reevaluar alojamiento', exact: true }).click()
  await page.getByLabel('Usa doble factor', { exact: true }).check()
  await page.getByRole('button', { name: 'Analizar y guardar', exact: true }).click()
  await expect(page.getByText(/Variacion respecto/)).toBeVisible()
  await page.getByRole('button', { name: 'Politicas', exact: true }).click()
  await expect(page.locator('.policy-item')).toHaveCount(10)
  await page.screenshot({ path: resolve(evidence, '05_politicas.png'), fullPage: true })
  await page.screenshot({ path: resolve(evidence, '05_politicas_vista.png') })
  await detailFigure(page, '.policy-item', '05_politicas_detalle.png')
  await page.getByRole('button', { name: 'Mi cuenta', exact: true }).click()
  await expect(
    page.getByRole('cell', { name: 'record.created', exact: true }).first(),
  ).toBeVisible()
})
test('movil y contradiccion confirmada antes de guardar', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await register(page, 'Movil')
  await page.getByRole('button', { name: 'Nuevo analisis', exact: true }).last().click()
  await page.getByLabel('Usa doble factor', { exact: true }).check()
  await page
    .getByLabel('Contexto adicional', { exact: true })
    .fill('No usamos MFA y no hacemos copias.')
  await page.getByRole('button', { name: 'Analizar y guardar', exact: true }).click()
  await expect(page.getByRole('dialog')).toBeVisible()
  await expect(page.getByText('uses_mfa: formulario true, texto false')).toBeVisible()
  await page.screenshot({
    path: resolve(evidence, '06_conflicto_movil.png'),
    fullPage: true,
  })
  await page.screenshot({ path: resolve(evidence, '06_conflicto_vista.png') })
  await page
    .getByRole('dialog')
    .screenshot({ path: resolve(evidence, '06_conflicto_detalle.png') })
  await page.getByRole('button', { name: 'Usar texto', exact: true }).click()
  await expect(
    page.getByRole('heading', { name: 'Dashboard', exact: true }),
  ).toBeVisible()
  const overflow = await page.evaluate(
    () => document.documentElement.scrollWidth > window.innerWidth,
  )
  expect(overflow).toBe(false)
  await page.screenshot({
    path: resolve(evidence, '07_dashboard_movil.png'),
    fullPage: true,
  })
})
