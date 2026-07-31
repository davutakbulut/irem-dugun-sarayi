import re

file_path = '/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Insert CSS Rule for nordic-light emoji hiding
css_target = 'html[data-ui-theme="nordic-light"] {'
css_replacement = '''html[data-ui-theme="nordic-light"] .emoji-text,
    html[data-ui-theme="nordic_light"] .emoji-text {
      display: none !important;
    }

    html[data-ui-theme="nordic-light"] {'''

if 'html[data-ui-theme="nordic-light"] .emoji-text' not in content:
    content = content.replace(css_target, css_replacement, 1)

# 2. Expand NordicSvgMap definition
old_map_start = 'const NordicSvgMap = {'
expanded_map = '''const NordicSvgMap = {
      crown: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M3 18h18L19 7l-5 4-2-6-2 6-5-4-2 11zM3 18v2h18v-2" /></svg>,
      user: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>,
      calendar: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="3" y="4" width="18" height="18" rx="2" ry="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" /></svg>,
      venue: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0v-5a2 2 0 012-2h2a2 2 0 012 2v5m-6 0h6" /></svg>,
      gift: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polyline points="20 12 20 22 4 22 4 12" /><rect x="2" y="7" width="20" height="5" /><line x1="12" y1="22" x2="12" y2="7" /><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z" /><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z" /></svg>,
      money: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="2" y="6" width="20" height="12" rx="2" /><circle cx="12" cy="12" r="3" /><path strokeLinecap="round" d="M6 12h.01M18 12h.01" /></svg>,
      edit: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>,
      preview: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>,
      delete: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polyline points="3 6 5 6 21 6" /><path strokeLinecap="round" strokeLinejoin="round" d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2" /></svg>,
      plus: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>,
      check: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><polyline points="20 6 9 17 4 12" /></svg>,
      close: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>,
      clock: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" /></svg>,
      document: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" /></svg>,
      email: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>,
      notes: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>,
      flow: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><line x1="10" y1="6" x2="21" y2="6" /><line x1="10" y1="12" x2="21" y2="12" /><line x1="10" y1="18" x2="21" y2="18" /><path strokeLinecap="round" strokeLinejoin="round" d="M4 6h1v4H4zM4 12h1v4H4z" /></svg>,
      warning: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>,
      campaign: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>,
      phone: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>,
      location: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" /><path strokeLinecap="round" strokeLinejoin="round" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" /></svg>,
      filter: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" /></svg>,
      list: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" /><line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" /></svg>,
      chart: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>,
      sparkles: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M5 3v4M3 5h4M6 17v4M4 19h4M13 3l2.5 6.5L22 12l-6.5 2.5L13 21l-2.5-6.5L4 12l6.5-2.5L13 3z" /></svg>,
      shield: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg>,
      settings: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="12" cy="12" r="3" /><path strokeLinecap="round" strokeLinejoin="round" d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" /></svg>,
      brain: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M9.5 2A2.5 2.5 0 007 4.5v.18A3.001 3.001 0 005 7.5a3 3 0 00.5 1.65A3.001 3.001 0 004 12a3 3 0 001.5 2.6A3.001 3.001 0 005 16.5a3 3 0 002 2.82V19.5A2.5 2.5 0 009.5 22h.5V2h-.5zM14.5 2A2.5 2.5 0 0117 4.5v.18A3.001 3.001 0 0119 7.5a3 3 0 01-.5 1.65A3.001 3.001 0 0120 12a3 3 0 01-1.5 2.6A3.001 3.001 0 0119 16.5a3 3 0 01-2 2.82V19.5A2.5 2.5 0 0114.5 22h-.5V2h.5z" /></svg>,
      target: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="12" cy="12" r="10" /><circle cx="12" cy="12" r="6" /><circle cx="12" cy="12" r="2" /></svg>,
      chat: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" /></svg>,
      leaf: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M11 20A9 9 0 012 11C2 6 6 2 11 2a9 9 0 019 9c0 5-4 9-9 9zM2 21l9-9" /></svg>,
      ruler: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M21 3L3 21M9 3l12 12M14 3l7 7M4 8l12 12M3 14l7 7" /></svg>,
      paint: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M12 21a9 9 0 100-18 9 9 0 000 18zm-4-9a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4-4a1.5 1.5 0 110-3 1.5 1.5 0 010 3zm4 4a1.5 1.5 0 110-3 1.5 1.5 0 010 3z" /></svg>,
      zap: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>,
      alert: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>,
      search: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2"><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></svg>,
      refresh: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2"><path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>,
      whatsapp: (props) => <svg className={props.className || "w-4 h-4 fill-white text-white inline-block"} fill="currentColor" viewBox="0 0 24 24"><path d="M12.012 2c-5.506 0-9.969 4.463-9.969 9.969 0 1.758.459 3.473 1.332 4.989l-1.416 5.176 5.297-1.389c1.464.798 3.119 1.218 4.756 1.218 5.506 0 9.969-4.463 9.969-9.969s-4.463-9.994-9.969-9.994zm5.829 14.157c-.247.695-1.436 1.341-1.968 1.386-.532.045-1.214.218-3.957-.919-3.308-1.365-5.422-4.733-5.586-4.952-.164-.218-1.341-1.782-1.341-3.401 0-1.619.845-2.415 1.146-2.742.301-.327.655-.409.873-.409.218 0 .436.009.627.018.2.009.473-.073.746.573.273.646.928 2.264 1.009 2.428.082.164.136.355.027.573-.109.218-.164.355-.327.546-.164.191-.345.427-.491.573-.164.164-.336.345-.145.673.191.327.855 1.401 1.837 2.274 1.264 1.128 2.328 1.482 2.655 1.646.327.164.518.136.709-.082.191-.218.818-.955 1.036-1.282.218-.327.436-.273.736-.164.3.109 1.909.901 2.236 1.064.327.164.545.245.627.382.082.137.082.846-.164 1.541z" /></svg>,
      camera: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><circle cx="12" cy="13" r="3" /></svg>,
      heart: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" /></svg>,
      card: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><rect x="1" y="4" width="22" height="16" rx="2" ry="2" /><line x1="1" y1="10" x2="23" y2="10" /></svg>,
      rocket: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M15.59 14.37a6 6 0 01-5.84 7.38v-4.8m5.84-2.58a14.98 14.98 0 006.16-12.12A14.98 14.98 0 009.63 8.41m5.96 5.96a14.926 14.926 0 01-5.841 2.58m-.119-8.54a6 6 0 00-7.381 5.84h4.8m2.581-5.84a14.927 14.927 0 00-2.58 5.84m2.58-5.84l4.14-4.14" /></svg>,
      bell: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>,
      print: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polyline points="6 9 6 2 18 2 18 9" /><path strokeLinecap="round" strokeLinejoin="round" d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2" /><rect x="6" y="14" width="12" height="8" /></svg>,
      key: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="7.5" cy="15.5" r="4.5" /><path d="M21 2l-9.6 9.6M15.5 7.5l3 3M18.5 4.5l3 3" /></svg>,
      celebrate: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M5 3l14 9-9 5L5 3zM12 17l-3 4M17 12l4 3M19 5l2-2M14 2l1 3" /></svg>,
      sun: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><circle cx="12" cy="12" r="5" /><line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" /><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" /><line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" /><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" /></svg>,
      moon: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>,
      diamond: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polygon points="6 3 18 3 22 9 12 22 2 9 6 3" /></svg>,
      idea: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3a7 7 0 00-7 7c0 2.38 1.157 4.49 2.92 5.8 1.07.8 1.08 1.2 1.08 2.2h6c0-1-.01-1.4 1.08-2.2C17.843 14.49 19 12.38 19 10a7 7 0 00-7-7z" /></svg>,
      door: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><path strokeLinecap="round" strokeLinejoin="round" d="M13 3h-6a2 2 0 00-2 2v14a2 2 0 002 2h6M13 3v18M13 3l6 2v14l-6 2M16 11h.01" /></svg>,
      map: (props) => <svg className={props.className || "w-4 h-4 inline-block"} fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="1.75"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6" /><line x1="8" y1="2" x2="8" y2="18" /><line x1="16" y1="6" x2="16" y2="22" /></svg>
    };'''

content = re.sub(r'const NordicSvgMap = \{.*?\};', expanded_map, content, flags=re.DOTALL)

# 3. Update ThemeIcon Component
old_theme_icon = re.search(r'function ThemeIcon\(\{.*?\}\) \{.*?\}', content, flags=re.DOTALL).group(0)

new_theme_icon = '''function ThemeIcon({ icon, fallbackEmoji, activeTheme, className = "w-4 h-4" }) {
      const domTheme = typeof document !== 'undefined' ? document.documentElement.getAttribute('data-ui-theme') : null;
      const rawTheme = activeTheme || domTheme || (typeof window !== 'undefined' ? (localStorage.getItem('selected_theme') || localStorage.getItem('irem_cache_theme_color')) : 'classic_gold') || 'classic_gold';

      const isNordic = rawTheme === 'nordic-light' || rawTheme === 'nordic_light';

      if (isNordic) {
        // NORDIC CLARITY LIGHT TEMASINDA HİÇBİR RENKLİ EMOJİ GÖRÜNMEYECEK
        const SvgComponent = NordicSvgMap[icon];
        if (SvgComponent) {
          return <SvgComponent className={className} />;
        }
        if (fallbackEmoji) {
          return <span className="emoji-text inline-block">{fallbackEmoji}</span>;
        }
        return null;
      }

      // DİĞER TEMALARDA (Elite Luxury, Sapphire Clean, Emerald Royal, Classic Gold, Obsidian Gold vb.)
      // Tema kimliğine uygun renkli/orijinal ikon ve emojiler görünür.
      if (ThemeConceptEmojis[icon] && ThemeConceptEmojis[icon][rawTheme]) {
        return <span className="emoji-text inline-block">{ThemeConceptEmojis[icon][rawTheme]}</span>;
      }
      if (fallbackEmoji) {
        return <span className="emoji-text inline-block">{fallbackEmoji}</span>;
      }
      if (NordicSvgMap[icon]) {
        const SvgComponent = NordicSvgMap[icon];
        return <SvgComponent className={className} />;
      }
      return null;
    }'''

content = content.replace(old_theme_icon, new_theme_icon)

# 4. Add renderFormattedMessage helper right after ThemeIcon
helper_code = '''
    function renderFormattedMessage(msg) {
      if (typeof msg !== 'string') return msg;

      const emojiMap = {
        '🏰': 'venue', '🏛️': 'venue', '🏛': 'venue', '🏢': 'venue', '🏡': 'venue', '🏬': 'venue',
        '🗑️': 'delete', '🗑': 'delete',
        '✨': 'sparkles',
        '🎁': 'gift',
        '🚀': 'rocket',
        '💰': 'money', '💸': 'money', '💳': 'card',
        '⚙️': 'settings', '⚙': 'settings',
        '📅': 'calendar',
        '✏️': 'edit', '✏': 'edit', '🖊️': 'edit', '✍️': 'edit',
        '🚪': 'door',
        '👤': 'user', '👥': 'user',
        '🎨': 'paint',
        '⚠️': 'alert', '⚠': 'alert', '🚨': 'alert', '⛔': 'warning',
        '🎉': 'celebrate',
        '✅': 'check', '✓': 'check',
        '📸': 'camera', '📷': 'camera',
        '🔔': 'bell',
        '🧠': 'brain',
        '🎯': 'target',
        '💬': 'chat',
        '🌿': 'leaf', '🌱': 'leaf', '🍂': 'leaf',
        '📐': 'ruler',
        '⚡': 'zap',
        '🔍': 'search',
        '🔄': 'refresh', '↺': 'refresh',
        '👑': 'crown', '🖤': 'crown', '💎': 'diamond', '🔷': 'diamond', '🌸': 'flower', '🍇': 'flower', '⬛': 'crown', '🪙': 'coin', '🌲': 'leaf'
      };

      const match = msg.match(/^([\\u{1F300}-\\u{1F9FF}\\u{2600}-\\u{26FF}\\u{2700}-\\u{27BF}\\u{2300}-\\u{23FF}\\u{2B00}-\\u{2BFF}\\u{1FA00}-\\u{1FAFF}\\ufe0f\\u200d]+)\\s*(.*)/u);
      if (match) {
        const rawEmoji = match[1].trim();
        const textPart = match[2];
        const iconKey = emojiMap[rawEmoji] || emojiMap[rawEmoji.replace(/\\ufe0f/g, '')] || 'sparkles';
        return (
          <span className="inline-flex items-center space-x-1.5">
            <ThemeIcon icon={iconKey} fallbackEmoji={rawEmoji} className="w-4 h-4 shrink-0" />
            <span>{textPart}</span>
          </span>
        );
      }
      return msg;
    }
'''

if 'function renderFormattedMessage' not in content:
    content = content.replace(new_theme_icon, new_theme_icon + '\n' + helper_code)

# Update Toast render line to use renderFormattedMessage
content = content.replace('<span>{toast.msg}</span>', '<span>{renderFormattedMessage(toast.msg)}</span>')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated ThemeIcon, NordicSvgMap, CSS, and toast formatting in index.html successfully.')
