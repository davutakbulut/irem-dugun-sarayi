import json
import re

# 1. Update index.html
with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Update version badges in index.html
# Add v1.5.29 badge for VendorLedgerTracker
new_badge = '''                <span className="hidden md:inline-block text-[10px] font-mono text-purple-700 dark:text-purple-300 bg-purple-500/10 px-2 py-0.5 rounded-md border border-purple-500/20 font-bold" title="VendorLedgerTracker v1.5.29: Cari Hesap & Tedarikçi Borç-Alacak Takip Kalkanı">
                  🤝 Tedarikçi Cari (v1.5.29)
                </span>'''

if 'VendorLedgerTracker v1.5.29' not in html_content:
    # Insert after ExpenseVendorTracker badge
    target_str = '📊 Gider & Net Kar (v1.5.28)\n                </span>'
    if target_str in html_content:
        html_content = html_content.replace(target_str, target_str + '\n' + new_badge)

# Replace remaining v1.5.28 version footer strings if needed
html_content = html_content.replace('v1.5.28 🤖 Otomatik Yapay Zeka Geliştirmesi', 'v1.5.29 🤖 Otomatik Yapay Zeka Geliştirmesi')

with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)
print("index.html updated successfully!")

# 2. Update db_system_settings.json
with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
    db_data = json.load(f)

db_data['systemVersion'] = 'v1.5.29'
if 'releaseNotes' not in db_data:
    db_data['releaseNotes'] = []
db_data['releaseNotes'].append({
    'version': 'v1.5.29',
    'date': '2026-08-03T05:00:00Z',
    'title': 'Cari Hesap & Tedarikçi Borç-Alacak Takibi (VendorLedgerTracker v1.5.29)',
    'details': 'Çiçekçi, fotoğrafçı, orkestra, catering ve diğer dış hizmet tedarikçilerinin cari hesap bakiyelerinin tutulması, borç-alacak ekstralarının üretilmesi ve mutabakat kalkanı.'
})

with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
    json.dump(db_data, f, ensure_ascii=False, indent=2)
print("db_system_settings.json updated successfully!")

# 3. Update system_roadmap_100_items.json
with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/scratch/system_roadmap_100_items.json', 'r', encoding='utf-8') as f:
    roadmap_data = json.load(f)

for item in roadmap_data.get('items', []):
    if item['id'] == 26:
        item['status'] = '✅ Tamamlandı'
        item['version'] = 'v1.5.29'
        item['completedAt'] = '2026-08-03T05:00:00Z'
        break

with open('/Users/davutakbulut/.gemini/antigravity/scratch/irem_dugun_sarayi/scratch/system_roadmap_100_items.json', 'w', encoding='utf-8') as f:
    json.dump(roadmap_data, f, ensure_ascii=False, indent=2)
print("system_roadmap_100_items.json updated successfully!")
