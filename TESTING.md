# Testing Strategy and Guidelines

## Overview

This document outlines the comprehensive testing strategy for the Roots Revealed application, including unit tests, integration tests, and end-to-end tests.

## Testing Philosophy

- **Test Pyramid**: Heavy on unit tests, moderate integration tests, light E2E tests
- **Coverage Goals**: 80% backend, 70% frontend minimum
- **Test Quality**: Tests should be fast, reliable, and maintainable
- **Continuous Testing**: Tests run on every commit via CI/CD

## Testing Stack

### Backend Testing
- **Framework**: Jest with ts-jest
- **Integration**: Supertest for API testing
- **Coverage**: Istanbul/NYC
- **Mocking**: jest.mock() for external services

### Frontend Testing
- **Framework**: Jest with React Testing Library
- **Environment**: jsdom
- **Coverage**: Jest coverage with v8
- **Component Testing**: React Testing Library best practices

### End-to-End Testing
- **Framework**: Playwright
- **Browsers**: Chromium, Firefox, WebKit, Mobile devices
- **Parallel Execution**: Full parallelization support
- **Visual Testing**: Screenshots and videos on failure

## Test Organization

```
backend/
  src/
    __tests__/
      *.test.ts          # Test files
      testFixtures.ts    # Shared test data and utilities

frontend/
  src/
    **/__tests__/
      *.test.tsx         # Component tests

e2e/
  tests/
    *.spec.ts            # E2E test files
```

## Backend Testing Guidelines

### Unit Tests

Test individual functions and classes in isolation:

```typescript
describe('authenticateToken', () => {
  it('should authenticate valid token', () => {
    // Arrange
    const token = generateValidToken();
    
    // Act
    const result = authenticateToken(token);
    
    // Assert
    expect(result.user).toBeDefined();
  });
});
```

### Integration Tests

Test API endpoints with real HTTP requests:

```typescript
describe('POST /api/charts', () => {
  it('should create a new chart', async () => {
    const response = await request(app)
      .post('/api/charts')
      .set('Authorization', `Bearer ${token}`)
      .send(chartData);

    expect(response.status).toBe(201);
    expect(response.body.data).toHaveProperty('id');
  });
});
```

### Test Fixtures

Use shared fixtures for consistent test data:

```typescript
import { chartFixtures, userFixtures } from './testFixtures';

const chart = chartFixtures.validChart;
const user = userFixtures.validUser;
```

### Mocking

Mock external dependencies:

```typescript
jest.mock('../services/emailService', () => ({
  sendEmail: jest.fn().mockResolvedValue(true),
}));
```

## Frontend Testing Guidelines

### Component Tests

Test React components with React Testing Library:

```typescript
describe('ChartCard', () => {
  it('should render chart information', () => {
    render(<ChartCard chart={mockChart} />);
    
    expect(screen.getByText(mockChart.name)).toBeInTheDocument();
    expect(screen.getByText(/birth date/i)).toBeInTheDocument();
  });
  
  it('should call onDelete when delete button clicked', async () => {
    const onDelete = jest.fn();
    render(<ChartCard chart={mockChart} onDelete={onDelete} />);
    
    const deleteButton = screen.getByRole('button', { name: /delete/i });
    await userEvent.click(deleteButton);
    
    expect(onDelete).toHaveBeenCalledWith(mockChart.id);
  });
});
```

### Testing User Interactions

Use @testing-library/user-event for realistic user interactions:

```typescript
import userEvent from '@testing-library/user-event';

it('should handle form submission', async () => {
  const user = userEvent.setup();
  render(<LoginForm />);
  
  await user.type(screen.getByLabelText(/email/i), 'test@example.com');
  await user.type(screen.getByLabelText(/password/i), 'password123');
  await user.click(screen.getByRole('button', { name: /log in/i }));
  
  expect(screen.getByText(/success/i)).toBeInTheDocument();
});
```

### Async Testing

Wait for async operations:

```typescript
it('should load data', async () => {
  render(<ChartList />);
  
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  
  await waitFor(() => {
    expect(screen.getByText(/my chart/i)).toBeInTheDocument();
  });
});
```

## End-to-End Testing Guidelines

### Page Object Pattern

Create reusable page objects:

```typescript
class LoginPage {
  constructor(private page: Page) {}
  
  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}
```

### Test Isolation

Each test should be independent:

```typescript
test.beforeEach(async ({ page }) => {
  // Reset state
  await page.goto('/');
});

test.afterEach(async ({ page }) => {
  // Clean up
  await page.close();
});
```

### Waiting Strategies

Use appropriate waiting strategies:

```typescript
// Wait for navigation
await page.waitForURL('**/dashboard');

// Wait for element
await page.waitForSelector('[data-testid="chart"]');

// Wait for API response
await page.waitForResponse(response => 
  response.url().includes('/api/charts') && response.status() === 200
);
```

## Test Data Management

### Fixtures

Create reusable test fixtures:

```typescript
export const chartFixtures = {
  validChart: {
    name: 'Test Chart',
    birthDate: '1990-01-01',
    birthTime: '12:00',
    latitude: 40.7128,
    longitude: -74.0060,
  },
};
```

### Factories

Use factories for dynamic test data:

```typescript
export const generateUniqueEmail = () => 
  `test-${Date.now()}@example.com`;
```

### Database Seeding

Seed test database with known data:

```typescript
beforeAll(async () => {
  await seedDatabase(testData);
});

afterAll(async () => {
  await cleanDatabase();
});
```

## Running Tests

### Backend Tests

```bash
cd backend
npm test                 # Run all tests with coverage
npm run test:watch       # Watch mode
```

### Frontend Tests

```bash
cd frontend
npm test                 # Run all tests
npm run test:coverage    # Run with coverage
npm run test:watch       # Watch mode
```

### E2E Tests

```bash
cd e2e
npm test                 # Run all E2E tests
npm run test:headed      # Run with browser visible
npm run test:ui          # Interactive UI mode
npm run test:debug       # Debug mode
```

### All Tests

```bash
npm run test:all         # Run all tests (backend + frontend + E2E)
```

## CI/CD Integration

Tests run automatically on:
- Push to main, develop, or copilot/** branches
- Pull requests to main or develop

See `.github/workflows/ci.yml` for full configuration.

### Coverage Reports

Coverage reports are:
- Generated on every test run
- Uploaded to Codecov (if configured)
- Available as CI artifacts
- Displayed in PR comments

## Code Coverage Metrics

### Backend Coverage Targets (Current: 94.69%)
- Statements: 80%
- Branches: 80%
- Functions: 80%
- Lines: 80%

### Frontend Coverage Targets
- Statements: 70%
- Branches: 60%
- Functions: 60%
- Lines: 70%

### Current Coverage

**Backend**: 94.69% statements, 84.84% branches, 94.11% functions ✅ Exceeds all targets

**Frontend**: Check latest CI run for current metrics

## Best Practices

### Do's ✅

- Write tests before fixing bugs (TDD)
- Keep tests simple and focused
- Use descriptive test names
- Test edge cases and error conditions
- Mock external dependencies
- Use data-testid for E2E selectors
- Clean up after tests
- Run tests locally before pushing

### Don'ts ❌

- Don't test implementation details
- Don't share state between tests
- Don't use brittle selectors (CSS classes that may change)
- Don't skip tests in CI
- Don't commit failing tests
- Don't test third-party libraries
- Don't make tests dependent on execution order

## Testing Checklist

When adding new features:

- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Component tests for UI components
- [ ] E2E tests for critical user paths
- [ ] Test error handling
- [ ] Test edge cases
- [ ] Update test fixtures if needed
- [ ] Verify coverage thresholds
- [ ] All tests pass locally
- [ ] All tests pass in CI

## Debugging Tests

### Backend Tests

```bash
# Run specific test file
npm test -- auth.test.ts

# Run with verbose output
npm test -- --verbose

# Run single test
npm test -- -t "should authenticate valid token"
```

### Frontend Tests

```bash
# Run specific test file
npm test -- page.test.tsx

# Run with coverage
npm test -- --coverage --watchAll=false

# Debug in Chrome DevTools
node --inspect-brk node_modules/.bin/jest --runInBand
```

### E2E Tests

```bash
# Run in debug mode
npm run test:debug

# Run specific test
npx playwright test auth.spec.ts

# Run with UI
npm run test:ui
```

## Performance Testing

### Load Testing

For API endpoints, consider:
- Apache JMeter
- Artillery
- k6

### Frontend Performance

Monitor:
- Bundle size
- Load times
- Core Web Vitals

## Maintenance

### Regular Tasks

- Review and update test fixtures
- Remove obsolete tests
- Refactor duplicated test code
- Update snapshots when UI changes
- Keep testing dependencies up to date

### Test Health Metrics

Monitor:
- Test execution time
- Flaky test rate
- Coverage trends
- Test maintenance burden

## Resources

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [Testing Best Practices](https://testingjavascript.com/)

## Getting Help

- Check test output for error messages
- Review this documentation
- Check existing tests for examples
- Ask in team channels
- Create detailed bug reports for test failures
