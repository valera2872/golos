import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://somnori.com',
  output: 'static',
  trailingSlash: 'never',
  integrations: [sitemap()],
  compressHTML: true,
});
