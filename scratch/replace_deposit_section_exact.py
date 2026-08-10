import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hasDeposit select
old_has_dep = """                  <div>
                    <label className="font-bold block mb-1">Kapora Ödendi Mi?</label>
                    <select value={hasDeposit ? 'yes' : 'no'} onChange={e => setHasDeposit(e.target.value === 'yes')} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold">
                      <option value="yes">Evet, Kapora Alındı</option>
                      <option value="no">Hayır, Henüz Ödenmedi</option>
                    </select>
                  </div>"""

new_has_dep = """                  <div>
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
                  </div>"""

if old_has_dep in content:
    content = content.replace(old_has_dep, new_has_dep)
    print("1. Updated hasDeposit select.")

# Replace depositPaid input
old_dep_paid = """                          onChange={e => setDepositPaid(e.target.value)}"""
new_dep_paid = """                          onChange={e => {
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
                          }}"""

if old_dep_paid in content:
    content = content.replace(old_dep_paid, new_dep_paid)
    print("2. Updated depositPaid onChange handler.")

# Replace paymentStatus select
old_pay_stat = """                  <select
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
                  >"""

new_pay_stat = """                  <select
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
                  >"""

if old_pay_stat in content:
    content = content.replace(old_pay_stat, new_pay_stat)
    print("3. Updated paymentStatus select.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
