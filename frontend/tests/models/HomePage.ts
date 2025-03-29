import { Page, expect } from '@playwright/test';

export class HomePage {
    readonly page: Page;

    constructor(page: Page) {
        this.page = page;
    }

    async goto() {
        await this.page.goto('/');
    }

    async getTitle() {
        return this.page.title();
    }

    async expectTitleContains(text: string) {
        await expect(this.page).toHaveTitle(new RegExp(text));
    }

    // Add more methods as needed for your specific application
    // For example:
    // async login(username: string, password: string) { ... }
    // async navigateToSection(sectionName: string) { ... }
}
