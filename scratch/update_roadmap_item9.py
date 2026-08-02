import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 9:
        item["status"] = "✅ Tamamlandı (v1.5.12)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.12"
release_note = {
    "version": "v1.5.12",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Görsel Oturma Planı Tasarlayıcı (VisualSeatingChartPlanner v1.5.12)",
    "description": "119 maddelik yol haritasının 9. maddesi otonom yapay zeka hattı tarafından tamamlandı. Protokol, VIP ve aile masaları için görsel oturma planı ve masa düzeni ikaz rozeti entegre edildi. GitHub Project #2 panosunda Madde #9 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #9 to Completed and bumped DB to v1.5.12")
