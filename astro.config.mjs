import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import mdx from '@astrojs/mdx';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://nateseluga.com',
  integrations: [
    tailwind(),
    mdx(),
    react(),
    // Sitemap is generated via robots.txt reference
  ],
});
