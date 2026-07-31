import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Find all function definitions in index.html
functions_in_index = re.findall(r'function ([A-Za-z0-9_]+)\s*\(', index_html)

print("=== ALL COMPONENT FUNCTIONS IN index.html ===")
page_comps_in_index = [fn for fn in functions_in_index if 'Component' in fn or 'Page' in fn]
for fn in sorted(set(page_comps_in_index)):
    print(f" - {fn}")

# Now let's compare every single page in src/pages with its counterpart in index.html
src_pages = sorted([f for f in os.listdir('src/pages') if f.endswith('.jsx')])

print("\n=== DETAILED COMPARISON PER PAGE ===")
for page in src_pages:
    src_path = os.path.join('src/pages', page)
    with open(src_path, 'r', encoding='utf-8') as f:
        src_code = f.read()

    # match function in index.html
    base_name = page.replace('.jsx', '')
    possible_names = [
        base_name,
        base_name + 'Component',
        base_name.replace('Page', '') + 'Component',
        base_name.replace('Page', '') + 'PageComponent',
        'CreateReservationPageComponent',
        'ReservationsListComponent',
        'MindMapPageComponent'
    ]

    found_name = None
    for name in possible_names:
        if f'function {name}' in index_html or f'const {name}' in index_html:
            found_name = name
            break

    src_len = len(src_code.split('\n'))
    
    index_len = 0
    if found_name:
        # extract function code from index.html
        pos = index_html.find(found_name)
        # rough extract
        sub = index_html[pos:pos+50000]
        # find end of function roughly
        index_len = len(sub.split('\n'))

    print(f"\n📄 {page}:")
    print(f"   Matches in index.html: {found_name}")
    print(f"   src/ lines: {src_len}")

