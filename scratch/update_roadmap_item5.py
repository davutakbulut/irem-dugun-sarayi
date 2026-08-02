import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 5:
        item["status"] = "✅ Tamamlandı (v1.5.08)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.08"
release_note = {
    "version": "v1.5.08",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Otomatik Kapora Takibi ve Süre Aşımı Bildirimi (DepositExpirationTracker v1.5.08)",
    "description": "119 maddelik yol haritasının 5. maddesi otonom yapay zeka hattı tarafından tamamlandı. Kaporası henüz ödenmemiş taslak rezervasyonlar için 7 günlük otomatik opsiyon süresi takibi ve ikaz rozeti entegre edildi. Salon takviminin gereksiz yere kilitlenmesi engellendi. GitHub Project #2 panosunda Madde #5 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #5 to Completed and bumped DB to v1.5.08")
