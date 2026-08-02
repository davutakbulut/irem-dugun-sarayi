import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 8:
        item["status"] = "✅ Tamamlandı (v1.5.11)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.11"
release_note = {
    "version": "v1.5.11",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Salona Özel Kapasite Uyarısı (VenueCapacityOverLimitGuard v1.5.11)",
    "description": "119 maddelik yol haritasının 8. maddesi otonom yapay zeka hattı tarafından tamamlandı. Seçilen salon kapasitesini aşan davetli girişlerinde amber ikaz kalkanı ve aşırı yüklenme engeli entegre edildi. GitHub Project #2 panosunda Madde #8 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #8 to Completed and bumped DB to v1.5.11")
