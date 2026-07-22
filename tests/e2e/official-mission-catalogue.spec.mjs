import { test, expect } from "@playwright/test";

test("official UK mission catalogue is complete, reconciled and searchable", async ({ page, request }) => {
  const catalogueResponse = await request.get("assets/data/official/uk-missions.json");
  expect(catalogueResponse.ok(), "Official UK mission catalogue endpoint must be available").toBeTruthy();
  const catalogue = await catalogueResponse.json();

  const coverageResponse = await request.get("assets/data/official/uk-mission-coverage.json");
  expect(coverageResponse.ok(), "Official UK mission coverage endpoint must be available").toBeTruthy();
  const coverage = await coverageResponse.json();

  expect(catalogue.collection).toBe("official-uk-missions");
  expect(catalogue.count).toBe(catalogue.records.length);
  expect(catalogue.count).toBeGreaterThan(1000);
  expect(coverage.official_count).toBe(catalogue.count);
  expect(coverage.matched_count + coverage.official_only_count).toBe(coverage.official_count);
  expect(coverage.canonical_count).toBeGreaterThan(0);
  expect(coverage.official_only_count).toBeGreaterThan(900);
  expect(catalogue.source.url).toBe("https://www.missionchief.co.uk/einsaetze.json");
  expect(catalogue.source.sha256).toMatch(/^[a-f0-9]{64}$/);

  await page.goto("tools/mission-lookup/", { waitUntil: "networkidle" });
  const root = page.locator("[data-mcuk-tool='mission-lookup']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect(root.locator("[data-role='summary']")).toContainText(
    `${coverage.official_only_count} official records awaiting full mapping`
  );

  await root.locator("select[data-role='source']").selectOption("official");
  await root.locator("input[data-role='query']").fill("Burning motorbike");
  const officialCard = root.locator("article.mcuk-mission-card--official").first();
  await expect(officialCard).toContainText("Burning motorbike");
  await expect(officialCard).toContainText("#3");
  await expect(officialCard).toContainText("Official UK catalogue");
  await expect(officialCard).toContainText("Canonical mapping pending");

  const officialDetails = officialCard.locator("details.mcuk-official-record-details");
  await expect(officialDetails).toContainText("Complete official catalogue record");
  await officialDetails.locator("summary").click();
  await expect(officialDetails.locator("pre")).toContainText('"id": 3');
  await expect(officialDetails.locator("pre")).toContainText('"requirements"');
  await expect(officialDetails.locator("pre")).toContainText('"prerequisites"');

  await root.locator("select[data-role='source']").selectOption("canonical");
  await root.locator("input[data-role='query']").fill("588");
  const canonicalCard = root.locator("article.mcuk-mission-card--canonical").first();
  await expect(canonicalCard).toContainText("Aircraft Accident - Code F");
  await expect(canonicalCard).toContainText("Canonical mapped");

  const canonicalDetails = canonicalCard.locator("details.mcuk-official-record-details");
  await expect(canonicalDetails).toContainText("Complete official catalogue record");
  await canonicalDetails.locator("summary").click();
  await expect(canonicalDetails.locator("pre")).toContainText('"id": 588');
  await expect(canonicalDetails.locator("pre")).toContainText('"additional"');

  const dimensions = await page.locator(".md-content").evaluate((element) => ({
    clientWidth: element.clientWidth,
    scrollWidth: element.scrollWidth
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth + 2);
});
