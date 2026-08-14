import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_start = """          {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ) */}
          {isModalOpen && (
            <div className="fixed inset-0 z-[999999] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl">"""

new_start = """          {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ - GLOBAL BODY PORTAL) */}
          {isModalOpen && typeof document !== 'undefined' && ReactDOM.createPortal(
            <div className="fixed inset-0 z-[999999] bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in" onClick={() => setIsModalOpen(false)}>
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl my-auto max-h-[92vh] overflow-y-auto custom-scrollbar relative" onClick={e => e.stopPropagation()}>"""

old_end = """                    <button
                      type="submit"
                      className={`font-bold px-5 py-2 rounded-xl text-white shadow cursor-pointer ${transType === 'gelir' ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-red-600 hover:bg-red-500'}`}
                    >
                      {transType === 'gelir' ? '+ Geliri Kaydet' : '- Gideri Kaydet'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}"""

new_end = """                    <button
                      type="submit"
                      className={`font-bold px-5 py-2 rounded-xl text-white shadow cursor-pointer ${transType === 'gelir' ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-red-600 hover:bg-red-500'}`}
                    >
                      {transType === 'gelir' ? '+ Geliri Kaydet' : '- Gideri Kaydet'}
                    </button>
                  </div>
                </form>
              </div>
            </div>,
            document.body
          )}"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_start in content:
        content = content.replace(old_start, new_start)
        print(f"Replaced start in {h_file}")
    else:
        print(f"old_start not found in {h_file}")

    if old_end in content:
        content = content.replace(old_end, new_end)
        print(f"Replaced end in {h_file}")
    else:
        print(f"old_end not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("General finance modal portaled directly to document.body across all files!")
