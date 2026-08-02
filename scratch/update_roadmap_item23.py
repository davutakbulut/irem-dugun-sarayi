import json

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "AutoPaymentReminderDispatch (v1.5.26)" not in html:
    html = html.replace(
        '<span>💳 Parçalı Ödeme & Taksit Sistemi (v1.5.25)</span>\n                  </span>',
        '<span>💳 Parçalı Ödeme & Taksit Sistemi (v1.5.25)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-sky-500/10 text-sky-700 dark:text-sky-300 border border-sky-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="AutoPaymentReminderDispatch v1.5.26: Otomatik Ödeme Hatırlatma SMS & WhatsApp Kalkanı">\n                    <span>💬 Ödeme Hatırlatma Servisi (v1.5.26)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "Ödeme Hatırlatma (v1.5.26)" not in html:
    html = html.replace(
        '💳 Parçalı Ödeme & Taksit (v1.5.25)\n                </span>',
        '💳 Parçalı Ödeme & Taksit (v1.5.25)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-sky-700 dark:text-sky-300 bg-sky-500/10 px-2 py-0.5 rounded-md border border-sky-500/20 font-bold" title="AutoPaymentReminderDispatch v1.5.26: Vadesi Yaklaşan Ödeme SMS & WhatsApp Hatırlatıcı Motoru">\n                  💬 Ödeme Hatırlatma (v1.5.26)\n                </span>'
    )

html = html.replace('v1.5.25', 'v1.5.26')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.26 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.26"
db["lastUpdated"] = "2026-08-03T04:00:00Z"

item23_note = {
    "version": "v1.5.26",
    "date": "03 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Otomatik Ödeme Hatırlatma SMS/WhatsApp Servisi (AutoPaymentReminderDispatch v1.5.26)",
    "description": "119 maddelik yol haritasının 23. maddesi otonom yapay zeka hattı tarafından tamamlandı. Vadesine 7 gün, 3 gün kalan ve vadesi geçen taksit ödemeleri için şablonlu WhatsApp ve SMS ödeme hatırlatma bağlantısı gönderen, Gece Kalkanı (Quiet Hours) ve sıklık sınırlamalı otomatik iletim kalkanı entegre edildi. GitHub Project #2 panosunda Madde #23 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.26" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item23_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.26.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 23:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.26"
            item["completedAt"] = "2026-08-03T04:00:00Z"
            print(f"Roadmap Item #23 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
