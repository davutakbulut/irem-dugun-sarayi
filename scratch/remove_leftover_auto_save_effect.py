import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

start_marker = "      // 650ms DEBOUNCED LIVE AUTO-SAVE EFFECT"
end_marker = "      const selectedVenue = venues.find(v => v.id === venueId);"

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if start_marker in content and end_marker in content:
        s_pos = content.find(start_marker)
        e_pos = content.find(end_marker, s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            with open(h_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully removed leftover AUTO-SAVE effect from {h_file}!")
        else:
            print(f"Indices invalid in {h_file}")
    else:
        print(f"Markers not found in {h_file}")

print("Done removing leftover auto-save effect!")
