import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load home page successfully', async ({ page }) => {
    await page.goto('/');

    // Check if the main heading is visible
    await expect(page.getByRole('heading', { name: /Roots Revealed/i })).toBeVisible();
    
    // Check if the description is present
    await expect(page.getByText(/Explore your cosmic journey/i)).toBeVisible();
  });

  test('should navigate to dashboard', async ({ page }) => {
    await page.goto('/');

    // Click on dashboard link
    const dashboardLink = page.getByRole('link', { name: /View Dashboard/i });
    await expect(dashboardLink).toBeVisible();
    
    await dashboardLink.click();

    // Wait for navigation
    await page.waitForURL('**/dashboard');
    
    // Verify we're on the dashboard page
    await expect(page).toHaveURL(/\/dashboard/);
  });

  test('should have proper meta tags', async ({ page }) => {
    await page.goto('/');

    // Check title
    await expect(page).toHaveTitle(/Roots Revealed/i);
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Main heading should still be visible
    await expect(page.getByRole('heading', { name: /Roots Revealed/i })).toBeVisible();
  });
});
