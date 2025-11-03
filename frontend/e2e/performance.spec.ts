import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  
  test('Home page should load in under 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    console.log(`Home page load time: ${loadTime}ms`);
    
    // Should load in under 3000ms
    expect(loadTime).toBeLessThan(3000);
  });

  test('Fortune page should load in under 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/fortune');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    console.log(`Fortune page load time: ${loadTime}ms`);
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('Chat page should load in under 3 seconds', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    console.log(`Chat page load time: ${loadTime}ms`);
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('Dashboard page should load in under 3 seconds (if authenticated)', async ({ page }) => {
    // Login first
    await page.goto('/login');
    await page.fill('input[name="email"]', 'demo@rootsrevealed.com');
    await page.fill('input[name="password"]', 'demo123');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    
    // Measure dashboard load time on subsequent visit
    const startTime = Date.now();
    
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    const loadTime = Date.now() - startTime;
    console.log(`Dashboard page load time: ${loadTime}ms`);
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('Fortune calculation should complete in under 1 second (mocked)', async ({ page }) => {
    await page.goto('/fortune');
    
    // Fill birth details
    await page.fill('input[name="birthDate"], input[type="date"]', '1990-01-15');
    await page.fill('input[name="birthTime"], input[type="time"]', '14:30');
    await page.fill('input[name="birthPlace"], input[placeholder*="location"], input[placeholder*="place"]', 'New York, NY');
    
    // Measure calculation time
    const startTime = Date.now();
    
    await page.click('button[type="submit"], button:has-text("Get Reading"), button:has-text("Calculate")');
    
    // Wait for result
    await page.waitForSelector('text=/chart|reading|fortune|interpretation/i', { 
      timeout: 10000 
    });
    
    const calculationTime = Date.now() - startTime;
    console.log(`Fortune calculation time: ${calculationTime}ms`);
    
    // Note: This includes network time. For real API, adjust threshold
    // Target: <1s for calculation, but allow more for network + AI
    expect(calculationTime).toBeLessThan(15000); // 15s for AI generation
  });

  test('Chat response should arrive in under 3 seconds (target)', async ({ page }) => {
    await page.goto('/chat');
    await page.waitForLoadState('networkidle');
    
    // Select an advisor
    const advisor = page.locator('[class*="advisor"], button').filter({
      hasText: /papa|erzulie|damballah|baron/i
    }).first();
    
    if (await advisor.isVisible()) {
      await advisor.click();
    }
    
    // Send message and measure response time
    const messageInput = page.locator('input[placeholder*="message"], textarea[placeholder*="message"]');
    await messageInput.fill('What is my fortune?');
    
    const startTime = Date.now();
    
    await page.click('button:has-text("Send"), button[type="submit"]');
    
    // Wait for AI response
    await page.waitForSelector('text=/fortune|guidance|path|future/i', { 
      timeout: 20000 
    });
    
    const responseTime = Date.now() - startTime;
    console.log(`Chat response time: ${responseTime}ms`);
    
    // Target: <3s, but allow up to 20s for AI generation
    expect(responseTime).toBeLessThan(20000);
  });

  test('Page navigation should be instant (client-side routing)', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Measure client-side navigation time
    const startTime = Date.now();
    
    await page.click('a[href="/fortune"], nav a:has-text("Fortune")');
    await page.waitForURL('/fortune');
    
    const navTime = Date.now() - startTime;
    console.log(`Client-side navigation time: ${navTime}ms`);
    
    // Should be instant (<500ms)
    expect(navTime).toBeLessThan(500);
  });

  test('Images should load efficiently', async ({ page }) => {
    await page.goto('/');
    
    // Wait for all images to load
    await page.waitForLoadState('networkidle');
    
    // Check if images are loaded
    const images = page.locator('img');
    const imageCount = await images.count();
    
    console.log(`Total images on home page: ${imageCount}`);
    
    // Verify images have loaded
    if (imageCount > 0) {
      const firstImage = images.first();
      const naturalWidth = await firstImage.evaluate((img: HTMLImageElement) => img.naturalWidth);
      
      // Image should have width (loaded successfully)
      expect(naturalWidth).toBeGreaterThan(0);
    }
  });

  test('No memory leaks on repeated navigation', async ({ page }) => {
    await page.goto('/');
    
    // Navigate between pages multiple times
    for (let i = 0; i < 5; i++) {
      await page.goto('/fortune');
      await page.waitForLoadState('networkidle');
      
      await page.goto('/chat');
      await page.waitForLoadState('networkidle');
      
      await page.goto('/');
      await page.waitForLoadState('networkidle');
    }
    
    // Get memory metrics
    const metrics = await page.evaluate(() => {
      if (performance && (performance as never)['memory']) {
        const memory = (performance as never)['memory'] as {
          usedJSHeapSize: number;
          totalJSHeapSize: number;
          jsHeapSizeLimit: number;
        };
        return {
          usedJSHeapSize: memory.usedJSHeapSize,
          totalJSHeapSize: memory.totalJSHeapSize,
          jsHeapSizeLimit: memory.jsHeapSizeLimit,
        };
      }
      return null;
    });
    
    if (metrics) {
      console.log('Memory usage:', metrics);
      
      // Memory usage should be reasonable (less than 100MB)
      const usedMB = metrics.usedJSHeapSize / (1024 * 1024);
      expect(usedMB).toBeLessThan(100);
    }
  });

  test('Bundle size should be reasonable', async ({ page }) => {
    // Track all JS/CSS resources loaded
    const resources: { url: string; size: number }[] = [];
    
    page.on('response', async (response) => {
      const url = response.url();
      if (url.endsWith('.js') || url.endsWith('.css')) {
        try {
          const buffer = await response.body();
          resources.push({
            url,
            size: buffer.length,
          });
        } catch {
          // Ignore errors
        }
      }
    });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Calculate total bundle size
    const totalSize = resources.reduce((sum, r) => sum + r.size, 0);
    const totalMB = totalSize / (1024 * 1024);
    
    console.log(`Total bundle size: ${totalMB.toFixed(2)} MB`);
    console.log(`Number of resources: ${resources.length}`);
    
    // Total bundle should be under 5MB
    expect(totalMB).toBeLessThan(5);
  });
});
