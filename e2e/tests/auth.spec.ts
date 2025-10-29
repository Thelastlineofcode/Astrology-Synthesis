import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  const testUser = {
    email: `test-${Date.now()}@example.com`,
    password: 'TestPassword123!',
    name: 'Test User',
  };

  test.describe('Registration', () => {
    test('should register a new user successfully', async ({ page }) => {
      await page.goto('/auth/register');

      // Fill in registration form
      await page.fill('input[name="name"]', testUser.name);
      await page.fill('input[name="email"]', testUser.email);
      await page.fill('input[name="password"]', testUser.password);
      await page.fill('input[name="confirmPassword"]', testUser.password);

      // Submit form
      await page.click('button[type="submit"]');

      // Wait for redirect or success message
      await page.waitForURL('**/dashboard', { timeout: 5000 }).catch(() => {
        // If redirect doesn't happen, check for success message
        expect(page.getByText(/success/i)).toBeVisible();
      });
    });

    test('should show error for invalid email', async ({ page }) => {
      await page.goto('/auth/register');

      await page.fill('input[name="name"]', 'Test User');
      await page.fill('input[name="email"]', 'invalid-email');
      await page.fill('input[name="password"]', testUser.password);
      await page.fill('input[name="confirmPassword"]', testUser.password);

      await page.click('button[type="submit"]');

      // Check for error message or validation state
      const hasErrorMessage = await page.getByText(/valid email/i).isVisible({ timeout: 3000 }).catch(() => false);
      const hasInvalidInput = await page.locator('input[name="email"]:invalid').count() > 0;
      
      expect(hasErrorMessage || hasInvalidInput).toBeTruthy();
    });

    test('should show error for weak password', async ({ page }) => {
      await page.goto('/auth/register');

      await page.fill('input[name="name"]', 'Test User');
      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="password"]', '123');
      await page.fill('input[name="confirmPassword"]', '123');

      await page.click('button[type="submit"]');

      // Check for password error
      const hasErrorMessage = await page.getByText(/password.*characters/i).isVisible({ timeout: 3000 }).catch(() => false);
      const hasInvalidInput = await page.locator('input[name="password"]:invalid').count() > 0;
      
      expect(hasErrorMessage || hasInvalidInput).toBeTruthy();
    });
  });

  test.describe('Login', () => {
    // Use a unique email for login tests to avoid conflicts
    const loginTestEmail = `login-${Date.now()}@example.com`;

    test.beforeEach(async ({ page }) => {
      // Register a user before each login test for isolation
      await page.goto('/auth/register');
      
      await page.fill('input[name="name"]', testUser.name);
      await page.fill('input[name="email"]', loginTestEmail);
      await page.fill('input[name="password"]', testUser.password);
      await page.fill('input[name="confirmPassword"]', testUser.password);
      await page.click('button[type="submit"]');
      
      // Wait for registration to complete
      await page.waitForTimeout(1000);
    });

    test('should login with valid credentials', async ({ page }) => {
      await page.goto('/auth/login');

      await page.fill('input[name="email"]', loginTestEmail);
      await page.fill('input[name="password"]', testUser.password);

      await page.click('button[type="submit"]');

      // Should redirect to dashboard or show success
      const onDashboard = await page.waitForURL('**/dashboard', { timeout: 5000 }).then(() => true).catch(() => false);
      const hasSuccess = await page.getByText(/success/i).isVisible({ timeout: 1000 }).catch(() => false);
      
      expect(onDashboard || hasSuccess).toBeTruthy();
    });

    test('should show error for invalid credentials', async ({ page }) => {
      await page.goto('/auth/login');

      await page.fill('input[name="email"]', 'wrong@example.com');
      await page.fill('input[name="password"]', 'wrongpassword');

      await page.click('button[type="submit"]');

      // Check for error message
      await expect(page.getByText(/invalid.*credentials/i)).toBeVisible({ timeout: 3000 });
    });

    test('should validate required fields', async ({ page }) => {
      await page.goto('/auth/login');

      // Try to submit without filling fields
      await page.click('button[type="submit"]');

      // Form should not submit
      await expect(page).toHaveURL(/\/auth\/login/);
    });
  });

  test.describe('Protected Routes', () => {
    test('should redirect to login when accessing protected route', async ({ page }) => {
      await page.goto('/dashboard');

      // Should redirect to login or show auth prompt
      const onLoginPage = await page.waitForURL('**/auth/login', { timeout: 5000 }).then(() => true).catch(() => false);
      const hasLoginPrompt = await page.getByText(/log.*in/i).isVisible({ timeout: 1000 }).catch(() => false);
      
      expect(onLoginPage || hasLoginPrompt).toBeTruthy();
    });
  });
});
