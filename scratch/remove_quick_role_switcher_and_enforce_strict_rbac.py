import os, re

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove ROW 2: DEDICATED SUB-HEADER BAR (Hızlı Rol Değiştir bar)
    sub_header_start = "{/* ROW 2: DEDICATED SUB-HEADER BAR (ALWAYS PRESENT BETWEEN MAIN HEADER & NAVIGATION MENU) */}"
    sub_header_end = "</span>\n                    </button>\n                  </div>\n                </div>\n              )}"

    s_idx = content.find(sub_header_start)
    if s_idx != -1:
        e_idx = content.find(sub_header_end, s_idx)
        if e_idx != -1:
            content = content[:s_idx] + content[e_idx + len(sub_header_end):]
            print(f"Successfully removed Sub-Header bar from {f_path}!")

    # 2. Make activeRole read-only derived state from sessionUser in App
    old_active_role_state = "const [activeRole, setActiveRole] = useState(() => {"
    if old_active_role_state in content:
        # Replace activeRole state with derived value
        state_block_start = content.find(old_active_role_state)
        state_block_end = content.find("});", state_block_start)
        if state_block_start != -1 and state_block_end != -1:
            derived_active_role = "const activeRole = (sessionUser?.role || currentUserState?.role || 'admin');"
            content = content[:state_block_start] + derived_active_role + content[state_block_end + 3:]
            print(f"Successfully converted activeRole to derived state in {f_path}!")

    # 3. Clean up ProfileComponent role dropdown to be read-only badge
    old_profile_role_dropdown = """              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">
                  Sistem Rolü & Yetkileri: {isAdmin ? '(Admin Yetkisi)' : '(Salt Okunur)'}
                </label>
                {isAdmin ? (
                  <select
                    value={selectedRole}
                    onChange={e => setSelectedRole(e.target.value)}
                    className="w-full bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                  >
                    <option value="admin">Admin (Tam Yetkili)</option>
                    <option value="satisci">Satış Müdürü (Rezervasyon & Müşteri)</option>
                    <option value="sosyal_medyaci">Sosyal Medya (Fotoğraf & Galeri)</option>
                    <option value="musteri">Müşteri (Özelleştirilmiş Görünüm)</option>
                  </select>
                ) : (
                  <div className="p-2.5 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                    {ROLE_NAMES[activeRole]} — Roller sadece Sistem Yöneticisi (Admin) tarafından değiştirilebilir.
                  </div>
                )}
              </div>"""

    new_profile_role_badge = """              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">
                  Sistem Rolü & Yetkileri:
                </label>
                <div className="p-2.5 bg-amber-500/10 rounded-xl border border-amber-500/30 text-amber-800 dark:text-amber-300 font-bold flex items-center space-x-2">
                  <ThemeIcon icon="shield" className="w-4 h-4 text-amber-500 shrink-0" />
                  <span>{ROLE_NAMES[activeRole] || activeRole}</span>
                </div>
              </div>"""

    if old_profile_role_dropdown in content:
        content = content.replace(old_profile_role_dropdown, new_profile_role_badge)
        print(f"Successfully updated ProfileComponent role view in {f_path}!")

    # 4. Enforce Admin absolute access rule in all tab filter checks
    # Mega Menu Drawer filter:
    old_mega_filter = "const validItems = group.items.filter(item => (tabPermissionsState[item.id] || []).includes(activeRole));"
    new_mega_filter = "const validItems = group.items.filter(item => activeRole === 'admin' || (tabPermissionsState[item.id] || TAB_PERMISSIONS[item.id] || []).includes(activeRole));"

    if old_mega_filter in content:
        content = content.replace(old_mega_filter, new_mega_filter)

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Quick Role Switcher bar removal and strict Admin permission enforcement finished!")
