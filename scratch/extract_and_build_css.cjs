const fs = require('fs');

const backupLines = fs.readFileSync('index_monolithic_backup.html', 'utf8').split('\n');

// Extract ONLY CSS lines between 183 and 1122 (inside <style> tag)
const cssLines = backupLines.slice(183, 1122).filter(l => !l.includes('</style>') && !l.includes('<style>') && !l.includes('<script>'));
const extractedCss = cssLines.join('\n');

const newCss = `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Space+Grotesk:wght@600;700&display=swap');

@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --color-gold: #d97706;
  --color-gold-hover: #b45309;
  --color-gold-light: #fef3c7;
  --color-bg: #faf9f6;
  --color-card: #ffffff;
  --color-card-border: #e2e8f0;
  --color-text-main: #0f172a;
  --color-text-muted: #64748b;
  --glass-bg: rgba(255, 255, 255, 0.96);
  --glass-border: rgba(217, 119, 6, 0.25);
}

.dark {
  --color-bg: #0f172a;
  --color-card: #1e293b;
  --glass-bg: rgba(30, 41, 59, 0.96);
  --glass-border: rgba(217, 119, 6, 0.35);
}

/* ==========================================================================
   KURUMSAL TEMA PALETİ & GEOMETRİ/ÇEPER EFEKTİ SİSTEMİ (11 TEMA COMPLETE CSS)
   ========================================================================== */

${extractedCss}

/* REUSABLE BASE UTILITIES & ANIMATIONS */
body {
  background-color: var(--color-bg);
  color: var(--color-text-main);
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

.glass-panel {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  isolation: isolate;
  transform: translateZ(0);
  backface-visibility: hidden;
}

@supports (backdrop-filter: blur(12px)) or (-webkit-backdrop-filter: blur(12px)) {
  .glass-panel {
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
  }
}

.gold-gradient-text {
  color: var(--color-gold);
  background: linear-gradient(135deg, var(--color-gold) 0%, #d97706 50%, #92400e 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: inline-block;
}

.gold-button {
  background: linear-gradient(135deg, var(--color-gold) 0%, #b45309 100%);
  color: #ffffff;
  transition: all 0.2s ease-in-out;
}

.gold-button:hover {
  background: linear-gradient(135deg, #fbbf24 0%, var(--color-gold) 100%);
  box-shadow: 0 4px 20px rgba(217, 119, 6, 0.3);
}

:focus-visible {
  outline: 3px solid var(--color-gold, #d97706) !important;
  outline-offset: 2px !important;
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--color-bg); }
::-webkit-scrollbar-thumb { background: var(--color-card-border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--color-gold); }

main {
  -webkit-overflow-scrolling: touch;
  transform: translateZ(0);
}

@keyframes slideInLeft {
  0% { transform: translateX(-100%); opacity: 0.7; }
  100% { transform: translateX(0); opacity: 1; }
}
.animate-slide-in-left {
  animation: slideInLeft 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
  will-change: transform;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton-shimmer {
  background: linear-gradient(90deg, rgba(226, 232, 240, 0.5) 25%, rgba(203, 213, 225, 0.9) 50%, rgba(226, 232, 240, 0.5) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
}
.dark .skeleton-shimmer {
  background: linear-gradient(90deg, rgba(30, 41, 59, 0.5) 25%, rgba(51, 65, 85, 0.9) 50%, rgba(30, 41, 59, 0.5) 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite linear;
}
`;

fs.writeFileSync('src/index.css', newCss, 'utf8');
console.log(`🎉 EXTRACTED EXACT ${cssLines.length} CSS LINES INTO src/index.css SUCCESSFUL!`);
