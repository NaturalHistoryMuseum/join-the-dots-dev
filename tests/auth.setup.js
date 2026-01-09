import { test } from '@playwright/test';

test('authenticate and save storage state', async ({ page }) => {
  // CI-only test login endpoint
  await page.request.post('http://127.0.0.1:5000/api/auth_test/test-login');

  // Go to frontend - ensure cookies are attached to browser context
  await page.goto('http://localhost:4173/');

  // Save cookies + localStorage
  await page.context().storageState({ path: 'auth.json' });
});
