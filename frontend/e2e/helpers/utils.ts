import { Page, expect } from "@playwright/test";

/**
 * Wait for page to be fully loaded
 */
export async function waitForPageLoad(page: Page, timeout = 30000) {
  await page.waitForLoadState("networkidle", { timeout });
}

/**
 * Take a screenshot with a descriptive name
 */
export async function takeScreenshot(page: Page, name: string) {
  await page.screenshot({
    path: `screenshots/${name}-${Date.now()}.png`,
    fullPage: true,
  });
}

/**
 * Check for console errors
 */
export async function getConsoleErrors(page: Page): Promise<string[]> {
  const errors: string[] = [];

  page.on("console", (msg) => {
    if (msg.type() === "error") {
      errors.push(msg.text());
    }
  });

  return errors;
}

/**
 * Wait for API response
 */
export async function waitForAPIResponse(
  page: Page,
  urlPattern: string | RegExp,
  timeout = 10000
) {
  return page.waitForResponse(
    (response) => {
      const url = response.url();
      if (typeof urlPattern === "string") {
        return url.includes(urlPattern);
      }
      return urlPattern.test(url);
    },
    { timeout }
  );
}

/**
 * Fill form field with validation
 */
export async function fillField(
  page: Page,
  selector: string,
  value: string,
  validate = true
) {
  await page.fill(selector, value);

  if (validate) {
    const inputValue = await page.inputValue(selector);
    expect(inputValue).toBe(value);
  }
}

/**
 * Click and wait for navigation
 */
export async function clickAndNavigate(page: Page, selector: string) {
  await Promise.all([page.waitForNavigation(), page.click(selector)]);
}

/**
 * Scroll to element
 */
export async function scrollToElement(page: Page, selector: string) {
  await page.locator(selector).scrollIntoViewIfNeeded();
}

/**
 * Check if element is visible
 */
export async function isVisible(
  page: Page,
  selector: string
): Promise<boolean> {
  try {
    await page.waitForSelector(selector, { state: "visible", timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

/**
 * Wait for text content
 */
export async function waitForText(
  page: Page,
  selector: string,
  text: string | RegExp,
  timeout = 10000
) {
  await page.waitForSelector(selector, { timeout });
  await expect(page.locator(selector)).toContainText(text);
}

/**
 * Clear and type with delay (simulates real user)
 */
export async function typeSlowly(
  page: Page,
  selector: string,
  text: string,
  delay = 50
) {
  await page.click(selector);
  await page.fill(selector, "");
  await page.type(selector, text, { delay });
}

/**
 * Mock API response
 */
export async function mockAPIResponse(
  page: Page,
  urlPattern: string | RegExp,
  response: unknown
) {
  await page.route(urlPattern, (route) => {
    route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify(response),
    });
  });
}

/**
 * Setup mock auth for tests
 */
export async function setupMockAuth(page: Page) {
  // Set mock auth token
  await page.addInitScript(() => {
    localStorage.setItem("authToken", "mock-test-token-12345");
  });
}
