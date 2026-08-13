import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update grid wrapper to add items-start for reliable sticky behavior
    old_grid = '<div className="grid grid-cols-1 lg:grid-cols-12 gap-6">'
    new_grid = '<div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">'
    if old_grid in content:
        content = content.replace(old_grid, new_grid)
        print(f"Updated grid wrapper in {h_file}")

    # 2. Update right column to be lg:sticky lg:top-6 lg:self-start
    old_right_col = """            {/* RIGHT COLUMN: LIVE INTERACTIVE PREVIEW & SUMMARY CARD (4 Cols - STICKY DESKTOP SIDEBAR) */}
            <div className="lg:col-span-4 space-y-6">
              
              {/* DESKTOP SIDEBAR CANLI FİNANSAL ÖZET & SÖZLEŞME ONAY KARTI (ALWAYS STICKY AT TOP RIGHT) */}
              <div className="hidden sm:block glass-panel p-6 rounded-3xl space-y-4 shadow-xl border-2 border-amber-500/40 dark:border-amber-500/30 lg:sticky lg:top-24 z-30">"""

    new_right_col = """            {/* RIGHT COLUMN: LIVE INTERACTIVE PREVIEW & SUMMARY CARD (4 Cols - STICKY DESKTOP SIDEBAR) */}
            <div className="lg:col-span-4 lg:sticky lg:top-6 lg:self-start space-y-5 z-20">
              
              {/* DESKTOP SIDEBAR CANLI FİNANSAL ÖZET & SÖZLEŞME ONAY KARTI (STICKY AT TOP RIGHT) */}
              <div className="glass-panel p-5 sm:p-6 rounded-3xl space-y-4 shadow-xl border-2 border-amber-500/40 dark:border-amber-500/30 bg-white/95 dark:bg-brand-card/95 backdrop-blur-md">"""

    if old_right_col in content:
        content = content.replace(old_right_col, new_right_col)
        print(f"Updated right column sticky in {h_file}")
    else:
        print(f"old_right_col not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("Sticky sidebar script completed!")
