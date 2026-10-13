import { defineConfig } from '@playwright/test'
export default defineConfig({
  testDir: './e2e',
  outputDir: 'test-results/artifacts',
  workers: 1,
  timeout: 60000,
  use: {
    baseURL: process.env.E2E_URL ?? 'http://localhost:8085',
    trace: 'retain-on-failure',
  },
  reporter: [
    ['list'],
    ['json', { outputFile: process.env.E2E_RESULTS_FILE ?? 'test-results/results.json' }],
  ],
})
