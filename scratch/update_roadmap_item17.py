import json
import re

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "MediaRetentionGuard (v1.5.20)" not in html:
    html = html.replace(
        '<span>🖼️ Otomatik Filigran (v1.5.19)</span>\n                  </span>',
        '<span>🖼️ Otomatik Filigran (v1.5.19)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-sky-500/10 text-sky-700 dark:text-sky-300 border border-sky-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="MediaRetentionGuard v1.5.20: 30 Gün Saklama & Otomatik Arşiv Uyarısı">\n                    <span>⏳ 30 Gün Saklama & Arşiv Kalkanı (v1.5.20)</span>\n                  </span>'
    )

# Add Retention Banner in Media section if not present
if "30 Günlük Medya Saklama Garantisi" not in html:
    html = html.replace(
        'Mükerrer Engeli\n                </span>',
        'Mükerrer Engeli\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-sky-700 dark:text-sky-300 bg-sky-500/10 px-2 py-0.5 rounded-md border border-sky-500/20 font-bold" title="MediaRetentionGuard v1.5.20: 30 Günlük Saklama Garantisi Kalkanı">\n                  ⏳ 30 Gün Saklama (v1.5.20)\n                </span>'
    )

html = html.replace('v1.5.19', 'v1.5.20')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.20 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.20"
db["lastUpdated"] = "2026-08-02T03:40:00Z"

item17_note = {
    "version": "v1.5.20",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Medya Retention & Otomatik Silme Uyarısı (MediaRetentionGuard v1.5.20)",
    "description": "119 maddelik yol haritasının 17. maddesi otonom yapay zeka hattı tarafından tamamlandı. Düğün bittikten sonra yüklenen fotoğrafların 30 gün boyunca güvenle saklanacağını belirten geri sayım sayacı, otomatik e-posta/SMS saklama uyarısı ve .ZIP arşivleme kalkanı entegre edildi. GitHub Project #2 panosunda Madde #17 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.20" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item17_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.20.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 17:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.20"
            item["completedAt"] = "2026-08-02T03:40:00Z"
            print(f"Roadmap Item #17 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
