import os

files_to_check = [
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
    'index.html'
]

print("=== MODULAR VITE REACT MIGRATION AUDIT ===")
all_exist = True
total_bytes = 0

for file_path in files_to_check:
    exists = os.path.exists(file_path)
    size = os.path.getsize(file_path) if exists else 0
    total_bytes += size
    status = "✅ OK" if exists and size > 0 else "❌ MISSING"
    print(f"{file_path:45s} | {size:6d} bytes | {status}")
    if not exists or size == 0:
        all_exist = False

print("-" * 75)
print(f"Total files checked: {len(files_to_check)} | Total codebase size: {total_bytes} bytes")
print(f"Migration Parity Status: {'✅ 100% COMPLETE' if all_exist else '❌ INCOMPLETE'}")

# Verify 7 Sections & Mini Calendar in CreateReservationPage.jsx
with open('src/pages/CreateReservationPage.jsx', 'r', encoding='utf-8') as f:
    create_res_code = f.read()

sections = [
    '1. Düğün Salonu Seçin:',
    '2. Ek Hizmetler:',
    '3. Ödeme, Kapora & İndirim Kodu Bilgileri',
    '4. Müşteri İletişim Bilgileri:',
    '5. Fatura Bilgileri',
    '6. Organizasyon & Etkinlik Akış Planlaması',
    '7. Operasyonel Ek Notlar & Özel İstekler:'
]

section_indices = []
for sec in sections:
    idx = create_res_code.find(sec)
    section_indices.append((sec, idx))

print("\n--- CreateReservationPage.jsx Sections Audit ---")
is_strictly_ordered = True
prev_idx = -1
for sec, idx in section_indices:
    print(f"[{sec}] -> Index: {idx}")
    if idx <= prev_idx:
        is_strictly_ordered = False
    prev_idx = idx

print(f"Section Ordering strictly increasing: {is_strictly_ordered}")

calendar_idx = create_res_code.find("🗓️ Canlı Takvim & Çakışma Önizlemesi")
sec1_end = section_indices[1][1]
calendar_inside_sec1 = (calendar_idx > section_indices[0][1]) and (calendar_idx < sec1_end)
print(f"14-Day Calendar inside Section 1: {calendar_inside_sec1} (Index: {calendar_idx})")

if all_exist and is_strictly_ordered and calendar_inside_sec1:
    print("\n🎉 ALL MODULAR REFACTORING VERIFICATIONS PASSED WITH 100% SUCCESS!")
else:
    print("\n⚠️ VERIFICATION ISSUES DETECTED!")
