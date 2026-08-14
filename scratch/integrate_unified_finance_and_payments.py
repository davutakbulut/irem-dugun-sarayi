import os, re

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

# 1. New Upgraded ReservationDetailModal
new_detail_modal_code = """// --- RESERVATION DETAIL & MULTI-PAYMENT MODAL ---
    function ReservationDetailModal({ res, venues = [], services = [], onClose, onPrintInvoice, onUpdatePayment, onShowEmail, onEditReservation }) {
      if (!res) return null;
      const venue = (venues || []).find(v => v.id === res.venueId);
      const [payments, setPayments] = useState(Array.isArray(res.payments) ? res.payments : []);
      const [isAddingPayment, setIsAddingPayment] = useState(false);
      const [payAmount, setPayAmount] = useState('');
      const [payDate, setPayDate] = useState(new Date().toISOString().split('T')[0]);
      const [payMethod, setPayMethod] = useState('Banka Havalesi & EFT');
      const [payType, setPayType] = useState('Kısmi Ara Ödeme');
      const [payNote, setPayNote] = useState('');
      const [payReceipt, setPayReceipt] = useState('');
      const [isSubmitting, setIsSubmitting] = useState(false);

      const totalAmount = Number(res.totalAmount || 0);
      const totalPaid = payments.reduce((sum, p) => sum + Number(p.amount || 0), 0);
      const remainingBalance = Math.max(0, totalAmount - totalPaid);
      const paymentPercent = totalAmount > 0 ? Math.min(100, Math.round((totalPaid / totalAmount) * 100)) : 0;

      const handleAddPaymentSubmit = async (e) => {
        e.preventDefault();
        if (!payAmount || Number(payAmount) <= 0) return;
        setIsSubmitting(true);
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${res.id}/payments`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              amount: Number(payAmount),
              date: payDate,
              method: payMethod,
              type: payType,
              note: payNote,
              receiptNo: payReceipt,
              recordedBy: 'Yetkili Yönetici'
            })
          });
          const data = await resp.json();
          if (data.success && data.payments) {
            setPayments(data.payments);
            setPayAmount('');
            setPayNote('');
            setPayReceipt('');
            setIsAddingPayment(false);
            if (onUpdatePayment) {
              onUpdatePayment(res.id, data.depositPaid, data.paymentStatus, data.payments);
            }
          }
        } catch(err) {
          console.error('Payment submit error:', err);
        } finally {
          setIsSubmitting(false);
        }
      };

      const handleDeletePayment = async (paymentId) => {
        if (!confirm('Bu tahsilat kaydını silmek istediğinize emin misiniz?')) return;
        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn(`/api/reservations/${res.id}/payments/${paymentId}`, {
            method: 'DELETE'
          });
          const data = await resp.json();
          if (data.success && data.payments) {
            setPayments(data.payments);
            if (onUpdatePayment) {
              onUpdatePayment(res.id, data.depositPaid, data.paymentStatus, data.payments);
            }
          }
        } catch(err) {
          console.error('Payment delete error:', err);
        }
      };

      return (
        <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in" role="dialog" aria-modal="true" aria-labelledby="modal-title">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-2xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto custom-scrollbar my-auto shadow-2xl">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <div>
                <span className="font-mono text-amber-700 dark:text-gold-400 font-bold text-xs">{res.id}</span>
                <h3 id="modal-title" className="text-xl font-heading font-extrabold text-slate-900 dark:text-white">{res.customerName}</h3>
              </div>
              <button onClick={onClose} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center hover:bg-slate-200" aria-label="Modalı Kapat">✕</button>
            </div>

            {/* QUICK STATS 4-GRID */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 text-xs">
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-slate-500 text-[10px] font-bold">Salon</div>
                <div className="font-extrabold text-slate-800 dark:text-gray-200 truncate">{venue?.name || '-'}</div>
              </div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-slate-500 text-[10px] font-bold">Tarih & Saat</div>
                <div className="font-extrabold text-slate-800 dark:text-gray-200">{formatDate(res.date || res.eventDate)}</div>
              </div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-slate-500 text-[10px] font-bold">Sözleşme Tutarı</div>
                <div className="font-extrabold text-amber-700 dark:text-gold-400">{formatCurrency(totalAmount)}</div>
              </div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border">
                <div className="text-slate-500 text-[10px] font-bold">Kalan Bakiye</div>
                <div className="font-extrabold text-red-500 dark:text-red-400">{formatCurrency(remainingBalance)}</div>
              </div>
            </div>

            {/* LIVE PAYMENT PROGRESS BAR */}
            <div className="bg-amber-500/10 dark:bg-brand-dark p-3.5 rounded-2xl border border-amber-500/30 space-y-2">
              <div className="flex justify-between items-center text-xs font-bold">
                <span className="text-slate-700 dark:text-gray-300 flex items-center space-x-1.5">
                  <span>💳 Tahsilat Durumu:</span>
                  <span className={`px-2 py-0.5 rounded-full text-[10px] ${remainingBalance === 0 ? 'bg-emerald-500 text-white' : 'bg-amber-500 text-slate-950'}`}>
                    {remainingBalance === 0 ? 'Tamamı Ödendi' : totalPaid > 0 ? 'Kısmi Ödeme Alındı' : 'Ödeme Bekliyor'}
                  </span>
                </span>
                <span className="font-mono text-amber-700 dark:text-gold-400 font-extrabold">
                  {formatCurrency(totalPaid)} / {formatCurrency(totalAmount)} (%{paymentPercent})
                </span>
              </div>
              <div className="w-full h-2.5 bg-slate-200 dark:bg-brand-border/60 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-amber-500 to-emerald-500 transition-all duration-500" style={{ width: `${paymentPercent}%` }}></div>
              </div>
            </div>

            {/* PARÇALI TAHSİLAT HAREKETLERİ LİSTESİ & EKLEME */}
            <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
              <div className="flex justify-between items-center">
                <h4 className="font-extrabold text-xs text-slate-800 dark:text-gray-100 flex items-center space-x-1.5">
                  <ThemeIcon icon="money" className="w-4 h-4 text-emerald-500 shrink-0" />
                  <span>Tahsilat & Ödeme Hareketleri ({payments.length})</span>
                </h4>
                <button
                  type="button"
                  onClick={() => setIsAddingPayment(!isAddingPayment)}
                  className="px-3 py-1.5 gold-button font-bold text-[11px] rounded-xl shadow cursor-pointer flex items-center space-x-1"
                >
                  <span>{isAddingPayment ? '✕ Vazgeç' : '+ Yeni Tahsilat Ekle'}</span>
                </button>
              </div>

              {/* YENİ TAHSİLAT FORMU */}
              {isAddingPayment && (
                <form onSubmit={handleAddPaymentSubmit} className="p-3.5 bg-white dark:bg-brand-card rounded-2xl border border-amber-500/40 space-y-3 text-xs animate-fade-in">
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Tahsilat Tutarı (TL):</label>
                      <input
                        type="number"
                        placeholder="Örn: 25000"
                        value={payAmount}
                        onChange={e => setPayAmount(e.target.value)}
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Ödeme Tarihi:</label>
                      <input
                        type="date"
                        value={payDate}
                        onChange={e => setPayDate(e.target.value)}
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Ödeme Türü:</label>
                      <select
                        value={payType}
                        onChange={e => setPayType(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold text-slate-800 dark:text-gray-100"
                      >
                        <option value="İlk Kapora">İlk Kapora (Sözleşme İmzası)</option>
                        <option value="Kısmi Ara Ödeme">Kısmi Ara Ödeme (Taksit)</option>
                        <option value="Kalan Bakiye Kapatma">Kalan Bakiye Kapatma (Düğün Günü)</option>
                        <option value="Ekstra Hizmet Tahsilatı">Ekstra Hizmet Tahsilatı</option>
                      </select>
                    </div>
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Ödeme Yöntemi:</label>
                      <select
                        value={payMethod}
                        onChange={e => setPayMethod(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold text-slate-800 dark:text-gray-100"
                      >
                        <option value="Banka Havalesi & EFT">Banka Havalesi & EFT</option>
                        <option value="Nakit Elden">Nakit (Elden Kasa)</option>
                        <option value="Kredi Kartı / POS">Kredi Kartı / POS</option>
                      </select>
                    </div>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Dekont / Makbuz No (Opsiyonel):</label>
                      <input
                        type="text"
                        placeholder="Örn: DEK-2026-8849"
                        value={payReceipt}
                        onChange={e => setPayReceipt(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-100 font-medium"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1 text-slate-600 dark:text-gray-300">Açıklama / Not:</label>
                      <input
                        type="text"
                        placeholder="Örn: Damat bey bankadan havale yaptı"
                        value={payNote}
                        onChange={e => setPayNote(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-100 font-medium"
                      />
                    </div>
                  </div>
                  <div className="flex justify-end space-x-2 pt-1">
                    <button type="button" onClick={() => setIsAddingPayment(false)} className="px-3 py-1.5 bg-slate-100 dark:bg-brand-dark text-slate-600 rounded-xl font-bold">İptal</button>
                    <button type="submit" disabled={isSubmitting} className="gold-button font-bold px-4 py-1.5 rounded-xl shadow cursor-pointer">
                      {isSubmitting ? 'Kaydediliyor...' : '✓ Tahsilatı Kaydet'}
                    </button>
                  </div>
                </form>
              )}

              {/* PAYMENTS HISTORY TABLE */}
              <div className="space-y-1.5 max-h-48 overflow-y-auto custom-scrollbar">
                {payments.length === 0 ? (
                  <div className="text-center py-4 text-slate-400 font-medium text-xs bg-white dark:bg-brand-card rounded-xl border border-dashed border-slate-200 dark:border-brand-border">
                    Henüz kayıtlı bir tahsilat veya kapora bulunmuyor.
                  </div>
                ) : (
                  payments.map(p => (
                    <div key={p.id} className="p-2.5 bg-white dark:bg-brand-card rounded-xl border border-slate-200/80 dark:border-brand-border flex items-center justify-between text-xs hover:border-amber-400 transition">
                      <div className="flex items-center space-x-2.5">
                        <div className="w-8 h-8 rounded-lg bg-emerald-500/10 text-emerald-600 font-bold flex items-center justify-center text-sm">₺</div>
                        <div>
                          <div className="font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-1.5">
                            <span>{p.type || 'Tahsilat'}</span>
                            <span className="text-[10px] px-1.5 py-0.2 bg-slate-100 dark:bg-brand-dark rounded text-slate-500 font-medium">{p.method}</span>
                          </div>
                          <div className="text-[10px] text-slate-400">
                            {formatDate(p.date)} {p.receiptNo ? `• No: ${p.receiptNo}` : ''} {p.note ? `• "${p.note}"` : ''}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-3">
                        <span className="font-mono text-sm font-extrabold text-emerald-600 dark:text-emerald-400">+{formatCurrency(p.amount)}</span>
                        <button
                          type="button"
                          onClick={() => handleDeletePayment(p.id)}
                          className="w-6 h-6 rounded-md bg-red-500/10 hover:bg-red-500 text-red-500 hover:text-white flex items-center justify-center transition cursor-pointer text-xs"
                          title="Tahsilatı Sil"
                        >
                          ✕
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* FLOW PLAN PREVIEW */}
            {res.flowPlan && res.flowPlan.length > 0 && (
              <div className="bg-slate-50 dark:bg-brand-dark/70 p-3 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2 text-xs">
                <h4 className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" /> Etkinlik Akış Planlaması ({res.flowPlan.length} Adım):</h4>
                <div className="space-y-1 max-h-24 overflow-y-auto">
                  {res.flowPlan.map((fp, idx) => (
                    <div key={idx} className="flex justify-between items-center text-[11px] bg-white dark:bg-brand-card p-1.5 rounded border border-slate-200/60 dark:border-brand-border/40">
                      <span className="font-mono font-bold text-amber-700 dark:text-gold-300">{fp.time}</span>
                      <span className="text-slate-800 dark:text-gray-200 font-medium">{fp.title}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* BOTTOM ACTIONS */}
            <div className="flex justify-between items-center pt-2 border-t border-slate-200 dark:border-brand-border gap-2 flex-wrap">
              <div className="flex space-x-2">
                <button onClick={onPrintInvoice} className="bg-slate-800 hover:bg-slate-900 text-white font-bold px-3 py-2 rounded-xl text-xs inline-flex items-center space-x-1 shadow cursor-pointer">
                  <span><ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" /></span><span>Sözleşme Yazdır</span>
                </button>
                {onShowEmail && (
                  <button onClick={() => onShowEmail(res)} className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-3 py-2 rounded-xl text-xs inline-flex items-center space-x-1 shadow cursor-pointer">
                    <span><ThemeIcon icon="email" className="w-4 h-4 inline-block shrink-0" /></span><span>E-Posta Gönder</span>
                  </button>
                )}
                {onEditReservation && (
                  <button
                    onClick={() => {
                      onClose();
                      onEditReservation(res);
                    }}
                    className="bg-amber-600 hover:bg-amber-500 text-white font-bold px-3 py-2 rounded-xl text-xs inline-flex items-center space-x-1 shadow cursor-pointer"
                  >
                    <span><ThemeIcon icon="edit" className="w-4 h-4 inline-block shrink-0" /></span><span>Düzenle</span>
                  </button>
                )}
              </div>

              <div className="flex space-x-2">
                <button onClick={onClose} className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold cursor-pointer">Kapat</button>
              </div>
            </div>
          </div>
        </div>
      );
    }"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace ReservationDetailModal
    modal_pattern = re.compile(r'// --- RESERVATION DETAIL MODAL ---[\s\S]*?function ReservationDetailModal[\s\S]*?^    }', re.MULTILINE)
    if modal_pattern.search(content):
        content = modal_pattern.sub(new_detail_modal_code, content)
        print(f"Replaced ReservationDetailModal in {h_file}")
    else:
        print(f"ReservationDetailModal pattern not matched in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Detail modal successfully upgraded across all files!")
