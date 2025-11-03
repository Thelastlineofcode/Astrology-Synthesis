import { test, expect } from "@playwright/test";
import { TEST_USER } from "./helpers/auth";
import { waitForPageLoad, isVisible } from "./helpers/utils";

test.describe("Critical User Flows", () => {
  test.describe("Authentication Flow", () => {
    test("should successfully register a new user", async ({ page }) => {
      await page.goto("/register");

      // Generate unique email for each test run
      const uniqueEmail = `test-${Date.now()}@example.com`;

      // Fill registration form
      await page.fill('input[name="email"]', uniqueEmail);
      await page.fill('input[name="password"]', TEST_USER.password);
      await page.fill('input[name="confirmPassword"]', TEST_USER.password);
      await page.fill('input[name="name"]', TEST_USER.name);

      // Submit form
      await page.click('button[type="submit"]');

      // Verify redirect to dashboard or login
      await page.waitForURL(/\/(dashboard|login)/, { timeout: 10000 });

      // Verify success message or welcome text
      const hasDashboard = await isVisible(page, "text=/Welcome|Dashboard/i");
      expect(hasDashboard).toBeTruthy();
    });

    test("should successfully login with valid credentials", async ({
      page,
    }) => {
      await page.goto("/login");

      // Use demo credentials (adjust based on your test environment)
      await page.fill('input[name="email"]', "demo@rootsrevealed.com");
      await page.fill('input[name="password"]', "demo123");

      // Submit form
      await page.click('button[type="submit"]');

      // Verify redirect to dashboard
      await page.waitForURL("/dashboard", { timeout: 10000 });

      // Verify dashboard loaded
      await expect(page.locator("h1, h2")).toContainText(/Dashboard|Welcome/i);

      // Verify auth token stored
      const token = await page.evaluate(() =>
        localStorage.getItem("authToken")
      );
      expect(token).toBeTruthy();
    });

    test("should show error with invalid credentials", async ({ page }) => {
      await page.goto("/login");

      // Fill with invalid credentials
      await page.fill('input[name="email"]', "invalid@example.com");
      await page.fill('input[name="password"]', "wrongpassword");

      // Submit form
      await page.click('button[type="submit"]');

      // Verify error message appears
      const errorVisible = await isVisible(
        page,
        "text=/invalid|error|incorrect/i"
      );
      expect(errorVisible).toBeTruthy();

      // Verify still on login page
      await expect(page).toHaveURL(/login/);
    });

    test("should successfully logout", async ({ page }) => {
      // First login
      await page.goto("/login");
      await page.fill('input[name="email"]', "demo@rootsrevealed.com");
      await page.fill('input[name="password"]', "demo123");
      await page.click('button[type="submit"]');
      await page.waitForURL("/dashboard");

      // Then logout
      await page.click('button:has-text("Logout"), a:has-text("Logout")');

      // Verify redirect to home or login
      await page.waitForURL(/\/(|login)/, { timeout: 5000 });

      // Verify auth token removed
      const token = await page.evaluate(() =>
        localStorage.getItem("authToken")
      );
      expect(token).toBeNull();
    });
  });

  test.describe("Fortune Reading Flow", () => {
    test("should display fortune form and request reading", async ({
      page,
    }) => {
      // Navigate to fortune page
      await page.goto("/fortune");
      await waitForPageLoad(page);

      // Verify form elements present
      await expect(
        page.locator('input[name="birthDate"], input[type="date"]')
      ).toBeVisible();
      await expect(
        page.locator('input[name="birthTime"], input[type="time"]')
      ).toBeVisible();
      await expect(
        page.locator(
          'input[name="birthPlace"], input[placeholder*="location"], input[placeholder*="place"]'
        )
      ).toBeVisible();

      // Fill birth details
      await page.fill(
        'input[name="birthDate"], input[type="date"]',
        "1990-01-15"
      );
      await page.fill('input[name="birthTime"], input[type="time"]', "14:30");
      await page.fill(
        'input[name="birthPlace"], input[placeholder*="location"], input[placeholder*="place"]',
        "New York, NY"
      );

      // Submit fortune request
      await page.click(
        'button[type="submit"], button:has-text("Get Reading"), button:has-text("Calculate")'
      );

      // Wait for fortune result (adjust timeout for AI generation)
      await page.waitForSelector(
        "text=/chart|reading|fortune|interpretation/i",
        {
          timeout: 15000,
        }
      );

      // Verify fortune content displayed
      const hasChart = await isVisible(page, '[class*="chart"], svg, canvas');
      const hasText = await isVisible(
        page,
        "text=/sun|moon|planet|house|sign/i"
      );

      expect(hasChart || hasText).toBeTruthy();
    });

    test("should validate required birth information", async ({ page }) => {
      await page.goto("/fortune");

      // Try to submit without filling fields
      await page.click(
        'button[type="submit"], button:has-text("Get Reading"), button:has-text("Calculate")'
      );

      // Verify validation errors
      const hasValidationError = await isVisible(
        page,
        "text=/required|enter|provide|missing/i"
      );

      expect(hasValidationError).toBeTruthy();
    });
  });

  test.describe("Advisor Chat Flow", () => {
    test("should display advisor selection and start chat", async ({
      page,
    }) => {
      // Navigate to chat page
      await page.goto("/chat");
      await waitForPageLoad(page);

      // Verify advisors are displayed
      const advisorCards = page
        .locator('[class*="advisor"], [class*="card"], article, section')
        .filter({
          hasText: /papa|erzulie|damballah|baron/i,
        });

      const count = await advisorCards.count();
      expect(count).toBeGreaterThan(0);

      // Select first advisor
      await advisorCards.first().click();

      // Verify chat interface appears
      await expect(
        page.locator(
          'input[placeholder*="message"], textarea[placeholder*="message"]'
        )
      ).toBeVisible();

      // Send a test message
      await page.fill(
        'input[placeholder*="message"], textarea[placeholder*="message"]',
        "What can you tell me about my career?"
      );
      await page.click('button:has-text("Send"), button[type="submit"]');

      // Wait for AI response (adjust timeout)
      await page.waitForSelector("text=/career|path|guidance|future/i", {
        timeout: 20000,
      });
    });

    test("should allow switching between advisors", async ({ page }) => {
      await page.goto("/chat");
      await waitForPageLoad(page);

      // Get all advisor buttons/cards
      const advisors = page.locator(
        'button:has-text("Papa"), button:has-text("Erzulie"), button:has-text("Damballah"), button:has-text("Baron")'
      );
      const count = await advisors.count();

      if (count >= 2) {
        // Click first advisor
        await advisors.nth(0).click();
        await page.waitForTimeout(1000);

        // Click second advisor
        await advisors.nth(1).click();
        await page.waitForTimeout(1000);

        // Verify advisor switched (check for different personality)
        const chatArea = page.locator('main, [class*="chat"]');
        expect(await chatArea.isVisible()).toBeTruthy();
      }
    });
  });

  test.describe("Profile Management Flow", () => {
    test("should display and update user profile", async ({ page }) => {
      // Login first (use demo account)
      await page.goto("/login");
      await page.fill('input[name="email"]', "demo@rootsrevealed.com");
      await page.fill('input[name="password"]', "demo123");
      await page.click('button[type="submit"]');
      await page.waitForURL("/dashboard");

      // Navigate to profile
      await page.goto("/profile");
      await waitForPageLoad(page);

      // Verify profile form displayed
      await expect(
        page.locator('input[name="name"], input[name="email"]')
      ).toBeVisible();

      // Click edit button if present
      const editButton = page.locator('button:has-text("Edit")');
      if (await editButton.isVisible()) {
        await editButton.click();
      }

      // Update name
      const nameInput = page.locator('input[name="name"]');
      await nameInput.clear();
      await nameInput.fill("Updated Test User");

      // Save changes
      await page.click('button:has-text("Save"), button[type="submit"]');

      // Verify success message
      await page.waitForSelector("text=/saved|updated|success/i", {
        timeout: 5000,
      });
    });

    test("should display reading history", async ({ page }) => {
      // Login first
      await page.goto("/login");
      await page.fill('input[name="email"]', "demo@rootsrevealed.com");
      await page.fill('input[name="password"]', "demo123");
      await page.click('button[type="submit"]');
      await page.waitForURL("/dashboard");

      // Navigate to readings history
      await page.goto("/readings");
      await waitForPageLoad(page);

      // Verify readings page structure
      const hasHeader = await isVisible(page, "h1, h2");
      expect(hasHeader).toBeTruthy();

      // Check for readings list or empty state
      const hasReadings = await isVisible(
        page,
        '[class*="reading"], article, li'
      );
      const hasEmptyState = await isVisible(
        page,
        "text=/no reading|empty|get started/i"
      );

      expect(hasReadings || hasEmptyState).toBeTruthy();
    });
  });

  test.describe("Navigation Flow", () => {
    test("should navigate between main pages", async ({ page }) => {
      // Start at home
      await page.goto("/");
      await expect(page).toHaveURL("/");

      // Navigate to fortune
      await page.click('a[href="/fortune"], nav a:has-text("Fortune")');
      await expect(page).toHaveURL("/fortune");

      // Navigate to chat
      await page.click('a[href="/chat"], nav a:has-text("Chat")');
      await expect(page).toHaveURL("/chat");

      // Navigate back home
      await page.click('a[href="/"], nav a:has-text("Home")');
      await expect(page).toHaveURL("/");
    });

    test("should protect authenticated routes", async ({ page }) => {
      // Try to access profile without login
      await page.goto("/profile");

      // Should redirect to login
      await page.waitForURL(/login/, { timeout: 5000 });

      // Try to access readings without login
      await page.goto("/readings");

      // Should redirect to login
      await page.waitForURL(/login/, { timeout: 5000 });
    });
  });
});
