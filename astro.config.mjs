import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';
// import sitemap from '@astrojs/sitemap'; // Will be enabled when site is live

// https://astro.build/config
export default defineConfig({
  site: 'https://nateseluga.com',
  integrations: [
    tailwind(),
    mdx(),
    react(),
    // sitemap(), // TODO: Enable once site is deployed
  ],
});
