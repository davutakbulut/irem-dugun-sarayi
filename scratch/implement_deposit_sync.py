import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace deposit & payment status section rendering in index.html with synchronized handlers
old_deposit_section = """                  <div>
                    <label className="font-bold block mb-1">Kapora Ödendi Mi?</label>
                    <select value={hasDeposit ? 'yes' : 'no'} onChange={e => setHasDeposit(e.target.value === 'yes')} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold">
                      <option value="yes">Evet, Kapora Alındı</option>
                      <option value="no">Hayır, Henüz Ödenmedi</option>
                    </select>
                  </div>

                  {hasDeposit && (
                    <div>
                      <label className="font-bold block mb-1">Ödenen Kapora Tutarı (TL):</label>
                      <div>
                        <input
                          type="number"
                          id="deposit-paid-input"
                          placeholder="Örn: 5000"
                          value={depositPaid}
                          onChange={e => setDepositPaid(e.target.value)}
                          className={`w-full border rounded-xl p-2.5 font-bold text-emerald-600 ${
                            depositPaid !== '' && Number(depositPaid) < 0
                              ? 'border-2 border-red-500 bg-red-500/10'
                              : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'
                          }`}
                        />
                        {depositPaid !== '' && Number(depositPaid) < 0 && (
                          <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span><ThemeIcon icon="warning" className="w-4 h-4 inline-block text-amber-500 shrink-0" /> 0'dan büyük giriniz</span>
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <div className="text-xs">
                  <label className="font-bold block mb-1">Genel Ödeme Statüsü (Anlık Bakiye Hesabı):</label>
                  <select
                    value={paymentStatus}
                    onChange={e => {
                      const val = e.target.value;
                      setPaymentStatus(val);
                      if (val === 'Kapora Alındı' && !hasDeposit) {
                        setHasDeposit(true);
                        if (!depositPaid || depositPaid === 0) setDepositPaid(5000);
                      }
                    }}
                    className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold"
                  >
                    <option value="Bekliyor">Bekliyor (Ödeme Bekleniyor)</option>
                    <option value="Kapora Alındı">Kapora Alındı (Kısmi Kapora Tahsil Edildi)</option>
                    <option value="Ödendi">Ödendi (Tam ödeme yapıldı - Net Bakiye ₺0)</option>
                    <option value="Tamamlandı">Tamamlandı (Tam ödeme yapıldı - Net Bakiye ₺0)</option>
                  </select>
                </div>"""

new_deposit_section = """                  <div>
                    <label className="font-bold block mb-1">Kapora Ödendi Mi?</label>
                    <select
                      value={hasDeposit ? 'yes' : 'no'}
                      onChange={e => {
                        const isYes = e.target.value === 'yes';
                        setHasDeposit(isYes);
                        if (isYes) {
                          if (paymentStatus === 'Bekliyor') setPaymentStatus('Kapora Alındı');
                          if (!depositPaid || depositPaid === '' || Number(depositPaid) === 0) setDepositPaid(5000);
                        } else {
                          if (paymentStatus === 'Kapora Alındı') setPaymentStatus('Bekliyor');
                          setDepositPaid('');
                        }
                      }}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                    >
                      <option value="yes">Evet, Kapora Alındı</option>
                      <option value="no">Hayır, Henüz Ödenmedi</option>
                    </select>
                  </div>

                  {hasDeposit && (
                    <div>
                      <label className="font-bold block mb-1">Ödenen Kapora Tutarı (TL):</label>
                      <div>
                        <input
                          type="number"
                          id="deposit-paid-input"
                          placeholder="Örn: 5000"
                          value={depositPaid}
                          onChange={e => {
                            const rawVal = e.target.value;
                            setDepositPaid(rawVal);
                            const numVal = Number(rawVal);
                            if (rawVal !== '' && numVal > 0) {
                              setHasDeposit(true);
                              if (paymentStatus === 'Bekliyor') setPaymentStatus('Kapora Alındı');
                            } else if (rawVal === '' || numVal === 0) {
                              if (paymentStatus === 'Kapora Alındı') {
                                setHasDeposit(false);
                                setPaymentStatus('Bekliyor');
                              }
                            }
                          }}
                          className={`w-full border rounded-xl p-2.5 font-bold text-emerald-600 ${
                            depositPaid !== '' && Number(depositPaid) < 0
                              ? 'border-2 border-red-500 bg-red-500/10'
                              : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'
                          }`}
                        />
                        {depositPaid !== '' && Number(depositPaid) < 0 && (
                          <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span><ThemeIcon icon="warning" className="w-4 h-4 inline-block text-amber-500 shrink-0" /> 0'dan büyük giriniz</span>
                          </p>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <div className="text-xs">
                  <label className="font-bold block mb-1">Genel Ödeme Statüsü (Anlık Bakiye Hesabı):</label>
                  <select
                    value={paymentStatus}
                    onChange={e => {
                      const val = e.target.value;
                      setPaymentStatus(val);
                      if (val === 'Kapora Alındı') {
                        setHasDeposit(true);
                        if (!depositPaid || depositPaid === '' || Number(depositPaid) === 0) setDepositPaid(5000);
                      } else if (val === 'Ödendi' || val === 'Tamamlandı') {
                        setHasDeposit(true);
                        setDepositPaid(calculations?.grandTotal || 0);
                      } else if (val === 'Bekliyor') {
                        setHasDeposit(false);
                        setDepositPaid('');
                      }
                    }}
                    className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold"
                  >
                    <option value="Bekliyor">Bekliyor (Ödeme Bekleniyor)</option>
                    <option value="Kapora Alındı">Kapora Alındı (Kısmi Kapora Tahsil Edildi)</option>
                    <option value="Ödendi">Ödendi (Tam ödeme yapıldı - Net Bakiye ₺0)</option>
                    <option value="Tamamlandı">Tamamlandı (Tam ödeme yapıldı - Net Bakiye ₺0)</option>
                  </select>
                </div>"""

if old_deposit_section in content:
    content = content.replace(old_deposit_section, new_deposit_section)
    print("1. Successfully updated Section 3 deposit fields with 100% synchronized handlers!")
else:
    print("WARNING: Could not find old_deposit_section exact match in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
