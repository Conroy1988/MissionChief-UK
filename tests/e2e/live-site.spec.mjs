import { readFileSync } from "node:fs";
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

const RELEASE = JSON.parse(
  readFileSync(new URL("../../data/version.json", import.meta.url), "utf8")
);
const RELEASE_VERSION = RELEASE.version;

const CRITICAL_ROUTES = [
  { path: "", heading: "MissionChief UK" },
  { path: "getting-started/", heading: "Getting Started" },
  { path: "getting-started/first-expansion/", heading: "First Expansion" },
  { path: "systems/", heading: "Game Systems" },
  { path: "systems/missions-and-dispatching/", heading: "Missions and Dispatching" },
  { path: "systems/buildings-and-extensions/", heading: "Buildings and Extensions" },
  { path: "services/", heading: "Emergency Services" },
  { path: "services/fire-and-rescue/", heading: "Fire and Rescue Operational Progression" },
  { path: "services/ambulance/", heading: "Ambulance and HART Operational Progression" },
  { path: "services/police/", heading: "Police and Public Safety Operational Progression" },
  { path: "services/coastguard-and-lifeboat/", heading: "Coastguard and Lifeboat Operational Progression" },
  { path: "services/mountain-rescue/", heading: "Mountain Rescue Operational Progression" },
  { path: "services/search-and-rescue/", heading: "Search and Rescue HQ Operational Progression" },
  { path: "services/bomb-disposal/", heading: "Bomb Disposal and EOD Operational Progression" },
  { path: "services/airfield-operations/", heading: "Airfield Operations Operational Progression" },
  { path: "services/recovery/", heading: "Recovery and HGV Recovery Operational Progression" },
  { path: "services/railway-response/", heading: "Railway Police and Railway Fire Operational Progression" },
  { path: "strategy/", heading: "Strategy Command Centre" },
  { path: "strategy/account-progression/", heading: "Cross-Service Account Progression" },
  { path: "strategy/station-placement/", heading: "Station Placement and Coverage" },
  { path: "alliances/", heading: "Alliance Operations" },
  { path: "tools/mission-lookup/", heading: "Mission Requirement Lookup" },
  { path: "tools/resource-comparison/", heading: "Resource and Qualification Comparison" },
  { path: "tools/fleet-planner/", heading: "Concurrent Fleet Planner" },
  { path: "tools/account-readiness/", heading: "Account Readiness Planner" },
  { path: "tools/query-catalogue/", heading: "Natural-Language Query Catalogue" },
  { path: "reference/generated-faq/", heading: "Generated FAQ" },
  { path: "api/", heading: "MissionChief UK Static Data API" },
  { path: "quality-assurance/", heading: "Quality Assurance" },
  { path: `releases/v${RELEASE_VERSION}/`, heading: `MissionChief UK v${RELEASE_VERSION}` }
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

const FIRST_PARTY_HOSTNAMES = new Set(["conroy1988.github.io", "127.0.0.1", "localhost"]);

function isFirstParty(url) {
  try {
    return FIRST_PARTY_HOSTNAMES.has(new URL(url).hostname);
  } catch {
    return false;
  }
}

function isIgnorableBrowserRequest(url) {
  try {
    return new URL(url).pathname.endsWith("/favicon.ico");
  } catch {
    return false;
  }
}

function isExpectedNavigationCancellation(request) {
  const errorText = request.failure()?.errorText || "";
  return request.resourceType() === "document"
    && (errorText.includes("NS_BINDING_ABORTED") || errorText.includes("ERR_ABORTED"));
}

function runtimeFailures(page) {
  const failures = [];
  page.on("pageerror", (error) => failures.push(`pageerror: ${error.message}`));
  page.on("console", (message) => {
    if (message.type() === "error" && !message.text().startsWith("Failed to load resource")) {
      failures.push(`console: ${message.text()}`);
    }
  });
  page.on("response", (response) => {
    if (isFirstParty(response.url()) && !isIgnorableBrowserRequest(response.url()) && response.status() >= 400) {
      failures.push(`response: ${response.url()} — HTTP ${response.status()}`);
    }
  });
  page.on("requestfailed", (request) => {
    if (
      isFirstParty(request.url())
      && !isIgnorableBrowserRequest(request.url())
      && !isExpectedNavigationCancellation(request)
    ) {
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

    const dimensions = await page.locator(".md-content").evaluate((element) => {
      const contentRect = element.getBoundingClientRect();
      const offenders = [...element.querySelectorAll("*")]
        .map((candidate) => {
          const rect = candidate.getBoundingClientRect();
          const style = getComputedStyle(candidate);
          return {
            tag: candidate.tagName.toLowerCase(),
            id: candidate.id,
            className: typeof candidate.className === "string" ? candidate.className : "",
            role: candidate.getAttribute("data-role"),
            right: Math.round(rect.right),
            width: Math.round(rect.width),
            clientWidth: candidate.clientWidth,
            scrollWidth: candidate.scrollWidth,
            overflowX: style.overflowX,
            minWidth: style.minWidth,
            maxWidth: style.maxWidth,
            whiteSpace: style.whiteSpace,
            text: (candidate.textContent || "").trim().slice(0, 80)
          };
        })
        .filter((candidate) =>
          candidate.right > contentRect.right + 2
          || candidate.scrollWidth > candidate.clientWidth + 2
        )
        .sort((left, right) =>
          Math.max(right.right - contentRect.right, right.scrollWidth - right.clientWidth)
          - Math.max(left.right - contentRect.right, left.scrollWidth - left.clientWidth)
        )
        .slice(0, 12);
      return {
        clientWidth: element.clientWidth,
        scrollWidth: element.scrollWidth,
        offenders
      };
    });
    expect(
      dimensions.scrollWidth,
      `Horizontal overflow detected on ${route.path}: ${JSON.stringify(dimensions.offenders)}`
    ).toBeLessThanOrEqual(dimensions.clientWidth + 2);
    expect(failures).toEqual([]);
  });
}

test("long service pages expose accessible section navigation", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "services/ambulance/");
  const details = page.locator("details.mcuk-page-sections");
  await expect(details).toBeVisible();
  await expect(details.locator("summary")).toContainText("Page sections");
  await details.locator("summary").click();
  const links = details.getByRole("link");
  await expect.poll(() => links.count()).toBeGreaterThan(3);
  const firstHref = await links.first().getAttribute("href");
  expect(firstHref).toMatch(/^#/);
  await links.first().click();
  await expect(page).toHaveURL(/#.+$/);
  expect(failures).toEqual([]);
});

test("Command Centre remains free of generated page-section navigation", async ({ page }) => {
  await openPage(page, "");
  await expect(page.locator("details.mcuk-page-sections")).toHaveCount(0);
});

test("mission lookup loads, filters and renders mission evidence", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/mission-lookup/");
  const root = page.locator("[data-mcuk-tool='mission-lookup']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => root.locator("select[data-role='service'] option").count()).toBeGreaterThan(1);
  await expect.poll(() => root.locator("article.mcuk-tool-card").count()).toBeGreaterThan(0);

  await root.locator("input[data-role='query']").fill("588");
  await expect(root.locator("article.mcuk-tool-card")).toContainText("Aircraft Accident - Code F");
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
  await expect(root.locator("[data-role='results']")).toContainText("Aircraft Accident - Code F");
  await expect(root.locator("[data-role='results'] table")).toContainText("3 concurrent");
  expect(failures).toEqual([]);
});

test("account readiness calculates reserve cover and persists a local scenario", async ({ page }) => {
  const failures = runtimeFailures(page);
  await openPage(page, "tools/account-readiness/");
  const root = page.locator("[data-mcuk-tool='account-readiness']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect.poll(() => root.locator("select[data-role='mission'] option").count()).toBeGreaterThan(1);

  await root.locator("select[data-role='mission']").selectOption("0");
  await root.locator("button[data-action='add-mission']").click();
  const fireEngineRow = root.locator("tr[data-resource-id='fire_engine']");
  await expect(fireEngineRow).toBeVisible();
  await fireEngineRow.locator("input[data-field='dispatchable']").fill("2");
  await fireEngineRow.locator("input[data-field='reserve']").fill("1");
  await expect(root.locator("[data-role='summary']")).toContainText("Ready");

  await root.locator("input[data-role='scenario-name']").fill("Playwright readiness");
  await root.locator("button[data-action='save-local']").click();
  await expect(root.locator("[data-role='storage-status']")).toContainText("Saved");
  await root.locator("button[data-action='clear-current']").click();
  await expect(root.locator("[data-role='scenario']")).toContainText("No missions selected");
  await root.locator("select[data-role='saved-scenarios']").selectOption("Playwright readiness");
  await root.locator("button[data-action='load-local']").click();
  await expect(root.locator("[data-role='scenario']")).toContainText("Bin fire");
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

test("MkDocs instant navigation reinitialises page and intelligence enhancements", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "chromium-desktop", "One desktop browser is sufficient for the navigation lifecycle test");
  const failures = runtimeFailures(page);
  await openPage(page, "services/ambulance/");
  await expect(page.locator("details.mcuk-page-sections")).toBeVisible();

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
  expect(manifest.data_version).toBe(RELEASE_VERSION);
  expect(manifest.stage).toBe(RELEASE.stage);
  expect(manifest.status).toBe(RELEASE.status);

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

test("interactive and command surfaces have no critical WCAG violations", async ({ page }) => {
  const paths = [
    "",
    "getting-started/",
    "systems/missions-and-dispatching/",
    "services/ambulance/",
    "strategy/account-progression/",
    "alliances/",
    "tools/mission-lookup/",
    "tools/resource-comparison/",
    "tools/fleet-planner/",
    "tools/account-readiness/",
    "tools/query-catalogue/"
  ];
  for (const path of paths) {
    await openPage(page, path);
    const results = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"])
      .analyze();
    const critical = results.violations.filter((violation) => violation.impact === "critical");
    expect(critical, `Critical accessibility violations on ${path || "home"}: ${JSON.stringify(critical, null, 2)}`).toEqual([]);
  }
});
