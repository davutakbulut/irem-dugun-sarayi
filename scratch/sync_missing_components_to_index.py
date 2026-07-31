import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def prepare_component(file_path, comp_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    lines = code.split('\n')
    clean = []
    for line in lines:
        if line.strip().startswith('import '):
            continue
        clean.append(line)
    
    res = '\n'.join(clean)
    res = res.replace('export function ', 'function ')
    res = res.replace('export const ', 'const ')
    res = res.replace('export default ', '// export default ')
    
    if 'function ReservationsPage' in res:
        res = res.replace('function ReservationsPage', f'function {comp_name}')
    elif 'function UsersPage' in res:
        res = res.replace('function UsersPage', f'function {comp_name}')
    elif 'function MediaPage' in res:
        res = res.replace('function MediaPage', f'function {comp_name}')
        
    return res

reservations_code = prepare_component('src/pages/ReservationsListPage.jsx', 'ReservationsListComponent')
users_code = prepare_component('src/pages/UsersPage.jsx', 'UsersComponent')
media_code = prepare_component('src/pages/MediaPage.jsx', 'MediaComponent')

target_marker = '// --- MAIN APP COMPONENT ---'
if target_marker in html:
    insert_block = f"""
// --- RESERVATIONS LIST COMPONENT ---
{reservations_code}

// --- USERS COMPONENT ---
{users_code}

// --- MEDIA COMPONENT ---
{media_code}

"""
    html = html.replace(target_marker, insert_block + target_marker)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully added ReservationsListComponent, UsersComponent, MediaComponent to index.html!")
else:
    print("Error: target marker not found!")

