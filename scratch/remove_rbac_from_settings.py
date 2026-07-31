import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove settings-rbac item from Topbar Mega Menu (HorizontalNavbarComponent)
old_topbar_rbac_item = "            { id: 'settings-rbac', label: 'Rol & İzin Matrisi', desc: 'Sayfa bazlı rol erişim yetkilerini özelleştirme', icon: 'shield', fallbackEmoji: '🛡️', badge: 'RBAC' },\n"
if old_topbar_rbac_item in html:
    html = html.replace(old_topbar_rbac_item, '')
    print("Removed settings-rbac item from Topbar Mega Menu")

# 2. Remove settings-rbac button from Mobile Drawer menu
old_drawer_rbac_button = """                        <button
                          onClick={() => { navigateTo('settings-rbac'); setIsMobileMenuOpen(false); }}
                          className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left cursor-pointer ${
                            activeTab === 'settings-rbac' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                          }`}
                        >
                          <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0" />
                          <span>Rol & İzin Yönetimi</span>
                        </button>"""

if old_drawer_rbac_button in html:
    html = html.replace(old_drawer_rbac_button, '')
    print("Removed settings-rbac button from Mobile Drawer menu")

# 3. Remove 'rbac' subtab button from SettingsComponent top tab bar
old_settings_rbac_button = """            <button
              onClick={() => setSettingsTab('rbac')}
              className={`px-4 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 flex items-center space-x-2 ${
                settingsTab === 'rbac' ? 'gold-button shadow-md' : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
              }`}
            >
              <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0" />
              <span>Rol & İzin Matrisi (RBAC)</span>
            </button>"""

if old_settings_rbac_button in html:
    html = html.replace(old_settings_rbac_button, '')
    print("Removed rbac subtab button from SettingsComponent")

# 4. Remove rbac subtab section from inside SettingsComponent
# In SettingsComponent, remove settingsTab === 'rbac' section if present
rbac_section_pattern = r'\{\/\* TAB 3: RBAC PERMISSIONS MATRIX \*\/\}[\s\S]*?\{/\* TAB 4: ERROR'
if re.search(rbac_section_pattern, html):
    html = re.sub(rbac_section_pattern, '{/* TAB 4: ERROR', html)
    print("Removed inline RBAC section from inside SettingsComponent")

# 5. Add a direct quick link in SettingsComponent header to navigate to dedicated Roles page
old_settings_header_actions = """              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1 font-medium">
                Tema tercihlerini, Rol & İzin matrisini, önbellek ve hata simülasyonlarını tam ekranda yönetin.
              </p>
            </div>
          </div>"""

new_settings_header_actions = """              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1 font-medium">
                Tema tercihlerini, görünüm mimarisini, önbellek ve hata simülasyonlarını tam ekranda yönetin.
              </p>
            </div>

            <button
              type="button"
              onClick={() => onNavigate && onNavigate('roles')}
              className="px-4 py-2 bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 rounded-xl text-xs font-bold hover:bg-amber-500 hover:text-slate-900 transition flex items-center space-x-1.5 shrink-0"
            >
              <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-4 h-4 shrink-0" />
              <span>🛡️ Rol Yönetimi Sayfasına Git →</span>
            </button>
          </div>"""

if old_settings_header_actions in html:
    html = html.replace(old_settings_header_actions, new_settings_header_actions)
    print("Added quick link to Roles page in SettingsComponent header")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
