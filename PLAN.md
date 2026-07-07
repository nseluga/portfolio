# Portfolio Website — Manual Refinement Plan & Working TODO (v3)

> Working document for the agent building this site with Nate. Update it every pass: check off
> completed items, add follow-ups as they surface, keep it an accurate picture of remaining
> work. Source of truth for _what/why/feel_ is `portfolio-brief.md`; this file is _how_.
>
> **v3 (2026-07-06):** Content overhaul (v2, C1–C5) is complete — all writeups rewritten from
> audits, real visualizations committed, site copy refined, AI-native layer wired. This plan
> now focuses on **manual refinement with Nate**: working through each section with the appropriate
> skill (baseball-research-advisor for analytics projects, codebase-design + design-an-interface
> for engineering), using grilling to stress-test framing, and calibrating writing style to
> match examples of Nate's voice. Final polish before Human Hookup.

---

## Status

- **Built & audited:** Astro SSG + Tailwind + MDX + real ECharts visuals + AI-native layer
  (JSON-LD, llms.txt, projects.json). 10 pages, clean build, zero JS on non-chart pages,
  all content verified against repo outputs.
- **Next:** Manual refinement with Nate — grilling each section (baseball projects with
  baseball-research-advisor, Patio with codebase-design/design-an-interface), calibrating
  to Nate's writing voice.
- **Then:** Human Hookup (GitHub merge → Cloudflare Pages → `nateseluga.com`).
- **Startups & AI section:** Hidden until shipped work exists (2026-07-02, unchanged).

### The core problem this plan fixes

Every audited project writeup contains fabricated results the underlying repo cannot
produce (e.g. "78% AUC" vs real ~0.57–0.59; "2.1M shots" vs real 128K; "R² 0.52 predictive"
vs no forecasting model existing; a "sports betting platform with live odds" that is
actually a social drinking-games betting app with a Flask backend). Any technical
interviewer who opens the repos will catch this immediately — it converts strong real work
into a credibility liability. Meanwhile the writeups omit the genuinely impressive parts
(survival models, mixed-effects/CLR statistics, a scipy house-odds engine, SHAP suites,
Streamlit dashboards, honest negative results).

**New content rule (supersedes everything else): every number, method, and artifact named
on the site must be traceable to a repo output, file, or notebook cell.** Honest framing of
scope ("course project", "pre-launch MVP", "same-season skill isolation, not forecasting")
is a credibility asset, not a weakness.

---

## Finalized decisions (unchanged from v1)

| Area               | Decision                                                                                                         |
| ------------------ | ---------------------------------------------------------------------------------------------------------------- |
| **Framework**      | Astro, static output; interactivity via React islands only.                                                      |
| **Content model**  | MDX via Content Collections; `section` frontmatter enum; global data in `src/data/`.                             |
| **Styling**        | Tailwind, locked tokens, hand-built components, self-hosted fonts.                                               |
| **Visualizations** | ECharts in `client:visible` islands; data pre-computed offline → JSON committed to repo; browser never computes. |
| **Live apps**      | Outbound links only ("View live ↗").                                                                             |
| **Deployment**     | Cloudflare Pages on push to `main`; `nateseluga.com`.                                                            |

### Design guardrails (from the brief — enforce on every visual choice)

- Minimal, elegant, typography-led, high whitespace. Content _is_ the design.
- Muted-gray labels, near-black body, one accent used sparingly, near-white background.
- **Avoid:** hero splashes, gradients, decorative shapes, resume-card templates, skill bars, testimonial carousels, walls of text.
- Content rule: evidence over claims; show the artifact, don't describe it; depth over quantity — **and now: every claim traceable to the repo.**

### Project page structure (unchanged)

1. The Problem 2. Why It Matters 3. My Approach 4. Results (with visuals) 5. Key Takeaways

---

## Milestones & Tasks

### v2 (C0–C5) — Content overhaul ✅ done (2026-07-06)

All repos audited, writeups rewritten from real findings, visualizations replaced with
commits-pre-computed data, site copy refined by career-advisor, AI-native layer wired.
Details in `PROGRESS.md` log. Branch `overnight-content-overhaul` ready to merge.

---

### v3 — Manual refinement with Nate (in progress)

Now working through each section with you to polish framing, calibrate writing voice, and
stress-test key claims. Each project gets a grilling session with the appropriate skill
(baseball-research-advisor for analytics projects, codebase-design + design-an-interface
for engineering) — we'll use your writing samples to calibrate tone and specificity.

#### R1 — Pitcher Injury Risk+ (baseball-research-advisor + grilling)

- [ ] Read your writing samples (to calibrate voice).
- [ ] Open grilling session: depth of findings, confidence language, how to frame "discrimination is hard", value of the IR+ composite.
- [ ] Polish page copy: intro framing, results section wording, key-takeaways phrasing — make it sound like you.
- [ ] Verify: every number, every model choice, every metric is defensible to a baseball-ops reader.

#### R2 — NBA Shot-Value (baseball-research-advisor + grilling)

- [ ] Grilling: course-project framing, calibration results (what they mean), how to present
      the AUC ceiling honestly, Michael O'Brien co-authorship positioning.
- [ ] Polish copy: Results section clarity, the expected-points framing, takeaways.
- [ ] Verify: Brier score interpretation, SHAP feature naming, EV findings phrasing match your voice.

#### R3 — Batting Average Ability (baseball-research-advisor + grilling)

- [ ] Grilling: skill-isolation (not-a-forecast) framing, mixed-effects + ICC interpretation, why linear beat RF, luck component.
- [ ] Polish copy: Methods clarity, results scale and specificity, Arraez/Gallo examples.
- [ ] Verify: Statistical claims defensible; rejection reasoning clear; face validity arguments solid.

#### R4 — Patio (codebase-design + design-an-interface + grilling)

- [ ] Grilling: product positioning (pre-launch MVP, not "platform"), house-odds engine as the star feature, React/Flask architecture story.
- [ ] Polish copy: Problem/approach clarity, results section (what the engine does, why it matters), takeaways.
- [ ] Verify: Engineering decisions sound smart; honesty about mid-pivot reads as strength not weakness.

#### R5 — Site-wide voice pass (career-advisor + grilling)

- [ ] Home identity statement: does it read like you? Specific enough for a 10-second recruiter test?
- [ ] About page: concrete details, job targets clear, no generic adjectives.
- [ ] Section intros (`site.ts`): do they name real models without overclaiming?
- [ ] Tone check: evidence-led, no fluff, personality comes through the projects.

#### R6 — Final QA before Human Hookup

- [ ] Mobile + responsive check (layout unchanged, no content breaks).
- [ ] Build clean: `npm run build`.
- [ ] Lighthouse re-run (expect 100s locally).
- [ ] PROGRESS.md update.

---

⚠️ AUTONOMOUS RUN — STOP HERE

_Everything above is fully automatable except where marked (resume PDF, Patio screenshots
from a live instance, publishing the second-brain repo — those need Nate). Everything below
requires the user's accounts/money/auth and cannot be done unattended._

---

## Human Hookup (do together — ~15 min)

These are account/money/auth steps, not code. Order matters. (Unchanged from v1.)

- [ ] **GitHub:** repo exists (`nseluga/portfolio`) — merge working branch → `main`.
- [ ] **Cloudflare Pages:** connect repo, build `npm run build`, output `dist`, verify `*.pages.dev` deploy.
- [ ] **Domain:** register `nateseluga.com` (Cloudflare Registrar), attach, DNS + SSL, redirect.
- [ ] **Verify live:** Lighthouse against live URL; charts hydrate; zero JS on non-chart pages.
- [ ] Optional: Cloudflare Web Analytics.

### Needs-Nate follow-ups (surfaced by the audit)

- [ ] Patio: confirm whether `patio.nateseluga.com` is live (link or cut); capture real UI screenshots.
- [ ] LinkedIn URL — add to C3.3 contact block when available.
- [ ] Resume PDF — add to `public/resume.pdf` and uncomment link in C3.3 when updated.

---

## Open follow-ups / decisions deferred

- [ ] Which project gets a full **dashboard** island vs single chart (Injury Risk+ is the candidate — it has a real Streamlit app to link and real leaderboard data to embed).
- [ ] Contact method: mailto (current) vs form — unchanged, mailto is fine for now.
- [ ] OG images: default is clean; per-project OG images from real charts are a nice-to-have after C2.

---

## Conventions (for the agent)

- Reusable components in `src/components/`; layouts in `src/layouts/`; project MDX in `src/content/projects/`; chart JSON in `src/data/`; static visuals in `public/`.
- Never compute analytics in the browser — commit pre-aggregated JSON **exported from the actual project repos** (note the generating notebook/script in a JSON `_source` field or adjacent comment).
- Every new project addable via content only; component gaps get fixed, not hacked around.
- Keep zero-JS on any page without an intentional island.
- **Accuracy rule: no number, method, or artifact appears on the site unless it is traceable to a repo output. When content changes, update `llms.txt` and per-page meta in the same pass.**
