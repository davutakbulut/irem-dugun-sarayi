import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Header Brand Crown Badge to match Footer Crown Badge (Yellow gradient with crown icon)
old_header_badge = """<div className="w-9 h-9 sm:w-10 sm:h-10 rounded-xl gold-button flex items-center justify-center font-bold text-lg sm:text-xl shadow-lg shrink-0 group-hover:scale-105 transition" aria-hidden="true">
                      <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-5 h-5 text-amber-900 dark:text-gold-400" />
                    </div>"""

new_header_badge = """<div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white shadow-md shrink-0 group-hover:scale-105 transition" aria-hidden="true">
                      <ThemeIcon icon="crown" fallbackEmoji="" className="w-6 h-6 text-white" />
                    </div>"""

if old_header_badge in html:
    html = html.replace(old_header_badge, new_header_badge)
    print("Updated Header Logo to use yellow crown badge matching footer")

# 2. Sanitize raw emojis in RolesPageComponent and newly updated components
# Replace raw emojis in RolesPageComponent header and actions
html = html.replace('<span>🛡️ Sistem Rol Yönetimi & Sayfa İzin Matrisi</span>', '<ThemeIcon icon="shield" fallbackEmoji="" className="w-5 h-5 text-amber-500 inline-block mr-1.5" /><span>Sistem Rol Yönetimi & Sayfa İzin Matrisi</span>')
html = html.replace('<span>➕ Yeni Sistem Rolü Tanımla</span>', '<ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Yeni Sistem Rolü Tanımla</span>')
html = html.replace('<span>Sisteme Yeni Rolü Ekle +</span>', '<span>Sisteme Yeni Rolü Ekle</span>')
html = html.replace('<span>✏️ Düzenle</span>', '<ThemeIcon icon="edit" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Düzenle</span>')
html = html.replace('<span>🗑️ Sil</span>', '<ThemeIcon icon="trash" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Sil</span>')
html = html.replace('<span>✏️ Rol Unvanını Güncelle', '<ThemeIcon icon="edit" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Rol Unvanını Güncelle')
html = html.replace('<span>🛡️ Rol Yönetimi Sayfasına Git →</span>', '<ThemeIcon icon="shield" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Rol Yönetimi Sayfasına Git →</span>')

# Replace emojis in profile dropdown
html = html.replace('<span>👤</span>\n                          <span>Profilimi Düzenle</span>', '<ThemeIcon icon="user" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" /><span>Profilimi Düzenle</span>')
html = html.replace('<span>⚙️</span>\n                          <span>Sistem Ayarları</span>', '<ThemeIcon icon="settings" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" /><span>Sistem Ayarları</span>')
html = html.replace('<span>🚪</span>\n                          <span>Çıkış Yap</span>', '<ThemeIcon icon="logout" fallbackEmoji="" className="w-4 h-4 text-red-500 shrink-0" /><span>Çıkış Yap</span>')

# Replace emojis in CampaignModalComponent
html = html.replace("fallbackEmoji=\"🎁\"", "fallbackEmoji=\"\"")
html = html.replace("fallbackEmoji=\"➕\"", "fallbackEmoji=\"\"")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Sanitized inline emojis and updated header logo successfully!")
