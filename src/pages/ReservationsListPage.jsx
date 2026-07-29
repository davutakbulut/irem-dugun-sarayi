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

  // Drag & Drop State
  const [draggedResId, setDraggedResId] = useState(null);
  const [dragOverDate, setDragOverDate] = useState(null);

  // Modals State
  const [selectedResForPreview, setSelectedResForPreview] = useState(null);
  const [selectedDayInspector, setSelectedDayInspector] = useState(null);
  const [editingRes, setEditingRes] = useState(null);
  const [deletingRes, setDeletingRes] = useState(null);

  // Edit Form Fields State
  const [editForm, setEditForm] = useState(null);
  const [editError, setEditError] = useState(false);

  // Open Edit Modal Helper
  const handleOpenEdit = (res) => {
    setSelectedResForPreview(null);
    setSelectedDayInspector(null);
    setEditingRes(res);
    setEditForm({
      ...res,
      venuePrice: res.venuePrice || 85000,
      guestCount: res.guestCount || 500,
      startDate: res.startDate || res.eventDate || res.date || '',
      endDate: res.endDate || res.eventDate || res.date || '',
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
    const rDate = r.eventDate || r.date;
    if (startDateFilter && rDate < startDateFilter) matchesDate = false;
    if (endDateFilter && rDate > endDateFilter) matchesDate = false;

    return matchesSearch && matchesVenue && matchesStatus && matchesDate;
  });

  // August 2026 Calendar Grid Setup (1 to 31 Days)
  // August 1, 2026 is Saturday (Day 6 of week: Pzt=1, Sal=2, Çar=3, Per=4, Cum=5, Cmt=6, Paz=7)
  const augustStartEmptyCount = 5;
  const augustDaysCount = 31;

  const calendarGridCells = [];
  for (let i = 0; i < augustStartEmptyCount; i++) {
    calendarGridCells.push({ isEmpty: true, key: `empty-${i}` });
  }
  for (let day = 1; day <= augustDaysCount; day++) {
    const dayStr = day < 10 ? `0${day}` : `${day}`;
    const dateStr = `2026-08-${dayStr}`;
    calendarGridCells.push({ isEmpty: false, dayNumber: day, dateStr, key: dateStr });
  }

  // Handle Drag & Drop Date Change
  const handleDropReschedule = (resId, newDateStr) => {
    const targetRes = reservations.find(r => r.id === resId);
    if (targetRes && targetRes.eventDate !== newDateStr && targetRes.date !== newDateStr) {
      if (onUpdateReservation) {
        onUpdateReservation({
          ...targetRes,
          eventDate: newDateStr,
          date: newDateStr,
          startDate: newDateStr,
          endDate: newDateStr
        });
      }
    }
    setDraggedResId(null);
    setDragOverDate(null);
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in pb-20">
      
      {/* 1. HEADER & TOP CONTROLS */}
      <div className="glass-panel p-5 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            📅 Rezervasyonlar & Canlı Takvim Yönetimi
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Tüm düğün sözleşmelerini filtreleyin, canlı takvimde sürükleyip taşıyın veya düzenleyin.
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

      {/* 2. COLLAPSIBLE FILTER PANEL */}
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

      {/* 3. VIEW SWITCHER: TABLE OR INTERACTIVE MONTHLY CALENDAR */}
      {viewMode === 'table' ? (
        /* TABLE LIST VIEW */
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
                          <div>{formatDate(res.eventDate || res.date)}</div>
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
        /* INTERACTIVE MONTHLY CALENDAR VIEW (FULL 31-DAY AUG 2026 GRID WITH DRAG-AND-DROP & HOURLY TIMELINE FLOW) */
        <div className="space-y-4">
          
          {/* CALENDAR HEADER & HELP BADGE */}
          <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-3 shadow-sm">
            <div>
              <h3 className="font-heading font-extrabold text-lg sm:text-xl text-slate-900 dark:text-white">
                İnteraktif Takvim & Saat Çakışma Denetleyicisi
              </h3>
            </div>
            <div className="bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-amber-900 dark:text-amber-300 px-3.5 py-1.5 rounded-full text-xs font-semibold flex items-center space-x-1.5 shadow-sm">
              <span>💡</span>
              <span>Günün üzerine tıklayarak tüm salon doluluklarını saat akışında inceleyebilir veya kartı sürükleyerek başka güne taşıyabilirsiniz.</span>
            </div>
          </div>

          {/* MONTH TITLE */}
          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
            <div className="flex items-center space-x-2">
              <span className="text-xl">📅</span>
              <h4 className="font-heading font-extrabold text-lg text-slate-900 dark:text-white">
                Ağustos 2026
              </h4>
            </div>

            {/* 7 DAYS COLUMN HEADERS */}
            <div className="grid grid-cols-7 gap-2 text-center font-bold text-xs text-slate-600 dark:text-gray-300">
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Pzt</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Sal</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Çar</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Per</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Cum</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Cmt</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Paz</div>
            </div>

            {/* 31 DAYS MONTHLY GRID WITH DRAG-AND-DROP TARGETS */}
            <div className="grid grid-cols-7 gap-2 text-xs">
              {calendarGridCells.map(cell => {
                if (cell.isEmpty) {
                  return (
                    <div key={cell.key} className="min-h-[110px] bg-slate-50/50 dark:bg-brand-dark/40 rounded-2xl border border-slate-100 dark:border-brand-border/40" />
                  );
                }

                // Get reservations for this day sorted chronologically
                const dayResList = filteredReservations
                  .filter(r => (r.eventDate === cell.dateStr || r.date === cell.dateStr) && r.paymentStatus !== 'İptal')
                  .sort((a, b) => {
                    const timeA = a.startTime || a.timeSlot || '00:00';
                    const timeB = b.startTime || b.timeSlot || '00:00';
                    return timeA.localeCompare(timeB);
                  });

                const hasEvents = dayResList.length > 0;
                const isDragOver = dragOverDate === cell.dateStr;

                return (
                  <div
                    key={cell.key}
                    onClick={() => setSelectedDayInspector({ dateStr: cell.dateStr, dayNumber: cell.dayNumber, reservations: dayResList })}
                    onDragOver={(e) => {
                      e.preventDefault();
                      e.dataTransfer.dropEffect = 'move';
                    }}
                    onDragEnter={(e) => {
                      e.preventDefault();
                      setDragOverDate(cell.dateStr);
                    }}
                    onDragLeave={() => setDragOverDate(null)}
                    onDrop={(e) => {
                      e.preventDefault();
                      const resId = e.dataTransfer.getData('text/plain') || draggedResId;
                      if (resId) {
                        handleDropReschedule(resId, cell.dateStr);
                      }
                    }}
                    className={`min-h-[110px] p-2.5 rounded-2xl border transition flex flex-col justify-between cursor-pointer space-y-1.5 group ${
                      isDragOver
                        ? 'bg-amber-100/90 dark:bg-amber-900/50 border-2 border-amber-500 scale-[1.03] shadow-lg ring-2 ring-amber-400'
                        : hasEvents
                        ? 'bg-amber-50/80 dark:bg-amber-950/20 border-amber-300 dark:border-amber-700/60 shadow-sm hover:border-amber-500'
                        : 'bg-white dark:bg-brand-card border-slate-200 dark:border-brand-border hover:border-amber-400'
                    }`}
                  >
                    {/* DAY NUMBER TOP LEFT & EVENT COUNT BADGE TOP RIGHT */}
                    <div className="flex justify-between items-center text-xs font-extrabold">
                      <span className="text-slate-800 dark:text-gray-200 text-sm group-hover:text-amber-600 transition">
                        {cell.dayNumber}
                      </span>
                      {hasEvents && (
                        <span className="bg-slate-200 dark:bg-brand-dark text-slate-800 dark:text-gray-200 font-extrabold text-[9px] px-1.5 py-0.5 rounded-md border border-slate-300 dark:border-brand-border shadow-xs">
                          {dayResList.length} Etkinlik
                        </span>
                      )}
                    </div>

                    {/* EVENT PILLS :: CustomerName (StartTime) WITH HTML5 DRAGGABLE */}
                    <div className="space-y-1 overflow-y-auto max-h-20 custom-scrollbar">
                      {dayResList.map(r => {
                        const firstName = (r.customerName || 'Etkinlik').split(' ')[0];
                        return (
                          <div
                            key={r.id}
                            draggable={true}
                            onDragStart={(e) => {
                              e.stopPropagation();
                              e.dataTransfer.setData('text/plain', r.id);
                              setDraggedResId(r.id);
                            }}
                            onDragEnd={() => {
                              setDraggedResId(null);
                              setDragOverDate(null);
                            }}
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedResForPreview(r);
                            }}
                            className="bg-white dark:bg-brand-dark border border-slate-200 dark:border-brand-border hover:border-amber-500/60 p-1.5 rounded-xl text-[10px] font-bold text-slate-700 dark:text-gray-300 shadow-xs hover:scale-[1.02] transition flex items-center justify-between cursor-grab active:cursor-grabbing"
                            title="Sürükleyip başka bir güne bırakabilirsiniz. Tıklayarak Detay Önizleyin."
                          >
                            <span className="truncate">:: {firstName}</span>
                            <span className="text-[9px] font-mono text-amber-700 dark:text-gold-400 font-extrabold ml-1">({r.startTime || '18:00'})</span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 4. HOURLY TIMELINE SCHEDULE FLOW MODAL (GÜNE TIKLAYINCA SAAT AKIŞI GÖRÜNÜMÜ) */}
      {selectedDayInspector && (
        <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <div>
                <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Saat Akışı & Doluluk Çizelgesi</span>
                <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">
                  🕒 {formatDate(selectedDayInspector.dateStr)} ({selectedDayInspector.reservations.length} Etkinlik)
                </h3>
              </div>
              <button onClick={() => setSelectedDayInspector(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center">✕</button>
            </div>

            {/* HOURLY TIMELINE SCHEDULE FLOW (08:00 - 24:00) */}
            <div className="space-y-4 text-xs">
              <div className="p-3 bg-amber-50 dark:bg-amber-950/30 rounded-2xl border border-amber-200 dark:border-amber-800/40 text-amber-900 dark:text-amber-300 font-medium">
                💡 <strong>Saat Akış Çizelgesi:</strong> Gün içindeki düğün ve etkinliklerin başlangıç-bitiş saatlerine göre kronolojik zaman çizelgesidir.
              </div>

              {/* VISUAL HOURLY TIME BARS */}
              <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">⏱️ Günlük Zaman Çizelgesi (08:00 - 24:00):</span>
                <div className="flex justify-between text-[10px] font-mono font-bold text-slate-400 border-b pb-1">
                  <span>08:00</span><span>10:00</span><span>12:00</span><span>14:00</span><span>16:00</span><span>18:00</span><span>20:00</span><span>22:00</span><span>24:00</span>
                </div>

                {selectedDayInspector.reservations.length === 0 ? (
                  <div className="py-4 text-center text-slate-400 font-bold">Bu saat aralıklarında kayıtlı organizasyon yok.</div>
                ) : (
                  selectedDayInspector.reservations.map(r => {
                    const vObj = venues.find(v => v.id === r.venueId);
                    const startH = parseInt((r.startTime || '18:00').split(':')[0]) || 18;
                    const endH = parseInt((r.endTime || '23:00').split(':')[0]) || 23;
                    const leftPct = Math.max(0, ((startH - 8) / 16) * 100);
                    const widthPct = Math.min(100 - leftPct, Math.max(10, ((endH - startH) / 16) * 100));

                    return (
                      <div key={r.id} className="space-y-1">
                        <div className="flex justify-between text-[11px] font-bold">
                          <span className="text-slate-800 dark:text-gray-200">👑 {r.customerName} ({vObj?.name || r.venueId})</span>
                          <span className="font-mono text-amber-600 font-extrabold">{r.startTime || '18:00'} - {r.endTime || '23:00'}</span>
                        </div>
                        <div className="w-full bg-slate-200 dark:bg-brand-card h-4 rounded-full overflow-hidden relative border border-slate-300 dark:border-brand-border">
                          <div
                            className="bg-amber-500 h-full rounded-full flex items-center justify-center text-[9px] text-slate-900 font-extrabold truncate px-2 shadow-sm"
                            style={{ marginLeft: `${leftPct}%`, width: `${widthPct}%` }}
                          >
                            {r.startTime || '18:00'} - {r.customerName}
                          </div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>

              {/* DETAILED RESERVATION LIST FOR THE DAY */}
              <div className="space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">📋 Günlük Etkinlik Kartları ({selectedDayInspector.reservations.length}):</span>
                {selectedDayInspector.reservations.length === 0 ? (
                  <div className="p-6 text-center text-slate-400 font-bold bg-slate-50 dark:bg-brand-dark rounded-2xl border border-dashed">
                    Bu tarihte henüz herhangi bir düğün veya organizasyon kaydı yok.
                  </div>
                ) : (
                  selectedDayInspector.reservations.map(r => {
                    const vObj = venues.find(v => v.id === r.venueId);
                    return (
                      <div key={r.id} className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                        <div className="flex justify-between items-center font-bold">
                          <span className="text-amber-700 dark:text-gold-400 font-mono">{r.id} - {vObj?.name || r.venueId}</span>
                          <span className="text-emerald-600 font-mono font-extrabold">{r.startTime || '18:00'} - {r.endTime || '23:00'}</span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="font-extrabold text-sm text-slate-900 dark:text-white">👑 {r.customerName} ({r.guestCount} Kişi)</span>
                          <span className="font-mono font-bold text-amber-600">{formatCurrency(r.totalAmount)}</span>
                        </div>
                        <div className="flex justify-end space-x-2 pt-1 border-t border-slate-200 dark:border-brand-border/40">
                          <button
                            onClick={() => setSelectedResForPreview(r)}
                            className="px-3 py-1.5 bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-200 rounded-xl font-bold text-xs"
                          >
                            👁️ Detay Önizle
                          </button>
                          <button
                            onClick={() => handleOpenEdit(r)}
                            className="gold-button px-4 py-1.5 rounded-xl font-bold text-xs shadow"
                          >
                            ✏️ Rezervasyonu Düzenle
                          </button>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>

            <div className="pt-2 border-t flex justify-between items-center text-xs font-bold">
              <button
                onClick={() => {
                  setSelectedDayInspector(null);
                  onNewResClick();
                }}
                className="gold-button px-4 py-2 rounded-xl shadow"
              >
                ➕ Bu Tarihe Yeni Rezervasyon Ekle
              </button>
              <button onClick={() => setSelectedDayInspector(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl">Kapat</button>
            </div>
          </div>
        </div>
      )}

      {/* 5. PREVIEW MODAL */}
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
                <div className="font-bold font-mono">{formatDate(selectedResForPreview.eventDate || selectedResForPreview.date)}</div>
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

            {/* PREVIEW ACTIONS */}
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

      {/* 6. DELETE CONFIRMATION MODAL */}
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
                  if (onDeleteReservation) onDeleteReservation(deletingRes.id);
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

      {/* 7. FULL EDIT RESERVATION MODAL */}
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
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="font-bold block mb-1">Düğün Salonu:</label>
                  <select
                    value={editForm.venueId}
                    onChange={e => setEditForm({ ...editForm, venueId: e.target.value })}
                    className="w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold"
                  >
                    {(venues || []).map(v => <option key={v.id} value={v.id}>{v.name}</option>)}
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

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="font-bold block mb-1">Etkinlik Tarihi:</label>
                  <input
                    type="date"
                    value={editForm.startDate}
                    onChange={e => setEditForm({ ...editForm, startDate: e.target.value, eventDate: e.target.value, date: e.target.value })}
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

            <div className="pt-3 border-t flex justify-end space-x-3 text-xs font-bold">
              <button onClick={() => setEditingRes(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark rounded-xl">İptal</button>
              <button
                onClick={() => {
                  if (!editForm.customerName || !editForm.customerPhone) {
                    setEditError(true);
                    return;
                  }
                  if (onUpdateReservation) onUpdateReservation(editForm);
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
