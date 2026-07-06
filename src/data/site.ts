/**
 * Global site configuration: nav, socials, section definitions/intros
 */

export const SITE = {
  title: 'Nate Seluga',
  description: 'CS junior at Harvey Mudd College. Building full-stack apps and sports analytics models.',
  url: 'https://nateseluga.com',
  author: 'Nate Seluga',
};

/**
 * Navigation links - appears in header
 */
export const NAV_LINKS = [
  { label: 'Engineering', href: '/engineering' },
  { label: 'Sports Analytics', href: '/sports-analytics' },
  // Hidden for now — restore when there's shipped work to show.
  // { label: 'Startups & AI', href: '/startups' },
  { label: 'About', href: '/about' },
];

/**
 * Social links - appears in footer
 */
export const SOCIAL_LINKS = [
  { label: 'GitHub', href: 'https://github.com/nseluga', icon: 'github' },
  { label: 'LinkedIn', href: 'https://linkedin.com/in/nseluga', icon: 'linkedin' },
  { label: 'Email', href: 'mailto:nseluga@g.hmc.edu', icon: 'email' },
];

/**
 * Section definitions: heading, intro text for each section landing page
 */
export const SECTIONS = {
  engineering: {
    title: 'Software Engineering',
    slug: 'engineering',
    intro:
      'Full-stack products built from the ground up. Patio is a social betting app for backyard games — React 19, Flask, Supabase, and a scipy house-odds engine at its core.',
  },
  'sports-analytics': {
    title: 'Sports Analytics',
    slug: 'sports-analytics',
    intro:
      'Statistical models and ML research in baseball and basketball. Projects: multi-model MLB pitcher injury prediction (Injury Risk+), batting average skill isolation (BAA), and NBA shot-value estimation with SHAP interpretability.',
  },
  startups: {
    title: 'Startups & AI',
    slug: 'startups',
    intro:
      'Early-stage ideas and AI-enabled tools. Concepts, POCs, and emerging directions in applied machine learning.',
  },
};
