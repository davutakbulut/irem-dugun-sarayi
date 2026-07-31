import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Nordic Light Theme Dark Overlay Contrast Protection CSS rules
nordic_contrast_css = """
    /* ------------------------------------------------------------------- */
    /* NORDIC LIGHT THEME: DARK OVERLAY & LIGHTBOX HIGH-CONTRAST PROTECTION */
    /* ------------------------------------------------------------------- */
    html[data-ui-theme="nordic-light"] [class*="z-[999"] .text-amber-400,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-900 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-slate-950 .text-amber-400,
    html[data-ui-theme="nordic-light"] .bg-black .text-amber-400 {
      color: #F59E0B !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .text-slate-300,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .text-slate-300,
    html[data-ui-theme="nordic-light"] .bg-slate-900 .text-slate-300,
    html[data-ui-theme="nordic-light"] .bg-slate-950 .text-slate-300 {
      color: #E2E8F0 !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .text-white,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .text-white,
    html[data-ui-theme="nordic-light"] .bg-slate-900 .text-white,
    html[data-ui-theme="nordic-light"] .bg-slate-950 .text-white {
      color: #FFFFFF !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .bg-gradient-to-r,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .bg-gradient-to-r {
      background: #0F172A !important;
      color: #FFFFFF !important;
      border: 2px solid #334155 !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .bg-gradient-to-r *,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .bg-gradient-to-r * {
      color: #FFFFFF !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .bg-amber-500,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .bg-amber-500 {
      background-color: #0F172A !important;
      color: #FFFFFF !important;
      border: 2px solid #334155 !important;
    }

    html[data-ui-theme="nordic-light"] [class*="z-[999"] .bg-amber-500 *,
    html[data-ui-theme="nordic-light"] [class*="z-[1000"] .bg-amber-500 * {
      color: #FFFFFF !important;
    }
"""

# Insert before focus-visible in CSS
target_css_anchor = "    :focus-visible {"
if target_css_anchor in html and "NORDIC LIGHT THEME: DARK OVERLAY" not in html:
    html = html.replace(target_css_anchor, nordic_contrast_css + "\n" + target_css_anchor)
    print("Inserted Nordic Light Theme Dark Overlay Contrast Protection CSS rules!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html nordic light theme harmonization successfully!")
