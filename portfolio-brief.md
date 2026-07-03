# Portfolio Website — Brief

**Author:** Nate Seluga — Computer Science, Harvey Mudd College
**Document purpose:** A reference brief for building a personal portfolio site. This defines *why* the site exists, *who* it's for, *how* it should look and feel, and *what* projects it will showcase. Architecture and implementation decisions are intentionally left out — those are decided separately.

---

## 1. Purpose & Goals

### What this site is
A curated collection of work, ideas, and interests — not a resume in HTML. The site should read like a portfolio of someone who builds things and thinks carefully, closer to a baseball operations analytics portfolio or a working engineer's project log than a "hire me" landing page.

### Primary goal
Demonstrate technical ability, analytical thinking, and execution through evidence, so that a visitor leaves wanting to talk to me or work with me.

### Audiences (in rough priority order)
1. **Software engineering recruiters** — want to see real systems, clean execution, shipping ability.
2. **Sports analytics / baseball operations organizations** — want to see modeling rigor, data handling, and baseball-specific reasoning.
3. **Data science recruiters** — want to see methodology, evaluation, and clear results.
4. **Startup founders** — want to see initiative, range, and the ability to build end-to-end.
5. **Professors / researchers** — want to see depth and intellectual honesty.
6. **Potential collaborators** — want to understand how I think and what I care about.

### What every visitor should understand quickly
1. Who I am
2. What I care about
3. What I've built
4. How I think
5. Why they should work with me

### Decision rule
When any content or design choice is uncertain, choose the option that better showcases real accomplishments and makes the visitor want to keep exploring. Credibility first, then clarity, then visual impact, then recruiter experience, then storytelling.

---

## 2. Content Principles

These govern all writing on the site.

- **Evidence over claims.** No "passionate," "hard-working," "team player," "fast learner." Replace adjectives with artifacts.
  - Bad: "Experienced in machine learning."
  - Good: "Built an MLB pitcher injury-risk model using Statcast and injury-history data spanning 2015–2024."
- **Depth over quantity.** A few projects told well beats a long list.
- **Show the work, don't describe it.** Charts, dashboards, model outputs, screenshots, and diagrams carry more weight than prose.
- **Assume an intelligent reader unfamiliar with the project.** Writing is clear, technical, concise, and professional.
- **Organize around interests, not technologies.** Sections are framed by domain (engineering, sports analytics, startups), not by language or framework.

### Project page structure
Every project page should answer, in order:
1. **The Problem** — what challenge existed.
2. **Why It Matters** — why anyone should care.
3. **My Approach** — how it was solved (data, methodology, decisions).
4. **Results** — what happened, with visuals.
5. **Key Takeaways** — what I learned.

---

## 3. Visual Design Goals

### Target aesthetic
Minimal, elegant, typography-led, high whitespace. The reference north stars are **exampel_screenshots** — modern technical portfolios where the content is the design and restraint signals confidence.

### What to emulate (from the references)
- Clean single-column or generous two-column layouts with lots of breathing room.
- Quiet typographic hierarchy: dates/labels in muted gray, content in near-black, small section headers ("About," "Work," "Writing").
- Restrained palette — near-white background, one accent color used sparingly.
- Inline preview cards for writing/projects (thumbnail + title + one-line context) rather than walls of text.
- Subtle interaction cues (small arrows on links, gentle hover states) rather than loud animation.

### What to explicitly avoid (the other references show what *not* to do)
The bold-purple "Frontend Developer" hero, the gradient "Hello I'm…" splash, and the boxed-card resume templates (sidebar avatar, "Resume / Portfolio / Testimonials" accordions, "Download CV" buttons, colored skill icons) represent the **generic template look this site should not have.** Specifically avoid:
- Excessive colors and decorative shapes/dots/zigzags.
- Generic templates and resume-card layouts.
- Skill bars and progress meters.
- Large unbroken walls of text.
- Testimonial carousels and "What I'm Doing" service grids.

### Design characteristics checklist
- Minimal and elegant
- High whitespace
- Typography-focused
- Clean, restrained animation
- Fast loading
- Fully mobile responsive

### Visual content priority
Prioritize, wherever a project allows it: charts, dashboards, model outputs, screenshots, interactive demos, and project diagrams. The default move is to show an artifact, not describe one.

---

## 4. Information Architecture

Organized by interest. Four primary sections plus individual project pages.

### Software Engineering
Full-stack apps, backend systems, APIs, databases, automation, software architecture.

### Sports Analytics
A dedicated section for baseball and sports analytics modeling. This section should feel like a baseball-operations analytics portfolio: problem, data, methodology, results, visualizations, key findings for each project.

### Startups & AI
Startup concepts, AI systems, experiments, and entrepreneurial projects — demonstrating initiative and range.

### About
A compelling, specific story (not generic biography) connecting Harvey Mudd, software engineering, data science, sports analytics, startups, and a throughline of building useful things.

---

## 5. Projects to Include

Short descriptions and how each one ladders up to the larger goal. (Details, metrics, and visuals get filled in on the project pages themselves.)

### Software Engineering

**Patio — Sports Betting Platform**
A full-stack sports betting application. Demonstrates end-to-end engineering: frontend, backend, data, and the ability to ship a real product with real complexity. This is the flagship "I can build complete systems" proof point.

**Second Brain System**
A personal knowledge-management / note system. Demonstrates systems thinking, automation, and designing tools for my own workflow — and bridges into the Startups & AI section.

*(Placeholder slots for future startup projects and internship work where permissible — included so the architecture leaves room for them.)*

### Sports Analytics

**Pitcher Injury-Risk Model**
An MLB pitcher injury-risk model built on Statcast and injury-history data (2015–2024). The anchor project for the sports-analytics audience: shows real data work, modeling methodology, evaluation, and baseball-specific reasoning. This is the single most important credibility piece for baseball-operations readers.

**NBA Shot-Value Project**
A model evaluating shot value in the NBA. Demonstrates range across sports, spatial/contextual modeling, and the ability to turn tracking-style data into actionable insight.

**Batting Average Control Stat**
A hitter-evaluation model focused on separating batting-average skill from noise by using plate-discipline, power, and batted-ball indicators. Demonstrates baseball analytics judgment, metric design, and the ability to build interpretable player-evaluation tools from underlying performance drivers rather than relying only on traditional box-score outcomes.

*(Placeholder slots for future baseball analytics work and research investigations.)*

### Startups & AI

> **Status (2026-07-02): currently hidden.** This section is pulled from the nav and homepage until at least one project here is actually shipped. The vision below is retained; restore the section when there's real work to back it. See PROGRESS.md.

**Keep in mind none of these projects are complete yet**

**AI Construction Documentation Startup**
A startup concept applying AI to construction documentation. Demonstrates entrepreneurial thinking and the ability to identify a real-world problem and design a product around it. 

**AI Workflow Tools / Second-Brain Systems**
Experiments and tools built around AI-assisted workflows. Demonstrates that I use and build with AI deliberately, not just talk about it — initiative plus practical execution.

*(Placeholder slots for additional startup explorations and product concepts.)*

---

## 6. How the Pieces Fit the Larger Goal

- **Patio** proves I can ship complete software.
- **Pitcher Injury-Risk + NBA Shot Value** prove I can do rigorous, domain-specific data science — and target the sports-analytics audience directly.
- **AI / startup work** proves initiative and range.
- **About** ties it together into a coherent story rather than a pile of projects.

The combination is the point: an engineer who can also model, who also builds products, who also ships. The site's job is to make that combination obvious and credible without ever having to claim it in adjectives.
