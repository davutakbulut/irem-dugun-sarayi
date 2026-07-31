import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_nordic_overlay_css = """    /* ------------------------------------------------------------------- */
    /* NORDIC LIGHT THEME: DARK OVERLAY & LIGHTBOX HIGH-CONTRAST PROTECTION */
    /* ------------------------------------------------------------------- */
    html[data-ui-theme="nordic-light"] [class*="z-[999"] .text-amber-400,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-900 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-950 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-black .text-amber-400 {
      color: #F59E0B !important;
    }"""

new_nordic_overlay_css = """    /* ------------------------------------------------------------------- */
    /* NORDIC LIGHT THEME: PURE MONOCHROME SLATE & WHITE (NO ORANGE / AMBER) */
    /* ------------------------------------------------------------------- */
    html[data-ui-theme="nordic-light"] [class*="z-[999"] .text-amber-400,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-900 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-950 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-black .text-amber-400 {
      color: #FFFFFF !important;
    }

    html[data-ui-theme="nordic-light"] .gold-gradient-text {
      background: linear-gradient(135deg, #0F172A 0%, #334155 100%) !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .gold-gradient-text,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .gold-gradient-text {
      background: none !important;
      -webkit-text-fill-color: initial !important;
      color: #FFFFFF !important;
    }"""

if old_nordic_overlay_css in html:
    html = html.replace(old_nordic_overlay_css, new_nordic_overlay_css)
    print("Purged orange/amber from Nordic Light theme in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html Nordic Light color hierarchy successfully!")
