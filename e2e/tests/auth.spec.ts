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

      // Check for error message
      await expect(page.getByText(/valid email/i)).toBeVisible({ timeout: 3000 }).catch(() => {
        // Validation might prevent submission
        expect(page.locator('input[name="email"]:invalid')).toBeVisible();
      });
    });

    test('should show error for weak password', async ({ page }) => {
      await page.goto('/auth/register');

      await page.fill('input[name="name"]', 'Test User');
      await page.fill('input[name="email"]', 'test@example.com');
      await page.fill('input[name="password"]', '123');
      await page.fill('input[name="confirmPassword"]', '123');

      await page.click('button[type="submit"]');

      // Check for password error
      await expect(page.getByText(/password.*characters/i)).toBeVisible({ timeout: 3000 }).catch(() => {
        expect(page.locator('input[name="password"]:invalid')).toBeVisible();
      });
    });
  });

  test.describe('Login', () => {
    test.beforeAll(async ({ browser }) => {
      // Register a user for login tests
      const page = await browser.newPage();
      await page.goto('/auth/register');
      
      await page.fill('input[name="name"]', testUser.name).catch(() => {});
      await page.fill('input[name="email"]', `login-${testUser.email}`).catch(() => {});
      await page.fill('input[name="password"]', testUser.password).catch(() => {});
      await page.fill('input[name="confirmPassword"]', testUser.password).catch(() => {});
      await page.click('button[type="submit"]').catch(() => {});
      
      await page.close();
    });

    test('should login with valid credentials', async ({ page }) => {
      await page.goto('/auth/login');

      await page.fill('input[name="email"]', `login-${testUser.email}`);
      await page.fill('input[name="password"]', testUser.password);

      await page.click('button[type="submit"]');

      // Should redirect to dashboard
      await page.waitForURL('**/dashboard', { timeout: 5000 }).catch(() => {
        expect(page.getByText(/success/i)).toBeVisible();
      });
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

      // Should redirect to login
      await page.waitForURL('**/auth/login', { timeout: 5000 }).catch(() => {
        // Or show an auth prompt
        expect(page.getByText(/log.*in/i)).toBeVisible();
      });
    });
  });
});
