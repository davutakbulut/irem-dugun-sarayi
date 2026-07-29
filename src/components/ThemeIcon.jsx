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
  ),
  chart: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  ),
  sparkles: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l2.5 6.5L22 12l-6.5 2.5L13 21l-2.5-6.5L4 12l6.5-2.5L13 3z" />
    </svg>
  ),
  shield: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  ),
  settings: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <circle cx="12" cy="12" r="3" />
      <path strokeLinecap="round" strokeLinejoin="round" d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
    </svg>
  ),
  brain: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M9.5 2A2.5 2.5 0 007 4.5v.18A3.001 3.001 0 005 7.5a3 3 0 00.5 1.65A3.001 3.001 0 004 12a3 3 0 001.5 2.6A3.001 3.001 0 005 16.5a3 3 0 002 2.82V19.5A2.5 2.5 0 009.5 22h.5V2h-.5zM14.5 2A2.5 2.5 0 0117 4.5v.18A3.001 3.001 0 0119 7.5a3 3 0 01-.5 1.65A3.001 3.001 0 0120 12a3 3 0 01-1.5 2.6A3.001 3.001 0 0119 16.5a3 3 0 01-2 2.82V19.5A2.5 2.5 0 0114.5 22h-.5V2h.5z" />
    </svg>
  ),
  target: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <circle cx="12" cy="12" r="10" />
      <circle cx="12" cy="12" r="6" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  ),
  chat: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
    </svg>
  ),
  leaf: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M11 20A9 9 0 012 11C2 6 6 2 11 2a9 9 0 019 9c0 5-4 9-9 9zM2 21l9-9" />
    </svg>
  ),
  ruler: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M21 3L3 21M9 3l12 12M14 3l7 7M4 8l12 12M3 14l7 7" />
    </svg>
  ),
  paint: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9 9 0 100-18 9 9 0 000 18zm-4-9a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4-4a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4 4a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" />
    </svg>
  ),
  zap: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
  ),
  whatsapp: (props) => (
    <svg className={props.className || "w-4 h-4 fill-white text-white inline-block"} fill="currentColor" viewBox="0 0 24 24">
      <path d="M12.012 2c-5.506 0-9.969 4.463-9.969 9.969 0 1.758.459 3.473 1.332 4.989l-1.416 5.176 5.297-1.389c1.464.798 3.119 1.218 4.756 1.218 5.506 0 9.969-4.463 9.969-9.969s-4.463-9.994-9.969-9.994zm5.829 14.157c-.247.695-1.436 1.341-1.968 1.386-.532.045-1.214.218-3.957-.919-3.308-1.365-5.422-4.733-5.586-4.952-.164-.218-1.341-1.782-1.341-3.401 0-1.619.845-2.415 1.146-2.742.301-.327.655-.409.873-.409.218 0 .436.009.627.018.2.009.473-.073.746.573.273.646.928 2.264 1.009 2.428.082.164.136.355.027.573-.109.218-.164.355-.327.546-.164.191-.345.427-.491.573-.164.164-.336.345-.145.673.191.327.855 1.401 1.837 2.274 1.264 1.128 2.328 1.482 2.655 1.646.327.164.518.136.709-.082.191-.218.818-.955 1.036-1.282.218-.327.436-.273.736-.164.3.109 1.909.901 2.236 1.064.327.164.545.245.627.382.082.137.082.846-.164 1.541z" />
    </svg>
  ),
  alert: (props) => (
    <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75">
      <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
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
  },
  campaign: {
    'classic_gold': '🎁',
    'obsidian_gold': '🏷️',
    'sapphire_clean': '🔷',
    'platinum_silver': '💎',
    'emerald_royal': '🌿',
    'titanium_tech': '⚡'
  },
  gift: {
    'classic_gold': '🎁',
    'obsidian_gold': '💎',
    'sapphire_clean': '🔹',
    'platinum_silver': '▫️',
    'emerald_royal': '🍃',
    'titanium_tech': '⚡'
  },
  chart: {
    'classic_gold': '📈',
    'obsidian_gold': '📊',
    'sapphire_clean': '📊',
    'platinum_silver': '📈',
    'emerald_royal': '📊',
    'titanium_tech': '💻'
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

/**
 * Official WhatsApp Icon SVG Component
 * - variant="white": Pure White (#FFFFFF) fill for Green Backgrounds (e.g. Buttons).
 * - variant="green": Official Brand Green (#25D366) fill for Light Backgrounds.
 */
export function WhatsAppIcon({ className = "w-4 h-4 shrink-0" }) {
  return (
    <svg className={`fill-white text-white ${className}`} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12.012 2c-5.506 0-9.969 4.463-9.969 9.969 0 1.758.459 3.473 1.332 4.989l-1.416 5.176 5.297-1.389c1.464.798 3.119 1.218 4.756 1.218 5.506 0 9.969-4.463 9.969-9.969s-4.463-9.994-9.969-9.994zm5.829 14.157c-.247.695-1.436 1.341-1.968 1.386-.532.045-1.214.218-3.957-.919-3.308-1.365-5.422-4.733-5.586-4.952-.164-.218-1.341-1.782-1.341-3.401 0-1.619.845-2.415 1.146-2.742.301-.327.655-.409.873-.409.218 0 .436.009.627.018.2.009.473-.073.746.573.273.646.928 2.264 1.009 2.428.082.164.136.355.027.573-.109.218-.164.355-.327.546-.164.191-.345.427-.491.573-.164.164-.336.345-.145.673.191.327.855 1.401 1.837 2.274 1.264 1.128 2.328 1.482 2.655 1.646.327.164.518.136.709-.082.191-.218.818-.955 1.036-1.282.218-.327.436-.273.736-.164.3.109 1.909.901 2.236 1.064.327.164.545.245.627.382.082.137.082.846-.164 1.541z" />
    </svg>
  );
}

/**
 * Official Brand Styled WhatsApp Action Button Component
 */
export function WhatsAppButton({ phone, customerName = '', text = 'WhatsApp İle Mesaj At', className = '' }) {
  const cleanPhone = (phone || '').replace(/[^0-9]/g, '');
  const encodedText = encodeURIComponent(`Merhabalar ${customerName ? customerName + ' ' : ''}İrem Düğün Sarayı'ndan sizlere ulaşıyorum.`);
  const href = `https://wa.me/${cleanPhone}?text=${encodedText}`;

  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`bg-[#25D366] hover:bg-[#20BA5A] text-white font-extrabold px-3.5 py-2 rounded-xl text-xs inline-flex items-center space-x-2 shadow-md shadow-emerald-500/20 hover:shadow-lg hover:shadow-emerald-500/30 transition-all duration-200 transform hover:-translate-y-0.5 border border-emerald-400/30 active:scale-95 ${className}`}
    >
      <WhatsAppIcon variant="white" className="w-4 h-4 shrink-0" />
      <span>{text}</span>
    </a>
  );
}
