# Project Standards

Project-specific efficiency, reliability, and resilience conventions for this Astro portfolio site. These extend the global standards in `~/.claude/skills/dev-team/code-standards.md`.

## Content Schema

- **Optional fields for backward compat**: New fields added to the Zod projects schema (`src/content/config.ts`) must be `.optional()` so existing MDX files that omit them continue to validate without changes.
- **No breaking schema additions**: Adding a required field to the collection schema is a breaking change — every existing `.mdx` file in `src/content/projects/` must be updated to include it, or the build will throw a validation error.

## MDX Imports

- **Remove imports with no current JSX usage**: MDX files that import a component but never render it should have the import removed. Astro's MDX compiler does not error on unused imports, but they are dead weight and mislead future editors about what the file renders. Exception: an import may be left in place only when a `{/* TODO: wire up at <task> */}` comment immediately below it names the specific future task that will use it.

## External Links

- **External link attributes**: Every URL field rendered as a link in ProjectLayout must include `target="_blank" rel="noopener noreferrer"`. ProjectLayout already follows this for `repoUrl`; apply the same pattern when wiring up `liveUrl` or any future URL field.
- **New-tab screen reader signal**: Links that open in a new tab should carry `aria-label="[visible text] (opens in new tab)"` so assistive technology users know a new context will be created.

## URL Schema Validation

- **Restrict URL fields to http/https**: URL fields in the projects Zod schema must use `.url().refine(v => /^https?:\/\//i.test(v), 'Must be an http/https URL')` rather than bare `.url()`. Zod v3's `.url()` validator accepts `javascript:` URIs; the refine restricts values to http/https and prevents non-web schemes from passing build-time validation.

## ECharts Charts in MDX

- **Y-axis baseline**: ECharts comparison bar charts must start the y-axis at 0 unless a non-zero baseline is explicitly labeled (via `subtext`, a `markLine` note, or axis `name`). Truncated axes exaggerate visual differences — especially sensitive on a portfolio piece where the chart is primary evidence.
- **Aria-label for chart data**: `Chart.tsx` derives `aria-label` from `option.title?.text`, which identifies the chart but does not convey data values. When a chart is the primary evidence for a quantitative finding, wrap the `ChartWrapper` in a `<figure>` with a `<figcaption>` listing the key values, or pass an explicit `ariaLabel` prop (requires adding the prop to ChartWrapper/Chart) with a data summary.
