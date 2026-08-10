import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add '/yonetim/eposta-sablonlari' mapping to URL_TO_TAB
old_url_map = "'settings-errors': '/yonetim/ayarlar/hata-simulasyonu',"
new_url_map = "'settings-errors': '/yonetim/ayarlar/hata-simulasyonu',\n      'email-templates': '/yonetim/eposta-sablonlari',"

if old_url_map in content:
    content = content.replace(old_url_map, new_url_map, 1)
    print("1. Added '/yonetim/eposta-sablonlari' to URL_TO_TAB.")

# 2. Add to Mobile Drawer Menu under SETTINGS LINKS IN DRAWER
old_drawer = """                        <button
                          onClick={() => { navigateTo('settings-appearance'); setIsMobileMenuOpen(false); }}
                          className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left cursor-pointer ${
                            activeTab === 'settings-appearance' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                          }`}
                        >
                          <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                          <span>Görünüm & Tema Ayarları</span>
                        </button>"""

new_drawer = old_drawer + """
                        <button
                          onClick={() => { navigateTo('email-templates'); setIsMobileMenuOpen(false); }}
                          className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left cursor-pointer ${
                            activeTab === 'email-templates' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                          }`}
                        >
                          <ThemeIcon icon="mail" fallbackEmoji="" className="w-4 h-4 shrink-0 text-amber-500" />
                          <span>E-Posta Şablonları & Otomasyon</span>
                        </button>"""

if old_drawer in content:
    content = content.replace(old_drawer, new_drawer, 1)
    print("2. Added E-Posta Şablonları & Otomasyon to Mobile Drawer Navigation.")

# 3. Add to Desktop Mega Menu (menuGroups) under 'Yönetim & Ayarlar'
old_mega_item = "{ id: 'settings-appearance', label: 'Görünüm & Temalar', desc: '5 kurumsal renk teması, buton tarzları ve görünüm modu', icon: 'sparkles', fallbackEmoji: '' },"
new_mega_item = old_mega_item + "\n            { id: 'email-templates', label: 'E-Posta Şablonları & Otomasyon', desc: 'Canlı HTML şablon önizleme, SMTP gönderim testi ve otomasyon ayarları', icon: 'mail', fallbackEmoji: '', badge: 'SMTP 200 OK' },"

if old_mega_item in content:
    content = content.replace(old_mega_item, new_mega_item, 1)
    print("3. Added E-Posta Şablonları & Otomasyon to Desktop Mega Menu under Yönetim & Ayarlar.")

# 4. Add to GlobalFooterComponent links
old_footer_link = """<button onClick={() => onNavigate('settings-appearance')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Görünüm Ayarları</button>"""
new_footer_link = old_footer_link + """\n              <span>•</span>\n              <button onClick={() => onNavigate('email-templates')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">E-Posta Şablonları</button>"""

if old_footer_link in content:
    content = content.replace(old_footer_link, new_footer_link, 1)
    print("4. Added E-Posta Şablonları to Global Footer links.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
