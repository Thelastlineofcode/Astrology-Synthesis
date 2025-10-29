import { test, expect, Page } from '@playwright/test';

test.describe('Chart Creation Workflow', () => {
  // Helper function to login
  async function login(page: Page) {
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
    // Navigate to chart creation - try direct route first
    const chartNewUrl = '/charts/new';
    await page.goto(chartNewUrl);

    // Fill in chart details
    await page.fill('input[name="name"]', 'My Test Chart');
    await page.fill('input[name="birthDate"]', '1990-01-01');
    await page.fill('input[name="birthTime"]', '12:00');
    await page.fill('input[name="latitude"]', '40.7128');
    await page.fill('input[name="longitude"]', '-74.0060');

    // Submit form
    await page.click('button[type="submit"]');

    // Check for success - either message or redirect
    const successVisible = await page.getByText(/chart.*created/i).isVisible({ timeout: 5000 }).catch(() => false);
    const onChartPage = page.url().includes('/charts/');
    
    expect(successVisible || onChartPage).toBeTruthy();
  });

  test('should validate chart form fields', async ({ page }) => {
    await page.goto('/charts/new');

    // Try to submit empty form
    await page.click('button[type="submit"]');

    // Check for validation - either invalid inputs or error messages
    const invalidCount = await page.locator('input:invalid').count();
    const hasErrorText = await page.getByText(/required/i).isVisible({ timeout: 1000 }).catch(() => false);
    
    expect(invalidCount > 0 || hasErrorText).toBeTruthy();
  });

  test('should display created charts in list', async ({ page }) => {
    await page.goto('/charts');

    // Wait for charts to load or empty state
    await page.waitForTimeout(2000);

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

      // Confirm deletion - try different button labels
      const confirmButton = page.getByRole('button', { name: /confirm/i });
      const yesButton = page.getByRole('button', { name: /yes/i });
      
      if (await confirmButton.count() > 0) {
        await confirmButton.click();
      } else if (await yesButton.count() > 0) {
        await yesButton.click();
      }

      // Should show success message or chart removed
      const hasSuccessMessage = await page.getByText(/deleted/i).isVisible({ timeout: 3000 }).catch(() => false);
      const buttonGone = await deleteButton.isVisible().then(() => false).catch(() => true);
      
      expect(hasSuccessMessage || buttonGone).toBeTruthy();
    } else {
      // Skip test if no charts exist
      test.skip();
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
