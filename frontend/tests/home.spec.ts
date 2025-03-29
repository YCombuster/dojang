import { test, expect } from '@playwright/test';
import { HomePage } from './models/HomePage';

test.describe('Home Page Tests', () => {
    test('should display the correct title', async ({ page }) => {
        const homePage = new HomePage(page);
        await homePage.goto();
        await homePage.expectTitleContains('Study AI');
    });

    test('should have visible content', async ({ page }) => {
        const homePage = new HomePage(page);
        await homePage.goto();

        // Check if the page has loaded with content
        await expect(page.locator('body')).not.toBeEmpty();
    });

    // Add more specific tests based on your application's functionality
});
