import AxeBuilder from '@axe-core/playwright';
import { expect, test } from '@playwright/test';

const PAGES = [
  // '/login',
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

// Use authenticated state for all tests
// test.use({ storageState: 'auth.json' });

// Accessibility test for each page
for (const path of PAGES) {
  // Starts the test from playwright with the title, including the path
  test(`Accessibility check: ${path}`, async ({ page }) => {
    // Navigate to the page
    await page.goto(`http://localhost:5173${path}`);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2aa', 'wcag2a'])
      .analyze();

    if (results.violations.length > 0) {
      console.log(results.violations);
    }

    expect(results.violations).toEqual([]);
  });
}
