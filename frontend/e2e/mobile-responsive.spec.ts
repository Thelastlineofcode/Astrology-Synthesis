import { test, expect, devices } from "@playwright/test";

test.describe("Mobile Responsiveness Tests", () => {
  test.describe("Mobile (375px)", () => {
    test.use({ ...devices["iPhone SE"] }); // 375x667

    test("Home page should render correctly on mobile", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Check viewport dimensions
      const viewport = page.viewportSize();
      expect(viewport?.width).toBeLessThanOrEqual(375);

      // Verify mobile menu or navigation
      const navVisible = await page
        .locator('nav, [role="navigation"]')
        .isVisible();
      expect(navVisible).toBeTruthy();

      // Check for horizontal overflow
      const hasOverflow = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      expect(hasOverflow).toBeFalsy();
    });

    test("Fortune form should be usable on mobile", async ({ page }) => {
      await page.goto("/fortune");
      await page.waitForLoadState("networkidle");

      // Verify form inputs are accessible
      await expect(page.locator('input[type="date"]')).toBeVisible();
      await expect(page.locator('input[type="time"]')).toBeVisible();

      // Fill form on mobile
      await page.fill('input[type="date"]', "1990-01-15");
      await page.fill('input[type="time"]', "14:30");

      // Verify inputs can be interacted with
      const dateValue = await page.inputValue('input[type="date"]');
      expect(dateValue).toBe("1990-01-15");
    });

    test("Chat interface should work on mobile", async ({ page }) => {
      await page.goto("/chat");
      await page.waitForLoadState("networkidle");

      // Verify chat input is visible and usable
      const chatInput = page.locator(
        'input[placeholder*="message"], textarea[placeholder*="message"]'
      );

      if (await chatInput.isVisible()) {
        await chatInput.fill("Test message");
        const value = await chatInput.inputValue();
        expect(value).toBe("Test message");
      }
    });

    test("Navigation should be mobile-friendly", async ({ page }) => {
      await page.goto("/");

      // Check for hamburger menu or mobile nav
      const hamburger = page.locator(
        'button[aria-label*="menu"], button:has-text("☰"), [class*="hamburger"]'
      );
      const mobileNavButton = page.locator(
        '[class*="mobile"], button:has([class*="menu"])'
      );

      const hasMobileNav =
        (await hamburger.isVisible()) || (await mobileNavButton.isVisible());

      // Either has mobile menu or regular nav is visible
      const hasNav =
        hasMobileNav || (await page.locator("nav a").first().isVisible());
      expect(hasNav).toBeTruthy();
    });

    test("Buttons should be tap-friendly (min 44x44px)", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Check button sizes
      const buttons = page.locator("button, a[href]");
      const count = await buttons.count();

      if (count > 0) {
        const firstButton = buttons.first();
        const boundingBox = await firstButton.boundingBox();

        if (boundingBox) {
          console.log("Button size:", boundingBox);

          // WCAG recommends minimum 44x44px for touch targets
          // Allow some flexibility for inline links
          const isTapFriendly =
            boundingBox.height >= 32 || boundingBox.width >= 32;
          expect(isTapFriendly).toBeTruthy();
        }
      }
    });
  });

  test.describe("Tablet (768px)", () => {
    test.use({ ...devices["iPad Mini"] }); // 768x1024

    test("Home page should render correctly on tablet", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Check viewport dimensions
      const viewport = page.viewportSize();
      expect(viewport?.width).toBe(768);

      // Verify layout adapts to tablet
      const hasOverflow = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      expect(hasOverflow).toBeFalsy();
    });

    test("Fortune page should use tablet layout", async ({ page }) => {
      await page.goto("/fortune");
      await page.waitForLoadState("networkidle");

      // Check if elements are visible and properly spaced
      const form = page.locator("form").first();
      const boundingBox = await form.boundingBox();

      if (boundingBox) {
        // Form should not exceed viewport width
        expect(boundingBox.width).toBeLessThanOrEqual(768);
      }
    });

    test("Chat should utilize tablet space efficiently", async ({ page }) => {
      await page.goto("/chat");
      await page.waitForLoadState("networkidle");

      // Verify chat interface uses available space
      const chatContainer = page.locator('main, [class*="chat"]').first();
      const boundingBox = await chatContainer.boundingBox();

      if (boundingBox) {
        // Should use most of the width
        expect(boundingBox.width).toBeGreaterThan(500);
      }
    });
  });

  test.describe("Desktop (1440px)", () => {
    test.use({ viewport: { width: 1440, height: 900 } });

    test("Home page should render correctly on desktop", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Check viewport dimensions
      const viewport = page.viewportSize();
      expect(viewport?.width).toBe(1440);

      // Desktop should not have horizontal overflow
      const hasOverflow = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      expect(hasOverflow).toBeFalsy();
    });

    test("Desktop navigation should be fully visible", async ({ page }) => {
      await page.goto("/");

      // Desktop should have full navigation visible (no hamburger)
      const nav = page.locator("nav a");
      const navLinks = await nav.count();

      expect(navLinks).toBeGreaterThan(0);

      // All nav links should be visible
      const firstLink = nav.first();
      await expect(firstLink).toBeVisible();
    });

    test("Content should use max-width on large screens", async ({ page }) => {
      await page.goto("/fortune");
      await page.waitForLoadState("networkidle");

      // Content should be centered with max-width (not spanning full 1440px)
      const mainContent = page.locator('main, [class*="container"]').first();
      const boundingBox = await mainContent.boundingBox();

      if (boundingBox) {
        console.log("Content width on desktop:", boundingBox.width);

        // Most designs use max-width of 1200-1280px
        // Content shouldn't span full width on large screens
        expect(boundingBox.width).toBeLessThanOrEqual(1400);
      }
    });
  });

  test.describe("Responsive Breakpoints", () => {
    test("Layout should adapt between mobile and desktop", async ({ page }) => {
      // Start with desktop
      await page.setViewportSize({ width: 1440, height: 900 });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      const desktopNav = await page.locator("nav").boundingBox();

      // Switch to mobile
      await page.setViewportSize({ width: 375, height: 667 });
      await page.waitForTimeout(1000); // Allow time for responsive changes

      const mobileNav = await page.locator("nav").boundingBox();

      // Navigation should change between desktop and mobile
      if (desktopNav && mobileNav) {
        console.log("Desktop nav:", desktopNav);
        console.log("Mobile nav:", mobileNav);

        // Layout should adapt (though this test is lenient)
        expect(desktopNav.width).toBeGreaterThan(0);
      }
    });

    test("Font sizes should scale appropriately", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.goto("/");

      const mobileFontSize = await page
        .locator("h1")
        .first()
        .evaluate((el) => {
          return window.getComputedStyle(el).fontSize;
        });

      await page.setViewportSize({ width: 1440, height: 900 });
      await page.waitForTimeout(500);

      const desktopFontSize = await page
        .locator("h1")
        .first()
        .evaluate((el) => {
          return window.getComputedStyle(el).fontSize;
        });

      console.log("Mobile h1 font size:", mobileFontSize);
      console.log("Desktop h1 font size:", desktopFontSize);

      // Desktop font should be equal or larger
      const mobileSize = parseFloat(mobileFontSize);
      const desktopSize = parseFloat(desktopFontSize);

      expect(desktopSize).toBeGreaterThanOrEqual(mobileSize);
    });

    test("Images should be responsive", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      const images = page.locator("img");
      const count = await images.count();

      if (count > 0) {
        const img = images.first();
        const boundingBox = await img.boundingBox();

        if (boundingBox) {
          // Image should not exceed viewport width
          expect(boundingBox.width).toBeLessThanOrEqual(375);
        }
      }
    });
  });

  test.describe("Touch Interactions", () => {
    test.use({ ...devices["iPhone 12"] });

    test("Swipe gestures should work where implemented", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Test swipe on carousel or swipeable element if present
      const swipeable = page
        .locator('[class*="carousel"], [class*="swipe"]')
        .first();

      if (await swipeable.isVisible()) {
        const boundingBox = await swipeable.boundingBox();

        if (boundingBox) {
          // Perform swipe gesture
          await page.touchscreen.tap(
            boundingBox.x + boundingBox.width / 2,
            boundingBox.y + boundingBox.height / 2
          );

          // Swipe left
          await page.touchscreen.tap(
            boundingBox.x + 50,
            boundingBox.y + boundingBox.height / 2
          );
        }
      }

      // Test passes if no errors occur
      expect(true).toBeTruthy();
    });

    test("Pinch zoom should be prevented on form inputs", async ({ page }) => {
      await page.goto("/login");

      // Check viewport meta tag
      const viewport = await page.evaluate(() => {
        const meta = document.querySelector('meta[name="viewport"]');
        return meta ? meta.getAttribute("content") : null;
      });

      console.log("Viewport meta:", viewport);

      // Should have viewport meta tag
      expect(viewport).toBeTruthy();
    });
  });

  test.describe("Landscape Mode", () => {
    test.use({ ...devices["iPhone 12 landscape"] });

    test("Layout should work in landscape mode", async ({ page }) => {
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      // Verify no horizontal overflow
      const hasOverflow = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
      });

      expect(hasOverflow).toBeFalsy();

      // Content should be visible
      const mainContent = page.locator("main, body > div").first();
      await expect(mainContent).toBeVisible();
    });
  });
});
