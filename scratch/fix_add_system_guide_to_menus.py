import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Vertical Sidebar Menu array under YÖNETİM & AYARLAR
old_sidebar_settings = "{ id: 'settings', label: 'Sistem Ayarları', icon: 'settings', fallbackEmoji: '⚙️' }"
new_sidebar_settings = "{ id: 'settings', label: 'Sistem Ayarları', icon: 'settings', fallbackEmoji: '⚙️' },\n                        { id: 'system-guide', label: 'Sistem Kılavuzu & Mimarisi', icon: 'sparkles', fallbackEmoji: '📖', badge: 'V1.4 MASTER' }"

if old_sidebar_settings in html:
    html = html.replace(old_sidebar_settings, new_sidebar_settings)
    print("Added Sistem Kılavuzu & Mimarisi to Vertical Sidebar Menu!")

# 2. Update Horizontal Navbar Menu array under Yönetim & Ayarlar
old_navbar_settings = "{ id: 'settings', label: 'Tüm Sistem Ayarları', desc: 'Genel yapılandırma ve gelişmiş tercihler', icon: 'settings', fallbackEmoji: '⚙️' }"
new_navbar_settings = "{ id: 'settings', label: 'Tüm Sistem Ayarları', desc: 'Genel yapılandırma ve gelişmiş tercihler', icon: 'settings', fallbackEmoji: '⚙️' },\n            { id: 'system-guide', label: 'Sistem Kılavuzu & Mimarisi', desc: 'Tüm 16 sayfa, 11 tema, veritabanı mimarisi ve 10 Vercel Ajan Yeteneği', icon: 'sparkles', fallbackEmoji: '📖', badge: 'V1.4 MASTER' }"

if old_navbar_settings in html:
    html = html.replace(old_navbar_settings, new_navbar_settings)
    print("Added Sistem Kılavuzu & Mimarisi to Horizontal Navbar Menu!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html menu arrays successfully!")
