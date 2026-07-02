import { defineCollection, z } from 'astro:content';

/**
 * Zod schema for the projects collection
 * Defines the structure of all .mdx files in src/content/projects/
 */
const projects = defineCollection({
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    section: z.enum(['engineering', 'sports-analytics', 'startups']),
    date: z.date(),
    summary: z.string(), // one-liner for cards
    thumbnail: z.string().optional(), // path to image
    liveUrl: z.string().url().optional(), // optional link to live app
    draft: z.boolean().default(false),
    order: z.number().default(0),
    // Optional section-specific fields can be added per project
  }),
});

export const collections = {
  projects,
};
