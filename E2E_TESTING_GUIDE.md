# E2E Testing Guide - Roots Revealed

## Overview

This document describes the comprehensive E2E testing suite for the Roots Revealed astrology application. The test suite ensures quality, performance, accessibility, and mobile responsiveness across all user flows.

## Test Coverage

### 📊 Test Statistics

- **Total Test Suites**: 4 (Critical Flows, Performance, Accessibility, Mobile Responsive)
- **Total Tests**: 45+
- **Target Coverage**: >90%
- **Browsers Tested**: Chromium, Firefox, WebKit
- **Mobile Devices**: iPhone SE, iPhone 12, iPad Mini

### 🎯 Critical User Flows Tested

1. **Authentication Flow**
   - User registration with validation
   - Login with valid/invalid credentials
   - Logout functionality
   - Session persistence

2. **Fortune Reading Flow**
   - Birth data form submission
   - Chart calculation and display
   - Fortune interpretation
   - Form validation

3. **Advisor Chat Flow**
   - Advisor selection (4 Lwa personalities)
   - Message sending and receiving
   - Advisor switching
   - Chat history

4. **Profile Management Flow**
   - Profile viewing and editing
   - Reading history display
   - User data updates
   - Pagination

5. **Navigation Flow**
   - Inter-page navigation
   - Protected route handling
   - Deep linking

## Test Suites

### 1. Critical Flows (`critical-flows.spec.ts`)

Tests all essential user journeys from registration to reading history.

**Key Tests**:

- Registration with unique email generation
- Login/logout cycle
- Fortune request with birth data
- Advisor chat interactions
- Profile updates
- Reading history pagination
- Protected route redirects

**Run**:

```bash
npx playwright test critical-flows.spec.ts
```

### 2. Performance Tests (`performance.spec.ts`)

Validates application performance meets targets.

**Performance Targets**:

- Page load: <3 seconds
- Fortune calculation: <1 second (calculation only)
- AI response: <3 seconds (target), <20 seconds (max)
- Client-side navigation: <500ms
- Bundle size: <5MB
- Memory usage: <100MB

**Key Tests**:

- Home/Fortune/Chat/Dashboard load times
- Fortune calculation performance
- Chat AI response time
- Navigation speed
- Image loading efficiency
- Memory leak detection
- Bundle size analysis

**Run**:

```bash
npx playwright test performance.spec.ts
```

### 3. Accessibility Tests (`accessibility.spec.ts`)

Ensures WCAG 2.1 AA compliance for all pages.

**Accessibility Standards**:

- WCAG 2.1 Level AA
- Keyboard navigation
- Screen reader compatibility
- Color contrast ratios
- Semantic HTML
- ARIA attributes

**Key Tests**:

- Automated axe-core scans on all pages
- Keyboard navigation functionality
- Form label associations
- Button accessible names
- Image alt text
- Color contrast validation
- Heading hierarchy
- Focus indicators
- Link distinguishability

**Run**:

```bash
npx playwright test accessibility.spec.ts
```

### 4. Mobile Responsiveness Tests (`mobile-responsive.spec.ts`)

Validates responsive design across all viewport sizes.

**Viewports Tested**:

- Mobile: 375px (iPhone SE)
- Tablet: 768px (iPad Mini)
- Desktop: 1440px

**Key Tests**:

- Layout adaptation across breakpoints
- No horizontal overflow
- Tap-friendly button sizes (min 44x44px)
- Mobile-friendly forms
- Touch interactions
- Font scaling
- Responsive images
- Landscape mode
- Hamburger menu (mobile)

**Run**:

```bash
npx playwright test mobile-responsive.spec.ts
```

## Quick Start

### Prerequisites

```bash
cd frontend
npm install
npx playwright install --with-deps
```

### Running Tests

**All tests (recommended)**:

```bash
npm run test:e2e
# or
npx playwright test
```

**Specific browser**:

```bash
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

**Specific test file**:

```bash
npx playwright test critical-flows.spec.ts
npx playwright test performance.spec.ts
npx playwright test accessibility.spec.ts
npx playwright test mobile-responsive.spec.ts
```

**With UI mode (debugging)**:

```bash
npx playwright test --ui
```

**Headed mode (see browser)**:

```bash
npx playwright test --headed
```

**Debug mode**:

```bash
npx playwright test --debug
```

### Using the Test Runner Script

The project includes a convenient bash script:

```bash
# Run all tests in chromium
./run-e2e-tests.sh

# Run all tests in firefox
./run-e2e-tests.sh firefox

# Run specific test file
./run-e2e-tests.sh chromium critical-flows.spec.ts

# Run performance tests only
./run-e2e-tests.sh chromium performance.spec.ts
```

## Test Reports

### HTML Report

After running tests, view the interactive HTML report:

```bash
npx playwright show-report
```

The report includes:

- Test results by browser
- Screenshots on failure
- Video recordings
- Test execution timeline
- Trace viewer for debugging

### JSON Report

Machine-readable results are in `test-results.json`:

```bash
cat frontend/test-results.json | jq
```

### CI/CD Reports

GitHub Actions automatically:

- Runs tests on push/PR
- Uploads test artifacts
- Comments on PRs with results
- Generates coverage reports

## Test Configuration

### Playwright Config (`playwright.config.ts`)

Key settings:

- **Base URL**: `http://localhost:3000`
- **Retries**: 2 on CI, 0 locally
- **Timeout**: 30s per test
- **Workers**: Parallel on local, sequential on CI
- **Reporters**: HTML, JSON, List
- **Screenshots**: On failure
- **Videos**: Retain on failure
- **Traces**: On first retry

### Environment Variables

Create `.env.test` in frontend directory:

```env
BASE_URL=http://localhost:3000
API_URL=http://localhost:8000
TEST_EMAIL=demo@rootsrevealed.com
TEST_PASSWORD=demo123
```

## Helper Utilities

### Auth Helpers (`e2e/helpers/auth.ts`)

- `registerUser()` - Register new test user
- `loginUser()` - Login with credentials
- `logoutUser()` - Logout current user
- `isAuthenticated()` - Check auth status
- `setupAuthenticatedSession()` - Setup session

### Utils (`e2e/helpers/utils.ts`)

- `waitForPageLoad()` - Wait for full page load
- `takeScreenshot()` - Capture screenshot
- `waitForAPIResponse()` - Wait for API call
- `fillField()` - Fill and validate input
- `isVisible()` - Check element visibility
- `mockAPIResponse()` - Mock API responses
- `setupMockAuth()` - Mock authentication

## Best Practices

### Writing Tests

1. **Use descriptive test names**:

   ```typescript
   test("should successfully login with valid credentials", async ({
     page,
   }) => {
     // ...
   });
   ```

2. **Use page object patterns for complex flows**:

   ```typescript
   const loginPage = new LoginPage(page);
   await loginPage.login(email, password);
   ```

3. **Make tests independent**:
   - Don't rely on test execution order
   - Setup/cleanup in each test
   - Use unique test data

4. **Use proper waits**:

   ```typescript
   await page.waitForLoadState("networkidle");
   await expect(page.locator(".result")).toBeVisible();
   ```

5. **Handle async operations**:
   ```typescript
   await Promise.all([page.waitForNavigation(), page.click("button")]);
   ```

### Debugging

**View test in browser**:

```bash
npx playwright test --headed --project=chromium
```

**Use debug mode**:

```bash
npx playwright test --debug
```

**Inspect specific test**:

```bash
npx playwright test critical-flows.spec.ts:10 --debug
```

**Generate trace**:

```bash
npx playwright test --trace on
npx playwright show-trace trace.zip
```

## Continuous Integration

### GitHub Actions Workflow

The `.github/workflows/e2e-tests.yml` workflow:

- Runs on push to main/master/develop
- Runs on pull requests
- Tests all browsers in parallel
- Uploads artifacts on failure
- Comments on PRs with results

### Running Tests in CI

Tests automatically run on:

- Push to main branches
- Pull request creation/update
- Manual workflow dispatch

View results in GitHub Actions tab.

## Maintenance

### Updating Tests

When adding new features:

1. Add test cases to appropriate spec file
2. Update this documentation
3. Ensure tests pass locally
4. Submit PR with tests
5. Verify CI passes

### Test Data Management

- Use demo accounts: `demo@rootsrevealed.com`
- Generate unique emails: `test-${Date.now()}@example.com`
- Mock API responses for unreliable endpoints
- Clean up test data after runs

### Keeping Dependencies Updated

```bash
cd frontend
npm update @playwright/test
npx playwright install
```

## Troubleshooting

### Common Issues

**Issue**: Dev server not starting

```bash
# Manually start dev server
npm run dev
# Then run tests in another terminal
npx playwright test
```

**Issue**: Browser not installed

```bash
npx playwright install chromium
# or install all browsers
npx playwright install
```

**Issue**: Tests timing out

- Check if API is running
- Increase timeout in test
- Check network conditions

**Issue**: Tests flaky

- Use proper waits (`waitForLoadState`)
- Don't use `setTimeout`
- Mock unreliable APIs
- Increase retry count in config

## Metrics & Goals

### Current Coverage

- **Critical Flows**: 13+ tests
- **Performance**: 10 tests
- **Accessibility**: 15+ tests
- **Mobile Responsive**: 20+ tests
- **Total**: 45+ tests

### Quality Targets

- ✅ >90% test coverage
- ✅ WCAG 2.1 AA compliance
- ✅ <3s page load times
- ✅ Mobile-first responsive design
- ✅ Cross-browser compatibility

## Resources

- [Playwright Documentation](https://playwright.dev/)
- [Axe Accessibility Testing](https://www.deque.com/axe/)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Vitals](https://web.dev/vitals/)

## Support

For issues or questions:

1. Check this documentation
2. Review test failures in CI
3. Run tests locally with `--debug`
4. Check Playwright docs
5. Open GitHub issue with details

---

**Last Updated**: 2025-01-29
**Version**: 1.0.0
**Status**: ✅ Ready for QA
