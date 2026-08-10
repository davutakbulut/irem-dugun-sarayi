import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_switcher_block = """                  {/* LEFT: ROLE SWITCHER BUTTONS */}
                  <div className="flex items-center space-x-2 overflow-x-auto custom-scrollbar">
                    <span className="text-[10px] uppercase font-extrabold text-slate-400 dark:text-gray-400 flex items-center space-x-1 shrink-0">
                      <ThemeIcon icon="shield" fallbackEmoji="" className="w-3.5 h-3.5 text-amber-500" />
                      <span>Hızlı Rol Değiştir:</span>
                    </span>
                    <div className="flex items-center space-x-1 shrink-0">
                      {Object.keys(rolesState).map(rId => {
                        const roleNameOnly = (rolesState[rId] || rId).replace(/[\\u{1F300}-\\u{1F9FF}]|[\\u{2600}-\\u{26FF}]|[\\u{2700}-\\u{27BF}]/gu, '').trim();
                        return (
                          <button
                            key={rId}
                            onClick={() => {
                              setActiveRole(rId);
                              showToast(`Rol Değiştirildi: ${roleNameOnly}`);
                            }}
                            className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition cursor-pointer ${
                              activeRole === rId
                                ? 'bg-amber-500 text-white shadow-xs'
                                : 'bg-white dark:bg-brand-card text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:bg-slate-100'
                            }`}
                          >
                            {roleNameOnly}
                          </button>
                        );
                      })}
                    </div>
                  </div>"""

new_switcher_block = """                  {/* LEFT: ROLE SWITCHER BUTTONS (RESTRICTED ONLY TO ADMIN ROLE) */}
                  {activeRole === 'admin' ? (
                    <div className="flex items-center space-x-2 overflow-x-auto custom-scrollbar">
                      <span className="text-[10px] uppercase font-extrabold text-slate-400 dark:text-gray-400 flex items-center space-x-1 shrink-0">
                        <ThemeIcon icon="shield" fallbackEmoji="" className="w-3.5 h-3.5 text-amber-500" />
                        <span>Hızlı Rol Değiştir:</span>
                      </span>
                      <div className="flex items-center space-x-1 shrink-0">
                        {Object.keys(rolesState).map(rId => {
                          const roleNameOnly = (rolesState[rId] || rId).replace(/[\\u{1F300}-\\u{1F9FF}]|[\\u{2600}-\\u{26FF}]|[\\u{2700}-\\u{27BF}]/gu, '').trim();
                          return (
                            <button
                              key={rId}
                              onClick={() => {
                                setActiveRole(rId);
                                showToast(`Rol Değiştirildi: ${roleNameOnly}`);
                              }}
                              className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition cursor-pointer ${
                                activeRole === rId
                                  ? 'bg-amber-500 text-white shadow-xs'
                                  : 'bg-white dark:bg-brand-card text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:bg-slate-100'
                              }`}
                            >
                              {roleNameOnly}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center space-x-2 text-[10px] font-bold text-slate-500 dark:text-gray-400">
                      <ThemeIcon icon="shield" fallbackEmoji="" className="w-3.5 h-3.5 text-amber-500" />
                      <span>Aktif Rol Yetkisi: <strong className="text-amber-600 dark:text-amber-400 uppercase font-black">{(rolesState[activeRole] || activeRole).replace(/[\\u{1F300}-\\u{1F9FF}]|[\\u{2600}-\\u{26FF}]|[\\u{2700}-\\u{27BF}]/gu, '').trim()}</strong></span>
                    </div>
                  )}"""

if old_switcher_block in content:
    content = content.replace(old_switcher_block, new_switcher_block)
    print("1. Successfully restricted 'Hızlı Rol Değiştir' bar to Admin role only!")
else:
    print("WARNING: Could not find old_switcher_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
