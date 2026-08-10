import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add expandedResIds state inside FinanceComponent
old_fn = "    function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation }) {"

new_fn = """    function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation }) {
      const [expandedResIds, setExpandedResIds] = useState({});
      const toggleExpandRes = (resId) => {
        setExpandedResIds(prev => ({
          ...prev,
          [resId]: !prev[resId]
        }));
      };"""

if old_fn in content:
    content = content.replace(old_fn, new_fn)
    print("1. Added expandedResIds state to FinanceComponent.")

# 2. Add expandable detail panel row
old_end = """                                <td className="p-3.5 text-center whitespace-nowrap">
                                  <button
                                    type="button"
                                    onClick={() => setCustomExpenseModalRes(r)}
                                    className="px-2.5 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/40 transition inline-flex items-center space-x-1 cursor-pointer"
                                    title="Rezervasyona Özel Ek Gider Ekle veya Çıkar"
                                  >
                                    <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 text-amber-600 dark:text-gold-400 shrink-0" />
                                    <span>Ek Gider Ynet</span>
                                  </button>
                                </td>
                              </tr>
                            );
                          })"""

new_end = """                                <td className="p-3.5 text-center whitespace-nowrap" onClick={e => e.stopPropagation()}>
                                  <button
                                    type="button"
                                    onClick={() => setCustomExpenseModalRes(r)}
                                    className="px-2.5 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/40 transition inline-flex items-center space-x-1 cursor-pointer"
                                    title="Rezervasyona Özel Ek Gider Ekle veya Çıkar"
                                  >
                                    <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 text-amber-600 dark:text-gold-400 shrink-0" />
                                    <span>Ek Gider Yönet</span>
                                  </button>
                                </td>
                              </tr>

                              {/* 🔽 EXPANDABLE ITEMIZED EXPENSE & REMAINING BALANCE PANEL */}
                              {isExpanded && (
                                <tr className="bg-slate-50/90 dark:bg-brand-dark/90 border-b border-amber-500/30 animate-fade-in">
                                  <td colSpan="9" className="p-4">
                                    <div className="glass-panel p-4 rounded-2xl border border-amber-500/30 space-y-4 shadow-inner">
                                      {/* HEADER */}
                                      <div className="flex justify-between items-center border-b pb-2 border-slate-200 dark:border-brand-border/40">
                                        <div className="flex items-center space-x-2">
                                          <span className="text-amber-500 font-bold">📄</span>
                                          <span className="font-bold text-slate-800 dark:text-gray-100 text-xs">
                                            {r.id} — Kalem Kalem Gider & Finansal Döküm Detayı ({r.customerName})
                                          </span>
                                        </div>
                                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/30">
                                          {rf.venueName}
                                        </span>
                                      </div>

                                      {/* 3-COLUMN ITEMIZATION GRID */}
                                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                                        
                                        {/* COLUMN 1: VENUE COST */}
                                        <div className="bg-white dark:bg-brand-card p-3 rounded-xl border border-slate-200 dark:border-brand-border/40 space-y-2">
                                          <div className="font-bold text-blue-600 dark:text-blue-400 flex items-center space-x-1.5 border-b pb-1.5 border-slate-100 dark:border-brand-border/30">
                                            <span>🏰 Salon İşletim Maliyeti</span>
                                          </div>
                                          <div className="flex justify-between items-center pt-1 font-mono">
                                            <span className="text-slate-500">Mekan Tahsis Maliyeti:</span>
                                            <span className="font-bold text-blue-600 dark:text-blue-400">{formatCurrency(rf.venueCost)}</span>
                                          </div>
                                          <p className="text-[10px] text-slate-400 italic">Salon kiralama, enerji ve personel hazırlık maliyet bedeli.</p>
                                        </div>

                                        {/* COLUMN 2: SELECTED EXTRA SERVICES COSTS */}
                                        <div className="bg-white dark:bg-brand-card p-3 rounded-xl border border-slate-200 dark:border-brand-border/40 space-y-2">
                                          <div className="font-bold text-purple-600 dark:text-purple-400 flex items-center justify-between border-b pb-1.5 border-slate-100 dark:border-brand-border/30">
                                            <span>🛠️ Seçilen Ek Hizmetler ({(r.selectedServices || []).length})</span>
                                            <span className="font-mono text-xs font-extrabold">{formatCurrency(rf.servicesCost)}</span>
                                          </div>
                                          <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                            {(r.selectedServices || []).length === 0 ? (
                                              <div className="text-[11px] text-slate-400 italic py-1">Ek hizmet seçilmemiş.</div>
                                            ) : (
                                              (r.selectedServices || []).map((s, idx) => {
                                                const sObj = (services || []).find(srv => srv.id === s.serviceId);
                                                const uCost = s.costPrice !== undefined ? Number(s.costPrice) : (sObj?.costPrice !== undefined ? Number(sObj.costPrice) : Math.round(Number(s.unitPrice || 250) * 0.6));
                                                const itemTotalCost = uCost * Number(s.quantity || 1);
                                                return (
                                                  <div key={idx} className="flex justify-between items-center text-[11px] p-1.5 bg-slate-50 dark:bg-brand-dark/50 rounded-lg">
                                                    <div className="truncate pr-2">
                                                      <span className="font-bold text-slate-700 dark:text-gray-200">{s.serviceName || sObj?.name || s.serviceId}</span>
                                                      <span className="text-[9px] text-slate-400 block">{s.quantity || 1} adet x {formatCurrency(uCost)} maliyet</span>
                                                    </div>
                                                    <span className="font-mono font-bold text-purple-600 dark:text-purple-400 shrink-0">{formatCurrency(itemTotalCost)}</span>
                                                  </div>
                                                );
                                              })
                                            )}
                                          </div>
                                        </div>

                                        {/* COLUMN 3: CUSTOM EXPENSES / YEVMİYELER */}
                                        <div className="bg-white dark:bg-brand-card p-3 rounded-xl border border-slate-200 dark:border-brand-border/40 space-y-2">
                                          <div className="font-bold text-amber-700 dark:text-gold-400 flex items-center justify-between border-b pb-1.5 border-slate-100 dark:border-brand-border/30">
                                            <span>📝 Harcama & Yevmiyeler ({(rf.customExpensesList || []).length})</span>
                                            <span className="font-mono text-xs font-extrabold">{formatCurrency(rf.customExpensesTotal)}</span>
                                          </div>
                                          <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                            {(rf.customExpensesList || []).length === 0 ? (
                                              <div className="text-[11px] text-slate-400 italic py-1">Özel ek harcama girilmemiş.</div>
                                            ) : (
                                              (rf.customExpensesList || []).map((exp, idx) => (
                                                <div key={idx} className="flex justify-between items-center text-[11px] p-1.5 bg-slate-50 dark:bg-brand-dark/50 rounded-lg">
                                                  <div className="truncate pr-2">
                                                    <span className="font-bold text-slate-700 dark:text-gray-200">{exp.title}</span>
                                                    <span className="text-[9px] text-slate-400 block">{exp.category} ({exp.date || ''})</span>
                                                  </div>
                                                  <span className="font-mono font-bold text-amber-600 dark:text-gold-400 shrink-0">{formatCurrency(exp.amount || 0)}</span>
                                                </div>
                                              ))
                                            )}
                                          </div>
                                        </div>

                                      </div>

                                      {/* SUMMARY FOOTER BAR: KALAN BAKİYE & FİNANSAL TABLO */}
                                      <div className="p-3 bg-amber-500/10 rounded-xl border border-amber-500/30 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                                        <div className="flex flex-wrap items-center gap-4">
                                          <div>
                                            <span className="text-slate-500 text-[10px] font-bold block">Sözleşme Tutarı:</span>
                                            <span className="font-mono font-extrabold text-emerald-600 dark:text-emerald-400">{formatCurrency(rf.grossIncome)}</span>
                                          </div>
                                          <div>
                                            <span className="text-slate-500 text-[10px] font-bold block">Tahsil Edilen Kapora:</span>
                                            <span className="font-mono font-bold text-slate-700 dark:text-gray-200">{formatCurrency(r.depositPaid || 0)}</span>
                                          </div>
                                          <div className="p-1.5 bg-amber-500/20 rounded-lg border border-amber-500/40">
                                            <span className="text-amber-900 dark:text-gold-300 text-[10px] font-bold block">💰 Kalan Tahsil Edilecek Bakiye:</span>
                                            <span className="font-mono font-extrabold text-amber-700 dark:text-gold-400">{formatCurrency(remainingBalance)}</span>
                                          </div>
                                        </div>

                                        <div className="flex items-center space-x-4 border-t sm:border-t-0 sm:border-l pt-2 sm:pt-0 sm:pl-4 border-amber-500/30">
                                          <div>
                                            <span className="text-slate-500 text-[10px] font-bold block">Toplam Gider:</span>
                                            <span className="font-mono font-bold text-red-600 dark:text-red-400">{formatCurrency(rf.totalCost)}</span>
                                          </div>
                                          <div>
                                            <span className="text-slate-500 text-[10px] font-bold block">Net Kâr (Marj):</span>
                                            <span className={`font-mono font-extrabold ${rf.netProfit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                                              {rf.netProfit >= 0 ? '+' : ''}{formatCurrency(rf.netProfit)} (%{rf.profitMargin})
                                            </span>
                                          </div>
                                        </div>
                                      </div>

                                    </div>
                                  </td>
                                </tr>
                              )}
                            </React.Fragment>
                          );
                        })"""

if old_end in content:
    content = content.replace(old_end, new_end)
    print("2. Added expandable itemized panel to FinanceComponent table.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
