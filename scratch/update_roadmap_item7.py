import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 7:
        item["status"] = "✅ Tamamlandı (v1.5.10)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.10"
release_note = {
    "version": "v1.5.10",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Tekrarlanan Etkinlik Şablonları (RecurringEventTemplates v1.5.10)",
    "description": "119 maddelik yol haritasının 7. maddesi otonom yapay zeka hattı tarafından tamamlandı. Kurumsal bayi toplantıları, dernek yemekleri ve özel organizasyonlar için hızlı şablon seçimi ve otomatik alan doldurma motoru entegre edildi. GitHub Project #2 panosunda Madde #7 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #7 to Completed and bumped DB to v1.5.10")
