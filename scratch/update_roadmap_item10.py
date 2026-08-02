import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 10:
        item["status"] = "✅ Tamamlandı (v1.5.13)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.13"
release_note = {
    "version": "v1.5.13",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Rezervasyon Geçmişi & Değişiklik Logu (ReservationAuditLog v1.5.13)",
    "description": "119 maddelik yol haritasının 10. maddesi otonom yapay zeka hattı tarafından tamamlandı. Tüm fiyat, tarih, davetli sayısı ve durum değişikliklerini zaman damgalı kaydeden denetim izi paneli entegre edildi. GitHub Project #2 panosunda Madde #10 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #10 to Completed and bumped DB to v1.5.13")
