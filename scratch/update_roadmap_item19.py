import json
import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "AutoVideoThumbnailGenerator (v1.5.22)" not in html:
    html = html.replace(
        '<span>🛡️ Toplu Moderasyon Modu (v1.5.21)</span>\n                  </span>',
        '<span>🛡️ Toplu Moderasyon Modu (v1.5.21)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-purple-500/10 text-purple-700 dark:text-purple-300 border border-purple-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="AutoVideoThumbnailGenerator v1.5.22: Otomatik Video Kapak Resmi & Poster Motoru">\n                    <span>🎥 Video Kapak Motoru (v1.5.22)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "Video Kapak (v1.5.22)" not in html:
    html = html.replace(
        '🛡️ Toplu Moderasyon (v1.5.21)\n                </span>',
        '🛡️ Toplu Moderasyon (v1.5.21)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-purple-700 dark:text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded-md border border-purple-500/20 font-bold" title="AutoVideoThumbnailGenerator v1.5.22: Otomatik Video Kapak Resmi & Poster Motoru">\n                  🎥 Video Kapak (v1.5.22)\n                </span>'
    )

html = html.replace('v1.5.21', 'v1.5.22')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.22 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.22"
db["lastUpdated"] = "2026-08-02T04:00:00Z"

item19_note = {
    "version": "v1.5.22",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Video Thumbnail Otomatik Oluşturucu (AutoVideoThumbnailGenerator v1.5.22)",
    "description": "119 maddelik yol haritasının 19. maddesi otonom yapay zeka hattı tarafından tamamlandı. Yüklenen tüm düğün ve organizasyon videolarından ilk kare (poster frame) kapağını otomatik oluşturan ve bant genişliğini koruyan video thumbnail motoru entegre edildi. GitHub Project #2 panosunda Madde #19 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.22" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item19_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.22.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 19:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.22"
            item["completedAt"] = "2026-08-02T04:00:00Z"
            print(f"Roadmap Item #19 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
