import os

# 1. UPDATE server.js: Ensure express routes all /yonetim and /yonetim/* requests to yonetim.html
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

old_server_route = "app.get(['/yonetim', '/yonetim.html', '/giris', '/login'], (req, res) => {"
new_server_route = "app.get(['/yonetim', '/yonetim/*', '/yonetim.html', '/giris', '/login'], (req, res) => {"

if old_server_route in server_code:
    server_code = server_code.replace(old_server_route, new_server_route)
    with open('server.js', 'w', encoding='utf-8') as f:
        f.write(server_code)
    print("Updated server.js routing for /yonetim/* successfully!")

# 2. UPDATE HTML files: Add routing mappings and menu links
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. Add to PATH_TO_TAB
    old_path_to_tab_entry = "'ayarlar': 'settings',"
    new_path_to_tab_entry = """'ayarlar': 'settings',
      'company-settings': 'company-settings',
      'sirket-bilgileri': 'company-settings',
      'sozlesme-sablonu': 'company-settings',
      'ayarlar/sirket-bilgileri': 'company-settings',
      'yonetim/company-settings': 'company-settings',
      'yonetim/sirket-bilgileri': 'company-settings',
      'yonetim/sozlesme-sablonu': 'company-settings',"""

    if old_path_to_tab_entry in content and "'company-settings': 'company-settings'" not in content:
        content = content.replace(old_path_to_tab_entry, new_path_to_tab_entry)
        print(f"Added PATH_TO_TAB mappings in {h_file}")

    # B. Add to TAB_TO_PATH
    old_tab_to_path_entry = "'settings': '/yonetim/ayarlar',"
    new_tab_to_path_entry = """'company-settings': '/yonetim/sirket-bilgileri',
      'settings': '/yonetim/ayarlar',"""

    if old_tab_to_path_entry in content and "'company-settings': '/yonetim/sirket-bilgileri'" not in content:
        content = content.replace(old_tab_to_path_entry, new_tab_to_path_entry)
        print(f"Added TAB_TO_PATH mappings in {h_file}")

    # C. Add link into Sidebar sub-menu under Sistem Ayarları
    old_sidebar_sub = """                                  <a
                                    href="#/ayarlar/gorunum"
                                    onClick={(e) => { e.preventDefault(); navigateTo('settings-appearance'); }}"""

    new_sidebar_sub = """                                  <a
                                    href="/yonetim/sirket-bilgileri"
                                    onClick={(e) => { e.preventDefault(); navigateTo('company-settings'); }}
                                    className={`w-full flex items-center space-x-2 px-2.5 py-1.5 rounded-lg text-[11px] font-medium transition ${
                                      activeTab === 'company-settings' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 border border-amber-500/20' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800 dark:hover:text-gray-200'
                                    }`}
                                  >
                                    <ThemeIcon icon="document" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0 text-amber-500" />
                                    <span>Şirket Bilgileri & Sözleşme</span>
                                  </a>
                                  <a
                                    href="#/ayarlar/gorunum"
                                    onClick={(e) => { e.preventDefault(); navigateTo('settings-appearance'); }}"""

    if old_sidebar_sub in content and "navigateTo('company-settings')" not in content:
        content = content.replace(old_sidebar_sub, new_sidebar_sub)
        print(f"Added sidebar sub-menu item in {h_file}")

    # D. Add link into Settings Component Hub cards
    old_hub_item = "{ id: 'settings-appearance', label: 'Görünüm & Temalar'"
    new_hub_item = "{ id: 'company-settings', label: 'Şirket Bilgileri & Sözleşme', desc: 'Fatura başlığı, şirket iletişim verileri ve 3 sayfalık resmi sözleşme maddeleri', icon: 'document', fallbackEmoji: '' },\n            { id: 'settings-appearance', label: 'Görünüm & Temalar'"

    if old_hub_item in content and "id: 'company-settings', label: 'Şirket Bilgileri & Sözleşme'" not in content:
        content = content.replace(old_hub_item, new_hub_item)
        print(f"Added hub card in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All routing and menu items for Company Settings fixed successfully!")
