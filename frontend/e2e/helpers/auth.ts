import { Page, expect } from "@playwright/test";

/**
 * Test user credentials
 */
export const TEST_USER = {
  email: "test@example.com",
  password: "TestPassword123!",
  name: "Test User",
  birthDate: "1990-01-15",
  birthTime: "14:30",
  birthPlace: "New York, NY",
};

/**
 * Register a new test user
 */
export async function registerUser(page: Page, userData = TEST_USER) {
  await page.goto("/register");

  // Fill registration form
  await page.fill('input[name="email"]', userData.email);
  await page.fill('input[name="password"]', userData.password);
  await page.fill('input[name="confirmPassword"]', userData.password);
  await page.fill('input[name="name"]', userData.name);

  // Submit form
  await page.click('button[type="submit"]');

  // Wait for successful registration (redirect to login or dashboard)
  await expect(page).toHaveURL(/\/(login|dashboard)/);
}

/**
 * Login with test user credentials
 */
export async function loginUser(page: Page, credentials = TEST_USER) {
  await page.goto("/login");

  // Fill login form
  await page.fill('input[name="email"]', credentials.email);
  await page.fill('input[name="password"]', credentials.password);

  // Submit form
  await page.click('button[type="submit"]');

  // Wait for successful login (redirect to dashboard)
  await expect(page).toHaveURL("/dashboard");
}

/**
 * Logout current user
 */
export async function logoutUser(page: Page) {
  // Click logout button (adjust selector based on your implementation)
  await page.click('button:has-text("Logout"), a:has-text("Logout")');

  // Verify redirect to home or login
  await expect(page).toHaveURL(/\/(|login)/);
}

/**
 * Check if user is authenticated
 */
export async function isAuthenticated(page: Page): Promise<boolean> {
  try {
    // Check for auth token in localStorage
    const token = await page.evaluate(() => localStorage.getItem("authToken"));
    return !!token;
  } catch {
    return false;
  }
}

/**
 * Setup authenticated session
 */
export async function setupAuthenticatedSession(page: Page) {
  await loginUser(page);

  // Verify authentication
  const authenticated = await isAuthenticated(page);
  expect(authenticated).toBeTruthy();
}
