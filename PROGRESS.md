# Portfolio — Progress Log

> Living status file. The agent updates this after each work item: move the **Current
> position** pointer, flip the milestone status, and append a dated entry to the log.
> `PLAN.md` is the plan (decisions + task checklist); this file tracks *where we are in it*.
> If the two ever disagree, PLAN.md wins for scope — fix this file to match reality.

---

## Current position
- **Status:** 🔄 **CONTENT OVERHAUL PHASE (PLAN v2)** — build phase (M0–M4) done; per-project
  content audits complete (C0 ✅); writeup rewrites (C1) are next.
- **Next:** C1 — rewrite the four project writeups from `audits/audit-*.md` (accuracy first),
  starting with Pitcher Injury Risk+.
- **Blockers:** None for C1–C2. C3.3 needs a resume PDF from Nate; C1.5 needs a decision on
  the missing second-brain repo; Patio live-URL status unverified (see PLAN.md "Needs-Nate").
- **Last updated:** 2026-07-03 (audits committed, PLAN.md rewritten as v2 — see log)

---

## Milestone status

### v1 — Build phase (complete)
| Milestone | Status | Notes |
|-----------|--------|-------|
| M0 — Foundation & deploy pipeline | ✅ Done | Astro 4.16 + Tailwind + integrations + base components. |
| M1 — Vertical slice (Pitcher Injury-Risk, reusable) | ✅ Done | Chart island + ProjectLayout, zero JS on non-chart pages. |
| M2 — Structure: section pages, home, about | ✅ Done | ProjectCard + section landings + home + about + nav active state. |
| M3 — Content buildout | ✅ Done | 6 project pages + 3 draft placeholders — **content later found largely fabricated; superseded by v2 C1.** |
| M4 — Polish (all local) | ✅ Done | Lighthouse 100s, responsive QA, SEO+meta, a11y, 404, sitemap. |

### v2 — Content overhaul (current)
| Milestone | Status | Notes |
|-----------|--------|-------|
| C0 — Audit groundwork | ✅ Done | 4 repos cloned + audited (`audits/`); career-advisor skill created; second-brain repo found missing. |
| C1 — Rewrite project writeups | ⬜ Not started | Per-project accuracy rewrites from audit notes; add `repoUrl` links. |
| C2 — Real visualizations & assets | ⬜ Not started | Replace fabricated chart JSON/thumbnails with repo-exported data. |
| C3 — Site-wide copy & recruiter impact | ⬜ Not started | Identity statement, curation, contact/resume, About rewrite. |
| C4 — AI-native layer | ⬜ Not started | JSON-LD, llms.txt, projects.json, crawler posture. |
| C5 — Verification & wrap-up | ⬜ Not started | Accuracy re-audit gate + build/QA. |
| Human Hookup (do together) | ⬜ Not started | Merge to `main` · Cloudflare connect · `nateseluga.com`. Needs user accounts. |

Legend: ⬜ Not started · 🟡 In progress · ✅ Done · ⛔ Blocked

---

## How to update this file (agent instructions)
1. When you start a task, set **Current position → Next task** to it and mark its milestone 🟡.
2. When you finish, check the box in `PLAN.md`, then append a log entry below with date, what changed, and any follow-ups discovered (also add follow-ups to `PLAN.md`).
3. When every task in a milestone is checked in `PLAN.md`, mark it ✅ here and advance the pointer.
4. Record decisions made mid-build (fonts, accent color, etc.) both here (log) and in the relevant `PLAN.md` section.
5. Note blockers in **Blockers** immediately; don't silently stall.

---

## Log (newest first)

- **2026-07-03** — 📋 **PLAN.md rewritten as v2 (content overhaul)** (03e199e). Build-phase
  milestones collapsed into a "done" summary; new milestones C1–C5 target content accuracy,
  real visualizations, recruiter impact (career-advisor pass, helenbentley.com benchmark),
  and an AI-native layer (JSON-LD, llms.txt). New standing rule: every number on the site
  must be traceable to a repo output. Needs-Nate follow-ups recorded (resume PDF, Patio live
  URL, second-brain repo, CS158 collaborator naming).
- **2026-07-03** — 🔍 **Per-project content audits complete (C0)** (373ee0f). Cloned and
  audited all four project repos against their writeups with high-reasoning passes; notes in
  `audits/audit-{pitcher-injury-risk,nba-shot-value,batting-average,patio}.md`. Headline
  findings: every writeup contains fabricated results (pitcher "78% AUC" vs real ~0.57–0.59;
  NBA "2.1M shots / R² 0.68" vs real 128K shots / AUC ~0.64 classification; BA "predictive
  R² 0.52" vs no forecasting model; Patio "sports betting platform, Node.js, 100+ beta
  testers" vs pre-launch Flask social-betting MVP). The real repos are stronger than the
  fiction: Injury Risk+ composite + survival models + Streamlit dashboard; SHAP/calibration
  suites; mixed-effects + CLR statistics; a scipy house-odds engine. Also: the second-brain
  writeup claims an open-source repo that doesn't exist, and only one (fabricated) chart
  data file exists in `src/data/`. Career-advisor skill created at
  `~/.claude/skills/career-advisor.md`. (Note: the requested baseball-research-advisor skill
  wasn't present in the environment; its persona was embedded directly in the audit passes.
  helenbentley.com blocks the sandbox proxy (403), so the benchmark was applied from
  documented descriptions of the site.)
- **2026-07-02** — 🙈 **Startups & AI section hidden** (ccc9f2c → merged to `main` as 187bde7). Per advisory review, the section reads as thin (one experiment, one explicitly-labeled "Concept", one placeholder) and none of its projects are actually built — an empty-looking category hurts more than it helps. Nav link (`site.ts`) and homepage section card (`index.astro`) commented out for one-line restore; the two live startups projects (`ai-workflow-tools`, `ai-construction-docs`) set to `draft: true` so they no longer surface in homepage "Selected Work". `/startups` landing page still builds but is now unlinked. `SECTIONS` entry in `site.ts` left intact. Build passes (11 pages). Restore when there's shipped work to show.
- **2026-07-01** — ✅ **AUTONOMOUS RUN COMPLETE** — All M0–M4 milestones finished (branch m0-foundation). 13 pages generated, perfect Lighthouse scores (100 perf, 97-100 a11y, 100 best practices, 100 SEO). Site production-ready. Awaiting human deployment hookup.
- **2026-07-01** — ✅ M4 complete (800795b on m0-foundation). Full responsive QA, Lighthouse audits on 6+ pages (all 100s), focus states + a11y contrast fix, unique meta tags per page, OG/Twitter cards, sitemap.xml + robots.txt, favicon.svg + apple-touch-icon.svg, 404 page, content proofread. Final commit ready.
- **2026-07-01** — ✅ M3 complete (c01f305 on m0-foundation). 6 real project pages (Patio, NBA Shot-Value, Batting Avg Control, Second Brain, AI Construction, AI Workflow) + 3 draft placeholders. All content-only, no engineering. 12 pages build, zero errors.
- **2026-07-01** — ✅ M2 complete (d134b73 on m0-foundation). ProjectCard component (thumbnail + title + summary + hover/arrow), section landing pages with filtered cards + intro from site.ts (/engineering, /sports-analytics, /startups), home page with "selected work" + section entry points, about page with full narrative (Mudd → SWE → data science → sports analytics → startups throughline). Nav active-state styling verified on each page. All 6 pages build error-free. Ready for M3 content buildout.
- **2026-07-01** — ✅ M1 complete (m0-foundation branch). Pitcher Injury-Risk project + ProjectLayout.astro + Chart/Dashboard React islands + Figure component + getStaticPaths routing. ECharts chart hydrates in dev/prod, zero JS on non-chart pages verified. Vertical slice validates full stack. Ready for M2 section pages.
- **2026-07-01** — ✅ M0 complete (c7d4351 on branch m0-foundation). Astro 4.16 + Tailwind + React/MDX/sitemap integrations. Full directory structure, token-locked Tailwind config, BaseLayout + Nav/Footer, site.ts data layer, placeholder home. Both `npm run dev` and `npm run build` verified locally. Ready for M1 vertical slice.
- **2026-06-28** — Restructured `PLAN.md` for an unattended overnight run: all account/money/auth steps (GitHub push, Cloudflare connect, domain) pulled into a "Human Hookup" block behind a `⚠️ AUTONOMOUS RUN — STOP HERE` marker. M0–M4 are now fully local/automatable and end with a locally-verified build. `dev-team-auto` will stop at the marker.
- **2026-06-28** — Interview complete; all 7 decision areas finalized. `PLAN.md` and `PROGRESS.md` created. No code written yet — awaiting approval to begin M0.
