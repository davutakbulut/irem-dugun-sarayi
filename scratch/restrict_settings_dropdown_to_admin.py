import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Wrap Sistem Ayarları profile dropdown button with activeRole === 'admin' check
old_settings_btn = """                        <button
                          onClick={() => {
                            navigateTo('settings');
                            setIsProfileDropdownOpen(false);
                          }}
                          className="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-gray-200 hover:bg-amber-500/10 hover:text-amber-700 font-bold transition text-left"
                        >
                          <ThemeIcon icon="settings" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" /><span>Sistem Ayarları</span>
                        </button>"""

new_settings_btn = """                        {activeRole === 'admin' && (
                          <button
                            onClick={() => {
                              navigateTo('settings');
                              setIsProfileDropdownOpen(false);
                            }}
                            className="w-full flex items-center space-x-2.5 px-3 py-2 rounded-xl text-slate-700 dark:text-gray-200 hover:bg-amber-500/10 hover:text-amber-700 font-bold transition text-left"
                          >
                            <ThemeIcon icon="settings" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" /><span>Sistem Ayarları</span>
                          </button>
                        )}"""

if old_settings_btn in html:
    html = html.replace(old_settings_btn, new_settings_btn)
    print("Restricted Sistem Ayarları profile dropdown button to Admin role only!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html successfully!")
