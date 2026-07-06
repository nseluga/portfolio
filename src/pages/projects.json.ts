import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export const GET: APIRoute = async () => {
  const projects = await getCollection('projects', (p) => !p.data.draft);
  const sorted = projects.sort((a, b) => (b.data.order ?? 0) - (a.data.order ?? 0));

  const payload = sorted.map((p) => ({
    slug: p.slug,
    title: p.data.title,
    section: p.data.section,
    summary: p.data.summary,
    date: p.data.date.toISOString().slice(0, 10),
    repoUrl: p.data.repoUrl ?? null,
    collaborators: p.data.collaborators ?? [],
    metrics: p.data.metrics ?? [],
    url: `https://nateseluga.com/${p.data.section}/${p.slug}/`,
  }));

  return new Response(JSON.stringify({ projects: payload }, null, 2), {
    headers: { 'Content-Type': 'application/json' },
  });
};
