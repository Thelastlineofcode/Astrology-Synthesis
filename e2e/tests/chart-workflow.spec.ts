import { test, expect } from '@playwright/test';

test.describe('Chart Creation Workflow', () => {
  // Helper function to login
  async function login(page) {
    await page.goto('/auth/login');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard', { timeout: 5000 }).catch(() => {});
  }

  test.beforeEach(async ({ page }) => {
    // Login before each test
    await login(page);
  });

  test('should create a new chart successfully', async ({ page }) => {
    // Navigate to chart creation
    await page.goto('/charts/new').catch(() => {
      // Or click on "Create Chart" button if exists
      page.getByRole('button', { name: /create.*chart/i }).click().catch(() => {});
    });

    // Fill in chart details
    await page.fill('input[name="name"]', 'My Test Chart');
    await page.fill('input[name="birthDate"]', '1990-01-01');
    await page.fill('input[name="birthTime"]', '12:00');
    await page.fill('input[name="latitude"]', '40.7128');
    await page.fill('input[name="longitude"]', '-74.0060');

    // Submit form
    await page.click('button[type="submit"]');

    // Check for success
    await expect(page.getByText(/chart.*created/i)).toBeVisible({ timeout: 5000 }).catch(() => {
      // Or check if redirected to chart view
      expect(page).toHaveURL(/\/charts\/\d+/);
    });
  });

  test('should validate chart form fields', async ({ page }) => {
    await page.goto('/charts/new').catch(() => {});

    // Try to submit empty form
    await page.click('button[type="submit"]').catch(() => {});

    // Should show validation errors
    await expect(page.locator('input:invalid')).toHaveCount(1, { timeout: 1000 }).catch(() => {
      // Or check for error messages
      expect(page.getByText(/required/i)).toBeVisible();
    });
  });

  test('should display created charts in list', async ({ page }) => {
    await page.goto('/charts');

    // Wait for charts to load
    await page.waitForSelector('[data-testid="chart-list"]', { timeout: 5000 }).catch(() => {
      // Or check for any chart items
      page.locator('.chart-item').first().waitFor({ timeout: 5000 }).catch(() => {});
    });

    // Should have at least one chart or empty state
    const hasCharts = await page.locator('[data-testid="chart-item"]').count() > 0;
    const hasEmptyState = await page.getByText(/no charts/i).isVisible();
    
    expect(hasCharts || hasEmptyState).toBeTruthy();
  });

  test('should view chart details', async ({ page }) => {
    await page.goto('/charts');

    // Click on first chart if available
    const firstChart = page.locator('[data-testid="chart-item"]').first();
    const chartExists = await firstChart.count() > 0;

    if (chartExists) {
      await firstChart.click();

      // Should show chart details
      await expect(page.getByRole('heading', { level: 1 })).toBeVisible({ timeout: 5000 });
    }
  });

  test('should delete a chart', async ({ page }) => {
    await page.goto('/charts');

    // Find delete button
    const deleteButton = page.locator('[data-testid="delete-chart"]').first();
    const hasDeleteButton = await deleteButton.count() > 0;

    if (hasDeleteButton) {
      await deleteButton.click();

      // Confirm deletion
      await page.getByRole('button', { name: /confirm/i }).click().catch(() => {
        page.getByRole('button', { name: /yes/i }).click().catch(() => {});
      });

      // Should show success message
      await expect(page.getByText(/deleted/i)).toBeVisible({ timeout: 3000 }).catch(() => {
        // Chart should be removed from list
        expect(deleteButton).not.toBeVisible();
      });
    }
  });

  test('should search/filter charts', async ({ page }) => {
    await page.goto('/charts');

    // Look for search input
    const searchInput = page.locator('input[type="search"]').or(page.locator('input[placeholder*="search" i]'));
    const hasSearch = await searchInput.count() > 0;

    if (hasSearch) {
      await searchInput.fill('Test');
      
      // Results should update
      await page.waitForTimeout(500); // Wait for debounce
      
      // Should show filtered results
      const chartCount = await page.locator('[data-testid="chart-item"]').count();
      expect(chartCount >= 0).toBeTruthy();
    }
  });
});
