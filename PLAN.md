# Portfolio Website — Plan (v4)

> Source of truth for remaining work. V0–V8 complete. Two items left before deployment.

---

## Status

- **Complete:** Astro SSG + Tailwind + MDX + ECharts + AI-native layer. 12 pages, clean build. All project pages written in-voice with real data (V0–V8 done).
- **Next (run 1):** V9 — analytics accuracy + visualization pass, via `dev-team-auto` with baseball-researcher loop.
- **Then (run 2):** V10 — visual polish via Fable + Claude Computer Use (launch from Claude app with Fable selected).
- **Then:** Human Hookup (GitHub → Cloudflare Pages → `nateseluga.com`).
- **Startups & AI section:** Hidden until shipped work exists.

---

## Finalized decisions

| Area | Decision |
| --- | --- |
| **Framework** | Astro, static output; interactivity via React islands only. |
| **Content model** | MDX via Content Collections; `section` frontmatter enum; global data in `src/data/`. |
| **Styling** | Tailwind, locked tokens, hand-built components, self-hosted fonts. |
| **Visualizations** | ECharts in `client:visible` islands; data pre-computed offline → JSON committed to `src/data/`; browser never computes. All chart data must be exported from actual notebook outputs. |
| **Live apps** | Outbound links only ("View live ↗"). |
| **Deployment** | Cloudflare Pages on push to `main`; `nateseluga.com`. |

### Design guardrails

- Minimal, elegant, typography-led, high whitespace. Content _is_ the design.
- Muted-gray labels, near-black body, one accent used sparingly, near-white background.
- **Avoid:** hero splashes, gradients, decorative shapes, resume-card templates, skill bars, testimonial carousels, walls of text.
- **Accuracy rule:** no number, method, or artifact appears on the site unless it is traceable to a notebook or repo output. When content changes, update `llms.txt` and per-page meta in the same pass.

---

## Remaining work

### V9 — Analytics accuracy + visualization pass · `status: done` · `track: full`

**Scope is narrow and hard-bounded.** The agent only touches the two categories below. Everything else is Naté's decision and must not be changed.

**What the agent owns (non-subjective):**
- Exact metric values and model results: AUC, C-index, R², MAE, ICC, feature importances, n counts, p-values, calibration scores — verify each against actual notebook cell outputs and correct any discrepancy.
- Modeling approach descriptions: verify that what the prose says was done matches what the code actually does (e.g. "walk-forward CV" → confirm the notebook uses temporal splits, not shuffled).
- Chart data: export real outputs from notebooks into `src/data/` JSON files, replace any fabricated or unverified inline chart data with values from actual notebook cells. Source field (`_source`) must name the notebook and cell/section.

**What Nate owns — do not touch:**
- Project motivation and "why it matters" framing
- Opening summary and problem statement
- Interpretation of what results mean for the sport/domain
- Visualization type choice (which chart, what it shows)
- Any sentence that is primarily about framing or emphasis rather than stating a number

**Files in scope (analytics only):**
- `src/content/projects/pitcher-injury-risk.mdx` + `src/data/pitcher-injury-risk.json`
- `src/content/projects/nba-shot-value.mdx` (needs `src/data/nba-shot-value.json` created)
- `src/content/projects/batting-average-control.mdx` (needs `src/data/batting-average-control.json` created)

**Notebooks to read (local):**
- Pitcher: `/Users/nateseluga/Pitcher-Injury-Risk/notebooks/` — read all relevant notebooks; NB11 (`11_baseball_specific_insights.ipynb`) is the source for visualization numbers on the site.
- NBA: `/Users/nateseluga/Downloads/Shot-Value-Machine-Learning/notebooks` — the current shot value visualizations
are incorrect compared to the notebook.
- BAA: find the batting-average-ability notebooks (check `~/batting-average-ability/` or similar); the Arraez 133.2 and Gallo 61.2 values need to be verified.

**Software projects — out of scope for deep accuracy work.** Patio, OS workflow, and project dashboard do not have the same depth requirement. Verify only that each has: a clear one-paragraph explanation of what it is, the stack/systems used, and a working link to the repo or live app. No deep methodological accuracy pass.

**Loop mechanic:** For each analytics project in sequence:
1. Read the notebooks fully. Extract all metric values and model descriptions.
2. Read the corresponding MDX page.
3. Use `baseball-research-advisor` to compare: flag every place where the prose states a number, a method, or a model behavior that does not match what the notebook actually shows.
4. Fix discrepancies in the prose and update/create the corresponding JSON data file with real notebook output.
5. Rebuild and confirm build clean.

- **done when:** Build clean. Every metric and model description in the three analytics pages is traceable to a specific notebook cell. Fabricated chart data replaced with real exports. `src/data/` JSON files updated with `_source` fields naming the notebook and section. `baseball-research-advisor` review passes for each page with no remaining factual discrepancies.

---

> **⚠️ AUTONOMOUS RUN — STOP HERE**

_V9 is run 1. V10 below requires Fable + Claude Computer Use and must be launched from the Claude app with Fable selected._

---

### V10 — Visual polish pass · `status: not started` · `track: full`

> **How to run:** Open the Claude app, select Fable as the model, then run `/dev-team-auto`.
> Fable acts as the orchestrator and visual decision maker — it views the actual rendered site
> via Claude Computer Use and uses that visual judgment to direct fixes. Sub-agents
> (`dt-engineer`, `dt-qa`, `dt-fix`) use their standard models for implementation.

The site is functionally clean but looks stock Tailwind. This pass elevates the visual quality to match a strong reference point.

**Reference:** `https://brittanychiang.com/#projects` — study the typography, spacing, card layout, and color use. The goal is that level of visual polish: opinionated but restrained, high whitespace, every element placed deliberately. Not a copy — apply the same quality bar to the existing minimal/muted aesthetic.

- **task:** Open the local dev server (`npm run dev`) in Chrome via Claude Computer Use. Do a visual audit of the homepage, engineering section, a sports-analytics project page, and the about page. Compare against the reference site's quality bar. Then fix in order:

  1. **Typography** — The current font stack is generic Tailwind system fonts. Choose and wire a characterful typeface for headings (geometric sans-serif like Inter/Geist at heavy weight, or a light-weight serif like DM Serif Display) while keeping body text clean. The reference site's heading treatment is a good model — weight and size contrast that makes hierarchy instantly readable.
  2. **Spacing and layout** — Identify any sections where content feels cramped or floated without intention. The reference site has very deliberate section breathing room and card padding. Fix so every spacing decision looks chosen, not default.
  3. **Project cards and section landing pages** — The cards are the primary recruiter touchpoint. Compare card treatment against the reference: does each card communicate clearly at a glance? Does hover state feel polished? Are labels and metadata visually subordinate to the project name?
  4. **Visual bugs** — Fix overlapping text, clipped labels, misaligned elements, or layout breaks at 375px mobile and 1280px desktop.

  Use Fable's visual judgment throughout: view the rendered page, identify issues against the reference bar, direct `dt-engineer` to implement, verify visually before marking resolved. Do not mark a fix done without visual confirmation.

- **done when:** Build clean. No overlapping or clipped elements at 375px and 1280px. Typography has clear hierarchy and personality beyond default Tailwind. Spacing looks deliberate throughout. Project cards read clearly at a glance. Fable's final visual review confirms the site reads as polished, not generic, at the reference quality bar.

---

> **⚠️ AUTONOMOUS RUN — STOP HERE**

_Everything below requires user accounts/money/auth and cannot run unattended._

---

## Human Hookup (do together — ~15 min)

- [ ] **GitHub:** merge working branch → `main`.
- [ ] **Cloudflare Pages:** connect repo, build `npm run build`, output `dist`, verify `*.pages.dev` deploy.
- [ ] **Domain:** register `nateseluga.com` (Cloudflare Registrar), attach, DNS + SSL, redirect.
- [ ] **Verify live:** Lighthouse against live URL; charts hydrate; zero JS on non-chart pages.
- [ ] Optional: Cloudflare Web Analytics.

## Needs-Nate

- [ ] Patio: confirm whether a live deploy exists (link or cut the placeholder); capture real UI screenshots.
- [ ] LinkedIn URL — add to contact block when available.
- [ ] Resume PDF — add to `public/resume.pdf` and uncomment link when updated.
- [ ] BAA page: decide whether to add an IR+-style leaderboard chart (real data is in the BAA notebooks once located) or keep the current two-row table.
- [ ] Review V9 output: the accuracy pass will not touch motivation, problem framing, or "why it matters" sections — those sections should be reviewed by Nate after V9 completes.

---

## Conventions (for the agent)

- Reusable components in `src/components/`; layouts in `src/layouts/`; project MDX in `src/content/projects/`; chart JSON in `src/data/`; static visuals in `public/`.
- Never compute analytics in the browser — commit pre-aggregated JSON **exported from the actual project notebooks** (note the generating notebook and section in a JSON `_source` field).
- Every new project addable via content only; component gaps get fixed, not hacked around.
- Keep zero-JS on any page without an intentional island.
- **Style rule:** all analytics writeups follow the voice in `~/os/knowledge/library/style_reference/` — specific, evidence-driven, honest about scope. When touching copy, compare against this reference.
- **Accuracy rule:** no number, method, or artifact appears on the site unless traceable to a notebook output. When content changes, update `llms.txt` and per-page meta in the same pass.
