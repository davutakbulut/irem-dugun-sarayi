import re

with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Strip imports
lines = code.split('\n')
clean_lines = [l for l in lines if not l.strip().startswith('import ')]
clean_code = '\n'.join(clean_lines)

clean_code = clean_code.replace('export function ReservationsListPage(', 'function ReservationsListComponent(')
clean_code = clean_code.replace('export function ReservationsListPage', 'function ReservationsListComponent')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

p_start = html.find('// --- RESERVATIONS LIST COMPONENT ---')
p_end = html.find('// --- USERS COMPONENT ---')

if p_start != -1 and p_end != -1:
    new_html = html[:p_start] + '// --- RESERVATIONS LIST COMPONENT ---\n' + clean_code + '\n\n' + html[p_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Cleanly re-synced ReservationsListComponent into index.html!")
else:
    print("Error finding markers!", p_start, p_end)

