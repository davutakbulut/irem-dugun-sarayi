import json

print("=== VERİTABANI DÜĞÜN SALONLARI & EK HİZMETLER RAPORU ===")

with open('scratch/db_venues.json', 'r', encoding='utf-8') as f:
    venues = json.load(f)

with open('scratch/db_services.json', 'r', encoding='utf-8') as f:
    services = json.load(f)

print(f"\n🏰 TOPLAM MEKAN / SALON SAYISI: {len(venues)}\n")
for idx, v in enumerate(venues, 1):
    print(f"{idx}. {v.get('name')} (ID: {v.get('id')})")
    print(f"   - Kategori: {v.get('category')}")
    print(f"   - Kapasite: {v.get('capacity')} Kişi")
    print(f"   - Fiyat: {v.get('price'):,} TL | Maliyet: {v.get('costPrice'):,} TL | Kapora: {v.get('deposit'):,} TL")
    print(f"   - Etkinlik Türleri: {', '.join(v.get('eventTypes', []))}")
    print(f"   - Açıklama: {v.get('description')}\n")

print(f"🛠️ TOPLAM EK HİZMET SAYISI: {len(services)}\n")
for idx, s in enumerate(services, 1):
    unit_str = "Kişi Başı" if s.get('pricingType') == 'per_person' else "Sabit Paket"
    print(f"{idx}. {s.get('name')} (ID: {s.get('id')})")
    print(f"   - Kategori: {s.get('category')}")
    print(f"   - Fiyat: {s.get('price'):,} TL ({unit_str}) | Maliyet: {s.get('costPrice'):,} TL")
    print(f"   - Sıra (Order): {s.get('order') or s.get('sortOrder')}")
    print(f"   - Açıklama: {s.get('description')}\n")
