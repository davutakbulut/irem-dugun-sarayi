import json
import os
import re
import sys

print("==================================================")
print("🚀 IMPLEMENTING AUTOMATIC DATABASE-BACKED VERSION UPDATER")
print("==================================================")

# 1. Update db_system_settings.json with systemVersion and versionHistory
db_file = 'scratch/db_system_settings.json'
existing_db = {}
if os.path.exists(db_file):
    try:
        with open(db_file, 'r', encoding='utf-8') as f:
            existing_db = json.load(f)
    except Exception: pass

existing_db['systemVersion'] = existing_db.get('systemVersion', 'v1.4.48')
existing_db['lastUpdated'] = existing_db.get('lastUpdated', '2026-08-01T02:45:00Z')

initial_history = [
    { "version": "v1.4.48", "date": "1 Ağustos 2026", "title": "Otomatik Veritabanı Sürüm Güncelleyici", "desc": "Sistemdeki her geliştirmede sürümün sunucu veritabanında (db_system_settings.json) otomatik yükselmesi ve canlı çekilmesi sağlandı." },
    { "version": "v1.4.47", "date": "1 Ağustos 2026", "title": "Sistem Master Kılavuzu & Mimarisi Sayfası", "desc": "Navigasyon menüsünün en altına 16 sayfa, 11 tema ve 10 Vercel yeteneğini içeren interaktif kılavuz eklendi." },
    { "version": "v1.4.45", "date": "1 Ağustos 2026", "title": "Vercel Labs Agent Skills Entegrasyonu", "desc": "10 adet resmi Vercel Yeteneği (.skills/) projeye entegre edildi." },
    { "version": "v1.4.43", "date": "1 Ağustos 2026", "title": "Ağ İstekleri Auto-Retry Mekanizması", "desc": "fetchWithRetry fonksiyonu ile mikro kesintilerde isteklerin 3 kez otomatik tekrar denenmesi sağlandı." },
    { "version": "v1.4.41", "date": "1 Ağustos 2026", "title": "%100 Tek Sunucu Veritabanı Mimarisi", "desc": "Tema ve Menü seçimleri 0ms server HTML attribute injection ile veritabanına bağlandı." }
]

existing_db['versionHistory'] = existing_db.get('versionHistory', initial_history)

with open(db_file, 'w', encoding='utf-8') as f:
    json.dump(existing_db, f, indent=2, ensure_ascii=False)

print(f"Updated {db_file} with systemVersion: {existing_db['systemVersion']}!")

# 2. Update build_precompiled.py to automatically auto-increment patch version in db_system_settings.json on every build!
with open('scratch/build_precompiled.py', 'r', encoding='utf-8') as f:
    build_py = f.read()

auto_inc_code = """
# Automatically Auto-Increment System Version in db_system_settings.json on build
try:
    db_path = os.path.join(os.path.dirname(__file__), 'db_system_settings.json')
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as dbf:
            db_data = json.load(dbf)
        cur_v = db_data.get('systemVersion', 'v1.4.48')
        v_match = re.search(r'v?(\d+)\.(\d+)\.(\d+)', cur_v)
        if v_match:
            major, minor, patch = v_match.groups()
            new_v = f"v{major}.{minor}.{int(patch) + 1}"
            db_data['systemVersion'] = new_v
            db_data['lastUpdated'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            with open(db_path, 'w', encoding='utf-8') as dbf:
                json.dump(db_data, dbf, indent=2, ensure_ascii=False)
            print(f"🚀 AUTO-INCREMENTED SYSTEM VERSION IN BACKEND DB: {cur_v} -> {new_v}")
except Exception as e:
    print("Auto-increment warning:", e)
"""

if "AUTO-INCREMENTED SYSTEM VERSION" not in build_py:
    build_py = auto_inc_code + "\n" + build_py

with open('scratch/build_precompiled.py', 'w', encoding='utf-8') as f:
    f.write(build_py)

print("Updated build_precompiled.py to auto-increment version on every build!")

# 3. Update index.html to bind header version badge and VersionHistoryModalComponent to systemVersion state from /api/system-settings
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add systemVersion state to App component
old_app_states = "const [themeColor, setThemeColor] = useState("
new_app_states = "const [systemVersion, setSystemVersion] = useState('v1.4.48');\n      const [versionHistoryState, setVersionHistoryState] = useState([]);\n      " + old_app_states

if "const [systemVersion, setSystemVersion]" not in html:
    html = html.replace(old_app_states, new_app_states, 1)
    print("Added systemVersion state to App component!")

# Update system-settings fetch response in App effect to update systemVersion
old_settings_fetch = "if (data.themeColor) {"
new_settings_fetch = """if (data.systemVersion) {
              setSystemVersion(data.systemVersion);
            }
            if (data.versionHistory) {
              setVersionHistoryState(data.versionHistory);
            }
            if (data.themeColor) {"""

if "if (data.systemVersion)" not in html and old_settings_fetch in html:
    html = html.replace(old_settings_fetch, new_settings_fetch, 1)
    print("Connected App system-settings fetch to setSystemVersion!")

# Replace hardcoded v1.4.0 badges in index.html with {systemVersion}
html = html.replace("Canlı Sistem (v1.4.0)", "Canlı Sistem ({systemVersion || 'v1.4.48'})")
html = html.replace("Sürüm Geçmişi (v1.4.0)", "Sürüm Geçmişi ({systemVersion || 'v1.4.48'})")
html = html.replace("Canlı Sistem (v1.4.45)", "Canlı Sistem ({systemVersion || 'v1.4.48'})")
html = html.replace("Sürüm: v1.4.45", "Sürüm: {systemVersion || 'v1.4.48'}")

# Pass systemVersion and versionHistoryState to VersionHistoryModalComponent
html = html.replace(
    "<VersionHistoryModalComponent isOpen={isVersionModalOpen} onClose={() => setIsVersionModalOpen(false)} />",
    "<VersionHistoryModalComponent isOpen={isVersionModalOpen} onClose={() => setIsVersionModalOpen(false)} systemVersion={systemVersion} versionHistory={versionHistoryState} />"
)

# Update VersionHistoryModalComponent to accept systemVersion and versionHistory props
old_modal_header = "function VersionHistoryModalComponent({ isOpen, onClose }) {"
new_modal_header = "function VersionHistoryModalComponent({ isOpen, onClose, systemVersion, versionHistory }) {"

if old_modal_header in html:
    html = html.replace(old_modal_header, new_modal_header)
    print("Updated VersionHistoryModalComponent signature!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html with dynamic systemVersion integration successfully!")
