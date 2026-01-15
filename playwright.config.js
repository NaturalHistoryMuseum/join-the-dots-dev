import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',

  projects: [
    {
      name: 'setup',
      testMatch: /auth\.setup\.js/,
    },
    {
      name: 'chromium',
      use: {
        storageState: 'auth.json',
      },
      dependencies: ['setup'],
    },
  ],
});
