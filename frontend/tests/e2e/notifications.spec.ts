import { test, expect } from "@playwright/test";

// Requires E2E_BASE_URL (frontend) and NEXT_PUBLIC_API_BASE_URL (frontend env) pointing to a working backend

test.describe("Notifications preferences", () => {
  test("redirects unauthenticated users to login", async ({ page }) => {
    await page.goto("/settings/notifications");
    await expect(page).toHaveURL(/\/auth\/login/);
  });
});
