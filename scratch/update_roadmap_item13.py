import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 13:
        item["status"] = "✅ Tamamlandı (v1.5.16)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.16"
release_note = {
    "version": "v1.5.16",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Otomatik EXIF Konum & Metadata Temizliği (EXIFMetadataCleaner v1.5.16)",
    "description": "119 maddelik yol haritasının 13. maddesi otonom yapay zeka hattı tarafından tamamlandı. Misafirlerin canlı albüme yüklediği fotoğraflardan GPS konum koordinatlarını ve cihaz detaylarını otomatik arındıran KVKK koruma kalkanı entegre edildi. GitHub Project #2 panosunda Madde #13 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #13 to Completed and bumped DB to v1.5.16")
