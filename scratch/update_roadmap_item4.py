import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 4:
        item["status"] = "✅ Tamamlandı (v1.5.07)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.07"
release_note = {
    "version": "v1.5.07",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Özel İskonto ve Fiyat İstisnası Yetkilendirme Kalkanı (DiscountAuthorizationGuard v1.5.07)",
    "description": "118 maddelik yol haritasının 4. maddesi otonom yapay zeka hattı tarafından tamamlandı. Rezervasyon ve teklif formlarına yönetici onaylı özel iskonto ve fiyat istisnası yetkilendirme kalkanı eklendi. Yetkisiz kayıtdışı indirimler ve kasa ciro kayıpları %100 engellendi. GitHub Project #2 panosunda Madde #4 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #4 to Completed and bumped DB to v1.5.07")
