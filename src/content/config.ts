import { defineCollection, z } from 'astro:content';

/**
 * Zod schema for the projects collection
 * Defines the structure of all .mdx files in src/content/projects/
 */
const projects = defineCollection({
  schema: z.object({
    title: z.string(),
    section: z.enum(['engineering', 'sports-analytics', 'startups']),
    date: z.date(),
    summary: z.string(), // one-liner for cards
    thumbnail: z.string().optional(), // path to image
    metrics: z.array(z.object({
      label: z.string(),
      value: z.string(),
    })).optional(), // optional key metrics display
    liveUrl: z.string().url().refine(v => /^https?:\/\//i.test(v), 'Must be an http/https URL').optional(), // optional link to live app
    repoUrl: z.string().url().refine(v => /^https?:\/\//i.test(v), 'Must be an http/https URL').optional(), // optional link to source repo
    collaborators: z.array(z.string()).optional(), // optional list of collaborators
    draft: z.boolean().default(false),
    order: z.number().default(0),
    // Optional section-specific fields can be added per project
    // Note: slug is auto-generated from filename by Astro; don't define it here
  }),
});

export const collections = {
  projects,
};
