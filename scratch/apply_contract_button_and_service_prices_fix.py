import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update CreateReservationPageComponent props to receive handlePrintInvoice
old_prop = "function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations = [], setReservations, draftReservations = [], setDraftReservations, currentUser, prefilledDate, onSaveReservation, onCancel, showToast, navigateTo }) {"
new_prop = "function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations = [], setReservations, draftReservations = [], setDraftReservations, currentUser, prefilledDate, onSaveReservation, onCancel, showToast, navigateTo, handlePrintInvoice }) {"

if old_prop in content:
    content = content.replace(old_prop, new_prop)
    print("1. Updated CreateReservationPageComponent props signature.")

# 2. Update CreateReservationPageComponent invocation in App component to pass handlePrintInvoice
old_app_call = "onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {"
new_app_call = "handlePrintInvoice={handlePrintInvoice}\n                      onSaveReservation={(newRes, newCust, refKeyToRemove, isEdit) => {"

if old_app_call in content and "handlePrintInvoice={handlePrintInvoice}" not in content:
    content = content.replace(old_app_call, new_app_call)
    print("2. Passed handlePrintInvoice prop to CreateReservationPageComponent in App.")

# 3. Update service customUnitPrice loading in editingResFromUrl
old_service_load = """          if (editingResFromUrl.selectedServices && Array.isArray(editingResFromUrl.selectedServices)) {
            setSelectedServices([...editingResFromUrl.selectedServices]);
          }"""

new_service_load = """          if (editingResFromUrl.selectedServices && Array.isArray(editingResFromUrl.selectedServices)) {
            const normalizedServices = editingResFromUrl.selectedServices.map(item => ({
              ...item,
              customUnitPrice: item.customUnitPrice !== undefined ? item.customUnitPrice : (item.unitPrice !== undefined ? item.unitPrice : undefined)
            }));
            setSelectedServices(normalizedServices);
          }"""

if old_service_load in content:
    content = content.replace(old_service_load, new_service_load)
    print("3. Normalized editingResFromUrl.selectedServices to preserve customUnitPrice.")

# 4. Insert Contract View / Download Card above Takvim Canlı Ön İzlemesi
old_takvim_card = """              {/* TAKVİM ÖN İZLEME KARTI */}
              <div className="glass-panel p-5 rounded-3xl space-y-3 shadow-sm border border-slate-200 dark:border-brand-border">"""

new_contract_and_takvim_card = """              {/* RESMİ SÖZLEŞME GÖRÜNTÜLE & İNDİR (YAZDIR) KARTI */}
              <div className="glass-panel p-4 rounded-3xl space-y-3 shadow-sm border border-amber-500/40 bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                  <div className="flex items-center space-x-2.5">
                    <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 flex items-center justify-center font-bold text-xl shrink-0 shadow-sm border border-amber-500/30">
                      📄
                    </div>
                    <div>
                      <h4 className="font-extrabold text-xs text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                        <span>Resmi Etkinlik Sözleşmesi</span>
                        {isEditMode && <span className="text-[10px] bg-amber-500/20 text-amber-800 dark:text-gold-400 font-mono px-1.5 py-0.5 rounded">ID: {editingResFromUrl?.id}</span>}
                      </h4>
                      <p className="text-[11px] text-slate-500 dark:text-gray-400">Canlı girilen fiyatlarla A4 formatında sözleşme çıktısı al veya PDF indir.</p>
                    </div>
                  </div>
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
                    className="w-full sm:w-auto gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow-md flex items-center justify-center space-x-2 cursor-pointer hover:scale-105 transition"
                  >
                    <ThemeIcon icon="printer" fallbackEmoji="📄" className="w-4 h-4 shrink-0" />
                    <span>Sözleşmeyi Görüntüle / İndir (PDF)</span>
                  </button>
                </div>
              </div>

              {/* TAKVİM ÖN İZLEME KARTI */}
              <div className="glass-panel p-5 rounded-3xl space-y-3 shadow-sm border border-slate-200 dark:border-brand-border">"""

if old_takvim_card in content:
    content = content.replace(old_takvim_card, new_contract_and_takvim_card)
    print("4. Placed Contract View / Download Card directly above Takvim Canlı Ön İzlemesi.")
else:
    print("WARNING: Could not find old_takvim_card in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
