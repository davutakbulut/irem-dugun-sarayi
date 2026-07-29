import React from 'react';

// Unified SVG Icon Map for Nordic Clarity & Scandinavian Minimal (STRICT ZERO EMOJI)
const NordicSvgMap = {
  crown: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 18h18L19 7l-5 4-2-6-2 6-5-4-2 11zM3 18v2h18v-2" />
    </svg>
  ),
  user: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
    </svg>
  ),
  calendar: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  venue: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0h6" />
    </svg>
  ),
  gift: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <polyline points="20 12 20 22 4 22 4 12" />
      <rect x="2" y="7" width="20" height="5" />
      <line x1="12" y1="22" x2="12" y2="7" />
      <path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z" />
      <path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z" />
    </svg>
  ),
  money: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <rect x="2" y="6" width="20" height="12" rx="2" />
      <circle cx="12" cy="12" r="3" />
      <path strokeLinecap="round" d="M6 12h.01M18 12h.01" />
    </svg>
  ),
  edit: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
  ),
  preview: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
    </svg>
  ),
  delete: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <polyline points="3 6 5 6 21 6" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" />
    </svg>
  ),
  plus: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
      <line x1="12" y1="5" x2="12" y2="19" />
      <line x1="5" y1="12" x2="19" y2="12" />
    </svg>
  ),
  check: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  ),
  close: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  ),
  clock: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <circle cx="12" cy="12" r="10" />
      <polyline points="12 6 12 12 16 14" />
    </svg>
  ),
  document: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z" />
      <polyline points="14 2 14 8 20 8" />
      <line x1="16" y1="13" x2="8" y2="13" />
      <line x1="16" y1="17" x2="8" y2="17" />
      <line x1="10" y1="9" x2="8" y2="9" />
    </svg>
  ),
  email: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
    </svg>
  ),
  notes: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
    </svg>
  ),
  flow: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <line x1="10" y1="6" x2="21" y2="6" />
      <line x1="10" y1="12" x2="21" y2="12" />
      <line x1="10" y1="18" x2="21" y2="18" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M4 6h1v4H4zM4 12h1v4H4z" />
    </svg>
  ),
  warning: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
    </svg>
  ),
  campaign: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
    </svg>
  ),
  phone: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
    </svg>
  ),
  location: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
    </svg>
  ),
  sun: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  ),
  moon: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
    </svg>
  ),
  filter: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
    </svg>
  ),
  list: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" /><line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" />
    </svg>
  )
};

// CONCEPT-SPECIFIC EMOJI MAP FOR NON-NORDIC THEMES
const ThemeConceptEmojis = {
  crown: {
    'classic_gold': '👑',
    'obsidian_gold': '🖤',
    'sapphire_clean': '🔷',
    'platinum_silver': '🥈',
    'emerald_royal': '🌿',
    'titanium_tech': '⚡'
  },
  venue: {
    'classic_gold': '🏰',
    'obsidian_gold': '🏛️',
    'sapphire_clean': '🏢',
    'platinum_silver': '🏛️',
    'emerald_royal': '🏡',
    'titanium_tech': '🏬'
  },
  edit: {
    'classic_gold': '✏️',
    'obsidian_gold': '🖊️',
    'sapphire_clean': '📝',
    'platinum_silver': '⚙️',
    'emerald_royal': '✍️',
    'titanium_tech': '🛠️'
  },
  preview: {
    'classic_gold': '👁️',
    'obsidian_gold': '🌟',
    'sapphire_clean': '🔍',
    'platinum_silver': '🔍',
    'emerald_royal': '👁️',
    'titanium_tech': '📡'
  },
  delete: {
    'classic_gold': '🗑️',
    'obsidian_gold': '💣',
    'sapphire_clean': '❌',
    'platinum_silver': '🗑️',
    'emerald_royal': '🍂',
    'titanium_tech': '🚫'
  },
  plus: {
    'classic_gold': '➕',
    'obsidian_gold': '✨',
    'sapphire_clean': '🔹',
    'platinum_silver': '▫️',
    'emerald_royal': '🌱',
    'titanium_tech': '⚡'
  }
};

/**
 * Universal Theme-Aware Icon Component
 * - If theme is 'nordic' or 'nordic-light': renders clean Scandinavian SVG icons ONLY (Zero Emoji).
 * - For other themes: renders concept-specific emojis or fallback icons.
 */
export function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4 inline-block" }) {
  const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
  const rawTheme = activeTheme || domTheme || (typeof window !== 'undefined' ? (localStorage.getItem('selected_theme') || localStorage.getItem('irem_cache_theme_color')) : 'classic_gold') || 'classic_gold';
  
  // Normalize theme name
  const isNordic = rawTheme === 'nordic' || rawTheme === 'nordic-light' || rawTheme === 'nordic_light';

  if (isNordic) {
    const Component = NordicSvgMap[icon];
    if (Component) {
      return <Component className={className} />;
    }
  }

  // Concept-specific emojis for other themes
  if (ThemeConceptEmojis[icon] && ThemeConceptEmojis[icon][rawTheme]) {
    return <span className="inline-block">{ThemeConceptEmojis[icon][rawTheme]}</span>;
  }

  // Fallback to theme default emoji
  return <span className="inline-block">{fallbackEmoji}</span>;
}
