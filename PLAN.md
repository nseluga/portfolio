# Portfolio Website — Manual Refinement Plan & Working TODO (v3)

> Working document for the agent building this site with Nate. Update it every pass: check off
> completed items, add follow-ups as they surface, keep it an accurate picture of remaining
> work. Source of truth for _what/why/feel_ is `portfolio-brief.md`; this file is _how_.

---

## Status

- **Built & content-complete:** Astro SSG + Tailwind + MDX + real ECharts visuals + AI-native layer
  (JSON-LD, llms.txt, projects.json). 12 pages, clean build. V0–V7 done: all project pages
  rewritten with real data, in-voice, rubric-passing.
- **Next (run 1):** V8 (strip AI patterns, voice pass) via `dev-team-auto`.
- **Then (run 2):** V9 visual polish via Fable + Claude Computer Use (launch from Claude app with Fable selected).
- **Then:** Human Hookup (GitHub → Cloudflare Pages → `nateseluga.com`).
- **Startups & AI section:** Hidden until shipped work exists (2026-07-02, unchanged).

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

### v4 — Unattended run 1: voice pass (`dev-team-auto`)

One item. Run `dev-team-auto` normally — it will stop at the marker below when done.

---

#### V8 — Site-wide voice pass: strip AI patterns, mirror Nate's voice · `status: done` · `track: full`

All project writeups and site copy were written by AI. The content and facts are solid — this pass strips the AI-generated phrasing and rewrites to match Nate's natural voice without changing any content, numbers, structure, or meaning.

- **files:** All non-draft project pages in `src/content/projects/` + homepage bio/section descriptions in `src/pages/index.astro` + `src/pages/about.astro` + `src/data/site.ts` section intros
- **voice reference:** Load everything in `~/os/knowledge/library/style_reference/`. Use each file for a distinct purpose:
  - **Essays and longer writing** (e.g. `Seluga Final Paper.pdf`) — reference for rhythm, word choices, sentence variety, and how ideas connect. These show the structural and stylistic patterns that carry across Nate's writing regardless of topic.
  - **Personal project explanations** (any files Nate has labeled as rough/personal examples) — reference specifically for voice calibration: the informal register, how he explains technical decisions in his own words, what he emphasizes and skips. These make it sound like *him*, not just well-written.
- **task:** Pass over every file listed above and eliminate AI writing patterns. Rewrite phrasing only. Content, facts, numbers, and structure stay identical.

  Patterns to eliminate:
  - Em dashes (—) — replace with a comma, period, or restructured sentence
  - Parenthetical asides that break reading flow — fold into the sentence or cut
  - Hedging openers: "Of course," "Certainly," "It's worth noting," "To be clear," "Generally speaking"
  - Filler transitions: "Moreover," "Furthermore," "Additionally," "Consequently," "That said"
  - Vocabulary tells: "delve," "underscore," "showcase," "leverage" (as verb), "paramount," "meticulous," "pivotal," "realm," "tapestry," "beacon," "multifaceted," "commence," "foster," "align with," "facilitate," "harness"
  - Conclusion signals used as openers: "In summary," "In conclusion," "To summarize," "Ultimately"
  - Over-structured scaffolding: "First... Moreover... In addition... Finally..."
  - Lists that always resolve to exactly three items for rhetorical balance
  - Uniform sentence length — vary the rhythm, use short sentences where they land harder
  - Missing contractions where a person would naturally use them ("it is" → "it's", "do not" → "don't", etc.)

  Voice to target: direct, specific, active. States what was built and why without framing language. No theatrical transitions. Honest about scope without qualifying every claim. Varies sentence length naturally.

- **done when:** Build clean. Every file above reviewed and rewritten. No em dashes remain. Parenthetical asides cut or folded in. None of the vocabulary tells remain. The pages read as written by a person. `career-advisor` confirms no marketing language crept in during the rewrite.

---

> **⚠️ AUTONOMOUS RUN — STOP HERE**

_V8 is for run 1 (`dev-team-auto`, standard models). V9 below is run 2 — it uses Fable as orchestrator + Claude Computer Use and must be launched separately from the Claude app with Fable selected. Everything after V9 requires user accounts and cannot run unattended._

---

### v5 — Unattended run 2: visual polish (Fable + Claude Computer Use)

> **How to run:** Open the Claude app, select Fable as the model, then run `/dev-team-auto`.
> Fable acts as the orchestrator and visual decision maker — it views the actual rendered site
> via Claude Computer Use and uses that visual judgment to direct fixes. Sub-agents
> (`dt-engineer`, `dt-qa`, `dt-fix`) use their standard models for implementation.

---

#### V9 — Visual polish pass · `status: not started` · `track: full`

The site is functionally clean but looks stock. This pass improves spacing, typography, color, and removes small visual bugs. No content changes.

- **task:** Open the local dev server (`npm run dev`) in a browser using Claude Computer Use. Do a visual audit of the homepage, engineering section, a sports-analytics project page, and the about page. Then fix in order:

  1. **Spacing** — Identify any sections where content feels vertically off (text floating too high or low relative to its container, uneven card padding, sections that don't breathe). Fix so spacing looks intentional throughout, not default.
  2. **Visual style** — Move away from the default Tailwind aesthetic. Consider a more characterful font for headings (geometric sans-serif, or a light-weight serif) while keeping body text clean and readable. Add small personality to hover states or the accent color. Stay within the design guardrails from `PLAN.md`: no gradients, no decorative shapes, muted-gray labels, near-black body, near-white background.
  3. **Visual bugs** — Fix overlapping text, clipped labels, misaligned elements, or layout breaks at 375px mobile and 1280px desktop.

  Use Fable's visual judgment throughout: view the actual rendered page, identify issues, direct `dt-engineer` to implement the fix, then verify visually in the browser before marking it resolved. Do not mark fixed without visual confirmation.

- **done when:** Build clean. No overlapping or clipped elements at 375px and 1280px. Spacing looks deliberate throughout. Typography has personality beyond the default Tailwind font stack. The visual bugs identified in the opening audit are resolved. Fable's visual review after fixes confirms the site looks polished, not generic.

---

> **⚠️ AUTONOMOUS RUN — STOP HERE**

_Everything below requires user accounts/money/auth and cannot run unattended._

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
