import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Replace overflow-x: hidden !important on html, body with overflow-x: clip
    old_html_body_css = """    html, body {
      background-color: var(--color-bg);
      color: var(--color-text-main);
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      overflow-x: hidden !important;
      max-width: 100vw;
      width: 100%;
    }"""

    new_html_body_css = """    html, body {
      background-color: var(--color-bg);
      color: var(--color-text-main);
      font-family: 'Inter', sans-serif;
      margin: 0;
      padding: 0;
      overflow-x: clip;
      max-width: 100vw;
      width: 100%;
    }"""

    if old_html_body_css in content:
        content = content.replace(old_html_body_css, new_html_body_css)
        print(f"Fixed html/body overflow-x in {h_file}")

    # 2. Clean .glass-panel transform
    old_glass_css = """    /* FIX FOR BLANK WHITE BOXES & SCROLL REPAINT GLITCHES */
    .glass-panel {
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
      isolation: isolate;
      transform: translateZ(0);
      backface-visibility: hidden;
    }"""

    new_glass_css = """    /* FIX FOR BLANK WHITE BOXES & SCROLL REPAINT GLITCHES */
    .glass-panel {
      background: var(--glass-bg);
      border: 1px solid var(--glass-border);
    }"""

    if old_glass_css in content:
        content = content.replace(old_glass_css, new_glass_css)
        print(f"Cleaned .glass-panel transform in {h_file}")

    # 3. Add explicit sticky styling and classes to the right column in CreateReservationPageComponent
    old_right_col = '<div className="lg:col-span-4 lg:sticky lg:top-24 lg:self-start space-y-4 z-20 max-h-[calc(100vh-6.5rem)] overflow-y-auto no-scrollbar pb-6">'
    new_right_col = '<div className="lg:col-span-4 lg:sticky lg:top-24 lg:self-start space-y-4 z-20" style={{ position: "sticky", top: "96px", alignSelf: "flex-start" }}>'

    if old_right_col in content:
        content = content.replace(old_right_col, new_right_col)
        print(f"Applied guaranteed sticky right column in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated with guaranteed sticky sidebar!")
