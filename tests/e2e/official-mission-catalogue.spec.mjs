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
  expect(coverage.matched_count).toBeGreaterThan(0);
  expect(coverage.official_only_count).toBeGreaterThanOrEqual(0);
  expect(coverage.official_only_count).toBeLessThan(coverage.official_count);
  expect(catalogue.source.url).toBe("https://www.missionchief.co.uk/einsaetze.json");
  expect(catalogue.source.sha256).toMatch(/^[a-f0-9]{64}$/);

  const officialOnlyIds = new Set(
    coverage.official_only.map((record) => String(record.id))
  );
  const pendingRecord = catalogue.records.find((record) => {
    const additional = record.additional;
    return officialOnlyIds.has(String(record.id))
      && additional
      && typeof additional === "object"
      && !Array.isArray(additional)
      && Object.keys(additional).length > 0
      && record.base_mission_id !== undefined;
  });
  expect(
    pendingRecord,
    "Coverage must retain an official-only record with structured additional and base-mission evidence"
  ).toBeTruthy();

  const pendingId = String(pendingRecord.id);
  const pendingName = String(
    pendingRecord.name ?? pendingRecord.caption ?? pendingRecord.title
  );
  const pendingUrl = `https://www.missionchief.co.uk/einsaetze/${pendingId}`;
  const additionalKey = Object.keys(pendingRecord.additional).sort()[0];

  let catalogueRequests = 0;
  page.on("request", (browserRequest) => {
    try {
      const path = new URL(browserRequest.url()).pathname;
      if (path.endsWith("/assets/data/official/uk-missions.json")) catalogueRequests += 1;
    } catch {
      // Ignore browser-internal URLs that are not valid absolute URLs.
    }
  });

  await page.goto("tools/mission-lookup/", { waitUntil: "networkidle" });
  const root = page.locator("[data-mcuk-tool='mission-lookup']");
  await expect(root).toHaveAttribute("data-mcuk-ready", "true");
  await expect(root.locator("[data-role='summary']")).toContainText(
    `${coverage.official_only_count} official records awaiting full mapping`
  );

  await root.locator("select[data-role='source']").selectOption("official");
  await root.locator("input[data-role='query']").fill(pendingName);
  const officialCard = root
    .locator("article.mcuk-mission-card--official")
    .filter({ hasText: `#${pendingId}` })
    .first();
  await expect(officialCard).toContainText(pendingName);
  await expect(officialCard).toContainText(`#${pendingId}`);
  await expect(officialCard).toContainText("Official UK catalogue");
  await expect(officialCard).toContainText("Canonical mapping pending");

  const fieldDetails = officialCard.locator("details.mcuk-official-field-details");
  await expect(fieldDetails).toContainText("Patients, personnel, variants and additional fields");
  await fieldDetails.locator("summary").click();
  await expect(fieldDetails.locator("table")).toContainText(`additional.${additionalKey}`);
  await expect(fieldDetails.locator("table")).toContainText("base_mission_id");

  const officialDetails = officialCard.locator("details.mcuk-official-record-details");
  await expect(officialDetails).toContainText("Complete official catalogue record");
  await officialDetails.locator("summary").click();
  await expect(officialDetails.locator("pre")).toContainText(
    `"official_url": "${pendingUrl}"`
  );
  await expect(officialDetails.locator("pre")).toContainText('"requirements"');
  await expect(officialDetails.locator("pre")).toContainText('"prerequisites"');

  await root.locator("select[data-role='source']").selectOption("canonical");
  await root.locator("input[data-role='query']").fill("588");
  const canonicalCard = root
    .locator("article.mcuk-mission-card--canonical")
    .filter({ hasText: "#588" })
    .first();
  await expect(canonicalCard).toContainText("Aircraft Accident - Code F");
  await expect(canonicalCard).toContainText("Canonical mapped");

  const canonicalDetails = canonicalCard.locator("details.mcuk-official-record-details");
  await expect(canonicalDetails).toContainText("Complete official catalogue record");
  await canonicalDetails.locator("summary").click();
  await expect(canonicalDetails.locator("pre")).toContainText(
    '"official_url": "https://www.missionchief.co.uk/einsaetze/588"'
  );
  await expect(canonicalDetails.locator("pre")).toContainText('"additional"');

  expect(catalogueRequests, "Official catalogue should be fetched once and shared by all lookup surfaces").toBe(1);

  const dimensions = await page.locator(".md-content").evaluate((element) => ({
    clientWidth: element.clientWidth,
    scrollWidth: element.scrollWidth
  }));
  expect(dimensions.scrollWidth).toBeLessThanOrEqual(dimensions.clientWidth + 2);
});
