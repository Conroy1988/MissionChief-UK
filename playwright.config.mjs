import { defineConfig, devices } from "@playwright/test";

const baseURL = process.env.MCUK_BASE_URL || "https://conroy1988.github.io/MissionChief-UK/";

export default defineConfig({
  testDir: "tests/e2e",
  timeout: 45_000,
  expect: {
    timeout: 12_000
  },
  fullyParallel: true,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI
    ? [["line"], ["html", { open: "never", outputFolder: "playwright-report" }]]
    : [["list"], ["html", { open: "never", outputFolder: "playwright-report" }]],
  use: {
    baseURL,
    actionTimeout: 12_000,
    navigationTimeout: 30_000,
    ignoreHTTPSErrors: false,
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    video: "retain-on-failure"
  },
  outputDir: "test-results",
  projects: [
    {
      name: "chromium-desktop",
      use: { ...devices["Desktop Chrome"] }
    },
    {
      name: "firefox-desktop",
      use: { ...devices["Desktop Firefox"] }
    },
    {
      name: "webkit-iphone",
      use: { ...devices["iPhone 13"] }
    },
    {
      name: "webkit-ipad",
      use: { ...devices["iPad Pro 11"] }
    }
  ]
});
