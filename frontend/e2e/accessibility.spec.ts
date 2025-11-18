import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("Accessibility Tests (WCAG 2.1 AA)", () => {
  test("Home page should have no accessibility violations", async ({
    page,
  }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Home page violations: ${accessibilityScanResults.violations.length}`
    );

    if (accessibilityScanResults.violations.length > 0) {
      console.log(
        "Violations:",
        JSON.stringify(accessibilityScanResults.violations, null, 2)
      );
    }

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Fortune page should have no accessibility violations", async ({
    page,
  }) => {
    await page.goto("/fortune");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Fortune page violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Chat page should have no accessibility violations", async ({
    page,
  }) => {
    await page.goto("/chat");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Chat page violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Login page should have no accessibility violations", async ({
    page,
  }) => {
    await page.goto("/login");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Login page violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Register page should have no accessibility violations", async ({
    page,
  }) => {
    await page.goto("/register");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Register page violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Dashboard should have no accessibility violations (authenticated)", async ({
    page,
  }) => {
    // Login first
    await page.goto("/login");
    await page.fill('input[name="email"]', "demo@mula.app");
    await page.fill('input[name="password"]', "demo123");
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Dashboard violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Profile page should have no accessibility violations", async ({
    page,
  }) => {
    // Login first
    await page.goto("/login");
    await page.fill('input[name="email"]', "demo@mula.app");
    await page.fill('input[name="password"]', "demo123");
    await page.click('button[type="submit"]');
    await page.waitForURL("/dashboard");

    await page.goto("/profile");
    await page.waitForLoadState("networkidle");

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();

    console.log(
      `Profile page violations: ${accessibilityScanResults.violations.length}`
    );

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("Keyboard navigation should work on all pages", async ({ page }) => {
    await page.goto("/");

    // Test Tab navigation
    await page.keyboard.press("Tab");

    // Check if focus is visible
    const focusedElement = await page.evaluate(() => {
      const el = document.activeElement;
      return el ? el.tagName : null;
    });

    expect(focusedElement).toBeTruthy();
    console.log("First focused element:", focusedElement);

    // Tab through multiple elements
    for (let i = 0; i < 5; i++) {
      await page.keyboard.press("Tab");
    }

    // Should be able to navigate backwards
    await page.keyboard.press("Shift+Tab");
  });

  test("Forms should have proper labels", async ({ page }) => {
    await page.goto("/login");

    // Check email input has label
    const emailInput = page.locator('input[name="email"], input[type="email"]');
    const emailLabel = await emailInput.evaluate((el) => {
      const id = el.id;
      if (id) {
        const label = document.querySelector(`label[for="${id}"]`);
        return label ? label.textContent : null;
      }
      return el.getAttribute("aria-label") || el.getAttribute("placeholder");
    });

    expect(emailLabel).toBeTruthy();
    console.log("Email field label:", emailLabel);

    // Check password input has label
    const passwordInput = page.locator(
      'input[name="password"], input[type="password"]'
    );
    const passwordLabel = await passwordInput.evaluate((el) => {
      const id = el.id;
      if (id) {
        const label = document.querySelector(`label[for="${id}"]`);
        return label ? label.textContent : null;
      }
      return el.getAttribute("aria-label") || el.getAttribute("placeholder");
    });

    expect(passwordLabel).toBeTruthy();
    console.log("Password field label:", passwordLabel);
  });

  test("Buttons should have accessible names", async ({ page }) => {
    await page.goto("/fortune");
    await page.waitForLoadState("networkidle");

    // Find all buttons
    const buttons = page.locator("button");
    const count = await buttons.count();

    console.log(`Found ${count} buttons on fortune page`);

    // Check each button has accessible text
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const text = await button.textContent();
      const ariaLabel = await button.getAttribute("aria-label");
      const title = await button.getAttribute("title");

      const hasAccessibleName = text?.trim() || ariaLabel || title;
      expect(hasAccessibleName).toBeTruthy();
    }
  });

  test("Images should have alt text", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Find all images
    const images = page.locator("img");
    const count = await images.count();

    console.log(`Found ${count} images on home page`);

    // Check each image has alt text
    for (let i = 0; i < count; i++) {
      const img = images.nth(i);
      const alt = await img.getAttribute("alt");
      const role = await img.getAttribute("role");

      // Images should have alt text or role="presentation"
      const hasAccessibleAlt =
        alt !== null || role === "presentation" || role === "none";
      expect(hasAccessibleAlt).toBeTruthy();
    }
  });

  test("Color contrast should meet WCAG AA standards", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Run contrast check
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(["wcag2aa"])
      .include("body")
      .analyze();

    // Filter for color contrast violations
    const contrastViolations = accessibilityScanResults.violations.filter(
      (v: { id: string }) => v.id === "color-contrast"
    );

    console.log(`Color contrast violations: ${contrastViolations.length}`);

    if (contrastViolations.length > 0) {
      console.log(
        "Contrast issues:",
        JSON.stringify(contrastViolations, null, 2)
      );
    }

    expect(contrastViolations).toEqual([]);
  });

  test("Page should have proper heading hierarchy", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Check heading structure
    const headings = await page.evaluate(() => {
      const headingElements = document.querySelectorAll(
        "h1, h2, h3, h4, h5, h6"
      );
      return Array.from(headingElements).map((h) => ({
        level: parseInt(h.tagName[1]),
        text: h.textContent?.trim(),
      }));
    });

    console.log("Heading structure:", headings);

    // Should have at least one h1
    const h1Count = headings.filter((h) => h.level === 1).length;
    expect(h1Count).toBeGreaterThanOrEqual(1);
    expect(h1Count).toBeLessThanOrEqual(1); // Only one h1 per page

    // Headings should not skip levels
    for (let i = 1; i < headings.length; i++) {
      const prev = headings[i - 1].level;
      const curr = headings[i].level;

      // Next heading should not be more than 1 level deeper
      if (curr > prev) {
        expect(curr - prev).toBeLessThanOrEqual(1);
      }
    }
  });

  test("Links should be distinguishable", async ({ page }) => {
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    // Check if links are styled differently than regular text
    const linkStyle = await page
      .locator("a")
      .first()
      .evaluate((link) => {
        const style = window.getComputedStyle(link);
        return {
          textDecoration: style.textDecoration,
          color: style.color,
          cursor: style.cursor,
        };
      });

    console.log("Link styles:", linkStyle);

    // Links should have underline, different color, or cursor pointer
    const isDistinguishable =
      linkStyle.textDecoration.includes("underline") ||
      linkStyle.cursor === "pointer";

    expect(isDistinguishable).toBeTruthy();
  });

  test("Focus indicators should be visible", async ({ page }) => {
    await page.goto("/login");

    // Focus on first input
    await page.locator("input").first().focus();

    // Check if focus is styled
    const focusStyle = await page
      .locator("input:focus")
      .first()
      .evaluate((el) => {
        const style = window.getComputedStyle(el);
        return {
          outline: style.outline,
          outlineWidth: style.outlineWidth,
          boxShadow: style.boxShadow,
        };
      });

    console.log("Focus styles:", focusStyle);

    // Should have visible focus indicator
    const hasVisibleFocus =
      focusStyle.outline !== "none" ||
      focusStyle.outlineWidth !== "0px" ||
      focusStyle.boxShadow !== "none";

    expect(hasVisibleFocus).toBeTruthy();
  });
});
