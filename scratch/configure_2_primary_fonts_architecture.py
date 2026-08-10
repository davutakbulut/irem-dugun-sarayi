import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Google Fonts link to import Great Vibes, Cormorant Garamond, Playfair Display & Plus Jakarta Sans
old_google_fonts = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">'

new_google_fonts = '<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,600&family=Great+Vibes&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'

if old_google_fonts in content:
    content = content.replace(old_google_fonts, new_google_fonts)
    print("Updated Google Fonts import to 2 primary font families + hand-script accent!")

# 2. Add Typography CSS Rules inside style tag
font_rules_css = """
    /* ---------------------------------------------------------------------- */
    /* 2 PRIMARY FONTS SYSTEM + 1 UNIVERSAL CROSS-PLATFORM SYSTEM FALLBACK    */
    /* 1. Heading Font: 'Cormorant Garamond' / 'Great Vibes' (Şık, Zarif, Güven)*/
    /* 2. Body Font: 'Plus Jakarta Sans' (Sade, Net ve Okunabilir)           */
    /* 3. System Fallback: Georgia / system-ui, -apple-system, sans-serif    */
    /* ---------------------------------------------------------------------- */
    :root {
      --font-heading: 'Cormorant Garamond', 'Playfair Display', Georgia, 'Times New Roman', serif;
      --font-script: 'Great Vibes', 'Cormorant Garamond', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Headings & Luxury Titles */
    h1, h2, h3, h4, .font-serif, .font-heading {
      font-family: var(--font-heading) !important;
    }

    /* Elegant Hand-script Accents */
    .font-script, .script-accent {
      font-family: var(--font-script) !important;
    }

    /* Body, UI Elements, Buttons & Paragraphs */
    body, p, span, div, button, input, select, textarea, a, td, th, label, .font-sans {
      font-family: var(--font-body) !important;
    }
"""

style_end_idx = content.find('</style>')
if style_end_idx != -1:
    content = content[:style_end_idx] + font_rules_css + content[style_end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
