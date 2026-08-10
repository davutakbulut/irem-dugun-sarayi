import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

demo_block = """              {/* QUICK DEMO ROLE BUTTONS FOR MANAGERS */}
              <div className="pt-2 border-t border-slate-100 dark:border-slate-800 space-y-2">
                <span className="text-[10px] text-slate-400 font-bold block text-center uppercase tracking-wider">Hızlı Rol Girişleri:</span>
                <div className="grid grid-cols-2 gap-2 text-[11px] font-bold">
                  <button
                    type="button"
                    onClick={() => handleQuickRoleLogin('admin', 'Sümeyra Yılmaz (Yönetici)', 'sumeyra@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=200&q=80')}
                    className="p-2 rounded-xl bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-amber-800 dark:text-amber-300 hover:bg-amber-100 transition cursor-pointer text-center"
                  >
                    👑 Yönetici (Admin)
                  </button>
                  <button
                    type="button"
                    onClick={() => handleQuickRoleLogin('satis', 'Ahmet Can (Satış Müdürü)', 'ahmet@iremdugunsarayi.com', 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80')}
                    className="p-2 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 transition cursor-pointer text-center"
                  >
                    💼 Satış Müdürü
                  </button>
                </div>
              </div>"""

if demo_block in content:
    content = content.replace(demo_block, "")
    print("1. Successfully removed QUICK DEMO ROLE BUTTONS from LoginComponent!")
else:
    print("WARNING: Could not find demo_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
