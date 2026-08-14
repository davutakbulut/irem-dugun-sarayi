import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. State addition
    old_state_def = """      // Selected Reservation for Custom Expense Modal
      const [customExpenseModalRes, setCustomExpenseModalRes] = useState(null);
      const [newResExpTitle, setNewResExpTitle] = useState('');
      const [newResExpAmount, setNewResExpAmount] = useState('');
      const [newResExpCategory, setNewResExpCategory] = useState('Personel & Yevmiye');"""

    new_state_def = """      // Selected Reservation for Custom Expense / Income Modal
      const [customExpenseModalRes, setCustomExpenseModalRes] = useState(null);
      const [resModalTab, setResModalTab] = useState('gider'); // 'gider' | 'gelir'
      const [newResExpTitle, setNewResExpTitle] = useState('');
      const [newResExpAmount, setNewResExpAmount] = useState('');
      const [newResExpCategory, setNewResExpCategory] = useState('Personel & Yevmiye');
      const [newResPayMethod, setNewResPayMethod] = useState('Nakit Kasa');
      const [newResPayType, setNewResPayType] = useState('Kısmi Ara Ödeme');
      const [newResPayDate, setNewResPayDate] = useState(new Date().toISOString().split('T')[0]);"""

    if old_state_def in content:
        content = content.replace(old_state_def, new_state_def)

    # 2. Add handlers for payment in reservation modal
    old_handlers_anchor = """      // Handle Delete Custom Expense From Reservation
      const handleDeleteCustomExpenseFromRes = async (expenseId) => {"""

    new_handlers_anchor = """      // Handle Add Payment to Reservation inside modal
      const handleAddPaymentToResInModal = async (e) => {
        e.preventDefault();
        if (!customExpenseModalRes || !newResExpAmount || Number(newResExpAmount) <= 0) return;
        const resId = customExpenseModalRes.id;
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${resId}/payments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              amount: Number(newResExpAmount),
              date: newResPayDate || new Date().toISOString().split('T')[0],
              method: newResPayMethod,
              type: newResPayType,
              note: newResExpTitle.trim() || `${customExpenseModalRes.customerName} - ${newResPayType}`,
              recordedBy: 'Sistem Yöneticisi'
            })
          });
          const data = await resp.json();
          if (data && data.success) {
            setCustomExpenseModalRes(prev => prev ? ({
              ...prev,
              payments: data.payments,
              depositPaid: data.depositPaid,
              remainingBalance: data.remainingBalance,
              paymentStatus: data.paymentStatus
            }) : null);

            if (typeof setReservations === 'function') {
              setReservations(prev => {
                const updated = (prev || []).map(r => {
                  if (r.id === resId) {
                    return {
                      ...r,
                      payments: data.payments,
                      depositPaid: data.depositPaid,
                      remainingBalance: data.remainingBalance,
                      paymentStatus: data.paymentStatus
                    };
                  }
                  return r;
                });
                CacheService.set('reservations', updated);
                return updated;
              });
            }
            if (typeof showToast === 'function') {
              showToast(`${formatCurrency(newResExpAmount)} tahsilat alındı! Kalan: ${formatCurrency(data.remainingBalance)}`);
            }
            setNewResExpAmount('');
            setNewResExpTitle('');
          }
        } catch(err) {
          console.error('Add payment error:', err);
        }
      };

      // Handle Delete Payment from Reservation inside modal
      const handleDeletePaymentFromRes = async (paymentId) => {
        if (!customExpenseModalRes) return;
        const resId = customExpenseModalRes.id;
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${resId}/payments/${paymentId}`, { method: 'DELETE' });
          const data = await resp.json();
          if (data && data.success) {
            setCustomExpenseModalRes(prev => prev ? ({
              ...prev,
              payments: data.payments,
              depositPaid: data.depositPaid,
              remainingBalance: data.remainingBalance,
              paymentStatus: data.paymentStatus
            }) : null);

            if (typeof setReservations === 'function') {
              setReservations(prev => {
                const updated = (prev || []).map(r => {
                  if (r.id === resId) {
                    return {
                      ...r,
                      payments: data.payments,
                      depositPaid: data.depositPaid,
                      remainingBalance: data.remainingBalance,
                      paymentStatus: data.paymentStatus
                    };
                  }
                  return r;
                });
                CacheService.set('reservations', updated);
                return updated;
              });
            }
            if (typeof showToast === 'function') {
              showToast('Tahsilat kaydı silindi ve bakiye güncellendi.');
            }
          }
        } catch(err) {
          console.error('Delete payment error:', err);
        }
      };

      // Handle Delete Custom Expense From Reservation
      const handleDeleteCustomExpenseFromRes = async (expenseId) => {"""

    if old_handlers_anchor in content and "handleAddPaymentToResInModal" not in content:
        content = content.replace(old_handlers_anchor, new_handlers_anchor)

    # 3. Update table row button label
    old_row_button = """                                       <button
                                         type="button"
                                         onClick={() => setCustomExpenseModalRes(r)}
                                         className="px-2 py-1 bg-amber-500/10 hover:bg-amber-500 text-amber-700 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-amber-500/30"
                                       >
                                         + Ek Gider
                                       </button>"""

    new_row_button = """                                       <button
                                         type="button"
                                         onClick={() => {
                                           setCustomExpenseModalRes(r);
                                           setResModalTab('gider');
                                         }}
                                         className="px-2.5 py-1 bg-amber-500/10 hover:bg-amber-500 text-amber-700 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-amber-500/30 flex items-center space-x-1"
                                         title="Bu rezervasyona gelir (tahsilat) veya gider ekle"
                                       >
                                         <span>+ Gelir / Gider</span>
                                       </button>"""

    if old_row_button in content:
        content = content.replace(old_row_button, new_row_button)

    old_expanded_header_button = """                                         <button
                                           type="button"
                                           onClick={() => setCustomExpenseModalRes(r)}
                                           className="px-3 py-1.5 gold-button font-bold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1"
                                         >
                                           <span>+ Bu Düğüne Ek Gider / Harcama Gir</span>
                                         </button>"""

    new_expanded_header_button = """                                         <button
                                           type="button"
                                           onClick={() => {
                                             setCustomExpenseModalRes(r);
                                             setResModalTab('gider');
                                           }}
                                           className="px-3 py-1.5 gold-button font-bold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1"
                                         >
                                           <span>+ Bu Düğüne Gelir / Gider Ekle</span>
                                         </button>"""

    if old_expanded_header_button in content:
        content = content.replace(old_expanded_header_button, new_expanded_header_button)

    # 4. Replace customExpenseModalRes Modal JSX with rich Gelir / Gider Tabs
    old_res_modal_jsx = """          {/* DEDICATED RESERVATION CUSTOM EXPENSE MANAGEMENT MODAL */}
          {customExpenseModalRes && typeof document !== 'undefined' && ReactDOM.createPortal(
            <div className="fixed inset-0 z-[999999] bg-slate-950/80 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <div>
                    <span className="text-[10px] font-mono font-extrabold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Rezervasyona Özel Harcama Yönetimi</span>
                    <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                      <ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" /> {customExpenseModalRes.id} - {customExpenseModalRes.customerName}
                    </h3>
                  </div>
                  <button onClick={() => setCustomExpenseModalRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center hover:bg-slate-200">✕</button>
                </div>

                {/* ADD NEW EXPENSE FORM */}
                <form onSubmit={handleAddCustomExpenseToRes} className="p-4 bg-amber-500/10 rounded-2xl border border-amber-500/30 space-y-3 text-xs">
                  <span className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                    <span><ThemeIcon icon="plus" className="w-4 h-4 inline-block shrink-0" /> Yeni Ek Gider Kalemi Ekle:</span>
                  </span>

                  <div className="space-y-2">
                    <input
                      type="text"
                      placeholder="Gider Açıklaması (Örn: Ekstra Orkestra, Garson Mesai, Sürpriz Volkan)"
                      value={newResExpTitle}
                      onChange={e => setNewResExpTitle(e.target.value)}
                      required
                      className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-medium"
                    />

                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <select
                          value={newResExpCategory}
                          onChange={e => setNewResExpCategory(e.target.value)}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-bold"
                        >
                          <option value="Personel & Yevmiye">Personel & Yevmiye</option>
                          <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                          <option value="Ses, Sahne & Sanatçı">Ses, Sahne & Sanatçı</option>
                          <option value="Mutfak & İkram">Mutfak & İkram</option>
                          <option value="Fotoğraf & Video Ekstra">Fotoğraf & Video Ekstra</option>
                          <option value="Diğer Özel Harcama">Diğer Özel Harcama</option>
                        </select>
                      </div>
                      <div>
                        <input
                          type="number"
                          placeholder="Tutar (TL)"
                          value={newResExpAmount}
                          onChange={e => setNewResExpAmount(e.target.value)}
                          required
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="w-full gold-button font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition"
                    >
                      + Bu Rezervasyona Gideri Ekle
                    </button>
                  </div>
                </form>

                {/* CURRENT CUSTOM EXPENSES LIST */}
                <div className="space-y-2">
                  <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                    Kayıtlı Özel Ek Giderler ({(customExpenseModalRes.customExpenses || []).length}):
                  </span>
                  {(!customExpenseModalRes.customExpenses || customExpenseModalRes.customExpenses.length === 0) ? (
                    <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                      Bu rezervasyona ait özel ek harcama girilmemiş.
                    </div>
                  ) : (
                    <div className="space-y-1.5 max-h-48 overflow-y-auto custom-scrollbar">
                      {customExpenseModalRes.customExpenses.map(exp => (
                        <div key={exp.id} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                          <div>
                            <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                            <div className="text-[10px] text-slate-400">{exp.category}</div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="font-mono font-bold text-red-500">{formatCurrency(exp.amount)}</span>
                            <button
                              type="button"
                              onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                              className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs"
                            >
                              ✕
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
                  <button
                    type="button"
                    onClick={() => setCustomExpenseModalRes(null)}
                    className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>,
            document.body
          )}"""

    new_res_modal_jsx = """          {/* DEDICATED RESERVATION CUSTOM EXPENSE & INCOME (PAYMENT) MANAGEMENT MODAL */}
          {customExpenseModalRes && typeof document !== 'undefined' && ReactDOM.createPortal(
            <div className="fixed inset-0 z-[999999] bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in" onClick={() => setCustomExpenseModalRes(null)}>
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[92vh] overflow-y-auto custom-scrollbar my-auto relative" onClick={e => e.stopPropagation()}>
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <div>
                    <span className="text-[10px] font-mono font-extrabold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Rezervasyon Özel Gelir & Gider Yönetimi</span>
                    <h3 className="text-base font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                      <ThemeIcon icon="document" className="w-4 h-4 inline-block text-amber-500 shrink-0" />
                      <span>{customExpenseModalRes.id} — {customExpenseModalRes.customerName}</span>
                    </h3>
                  </div>
                  <button onClick={() => setCustomExpenseModalRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center hover:bg-slate-200 cursor-pointer">✕</button>
                </div>

                {/* RESERVATION QUICK FINANCIAL SUMMARY BAR */}
                {(() => {
                  const cur = (reservations || []).find(r => r.id === customExpenseModalRes.id) || customExpenseModalRes;
                  const curTotal = Number(cur.totalAmount || 0);
                  const curPaid = Number(cur.depositPaid || (cur.payments || []).reduce((s, p) => s + Number(p.amount || 0), 0));
                  const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));

                  return (
                    <div className="p-3 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border grid grid-cols-3 gap-2 text-center text-[10px]">
                      <div>
                        <span className="text-slate-400 block font-medium">Sözleşme Tutarı:</span>
                        <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(curTotal)}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block font-medium">Ödenen (Tahsilat):</span>
                        <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(curPaid)}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block font-medium">Kalan Bakiye:</span>
                        <span className="font-mono font-extrabold text-red-500">{formatCurrency(curRemaining)}</span>
                      </div>
                    </div>
                  );
                })()}

                {/* MODAL ACTION TYPE TABS: GİDER (-) vs GELİR / TAHSİLAT (+) */}
                <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
                  <button
                    type="button"
                    onClick={() => {
                      setResModalTab('gider');
                      setNewResExpTitle('');
                      setNewResExpAmount('');
                    }}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      resModalTab === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>- Düğüne Ek Gider Ekle (-)</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setResModalTab('gelir');
                      setNewResExpTitle('');
                      setNewResExpAmount('');
                    }}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      resModalTab === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>+ Tahsilat / Gelir Al (+)</span>
                  </button>
                </div>

                {/* TAB 1: ADD EXPENSE TO RESERVATION */}
                {resModalTab === 'gider' && (
                  <div className="space-y-4">
                    <form onSubmit={handleAddCustomExpenseToRes} className="p-4 bg-red-500/10 rounded-2xl border border-red-500/30 space-y-3 text-xs">
                      <span className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                        <ThemeIcon icon="plus" className="w-4 h-4 inline-block text-red-500 shrink-0" />
                        <span>Bu Düğüne Özel Harcama / Maliyet Ekle:</span>
                      </span>

                      <div className="space-y-2">
                        <input
                          type="text"
                          placeholder="Gider Açıklaması (Örn: Ekstra Orkestra, Garson Mesai, Sürpriz Volkan)"
                          value={newResExpTitle}
                          onChange={e => setNewResExpTitle(e.target.value)}
                          required
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-medium"
                        />

                        <div className="grid grid-cols-2 gap-2">
                          <div>
                            <select
                              value={newResExpCategory}
                              onChange={e => setNewResExpCategory(e.target.value)}
                              className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-bold"
                            >
                              <option value="Personel & Yevmiye">Personel & Yevmiye</option>
                              <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                              <option value="Ses, Sahne & Sanatçı">Ses, Sahne & Sanatçı</option>
                              <option value="Mutfak & İkram">Mutfak & İkram</option>
                              <option value="Fotoğraf & Video Ekstra">Fotoğraf & Video Ekstra</option>
                              <option value="Diğer Özel Harcama">Diğer Özel Harcama</option>
                            </select>
                          </div>
                          <div>
                            <input
                              type="number"
                              placeholder="Tutar (TL)"
                              value={newResExpAmount}
                              onChange={e => setNewResExpAmount(e.target.value)}
                              required
                              className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                            />
                          </div>
                        </div>

                        <button
                          type="submit"
                          className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition cursor-pointer"
                        >
                          - Gideri Düğün Maliyetine Ekle
                        </button>
                      </div>
                    </form>

                    {/* CURRENT CUSTOM EXPENSES LIST */}
                    <div className="space-y-2">
                      <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                        Kayıtlı Özel Ek Giderler ({(customExpenseModalRes.customExpenses || []).length}):
                      </span>
                      {(!customExpenseModalRes.customExpenses || customExpenseModalRes.customExpenses.length === 0) ? (
                        <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                          Bu rezervasyona ait özel ek harcama girilmemiş.
                        </div>
                      ) : (
                        <div className="space-y-1.5 max-h-40 overflow-y-auto custom-scrollbar">
                          {customExpenseModalRes.customExpenses.map(exp => (
                            <div key={exp.id} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                              <div>
                                <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                                <div className="text-[10px] text-slate-400">{exp.category}</div>
                              </div>
                              <div className="flex items-center space-x-2">
                                <span className="font-mono font-bold text-red-500">{formatCurrency(exp.amount)}</span>
                                <button
                                  type="button"
                                  onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                                  className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs cursor-pointer"
                                  title="Gideri Sil"
                                >
                                  ✕
                                </button>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* TAB 2: ADD PAYMENT / INCOME (BAKİYE DÜŞ) */}
                {resModalTab === 'gelir' && (() => {
                  const cur = (reservations || []).find(r => r.id === customExpenseModalRes.id) || customExpenseModalRes;
                  const curTotal = Number(cur.totalAmount || 0);
                  const curPaid = Number(cur.depositPaid || (cur.payments || []).reduce((s, p) => s + Number(p.amount || 0), 0));
                  const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));
                  const afterRemaining = Math.max(0, curRemaining - Number(newResExpAmount || 0));

                  return (
                    <div className="space-y-4">
                      <form onSubmit={handleAddPaymentToResInModal} className="p-4 bg-emerald-500/10 rounded-2xl border border-emerald-500/30 space-y-3 text-xs">
                        <div className="flex justify-between items-center">
                          <span className="font-extrabold text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                            <ThemeIcon icon="money" className="w-4 h-4 inline-block text-emerald-500 shrink-0" />
                            <span>Tahsilat Al & Kalan Bakiyeden Düş:</span>
                          </span>
                          {curRemaining > 0 && (
                            <button
                              type="button"
                              onClick={() => setNewResExpAmount(String(curRemaining))}
                              className="text-emerald-700 dark:text-gold-400 font-bold hover:underline cursor-pointer text-[10px]"
                            >
                              ⚡ Tüm Bakiyeyi Doldur ({formatCurrency(curRemaining)})
                            </button>
                          )}
                        </div>

                        <div className="space-y-2">
                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label className="font-bold block mb-0.5 text-[11px]">Tahsilat Türü:</label>
                              <select
                                value={newResPayType}
                                onChange={e => setNewResPayType(e.target.value)}
                                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                              >
                                <option value="Kısmi Ara Ödeme">Kısmi Ara Ödeme / Taksit</option>
                                <option value="Kapora Tahsilatı">Kapora Tahsilatı</option>
                                <option value="Kalan Bakiyenin Kapatılması">Kalan Bakiyenin Kapatılması</option>
                                <option value="Ekstra Hizmet Tahsilatı">Ekstra Hizmet Tahsilatı</option>
                              </select>
                            </div>
                            <div>
                              <label className="font-bold block mb-0.5 text-[11px]">Ödeme Yöntemi:</label>
                              <select
                                value={newResPayMethod}
                                onChange={e => setNewResPayMethod(e.target.value)}
                                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                              >
                                <option value="Nakit Kasa">Nakit Kasa</option>
                                <option value="Banka Havalesi & EFT">Banka Havalesi & EFT</option>
                                <option value="Kredi Kartı / POS">Kredi Kartı / POS</option>
                              </select>
                            </div>
                          </div>

                          <div className="grid grid-cols-2 gap-2">
                            <div>
                              <label className="font-bold block mb-0.5 text-[11px]">Tahsil Edilen Tutar (TL):</label>
                              <input
                                type="number"
                                placeholder="0"
                                value={newResExpAmount}
                                onChange={e => setNewResExpAmount(e.target.value)}
                                required
                                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                              />
                            </div>
                            <div>
                              <label className="font-bold block mb-0.5 text-[11px]">Tahsilat Tarihi:</label>
                              <input
                                type="date"
                                value={newResPayDate}
                                onChange={e => setNewResPayDate(e.target.value)}
                                required
                                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                              />
                            </div>
                          </div>

                          <div>
                            <input
                              type="text"
                              placeholder="Makbuz / Not (Örn: Damat Bey Nakit Ödedi)"
                              value={newResExpTitle}
                              onChange={e => setNewResExpTitle(e.target.value)}
                              className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-medium"
                            />
                          </div>

                          {Number(newResExpAmount) > 0 && (
                            <div className="p-2 bg-emerald-500/20 rounded-xl text-center text-[11px] font-bold text-emerald-800 dark:text-emerald-300">
                              Tahsilat Sonrası Yeni Kalan Bakiye: <b className="font-mono text-red-500">{formatCurrency(afterRemaining)}</b>
                            </div>
                          )}

                          <button
                            type="submit"
                            className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition cursor-pointer"
                          >
                            + Tahsilatı Al & Bakiyeden Düş
                          </button>
                        </div>
                      </form>

                      {/* CURRENT PAYMENTS LIST FOR THIS RESERVATION */}
                      <div className="space-y-2">
                        <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                          Alınan Tahsilat Geçmişi ({(cur.payments || []).length}):
                        </span>
                        {(!cur.payments || cur.payments.length === 0) ? (
                          <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                            Bu sözleşmeye ait henüz tahsilat kaydı bulunmuyor.
                          </div>
                        ) : (
                          <div className="space-y-1.5 max-h-40 overflow-y-auto custom-scrollbar">
                            {cur.payments.map((p, idx) => (
                              <div key={p.id || idx} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                                <div>
                                  <div className="font-bold text-slate-800 dark:text-gray-200">{p.type || 'Tahsilat'} — {p.method || 'Kasa'}</div>
                                  <div className="text-[10px] text-slate-400">{p.note || ''} {p.date ? `• ${formatDate(p.date)}` : ''}</div>
                                </div>
                                <div className="flex items-center space-x-2">
                                  <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">+{formatCurrency(p.amount)}</span>
                                  {p.id && (
                                    <button
                                      type="button"
                                      onClick={() => handleDeletePaymentFromRes(p.id)}
                                      className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs cursor-pointer"
                                      title="Tahsilatı Sil"
                                    >
                                      ✕
                                    </button>
                                  )}
                                </div>
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })()}

                <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
                  <button
                    type="button"
                    onClick={() => setCustomExpenseModalRes(null)}
                    className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
                  >
                    Kapat
                  </button>
                </div>
              </div>
            </div>,
            document.body
          )}"""

    if old_res_modal_jsx in content:
        content = content.replace(old_res_modal_jsx, new_res_modal_jsx)
        print(f"Replaced reservation modal JSX in {h_file}")
    else:
        print(f"old_res_modal_jsx not matched in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All files updated successfully with row-specific Gelir & Gider modal!")
