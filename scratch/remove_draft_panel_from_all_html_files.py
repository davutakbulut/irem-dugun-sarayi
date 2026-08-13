import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

start_marker = '{/* DRAFT / UNCOMPLETED RESERVATIONS DEDICATED PANEL (TOP OF PAGE) */}'
end_marker = '{/* COLLAPSIBLE FILTER PANEL */}'

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if start_marker in content:
        s_idx = content.find(start_marker)
        e_idx = content.find(end_marker, s_idx)
        if s_idx != -1 and e_idx != -1:
            content = content[:s_idx] + content[e_idx:]
            with open(h_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully removed Draft Panel from {h_file}!")
        else:
            print(f"Markers found but indices invalid in {h_file}")
    else:
        print(f"start_marker not found in {h_file}")

print("Draft Panel removal completed!")
