import os
import re

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

required_components = [
    'DashboardComponent',
    'CreateReservationPageComponent',
    'ReservationsListComponent',
    'CalendarComponent',
    'CampaignsComponent',
    'ReportsComponent',
    'FinanceComponent',
    'VenuesComponent',
    'ServicesComponent',
    'CustomersComponent',
    'UsersComponent',
    'SettingsComponent',
    'MindMapPageComponent',
    'ProfileComponent',
    'MediaComponent'
]

print("=== CHECKING ALL 15 COMPONENTS IN index.html ===")

missing = []
for comp in required_components:
    if f'function {comp}' in index_html or f'const {comp}' in index_html:
        print(f"  ✅ {comp} found in index.html")
    else:
        print(f"  ❌ {comp} MISSING in index.html")
        missing.append(comp)

if missing:
    print(f"\nMissing components to add/sync in index.html: {missing}")
else:
    print("\nAll 15 components are present in index.html!")

