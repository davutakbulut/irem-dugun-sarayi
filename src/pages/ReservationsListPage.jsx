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
  const [isFilterOpen, setIsFilterOpen] = useState(true); // Default open on desktop

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
      flowPlan: res.flowPlan && res.flowPlan.length > 0 ? JSON.parse(JSON.stringify(res.flowPlan)) : [
        { time: '18:00', title: 'Karşılama ve İkram', description: 'Giriş kapısında lokum ve kolonya ikramı', responsible: 'Hoşgeldin Ekibi' },
        { time: '19:30', title: 'Çiftlerin Sahneye Girişi & İlk Dans', description: 'Sis ve konfeti eşliğinde sahnede ilk dans', responsible: 'Orkestra & Işık Şefi' },
        { time: '21:00', title: 'Pasta Kesimi & Takı Töreni', description: 'Görsel kutlama pastası ve takı alanı', responsible: 'Salon Müdürü' }
      ]
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

  // Dynamic Month & Year Navigation State (Defaults to real current date)
  const MONTH_NAMES = [
    'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'
  ];

  const today = new Date();
  const [currentYear, setCurrentYear] = useState(today.getFullYear());
  const [currentMonth, setCurrentMonth] = useState(today.getMonth()); // Real current month (July = 6)

  const handlePrevMonth = () => {
    if (currentMonth === 0) {
      setCurrentMonth(11);
      setCurrentYear(prev => prev - 1);
    } else {
      setCurrentMonth(prev => prev - 1);
    }
  };

  const handleNextMonth = () => {
    if (currentMonth === 11) {
      setCurrentMonth(0);
      setCurrentYear(prev => prev + 1);
    } else {
      setCurrentMonth(prev => prev + 1);
    }
  };

  const handleGoToday = () => {
    const now = new Date();
    setCurrentYear(now.getFullYear());
    setCurrentMonth(now.getMonth());
  };

  // Dynamic Calendar Grid Setup for currentYear & currentMonth (1 to 28..31 Days)
  const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
  const jsFirstDay = new Date(currentYear, currentMonth, 1).getDay(); // Sunday=0, Monday=1, ..., Saturday=6
  const monthStartEmptyCount = jsFirstDay === 0 ? 6 : jsFirstDay - 1; // Monday-first calendar index

  const calendarGridCells = [];
  for (let i = 0; i < monthStartEmptyCount; i++) {
    calendarGridCells.push({ isEmpty: true, key: `empty-${i}` });
  }
  for (let day = 1; day <= daysInMonth; day++) {
    const dayStr = day < 10 ? `0${day}` : `${day}`;
    const monthStr = (currentMonth + 1) < 10 ? `0${currentMonth + 1}` : `${currentMonth + 1}`;
    const dateStr = `${currentYear}-${monthStr}-${dayStr}`;
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
      <div className="glass-panel p-5 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            📅 Rezervasyonlar & Canlı Takvim Yönetimi
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Tüm düğün sözleşmelerini detaylarıyla inceleyin, takvimde sürükleyip taşıyın veya yeniden düzenleyin.
          </p>
        </div>

        {/* SINGLE LINE ACTION BAR ON MOBILE (Filtreler, Yeni Rez, Liste & Takvim Görünümü) */}
        <div className="flex items-center space-x-1.5 sm:space-x-2 w-full md:w-auto justify-between md:justify-end shrink-0">
          
          {/* FILTER TOGGLE BUTTON */}
          <button
            onClick={() => setIsFilterOpen(!isFilterOpen)}
            className={`h-10 px-3 rounded-xl font-bold text-xs border transition flex items-center space-x-1.5 shadow-xs ${
              isFilterOpen 
                ? 'bg-amber-500/15 border-amber-500/40 text-amber-900 dark:text-gold-400' 
                : 'bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border-slate-200 dark:border-brand-border hover:bg-slate-200 dark:hover:bg-slate-800'
            }`}
            title="Detaylı Filtreleri Aç / Kapat"
          >
            <svg className="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
            </svg>
            <span className="hidden sm:inline">Filtreler</span>
            <span className="text-[10px]">{isFilterOpen ? '▲' : '▼'}</span>
          </button>

          {/* YENİ REZERVASYON BUTTON */}
          <button 
            onClick={onNewResClick} 
            className="gold-button font-bold text-xs h-10 px-3 sm:px-4 rounded-xl shadow-sm flex items-center space-x-1.5 shrink-0"
            title="Yeni Rezervasyon Oluştur"
          >
            <span className="text-sm">➕</span>
            <span className="hidden sm:inline">Yeni Rezervasyon</span>
          </button>

          {/* NORDIC MINIMAL VIEW TOGGLE (LIST VS CALENDAR - ICONIC NO TEXT) */}
          <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border h-10 items-center shrink-0">
            <button
              onClick={() => setViewMode('table')}
              className={`h-8 w-9 sm:w-10 rounded-lg text-xs font-bold transition flex items-center justify-center ${
                viewMode === 'table' 
                  ? 'bg-white dark:bg-brand-card text-amber-700 dark:text-gold-400 shadow-sm border border-slate-200/60 dark:border-brand-border' 
                  : 'text-slate-400 hover:text-slate-700 dark:hover:text-gray-200'
              }`}
              title="Liste Görünümü"
              aria-label="Liste Görünümü"
            >
              {/* Nordic Minimalist Table/List SVG */}
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="8" y1="6" x2="21" y2="6"/>
                <line x1="8" y1="12" x2="21" y2="12"/>
                <line x1="8" y1="18" x2="21" y2="18"/>
                <line x1="3" y1="6" x2="3.01" y2="6"/>
                <line x1="3" y1="12" x2="3.01" y2="12"/>
                <line x1="3" y1="18" x2="3.01" y2="18"/>
              </svg>
            </button>

            <button
              onClick={() => setViewMode('calendar')}
              className={`h-8 w-9 sm:w-10 rounded-lg text-xs font-bold transition flex items-center justify-center ${
                viewMode === 'calendar' 
                  ? 'bg-white dark:bg-brand-card text-amber-700 dark:text-gold-400 shadow-sm border border-slate-200/60 dark:border-brand-border' 
                  : 'text-slate-400 hover:text-slate-700 dark:hover:text-gray-200'
              }`}
              title="Takvim Görünümü"
              aria-label="Takvim Görünümü"
            >
              {/* Nordic Minimalist Calendar Grid SVG */}
              <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="3" ry="3"/>
                <line x1="16" y1="2" x2="16" y2="6"/>
                <line x1="8" y1="2" x2="8" y2="6"/>
                <line x1="3" y1="10" x2="21" y2="10"/>
                <line x1="8" y1="14" x2="8.01" y2="14"/>
                <line x1="12" y1="14" x2="12.01" y2="14"/>
                <line x1="16" y1="14" x2="16.01" y2="14"/>
                <line x1="8" y1="18" x2="8.01" y2="18"/>
                <line x1="12" y1="18" x2="12.01" y2="18"/>
                <line x1="16" y1="18" x2="16.01" y2="18"/>
              </svg>
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
                          {res.remainingBalance === 0 ? '0 ₺ (Ödendi ✓)' : formatCurrency(res.remainingBalance)}
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
                              👁️ Detay Önizle
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
        /* INTERACTIVE MONTHLY CALENDAR VIEW */
        <div className="space-y-4">
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

          <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
            
            {/* DYNAMIC MONTH NAVIGATION TOOLBAR (PERFECTLY ALIGNED H-10) */}
            <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-200 dark:border-brand-border">
              
              {/* PREV / MONTH TITLE / NEXT GROUP */}
              <div className="flex items-center space-x-2">
                <button
                  onClick={handlePrevMonth}
                  className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-brand-dark hover:bg-amber-500/20 dark:hover:bg-slate-800 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-brand-border flex items-center justify-center transition cursor-pointer shrink-0 shadow-xs"
                  title="Önceki Ay"
                  aria-label="Önceki Ay"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"/>
                  </svg>
                </button>

                <div className="h-10 flex items-center space-x-2 bg-amber-500/10 px-4 rounded-xl border border-amber-500/30">
                  <span className="text-base sm:text-lg">📅</span>
                  <h4 className="font-heading font-extrabold text-sm sm:text-base text-slate-900 dark:text-white whitespace-nowrap">
                    {MONTH_NAMES[currentMonth]} {currentYear}
                  </h4>
                </div>

                <button
                  onClick={handleNextMonth}
                  className="w-10 h-10 rounded-xl bg-slate-100 dark:bg-brand-dark hover:bg-amber-500/20 dark:hover:bg-slate-800 text-slate-700 dark:text-gray-200 border border-slate-200 dark:border-brand-border flex items-center justify-center transition cursor-pointer shrink-0 shadow-xs"
                  title="Sonraki Ay"
                  aria-label="Sonraki Ay"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7"/>
                  </svg>
                </button>
              </div>

              {/* DROPDOWNS & SHORTCUT GROUP */}
              <div className="flex items-center space-x-2">
                <select
                  value={currentMonth}
                  onChange={(e) => setCurrentMonth(Number(e.target.value))}
                  className="h-10 bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 text-xs font-bold text-slate-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-amber-500/40 cursor-pointer shadow-xs"
                >
                  {MONTH_NAMES.map((name, idx) => (
                    <option key={idx} value={idx}>{name}</option>
                  ))}
                </select>

                <select
                  value={currentYear}
                  onChange={(e) => setCurrentYear(Number(e.target.value))}
                  className="h-10 bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 text-xs font-bold text-slate-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-amber-500/40 cursor-pointer shadow-xs"
                >
                  {[2024, 2025, 2026, 2027, 2028].map(y => (
                    <option key={y} value={y}>{y}</option>
                  ))}
                </select>

                <button
                  onClick={handleGoToday}
                  className="h-10 px-3.5 bg-amber-50 dark:bg-amber-950/40 text-amber-800 dark:text-gold-400 rounded-xl font-bold text-xs border border-amber-300 dark:border-amber-700/60 shadow-xs hover:bg-amber-100 transition cursor-pointer flex items-center space-x-1 shrink-0"
                >
                  <span>🎯</span>
                  <span className="hidden sm:inline">Bugünkü Ay ({MONTH_NAMES[today.getMonth()]} {today.getFullYear()})</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-7 gap-2 text-center font-bold text-xs text-slate-600 dark:text-gray-300">
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Pzt</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Sal</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Çar</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Per</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Cum</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Cmt</div>
              <div className="bg-slate-100 dark:bg-brand-dark py-2.5 rounded-xl border border-slate-200 dark:border-brand-border">Paz</div>
            </div>

            <div className="grid grid-cols-7 gap-2 text-xs">
              {calendarGridCells.map(cell => {
                if (cell.isEmpty) {
                  return (
                    <div key={cell.key} className="min-h-[110px] bg-slate-50/50 dark:bg-brand-dark/40 rounded-2xl border border-slate-100 dark:border-brand-border/40" />
                  );
                }

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

      {/* 4. HOURLY TIMELINE SCHEDULE FLOW MODAL */}
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

            <div className="space-y-4 text-xs">
              <div className="p-3 bg-amber-50 dark:bg-amber-950/30 rounded-2xl border border-amber-200 dark:border-amber-800/40 text-amber-900 dark:text-amber-300 font-medium">
                💡 <strong>Saat Akış Çizelgesi:</strong> Gün içindeki düğün ve etkinliklerin başlangıç-bitiş saatlerine göre kronolojik zaman çizelgesidir.
              </div>

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

      {/* 5. RICH DETAILED PREVIEW MODAL (HER ŞEY EKSİKSİZ VE DETAYLI) */}
      {selectedResForPreview && (
        <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto">
            
            {/* PREVIEW HEADER */}
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
              <div>
                <div className="flex items-center space-x-2">
                  <span className="bg-amber-500/20 text-amber-800 dark:text-gold-400 text-[10px] font-extrabold px-2.5 py-0.5 rounded-md border border-amber-500/30 uppercase font-mono">
                    Sözleşme No: {selectedResForPreview.id}
                  </span>
                  <span className={`text-[10px] font-extrabold px-2.5 py-0.5 rounded-md ${
                    selectedResForPreview.paymentStatus === 'Ödendi' || selectedResForPreview.paymentStatus === 'Tamamlandı' ? 'bg-emerald-500/20 text-emerald-600' :
                    selectedResForPreview.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-600' : 'bg-slate-200 text-slate-700'
                  }`}>
                    {selectedResForPreview.paymentStatus}
                  </span>
                </div>
                <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white mt-1">
                  👑 {selectedResForPreview.customerName}
                </h3>
              </div>
              <button onClick={() => setSelectedResForPreview(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center">✕</button>
            </div>

            <div className="space-y-4 text-xs">
              
              {/* SECTION A: MÜŞTERİ İLETİŞİM & SALON ZAMAN BİLGİLERİ */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5">
                  <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">👤 Müşteri İletişim Bilgileri:</span>
                  <div className="font-extrabold text-sm text-slate-900 dark:text-white">{selectedResForPreview.customerName}</div>
                  <div>📞 Birincil Tel: <strong className="font-mono text-slate-800 dark:text-gray-200">{selectedResForPreview.customerPhone}</strong></div>
                  <div>📱 İkinci Tel: <strong className="font-mono text-slate-800 dark:text-gray-200">{selectedResForPreview.customerSecondaryPhone || 'İkinci Tel Belirtilmedi'}</strong></div>
                  <div>✉️ E-Posta: <strong className="text-slate-800 dark:text-gray-200">{selectedResForPreview.customerEmail || 'E-Posta Girilmedi'}</strong></div>
                </div>

                <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5">
                  <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🏰 Etkinlik & Salon Detayı:</span>
                  <div className="font-extrabold text-sm text-slate-900 dark:text-white">
                    {(venues.find(v => v.id === selectedResForPreview.venueId))?.name || selectedResForPreview.venueId}
                  </div>
                  <div>📅 Tarih: <strong className="font-mono text-slate-800 dark:text-gray-200">{formatDate(selectedResForPreview.eventDate || selectedResForPreview.date)}</strong></div>
                  <div>⏰ Saat Aralığı: <strong className="font-mono text-emerald-600">{selectedResForPreview.startTime || '18:00'} - {selectedResForPreview.endTime || '23:00'}</strong></div>
                  <div>👥 Davetli Sayısı: <strong className="text-slate-800 dark:text-gray-200">{selectedResForPreview.guestCount} Davetli Kişi</strong></div>
                </div>
              </div>

              {/* SECTION B: DÜĞÜN AKIŞ PLANLAMASI (HANGİ BİLGİLER / AKIŞ VERİLDİ) */}
              <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">📜 Organizasyon & Zaman Akış Programı:</span>
                {(!selectedResForPreview.flowPlan || selectedResForPreview.flowPlan.length === 0) ? (
                  <div className="text-slate-400 italic">Standart akış programı uygulanacaktır. Özel akış bilgisi eklenmedi.</div>
                ) : (
                  <div className="space-y-2">
                    {selectedResForPreview.flowPlan.map((item, idx) => (
                      <div key={idx} className="flex justify-between items-center p-2.5 bg-white dark:bg-brand-card rounded-xl border border-slate-200 dark:border-brand-border">
                        <div className="flex items-center space-x-2">
                          <span className="font-mono font-bold text-amber-600 text-xs px-2 py-0.5 bg-amber-500/10 rounded">{item.time}</span>
                          <div>
                            <div className="font-bold text-slate-900 dark:text-white">{item.title}</div>
                            {item.description && <div className="text-[10px] text-slate-500">{item.description}</div>}
                          </div>
                        </div>
                        {item.responsible && (
                          <span className="text-[10px] font-bold text-slate-500 bg-slate-100 dark:bg-brand-dark px-2 py-0.5 rounded">
                            Sorumlu: {item.responsible}
                          </span>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* SECTION C: VERİLEN PAKETLER & EK HİZMETLER */}
              <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🎁 Verilen Hizmetler & Dahili Paketler:</span>
                {(!selectedResForPreview.selectedServices || selectedResForPreview.selectedServices.length === 0) ? (
                  <div className="text-slate-400 italic">Dahili temel salon paketi dâhildir. Ek paket seçilmedi.</div>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {selectedResForPreview.selectedServices.map((srvId, sIdx) => {
                      const sObj = services.find(s => s.id === srvId);
                      return (
                        <span key={sIdx} className="bg-white dark:bg-brand-card border border-amber-500/30 px-3 py-1.5 rounded-xl font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1 shadow-xs">
                          <span>🎁</span>
                          <span>{sObj?.name || srvId}</span>
                          {sObj?.price && <span className="font-mono text-amber-600 text-[10px]">({formatCurrency(sObj.price)})</span>}
                        </span>
                      );
                    })}
                  </div>
                )}
              </div>

              {/* SECTION D: ÖDEMELER NE DURUMDA & HANGİLERİNİN ÖDEMELERİ YAPILDI */}
              <div className="bg-amber-50/60 dark:bg-amber-950/20 p-4 rounded-2xl border border-amber-300 dark:border-amber-700/50 space-y-3">
                <span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider">💰 Detaylı Ödeme Durumları & Finansal Döküm:</span>
                
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-center">
                  <div className="p-2 bg-white dark:bg-brand-card rounded-xl border">
                    <span className="text-[10px] text-slate-400 block font-bold">Salon Bedeli:</span>
                    <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(selectedResForPreview.venuePrice || 85000)}</span>
                  </div>
                  <div className="p-2 bg-white dark:bg-brand-card rounded-xl border">
                    <span className="text-[10px] text-slate-400 block font-bold">Genel Toplam:</span>
                    <span className="font-mono font-bold text-amber-600">{formatCurrency(selectedResForPreview.totalAmount)}</span>
                  </div>
                  <div className="p-2 bg-white dark:bg-brand-card rounded-xl border">
                    <span className="text-[10px] text-emerald-600 block font-bold">Ödenen Kapora:</span>
                    <span className="font-mono font-extrabold text-emerald-600">{formatCurrency(selectedResForPreview.depositPaid)}</span>
                  </div>
                  <div className="p-2 bg-white dark:bg-brand-card rounded-xl border">
                    <span className="text-[10px] text-red-500 block font-bold">Kalan Net Bakiye:</span>
                    <span className="font-mono font-extrabold text-red-500">
                      {selectedResForPreview.remainingBalance === 0 ? '0 ₺ (Ödendi)' : formatCurrency(selectedResForPreview.remainingBalance)}
                    </span>
                  </div>
                </div>

                {/* HANGİ ÖDEMELER YAPILDI DÖKÜMÜ */}
                <div className="p-3 bg-white dark:bg-brand-card rounded-xl border space-y-2">
                  <span className="font-bold block text-slate-800 dark:text-gray-200">💳 Gerçekleşen Ödemeler Geçmişi:</span>
                  <div className="space-y-1 text-[11px]">
                    <div className="flex justify-between items-center text-emerald-600 font-bold">
                      <span>✓ 1. Ödeme (Kapora Tahsilatı):</span>
                      <span className="font-mono">{formatCurrency(selectedResForPreview.depositPaid)} (Tahsil Edildi)</span>
                    </div>
                    {selectedResForPreview.remainingBalance === 0 ? (
                      <div className="flex justify-between items-center text-emerald-600 font-bold">
                        <span>✓ 2. Ödeme (Kalan Bakiye Tahsilatı):</span>
                        <span className="font-mono">Tamamı Ödendi (Hesap Kapatıldı)</span>
                      </div>
                    ) : (
                      <div className="flex justify-between items-center text-amber-600 font-bold">
                        <span>⏳ 2. Ödeme (Kalan Bakiye Tahsilatı):</span>
                        <span className="font-mono">{formatCurrency(selectedResForPreview.remainingBalance)} (Etkinlik Günü Ödenecek)</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* SECTION E: OPERASYONEL NOTLAR */}
              {selectedResForPreview.notes && (
                <div className="bg-slate-50 dark:bg-brand-dark p-3.5 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1">
                  <span className="text-slate-400 font-bold block">📝 Operasyonel Notlar & Özel İstekler:</span>
                  <p className="text-slate-700 dark:text-gray-300 italic">{selectedResForPreview.notes}</p>
                </div>
              )}

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

      {/* 7. FULL EDIT RESERVATION MODAL (HER ŞEY YENİDEN DÜZENLENEBİLİR) */}
      {editingRes && editForm && (
        <div className="fixed inset-0 z-[9999] bg-black/70 backdrop-blur-md flex items-center justify-center p-4">
          <div className="bg-white dark:bg-brand-card border border-amber-500/50 rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto">
            
            {/* EDIT HEADER */}
            <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
              <div>
                <span className="text-[10px] font-bold text-amber-600 uppercase font-mono">Düzenlenen Sözleşme: {editForm.id}</span>
                <h3 className="text-lg font-heading font-extrabold text-slate-900 dark:text-white">✏️ Rezervasyon Bilgilerini Düzenle</h3>
              </div>
              <button onClick={() => setEditingRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold text-xs">✕</button>
            </div>

            <div className="space-y-4 text-xs">
              
              {/* SECTION 1: SALON VE DAVETLİ DÜZENLEME */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">1. Salon & Kapasite Bilgileri:</span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Düğün Salonu:</label>
                    <select
                      value={editForm.venueId}
                      onChange={e => setEditForm({ ...editForm, venueId: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    >
                      {(venues || []).map(v => <option key={v.id} value={v.id}>{v.name}</option>)}
                    </select>
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Salon Bedeli (TL):</label>
                    <input
                      type="number"
                      value={editForm.venuePrice}
                      onChange={e => setEditForm({ ...editForm, venuePrice: Number(e.target.value) })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Davetli Sayısı (Kişi):</label>
                    <input
                      type="number"
                      value={editForm.guestCount}
                      onChange={e => setEditForm({ ...editForm, guestCount: Number(e.target.value) })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 2: TARİH VE SAAT DÜZENLEME */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">2. Etkinlik Tarihi & Saat Dilimi:</span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Etkinlik Tarihi:</label>
                    <input
                      type="date"
                      value={editForm.startDate}
                      onChange={e => setEditForm({ ...editForm, startDate: e.target.value, eventDate: e.target.value, date: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Başlangıç Saati:</label>
                    <input
                      type="time"
                      value={editForm.startTime}
                      onChange={e => setEditForm({ ...editForm, startTime: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Bitiş Saati:</label>
                    <input
                      type="time"
                      value={editForm.endTime}
                      onChange={e => setEditForm({ ...editForm, endTime: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    />
                  </div>
                </div>
              </div>

              {/* SECTION 3: MÜŞTERİ İLETİŞİM BİLGİLERİ DÜZENLEME (HER ŞEY ZORUNLU) */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">3. Müşteri İletişim Bilgileri:</span>
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

              {/* SECTION 4: ÖDEME & KAPORA DÜZENLEME */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <span className="font-bold block text-slate-700 dark:text-gray-200">4. Finans, Kapora & Fatura Statüsü:</span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Tahsil Edilen Kapora (TL):</label>
                    <input
                      type="number"
                      value={editForm.depositPaid}
                      onChange={e => {
                        const dep = Number(e.target.value);
                        const tot = editForm.totalAmount || (editForm.venuePrice + 15000);
                        const rem = Math.max(0, tot - dep);
                        setEditForm({
                          ...editForm,
                          depositPaid: dep,
                          remainingBalance: rem,
                          paymentStatus: rem === 0 ? 'Ödendi' : dep > 0 ? 'Kapora Alındı' : 'Bekliyor'
                        });
                      }}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold text-emerald-600"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Ödeme Durumu:</label>
                    <select
                      value={editForm.paymentStatus}
                      onChange={e => setEditForm({ ...editForm, paymentStatus: e.target.value })}
                      className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5 font-bold"
                    >
                      <option value="Bekliyor">Bekliyor (Ödeme Bekleniyor)</option>
                      <option value="Kapora Alındı">Kapora Alındı</option>
                      <option value="Ödendi">Ödendi / Tamamlandı</option>
                    </select>
                  </div>
                  <div className="flex items-center pt-5">
                    <label className="flex items-center space-x-2 cursor-pointer font-bold">
                      <input
                        type="checkbox"
                        checked={editForm.isInvoiced}
                        onChange={e => setEditForm({ ...editForm, isInvoiced: e.target.checked })}
                        className="w-4 h-4 rounded text-amber-600"
                      />
                      <span>📄 Faturası Kesildi mi?</span>
                    </label>
                  </div>
                </div>
              </div>

              {/* SECTION 5: ORGANİZASYON AKIŞ DÜZENLEME */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-3">
                <div className="flex justify-between items-center">
                  <span className="font-bold block text-slate-700 dark:text-gray-200">5. Düğün & Etkinlik Akış Planlaması:</span>
                  <button
                    onClick={() => {
                      const newPlan = [...(editForm.flowPlan || [])];
                      newPlan.push({ time: '20:00', title: 'Yeni Akış Maddesi', description: 'Açıklama giriniz', responsible: 'Müdür' });
                      setEditForm({ ...editForm, flowPlan: newPlan });
                    }}
                    className="px-2.5 py-1 bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold rounded-lg text-[11px]"
                  >
                    ➕ Yeni Akış Maddesi Ekle
                  </button>
                </div>

                <div className="space-y-2">
                  {(editForm.flowPlan || []).map((step, idx) => (
                    <div key={idx} className="flex gap-2 items-center bg-white dark:bg-brand-card p-2 rounded-xl border">
                      <input
                        type="time"
                        value={step.time}
                        onChange={e => {
                          const updated = [...editForm.flowPlan];
                          updated[idx].time = e.target.value;
                          setEditForm({ ...editForm, flowPlan: updated });
                        }}
                        className="w-24 bg-slate-50 dark:bg-brand-dark p-1 rounded font-mono font-bold text-[11px]"
                      />
                      <input
                        type="text"
                        placeholder="Akış Başlığı"
                        value={step.title}
                        onChange={e => {
                          const updated = [...editForm.flowPlan];
                          updated[idx].title = e.target.value;
                          setEditForm({ ...editForm, flowPlan: updated });
                        }}
                        className="flex-1 bg-slate-50 dark:bg-brand-dark p-1 rounded font-bold text-[11px]"
                      />
                      <button
                        onClick={() => {
                          const updated = editForm.flowPlan.filter((_, i) => i !== idx);
                          setEditForm({ ...editForm, flowPlan: updated });
                        }}
                        className="text-red-500 font-bold px-2 py-1 hover:bg-red-50 rounded text-xs"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              {/* SECTION 6: OPERASYONEL NOTLAR */}
              <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border space-y-2">
                <span className="font-bold block text-slate-700 dark:text-gray-200">6. Operasyonel Ek Notlar & Özel İstekler:</span>
                <textarea
                  rows="3"
                  value={editForm.notes}
                  onChange={e => setEditForm({ ...editForm, notes: e.target.value })}
                  placeholder="Müşterinin özel istekleri, organizasyon detayları..."
                  className="w-full bg-white dark:bg-brand-card border rounded-xl p-2.5"
                />
              </div>

            </div>

            {/* EDIT MODAL FOOTER */}
            <div className="pt-3 border-t flex justify-between items-center text-xs font-bold">
              {editError && <span className="text-red-500 font-bold">⚠️ Müşteri adı ve telefonu zorunludur!</span>}
              <div className="flex space-x-3 ml-auto">
                <button onClick={() => setEditingRes(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark rounded-xl">İptal</button>
                <button
                  onClick={() => {
                    if (!editForm.customerName || !editForm.customerPhone) {
                      setEditError(true);
                      return;
                    }
                    const tot = (editForm.venuePrice || 85000) + (editForm.selectedServices ? editForm.selectedServices.length * 5000 : 0);
                    const rem = Math.max(0, tot - (editForm.depositPaid || 0));
                    const finalObj = {
                      ...editForm,
                      totalAmount: tot,
                      remainingBalance: rem,
                      paymentStatus: rem === 0 ? 'Ödendi' : (editForm.depositPaid > 0 ? 'Kapora Alındı' : 'Bekliyor')
                    };
                    if (onUpdateReservation) onUpdateReservation(finalObj);
                    setEditingRes(null);
                  }}
                  className="gold-button px-6 py-2.5 rounded-xl shadow"
                >
                  💾 Değişiklikleri Kaydet
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
