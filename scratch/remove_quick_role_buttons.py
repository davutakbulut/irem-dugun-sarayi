import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

quick_role_block = """                {/* QUICK ROLE DEMO LOGIN PRESET BUTTONS */}
                <div className="pt-4 border-t border-slate-200 dark:border-brand-border/60 space-y-2">
                  <div className="text-[11px] font-bold text-slate-500 dark:text-gray-400 flex items-center space-x-1">
                    <ThemeIcon icon="sparkles" className="w-3.5 h-3.5 text-amber-500 inline shrink-0" />
                    <span>Hızlı Canlı Rol Seçimi & Oturum Seçenekleri:</span>
                  </div>
                  <div className="grid grid-cols-2 gap-2 text-[11px] font-bold">
                    <button
                      type="button"
                      onClick={() => { setEmailInput('mustafa@iremdugunsarayi.com'); setPassword('Msytf2026'); handleQuickRoleLogin('admin', 'Mustafa Beyazyüz', 'mustafa@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-900 dark:text-gold-300 border border-amber-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-amber-500">👑</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Yönetici (Admin)</span>
                        <span className="text-[9px] opacity-75 block truncate">mustafa@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('satis@iremdugunsarayi.com'); setPassword('Satis2026'); handleQuickRoleLogin('satisci', 'Canan Güneş', 'satis@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-blue-500/10 hover:bg-blue-500/20 text-blue-900 dark:text-blue-300 border border-blue-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-blue-500">💼</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Satış Müdürü</span>
                        <span className="text-[9px] opacity-75 block truncate">satis@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('sosyal@iremdugunsarayi.com'); setPassword('Sosyal2026'); handleQuickRoleLogin('sosyal_medyaci', 'Murat Arslan', 'sosyal@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 text-purple-900 dark:text-purple-300 border border-purple-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-purple-500">📸</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Sosyal Medya</span>
                        <span className="text-[9px] opacity-75 block truncate">sosyal@...</span>
                      </div>
                    </button>

                    <button
                      type="button"
                      onClick={() => { setEmailInput('canan.ozturk@example.com'); setPassword('Musteri2026'); handleQuickRoleLogin('musteri', 'Canan & Serkan Öztürk', 'canan.ozturk@example.com', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'); }}
                      className="p-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-900 dark:text-emerald-300 border border-emerald-500/30 transition text-left flex items-center space-x-1.5"
                    >
                      <span className="text-emerald-500">👤</span>
                      <div className="truncate">
                        <span className="block font-extrabold truncate">Müşteri Portalı</span>
                        <span className="text-[9px] opacity-75 block truncate">canan.ozturk@...</span>
                      </div>
                    </button>
                  </div>
                </div>"""

if quick_role_block in content:
    content = content.replace(quick_role_block, "")
    print("1. Successfully removed Quick Role Login Preset Buttons block!")
else:
    print("WARNING: Could not find quick_role_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
