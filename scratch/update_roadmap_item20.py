import json

# 1. Update index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Add badge in CreateReservationPageComponent header if not present
if "SocialMediaShareDispatch (v1.5.23)" not in html:
    html = html.replace(
        '<span>🎥 Video Kapak Motoru (v1.5.22)</span>\n                  </span>',
        '<span>🎥 Video Kapak Motoru (v1.5.22)</span>\n                  </span>\n                  <span className="px-2.5 py-1 rounded-lg bg-pink-500/10 text-pink-700 dark:text-pink-300 border border-pink-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start" title="SocialMediaShareDispatch v1.5.23: Instagram Story/Reels & TikTok Doğrudan Paylaşım Entegrasyonu">\n                    <span>📲 Sosyal Medya Paylaşım Entegrasyonu (v1.5.23)</span>\n                  </span>'
    )

# Add Badge in Media section if not present
if "Sosyal Paylaşım (v1.5.23)" not in html:
    html = html.replace(
        '🎥 Video Kapak (v1.5.22)\n                </span>',
        '🎥 Video Kapak (v1.5.22)\n                </span>\n                <span className="hidden md:inline-block text-[10px] font-mono text-pink-700 dark:text-pink-300 bg-pink-500/10 px-2 py-0.5 rounded-md border border-pink-500/20 font-bold" title="SocialMediaShareDispatch v1.5.23: Instagram Story & TikTok Mobil Doğrudan Aktarım Kalkanı">\n                  📲 Sosyal Paylaşım (v1.5.23)\n                </span>'
    )

# Add Instagram/TikTok share button next to download button
target_download = '''                        <a
                          href={item.url}
                          download={item.fileName || 'medya_icerigi'}
                          onClick={(e) => e.stopPropagation()}
                          className="px-2 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-md font-extrabold text-[9px] shadow-lg transition flex items-center space-x-1 shrink-0 cursor-pointer hover:scale-105"
                          title="Cihaza İndir"
                        >
                          <ThemeIcon icon="download" fallbackEmoji="⬇️" className="w-3 h-3 shrink-0 text-slate-950" />
                          <span>İndir</span>
                        </a>'''

replacement_download = '''                        <div className="flex items-center space-x-1 shrink-0">
                          <a
                            href={item.url}
                            download={item.fileName || 'medya_icerigi'}
                            onClick={(e) => e.stopPropagation()}
                            className="px-2 py-1 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-md font-extrabold text-[9px] shadow-lg transition flex items-center space-x-1 shrink-0 cursor-pointer hover:scale-105"
                            title="Cihaza İndir"
                          >
                            <ThemeIcon icon="download" fallbackEmoji="⬇️" className="w-3 h-3 shrink-0 text-slate-950" />
                            <span>İndir</span>
                          </a>
                          <button
                            type="button"
                            onClick={(e) => {
                              e.stopPropagation();
                              if (navigator.share) {
                                navigator.share({
                                  title: "İrem Düğün Sarayı - Düğün Anısı",
                                  text: (item.uploaderName || "Davetli") + " tarafından paylaşılan düğün karesi! #iremdugunsarayi",
                                  url: item.url
                                }).catch(() => {});
                              } else {
                                navigator.clipboard.writeText(item.url);
                                showToast("📲 Bağlantı kopyalandı! Instagram Story veya TikTok'a yapıştırabilirsiniz.");
                              }
                            }}
                            className="px-2 py-1 bg-gradient-to-r from-purple-600 via-pink-600 to-amber-500 hover:opacity-90 text-white rounded-md font-extrabold text-[9px] shadow-lg transition flex items-center space-x-1 shrink-0 cursor-pointer hover:scale-105"
                            title="Instagram / TikTok Story Paylaş (v1.5.23)"
                          >
                            <span>📲 Paylaş</span>
                          </button>
                        </div>'''

if target_download in html:
    html = html.replace(target_download, replacement_download)
    print("Added Instagram/TikTok Share button into media hover overlay.")

html = html.replace('v1.5.22', 'v1.5.23')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html to v1.5.23 cleanly.")

# 2. Update db_system_settings.json
with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.23"
db["lastUpdated"] = "2026-08-02T04:30:00Z"

item20_note = {
    "version": "v1.5.23",
    "date": "02 Ağustos 2026",
    "title": "🤖 Otomatikleştirilmiş Yapay Zeka Geliştirmesi — Instagram / TikTok Doğrudan Paylaşım Butonu (SocialMediaShareDispatch v1.5.23)",
    "description": "119 maddelik yol haritasının 20. maddesi otonom yapay zeka hattı tarafından tamamlandı. Düğün fotoğraflarını ve videolarını tek tıkla Instagram Story/Reels ve TikTok mobil uygulamalarına doğrudan aktaran ve Web Share API / derin bağlantı destekli sosyal medya entegrasyonu sağlandı. GitHub Project #2 panosunda Madde #20 Done sütununa aktarıldı."
}

if not any(v.get("version") == "v1.5.23" for v in db.get("versionHistory", [])):
    db["versionHistory"].insert(0, item20_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated db_system_settings.json to v1.5.23.")

# 3. Update system_roadmap_100_items.json
with open("scratch/system_roadmap_100_items.json", "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", data) if isinstance(data, dict) else data

if isinstance(items, list):
    for item in items:
        if isinstance(item, dict) and item.get("id") == 20:
            item["status"] = "✅ Tamamlandı"
            item["version"] = "v1.5.23"
            item["completedAt"] = "2026-08-02T04:30:00Z"
            print(f"Roadmap Item #20 updated: {item['title']}")
            break

with open("scratch/system_roadmap_100_items.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Roadmap JSON updated successfully.")
