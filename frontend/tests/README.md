# Playwright Testing Framework

This directory contains end-to-end tests for the Study AI application using Playwright.

## Getting Started

### Prerequisites

-   Node.js (v16 or higher)
-   npm

### Running Tests

From the `frontend` directory, you can run the tests using the following commands:

```bash
# Run all tests
npm test

# Run tests with UI mode (for debugging)
npm run test:ui

# Run tests in debug mode
npm run test:debug

# Run tests in headed mode (visible browser)
npm run test:headed

# Run tests in a specific browser
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit
```

### Test Structure

-   `tests/` - Contains all test files
    -   `models/` - Page Object Models for better organization
    -   `example.spec.ts` - Basic example tests
    -   `home.spec.ts` - Tests for the home page

## Writing Tests

### Page Object Model

We use the Page Object Model pattern to organize our tests. Page objects are in the `tests/models/` directory.

Example:

```typescript
// Create a new test
test('my test', async ({ page }) => {
    const homePage = new HomePage(page);
    await homePage.goto();
    // Perform actions and assertions
});
```

### Best Practices

1. Use page objects for better organization
2. Keep tests independent
3. Use descriptive test names
4. Group related tests with `test.describe`
5. Use `beforeEach` for common setup

## CI/CD Integration

Tests are automatically run in GitHub Actions on push to main/master and on pull requests.

## Documentation

-   [Playwright Documentation](https://playwright.dev/docs/intro)
-   [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
