import json

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "VirtualPosIntegration (v1.5.27)" not in html:
    html = html.replace(
        '<span>💬 Ödeme Hatırlatma Servisi (v1.5.26)</span>\n                  </span>',
        '<span>💬 Ödeme Hatırlatma Servisi (v1.5.26)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border border-indigo-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="VirtualPosIntegration v1.5.27: Kredi Kartı & Sanal POS İzinli Tahsilat Entegrasyonu (PCI-DSS & 3D Secure)">\n                    <span>💳 Sanal POS & 3D Secure (v1.5.27)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "Sanal POS & 3D Secure (v1.5.27)" not in html:
    html = html.replace(
        '💬 Ödeme Hatırlatma (v1.5.26)\n                </span>',
        '💬 Ödeme Hatırlatma (v1.5.26)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-indigo-700 dark:text-indigo-300 bg-indigo-500/10 px-2 py-0.5 rounded-md border border-indigo-500/20 font-bold" title="VirtualPosIntegration v1.5.27: iZICO / PayTR Sanal POS & 3D Secure Tahsilat Entegrasyonu">\n                  💳 Sanal POS & 3D Secure (v1.5.27)\n                </span>'
    )

html = html.replace('v1.5.26', 'v1.5.27')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.27 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.27"
db["lastUpdated"] = "2026-08-03T04:30:00Z"

item24_note = {
    "version": "v1.5.27",
    "date": "03 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Kredi Kartı & Sanal POS İzinli Tahsilat Entegrasyonu (VirtualPosIntegration v1.5.27)",
    "description": "119 maddelik yol haritasının 24. maddesi otonom yapay zeka hattı tarafından tamamlandı. Düğün rezervasyon kaporası ve taksit ödemeleri için iZICO, PayTR ve Paratika PCI-DSS uyumlu Sanal POS entegrasyonu, 3D Secure (v2.2) OTP doğrulama simülasyonu ve otomatik POS komisyon gideri düşüm kalkanı entegre edildi. GitHub Project #2 panosunda Madde #24 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.27" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item24_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.27.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 24:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.27"
            item["completedAt"] = "2026-08-03T04:30:00Z"
            print(f"Roadmap Item #24 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
