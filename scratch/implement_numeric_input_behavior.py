import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Initial State Declarations for Numeric Inputs to default to empty string ''
old_states = """      const [venueId, setVenueId] = useState(venues[0]?.id || '');
      const [customVenuePrice, setCustomVenuePrice] = useState(venues[0]?.price || 0);"""

new_states = """      const [venueId, setVenueId] = useState(venues[0]?.id || '');
      const [customVenuePrice, setCustomVenuePrice] = useState(venues[0]?.price !== undefined ? venues[0].price : '');"""

if old_states in content:
    content = content.replace(old_states, new_states)
    print("1. Updated customVenuePrice initial state to allow empty string.")

old_guest_state = "      const [guestCount, setGuestCount] = useState(500);"
new_guest_state = "      const [guestCount, setGuestCount] = useState('');"

if old_guest_state in content:
    content = content.replace(old_guest_state, new_guest_state)
    print("2. Updated guestCount initial state to default to empty string '' instead of 500.")

old_fin_states = """      const [hasDeposit, setHasDeposit] = useState(false); // Default: Hayır
      const [depositPaid, setDepositPaid] = useState(0); // Default: 0 TL
      const [customDiscountAmount, setCustomDiscountAmount] = useState(0); // Default: 0 TL"""

new_fin_states = """      const [hasDeposit, setHasDeposit] = useState(false); // Default: Hayır
      const [depositPaid, setDepositPaid] = useState(''); // Default: Empty string
      const [customDiscountAmount, setCustomDiscountAmount] = useState(''); // Default: Empty string"""

if old_fin_states in content:
    content = content.replace(old_fin_states, new_fin_states)
    print("3. Updated depositPaid and customDiscountAmount initial states to empty string.")

# 2. Update customVenuePrice input rendering & validation warning
old_cvp_input = """                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Bu Rezervasyona Özel Mekan Kiralama Fiyatı (TL):</label>
                    <input
                      type="number"
                      value={customVenuePrice}
                      onChange={e => setCustomVenuePrice(Number(e.target.value))}
                      className="w-full bg-amber-500/10 border border-amber-500/40 rounded-xl p-2.5 text-amber-800 dark:text-gold-400 font-extrabold"
                    />"""

new_cvp_input = """                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Bu Rezervasyona Özel Mekan Kiralama Fiyatı (TL):</label>
                    <input
                      type="number"
                      placeholder="Örn: 100000"
                      value={customVenuePrice}
                      onChange={e => setCustomVenuePrice(e.target.value)}
                      className={`w-full border rounded-xl p-2.5 font-extrabold ${
                        customVenuePrice !== '' && Number(customVenuePrice) < 0
                          ? 'border-2 border-red-500 bg-red-500/10 text-red-600'
                          : 'bg-amber-500/10 border-amber-500/40 text-amber-800 dark:text-gold-400'
                      }`}
                    />
                    {customVenuePrice !== '' && Number(customVenuePrice) < 0 && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>⚠️ 0'dan büyük giriniz</span>
                      </p>
                    )}"""

if old_cvp_input in content:
    content = content.replace(old_cvp_input, new_cvp_input)
    print("4. Updated customVenuePrice input rendering with negative validation warning.")

# 3. Update guestCount input rendering & validation warning
old_gc_input = """                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Davetli Sayısı (Kişi):</label>
                    <input
                      type="number"
                      value={guestCount}
                      onChange={e => {
                        const val = Number(e.target.value);
                        setGuestCount(val);
                        setSelectedServices(prev => prev.map(item => {
                          const sObj = (services || []).find(x => x.id === item.serviceId);
                          return (sObj && sObj.pricingType === 'per_person') ? { ...item, quantity: val } : item;
                        }));
                      }}
                      className="w-full border rounded-xl p-2.5 font-bold bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border text-slate-800 dark:text-gray-200"
                    />"""

new_gc_input = """                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Davetli Sayısı (Kişi):</label>
                    <input
                      type="number"
                      placeholder="Örn: 500"
                      value={guestCount}
                      onChange={e => {
                        const rawVal = e.target.value;
                        setGuestCount(rawVal);
                        const numVal = rawVal === '' ? '' : Number(rawVal);
                        setSelectedServices(prev => prev.map(item => {
                          const sObj = (services || []).find(x => x.id === item.serviceId);
                          return (sObj && sObj.pricingType === 'per_person') ? { ...item, quantity: numVal } : item;
                        }));
                      }}
                      className={`w-full border rounded-xl p-2.5 font-bold ${
                        guestCount !== '' && Number(guestCount) < 0
                          ? 'border-2 border-red-500 bg-red-500/10 text-red-600'
                          : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border text-slate-800 dark:text-gray-200'
                      }`}
                    />
                    {guestCount !== '' && Number(guestCount) < 0 && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>⚠️ 0'dan büyük giriniz</span>
                      </p>
                    )}"""

if old_gc_input in content:
    content = content.replace(old_gc_input, new_gc_input)
    print("5. Updated guestCount input rendering with negative validation warning.")

# 4. Update customDiscountAmount & depositPaid inputs rendering & validation warnings
old_disc_input = """                        value={customDiscountAmount || ''}
                        onChange={e => setCustomDiscountAmount(Math.max(0, parseFloat(e.target.value) || 0))}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-red-500 font-mono text-sm pr-10"
                      />"""

new_disc_input = """                        value={customDiscountAmount}
                        onChange={e => setCustomDiscountAmount(e.target.value)}
                        className={`w-full border rounded-xl p-2.5 font-bold text-red-500 font-mono text-sm pr-10 ${
                          customDiscountAmount !== '' && Number(customDiscountAmount) < 0
                            ? 'border-2 border-red-500 bg-red-500/10'
                            : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'
                        }`}
                      />"""

if old_disc_input in content:
    content = content.replace(old_disc_input, new_disc_input)
    print("6. Updated customDiscountAmount input rendering.")

# Add validation warning text under customDiscountAmount wrapper
old_disc_wrapper = """                      <span className="absolute right-3 top-2.5 text-xs font-black text-amber-600 dark:text-gold-400">
                        {dipDiscountType === 'percent' ? '%' : '₺'}
                      </span>
                    </div>
                  </div>"""

new_disc_wrapper = """                      <span className="absolute right-3 top-2.5 text-xs font-black text-amber-600 dark:text-gold-400">
                        {dipDiscountType === 'percent' ? '%' : '₺'}
                      </span>
                    </div>
                    {customDiscountAmount !== '' && Number(customDiscountAmount) < 0 && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>⚠️ 0'dan büyük giriniz</span>
                      </p>
                    )}
                  </div>"""

if old_disc_wrapper in content:
    content = content.replace(old_disc_wrapper, new_disc_wrapper)
    print("7. Added negative validation warning for customDiscountAmount.")

# 5. Update depositPaid input rendering
old_dep_input = """<input type="number" min="0" id="deposit-paid-input" value={depositPaid} onChange={e => setDepositPaid(Math.max(0, parseFloat(e.target.value) || 0))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-emerald-600" />"""

new_dep_input = """<div>
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
                            <span>⚠️ 0'dan büyük giriniz</span>
                          </p>
                        )}
                      </div>"""

if old_dep_input in content:
    content = content.replace(old_dep_input, new_dep_input)
    print("8. Updated depositPaid input rendering with negative validation warning.")

# 6. Update Extra Service inputs (customUnitPrice & quantity)
old_service_cup = """                                <input
                                  type="number"
                                  value={found.customUnitPrice !== undefined ? found.customUnitPrice : s.price}
                                  onChange={e => {
                                    const val = Number(e.target.value);
                                    setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, customUnitPrice: val } : x));
                                  }}
                                  className="w-24 bg-amber-500/10 border border-amber-500/40 rounded-lg p-1 font-bold text-center text-amber-800 dark:text-gold-400"
                                />"""

new_service_cup = """                                <div className="flex flex-col">
                                  <input
                                    type="number"
                                    value={found.customUnitPrice !== undefined ? found.customUnitPrice : s.price}
                                    onChange={e => {
                                      const rawVal = e.target.value;
                                      setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, customUnitPrice: rawVal } : x));
                                    }}
                                    className={`w-24 border rounded-lg p-1 font-bold text-center ${
                                      found.customUnitPrice !== undefined && found.customUnitPrice !== '' && Number(found.customUnitPrice) < 0
                                        ? 'border-2 border-red-500 bg-red-500/10 text-red-600'
                                        : 'bg-amber-500/10 border-amber-500/40 text-amber-800 dark:text-gold-400'
                                    }`}
                                  />
                                  {found.customUnitPrice !== undefined && found.customUnitPrice !== '' && Number(found.customUnitPrice) < 0 && (
                                    <span className="text-[9px] font-bold text-red-500 mt-0.5">⚠️ 0'dan büyük giriniz</span>
                                  )}
                                </div>"""

if old_service_cup in content:
    content = content.replace(old_service_cup, new_service_cup)
    print("9. Updated extra service customUnitPrice input with negative validation warning.")

old_service_qty = """                                <input
                                  type="number"
                                  min="1"
                                  value={qty}
                                  onChange={e => {
                                    const val = Math.max(1, Number(e.target.value));
                                    setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, quantity: val } : x));
                                  }}
                                  className="w-20 bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-lg p-1 font-bold text-center"
                                />"""

new_service_qty = """                                <div className="flex flex-col">
                                  <input
                                    type="number"
                                    value={qty}
                                    onChange={e => {
                                      const rawVal = e.target.value;
                                      setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, quantity: rawVal } : x));
                                    }}
                                    className={`w-20 border rounded-lg p-1 font-bold text-center ${
                                      qty !== '' && Number(qty) < 0
                                        ? 'border-2 border-red-500 bg-red-500/10 text-red-600'
                                        : 'bg-white dark:bg-brand-card border-slate-200 dark:border-brand-border'
                                    }`}
                                  />
                                  {qty !== '' && Number(qty) < 0 && (
                                    <span className="text-[9px] font-bold text-red-500 mt-0.5">⚠️ 0'dan büyük giriniz</span>
                                  )}
                                </div>"""

if old_service_qty in content:
    content = content.replace(old_service_qty, new_service_qty)
    print("10. Updated extra service quantity input with negative validation warning.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
