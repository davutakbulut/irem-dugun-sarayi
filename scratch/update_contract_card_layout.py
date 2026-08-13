import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_card_start = '{/* RESMİ SÖZLEŞME GÖRÜNTÜLE & İNDİR (YAZDIR) KARTI */}'
old_card_end = '{/* TAKVİM ÖN İZLEME KARTI */}'

new_card = """{/* RESMİ SÖZLEŞME GÖRÜNTÜLE & İNDİR (YAZDIR) KARTI */}
              <div className="glass-panel p-4 sm:p-5 rounded-3xl space-y-3.5 shadow-sm border border-amber-500/30 bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-transparent">
                {/* Top Row: Icon + Title & Description */}
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-xl bg-slate-100/80 dark:bg-brand-dark/80 text-slate-800 dark:text-gray-200 flex items-center justify-center font-bold text-lg shrink-0 border border-slate-200 dark:border-brand-border">
                    <ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0 text-slate-800 dark:text-gray-200" />
                  </div>
                  <div className="flex-1">
                    <h4 className="font-extrabold text-xs sm:text-sm text-slate-900 dark:text-white flex items-center space-x-1.5">
                      <span>Resmi Etkinlik Sözleşmesi</span>
                      {isEditMode && <span className="text-[10px] bg-amber-500/20 text-amber-800 dark:text-gold-400 font-mono px-1.5 py-0.5 rounded">ID: {editingResFromUrl?.id}</span>}
                    </h4>
                    <p className="text-[11px] text-slate-500 dark:text-gray-400 leading-snug mt-0.5">Canlı girilen fiyatlarla A4 formatında sözleşme çıktısı al veya PDF indir.</p>
                  </div>
                </div>

                {/* Bottom Row: Full-width dark contract button on both Desktop and Mobile */}
                <button
                  type="button"
                  onClick={() => {
                    const currentCustName = customerMode === 'existing'
                      ? (customers.find(c => c.id === selectedCustomerId)?.name || '')
                      : newCustName;
                    const currentPhone = customerMode === 'existing'
                      ? (customers.find(c => c.id === selectedCustomerId)?.phone || '')
                      : newCustPhone;
                    const currentEmail = customerMode === 'existing'
                      ? (customers.find(c => c.id === selectedCustomerId)?.email || '')
                      : newCustEmail;

                    const previewRes = {
                      id: editingResFromUrl ? editingResFromUrl.id : (activeRefKey ? `RES-DRAFT-${activeRefKey.substring(0, 8)}` : `RES-${new Date().getFullYear()}-001`),
                      customerName: currentCustName || 'İsimsiz Müşteri',
                      customerEmail: currentEmail || '',
                      customerPhone: currentPhone || '05xx xxx xx xx',
                      venueId: venueId,
                      venueName: selectedVenue?.name || 'Salon Seçilmedi',
                      date: startDate || todayDateStr,
                      eventDate: startDate || todayDateStr,
                      startDate: startDate || todayDateStr,
                      endDate: endDate || startDate || todayDateStr,
                      startTime: startTime,
                      endTime: endTime,
                      timeSlot: `${startTime}-${endTime}`,
                      guestCount: guestCount || 0,
                      selectedServices: calculations.mappedServices || [],
                      venuePrice: calculations.vPrice,
                      subtotal: calculations.sub,
                      discountAmount: calculations.disc,
                      vatAmount: calculations.vat,
                      totalAmount: calculations.grandTotal,
                      depositPaid: calculations.dep,
                      remainingBalance: calculations.remaining,
                      paymentStatus: paymentStatus || 'Bekliyor',
                      invoiceType: invoiceType || 'individual',
                      tcNo: tcNo || '',
                      vknNo: vknNo || '',
                      taxOffice: taxOffice || '',
                      invoiceAddress: invoiceAddress || '',
                      notes: notes || '',
                      flowPlan: flowPlan || []
                    };
                    if (handlePrintInvoice) {
                      handlePrintInvoice(previewRes);
                    } else if (window.handlePrintInvoice) {
                      window.handlePrintInvoice(previewRes);
                    } else {
                      alert('Sözleşme yazdırma modülü hazırlandı.');
                    }
                  }}
                  className="w-full bg-[#0e1628] hover:bg-[#18233c] text-white font-extrabold text-xs py-3.5 px-4 rounded-2xl shadow-md flex items-center justify-center space-x-2 cursor-pointer transition hover:scale-[1.01] active:scale-[0.99] border border-slate-800"
                >
                  <svg className="w-4 h-4 text-white shrink-0 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <circle cx="12" cy="12" r="10" strokeWidth="2"></circle>
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 16v-4m0-4h.01"></path>
                  </svg>
                  <span className="tracking-wide">SÖZLEŞMEYİ GÖRÜNTÜLE / İNDİR (PDF)</span>
                </button>
              </div>

              """

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    s_idx = content.find(old_card_start)
    e_idx = content.find(old_card_end, s_idx)

    if s_idx != -1 and e_idx != -1:
        content = content[:s_idx] + new_card + content[e_idx:]
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated contract card layout in {h_file}")
    else:
        print(f"Markers not found in {h_file}")

print("All HTML files updated with new contract card layout!")
