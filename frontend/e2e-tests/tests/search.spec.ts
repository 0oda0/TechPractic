import { test, expect } from '@playwright/test';

test('search returns results', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('input[placeholder="Enter search query..."]')).toBeVisible();
  await page.fill('input[placeholder="Enter search query..."]', 'test');
  await page.click('button:has-text("Find")');
  await page.waitForSelector('.result-card', { timeout: 5000 });
  const count = await page.locator('.result-card').count();
  expect(count).toBeGreaterThan(0);
});