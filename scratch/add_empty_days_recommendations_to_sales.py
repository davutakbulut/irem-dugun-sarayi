import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_satisci_block = """          {activeRole === 'satisci' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Aktif Salon Sayısı</div>
                  <div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length} Salon</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Bu Ayın Boş Günleri</div>
                  <div className="text-2xl font-bold gold-gradient-text mt-1">12 Gün</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Kapora Alınan Rezervasyon</div>
                  <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{reservations.filter(r => r.depositPaid > 0).length} Adet</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-indigo-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Satış Dönüşüm Oranı</div>
                  <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">%84</div>
                </div>
              </div>"""

new_satisci_block = """          {activeRole === 'satisci' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Aktif Salon Sayısı</div>
                  <div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length} Salon</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Bu Ayın Boş Günleri</div>
                  <div className="text-2xl font-bold gold-gradient-text mt-1">12 Gün</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Kapora Alınan Rezervasyon</div>
                  <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{reservations.filter(r => r.depositPaid > 0).length} Adet</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-indigo-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Satış Dönüşüm Oranı</div>
                  <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">%84</div>
                </div>
              </div>

              {/* AI SMART RECOMMENDATION CARDS FOR SALES MANAGER */}
              <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 space-y-4">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                    <span>Yapay Zeka Boş Gün & Aksiyon Önerileri</span>
                  </h3>
                  <span className="text-[10px] bg-amber-500/10 text-amber-800 dark:text-gold-300 font-extrabold px-2.5 py-1 rounded-full border border-amber-500/20">
                    Satış Artırıcı Taktikler
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {aiRecs.map((rec, i) => (
                    <div key={i} className="p-4 rounded-2xl bg-white/60 dark:bg-brand-card/60 border border-slate-200 dark:border-brand-border space-y-3">
                      <div className="flex justify-between items-start">
                        <h4 className="font-bold text-xs text-amber-800 dark:text-gold-400 flex items-center space-x-1.5">
                          <span>{rec.title}</span>
                        </h4>
                        <span className="text-[9px] font-extrabold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-800 dark:text-gold-400">{rec.badge}</span>
                      </div>
                      <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed font-medium">{rec.description}</p>
                      <div className="pt-1 flex items-center space-x-2">
                        {rec.actionText && (
                          <button
                            onClick={() => onConvertToCampaign && onConvertToCampaign(rec)}
                            className="gold-button px-3.5 py-1.5 rounded-xl text-[11px] font-bold shadow hover:scale-105 transition cursor-pointer"
                          >
                            <ThemeIcon icon="gift" className="w-4 h-4 inline-block shrink-0" /> {rec.actionText}
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>"""

if old_satisci_block in content:
    content = content.replace(old_satisci_block, new_satisci_block)
    print("1. Added Empty Days AI Recommendation Cards for Sales Manager.")
else:
    print("WARNING: Could not find old_satisci_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
