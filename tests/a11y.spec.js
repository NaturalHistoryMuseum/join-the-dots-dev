import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const PAGES = [
  '/',
  '/about',
  '/reports',
  '/view-units',
  '/view-unit',
  '/account',
  '/rescore',
  '/admin',
  '/manage-unit-permissions',
  '/user-management',
  '/help',
];

// Accessibility test for each page
for (const path of PAGES) {
  // Starts the test from playwright with the title, including the path
  test(`Accessibility check: ${path}`, async ({ page }) => {
    // Navigate to the page
    await page.goto(`http://localhost:4173${path}`);

    const results = await new AxeBuilder({ page }).analyze();

    if (results.violations.length > 0) {
      console.log(results.violations);
    }

    expect(results.violations).toEqual([]);
  });
}
