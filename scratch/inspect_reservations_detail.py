import json
import os

print("=== VERİTABANI REZERVASYON DETAY RAPORU ===")

res_path = 'scratch/db_reservations.json'
draft_path = 'scratch/db_draft_reservations.json'

reservations = []
if os.path.exists(res_path):
    with open(res_path, 'r', encoding='utf-8') as f:
        reservations = json.load(f)

drafts = []
if os.path.exists(draft_path):
    with open(draft_path, 'r', encoding='utf-8') as f:
        drafts = json.load(f)

print(f"\n✅ ONAYLI REZERVASYON SAYISI: {len(reservations)} Adet")
for idx, r in enumerate(reservations, 1):
    print(f"{idx}. [{r.get('id')}] {r.get('customerName')} - {r.get('venueName')}")
    print(f"   - Tarih: {r.get('date')} ({r.get('timeSlot')}) | Davetli: {r.get('guestCount')} Kişi")
    print(f"   - Toplam Tutar: {r.get('totalAmount'):,} TL | Ödeme Durumu: {r.get('paymentStatus')}")

print(f"\n📝 TASLAK REZERVASYON SAYISI: {len(drafts)} Adet")
for idx, d in enumerate(drafts, 1):
    print(f"{idx}. [{d.get('id')}] Müşteri: {d.get('customerName') or 'İsimsiz'}")
    print(f"   - Tarih: {d.get('date')} | Tutar: {d.get('totalAmount'):,} TL")
