/**
 * Global site configuration: nav, socials, section definitions/intros
 */

export const SITE = {
  title: 'Nate Seluga',
  description: 'Software engineer, data scientist, sports analytics enthusiast.',
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
      'Flagship projects in full-stack development, infrastructure, and systems design. From live apps to data pipelines.',
  },
  'sports-analytics': {
    title: 'Sports Analytics',
    slug: 'sports-analytics',
    intro:
      'Data-driven explorations in baseball and basketball. Statistical models, interactive visualizations, and deep dives into what the numbers reveal.',
  },
  startups: {
    title: 'Startups & AI',
    slug: 'startups',
    intro:
      'Early-stage ideas and AI-enabled tools. Concepts, POCs, and emerging directions in applied machine learning.',
  },
};
