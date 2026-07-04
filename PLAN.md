# Portfolio Website — Content Overhaul Plan & Working TODO (v2)

> Working document for the agent building this site. Update it every pass: check off
> completed items, add follow-ups as they surface, keep it an accurate picture of remaining
> work. Source of truth for *what/why/feel* is `portfolio-brief.md`; this file is *how*.
>
> **v2 (2026-07-03):** The build phase (v1, M0–M4) is complete — the site's engineering is
> done and verified. This plan now focuses on **content**: a 2026-07-03 audit of every
> project repo (`audits/`) found that the current writeups are largely **fabricated** —
> invented metrics, wrong methodologies, wrong tech stacks — while the real projects are
> stronger and more interesting than the fiction. The work below replaces fiction with
> evidence and raises the site's recruiter impact.

---

## Where things stand

- **Built & verified (v1, M0–M4):** Astro SSG + Tailwind + MDX content collections + ECharts
  React islands. 11 pages build cleanly, perfect local Lighthouse scores, zero JS on
  non-chart pages. See PROGRESS.md log for details.
- **Not yet deployed:** Human Hookup (GitHub → Cloudflare Pages → `nateseluga.com`) still
  pending — see the block at the bottom.
- **Startups & AI section hidden** (2026-07-02) until there's shipped work. Unchanged.
- **New (2026-07-03):** Per-project content audits completed and committed in `audits/`.
  A `career-advisor` skill (senior tech-career advisor persona, benchmark:
  https://www.helenbentley.com/) was created at `~/.claude/skills/career-advisor.md` and
  informs milestone C3.

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

| Area | Decision |
|------|----------|
| **Framework** | Astro, static output; interactivity via React islands only. |
| **Content model** | MDX via Content Collections; `section` frontmatter enum; global data in `src/data/`. |
| **Styling** | Tailwind, locked tokens, hand-built components, self-hosted fonts. |
| **Visualizations** | ECharts in `client:visible` islands; data pre-computed offline → JSON committed to repo; browser never computes. |
| **Live apps** | Outbound links only ("View live ↗"). |
| **Deployment** | Cloudflare Pages on push to `main`; `nateseluga.com`. |

### Design guardrails (from the brief — enforce on every visual choice)
- Minimal, elegant, typography-led, high whitespace. Content *is* the design.
- Muted-gray labels, near-black body, one accent used sparingly, near-white background.
- **Avoid:** hero splashes, gradients, decorative shapes, resume-card templates, skill bars, testimonial carousels, walls of text.
- Content rule: evidence over claims; show the artifact, don't describe it; depth over quantity — **and now: every claim traceable to the repo.**

### Project page structure (unchanged)
1. The Problem  2. Why It Matters  3. My Approach  4. Results (with visuals)  5. Key Takeaways

---

## Milestones & Tasks

### C0 — Audit groundwork ✅ done (2026-07-03)
- [x] Create `career-advisor` skill (`~/.claude/skills/career-advisor.md`): senior tech-career
      advisor persona; axes = accuracy, clarity, credibility, recruiter impact; benchmark
      helenbentley.com.
- [x] Locate and clone all project repos: `nseluga/patio`, `nseluga/Pitcher-Injury-Risk`,
      `nseluga/Shot-Value-Machine-Learning`, `nseluga/Batting-Average-Ability`.
- [x] Audit each repo vs. its writeup (high-reasoning pass, baseball-research-advisor
      framing) → per-project notes committed in `audits/audit-*.md`.
- [x] Finding: **Second Brain System has no public repo**, despite the writeup claiming its
      infrastructure is "open-source in my GitHub" (tracked in C1.5).

### C1 — Rewrite project writeups (accuracy first) ⬜
Each rewrite works from its audit file — the audit's "Real findings", "Strongest
visualizations", and "Recommended framing" sections are the spec. Keep the 5-part page
structure. Add `repoUrl` to the frontmatter schema and link the repo prominently on every
project page ("View code ↗").

- [ ] **C1.1 Pitcher Injury-Risk → reframe as "Pitcher Injury Risk+"** (`audits/audit-pitcher-injury-risk.md`)
  - Kill: "78% AUC-ROC" (real: tuned RF test AUC 0.579, walk-forward CV mean 0.571), "top-10% precision 64%", "2,847 pitchers / 12 variables", Retrosheet sourcing, the invented age/usage chart (3.2%→13.1%), "+35%/+70% risk" bullets.
  - Tell the real (better) story: multi-model research platform over Statcast 2015–2024 — 3,249 pitchers, 205,911 pitcher-game rows, 76 features; baseline classifiers + survival models (ensemble C-index 0.566) + multi-task severity + the **Injury Risk+** composite (ERA+-style, mean 100 by season × archetype, 9,752 pitcher-seasons, YoY r = 0.583); isotonic calibration (ECE 0.059 → 0.029); temporal/walk-forward validation.
  - Lead findings: injury history + 90-day cumulative workload dominate (interventional SHAP shows `pitches_90d` beats ACWR); >2 mph chronic velocity decline ≈ doubles observed 30-day injury rate (6% → 12%, Risk+ 96.9 → 119.5); honest "discrimination is genuinely hard" framing — that candor *is* the credibility play for baseball-ops readers.
  - Frontmatter metrics → real ones (pitcher-game rows, features, CV AUC, IR+ YoY stability).
- [ ] **C1.2 NBA Shot-Value → reframe as calibration-first EV study** (`audits/audit-nba-shot-value.md`)
  - Kill: "2.1M shots (2019–2024)" (real: 128,069 shots, 2014–15 Kaggle shot logs, 122,203 cleaned), "R² = 0.68" (it's classification — tuned XGBoost AUC 0.6365), "500-cell hexagonal grid" and all x/y-coordinate features (dataset has none), per-zone precision numbers, star-vs-role-player EV claims (model is deliberately player-agnostic), "holdout 2024 season" (real: random 80/20).
  - Tell the real story: Harvey Mudd CS158 course project (with Michael O'Brien); 4-model comparison (LR/DT/RF/XGB, raw vs engineered); hard predictability ceiling at AUC ~0.63–0.64 with shooter skill as the named missing variable; well-calibrated probabilities (Brier 0.2296) → trustworthy expected points = p(make) × shot value; EV findings: open 0–4 ft ≈ 1.85 EV, mid-range trough, corner-3 (22–24 ft) bump; `defender_distance_ratio` is the top SHAP feature.
  - Credit **Michael O'Brien** as co-author (confirmed by Nate) and name the course (CS158 ML). Link the formal PDF writeup in the repo. Add `collaborators: ["Michael O'Brien"]` to frontmatter.
- [ ] **C1.3 Batting Average Control Stat → rename to the real metric, "BAA (Batting Average Ability)"** (`audits/audit-batting-average.md`)
  - Kill: "predictive R² 0.52" and "correlation with future BA 0.58" (no forecasting model exists — all modeling is same-season), elastic net (real: OLS/RF/statsmodels MixedLM), "5-fold CV by season" (real: random 80/20), shrinkage step, Statcast feature list (real: FanGraphs rates + sprint speed), the RMSE bar chart, the archetype table, Betts/Judge examples, "wider rookie intervals" (real PI coverage is 54.5% — poorly calibrated).
  - Tell the real story: skill-isolation metric, not a forecast — mixed-effects model with player random intercepts (ICC: 24.7% of AVG variance is between-player), CLR transform for batted-ball composition, PA-weighted fitting; Test R² 0.4570 / MAE 0.0215 for AVG from peripherals; RF and ensembles tried and **rejected on evidence** (BABIP Test R² 0.293 vs linear 0.372); BAA indexed 100 ± 10 per season with a per-season `luck_component`; face validity: Arraez 2023 = 133.2 vs Gallo 2023 = 61.2; sprint speed as the #2 BABIP driver.
  - Fix scale claims: 4,374 player-seasons / 1,173 players (not "1,200+ hitters").
  - Future-work section may honestly propose the next-season stability test as the natural extension.
- [ ] **C1.4 Patio → describe the actual product** (`audits/audit-patio.md`)
  - Kill: "sports betting platform", "Node.js backend" (real: React 19 + Python Flask + psycopg2 + Supabase Postgres), live odds feeds, WebSockets, "100+ beta testers", all latency/Lighthouse/conversion numbers, "zero balance discrepancies" (contradicted by the repo's own bug list), invented components (BetSlip, OddsBoard).
  - Tell the real story: solo-built social betting app where friends wager virtual "caps" on backyard games (Caps, Pong, Beerball); centerpiece is a **scipy-powered house-odds engine** (~760 LOC): recency-weighted player means, harmonic-mean team strength, normal-percentile line biasing for a ~4% house edge, push-proof x.5 lines — fed by a self-improving stats pipeline as bets settle; honor-system dual-confirmation settlement state machine; JWT auth; ~6,150 LOC, 20 routes, 6 pages.
  - Frame honestly as a **pre-launch MVP mid-pivot to React Native/iOS**, backed by a rigorous self-audit (the repo's own PLAN.md) — sell the applied statistics and engineering judgment.
  - Verify or remove the `patio.nateseluga.com` live link (unverifiable during audit).
- [ ] **C1.5 Second Brain System — remove project page from site**
  - This project is no longer being developed. Remove it entirely: set `draft: true` in the MDX frontmatter (do not delete the file) and remove it from any curated lists in `site.ts`. No rewrite needed.
- [ ] **C1.6 Cross-cutting fixes (all projects)**
  - Add `repoUrl` (and optional `collaborators`) to the Zod schema + ProjectLayout header link.
  - Fix frontmatter dates to match reality (current dates like 2024-03-15 predate the repos).
  - Update every project `summary` (card one-liner) and `metrics[]` to audited-real values — these surface on the home page and section cards, so they must match the rewritten pages.
  - Proofread rule for the pass: any number that can't be pointed to in the repo gets cut.

### C2 — Real visualizations & assets ⬜
The single-JSON status quo (`src/data/pitcher-injury-risk.json`, itself fabricated) gets
replaced by data exported from the actual repos. Never compute in the browser; commit
pre-computed JSON (or static images where interactivity adds nothing).

- [ ] **C2.1 Pitcher Injury Risk+:** replace the invented age/usage ECharts data with real
      exports — velocity-decline dose-response (Risk+ 96.9→119.5, injury rate 6%→12%) as the
      inline interactive chart; age × workload danger-zone heatmap as the second visual;
      link out to the Streamlit dashboard / Plotly HTML exports ("View live ↗" pattern).
      Consider embedding 1–2 danger-zone heatmap PNGs via `<Figure>`.
- [ ] **C2.2 NBA Shot-Value:** replace the fabricated court heatmap with the real
      pressure-stratified EV-by-distance curves (from `value_defender.png` data) as ECharts
      JSON; add the shot-uncertainty/calibration figure and SHAP beeswarm as static
      `<Figure>` images pulled from the repo's `models/` PNGs.
- [ ] **C2.3 BAA:** export the flagship BAA-vs-BA scatter (2019–2024, per-season trendlines)
      to JSON for an ECharts island; optional second visual: RF feature-importance bars or
      the Arraez/Gallo leaderboard as a small table.
- [ ] **C2.4 Patio:** real screenshots of the live UI (none exist in the repo — capture from
      a running instance) and/or a short muted screen-recording per the v1 decision; a
      simple diagram of the odds-engine feedback loop (stats → aggregates → lines → bets →
      stats) would show the best subsystem.
- [ ] **C2.5 Thumbnails:** replace the eight generic placeholder SVGs in `public/images/`
      with real-artifact-derived thumbnails (chart crops, UI screenshots) so cards preview
      actual work.

### C3 — Site-wide copy, hierarchy & recruiter impact ⬜
Career-advisor pass (see `~/.claude/skills/career-advisor.md`; benchmark helenbentley.com:
immediate identity statement, ruthless curation, role/impact framing, personality through
content, effortless nav).

- [ ] **C3.1 Home identity statement:** replace "Software engineer, data scientist, and
      sports analytics enthusiast… I build systems that work" (adjective-speak) with a
      specific, evidence-led line: who (CS @ Harvey Mudd, class year), what he builds
      (full-stack products + baseball/basketball analytics models), and one concrete hook —
      the 10-second recruiter test. No "enthusiast", no "passionate".
- [ ] **C3.2 Selected Work curation:** hand-curate order (currently an arbitrary `order`
      sort): lead with the strongest post-rewrite piece (likely Injury Risk+), then Patio,
      then BAA/Shot-Value. Add one real metric per card. Cards must read correctly to a
      non-technical recruiter.
- [ ] **C3.3 Contact & next-action:** put email + GitHub visibly on the home page (not just
      footer). Known facts: email = nseluga@g.hmc.edu, GitHub = github.com/nseluga. Omit
      resume PDF link (not current) and LinkedIn (unknown) — leave placeholders in HTML
      comments so they can be added later. Every page should have an obvious next action.
- [ ] **C3.4 About page rewrite:** the current version is generic narrative ("I care about
      evidence over claims") with zero verifiable specifics. Rewrite with concrete facts:
      class year, relevant coursework (e.g. CS158 ML), the real projects by name, what he's
      currently looking for (role type + timing). Cut the "What Drives Me" adjectives;
      let the projects carry that. Keep it typography-led.
- [ ] **C3.5 Section intros:** tighten `site.ts` intros to match audited reality (e.g.
      sports-analytics intro should name the real models; engineering intro shouldn't
      promise "flagship live apps" plural while only Patio exists).
- [ ] **C3.6 Layout flow check:** home → section → project journey QA after rewrites;
      confirm visual hierarchy still holds with new content lengths; mobile pass.

### C4 — AI-native layer ⬜
Recruiters increasingly ask AI assistants about candidates; make the site machine-legible
so those summaries are accurate.

- [ ] **C4.1 JSON-LD structured data:** `Person` schema on home/about (name, alumniOf Harvey
      Mudd, knowsAbout, sameAs → GitHub/LinkedIn, email); per-project
      `SoftwareSourceCode`/`CreativeWork` schema with `codeRepository` → the real repo URLs.
      Emit from `BaseLayout`/`ProjectLayout` off existing frontmatter — no per-page hand-authoring.
- [ ] **C4.2 `llms.txt`:** add `public/llms.txt` — a natural-language summary of Nate
      (background, skills, each project in 2–3 accurate sentences with repo + page links),
      built from the same audited facts as the writeups. Keep it in lockstep with content
      (add a "regenerate llms.txt" step to the content-change convention below).
- [ ] **C4.3 Machine-readable project index:** optional `public/projects.json` (title, slug,
      one-liner, real metrics, repo URL) generated at build time from the content collection.
- [ ] **C4.4 Crawler posture:** keep `robots.txt` permissive (incl. AI crawlers); verify
      sitemap URL correctness; per-page meta descriptions updated to the accurate one-liners
      from C1.6.

### C5 — Verification & wrap-up ⬜
- [ ] **C5.1 Accuracy re-audit:** re-run a career-advisor + per-repo spot-check pass over the
      rewritten pages: every number on the site must be findable in a repo output. This is
      the gate for calling C1 done.
- [ ] **C5.2 Build & QA:** `npm run build` clean; zero-JS check on non-chart pages; chart
      hydration check; Lighthouse re-run; mobile QA.
- [ ] **C5.3 Update PROGRESS.md** and check off this plan as milestones complete.

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
