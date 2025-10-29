# End-to-End Testing

This directory contains end-to-end tests for the Roots Revealed application using Playwright.

## Setup

Install dependencies:
```bash
npm install
npx playwright install
```

## Running Tests

Run all tests:
```bash
npm test
```

Run tests in headed mode (see browser):
```bash
npm run test:headed
```

Run tests in UI mode (interactive):
```bash
npm run test:ui
```

Debug tests:
```bash
npm run test:debug
```

View test report:
```bash
npm run report
```

## Test Structure

- `tests/home.spec.ts` - Home page tests
- `tests/auth.spec.ts` - Authentication flow tests
- `tests/chart-workflow.spec.ts` - Chart creation and management tests

## Configuration

Test configuration is in `playwright.config.ts`. Key settings:

- **Base URL**: `http://localhost:3000` (configurable via `BASE_URL` env var)
- **Browsers**: Chromium, Firefox, WebKit, Mobile Chrome, Mobile Safari
- **Retries**: 2 retries on CI, 0 locally
- **Screenshots**: Captured on failure
- **Videos**: Retained on failure
- **Traces**: Captured on first retry

## Writing Tests

Example test:

```typescript
import { test, expect } from '@playwright/test';

test('should do something', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading')).toBeVisible();
});
```

## CI/CD Integration

Tests run automatically on CI via GitHub Actions. See `.github/workflows/ci.yml` for configuration.

## Best Practices

1. Use `data-testid` attributes for stable selectors
2. Use `page.getByRole()` and semantic selectors when possible
3. Wait for network responses when testing API-dependent features
4. Use `page.waitForURL()` for navigation assertions
5. Take screenshots on critical paths for debugging
6. Keep tests independent and idempotent
