# Portfolio — Progress Log

> Living status file. The agent updates this after each work item: move the **Current
> position** pointer, flip the milestone status, and append a dated entry to the log.
> `PLAN.md` is the plan (decisions + task checklist); this file tracks *where we are in it*.
> If the two ever disagree, PLAN.md wins for scope — fix this file to match reality.

---

## Current position
- **Active milestone:** M1 — Vertical slice ✅ COMPLETE
- **Next task:** M2 — Section landing pages + home + about
- **Blockers:** None.
- **Last updated:** 2026-07-01

---

## Milestone status
| Milestone | Status | Notes |
|-----------|--------|-------|
| M0 — Foundation & deploy pipeline | ✅ Done | Astro+Tailwind+components complete; site builds zero-error. |
| M1 — Vertical slice (Pitcher Injury-Risk, reusable) | ✅ Done | Full-stack project page with interactive ECharts. |
| M2 — Structure: section pages, home, about | 🟡 In progress | ProjectCard + section landing + home + about next. |
| M3 — Content buildout | ⬜ Not started | NBA Shot, Batting Avg, Patio, etc. content-only. |
| M4 — Polish & launch (domain cutover) | ⬜ Not started | `nateseluga.com` goes live here. |

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
- **2026-07-01** — M1 complete. Built full vertical slice validating schema, layout, components, dynamic routing, and island hydration. Pitcher Injury-Risk page live with ECharts chart hydrating on client:visible; non-chart pages ship zero JS. Build succeeds; all 7 checklist items done. Ready for M2.
- **2026-06-28** — Interview complete; all 7 decision areas finalized. `PLAN.md` and `PROGRESS.md` created. No code written yet — awaiting approval to begin M0.
