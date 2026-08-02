import json

# 1. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data["items"]:
    if item["id"] == 3:
        item["status"] = "✅ Tamamlandı (v1.5.06)"

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.06"
release_note = {
    "version": "v1.5.06",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Sürükle-Bırak Tarih Güncelleme Güvenlik İkaz Kalkanı (RescheduleSafetyModal v1.5.06)",
    "description": "118 maddelik yol haritasının 3. maddesi otonom yapay zeka hattı tarafından tamamlandı. Takvim üzerinde rezervasyon tarihi sürüklendiğinde yanlışlıkla tarih kaydırmayı ve uyuşmazlıkları engelleyen güvenlik onay kalkanı, eski/yeni tarih karşılaştırması ve müşteriye otomatik SMS/WhatsApp bilgilendirme protokolü kuruldu. GitHub Project #2 panosunda Madde #3 Done sütununa aktarıldı."
}
db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated Roadmap Item #3 to Completed and bumped DB to v1.5.06")
