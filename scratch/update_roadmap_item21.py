import json

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "EInvoiceArchiveSimulator (v1.5.24)" not in html:
    html = html.replace(
        '<span>📲 Sosyal Medya Paylaşım Entegrasyonu (v1.5.23)</span>\n                  </span>',
        '<span>📲 Sosyal Medya Paylaşım Entegrasyonu (v1.5.23)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-teal-500/10 text-teal-700 dark:text-teal-300 border border-teal-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="EInvoiceArchiveSimulator v1.5.24: GİB Uyumlu UBL-TR 1.2 e-Fatura & e-Arşiv Simülasyon Kalkanı">\n                    <span>🧾 e-Fatura & e-Arşiv Simülatörü (v1.5.24)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "e-Fatura & e-Arşiv (v1.5.24)" not in html:
    html = html.replace(
        '📲 Sosyal Paylaşım (v1.5.23)\n                </span>',
        '📲 Sosyal Paylaşım (v1.5.23)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-teal-700 dark:text-teal-300 bg-teal-500/10 px-2 py-0.5 rounded-md border border-teal-500/20 font-bold" title="EInvoiceArchiveSimulator v1.5.24: GİB Uyumlu e-Fatura & e-Arşiv Fatura Simülasyonu">\n                  🧾 e-Fatura & e-Arşiv (v1.5.24)\n                </span>'
    )

html = html.replace('v1.5.23', 'v1.5.24')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.24 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.24"
db["lastUpdated"] = "2026-08-03T03:00:00Z"

item21_note = {
    "version": "v1.5.24",
    "date": "03 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — GİB Uyumlu e-Fatura & e-Arşiv Entegrasyon Simülasyonu (EInvoiceArchiveSimulator v1.5.24)",
    "description": "119 maddelik yol haritasının 21. maddesi otonom yapay zeka hattı tarafından tamamlandı. Kesilen düğün sözleşmeleri ve kaparo tahsilatları için Türkiye Gelir İdaresi Başkanlığı (GİB) VUK mevzuatına ve UBL-TR 1.2 standardına uygun e-Fatura / e-Arşiv taslak ve QR kodlu PDF simülatörü entegre edildi. GitHub Project #2 panosunda Madde #21 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.24" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item21_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.24.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 21:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.24"
            item["completedAt"] = "2026-08-03T03:00:00Z"
            print(f"Roadmap Item #21 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
