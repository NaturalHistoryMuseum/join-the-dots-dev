import { request } from '@playwright/test';
import fs from 'fs';

export default async () => {
  const context = await request.newContext({
    baseURL: 'http://localhost:5000',
  });

  // Call CI-only login endpoint
  const response = await context.post('/__test/login');

  if (!response.ok()) {
    throw new Error('CI login failed');
  }

  // Save cookies + storage
  const storageState = await context.storageState();

  fs.writeFileSync('auth.json', JSON.stringify(storageState, null, 2));
};
