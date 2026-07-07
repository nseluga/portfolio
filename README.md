# Portfolio

A personal portfolio website showcasing projects across software engineering and sports analytics.

## Overview

A curated collection of work and technical accomplishments across two main domains: software engineering and sports analytics. Designed to demonstrate ability, analytical thinking, and execution.

## Tech Stack

- **Framework:** [Astro](https://astro.build) with static generation
- **Styling:** Tailwind CSS
- **Interactive components:** React islands (charts, visualizations)
- **Language:** TypeScript
- **Content:** MDX for project pages

## Project Structure

```
src/
├── pages/              # Route pages (index, about, section pages)
├── layouts/            # Page templates (BaseLayout, ProjectLayout)
├── components/         # Reusable Astro & React components
├── content/            # MDX project content & collection config
├── data/               # JSON data for charts and site metadata
└── styles/             # Global CSS

public/                 # Static assets (images, fonts)
```

## Key Directories

- **`src/pages/`** — Site routes: home, about, section landings, and 404
- **`src/content/projects/`** — Project pages written in MDX
- **`src/components/`** — Reusable UI building blocks (nav, footer, cards, chart wrappers)
- **`src/data/`** — JSON datasets and site configuration

## Getting Started

Install dependencies:
```bash
npm install
```

Run locally:
```bash
npm run dev
```

Build for production:
```bash
npm run build
```

## Publishing

The site deploys from the `main` branch. Built assets are output to `dist/`.
