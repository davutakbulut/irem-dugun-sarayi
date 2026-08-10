import json
import os

print("=== CANLI VERİTABANI GÜNCEL DURUM RAPORU ===")

db_dir = 'scratch'

files = {
    'venues': 'db_venues.json',
    'services': 'db_services.json',
    'reservations': 'db_reservations.json',
    'draftReservations': 'db_draft_reservations.json',
    'customers': 'db_customers.json',
    'campaigns': 'db_campaigns.json',
    'users': 'db_users.json',
    'systemSettings': 'db_system_settings.json'
}

data = {}

for key, filename in files.items():
    path = os.path.join(db_dir, filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data[key] = json.load(f)
        except Exception as e:
            data[key] = f"Error: {e}"
    else:
        data[key] = "File not found"

print(f"\n1. 🏰 MEKANLAR / SALONLAR ({len(data.get('venues', [])) if isinstance(data.get('venues'), list) else 0} adet):")
if isinstance(data.get('venues'), list):
    for v in data['venues']:
        print(f"   - [{v.get('id')}] {v.get('name')} | Kapasite: {v.get('capacity')} | Fiyat: {v.get('price'):,} TL | Maliyet: {v.get('costPrice'):,} TL")

print(f"\n2. 🛠️ EK HİZMETLER ({len(data.get('services', [])) if isinstance(data.get('services'), list) else 0} adet):")
if isinstance(data.get('services'), list):
    for s in data['services']:
        print(f"   - [{s.get('id')}] {s.get('name')} | Fiyat: {s.get('price'):,} TL | Maliyet: {s.get('costPrice'):,} TL")

print(f"\n3. 📅 ONAYLI REZERVASYONLAR ({len(data.get('reservations', [])) if isinstance(data.get('reservations'), list) else 0} adet):")
if isinstance(data.get('reservations'), list):
    for r in data['reservations']:
        print(f"   - [{r.get('id')}] {r.get('customerName')} | {r.get('venueName')} | Tarih: {r.get('date')} | Tutar: {r.get('totalAmount'):,} TL")

print(f"\n4. 📝 TASLAK REZERVASYONLAR ({len(data.get('draftReservations', [])) if isinstance(data.get('draftReservations'), list) else 0} adet):")
if isinstance(data.get('draftReservations'), list):
    for d in data['draftReservations']:
        print(f"   - [{d.get('id')}] {d.get('customerName')} | Tarih: {d.get('date')} | Tutar: {d.get('totalAmount'):,} TL")

print(f"\n5. 👤 MÜŞTERİLER ({len(data.get('customers', [])) if isinstance(data.get('customers'), list) else 0} adet):")
if isinstance(data.get('customers'), list):
    for c in data['customers']:
        print(f"   - [{c.get('id')}] {c.get('name')} | Tel: {c.get('phone')}")

sys_cfg = data.get('systemSettings', {})
if isinstance(sys_cfg, dict):
    print(f"\n6. 🎨 AKTİF TEMA & AYARLAR:")
    print(f"   - Tema Renk Kodu: {sys_cfg.get('themeColor')}")
    print(f"   - Menü Yerleşimi: {sys_cfg.get('menuLayout')}")
    print(f"   - Sistem Sürümü: {sys_cfg.get('systemVersion')}")
