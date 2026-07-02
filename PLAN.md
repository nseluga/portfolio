# Portfolio Website — Implementation Plan & Working TODO

> Working document for the agent building this site. Update it every pass: check off
> completed items, add follow-ups as they surface, keep it an accurate picture of remaining
> work. Source of truth for *what/why/feel* is `portfolio-brief.md`; this file is *how*.

---

## Finalized Decisions (context for every pass)

| Area | Decision |
|------|----------|
| **Framework / rendering** | **Astro**, static output (SSG). Zero-JS baseline; interactivity via islands only. |
| **Content model** | **MDX** via Astro Content Collections. One `projects` collection with a Zod schema. `section` is a frontmatter enum, not a separate collection. Global data (nav, socials, section intros) in `src/data/`. |
| **Routing / structure** | **Per-section** landing pages + URLs. `/engineering`, `/sports-analytics`, `/startups` each render from the shared collection filtered by section, with a tailored intro. Project pages at `/[section]/[slug]`. Plus `/` (home) and `/about`. |
| **Styling** | **Tailwind CSS** with a tightly-locked token config (constrained type scale, muted-gray + near-black + one accent, generous spacing). Small set of hand-built Astro components. **No prebuilt UI kit** (template-look trap). Self-hosted fonts via `@fontsource` (non-default heading/body pairing chosen in design pass). |
| **Visualizations** | **ECharts** (`echarts-for-react`) as the single charting/dashboard engine, rendered in **React islands** (`client:visible`). Data is **pre-computed offline in Python → compact JSON committed to repo**; the browser only renders, never computes, no backend. Inline interactive viz is a first-class goal. |
| **Live apps / big dashboards** | **Outbound links only** ("View live ↗"). Patio and any full dashboard app are linked, not embedded. Prefer a muted screen-recording over fragile live embeds. |
| **Deployment / hosting** | **Cloudflare Pages**, auto-deploy on push to **`main`**. Single-branch workflow (no PR previews for now). Custom domain **`nateseluga.com`** (register via Cloudflare Registrar). |
| **Build strategy** | **Vertical-slice-first (B)** with a thin design pass up front. The slice validates the full pipeline but is built with **generic, reusable, scalable components** — nothing hardcoded to one project. Adding a future project = drop an MDX file + JSON, no engineering. |

### Design guardrails (from the brief — enforce on every visual choice)
- Minimal, elegant, typography-led, high whitespace. Content *is* the design.
- read.cv is the **content** north star (structured, muted labels, inline preview cards) — **not** a visual clone.
- Muted-gray dates/labels, near-black body, one accent used sparingly, near-white background.
- Subtle interaction cues (small link arrows, gentle hover), restrained animation.
- **Avoid:** loud hero splashes, gradients, decorative shapes/dots, resume-card templates, skill bars/progress meters, testimonial carousels, "What I'm Doing" service grids, walls of text.
- Content rule: evidence over claims; show the artifact, don't describe it; depth over quantity.

### Project page structure (every project MDX answers, in order)
1. The Problem  2. Why It Matters  3. My Approach  4. Results (with visuals)  5. Key Takeaways

### Sections & planned projects
- **Software Engineering:** Patio (flagship, links out to live app), Second Brain System. + future/internship placeholders.
- **Sports Analytics:** Pitcher Injury-Risk Model (anchor credibility piece; has inline ECharts viz), NBA Shot-Value (spatial court chart), Batting Average Control Stat. + future placeholders.
- **Startups & AI:** AI Construction Documentation, AI Workflow Tools / Second-Brain. (None complete yet — mark as concepts/WIP.) + future placeholders.

---

## Milestones & Tasks

### M0 — Foundation & deploy pipeline
- [ ] `npm create astro@latest` — minimal/empty template, TypeScript strict.
- [ ] Add integrations: `@astrojs/tailwind`, `@astrojs/mdx`, `@astrojs/react`, `@astrojs/sitemap`.
- [ ] Add `echarts` + `echarts-for-react`, `@fontsource/*` (fonts TBD in design pass).
- [ ] Create the target directory structure on top of the Astro scaffold (create dirs + `.gitkeep` where empty):
  ```
  src/
    components/        # hand-built Astro components (Nav, Footer, ProjectCard, Figure)
      charts/          # React island wrappers (Chart, Dashboard) — ECharts
    layouts/           # BaseLayout.astro, ProjectLayout.astro
    content/
      projects/        # one .mdx per project
      config.ts        # Zod schema for the projects collection
    data/              # site.ts (nav/socials/section intros) + per-project chart JSON
    pages/
      index.astro
      about.astro
      [section]/
        index.astro    # section landing (filtered by section)
        [slug].astro    # project page (getStaticPaths over collection)
    styles/            # global.css + token layer
  public/              # favicons, og images, static visuals, screen-recordings
  ```
- [ ] Tailwind token config: locked color palette (near-white bg, near-black text, muted gray, one accent), constrained type scale, spacing scale. Document tokens inline.
- [ ] Global styles + typographic base (`src/styles/global.css`).
- [ ] `BaseLayout.astro`: `<head>` meta, fonts, skip-link, Nav, Footer, `<slot/>`.
- [ ] `Nav` + `Footer` components (section links, About, socials from `src/data/site.ts`).
- [ ] `src/data/site.ts`: nav, socials, section definitions/intros.
- [ ] Placeholder home (`/`) so the site renders.
- [ ] Init git branch workflow on `main`; connect repo to Cloudflare Pages; verify auto-deploy on push.
- [ ] Confirm empty-but-styled site is live on the Cloudflare `*.pages.dev` URL.
- [ ] Follow-up: register `nateseluga.com` (deferred to M4 cutover, but reserve now if possible).

### M1 — Vertical slice (validate full stack on one real page, reusably)
- [ ] `src/content/config.ts`: Zod schema for `projects` collection — `title`, `slug`, `section` enum, `date`, `summary` (one-liner for cards), `thumbnail`, optional `metrics[]`, optional `liveUrl`, optional section-specific fields, `draft` flag, `order`.
- [ ] `ProjectLayout.astro`: renders the 5-part structure generically from any MDX (Problem → Why → Approach → Results → Takeaways scaffolding via headings/components, not hardcoded content).
- [ ] `<Figure>` component (image/SVG + caption) — the static-visual primitive.
- [ ] `<Chart>` / `<Dashboard>` React island wrapper: takes ECharts option + data JSON as props, `client:visible`, responsive, styled to token palette. Generic — no project knowledge.
- [ ] `src/pages/[section]/[slug].astro`: dynamic route using `getStaticPaths` over the collection.
- [ ] Build **Pitcher Injury-Risk** as the first slice: MDX content + one real interactive ECharts viz fed by committed JSON in `src/data/`.
- [ ] Deploy the slice; verify chart hydrates and site elsewhere stays zero-JS.

### M2 — Structure: section pages, home, about
- [ ] `<ProjectCard>` preview component (thumbnail + title + one-line context + hover/arrow cue).
- [ ] Section landing template rendering cards from the collection filtered by `section`, with intro from `site.ts`. Generate `/engineering`, `/sports-analytics`, `/startups`.
- [ ] Home `/`: concise intro + "selected work" (curated cross-section cards) + section entry points. No hero splash.
- [ ] `/about`: specific narrative per brief (Mudd → SWE → data science → sports analytics → startups throughline). Typography-led, no bio-card template.
- [ ] Nav reflects final sections; active-state styling.

### M3 — Content buildout (pour content through existing machinery)
- [ ] Patio project page (links out to live app; screen-recording/screenshots as visuals).
- [ ] NBA Shot-Value page + spatial ECharts court/heatmap viz (JSON).
- [ ] Batting Average Control Stat page + viz (JSON).
- [ ] Second Brain System page.
- [ ] AI Construction Documentation page (mark as concept/WIP).
- [ ] AI Workflow Tools / Second-Brain page (mark WIP).
- [ ] Add `draft: true` placeholder MDX for future/internship + future baseball/startup slots.
- [ ] Verify each new project needed **content only** (no component/engineering changes) — if not, note the gap here.

### M4 — Polish & launch
- [ ] Full mobile/responsive QA across breakpoints.
- [ ] Lighthouse pass: performance (verify islands don't leak JS to non-chart pages), a11y, best-practices, SEO.
- [ ] Accessibility: focus states, alt text on all visuals, color contrast, keyboard nav, chart fallbacks/descriptions.
- [ ] SEO/meta: per-page title/description, Open Graph + Twitter cards, generated OG images or a clean default, `sitemap`, `robots.txt`.
- [ ] Favicon / touch icons, 404 page.
- [ ] Register + connect `nateseluga.com` on Cloudflare; DNS + SSL; set as primary domain; redirect `*.pages.dev`.
- [ ] Final content proofread against content principles (kill any adjective-claims; ensure artifacts present).

---

## Open Follow-ups / Decisions Deferred
- [ ] Exact font pairing (heading + body) — decide in M0 design pass.
- [ ] Exact accent color — decide in M0 design pass.
- [ ] Which project(s) get a full interactive **dashboard** island vs a single chart.
- [ ] Contact method on the site (mailto vs. form — form would need a provider since no backend).
- [ ] Analytics? (Cloudflare Web Analytics is free + privacy-friendly if wanted.)

---

## Conventions (for the agent)
- Reusable components in `src/components/`; layouts in `src/layouts/`; project MDX in `src/content/projects/`; chart JSON in `src/data/`; static visuals in `public/` (or `src/assets/` if optimized).
- Never compute analytics in the browser — commit pre-aggregated JSON.
- Every new project should be addable via content only. If it isn't, that's a component gap to fix, not a one-off hack.
- Keep zero-JS on any page without an intentional island.
```
