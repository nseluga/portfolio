# Portfolio Website — Manual Refinement Plan & Working TODO (v3)

> Working document for the agent building this site with Nate. Update it every pass: check off
> completed items, add follow-ups as they surface, keep it an accurate picture of remaining
> work. Source of truth for _what/why/feel_ is `portfolio-brief.md`; this file is _how_.
>
> **v3 (2026-07-08):** Content overhaul (v2, C1–C5) is complete — all writeups rewritten from
> audits, real visualizations committed, site copy refined, AI-native layer wired. This plan
> now runs an **autonomous content-voice loop** (`dev-team-auto`, overnight): instead of manually
> grilling each section, every project page is driven to completion by the convergence loop
> against a skill-based rubric — the Engineer rewrites the page in Nate's voice using the style
> reference, and the loop only marks it DONE once QA confirms it is professionally written,
> fully accurate (every number traceable to the repo), and complete (what he did, why, what he
> learned, and the systems he used). Rubric per item: **baseball-research-advisor + career-advisor**
> for analytics pages, **career-advisor + dt-engineer** for software, **career-advisor +
> ai-usage-optimizer** for the AI-tooling pages. Final polish before Human Hookup.

---

## Status

- **Built & audited:** Astro SSG + Tailwind + MDX + real ECharts visuals + AI-native layer
  (JSON-LD, llms.txt, projects.json). 10 pages, clean build, zero JS on non-chart pages,
  all content verified against repo outputs.
- **Next:** Autonomous content-voice loop (`dev-team-auto`, V0–V7 below) — each project page
  rewritten in Nate's voice and driven to a passing skill-based rubric (accuracy, voice,
  process legibility) without manual intervention.
- **Then:** Human Hookup (GitHub merge → Cloudflare Pages → `nateseluga.com`).
- **Startups & AI section:** Hidden until shipped work exists (2026-07-02, unchanged).

### The core problem this plan fixes

v2 fixed the fabrication problem: the audited writeups once claimed results the repos could
not produce (e.g. "78% AUC" vs real ~0.57–0.59; "2.1M shots" vs real 128K; "R² 0.52
predictive" vs no forecasting model; a "sports betting platform" that is a Flask
social-betting MVP). C1–C5 killed those and rebuilt every page from real repo data, so the
site is now **accurate** — but accurate is not the same as **hireable**.

The problem v3 fixes is the next layer: the pages read like a corrected audit, not like Nate.
They are dry and generic where they should be in his voice, and — more costly — they under-sell
the genuinely impressive work by stating *what* was built without the reasoning a hirer reads
for: *why* each modeling/engineering decision was made, what alternatives were ruled out, what
he learned, and which systems he now knows. A SWE, ML, or baseball-ops interviewer skims for
exactly that judgment; its absence makes strong real work (survival models,
mixed-effects/ICC statistics, a scipy house-odds engine, SHAP suites, an honest predictability
ceiling) look like a class-assignment checklist. v3 rewrites each page in Nate's voice and
drives it — via the autonomous loop below — to the bar where a hirer can see the thinking, not
just the artifact, while holding the v2 accuracy rule as a hard gate.

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

### v3 — Autonomous content-voice loop (`dev-team-auto`)

Runs unattended overnight. Each item below is a `dev-team-auto` convergence-loop item
(`~/.claude/skills/dev-team-auto/skill.md` → `dev-team/convergence-loop.md`): the Engineer
(`dt-engineer`) rewrites the page, QA (`dt-qa`, gate mode `tests+behavioral`) gates it, the
Optimization Reviewer reviews, the Bug Fixer applies findings, repeating until the item passes
or hits the 5-attempt cap. What makes this a *content* loop rather than a code loop: the
acceptance rubric is a set of **skills**, and the loop only converges when the page satisfies
them.

**How the skills wire into the loop.** The named skills are the rubric, not extra agents. Each
item's `task:` instructs the Engineer to load and apply them while writing; each item's
`done when:` encodes their checks as concrete acceptance criteria; QA's behavioral gate re-runs
those same skill checklists against the rendered page before emitting PASS. An item is DONE only
when QA is PASS (page accurate + complete + in-voice) **and** the review pass is clean.

**Rubric by page type:**

| Page type | Review skills (the rubric) | Builder |
| --------- | -------------------------- | ------- |
| Sports analytics | `baseball-research-advisor` (research substance) + `career-advisor` (recruiter impact) | `dt-engineer` (Opus, `flag:`) |
| Software | `career-advisor` + `dt-engineer` (engineering substance) | `dt-engineer` |
| AI tooling | `career-advisor` + `ai-usage-optimizer` (AI-leverage substance) | `dt-engineer` |

**Voice reference (every item).** Rewrite in Nate's voice per
`~/os/knowledge/library/style_reference/Project_Writeup.pdf` — specific, evidence-driven,
honest about scope and uncertainty, zero marketing language. This is the target tone for all
copy below, and one of the acceptance criteria.

#### Content acceptance gate — applies to every V-item's `done when:`

An item passes only when **all** of these hold (QA verifies against the source repo and
`audits/` notes on the behavioral gate; the review skills confirm the qualitative ones):

1. **Builds clean** — `npm run build` succeeds; the page compiles with no MDX errors.
2. **Accurate / traceable** — every number, metric, method, and named artifact on the page
   traces to a repo output, file, or notebook cell. No fabricated or rounded-up figures.
   (This is the standing accuracy rule; it is the fastest way a technical interviewer fails a
   candidate — see "The core problem this plan fixes".)
3. **Structured** — the five-part page structure is present: Problem · Why It Matters ·
   My Approach · Results · Key Takeaways.
4. **Process-legible** — a hirer can see, without guessing: **what** Nate built, **why** he made
   each key decision, **what he learned**, and **which systems/tools/methods** he used and now
   knows. This is the bar the target audience (SWE / ML / analytics hirers) actually reads for.
5. **In Nate's voice** — matches the style reference (specific, evidence-driven, honest about
   scope, no marketing language).
6. **Skill review clean** — the item's review skills raise no unresolved Critical/Important
   issue. `career-advisor`'s four axes (accuracy, clarity, credibility, recruiter impact) pass
   on every page; the domain skill's substantive checks pass per item below.
7. **Meta synced** — `public/llms.txt` and the page's meta description are updated in the same
   pass to match the rewritten copy.

---

#### V0 — OS repo project page (AI tooling) · `status: done` · `track: full`

- **skills (rubric):** `career-advisor` + `ai-usage-optimizer`
- **file:** create `src/content/projects/os-workflow.mdx` (`section: engineering`, `draft: false`)
- **task:** Write the page for Nate's personal OS repo (`~/os`) — his strongest AI work because
  the repo is real and openable. Load `career-advisor` and `ai-usage-optimizer` and the style
  reference; audit `~/os` for real counts before writing. Lead with what exists (custom Claude
  Code skills, persistent memory system, `os/projects` structure, hooks). Pick 2–3 skills as
  concrete worked examples (e.g. `career-advisor`, `dev-team`, `baseball-research-advisor`) and
  say what each *enables* and why it is leverage — not a feature list. Then update the homepage
  bio in `src/pages/index.astro` to name AI tooling alongside full-stack and statistical
  modeling (covers all three target roles).
- **done when:** Content acceptance gate + (a) every count/skill named is verified against the
  live `~/os` repo — no invented metrics; (b) `ai-usage-optimizer` confirms the page reads as
  real, compounding AI leverage (systems that get used), not a shelf of unused tooling; (c) the
  homepage bio names all three role tracks; (d) links to the GitHub repo resolve.

#### V1 — Project Dashboard mini project (AI tooling) · `status: done` · `track: light`

Keep this one **brief** — it is a personal tool, included to show AI-usage optimization and
staying organized, not a flagship. One tight card/short page, not a full case study.

- **skills (rubric):** `career-advisor` + `ai-usage-optimizer`
- **file:** create `src/content/projects/project-dashboard.mdx` (`section: engineering`,
  `draft: false`) — short-form.
- **task:** Write a short writeup for the Project Dashboard (`~/project-dashboard`,
  `github.com/nseluga/project-dashboard`): a local Astro + Tailwind + TS (SSR via
  `@astrojs/node`) dashboard that reads project status from every `~/os/projects/*/README.md`,
  plus a weekly digest and quick-capture inbox — built for himself to keep his own AI-assisted
  work organized. Load `career-advisor` + `ai-usage-optimizer` + the style reference. Frame it
  as a personal-productivity tool that demonstrates he optimizes his own AI usage and stays
  organized; do **not** oversell it or pad it into a case study. A few sentences on what it is,
  why he built it, and what it shows about how he works.
- **done when:** Content acceptance gate (structure may be a short-form subset — at minimum what
  it is, why, and what it demonstrates) + (a) stays brief — no inflation, honest "personal tool"
  framing; (b) stack and data source (reads `os/projects` READMEs) are stated accurately and
  trace to the repo; (c) `career-advisor` confirms it reads as a credibility asset (organized,
  self-directed) rather than filler.

#### V2 — Pitcher Injury-Risk Model (sports analytics) · `status: done` · `track: full` · `flag: baseball research writing — Opus + framing exploration`

- **skills (rubric):** `baseball-research-advisor` + `career-advisor`
- **file:** `src/content/projects/pitcher-injury-risk.mdx`
- **task:** Rewrite the page in Nate's voice. Load `baseball-research-advisor`,
  `career-advisor`, the style reference, and the research references in
  `~/os/knowledge/library/baseball-research/`; verify all numbers against the repo /
  `audits/audit-pitcher-injury-risk.md`. Use `baseball-research-advisor` to write the
  **research-specific** content the way the reference papers do: the hypothesis / research
  question, modeling choices (baseline classifiers → survival analysis → the ERA+-style Injury
  Risk+ composite) with alternatives ruled out and why, stated assumptions (independence,
  leakage, sample), sports intuition (a mechanism a front-office analyst would accept), and
  honest accuracy/precision metrics (report the real ~0.57–0.59 discrimination and frame "risk
  discrimination is genuinely hard" as a finding, not a failure). `flag:` framing-exploration:
  the design pass explores 2–3 page framings and picks the most defensible.
- **done when:** Content acceptance gate + baseball-substance checks: (a) every model choice,
  assumption, and metric is defensible to a baseball-ops reader per `baseball-research-advisor`
  with no unresolved challenge; (b) accuracy/precision metrics are reported honestly with
  correct interpretation and the ceiling is framed as a result; (c) the IR+ composite's value
  and the survival-analysis work are legible; (d) methodological writing matches the
  `baseball-research/` reference standard.

#### V3 — NBA Shot-Value Model (sports analytics) · `status: done` · `track: full` · `flag: baseball research writing — Opus + framing exploration`

- **skills (rubric):** `baseball-research-advisor` + `career-advisor`
- **file:** `src/content/projects/nba-shot-value.mdx`
- **task:** Rewrite in Nate's voice. Same skill + reference loadout as V2; verify against the
  repo / `audits/audit-nba-shot-value.md`. Write the research content with
  `baseball-research-advisor`: the expected-value question and hypothesis, the 4-model pipeline
  (logistic regression, decision tree, random forest, XGBoost on raw vs. engineered features)
  with why each was compared, the honest predictability **ceiling** and what it implies
  (shooter skill as the key missing variable), correct interpretation of the classification AUC
  and Brier calibration, and SHAP feature naming. Frame it honestly as a course project and
  position Michael O'Brien's co-authorship cleanly.
- **done when:** Content acceptance gate + baseball-substance checks: (a) the AUC ceiling and
  Brier/calibration results are presented honestly with correct interpretation; (b) the
  4-model comparison, feature engineering, and the "missing variable = shooter skill"
  conclusion are defensible per `baseball-research-advisor`; (c) course-project scope and
  co-authorship are stated plainly; (d) EV framing and SHAP naming match the source repo.

#### V4 — Batting Average Ability (sports analytics) · `status: done` · `track: full` · `flag: baseball research writing — Opus + framing exploration`

- **skills (rubric):** `baseball-research-advisor` + `career-advisor`
- **file:** `src/content/projects/batting-average-control.mdx`
- **task:** Rewrite in Nate's voice. Same skill + reference loadout as V2; verify against the
  repo / `audits/audit-batting-average.md`. Use `baseball-research-advisor` for the research
  substance: frame it precisely as **same-season skill isolation, not a forecast**; the
  mixed-effects model over 4,374 player-seasons and the ICC / repeatability interpretation
  (ability vs. luck decomposition); why the linear model beat random forest and why that is the
  right conclusion; face-validity checks (Arraez / Gallo as endpoints of the ability–luck
  spectrum). Keep the "this is not prediction" boundary explicit — it is a credibility asset.
- **done when:** Content acceptance gate + baseball-substance checks: (a) the skill-isolation
  (not-forecast) framing is explicit and correct; (b) mixed-effects + ICC interpretation, the
  luck component, and the linear-beats-RF reasoning are defensible per
  `baseball-research-advisor`; (c) face-validity examples land; (d) statistical assumptions are
  stated and hold.

#### V5 — Patio (software) · `status: done` · `track: full`

- **skills (rubric):** `career-advisor` + `dt-engineer` (engineering substance)
- **file:** `src/content/projects/patio.mdx`
- **task:** Rewrite in Nate's voice. Load `career-advisor` + the style reference; verify against
  the repo / `audits/audit-patio.md`. Make the **engineering decisions** legible and sound
  (this is the `dt-engineer`-substance rubric): the scipy house-odds engine (~760 LOC,
  recency-weighted player means, ~4% house edge) as the centerpiece; the dual-confirmation
  settlement state machine; the React 19 + Flask + Supabase architecture and why; the real
  scale (~6,150 LOC, 20 API routes). Frame scope honestly as a solo-built **pre-launch MVP**,
  not a "platform"; present the mid-project pivot as an engineering-judgment strength.
- **done when:** Content acceptance gate + engineering-substance checks: (a) the house-odds
  engine and settlement state machine read as genuinely smart decisions with the reasoning
  visible; (b) architecture choices (React/Flask/Supabase) are justified, not just named;
  (c) LOC/route counts and the ~4% edge trace to the repo; (d) "pre-launch MVP" scope and the
  pivot read as strengths, not apologies.

#### V6 — Site-wide voice pass (software / all) · `status: done` · `track: light`

- **skills (rubric):** `career-advisor`
- **files:** `src/pages/index.astro`, `src/pages/about.astro` (About), `src/data/site.ts`
  (section intros)
- **task:** Load `career-advisor` + the style reference and pass over the connective site copy
  the project pages don't cover: the home identity statement (does it survive a 10-second
  recruiter test and name what he builds?), the About page (concrete story + clear job targets,
  no generic adjectives), and the section intros in `site.ts` (name real models without
  overclaiming). Enforce one consistent voice against the style reference across all of it.
- **done when:** Content acceptance gate (items 1, 2, 5, 6 — build, accuracy, voice, review)
  applied to site copy + (a) the home identity statement passes the 10-second recruiter test
  per `career-advisor`; (b) About reads as a specific story with the three role targets clear;
  (c) section intros name real models without overclaiming; (d) tone is consistent and
  evidence-led site-wide.

#### V7 — Final QA before Human Hookup · `status: done` · `track: light`

- **task:** After V0–V6 converge, run the whole-site pass: mobile + responsive check (layout
  unchanged, no content breaks); `npm run build` clean; Lighthouse re-run (expect 100s
  locally); confirm `llms.txt` and per-page meta reflect all rewritten copy; final PROGRESS.md
  update.
- **done when:** Build clean; responsive check passes; Lighthouse 100s locally; `llms.txt` +
  meta synced with the new copy; PROGRESS.md updated.

---

> **⚠️ AUTONOMOUS RUN — STOP HERE**

_Everything above (V0–V7) is fully automatable by `dev-team-auto`. The one caveat is Patio's
UI screenshots, which need a live instance (Nate) — the V5 copy rewrite does not depend on
them. Everything below requires the user's accounts/money/auth and cannot be done unattended._

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
- **Style rule: all explanations and project writeups follow Nate's voice as demonstrated in `~/os/knowledge/library/style_reference/Project_Writeup.pdf` — specific, evidence-driven, honest about scope/uncertainty, no marketing language. When polishing copy, compare against this reference.**
- **Accuracy rule: no number, method, or artifact appears on the site unless it is traceable to a repo output. When content changes, update `llms.txt` and per-page meta in the same pass.**
