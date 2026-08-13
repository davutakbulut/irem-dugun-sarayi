import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the right column start in CreateReservationPageComponent
    old_target = '{/* RIGHT COLUMN: LIVE INTERACTIVE PREVIEW & SUMMARY CARD (4 Cols - STICKY DESKTOP SIDEBAR) */}'
    
    # We want to replace the right column wrapper with a robust sticky implementation
    old_block_start = content.find(old_target)
    if old_block_start != -1:
        # Find closing of the div
        col_div_start = content.find('<div className="lg:col-span-4', old_block_start)
        col_div_end = content.find('>', col_div_start) + 1
        
        new_col_tag = '<div className="lg:col-span-4 lg:sticky lg:top-24 lg:self-start space-y-4 z-20 max-h-[calc(100vh-6.5rem)] overflow-y-auto no-scrollbar pb-6">'
        
        content = content[:col_div_start] + new_col_tag + content[col_div_end:]
        print(f"Updated right column sticky classes in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated for perfect sticky sidebar!")
