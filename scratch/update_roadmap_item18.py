import json
import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "AdminModerationMode (v1.5.21)" not in html:
    html = html.replace(
        '<span>⏳ 30 Gün Saklama & Arşiv Kalkanı (v1.5.20)</span>\n                  </span>',
        '<span>⏳ 30 Gün Saklama & Arşiv Kalkanı (v1.5.20)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="AdminModerationMode v1.5.21: Toplu Medya Onayı & İçerik Denetimi">\n                    <span>🛡️ Toplu Moderasyon Modu (v1.5.21)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "Toplu Moderasyon (v1.5.21)" not in html:
    html = html.replace(
        '🖼️ Otomatik Filigran (v1.5.20)\n                </span>',
        '🖼️ Otomatik Filigran (v1.5.20)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-emerald-700 dark:text-emerald-300 bg-emerald-500/10 px-2 py-0.5 rounded-md border border-emerald-500/20 font-bold" title="AdminModerationMode v1.5.21: Toplu Medya Onay Modu & İçerik Kalkanı">\n                  🛡️ Toplu Moderasyon (v1.5.21)\n                </span>'
    )

html = html.replace('v1.5.20', 'v1.5.21')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.21 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.21"
db["lastUpdated"] = "2026-08-02T03:50:00Z"

item18_note = {
    "version": "v1.5.21",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Toplu Medya Onay Modu (AdminModerationMode v1.5.21)",
    "description": "119 maddelik yol haritasının 18. maddesi otonom yapay zeka hattı tarafından tamamlandı. Davetlilerin yüklediği fotoğrafların canlı akışa girmeden önce yöneticinin onayından geçmesini sağlayan modül, toplu onaylama/reddetme paneli ve içerik denetim kalkanı entegre edildi. GitHub Project #2 panosunda Madde #18 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.21" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item18_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.21.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 18:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.21"
            item["completedAt"] = "2026-08-02T03:50:00Z"
            print(f"Roadmap Item #18 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
