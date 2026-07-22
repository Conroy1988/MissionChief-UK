import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const CRITICAL_ROUTES = [
  { path: "", heading: "MissionChief UK Command Centre" },
  { path: "tools/mission-lookup/", heading: "Mission Requirement Lookup" },
  { path: "tools/resource-comparison/", heading: "Resource and Qualification Comparison" },
  { path: "tools/fleet-planner/", heading: "Concurrent Fleet Planner" },
  { path: "tools/query-catalogue/", heading: "Natural-Language Query Catalogue" },
  { path: "reference/generated-faq/", heading: "Generated FAQ" },
  { path: "api/", heading: "MissionChief UK Static Data API" },
  { path: "releases/v1.0.0/", heading: "MissionChief UK v1.0.0" }
];

const API_FILES = [
  "manifest.json",
  "missions.json",
  "vehicles.json",
  "infrastructure.json",
  "training.json",
  "search-index.json",
  "faq.json",
  "openapi.json"
];

function runtimeFailures(page) {
  const failures = [];
  page.on("pageerror", (error) => failures.push(`pageerror: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error") failures.push(`console: ${message.text()}`);
  });
  page.on("requestfailed", (request) => {
    const url = new URL(request.url());
    if (url.hostname === "conroy1988.github.io") {
      failures.push(`request: ${request.url()} — ${request.failure()?.errorText || "failed"}`);
    }
  });
  return failures;
}

async function openPage(page, path) {
  const response = await page.goto(path, { waitUntil: "networkidle" });
  expect(response, `No navigation response for ${path}`).not.toBeNull();
  expect(response.ok(), `${path} returned HTTP ${response.status()}`).toBeTruthy();
}

for (const route of CRITICAL_ROUTES) {
  test(`${route.path || "home"} renders without runtime or viewport failures`, async ({ page }) => {
    const failures = runtimeFailures(page);
    await openPage(page, route.path);
    await expect(page.getByRole("heading", { level: 1, name: route.heading })).toBeVisible();

    const dimensions = await page.locator(".md-content").evaluate((element) => ({
      clientWidth: element.clientWidth,
      scrollWidth: element.scrollWidth
    }));
    expect(dimensions.scrollWidth, `Horizontal overflow detected on ${route.path}`).toBeLessThanOrEqual(dimensions.clientWidth + 2);
    expect(failures).toEqual([]);
  });
}

test("mission lookup loads, filters and renders mission evidence", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/mission-lookup/");
  const root = page.locator("[data-mcuk-tool='mission-lookup']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => root.locator("select[data-role='service'] option").count()).toBeGreaterThan(1);
  await expect.poll(() => root.locator("article.mcuk-tool-card").count()).toBeGreaterThan(0);

  await root.locator("input[data-role='query']").fill("588");
  await expect(root.locator("article.mcuk-tool-card")).toContainText("Aircraft Accident Code F");
  await expect(root.locator("article.mcuk-tool-card")).toContainText("#588");
  expect(failures).toEqual([]);
});

test("resource and qualification comparison switches datasets", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/resource-comparison/");
  const root = page.locator("[data-mcuk-tool='comparison']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => root.locator("select[data-role='first'] option").count()).toBeGreaterThan(1);
  await expect(root.locator("table")).toBeVisible();

  await root.locator("select[data-role='kind']").selectOption("training");
  await expect.poll(() => root.locator("select[data-role='first'] option").count()).toBeGreaterThan(1);
  await expect(root.locator("table")).toContainText("Qualification Type");
  expect(failures).toEqual([]);
});

test("fleet planner multiplies a verified mission", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/fleet-planner/");
  const root = page.locator("[data-mcuk-tool='fleet-planner']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => root.locator("select[data-role='mission'] option").count()).toBeGreaterThan(1);

  await root.locator("select[data-role='mission']").selectOption("588");
  await root.locator("input[data-role='concurrency']").fill("3");
  await expect(root.locator("[data-role='results']")).toContainText("Aircraft Accident Code F");
  await expect(root.locator("[data-role='results'] table")).toContainText("3 concurrent");
  expect(failures).toEqual([]);
});

test("query catalogue returns evidence-backed matches", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/query-catalogue/");
  const root = page.locator("[data-mcuk-tool='query-catalogue']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await root.locator("input[data-role='query']").fill("railway police officer");
  await expect.poll(() => root.locator("[data-role='results'] li").count()).toBeGreaterThan(0);
  expect(failures).toEqual([]);
});

test("MkDocs instant navigation reinitialises intelligence tools", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-desktop", "One desktop browser is sufficient for the navigation lifecycle test");
  const failures = runtimeFailures(page);
  await openPage(page, "tools/mission-lookup/");
  await expect(page.locator("[data-mcuk-tool='mission-lookup']")).toHaveAttribute("data-mcuk-ready", "true");

  await page.getByRole("link", { name: "Resource Comparison" }).first().click();
  await expect(page).toHaveURL(/\/tools\/resource-comparison\/$/);
  await expect(page.locator("[data-mcuk-tool='comparison']")).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => page.locator("[data-mcuk-tool='comparison'] select[data-role='first'] option").count()).toBeGreaterThan(1);
  expect(failures).toEqual([]);
});

test("public API collections are internally consistent", async ({ request }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-desktop", "API integrity only needs one project");
  const payloads = {};
  for (const filename of API_FILES) {
    const response = await request.get(`assets/data/v1/${filename}`);
    expect(response.ok(), `${filename} returned HTTP ${response.status()}`).toBeTruthy();
    payloads[filename] = await response.json();
  }

  const manifest = payloads["manifest.json"];
  expect(manifest.api_version).toBe("v1");
  expect(manifest.data_version).toBe("1.0.0");
  expect(manifest.stage).toBe(34);
  expect(manifest.status).toBe("production");

  let total = 0;
  for (const collection of ["missions", "vehicles", "infrastructure", "training"]) {
    const payload = payloads[`${collection}.json`];
    expect(payload.count).toBe(payload.records.length);
    expect(payload.data_version).toBe(manifest.data_version);
    expect(manifest.collections[collection].count).toBe(payload.count);
    total += payload.count;
  }
  expect(payloads["search-index.json"].count).toBe(total);
  expect(payloads["search-index.json"].records).toHaveLength(total);
  expect(payloads["faq.json"].count).toBe(payloads["faq.json"].entries.length);
  expect(payloads["openapi.json"].openapi).toBe("3.1.0");
  expect(payloads["openapi.json"].info.version).toBe(manifest.data_version);
});

test("interactive surfaces have no critical WCAG violations", async ({ page }) => {
  for (const path of ["", "tools/mission-lookup/", "tools/resource-comparison/", "tools/fleet-planner/", "tools/query-catalogue/"]) {
    await openPage(page, path);
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .analyze();
    const critical = results.violations.filter((violation) => violation.impact === "critical");
    expect(critical, `Critical accessibility violations on ${path || "home"}: ${JSON.stringify(critical, null, 2)}`).toEqual([]);
  }
});
