import { test, expect } from "@playwright/test";

async function openPage(page, path = "") {
  const response = await page.goto(path, { waitUntil: "networkidle" });
  expect(response).not.toBeNull();
  expect(response.ok()).toBeTruthy();
}

test("global command palette searches canonical data from the keyboard", async ({ page }) => {
  await openPage(page);
  await page.keyboard.press(process.platform === "darwin" ? "Meta+K" : "Control+K");

  const palette = page.locator("[data-mcuk-palette]");
  await expect(palette).toHaveAttribute("data-open", "true");

  const query = palette.getByRole("searchbox", { name: "Search verified MissionChief UK data" });
  await query.fill("fire engine");
  await expect.poll(() => palette.locator(".mcuk-palette__result").count()).toBeGreaterThan(0);
  await expect(palette.locator(".mcuk-palette__result").first()).toContainText("Fire engine", { ignoreCase: true });

  await page.keyboard.press("Escape");
  await expect(palette).toHaveAttribute("data-open", "false");
});

test("command palette filters collections and deep-links into mission lookup", async ({ page }) => {
  await openPage(page);
  await page.locator("[data-mcuk-palette-open]").first().click();

  const palette = page.locator("[data-mcuk-palette]");
  await palette.getByRole("button", { name: "Missions", exact: true }).click();
  await palette.getByRole("searchbox").fill("aircraft accident");

  const result = palette.locator(".mcuk-palette__result[data-collection='missions']").first();
  await expect(result).toBeVisible();
  await result.click();

  await expect(page).toHaveURL(/\/tools\/mission-lookup\/\?q=/);
  const lookup = page.locator("[data-mcuk-tool='mission-lookup']");
  await expect(lookup.locator("input[data-role='query']")).toHaveValue(/aircraft accident/i);
  await expect.poll(() => lookup.locator("article.mcuk-tool-card").count()).toBeGreaterThan(0);
});

test("command palette remains usable on an iPhone viewport", async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== "webkit-iphone", "Mobile posture only needs the iPhone project");
  await openPage(page, "services/fire-and-rescue/");
  await page.keyboard.press("Control+K");

  const palette = page.locator("[data-mcuk-palette]");
  await expect(palette).toHaveAttribute("data-open", "true");
  await expect(palette.locator(".mcuk-palette__dialog")).toBeVisible();
  await palette.getByRole("searchbox").fill("police car");
  await expect.poll(() => palette.locator(".mcuk-palette__result").count()).toBeGreaterThan(0);
});