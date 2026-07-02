// playwright.config.js
// Konfigurasi Playwright untuk Lab Session 15

const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
    testDir: './tests/e2e',
    timeout: 60000,
    expect: {
        timeout: 15000,
    },
    reporter: [
        ['list'],
        ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ],
    use: {
        browserName: 'chromium',
        headless: true,
        viewport: { width: 1280, height: 720 },
        actionTimeout: 15000,
        navigationTimeout: 30000,
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
        trace: 'retain-on-failure',
    },
});