import { test, expect } from "@playwright/test";

test("official UK mission catalogue is complete, fully canonical and searchable", async ({ page, request }) => {
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
  expect(coverage.matched_count).toBe(coverage.official_count);
  expect(coverage.matched_count + coverage.official_only_count).toBe(coverage.official_count);
  expect(coverage.canonical_count).toBeGreaterThan(coverage.official_count);
  expect(coverage.official_only_count).toBe(0);
  expect(coverage.official_only).toEqual([]);
  expect(coverage.coverage_percent).toBe(100);
  expect(catalogue.source.url).toBe("https://www.missionchief.co.uk/einsaetze.json");
  expect(catalogue.source.sha256).toMatch(/^[a-f0-9]{64}$/);

  const fullyMappedRecord = catalogue.records.find((record) => {
    const additional = record.additional;
    return additional
      && typeof additional === "object"
      && !Array.isArray(additional)
      && Object.keys(additional).length > 0
      && record.base_mission_id !== undefined;
  });
  expect(
    fullyMappedRecord,
    "Every official mission must have a canonical match, including records with structured additional and base-mission evidence"
  ).toBeTruthy();

  const mappedId = String(fullyMappedRecord.id);
  const mappedName = String(
    fullyMappedRecord.name ?? fullyMappedRecord.caption ?? fullyMappedRecord.title
  );
  const mappedUrl = String(
    fullyMappedRecord.official_url ?? `https://www.missionchief.co.uk/einsaetze/${mappedId}`
  );
  const additionalKey = Object.keys(fullyMappedRecord.additional).sort()[0];

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
    "0 official records awaiting full mapping"
  );

  await root.locator("select[data-role='source']").selectOption("canonical");
  await root.locator("input[data-role='query']").fill(mappedName);
  const mappedCard = root
    .locator("article.mcuk-mission-card--canonical")
    .filter({ hasText: `#${mappedId}` })
    .first();
  await expect(mappedCard).toContainText(mappedName);
  await expect(mappedCard).toContainText(`#${mappedId}`);
  await expect(mappedCard).toContainText("Canonical mapped");
  await expect(mappedCard).toContainText("Official ID matched");

  const fieldDetails = mappedCard.locator("details.mcuk-official-field-details");
  await expect(fieldDetails).toContainText("Patients, personnel, variants and additional fields");
  await fieldDetails.locator("summary").click();
  await expect(fieldDetails.locator("table")).toContainText(`additional.${additionalKey}`);
  await expect(fieldDetails.locator("table")).toContainText("base_mission_id");

  const mappedDetails = mappedCard.locator("details.mcuk-official-record-details");
  await expect(mappedDetails).toContainText("Complete official catalogue record");
  await mappedDetails.locator("summary").click();
  await expect(mappedDetails.locator("pre")).toContainText(
    `"official_url": "${mappedUrl}"`
  );
  await expect(mappedDetails.locator("pre")).toContainText('"requirements"');
  await expect(mappedDetails.locator("pre")).toContainText('"prerequisites"');

  await root.locator("input[data-role='query']").fill("588");
  const canonicalCard = root
    .locator("article.mcuk-mission-card--canonical")
    .filter({ hasText: "#588" })
    .first();
  await expect(canonicalCard).toContainText("Aircraft Accident - Code F");
  await expect(canonicalCard).toContainText("Canonical mapped");
  await expect(canonicalCard).toContainText("Official ID matched");

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
