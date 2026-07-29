import os

src_files = [
    'src/constants/mockData.js',
    'src/utils/formatters.js',
    'src/components/Navigation.jsx',
    'src/components/MobileBottomSummaryBar.jsx',
    'src/components/NotificationPopup.jsx',
    'src/components/Modals.jsx',
    'src/pages/DashboardPage.jsx',
    'src/pages/CreateReservationPage.jsx',
    'src/pages/ReservationsListPage.jsx',
    'src/pages/CustomersPage.jsx',
    'src/pages/CampaignsPage.jsx',
    'src/pages/ReportsPage.jsx',
    'src/pages/SettingsPage.jsx',
    'src/pages/VenuesPage.jsx',
    'src/pages/ServicesPage.jsx',
    'src/pages/UsersPage.jsx',
    'src/App.jsx',
    'src/main.jsx',
    'src/index.css'
]

print("=== SRC MODULAR CODEBASE INTEGRITY CHECK ===")
for fpath in src_files:
    if os.path.exists(fpath):
        lines = len(open(fpath, 'r', encoding='utf-8').readlines())
        size = os.path.getsize(fpath)
        print(f"✅ {fpath:45s} | {lines:4d} lines | {size:6d} bytes")
    else:
        print(f"❌ {fpath:45s} | MISSING!")
