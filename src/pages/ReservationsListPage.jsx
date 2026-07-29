import React, { useState } from 'react';
import { formatCurrency, formatDate, isValidPhoneNumber, formatPhoneNumber } from '../utils/formatters';

export function ReservationsListPage({
  reservations = [],
  venues = [],
  services = [],
  customers = [],
  campaigns = [],
  onNewResClick,
  onUpdateReservation,
  onDeleteReservation,
  onPrintInvoice,
  onShowEmail
}) {
  // View & Filter State
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'calendar'
  const [isFilterOpen, setIsFilterOpen] = useState(false);

  const [searchQuery, setSearchQuery] = useState('');
  const [venueFilter, setVenueFilter] = useState('ALL');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [startDateFilter, setStartDateFilter] = useState('');
  const [endDateFilter, setEndDateFilter] = useState('');

  // Modals State
  const [selectedResForPreview, setSelectedResForPreview] = useState(null);
  const [editingRes, setEditingRes] = useState(null);
  const [deletingRes, setDeletingRes] = useState(null);

  // Edit Form Fields State
  const [editForm, setEditForm] = useState(null);
  const [editError, setEditError] = useState(false);

  // Open Edit Modal Helper
  const handleOpenEdit = (res) => {
    setSelectedResForPreview(null);
    setEditingRes(res);
    setEditForm({
      ...res,
      venuePrice: res.venuePrice || 85000,
      guestCount: res.guestCount || 500,
      startDate: res.startDate || res.eventDate || '',
      endDate: res.endDate || res.eventDate || '',
      startTime: res.startTime || '18:00',
      endTime: res.endTime || '23:00',
      selectedServices: res.selectedServices ? [...res.selectedServices] : [],
      customerName: res.customerName || '',
      customerEmail: res.customerEmail || '',
      customerPhone: res.customerPhone || '',
      customerSecondaryPhone: res.customerSecondaryPhone || '',
      depositPaid: res.depositPaid || 0,
      paymentStatus: res.paymentStatus || 'Bekliyor',
      isInvoiced: res.isInvoiced || false,
      notes: res.notes || '',
      flowPlan: res.flowPlan ? JSON.parse(JSON.stringify(res.flowPlan)) : []
    });
    setEditError(false);
  };

  // Filter Logic
  const filteredReservations = reservations.filter(r => {
    const q = searchQuery.toLowerCase().trim();
    const matchesSearch = !q ||
      (r.customerName || '').toLowerCase().includes(q) ||
      (r.id || '').toLowerCase().includes(q) ||
      (r.customerPhone || '').includes(q);

    const matchesVenue = venueFilter === 'ALL' || r.venueId === venueFilter;
    const matchesStatus = statusFilter === 'ALL' || r.paymentStatus === statusFilter;

    let matchesDate = true;
    if (startDateFilter && r.eventDate < startDateFilter) matchesDate = false;
    if (endDateFilter && r.eventDate > endDateFilter) matchesDate = false;

    return matchesSearch && matchesVenue && matchesStatus && matchesDate;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in pb-20">
      
      {/* 1. HEADER & TOP CONTROLS (Görünüm Değiştirici En Sağda) */}
      <div className="glass-panel p-5 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            📅 Rezervasyonlar & Canlı Takvim Yönetimi
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Tüm düğün sözleşmelerini filtreleyin, canlı takvimde inceleyin veya düzenleyin.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full lg:w-auto justify-between lg:justify-end">
          <button
            onClick={() => setIsFilterOpen(!isFilterOpen)}
            className="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 font-bold text-xs border border-slate-200 dark:border-brand-border flex items-center space-x-1.5 shadow-sm hover:bg-slate-200 dark:hover:bg-slate-800 transition"
          >
            <span>🔍 Filtreler</span>
            <span>{isFilterOpen ? '▲' : '▼'}</span>
          </button>

          <button onClick={onNewResClick} className="gold-button font-bold text-xs px-4 py-2 rounded-xl shadow flex items-center space-x-1">
            <span>➕ Yeni Rezervasyon</span>
          </button>

          {/* VIEW TOGGLE (EN SAĞDA) */}
          <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border">
            <button
              onClick={() => setViewMode('table')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${viewMode === 'table' ? 'bg-white dark:bg-brand-card text-slate-800 dark:text-gray-100 shadow' : 'text-slate-500'}`}
            >
              <span>📋</span><span>Liste Görünümü</span>
            </button>
            <button
              onClick={() => setViewMode('calendar')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${viewMode === 'calendar' ? 'bg-white dark:bg-brand-card text-slate-800 dark:text-gray-100 shadow' : 'text-slate-500'}`}
            >
              <span>📅</span><span>Takvim Görünümü</span>
            </button>
          </div>
        </div>
      </div>

      {/* 2. COLLAPSIBLE FILTER PANEL (AÇILIR KAPANIR FİLTRE ÇEKMECESİ) */}
      {isFilterOpen && (
        <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 animate-fade-in shadow-md">
          <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-2 text-xs font-bold text-slate-700 dark:text-gray-300">
            <span>🔍 Detaylı Filtreleme & Arama Kriterleri</span>
            <button
              onClick={() => {
                setSearchQuery('');
                setVenueFilter('ALL');
                setStatusFilter('ALL');
                setStartDateFilter('');
                setEndDateFilter('');
              }}
              className="text-amber-700 dark:text-gold-400 hover:underline text-[11px]"
            >
              Filtreleri Temizle ↺
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs">
            <div>
              <label className="font-bold block mb-1">Arama Kriteri:</label>
              <input
                type="text"
                placeholder="🔍 Müşteri Adı, Tel veya Sözleşme Kodu..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-medium"
              />
            </div>

            <div>
              <label className="font-bold block mb-1">Düğün Salonu Filtresi:</label>
              <select
                value={venueFilter}
                onChange={e => setVenueFilter(e.target.value)}
                className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
              >
                <option value="ALL">Tüm Salonlar ({venues.length})</option>
                {venues.map(v => (
                  <option key={v.id} value={v.id}>{v.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="font-bold block mb-1">Ödeme Durumu Filtresi:</label>
              <select
                value={statusFilter}
                onChange={e => setStatusFilter(e.target.value)}
                className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
              >
                <option value="ALL">Tüm Durumlar ({reservations.length})</option>
                <option value="Kapora Alındı">Kapora Alındı</option>
                <option value="Ödendi">Ödendi / Tamamlandı</option>
                <option value="Bekliyor">Bekliyor</option>
                <option value="İptal">İptal Edilenler</option>
              </select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="font-bold block mb-1">Başlangıç Tarihi:</label>
                <input
                  type="date"
                  value={startDateFilter}
                  onChange={e => setStartDateFilter(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold"
                />
              </div>
              <div>
                <label className="font-bold block mb-1">Bitiş Tarihi:</label>
                <input
                  type="date"
                  value={endDateFilter}
                  onChange={e => setEndDateFilter(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 font-bold"
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 3. VIEW SWITCHER: TABLE OR MASTER CALENDAR */}
      {viewMode === 'table' ? (
        /* TABLE LIST VIEW WITH EDIT & DELETE BUTTONS */
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                  <th className="py-3 px-3">Sözleşme Kodu</th>
                  <th className="py-3 px-3">Müşteri / Çift</th>
                  <th className="py-3 px-3">Düğün Salonu</th>
                  <th className="py-3 px-3">Tarih & Saat</th>
                  <th className="py-3 px-3">Davetli</th>
                  <th className="py-3 px-3">Toplam Tutar</th>
                  <th className="py-3 px-3">Kalan Bakiye</th>
                  <th className="py-3 px-3">Ödeme Durumu</th>
                  <th className="py-3 px-3 text-right">İşlemler</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-brand-border">
                {filteredReservations.length === 0 ? (
                  <tr>
                    <td colSpan="9" className="py-8 text-center text-slate-400 font-bold">
                      Kriterlere uygun kayıtlı rezervasyon bulunamadı.
                    </td>
                  </tr>
                ) : (
                  filteredReservations.map(res => {
                    const vObj = venues.find(v => v.id === res.venueId);
                    return (
                      <tr key={res.id} className="hover:bg-slate-50 dark:hover:bg-brand-dark/50 font-medium text-slate-800 dark:text-gray-200 transition">
                        <td className="py-3.5 px-3 font-mono font-bold text-amber-700 dark:text-gold-400">{res.id}</td>
                        <td className="py-3.5 px-3">
                          <div className="font-bold">{res.customerName}</div>
                          <div className="text-[10px] text-slate-400">{res.customerPhone}</div>
                        </td>
                        <td className="py-3.5 px-3 font-bold">{vObj?.name || res.venueId}</td>
                        <td className="py-3.5 px-3 font-mono">
                          <div>{formatDate(res.eventDate)}</div>
                          <div className="text-[10px] text-slate-500">{res.startTime || '18:00'} - {res.endTime || '23:00'}</div>
                        </td>
                        <td className="py-3.5 px-3 font-bold">{res.guestCount} Kişi</td>
                        <td className="py-3.5 px-3 font-mono font-bold">{formatCurrency(res.totalAmount)}</td>
                        <td className="py-3.5 px-3 font-mono font-bold text-red-600 dark:text-red-400">
                          {res.remainingBalance === 0 ? '0 ₺ (Ödendi)' : formatCurrency(res.remainingBalance)}
                        </td>
                        <td className="py-3.5 px-3">
                          <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                            res.paymentStatus === 'Tamamlandı' || res.paymentStatus === 'Ödendi' ? 'bg-emerald-500/20 text-emerald-600' :
                            res.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-600' :
                            'bg-slate-200 text-slate-700'
                          }`}>
                            {res.paymentStatus}
                          </span>
                        </td>
                        <td className="py-3.5 px-3 text-right">
                          <div className="flex items-center justify-end space-x-1.5">
                            <button
                              onClick={() => setSelectedResForPreview(res)}
                              className="p-1.5 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 hover:bg-amber-500/20 transition font-bold text-xs"
                              title="Detaylı Önizle"
                            >
                              👁️
                            </button>
                            <button
                              onClick={() => handleOpenEdit(res)}
                              className="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold text-xs hover:bg-amber-500/30 transition"
                            >
                              ✏️ Düzenle
                            </button>
                            <button
                              onClick={() => setDeletingRes(res)}
                              className="px-2.5 py-1 rounded-lg bg-red-500/20 text-red-600 dark:text-red-400 font-bold text-xs hover:bg-red-500/30 transition"
                            >
                              🗑️ Sil
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* MASTER CALENDAR VIEW (Aynı gün saat sırasına göre sıralı) */
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
          <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
            <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">
              🗓️ Ağustos 2026 Master Etkinlik Çizelgesi
            </h3>
            <span className="text-xs text-slate-500 font-bold">14 Günlük Canlı Görünüm</span>
          </div>

          <div className="grid grid-cols-7 gap-2 text-center font-bold text-xs text-slate-500 pb-2 border-b">
            <span>Pzt</span><span>Sal</span><span>Çar</span><span>Per</span><span>Cum</span><span>Cmt</span><span>Paz</span>
          </div>

          <div className="grid grid-cols-7 gap-2 text-xs">
            {[...Array(14)].map((_, i) => {
              const dayDate = new Date(2026, 7, 20 + i);
              const dateStr = dayDate.toISOString().split('T')[0];
              
              // CHRONOLOGICAL SORTING BY START TIME (Aynı gün içinde saat sırasına göre sıralama)
              const dayResList = filteredReservations
                .filter(r => r.eventDate === dateStr && r.paymentStatus !== 'İptal')
                .sort((a, b) => {
                  const timeA = a.startTime || a.timeSlot || '00:00';
                  const timeB = b.startTime || b.timeSlot || '00:00';
                  return timeA.localeCompare(timeB);
                });

              return (
                <div key={dateStr} className="min-h-[110px] bg-slate-50 dark:bg-brand-dark p-2 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5 flex flex-col justify-between">
                  <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-1 text-[11px] font-bold">
                    <span className="text-slate-700 dark:text-gray-300">{dayDate.getDate()} Ağu</span>
                    <span className="text-[9px] bg-slate-200 dark:bg-brand-card px-1.5 rounded text-slate-600">{dayResList.length} Düğün</span>
                  </div>

                  <div className="space-y-1 overflow-y-auto max-h-24 custom-scrollbar">
                    {dayResList.map(r => {
                      const vObj = venues.find(v => v.id === r.venueId);
                      return (
                        <div
                          key={r.id}
                          onClick={() => setSelectedResForPreview(r)}
                          className="p-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/40 cursor-pointer transition text-[10px] space-y-0.5"
                          title="Tıklayarak Tüm Detayları Önizleyin"
                        >
                          <div className="flex justify-between font-mono text-[9px] text-amber-700 dark:text-gold-400 font-extrabold">
                            <span>🕒 {r.startTime || '18:00'}</span>
                            <span>{r.id}</span>
                          </div>
                          <div className="font-extrabold text-slate-800 dark:text-gray-100 truncate">{r.customerName}</div>
                          <div className="text-[9px] text-slate-500 dark:text-gray-400 truncate">{vObj?.name?.split(' ')[0]}</div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* 4. PREVIEW MODAL (Tüm detaylarıyla önizleme + Altta Düzenle Butonu) */}
      {selectedResForPreview && (
        <div className="fixed inset-0 z-[9999] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-3xl max-w-2xl w-full p-6 space-y-4 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <div>
                <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Sözleşme Kodu: {selectedResForPreview.id}</span>
                <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                  👑 {selectedResForPreview.customerName}
                </h3>
              </div>
              <button onClick={() => setSelectedResForPreview(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center">✕</button>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border space-y-1">
                <span className="text-slate-400 font-bold block">İletişim Bilgileri:</span>
                <div className="font-bold">{selectedResForPreview.customerPhone}</div>
                <div className="text-slate-500">{selectedResForPreview.customerEmail || 'E-posta girilmedi'}</div>
              </div>
              <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border space-y-1">
                <span className="text-slate-400 font-bold block">Etkinlik Zamanı:</span>
                <div className="font-bold font-mono">{formatDate(selectedResForPreview.eventDate)}</div>
                <div className="text-amber-600 font-bold">{selectedResForPreview.startTime || '18:00'} - {selectedResForPreview.endTime || '23:00'} ({selectedResForPreview.guestCount} Davetli)</div>
              </div>
            </div>

            <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border space-y-2 text-xs">
              <span className="text-slate-400 font-bold block">Finansal Döküm & Bakiye:</span>
              <div className="flex justify-between"><span>Salon Bedeli:</span><span className="font-mono font-bold">{formatCurrency(selectedResForPreview.venuePrice)}</span></div>
              <div className="flex justify-between"><span>Genel Toplam:</span><span className="font-mono font-bold">{formatCurrency(selectedResForPreview.totalAmount)}</span></div>
              <div className="flex justify-between"><span>Ödenen Kapora:</span><span className="font-mono font-bold text-emerald-600">{formatCurrency(selectedResForPreview.depositPaid)}</span></div>
              <div className="flex justify-between border-t pt-1 font-extrabold text-sm text-red-600 dark:text-red-400">
                <span>Kalan Net Bakiye:</span>
                <span>{selectedResForPreview.remainingBalance === 0 ? '0 ₺ (Ödendi ✓)' : formatCurrency(selectedResForPreview.remainingBalance)}</span>
              </div>
            </div>

            {/* PREVIEW BOTTOM ACTION BUTTONS */}
            <div className="pt-2 border-t border-slate-200 dark:border-brand-border flex justify-between items-center gap-2">
              <div className="flex space-x-2">
                {onPrintInvoice && (
                  <button onClick={() => onPrintInvoice(selectedResForPreview)} className="bg-slate-800 text-white px-3 py-2 rounded-xl font-bold text-xs">📄 Fatura Yazdır</button>
                )}
                {onShowEmail && (
                  <button onClick={() => onShowEmail(selectedResForPreview)} className="bg-emerald-600 text-white px-3 py-2 rounded-xl font-bold text-xs">✉️ E-Posta Önizle</button>
                )}
              </div>

              <div className="flex space-x-2">
                <button onClick={() => setSelectedResForPreview(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl text-xs font-bold">Kapat</button>
                <button
                  onClick={() => handleOpenEdit(selectedResForPreview)}
                  className="gold-button font-bold px-5 py-2 rounded-xl text-xs shadow"
                >
                  ✏️ Rezervasyonu Düzenle
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 5. DELETE CONFIRMATION MODAL */}
      {deletingRes && (
        <div className="fixed inset-0 z-[9999] bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border-2 border-red-500/60 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl animate-fade-in text-center">
            <div className="w-12 h-12 rounded-2xl bg-red-500/20 text-red-600 flex items-center justify-center text-2xl font-bold mx-auto border border-red-500/30">🗑️</div>
            <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
              Rezervasyon Silinsin Mi?
            </h3>
            <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed font-medium">
              <strong>{deletingRes.id}</strong> sözleşme kodlu <strong>{deletingRes.customerName}</strong> kaydı kalıcı olarak silinecektir. Bu işlem geri alınamaz.
            </p>
            <div className="pt-2 flex justify-center space-x-3 text-xs font-bold">
              <button onClick={() => setDeletingRes(null)} className="px-4 py-2.5 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl">İptal</button>
              <button
                onClick={() => {
                  onDeleteReservation(deletingRes.id);
                  setDeletingRes(null);
                }}
                className="px-5 py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-xl shadow"
              >
                Evet, Kalıcı Olarak Sil
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 6. FULL EDIT RESERVATION MODAL */}
      {editingRes && editForm && (
        <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-3xl max-w-3xl w-full p-6 space-y-4 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b pb-3">
              <div>
                <span className="text-[10px] font-bold text-amber-600 uppercase">Düzenlenen Sözleşme: {editForm.id}</span>
                <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">✏️ Rezervasyon Bilgilerini Düzenle</h3>
              </div>
              <button onClick={() => setEditingRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark font-bold text-xs">✕</button>
            </div>

            <div className="space-y-4 text-xs">
              {/* EDIT SALON & GUEST COUNT */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-bold block mb-1">Düğün Salonu:</label>
                  <select
                    value={editForm.venueId}
                    onChange={e => setEditForm({ ...editForm, venueId: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  >
                    {venues.map(v => <option key={v.id} value={v.id}>{v.name}</option>)}
                  </select>
                </div>
                <div>
                  <label className="font-bold block mb-1">Davetli Sayısı (Kişi):</label>
                  <input
                    type="number"
                    value={editForm.guestCount}
                    onChange={e => setEditForm({ ...editForm, guestCount: Number(e.target.value) })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  />
                </div>
              </div>

              {/* EDIT DATE & TIME */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="font-bold block mb-1">Etkinlik Tarihi:</label>
                  <input
                    type="date"
                    value={editForm.startDate}
                    onChange={e => setEditForm({ ...editForm, startDate: e.target.value, eventDate: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  />
                </div>
                <div>
                  <label className="font-bold block mb-1">Başlangıç Saati:</label>
                  <input
                    type="time"
                    value={editForm.startTime}
                    onChange={e => setEditForm({ ...editForm, startTime: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  />
                </div>
                <div>
                  <label className="font-bold block mb-1">Bitiş Saati:</label>
                  <input
                    type="time"
                    value={editForm.endTime}
                    onChange={e => setEditForm({ ...editForm, endTime: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  />
                </div>
              </div>

              {/* EDIT MANDATORY CUSTOMER CONTACT FIELDS */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">Müşteri İletişim Bilgileri (Zorunlu):</span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Müşteri Adı Soyadı <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      value={editForm.customerName}
                      onChange={e => setEditForm({ ...editForm, customerName: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">E-posta Adresi <span className="text-red-500">*</span>:</label>
                    <input
                      type="email"
                      value={editForm.customerEmail}
                      onChange={e => setEditForm({ ...editForm, customerEmail: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Birincil Telefon <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      value={editForm.customerPhone}
                      onChange={e => setEditForm({ ...editForm, customerPhone: formatPhoneNumber(e.target.value) })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">İkinci İletişim Telefonu <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      value={editForm.customerSecondaryPhone}
                      onChange={e => setEditForm({ ...editForm, customerSecondaryPhone: formatPhoneNumber(e.target.value) })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                </div>
              </div>

              {/* EDIT FINANCIALS & DEPOSIT */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-bold block mb-1">Tahsil Edilen Kapora (TL):</label>
                  <input
                    type="number"
                    value={editForm.depositPaid}
                    onChange={e => setEditForm({ ...editForm, depositPaid: Number(e.target.value) })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold text-emerald-600"
                  />
                </div>
                <div>
                  <label className="font-bold block mb-1">Ödeme Durumu:</label>
                  <select
                    value={editForm.paymentStatus}
                    onChange={e => setEditForm({ ...editForm, paymentStatus: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  >
                    <option value="Bekliyor">Bekliyor (Ödeme Bekleniyor)</option>
                    <option value="Kapora Alındı">Kapora Alındı</option>
                    <option value="Ödendi">Ödendi / Tamamlandı</option>
                  </select>
                </div>
              </div>
            </div>

            {/* EDIT SAVE ACTIONS */}
            <div className="pt-3 border-t flex justify-end space-x-3 text-xs font-bold">
              <button onClick={() => setEditingRes(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark rounded-xl">İptal</button>
              <button
                onClick={() => {
                  if (!editForm.customerName || !editForm.customerPhone) {
                    setEditError(true);
                    return;
                  }
                  onUpdateReservation(editForm);
                  setEditingRes(null);
                }}
                className="gold-button px-6 py-2.5 rounded-xl shadow"
              >
                💾 Değişiklikleri Kaydet
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
