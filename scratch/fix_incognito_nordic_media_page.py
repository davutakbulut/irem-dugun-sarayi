import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add exhaustive CSS overrides for html[data-ui-theme="nordic-light"] to force ALL amber classes to Scandinavian Slate (#0F172A)
nordic_exhaustive_override = """
    /* =================================================================== */
    /* NORDIC LIGHT EXHAUSTIVE AMBER PURGE & SLATE NORMALIZATION            */
    /* =================================================================== */
    html[data-ui-theme="nordic-light"] .bg-amber-500,
    html[data-ui-theme="nordic-light"] .bg-amber-600,
    html[data-ui-theme="nordic-light"] .bg-amber-700,
    html[data-ui-theme="nordic-light"] .bg-amber-800,
    html[data-ui-theme="nordic-light"] .bg-gold-500,
    html[data-ui-theme="nordic-light"] .bg-gold-600 {
      background-color: #0F172A !important;
      color: #FFFFFF !important;
    }

    html[data-ui-theme="nordic-light"] .bg-amber-500\/10,
    html[data-ui-theme="nordic-light"] .bg-amber-500\/20,
    html[data-ui-theme="nordic-light"] .bg-amber-500\/30,
    html[data-ui-theme="nordic-light"] .bg-amber-500\/5 {
      background-color: #F1F5F9 !important;
      color: #0F172A !important;
    }

    html[data-ui-theme="nordic-light"] .text-amber-400,
    html[data-ui-theme="nordic-light"] .text-amber-500,
    html[data-ui-theme="nordic-light"] .text-amber-600,
    html[data-ui-theme="nordic-light"] .text-amber-700,
    html[data-ui-theme="nordic-light"] .text-amber-800,
    html[data-ui-theme="nordic-light"] .text-gold-400,
    html[data-ui-theme="nordic-light"] .text-gold-500 {
      color: #0F172A !important;
    }

    html[data-ui-theme="nordic-light"] .border-amber-500,
    html[data-ui-theme="nordic-light"] .border-amber-500\/10,
    html[data-ui-theme="nordic-light"] .border-amber-500\/20,
    html[data-ui-theme="nordic-light"] .border-amber-500\/30,
    html[data-ui-theme="nordic-light"] .border-amber-500\/40,
    html[data-ui-theme="nordic-light"] .border-amber-500\/50,
    html[data-ui-theme="nordic-light"] .border-amber-500\/60 {
      border-color: #CBD5E1 !important;
    }
"""

anchor = "    /* ------------------------------------------------------------------- */\n    /* NORDIC LIGHT SCANDINAVIAN MINIMALIST ARCHITECTURE DESIGN SYSTEM    */"
if anchor in html and "NORDIC LIGHT EXHAUSTIVE AMBER PURGE" not in html:
    html = html.replace(anchor, nordic_exhaustive_override + "\n" + anchor)
    print("Added Nordic Light Exhaustive Amber Purge CSS to index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html incognito nordic media page fix successfully!")
