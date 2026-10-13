import { test, expect, type Page, type APIRequestContext } from '@playwright/test'
import { randomBytes } from 'node:crypto'
import { mkdirSync, readFileSync } from 'node:fs'
import { resolve } from 'node:path'

const evidence = resolve(
  process.env.E2E_EVIDENCE_DIR ?? '../docs/practica3/evidence/account-center-local',
)
mkdirSync(evidence, { recursive: true })
const accounts = new WeakMap<Page, { email: string; password: string; origin: string }>()

async function createAccount(page: Page, baseURL: string) {
  const account = {
    email: `account-${randomBytes(8).toString('hex')}@example.org`,
    password: randomBytes(24).toString('base64url'),
    origin: new URL(baseURL).origin,
  }
  const response = await page.request.post('/api/v1/auth/register', {
    data: { email: account.email, password: account.password, name: 'Cuenta de prueba' },
    headers: { Origin: account.origin },
  })
  expect(response.status()).toBe(201)
  accounts.set(page, account)
  await page.goto('/')
  await page.getByRole('button', { name: 'Mi cuenta', exact: true }).click()
  await expect(
    page.getByRole('button', { name: 'Cambiar correo', exact: true }),
  ).toBeDisabled()
  return account
}

test.afterEach(async ({ page }) => {
  const account = accounts.get(page)
  if (!account) return
  let response = await page.request.get('/api/v1/auth/me')
  if (response.status() === 401) {
    response = await page.request.post('/api/v1/auth/login', {
      data: { email: account.email, password: account.password },
      headers: { Origin: account.origin },
    })
  }
  expect(response.ok()).toBe(true)
  const session = await response.json()
  const deleted = await page.request.delete('/api/v1/auth/account', {
    data: { password: account.password },
    headers: { Origin: account.origin, 'X-CSRF-Token': session.csrf_token },
  })
  expect(deleted.status(), 'Delete only the temporary account created by this test').toBe(
    204,
  )
  accounts.delete(page)
})

test('perfil persistente, contrasena, revocacion, exportacion y modal accesible', async ({
  page,
  baseURL,
  playwright,
}) => {
  await page.setViewportSize({ width: 1440, height: 1000 })
  const account = await createAccount(page, baseURL!)
  await page
    .getByLabel('Nombre y apellidos', { exact: true })
    .fill('Cliente Demostracion')
  await page.getByLabel('Organizacion', { exact: true }).fill('Hotel Prueba Lanzarote')
  await page.getByLabel('Cargo', { exact: true }).fill('Responsable de seguridad')
  await page.getByRole('button', { name: 'Guardar cambios', exact: true }).click()
  await expect(page.getByRole('status')).toContainText('Datos guardados')
  await expect(page.getByLabel('Correo de acceso')).toHaveAttribute('readonly', '')
  await page.reload()
  await page.getByRole('button', { name: 'Mi cuenta', exact: true }).click()
  await expect(page.getByLabel('Organizacion', { exact: true })).toHaveValue(
    'Hotel Prueba Lanzarote',
  )
  await page.screenshot({
    path: resolve(evidence, '08_cuenta_perfil.png'),
    fullPage: true,
  })

  async function otherSession(): Promise<APIRequestContext> {
    const context = await playwright.request.newContext({
      baseURL,
      extraHTTPHeaders: { Origin: account.origin },
    })
    const login = await context.post('/api/v1/auth/login', {
      data: { email: account.email, password: account.password },
    })
    expect(login.status()).toBe(200)
    return context
  }
  const other = await otherSession()
  try {
    await page.getByRole('tab', { name: 'Seguridad', exact: true }).click()
    await page.getByLabel('Contrasena actual', { exact: true }).fill('Incorrecta-123456')
    const nextPassword = randomBytes(24).toString('base64url')
    await page.getByLabel('Nueva contrasena', { exact: true }).fill(nextPassword)
    await page.getByLabel('Repetir nueva contrasena', { exact: true }).fill(nextPassword)
    await page.getByRole('button', { name: 'Actualizar contrasena', exact: true }).click()
    await expect(page.getByRole('alert')).toContainText('no es correcta')
    await page.getByLabel('Contrasena actual', { exact: true }).fill(account.password)
    const changed = page.waitForResponse(
      (response) =>
        response.url().endsWith('/api/v1/auth/password') &&
        response.request().method() === 'POST',
    )
    await page.getByRole('button', { name: 'Actualizar contrasena', exact: true }).click()
    expect((await changed).status()).toBe(200)
    account.password = nextPassword
    await expect(page.getByRole('status')).toContainText('Contrasena actualizada')
    expect((await other.get('/api/v1/auth/me')).status()).toBe(401)
  } finally {
    await other.dispose()
  }
  const second = await otherSession()
  try {
    await page.getByRole('button', { name: 'Actualizar sesiones', exact: true }).click()
    await page
      .getByLabel('Contrasena para cerrar otras sesiones', { exact: true })
      .fill(account.password)
    await page.getByRole('button', { name: 'Cerrar otras sesiones', exact: true }).click()
    await expect(page.getByRole('status')).toContainText('otras sesiones se han cerrado')
    expect((await second.get('/api/v1/auth/me')).status()).toBe(401)
    await expect(page.locator('.account-session')).toHaveCount(1)
  } finally {
    await second.dispose()
  }
  await page.screenshot({
    path: resolve(evidence, '09_cuenta_seguridad.png'),
    fullPage: true,
  })
  await page.getByRole('tab', { name: 'Actividad', exact: true }).click()
  await expect(
    page.getByRole('cell', { name: 'Contrasena cambiada', exact: true }),
  ).toBeVisible()
  await page.getByRole('tab', { name: 'Mis datos', exact: true }).click()
  await page
    .getByLabel('Contrasena para exportar', { exact: true })
    .fill(account.password)
  const download = page.waitForEvent('download')
  await page.getByRole('button', { name: 'Descargar mis datos', exact: true }).click()
  const downloaded = await download
  expect(downloaded.suggestedFilename()).toBe('hotelsec-mis-datos.json')
  const exported = JSON.parse(readFileSync((await downloaded.path())!, 'utf8'))
  expect(exported.profile.name).toBe('Cliente Demostracion')
  expect(exported.profile.organization_name).toBe('Hotel Prueba Lanzarote')
  expect(exported.profile.email).toBe(account.email)
  expect(JSON.stringify(exported)).not.toMatch(/password_hash|csrf_token|token_hash/)
  await expect(page.getByRole('status')).toContainText('Descarga de datos preparada')
  await page
    .getByLabel('Contrasena para eliminar la cuenta', { exact: true })
    .fill(account.password)
  await page.getByLabel('Confirmacion: ELIMINAR', { exact: true }).fill('ELIMINAR')
  await page.getByRole('button', { name: 'Eliminar mi cuenta', exact: true }).click()
  const dialog = page.getByRole('dialog')
  await expect(dialog).toBeVisible()
  expect(
    await dialog.evaluate((element) => element.contains(document.activeElement)),
  ).toBe(true)
  await page.keyboard.press('Tab')
  expect(
    await dialog.evaluate((element) => element.contains(document.activeElement)),
  ).toBe(true)
  await page.keyboard.press('Escape')
  await expect(dialog).not.toBeVisible()
  expect((await page.request.get('/api/v1/auth/me')).status()).toBe(200)
})

test('cuenta movil sin desbordamiento y navegacion por teclado', async ({
  page,
  baseURL,
}) => {
  await page.setViewportSize({ width: 390, height: 844 })
  await createAccount(page, baseURL!)
  await page
    .getByLabel('Nombre y apellidos', { exact: true })
    .fill('Responsable de Ciberseguridad del Hotel de Demostracion')
  await page.getByRole('button', { name: 'Guardar cambios', exact: true }).click()
  await expect(page.getByRole('status')).toContainText('Datos guardados')
  await page.getByRole('tab', { name: 'Perfil', exact: true }).focus()
  await page.keyboard.press('ArrowRight')
  await expect(page.getByRole('tab', { name: 'Seguridad', exact: true })).toBeFocused()
  await expect(page.getByRole('tab', { name: 'Seguridad', exact: true })).toHaveAttribute(
    'aria-selected',
    'true',
  )
  expect(
    await page.evaluate(() => document.documentElement.scrollWidth > innerWidth),
  ).toBe(false)
  await page.screenshot({
    path: resolve(evidence, '10_cuenta_movil.png'),
    fullPage: true,
  })
})

test('recuperacion desactivada y enlace invalido sin exponer token', async ({ page }) => {
  await page.goto('/')
  await page.getByRole('button', { name: 'Recuperar acceso', exact: true }).click()
  await expect(
    page.getByText('La recuperacion por correo no esta disponible.'),
  ).toBeVisible()
  await expect(
    page.getByRole('button', { name: 'Solicitar enlace', exact: true }),
  ).toBeDisabled()
  const fakeToken = 'ficticio-sin-validez-012345678901234567890123'
  await page.goto(`/#account_token=${fakeToken}&purpose=verify_email`)
  await expect(page).toHaveURL(/\/$/)
  await expect(page.getByText(fakeToken)).toHaveCount(0)
  await page.getByRole('button', { name: 'Confirmar correo', exact: true }).click()
  await expect(page.getByRole('alert')).toContainText(/enlace/i)
})
