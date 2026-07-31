import os
import re

index_file = 'index.html'
src_dir = 'src/pages'

with open(index_file, 'r', encoding='utf-8') as f:
    index_content = f.read()

pages_in_src = [f for f in os.listdir(src_dir) if f.endswith('.jsx')]

print("=== PAGE COMPONENT AUDIT: index.html vs src/pages/ ===")

report = []

for page_file in sorted(pages_in_src):
    comp_name = page_file.replace('Page.jsx', 'Component').replace('.jsx', '')
    if comp_name == 'Dashboard': comp_name = 'DashboardComponent'
    elif comp_name == 'CreateReservation': comp_name = 'CreateReservationPageComponent'
    elif comp_name == 'ReservationsList': comp_name = 'ReservationsListComponent'
    elif comp_name == 'Calendar': comp_name = 'CalendarComponent'
    elif comp_name == 'Campaigns': comp_name = 'CampaignsComponent'
    elif comp_name == 'Reports': comp_name = 'ReportsComponent'
    elif comp_name == 'Finance': comp_name = 'FinanceComponent'
    elif comp_name == 'Venues': comp_name = 'VenuesComponent'
    elif comp_name == 'Services': comp_name = 'ServicesComponent'
    elif comp_name == 'Customers': comp_name = 'CustomersComponent'
    elif comp_name == 'Users': comp_name = 'UsersComponent'
    elif comp_name == 'Settings': comp_name = 'SettingsComponent'
    elif comp_name == 'MindMap': comp_name = 'MindMapPageComponent'

    src_path = os.path.join(src_dir, page_file)
    with open(src_path, 'r', encoding='utf-8') as f:
        src_code = f.read()

    # Search in index.html for component definition
    pattern = rf'function {comp_name}\s*\(.*?\)'
    match = re.search(pattern, index_content)
    
    index_len = 0
    if match:
        start_pos = match.start()
        # Find rough length
        sub = index_content[start_pos:start_pos+30000]
        index_len = len(sub.split('\n'))

    src_lines = len(src_code.split('\n'))

    # Check specific features
    src_features = {
        'buttons': len(re.findall(r'<button', src_code)),
        'inputs': len(re.findall(r'<input', src_code)),
        'modals': len(re.findall(r'Modal', src_code)),
        'state_uses': len(re.findall(r'useState', src_code)),
    }
    
    index_sub = index_content[start_pos:start_pos+40000] if match else ""
    index_features = {
        'buttons': len(re.findall(r'<button', index_sub[:15000])),
        'inputs': len(re.findall(r'<input', index_sub[:15000])),
        'modals': len(re.findall(r'Modal', index_sub[:15000])),
        'state_uses': len(re.findall(r'useState', index_sub[:15000])),
    }

    report.append({
        'page': page_file,
        'comp': comp_name,
        'in_index': bool(match),
        'src_lines': src_lines,
        'src_features': src_features,
        'index_features': index_features
    })

for item in report:
    print(f"📄 {item['page']} ({item['comp']}):")
    print(f"   Src Lines: {item['src_lines']} | Index Found: {item['in_index']}")
    print(f"   Src Buttons: {item['src_features']['buttons']} | Index Buttons: {item['index_features']['buttons']}")
    print(f"   Src Inputs:  {item['src_features']['inputs']} | Index Inputs:  {item['index_features']['inputs']}")

