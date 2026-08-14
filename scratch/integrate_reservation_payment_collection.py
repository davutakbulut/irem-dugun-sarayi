import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update FinanceComponent signature and props in App
    content = content.replace(
        "function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses, onUpdateReservation }) {",
        "function FinanceComponent({ financialStats, reservations = [], setReservations, venues = [], services = [], expenses = [], setExpenses, onUpdateReservation, showToast }) {"
    )

    content = content.replace(
        """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      venues={venues}
                      services={services}
                      expenses={expenses}
                      setExpenses={setExpenses}
                      onUpdateReservation={handleUpdateReservation}
                    />
                  )}""",
        """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      setReservations={setReservations}
                      venues={venues}
                      services={services}
                      expenses={expenses}
                      setExpenses={setExpenses}
                      showToast={showToast}
                      onUpdateReservation={handleUpdateReservation}
                    />
                  )}"""
    )

    # 2. Add state inside FinanceComponent
    old_state_block = """      // General Cashflow Transaction Modal State (Income vs Expense)
      const [transType, setTransType] = useState('gider'); // 'gelir' | 'gider'
      const [newTitle, setNewTitle] = useState('');
      const [newCategory, setNewCategory] = useState('Faturalar & Enerji');
      const [newAmount, setNewAmount] = useState('');
      const [newDate, setNewDate] = useState(new Date().toISOString().split('T')[0]);
      const [newStatus, setNewStatus] = useState('Tamamlandı');"""

    new_state_block = """      // General Cashflow Transaction Modal State (Income vs Expense)
      const [transType, setTransType] = useState('gider'); // 'gelir' | 'gider'
      const [incomeSource, setIncomeSource] = useState('reservation'); // 'reservation' | 'external'
      const [selectedResId, setSelectedResId] = useState('');
      const [paymentMethod, setPaymentMethod] = useState('Nakit Kasa');
      const [paymentType, setPaymentType] = useState('Kısmi Ara Ödeme');
      const [newTitle, setNewTitle] = useState('');
      const [newCategory, setNewCategory] = useState('Faturalar & Enerji');
      const [newAmount, setNewAmount] = useState('');
      const [newDate, setNewDate] = useState(new Date().toISOString().split('T')[0]);
      const [newStatus, setNewStatus] = useState('Tamamlandı');"""

    if old_state_block in content:
        content = content.replace(old_state_block, new_state_block)

    # 3. Update handleAddGeneralTransaction to support direct reservation payment collection
    old_handler_block = """      // Handle Add General Cash Transaction (Income or Expense)
      const handleAddGeneralTransaction = async (e) => {
        e.preventDefault();
        if (!newTitle.trim() || !newAmount) return;

        const newTrans = {
          id: `trans-${Date.now()}`,
          title: newTitle.trim(),
          category: newCategory,
          type: transType, // 'gelir' or 'gider'
          amount: Number(newAmount),
          createdAt: new Date().toISOString(),
          recordTimestamp: Date.now(),
          date: newDate || new Date().toISOString().split('T')[0],
          description: `Kasa Hareketi (${transType === 'gelir' ? 'Harici Gelir' : 'Harici Gider'})`,
          status: newStatus
        };

        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTrans)
          });
          const data = await resp.json();
          if (data.success && data.item) {
            setExpenses(prev => [data.item, ...prev.filter(x => x.id !== data.item.id)]);
          } else {
            setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
          }
        } catch(err) {
          console.error('Add expense error:', err);
          setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
        }

        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };"""

    new_handler_block = """      // Handle Add General Cash Transaction (Income or Expense)
      const handleAddGeneralTransaction = async (e) => {
        e.preventDefault();
        if (!newAmount || Number(newAmount) <= 0) return;

        // A) REZERVASYON TAHSİLATI ALMA & KALAN BAKİYEDEN DÜŞME
        if (transType === 'gelir' && incomeSource === 'reservation') {
          if (!selectedResId) {
            alert('Lütfen tahsilat yapılacak rezervasyonu seçiniz.');
            return;
          }
          const curRes = (reservations || []).find(r => r.id === selectedResId);
          if (!curRes) return;

          try {
            const fetchFn = window.fetchWithRetry || fetch;
            const resp = await fetchFn(`/api/reservations/${selectedResId}/payments`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                amount: Number(newAmount),
                date: newDate || new Date().toISOString().split('T')[0],
                method: paymentMethod,
                type: paymentType,
                note: newTitle.trim() || `${curRes.customerName} - ${paymentType} (${paymentMethod})`,
                recordedBy: 'Sistem Yöneticisi'
              })
            });
            const data = await resp.json();
            if (data && data.success) {
              if (setReservations) {
                setReservations(prev => {
                  const updated = (prev || []).map(r => {
                    if (r.id === selectedResId) {
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
              if (showToast) {
                showToast(`${curRes.customerName} için ${formatCurrency(newAmount)} tahsilat alındı! Kalan Bakiye: ${formatCurrency(data.remainingBalance)}`);
              }
            }
          } catch(err) {
            console.error('Reservation payment error:', err);
          }

          setNewTitle('');
          setNewAmount('');
          setSelectedResId('');
          setIsModalOpen(false);
          return;
        }

        // B) HARİCİ GELİR VEYA HARİCİ GİDER İŞLEMİ
        if (!newTitle.trim()) return;

        const newTrans = {
          id: `trans-${Date.now()}`,
          title: newTitle.trim(),
          category: newCategory,
          type: transType, // 'gelir' or 'gider'
          amount: Number(newAmount),
          createdAt: new Date().toISOString(),
          recordTimestamp: Date.now(),
          date: newDate || new Date().toISOString().split('T')[0],
          description: `Kasa Hareketi (${transType === 'gelir' ? 'Harici Gelir' : 'Harici Gider'})`,
          status: newStatus
        };

        try {
          const fetchFn = window.fetchWithRetry || fetch;
          const resp = await fetchFn('/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newTrans)
          });
          const data = await resp.json();
          if (data.success && data.item) {
            setExpenses(prev => [data.item, ...prev.filter(x => x.id !== data.item.id)]);
          } else {
            setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
          }
          if (showToast) {
            showToast(`${newTrans.title} kasa hareketi kaydedildi.`);
          }
        } catch(err) {
          console.error('Add expense error:', err);
          setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
        }

        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };"""

    if old_handler_block in content:
        content = content.replace(old_handler_block, new_handler_block)

    # 4. Replace the Modal UI in FinanceComponent
    old_modal_ui = """                {/* TYPE SWITCHER: GELİR (+) vs GİDER (-) */}
                <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
                  <button
                    type="button"
                    onClick={() => setTransType('gelir')}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>+ Harici Gelir (+)</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => setTransType('gider')}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>- Harici Gider (-)</span>
                  </button>
                </div>

                <form onSubmit={handleAddGeneralTransaction} className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold block mb-1">Harcama / Gelir Açıklaması:</label>
                    <input
                      type="text"
                      value={newTitle}
                      onChange={e => setNewTitle(e.target.value)}
                      placeholder={transType === 'gelir' ? 'Örn: Dış Fotoğraf Çekim Alanı Kiralama' : 'Örn: Temmuz Ayı Elektrik Faturası Ödemesi'}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1">Kategori:</label>
                    <select
                      value={newCategory}
                      onChange={e => setNewCategory(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    >
                      {transType === 'gelir' ? (
                        <>
                          <option value="Dış Çekim & Plato">Dış Çekim & Plato Kiralama Geliri</option>
                          <option value="Kafeterya & Mutfak Satışı">Kafeterya & Mutfak Günlük Satış Geliri</option>
                          <option value="Ses & Işık Kiralama">Ses & Işık Ekipman Dış Kiralama</option>
                          <option value="Sponsorluk & Reklam">Sponsorluk & Reklam Geliri</option>
                          <option value="Ekipman & Hurda Satışı">Eski Ekipman / Hurda Satış Geliri</option>
                          <option value="Muhtelif Gelir">Diğer Muhtelif Kasa Geliri</option>
                        </>
                      ) : (
                        <>
                          <option value="Faturalar & Enerji">Faturalar & Enerji (Elektrik, Su, Doğalgaz, İnternet)</option>
                          <option value="Yemek & Mutfak & İkram">Yemek & Mutfak & İkram Alımları</option>
                          <option value="Keyfi & Temsil Ağırlama">Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)</option>
                          <option value="Personel & Yevmiye">Personel Maaş, Yevmiye & SGK</option>
                          <option value="Dekorasyon & Çiçek">Dekorasyon, Çiçek & Sahne Süsleme</option>
                          <option value="Ekipman & Bakım">Ekipman, Ses, Işık & Bakım Onarım</option>
                          <option value="Ofis & Kırtasiye & Sarf">Ofis, Kırtasiye & Sarf Malzeme</option>
                          <option value="Vergi & Muhasebe">Vergi, Harç & Muhasebe Ödemeleri</option>
                          <option value="Genel Harcama">Diğer Genel İşletme Giderleri</option>
                        </>
                      )}
                    </select>
                  </div>

                  <div className="grid grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1">Tutar (TL):</label>
                      <input
                        type="number"
                        value={newAmount}
                        onChange={e => setNewAmount(e.target.value)}
                        placeholder="0"
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1">İşlem Tarihi:</label>
                      <input
                        type="date"
                        value={newDate}
                        onChange={e => setNewDate(e.target.value)}
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                  </div>"""

    new_modal_ui = """                {/* TYPE SWITCHER: GELİR (+) vs GİDER (-) */}
                <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
                  <button
                    type="button"
                    onClick={() => {
                      setTransType('gelir');
                    }}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>+ Kasa Geliri / Tahsilat (+)</span>
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setTransType('gider');
                    }}
                    className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                      transType === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                    }`}
                  >
                    <span>- İşletme Gideri (-)</span>
                  </button>
                </div>

                {/* IF GELIR: SUB-TOGGLE FOR RESERVATION PAYMENT VS EXTERNAL INCOME */}
                {transType === 'gelir' && (
                  <div className="grid grid-cols-2 gap-2 p-1 bg-emerald-500/10 rounded-2xl border border-emerald-500/30">
                    <button
                      type="button"
                      onClick={() => setIncomeSource('reservation')}
                      className={`py-1.5 rounded-xl text-[11px] font-extrabold transition cursor-pointer flex items-center justify-center space-x-1 ${
                        incomeSource === 'reservation' ? 'bg-emerald-600 text-white shadow-sm' : 'text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20'
                      }`}
                    >
                      <ThemeIcon icon="calendar" className="w-3.5 h-3.5 inline mr-1" />
                      <span>Rezervasyon Tahsilatı (Bakiye Düş)</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => setIncomeSource('external')}
                      className={`py-1.5 rounded-xl text-[11px] font-extrabold transition cursor-pointer flex items-center justify-center space-x-1 ${
                        incomeSource === 'external' ? 'bg-emerald-600 text-white shadow-sm' : 'text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20'
                      }`}
                    >
                      <ThemeIcon icon="money" className="w-3.5 h-3.5 inline mr-1" />
                      <span>Harici Gelir (Plato vb.)</span>
                    </button>
                  </div>
                )}

                <form onSubmit={handleAddGeneralTransaction} className="space-y-3 text-xs">
                  {/* RESERVATION SELECTOR & REMAINING BALANCE CARD */}
                  {transType === 'gelir' && incomeSource === 'reservation' ? (
                    <>
                      <div>
                        <label className="font-bold block mb-1">Tahsilat Yapılacak Rezervasyon / Sözleşme:</label>
                        <select
                          value={selectedResId}
                          onChange={e => {
                            const rId = e.target.value;
                            setSelectedResId(rId);
                            const found = (reservations || []).find(r => r.id === rId);
                            if (found) {
                              setNewTitle(`${found.customerName} - ${paymentType}`);
                            }
                          }}
                          required
                          className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                        >
                          <option value="">-- Lütfen Sözleşme / Müşteri Seçiniz --</option>
                          {(reservations || []).map(r => (
                            <option key={r.id} value={r.id}>
                              {r.customerName} ({r.id}) - Düğün: {formatDate(r.date || r.eventDate)} | Kalan: {formatCurrency(r.remainingBalance !== undefined ? r.remainingBalance : (r.totalAmount - (r.depositPaid || 0)))}
                            </option>
                          ))}
                        </select>
                      </div>

                      {/* LIVE SELECTED RESERVATION BALANCE INFO CARD */}
                      {selectedResId && (() => {
                        const cur = (reservations || []).find(r => r.id === selectedResId);
                        if (!cur) return null;
                        const vObj = (venues || []).find(v => v.id === cur.venueId);
                        const curTotal = Number(cur.totalAmount || 0);
                        const curPaid = Number(cur.depositPaid || 0);
                        const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));
                        const afterRemaining = Math.max(0, curRemaining - Number(newAmount || 0));

                        return (
                          <div className="p-3.5 bg-emerald-500/10 rounded-2xl border border-emerald-500/30 space-y-2">
                            <div className="flex justify-between items-center text-[11px]">
                              <span className="font-bold text-slate-700 dark:text-gray-200">{cur.customerName} ({vObj?.name || cur.venueName})</span>
                              <span className="px-2 py-0.5 rounded-lg text-[10px] font-extrabold bg-emerald-600 text-white">{cur.paymentStatus || 'Aktif'}</span>
                            </div>
                            <div className="grid grid-cols-3 gap-2 text-center text-[10px]">
                              <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                                <span className="text-slate-400 block">Sözleşme:</span>
                                <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(curTotal)}</span>
                              </div>
                              <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                                <span className="text-slate-400 block">Ödenen:</span>
                                <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(curPaid)}</span>
                              </div>
                              <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                                <span className="text-slate-400 block">Kalan Bakiye:</span>
                                <span className="font-mono font-extrabold text-red-500">{formatCurrency(curRemaining)}</span>
                              </div>
                            </div>
                            {curRemaining > 0 && (
                              <div className="flex justify-between items-center pt-1 border-t border-emerald-500/20 text-[11px]">
                                <button
                                  type="button"
                                  onClick={() => setNewAmount(String(curRemaining))}
                                  className="text-emerald-700 dark:text-gold-400 font-bold hover:underline cursor-pointer text-[10px]"
                                >
                                  ⚡ Tüm Kalan Bakiyeyi Doldur ({formatCurrency(curRemaining)})
                                </button>
                                {Number(newAmount) > 0 && (
                                  <span className="text-slate-600 dark:text-gray-300 text-[10px] font-bold">
                                    Yeni Kalan: <b className="font-mono text-red-500">{formatCurrency(afterRemaining)}</b>
                                  </span>
                                )}
                              </div>
                            )}
                          </div>
                        );
                      })()}

                      <div className="grid grid-cols-2 gap-2.5">
                        <div>
                          <label className="font-bold block mb-1">Tahsilat Türü:</label>
                          <select
                            value={paymentType}
                            onChange={e => {
                              setPaymentType(e.target.value);
                              const cur = (reservations || []).find(r => r.id === selectedResId);
                              if (cur) setNewTitle(`${cur.customerName} - ${e.target.value}`);
                            }}
                            className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                          >
                            <option value="Kısmi Ara Ödeme">Kısmi Ara Ödeme / Taksit</option>
                            <option value="Kapora Tahsilatı">Kapora Tahsilatı</option>
                            <option value="Kalan Bakiyenin Kapatılması">Kalan Bakiyenin Kapatılması</option>
                            <option value="Ekstra Hizmet Tahsilatı">Ekstra Hizmet Tahsilatı</option>
                          </select>
                        </div>
                        <div>
                          <label className="font-bold block mb-1">Ödeme Yöntemi:</label>
                          <select
                            value={paymentMethod}
                            onChange={e => setPaymentMethod(e.target.value)}
                            className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                          >
                            <option value="Nakit Kasa">Nakit Kasa</option>
                            <option value="Banka Havalesi & EFT">Banka Havalesi & EFT</option>
                            <option value="Kredi Kartı / POS">Kredi Kartı / POS</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="font-bold block mb-1">Makbuz / İşlem Notu:</label>
                        <input
                          type="text"
                          value={newTitle}
                          onChange={e => setNewTitle(e.target.value)}
                          placeholder="Örn: 2. Taksit Nakit Tahsilatı Yapıldı"
                          className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                        />
                      </div>
                    </>
                  ) : (
                    <>
                      <div>
                        <label className="font-bold block mb-1">Harcama / Gelir Açıklaması:</label>
                        <input
                          type="text"
                          value={newTitle}
                          onChange={e => setNewTitle(e.target.value)}
                          placeholder={transType === 'gelir' ? 'Örn: Dış Fotoğraf Çekim Alanı Kiralama' : 'Örn: Temmuz Ayı Elektrik Faturası Ödemesi'}
                          required
                          className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                        />
                      </div>

                      <div>
                        <label className="font-bold block mb-1">Kategori:</label>
                        <select
                          value={newCategory}
                          onChange={e => setNewCategory(e.target.value)}
                          className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                        >
                          {transType === 'gelir' ? (
                            <>
                              <option value="Dış Çekim & Plato">Dış Çekim & Plato Kiralama Geliri</option>
                              <option value="Kafeterya & Mutfak Satışı">Kafeterya & Mutfak Günlük Satış Geliri</option>
                              <option value="Ses & Işık Kiralama">Ses & Işık Ekipman Dış Kiralama</option>
                              <option value="Sponsorluk & Reklam">Sponsorluk & Reklam Geliri</option>
                              <option value="Ekipman & Hurda Satışı">Eski Ekipman / Hurda Satış Geliri</option>
                              <option value="Muhtelif Gelir">Diğer Muhtelif Kasa Geliri</option>
                            </>
                          ) : (
                            <>
                              <option value="Faturalar & Enerji">Faturalar & Enerji (Elektrik, Su, Doğalgaz, İnternet)</option>
                              <option value="Yemek & Mutfak & İkram">Yemek & Mutfak & İkram Alımları</option>
                              <option value="Keyfi & Temsil Ağırlama">Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)</option>
                              <option value="Personel & Yevmiye">Personel Maaş, Yevmiye & SGK</option>
                              <option value="Dekorasyon & Çiçek">Dekorasyon, Çiçek & Sahne Süsleme</option>
                              <option value="Ekipman & Bakım">Ekipman, Ses, Işık & Bakım Onarım</option>
                              <option value="Ofis & Kırtasiye & Sarf">Ofis, Kırtasiye & Sarf Malzeme</option>
                              <option value="Vergi & Muhasebe">Vergi, Harç & Muhasebe Ödemeleri</option>
                              <option value="Genel Harcama">Diğer Genel İşletme Giderleri</option>
                            </>
                          )}
                        </select>
                      </div>
                    </>
                  )}

                  <div className="grid grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1">Tahsil Edilen / Ödenen Tutar (TL):</label>
                      <input
                        type="number"
                        value={newAmount}
                        onChange={e => setNewAmount(e.target.value)}
                        placeholder="0"
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label className="font-bold block mb-1">İşlem Tarihi:</label>
                      <input
                        type="date"
                        value={newDate}
                        onChange={e => setNewDate(e.target.value)}
                        required
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      />
                    </div>
                  </div>"""

    if old_modal_ui in content:
        content = content.replace(old_modal_ui, new_modal_ui)
        print(f"Replaced modal UI in {h_file}")
    else:
        print(f"old_modal_ui not found in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("All HTML files updated with reservation payment collection in finance!")
