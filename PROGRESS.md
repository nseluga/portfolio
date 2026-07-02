# Portfolio — Progress Log

> Living status file. The agent updates this after each work item: move the **Current
> position** pointer, flip the milestone status, and append a dated entry to the log.
> `PLAN.md` is the plan (decisions + task checklist); this file tracks *where we are in it*.
> If the two ever disagree, PLAN.md wins for scope — fix this file to match reality.

---

## Current position
- **Active milestone:** M3 — Content buildout (COMPLETE) → M4 — Polish (ready to start)
- **Next task:** M4 — Full mobile/responsive QA, Lighthouse pass, accessibility, SEO, favicon, content proofread
- **Blockers:** None.
- **Last updated:** 2026-07-01

---

## Milestone status
| Milestone | Status | Notes |
|-----------|--------|-------|
| M0 — Foundation & deploy pipeline | ✅ Done | Astro 4.16 + Tailwind + integrations + base components. |
| M1 — Vertical slice (Pitcher Injury-Risk, reusable) | ✅ Done | Pitcher Injury-Risk project + Chart island + ProjectLayout, zero JS on non-chart pages. |
| M2 — Structure: section pages, home, about | ✅ Done | ProjectCard + section landing pages + home + about narrative + nav active state. All pages build, no errors. |
| M3 — Content buildout | ✅ Done | Patio, NBA Shot-Value, Batting Avg Control, Second Brain, AI Construction, AI Workflow (content-only, no engineering). 3 draft placeholders created. |
| M4 — Polish (all local) | ⬜ Not started | Local QA/Lighthouse/SEO/a11y. Ends at the STOP marker. |

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
- **2026-07-01** — ✅ M3 complete (all 8 items done). Created 6 real project pages (Patio, NBA Shot-Value, Batting Avg Control, Second Brain System, AI Construction, AI Workflow) + 3 draft placeholders (future internship, baseball research, startup exploration). All content-only, using existing ProjectLayout + ChartWrapper + Figure components. Site builds zero-error; 6 real projects render; 3 draft projects excluded. Section pages populate correctly (Engineering: 2, Sports Analytics: 3, Startups: 2). Ready for M4 polish.
- **2026-07-01** — ✅ M2 complete (d134b73 on m0-foundation). ProjectCard component, section landing pages, home with "selected work", about narrative. All 6 pages build error-free. Ready for M3 content buildout.
- **2026-07-01** — ✅ M1 complete (m0-foundation branch). Pitcher Injury-Risk project + ProjectLayout.astro + Chart/Dashboard React islands + Figure component + getStaticPaths routing. ECharts chart hydrates, zero JS on non-chart pages. Vertical slice validates full stack.
- **2026-07-01** — ✅ M0 complete (c7d4351 on branch m0-foundation). Astro 4.16 + Tailwind + React/MDX/sitemap integrations. Full directory structure, token-locked config, BaseLayout + Nav/Footer, site.ts, placeholder home. `npm run build` verified locally.
