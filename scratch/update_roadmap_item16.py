import json
import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

if "WatermarkShield v1.5.19" not in html:
    html = html.replace(
        'Mükerrer Engeli\n                </span>',
        'Mükerrer Engeli\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-indigo-700 dark:text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20 font-bold" title="WatermarkShield v1.5.19: Görsellere Otomatik Şeffaf İrem Düğün Sarayı Filigranı Uygulanır">\n                  🖼️ Otomatik Filigran (v1.5.19)\n                </span>'
    )

if "Otomatik Filigran (v1.5.19)" not in html:
    html = html.replace(
        '<span>⏱️ Canlı Otomatik Kayıt</span>\n                  </span>',
        '<span>⏱️ Canlı Otomatik Kayıt</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border border-indigo-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="Otomatik Filigran & Telif Kalkanı v1.5.19">\n                    <span>🖼️ Otomatik Filigran (v1.5.19)</span>\n                  </span>'
    )

html = html.replace('v1.5.18', 'v1.5.19')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.19 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.19"
db["lastUpdated"] = "2026-08-02T03:30:00Z"

item16_note = {
    "version": "v1.5.19",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Otomatik Filigran / Watermark Ekleme Modülü (WatermarkShield v1.5.19)",
    "description": "119 maddelik yol haritasının 16. maddesi otonom yapay zeka hattı tarafından tamamlandı. Yüklenen tüm düğün fotoğraflarına ve mekan görsellerine şeffaf İrem Düğün Sarayı logosu ve telif filigranı ekleyen WatermarkShield motoru entegre edildi. GitHub Project #2 panosunda Madde #16 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.19" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item16_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.19.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 16:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.19"
            item["completedAt"] = "2026-08-02T03:30:00Z"
            print(f"Roadmap Item #16 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
