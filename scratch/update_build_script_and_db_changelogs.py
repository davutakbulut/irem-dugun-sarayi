import os
import json

# 1. Update db_system_settings.json versionHistory entries
db_path = 'scratch/db_system_settings.json'
with open(db_path, 'r', encoding='utf-8') as f:
    db_data = json.load(f)

# Map specific detailed changelogs for v1.4.65 down to v1.4.59
custom_entries = {
    "v1.4.65": {
        "title": "🧹 Sistem Kılavuzu (`#/sistem-kilavuzu`) `find-skills` Temizliği",
        "desc": "Sistem Kılavuzu sayfasındaki Vercel Ajan Yetenekleri listesinden artık kullanılmayan find-skills kartı kaldırıldı ve aktif yetenek sayısı 9 adede güncellendi."
    },
    "v1.4.64": {
        "title": "🧼 Footer Mükerrer Sürüm Geçmişi Bağlantısı Temizliği",
        "desc": "Footer telif barındaki mükerrer Sürüm Geçmişi metin linki kaldırıldı, kurumsal sol sütundaki tekil yeşil Canlı Sistem rozeti korundu."
    },
    "v1.4.63": {
        "title": "📖 Sistem Kılavuzu Rota & RBAC İzin Entegrasyonu",
        "desc": "sistem-kilavuzu ve system-guide rotaları SLUG_TO_TAB haritasına, RBAC izin matrisine ve App render bloğuna eklenerek 404 hatası tamamen çözüldü."
    },
    "v1.4.62": {
        "title": "🐛 VersionHistoryModal Tanımsız Değişken ReferenceError Tamiri",
        "desc": "App bileşeni içerisindeki VersionHistoryModalComponent çağrısında kalan tanımsız systemSettings değişkeni temizlendi, canlı sürüm aktarımı sağlandı."
    },
    "v1.4.61": {
        "title": "⚙️ React App systemVersionState Eşleşme Bağlantısı",
        "desc": "systemVersionState ReferenceError hatası düzeltildi, canlı sürüm state binding systemVersion prop'u ile bağlandı."
    },
    "v1.4.60": {
        "title": "⚡ VersionHistoryModal Dynamic Props Aktarımı",
        "desc": "App bileşenindeki VersionHistoryModalComponent çağrısına systemVersion ve versionHistory prop'ları dinamik veritabanı state'inden aktarıldı."
    },
    "v1.4.59": {
        "title": "📜 Veritabanı Canlı Sürüm Geçmişi Kataloğu Entegrasyonu",
        "desc": "db_system_settings.json içerisine v1.4.0'dan bu yana yapılan tüm mimari yeniliklerin detaylı changelog kataloğu işlendi."
    }
}

history = db_data.get('versionHistory', [])
for entry in history:
    v = entry.get('version')
    if v in custom_entries:
        entry['title'] = custom_entries[v]['title']
        entry['desc'] = custom_entries[v]['desc']

db_data['versionHistory'] = history

with open(db_path, 'w', encoding='utf-8') as f:
    json.dump(db_data, f, indent=2, ensure_ascii=False)

print("Updated db_system_settings.json with detailed custom changelogs successfully!")

# 2. Update scratch/build_precompiled.py to avoid hardcoded generic string
build_script_path = 'scratch/build_precompiled.py'
with open(build_script_path, 'r', encoding='utf-8') as f:
    build_code = f.read()

old_build_changelog_snippet = """            # Add automatic changelog entry
            history = db_data.get('versionHistory', [])
            history.insert(0, {
                "version": new_v,
                "date": time.strftime('%d Ağustos %Y', time.localtime()),
                "title": f"Otomatik Sürüm Güncellemesi ({new_v})",
                "desc": "Sistem veritabanında (db_system_settings.json) otomatik sürüm yükseltme ve canlı veri çekme mekanizması devreye girdi."
            })"""

new_build_changelog_snippet = """            # Add automatic changelog entry (reads from scratch/next_changelog.json if available, or env vars)
            changelog_info = {
                "title": os.environ.get('BUILD_CHANGELOG_TITLE', f"Sürüm Güncellemesi ({new_v})"),
                "desc": os.environ.get('BUILD_CHANGELOG_DESC', "Sistem mimarisi, UI/UX düzenlemeleri ve kod optimizasyonları yapıldı.")
            }
            next_cl_path = os.path.join(os.path.dirname(__file__), 'next_changelog.json')
            if os.path.exists(next_cl_path):
                try:
                    with open(next_cl_path, 'r', encoding='utf-8') as ncf:
                        next_cl = json.load(ncf)
                        changelog_info['title'] = next_cl.get('title', changelog_info['title'])
                        changelog_info['desc'] = next_cl.get('desc', changelog_info['desc'])
                    os.remove(next_cl_path)
                except Exception as e:
                    print("next_changelog error:", e)

            history = db_data.get('versionHistory', [])
            history.insert(0, {
                "version": new_v,
                "date": time.strftime('%d Ağustos %Y', time.localtime()),
                "title": changelog_info['title'],
                "desc": changelog_info['desc']
            })"""

if old_build_changelog_snippet in build_code:
    build_code = build_code.replace(old_build_changelog_snippet, new_build_changelog_snippet)
    with open(build_script_path, 'w', encoding='utf-8') as f:
        f.write(build_code)
    print("Updated build_precompiled.py dynamic changelog mechanism successfully!")
else:
    print("Could not find old_build_changelog_snippet in build_precompiled.py!")
