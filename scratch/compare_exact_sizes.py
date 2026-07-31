import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Map of component names in index.html and their src files
mapping = {
    'DashboardComponent': 'src/pages/DashboardPage.jsx',
    'CreateReservationPageComponent': 'src/pages/CreateReservationPage.jsx',
    'ReservationsListComponent': 'src/pages/ReservationsListPage.jsx',
    'CalendarComponent': 'src/pages/CalendarPage.jsx',
    'CampaignsComponent': 'src/pages/CampaignsPage.jsx',
    'ReportsComponent': 'src/pages/ReportsPage.jsx',
    'FinanceComponent': 'src/pages/FinancePage.jsx',
    'VenuesComponent': 'src/pages/VenuesPage.jsx',
    'ServicesComponent': 'src/pages/ServicesPage.jsx',
    'CustomersComponent': 'src/pages/CustomersPage.jsx',
    'UsersComponent': 'src/pages/UsersPage.jsx',
    'SettingsComponent': 'src/pages/SettingsPage.jsx',
    'MindMapPageComponent': 'src/pages/MindMapPage.jsx',
    'ProfileComponent': 'src/pages/ProfilePage.jsx',
    'MediaComponent': 'src/pages/MediaPage.jsx',
}

print("=== EXACT COMPONENT SIZE COMPARISON: index.html vs src/pages/ ===")

for comp_name, src_file in mapping.items():
    # Find start position in index.html
    pos_start = html.find(f'function {comp_name}')
    if pos_start == -1:
        pos_start = html.find(f'const {comp_name}')
    
    index_lines = 0
    if pos_start != -1:
        # Find next function or component
        next_pos = len(html)
        for other_comp in mapping.keys():
            if other_comp != comp_name:
                p = html.find(f'function {other_comp}', pos_start + 20)
                if p != -1 and p < next_pos:
                    next_pos = p
                p2 = html.find(f'// --- ', pos_start + 20)
                if p2 != -1 and p2 < next_pos:
                    next_pos = p2
        
        comp_code_index = html[pos_start:next_pos]
        index_lines = len(comp_code_index.split('\n'))

    src_lines = 0
    try:
        with open(src_file, 'r', encoding='utf-8') as sf:
            src_lines = len(sf.read().split('\n'))
    except Exception:
        pass

    diff = index_lines - src_lines
    status = "OK" if abs(diff) < 20 else ("INDEX HAS MORE" if diff > 0 else "SRC HAS MORE")
    print(f"{comp_name:32} | index.html: {index_lines:4} lines | src: {src_lines:4} lines | Status: {status} ({diff:+d})")

