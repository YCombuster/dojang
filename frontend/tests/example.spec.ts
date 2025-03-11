import { test, expect } from '@playwright/test';

test('homepage has correct title', async ({ page }) => {
    await page.goto('/');

    // Verify the page title
    await expect(page).toHaveTitle(/Study AI/);
});

test('homepage loads successfully', async ({ page }) => {
    await page.goto('/');

    // Check if the page loaded successfully
    await expect(page.locator('body')).toBeVisible();
});

test('navigation works', async ({ page }) => {
    await page.goto('/');

    // This test will need to be updated based on your actual navigation elements
    // For now, it's a placeholder
    // Example: await page.click('text=About');
    // await expect(page).toHaveURL(/.*about/);
});
