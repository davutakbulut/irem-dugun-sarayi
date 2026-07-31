import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function ReservationsListComponent({
      reservations = [],
      draftReservations = [],
      setDraftReservations,
      currentUser,
      venues = [],
      services = [],
      customers = [],
      campaigns = [],
      navigateTo,
      onNewResClick,
      onUpdateReservation,
      onDeleteReservation,
      onPrintInvoice,
      onShowEmail
    }) {
      const [viewMode, setViewMode] = useState('table');
      const [isFilterOpen, setIsFilterOpen] = useState(typeof window !== 'undefined' ? window.innerWidth >= 768 : true);
      const [isDraftPanelOpen, setIsDraftPanelOpen] = useState(true);

      const [searchQuery, setSearchQuery] = useState('');
      const [venueFilter, setVenueFilter] = useState('ALL');
      const [statusFilter, setStatusFilter] = useState('ALL');
      const [startDateFilter, setStartDateFilter] = useState('');
      const [endDateFilter, setEndDateFilter] = useState('');

      const [selectedResForPreview, setSelectedResForPreview] = useState(null);
      const [selectedDayInspector, setSelectedDayInspector] = useState(null);
      const [editingRes, setEditingRes] = useState(null);
      const [deletingRes, setDeletingRes] = useState(null);

      const [editForm, setEditForm] = useState(null);
      const [editError, setEditError] = useState(false);

      const handleOpenEdit = (res) => {
        setSelectedResForPreview(null);
        setSelectedDayInspector(null);
        if (res && res.id) {
          window.location.hash = `#/rezervasyon-olustur?editId=${res.id}`;
        }
      };

      const filteredReservations = (reservations || []).filter(r => {
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

      // Drag & Drop State
      const [draggedResId, setDraggedResId] = useState(null);
      const [dragOverDate, setDragOverDate] = useState(null);

      // Handle Drag & Drop Date Change
      const handleDropReschedule = (resId, newDateStr) => {
        const targetRes = (reservations || []).find(r => r.id === resId);
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
          
          {/* HEADER & TOP CONTROLS (Görünüm Değiştirici En Sağda) */}
          <div className="glass-panel p-5 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4 shadow-sm">
            <div>
              <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
                <ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-6 h-6 text-amber-500 shrink-0" />
                <span>Rezervasyonlar & Canlı Takvim Yönetimi</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400">
                Tüm düğün sözleşmelerini filtreleyin, canlı takvimde inceleyin veya düzenleyin.
              </p>
            </div>

            {/* HARMONIOUS ACTION TOOLBAR (FORCED SINGLE ROW ON MOBILE, ICONIC WHEN TEXT DOESNT FIT) */}
            <div className="flex items-center space-x-1.5 sm:space-x-2.5 shrink-0 flex-nowrap w-full sm:w-auto justify-between sm:justify-end">
              
              {/* 1. FILTER TOGGLE BUTTON */}
              <button
                onClick={() => setIsFilterOpen(!isFilterOpen)}
                className={`h-10 px-2.5 sm:px-4 rounded-xl font-bold text-xs border transition flex items-center space-x-1.5 sm:space-x-2 shadow-xs cursor-pointer shrink-0 ${
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
                <span className="text-[10px] ml-0.5">{isFilterOpen ? '▲' : '▼'}</span>
              </button>

              {/* 2. YENİ REZERVASYON PRIMARY BUTTON */}
              <button 
                onClick={onNewResClick} 
                className="gold-button font-bold text-xs h-10 px-3 sm:px-4 rounded-xl shadow-sm flex items-center space-x-1.5 sm:space-x-2 shrink-0 cursor-pointer"
                title="Yeni Rezervasyon Oluştur"
              >
                <ThemeIcon icon="plus" fallbackEmoji="" className="w-3.5 h-3.5 shrink-0" />
                <span className="hidden sm:inline">Yeni Rezervasyon</span>
              </button>

              {/* 3. SEGMENTED VIEW SWITCHER (LIST VS CALENDAR) */}
              <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border h-10 items-center shrink-0">
                <button
                  onClick={() => setViewMode('table')}
                  className={`h-8 px-2 sm:px-3 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${
                    viewMode === 'table' 
                      ? 'bg-white dark:bg-brand-card text-amber-700 dark:text-gold-400 shadow-sm border border-slate-200/60 dark:border-brand-border' 
                      : 'text-slate-500 hover:text-slate-800 dark:hover:text-gray-200'
                  }`}
                  title="Liste Görünümü"
                >
                  <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="8" y1="6" x2="21" y2="6"/>
                    <line x1="8" y1="12" x2="21" y2="12"/>
                    <line x1="8" y1="18" x2="21" y2="18"/>
                    <line x1="3" y1="6" x2="3.01" y2="6"/>
                    <line x1="3" y1="12" x2="3.01" y2="12"/>
                    <line x1="3" y1="18" x2="3.01" y2="18"/>
                  </svg>
                  <span className="hidden md:inline">Liste</span>
                </button>

                <button
                  onClick={() => setViewMode('calendar')}
                  className={`h-8 px-2 sm:px-3 rounded-lg text-xs font-bold transition flex items-center space-x-1 ${
                    viewMode === 'calendar' 
                      ? 'bg-white dark:bg-brand-card text-amber-700 dark:text-gold-400 shadow-sm border border-slate-200/60 dark:border-brand-border' 
                      : 'text-slate-500 hover:text-slate-800 dark:hover:text-gray-200'
                  }`}
                  title="Takvim Görünümü"
                >
                  <svg className="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
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
                  <span className="hidden md:inline">Takvim</span>
                </button>
              </div>

            </div>
          </div>

          
          {/* DRAFT / UNCOMPLETED RESERVATIONS DEDICATED PANEL (TOP OF PAGE) */}
          <div className="glass-panel p-5 sm:p-6 rounded-3xl border-2 border-amber-500/40 bg-amber-500/5 dark:bg-amber-950/20 space-y-4 shadow-lg animate-fade-in">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-amber-500/20 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-700 dark:text-gold-400 flex items-center justify-center font-bold text-lg shrink-0">
                  <ThemeIcon icon="sparkles" fallbackEmoji="⏳" className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-heading font-extrabold text-base text-slate-900 dark:text-white flex items-center space-x-2">
                    <span>Tamamlanmamış Taslak Rezervasyonlar</span>
                    <span className="bg-amber-500 text-white font-mono text-xs px-2.5 py-0.5 rounded-full font-bold">
                      {(draftReservations || []).length} Adet
                    </span>
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
                    Form doldurulurken otomatik kaydedilmiş, yarım kalmış veya onay bekleyen taslaklar.
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setIsDraftPanelOpen(!isDraftPanelOpen)}
                className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline inline-flex items-center space-x-1 shrink-0 cursor-pointer"
              >
                <span>{isDraftPanelOpen ? 'Taslak Paneli Gizle ▲' : 'Taslak Paneli Göster ▼'}</span>
              </button>
            </div>

            {isDraftPanelOpen && (
              <>
                {(!draftReservations || draftReservations.length === 0) ? (
                  <div className="bg-white/60 dark:bg-brand-dark/40 p-4 rounded-2xl border border-dashed border-amber-500/30 text-center space-y-2">
                    <p className="text-xs text-slate-600 dark:text-gray-300 font-semibold">
                      Henüz yarım kalmış bir taslak rezervasyonunuz bulunmuyor.
                    </p>
                    <button
                      type="button"
                      onClick={() => navigateTo && navigateTo('create-reservation')}
                      className="gold-button font-bold text-xs px-3.5 py-1.5 rounded-xl shadow-sm inline-flex items-center space-x-1 cursor-pointer"
                    >
                      <ThemeIcon icon="plus" fallbackEmoji="" className="w-3.5 h-3.5 mr-1" />
                      <span>Yeni Rezervasyon Başlat</span>
                    </button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-1">
                    {draftReservations.map((draft, idx) => {
                      const custName = draft.customerInfo?.name || draft.formData?.newCustName || 'İsimsiz Müşteri';
                      const custPhone = draft.customerInfo?.phone || draft.formData?.newCustPhone || '-';
                      const venueName = draft.customerInfo?.venueName || (venues.find(v => v.id === draft.formData?.venueId)?.name) || 'Salon Seçilmedi';
                      const eventDate = draft.customerInfo?.date || draft.formData?.startDate || 'Tarih Belirtilmedi';
                      const percentage = draft.completionPercentage || 0;
                      const updatedAtFormatted = draft.updatedAt ? new Date(draft.updatedAt).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : '-';
                      const lastLogger = draft.accessLogs && draft.accessLogs.length > 0 ? draft.accessLogs[draft.accessLogs.length - 1].userName : 'Sistem';

                      return (
                        <div key={draft.refKey || idx} className="bg-white dark:bg-brand-card border border-amber-500/30 rounded-2xl p-4 space-y-3 shadow-md hover:shadow-lg transition flex flex-col justify-between">
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="font-mono text-xs font-extrabold bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/30 px-2.5 py-1 rounded-lg inline-flex items-center">
                                <ThemeIcon icon="shield" fallbackEmoji="🔑" className="w-3.5 h-3.5 mr-1 shrink-0 text-amber-600 dark:text-gold-400" />
                                <span>{draft.refKey}</span>
                              </span>
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-gold-400">
                                TASLAK (%{percentage})
                              </span>
                            </div>

                            <div>
                              <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-1.5">
                                <ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 text-amber-700 dark:text-gold-400 shrink-0" />
                                <span>{custName}</span>
                              </h4>
                              <p className="text-xs text-slate-500 dark:text-gray-400 font-mono mt-0.5 flex items-center space-x-1">
                                <ThemeIcon icon="phone" fallbackEmoji="📞" className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                                <span>{custPhone}</span>
                              </p>
                            </div>

                            <div className="text-xs text-slate-600 dark:text-gray-300 space-y-1 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border">
                              <div className="flex justify-between items-center">
                                <span className="text-slate-400">Salon:</span>
                                <span className="font-semibold">{venueName}</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-slate-400">Tarih:</span>
                                <span className="font-semibold">{eventDate}</span>
                              </div>
                              <div className="flex justify-between items-center text-[11px] pt-1 border-t border-slate-200/50 dark:border-brand-border">
                                <span className="text-slate-400">Son İşlem:</span>
                                <span className="font-mono">{updatedAtFormatted} ({lastLogger})</span>
                              </div>
                            </div>

                            <div>
                              <div className="flex justify-between text-[10px] font-bold text-slate-500 mb-1">
                                <span>Form Doluluğu</span>
                                <span>%{percentage}</span>
                              </div>
                              <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                                <div
                                  className="bg-amber-500 h-full rounded-full transition-all duration-500"
                                  style={{ width: `${percentage}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>

                          <div className="pt-2 flex items-center gap-2 border-t border-slate-100 dark:border-brand-border">
                            <button
                              type="button"
                              onClick={() => {
                                window.location.hash = `#/rezervasyon-olustur?ref=${draft.refKey}`;
                                if (navigateTo) navigateTo('create-reservation', { ref: draft.refKey });
                              }}
                              className="flex-1 gold-button font-bold py-2.5 px-3 rounded-xl text-xs shadow text-center flex items-center justify-center space-x-1.5 cursor-pointer"
                            >
                              <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                              <span>Devam Et & Tamamla</span>
                            </button>
                            
                            <button
                              type="button"
                              onClick={() => {
                                if (window.confirm(`${draft.refKey} referanslı taslağı silmek istediğinize emin misiniz?`)) {
                                  if (setDraftReservations) {
                                    setDraftReservations(prev => prev.filter(d => d.refKey !== draft.refKey));
                                  }
                                }
                              }}
                              className="p-2.5 bg-red-100 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-200 rounded-xl text-xs transition flex items-center justify-center cursor-pointer"
                              title="Taslağı Sil"
                            >
                              <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            )}
          </div>


          {/* COLLAPSIBLE FILTER PANEL */}
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
                    <option value="ALL">Tüm Salonlar ({(venues || []).length})</option>
                    {(venues || []).map(v => (
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
                    <option value="ALL">Tüm Durumlar ({(reservations || []).length})</option>
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

          {/* VIEW SWITCHER: TABLE OR MASTER CALENDAR */}
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
                        const vObj = (venues || []).find(v => v.id === res.venueId);
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
                              {res.paymentStatus === 'Tamamlandı' || res.paymentStatus === 'Ödendi' ? (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 shadow-xs">
                                  <ThemeIcon icon="check-circle" fallbackEmoji="✅" className="w-3.5 h-3.5 mr-1 shrink-0 text-emerald-600 dark:text-emerald-400" />
                                  <span>Ödeme Tamamlandı</span>
                                </span>
                              ) : res.paymentStatus === 'Kapora Alındı' ? (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-500/15 text-amber-800 dark:text-gold-400 border border-amber-500/40 shadow-xs">
                                  <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-3.5 h-3.5 mr-1 shrink-0 text-amber-600 dark:text-gold-400" />
                                  <span>Kapora Alındı</span>
                                </span>
                              ) : res.paymentStatus === 'İptal' ? (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold bg-rose-500/15 text-rose-700 dark:text-rose-300 border border-rose-500/30 shadow-xs">
                                  <ThemeIcon icon="x-circle" fallbackEmoji="❌" className="w-3.5 h-3.5 mr-1 shrink-0 text-rose-600 dark:text-rose-400" />
                                  <span>İptal Edildi</span>
                                </span>
                              ) : (
                                <span className="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold bg-blue-500/15 text-blue-800 dark:text-blue-300 border border-blue-500/30 shadow-xs">
                                  <ThemeIcon icon="clock" fallbackEmoji="🕒" className="w-3.5 h-3.5 mr-1 shrink-0 text-blue-600 dark:text-blue-400" />
                                  <span>{res.paymentStatus || 'Ödeme Bekliyor'}</span>
                                </span>
                              )}
                            </td>
                            <td className="py-3.5 px-3 text-right">
                              <div className="flex items-center justify-end space-x-1.5">
                                <button
                                  onClick={() => setSelectedResForPreview(res)}
                                  className="px-2 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 hover:bg-amber-500/20 transition font-bold text-xs flex items-center space-x-1"
                                  title="Detaylı Önizle"
                                >
                                  <ThemeIcon icon="preview" fallbackEmoji="👁️" className="w-3.5 h-3.5 shrink-0" />
                                </button>
                                <button
                                  onClick={() => handleOpenEdit(res)}
                                  className="px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold text-xs hover:bg-amber-500/30 transition flex items-center space-x-1"
                                >
                                  <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                                  <span>Düzenle</span>
                                </button>
                                <button
                                  onClick={() => setDeletingRes(res)}
                                  className="px-2.5 py-1 rounded-lg bg-red-500/15 hover:bg-red-500/25 text-red-600 dark:text-red-400 font-bold text-xs transition flex items-center space-x-1 border border-red-500/20"
                                  title="Rezervasyonu Sil"
                                >
                                  <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0 text-red-600 dark:text-red-400" />
                                  <span>Sil</span>
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
            /* INTERACTIVE MONTHLY CALENDAR VIEW (FULL 31-DAY AUG 2026 GRID MATCHING USER SCREENSHOT) */
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
                  <span>Günün üzerine tıklayarak tüm salon doluluklarını inceleyebilir veya kartı sürükleyerek başka güne taşıyabilirsiniz.</span>
                </div>
              </div>

              {/* MONTH TITLE & NAVIGATION TOOLBAR */}
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
                      <ThemeIcon icon="target" fallbackEmoji="🎯" className="w-3.5 h-3.5 shrink-0" />
                      <span className="hidden sm:inline">Bugünkü Ay ({MONTH_NAMES[today.getMonth()]} {today.getFullYear()})</span>
                    </button>
                  </div>
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

          {/* HOURLY TIMELINE SCHEDULE FLOW MODAL (GÜNE TIKLAYINCA SAAT AKIŞI GÖRÜNÜMÜ) */}
          {selectedDayInspector && createPortal(
            <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
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
                      selectedDayInspector.userReservations.map(r => {
                        const vObj = (venues || []).find(v => v.id === r.venueId);
                        const startH = parseInt((r.startTime || '18:00').split(':')[0]) || 18;
                        const endH = parseInt((r.endTime || '23:00').split(':')[0]) || 23;
                        const leftPct = Math.max(0, ((startH - 8) / 16) * 100);
                        const widthPct = Math.min(100 - leftPct, Math.max(10, ((endH - startH) / 16) * 100));

                        return (
                          <div key={r.id} className="space-y-1">
                            <div className="flex justify-between text-[11px] font-bold">
                              <span className="text-slate-800 dark:text-gray-200 flex items-center space-x-1">
                                <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-3.5 h-3.5 shrink-0" />
                                <span>{r.customerName} ({vObj?.name || r.venueId})</span>
                              </span>
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
                      selectedDayInspector.userReservations.map(r => {
                        const vObj = (venues || []).find(v => v.id === r.venueId);
                        return (
                          <div key={r.id} className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                            <div className="flex justify-between items-center font-bold">
                              <span className="text-amber-700 dark:text-gold-400 font-mono">{r.id} - {vObj?.name || r.venueId}</span>
                              <span className="text-emerald-600 font-mono font-extrabold">{r.startTime || '18:00'} - {r.endTime || '23:00'}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="font-extrabold text-sm text-slate-900 dark:text-white flex items-center space-x-1">
                                <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-4 h-4 shrink-0" />
                                <span>{r.customerName} ({r.guestCount} Kişi)</span>
                              </span>
                              <span className="font-mono font-bold text-amber-600">{formatCurrency(r.totalAmount)}</span>
                            </div>
                            <div className="flex justify-end space-x-2 pt-1 border-t border-slate-200 dark:border-brand-border/40">
                              <button
                                onClick={() => setSelectedResForPreview(r)}
                                className="px-3 py-1.5 bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-200 rounded-xl font-bold text-xs inline-flex items-center space-x-1"
                              >
                                <ThemeIcon icon="preview" fallbackEmoji="👁️" className="w-3.5 h-3.5 shrink-0" />
                                <span>Detay Önizle</span>
                              </button>
                              <button
                                onClick={() => handleOpenEdit(r)}
                                className="gold-button px-4 py-1.5 rounded-xl font-bold text-xs shadow inline-flex items-center space-x-1"
                              >
                                <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                                <span>Rezervasyonu Düzenle</span>
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
                    <ThemeIcon icon="plus" fallbackEmoji="" className="w-3.5 h-3.5 inline mr-1.5" /> Bu Tarihe Yeni Rezervasyon Ekle
                  </button>
                  <button onClick={() => setSelectedDayInspector(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl">Kapat</button>
                </div>
              </div>
            </div>,
            document.body
          )}

          {/* 5. RICH DETAILED PREVIEW MODAL */}
          {selectedResForPreview && createPortal(
            <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-3xl w-full p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
                
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
                    <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white mt-1 flex items-center space-x-2">
                      <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>{selectedResForPreview.customerName}</span>
                    </h3>
                  </div>
                  <button onClick={() => setSelectedResForPreview(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center">✕</button>
                </div>

                <div className="space-y-4 text-xs">
                  
                  {/* SECTION A: MÜŞTERİ İLETİŞİM & SALON ZAMAN BİLGİLERİ */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5">
                      <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="user" fallbackEmoji="👤" className="w-3 h-3 inline mr-1" /> Müşteri İletişim Bilgileri:</span>
                      <div className="font-extrabold text-sm text-slate-900 dark:text-white">{selectedResForPreview.customerName}</div>
                      <div><ThemeIcon icon="phone" fallbackEmoji="📞" className="w-3 h-3 inline mr-1" /> Birincil Tel: <strong className="font-mono text-slate-800 dark:text-gray-200">{selectedResForPreview.customerPhone}</strong></div>
                      <div><ThemeIcon icon="mobile" fallbackEmoji="📱" className="w-3 h-3 inline mr-1" /> İkinci Tel: <strong className="font-mono text-slate-800 dark:text-gray-200">{selectedResForPreview.customerSecondaryPhone || 'İkinci Tel Belirtilmedi'}</strong></div>
                      <div><ThemeIcon icon="email" fallbackEmoji="✉️" className="w-3 h-3 inline mr-1" /> E-Posta: <strong className="text-slate-800 dark:text-gray-200">{selectedResForPreview.customerEmail || 'E-Posta Girilmedi'}</strong></div>
                    </div>

                    <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5">
                      <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-3 h-3 inline mr-1" /> Etkinlik & Salon Detayı:</span>
                      <div className="font-extrabold text-sm text-slate-900 dark:text-white">
                        {(venues.find(v => v.id === selectedResForPreview.venueId))?.name || selectedResForPreview.venueId}
                      </div>
                      <div><ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-3 h-3 inline mr-1" /> Tarih: <strong className="font-mono text-slate-800 dark:text-gray-200">{formatDate(selectedResForPreview.eventDate || selectedResForPreview.date)}</strong></div>
                      <div><ThemeIcon icon="clock" fallbackEmoji="⏰" className="w-3 h-3 inline mr-1" /> Saat Aralığı: <strong className="font-mono text-emerald-600">{selectedResForPreview.startTime || '18:00'} - {selectedResForPreview.endTime || '23:00'}</strong></div>
                      <div><ThemeIcon icon="users" fallbackEmoji="👥" className="w-3 h-3 inline mr-1" /> Davetli Sayısı: <strong className="text-slate-800 dark:text-gray-200">{selectedResForPreview.guestCount} Davetli Kişi</strong></div>
                    </div>
                  </div>

                  {/* SECTION B: DÜĞÜN AKIŞ PLANLAMASI (HANGİ BİLGİLER / AKIŞ VERİLDİ) */}
                  <div className="bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="document" fallbackEmoji="📜" className="w-3 h-3 inline mr-1" /> Organizasyon & Zaman Akış Programı:</span>
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
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="gift" fallbackEmoji="" className="w-3 h-3 inline mr-1" /> Verilen Hizmetler & Dahili Paketler:</span>
                    {(!selectedResForPreview.selectedServices || selectedResForPreview.selectedServices.length === 0) ? (
                      <div className="text-slate-400 italic">Dahili temel salon paketi dâhildir. Ek paket seçilmedi.</div>
                    ) : (
                      <div className="flex flex-wrap gap-2">
                        {selectedResForPreview.selectedServices.map((srvItem, sIdx) => {
                          const serviceId = typeof srvItem === 'string' ? srvItem : (srvItem?.serviceId || srvItem?.id);
                          const sObj = services.find(s => s.id === serviceId);
                          const displayName = sObj?.name || (typeof srvItem === 'object' ? (srvItem.name || serviceId || 'Ek Hizmet') : String(srvItem));
                          const displayPrice = (typeof srvItem === 'object' && srvItem.customUnitPrice !== undefined) 
                            ? srvItem.customUnitPrice 
                            : (sObj?.price || (typeof srvItem === 'object' ? (srvItem.price || srvItem.unitPrice || 0) : 0));

                          return (
                            <span key={sIdx} className="bg-white dark:bg-brand-card border border-amber-500/30 px-3 py-1.5 rounded-xl font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1 shadow-xs">
                              <span>🎁</span>
                              <span>{displayName}</span>
                              {displayPrice ? <span className="font-mono text-amber-600 text-[10px]">({formatCurrency(displayPrice)})</span> : null}
                            </span>
                          );
                        })}
                      </div>
                    )}
                  </div>

                  {/* SECTION D: ÖDEMELER NE DURUMDA & HANGİLERİNİN ÖDEMELERİ YAPILDI */}
                  <div className="bg-amber-50/60 dark:bg-amber-950/20 p-4 rounded-2xl border border-amber-300 dark:border-amber-700/50 space-y-3">
                    <span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider"><ThemeIcon icon="money" fallbackEmoji="💰" className="w-3 h-3 inline mr-1" /> Detaylı Ödeme Durumları & Finansal Döküm:</span>
                    
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
                      <span className="font-bold block text-slate-800 dark:text-gray-200"><ThemeIcon icon="card" fallbackEmoji="💳" className="w-3 h-3 inline mr-1" /> Gerçekleşen Ödemeler Geçmişi:</span>
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
                      <span className="text-slate-400 font-bold block"><ThemeIcon icon="note" fallbackEmoji="📝" className="w-3 h-3 inline mr-1" /> Operasyonel Notlar & Özel İstekler:</span>
                      <p className="text-slate-700 dark:text-gray-300 italic">{selectedResForPreview.notes}</p>
                    </div>
                  )}

                </div>

                {/* PREVIEW ACTIONS */}
                <div className="pt-2 border-t border-slate-200 dark:border-brand-border flex justify-between items-center gap-2">
                  <div className="flex space-x-2">
                    {onPrintInvoice && (
                      <button onClick={() => onPrintInvoice(selectedResForPreview)} className="bg-slate-800 text-white px-3 py-2 rounded-xl font-bold text-xs inline-flex items-center space-x-1">
                        <ThemeIcon icon="document" fallbackEmoji="📄" className="w-3.5 h-3.5 shrink-0" />
                        <span>Fatura Yazdır</span>
                      </button>
                    )}
                    {onShowEmail && (
                      <button onClick={() => onShowEmail(selectedResForPreview)} className="bg-emerald-600 text-white px-3 py-2 rounded-xl font-bold text-xs inline-flex items-center space-x-1">
                        <ThemeIcon icon="email" fallbackEmoji="✉️" className="w-3.5 h-3.5 shrink-0" />
                        <span>E-Posta Önizle</span>
                      </button>
                    )}
                  </div>

                  <div className="flex space-x-2">
                    <button onClick={() => setSelectedResForPreview(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl text-xs font-bold">Kapat</button>
                    <button
                      onClick={() => { handleOpenEdit(selectedResForPreview); setSelectedResForPreview(null); }}
                      className="gold-button font-bold px-5 py-2 rounded-xl text-xs shadow inline-flex items-center space-x-1"
                    >
                      <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                      <span>Rezervasyonu Düzenle</span>
                    </button>
                  </div>
                </div>

              </div>
            </div>,
            document.body
          )}

          {/* DELETE CONFIRMATION MODAL */}
          {deletingRes && createPortal(
            <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border-2 border-red-500/60 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl animate-fade-in text-center my-auto">
                <div className="w-12 h-12 rounded-2xl bg-red-500/20 text-red-600 dark:text-red-400 flex items-center justify-center text-2xl font-bold mx-auto border border-red-500/30">
                  <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-6 h-6 shrink-0 text-red-600 dark:text-red-400" />
                </div>
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
            </div>,
            document.body
          )}

          {/* 7. FULL EDIT RESERVATION MODAL (REZERVASYON OLUŞTURURKEN YAPILABİLEN HER ŞEYİ DÜZENLEME) */}
          {editingRes && editForm && createPortal(
            <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/50 rounded-3xl max-w-4xl w-full p-5 sm:p-6 space-y-5 shadow-2xl animate-fade-in max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
                
                {/* EDIT HEADER */}
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <div>
                    <span className="text-[10px] font-bold text-amber-600 uppercase font-mono">Sözleşme Düzenleme Modu — ID: {editForm.id}</span>
                    <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-white mt-0.5 flex items-center space-x-1.5">
                      <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Rezervasyon Tüm Bilgilerini Düzenle</span>
                    </h3>
                  </div>
                  <button onClick={() => setEditingRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold text-xs hover:bg-red-500 hover:text-white transition">✕</button>
                </div>

                <div className="space-y-5 text-xs">
                  
                  {/* SECTION 1: SALON & KAPASİTE BİLGİLERİ */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider flex items-center space-x-1">
                      <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-3.5 h-3.5 shrink-0" />
                      <span>1. Salon & Kapasite Seçimi:</span>
                    </span>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Düğün Salonu:</label>
                        <select
                          value={editForm.venueId}
                          onChange={e => {
                            const vId = e.target.value;
                            const vObj = (venues || []).find(v => v.id === vId);
                            setEditForm({
                              ...editForm,
                              venueId: vId,
                              venuePrice: vObj?.price || editForm.venuePrice || 85000
                            });
                          }}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        >
                          {(venues || []).map(v => <option key={v.id} value={v.id}>{v.name} ({formatCurrency(v.price || 0)})</option>)}
                        </select>
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Özel Salon Bedeli (TL):</label>
                        <input
                          type="number"
                          value={editForm.venuePrice || 0}
                          onChange={e => setEditForm({ ...editForm, venuePrice: Number(e.target.value) })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-amber-600 font-mono"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Davetli Sayısı (Kişi):</label>
                        <input
                          type="number"
                          value={editForm.guestCount || 0}
                          onChange={e => setEditForm({ ...editForm, guestCount: Number(e.target.value) })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        />
                      </div>
                    </div>
                  </div>

                  {/* SECTION 2: TARİH, SEANS & SAAT DÜZENLEME */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider flex items-center space-x-1">
                        <ThemeIcon icon="clock" fallbackEmoji="⏰" className="w-3.5 h-3.5 shrink-0" />
                        <span>2. Etkinlik Tarihi & Hızlı Seans Seçimi:</span>
                      </span>
                      
                      {/* HIZLI SEANS BUTONLARI */}
                      <div className="flex gap-1">
                        <button
                          type="button"
                          onClick={() => setEditForm({ ...editForm, startTime: '12:00', endTime: '17:00' })}
                          className="px-2 py-1 bg-amber-500/10 hover:bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold rounded-lg text-[10px]"
                        >
                          ☀️ Gündüz (12-17)
                        </button>
                        <button
                          type="button"
                          onClick={() => setEditForm({ ...editForm, startTime: '18:00', endTime: '23:00' })}
                          className="px-2 py-1 bg-purple-500/10 hover:bg-purple-500/20 text-purple-700 dark:text-purple-300 font-bold rounded-lg text-[10px]"
                        >
                          🌙 Gece (18-23)
                        </button>
                        <button
                          type="button"
                          onClick={() => setEditForm({ ...editForm, startTime: '09:00', endTime: '23:30' })}
                          className="px-2 py-1 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-700 dark:text-emerald-300 font-bold rounded-lg text-[10px] flex items-center space-x-1"
                        >
                          <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-3 h-3 shrink-0" />
                          <span>Tüm Gün</span>
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Etkinlik Tarihi:</label>
                        <input
                          type="date"
                          value={editForm.startDate || editForm.eventDate || editForm.date || ''}
                          onChange={e => setEditForm({ ...editForm, startDate: e.target.value, eventDate: e.target.value, date: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold font-mono"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Başlangıç Saati:</label>
                        <input
                          type="time"
                          value={editForm.startTime || '18:00'}
                          onChange={e => setEditForm({ ...editForm, startTime: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold font-mono"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Bitiş Saati:</label>
                        <input
                          type="time"
                          value={editForm.endTime || '23:00'}
                          onChange={e => setEditForm({ ...editForm, endTime: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold font-mono"
                        />
                      </div>
                    </div>
                  </div>

                  {/* SECTION 3: EK HİZMETLER & DAHİLİ PAKET DÜZENLEYİCİ */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🎁 3. Ek Hizmetler & Dahili Paket Seçimi:</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                      {(services || []).map(srv => {
                        const isSelected = (editForm.selectedServices || []).some(s => (typeof s === 'string' ? s === srv.id : s.serviceId === srv.id || s.id === srv.id));
                        return (
                          <label
                            key={srv.id}
                            className={`p-3 rounded-xl border flex items-center justify-between cursor-pointer transition ${
                              isSelected 
                                ? 'bg-amber-500/10 border-amber-500/50 dark:bg-amber-950/30' 
                                : 'bg-white dark:bg-brand-card border-slate-200 dark:border-brand-border hover:border-slate-300'
                            }`}
                          >
                            <div className="flex items-center space-x-2.5">
                              <input
                                type="checkbox"
                                checked={isSelected}
                                onChange={e => {
                                  let current = [...(editForm.selectedServices || [])];
                                  if (e.target.checked) {
                                    current.push({ serviceId: srv.id, name: srv.name, customUnitPrice: srv.price, quantity: 1 });
                                  } else {
                                    current = current.filter(s => (typeof s === 'string' ? s !== srv.id : (s.serviceId || s.id) !== srv.id));
                                  }
                                  setEditForm({ ...editForm, selectedServices: current });
                                }}
                                className="w-4 h-4 rounded text-amber-600"
                              />
                              <div>
                                <div className="font-bold text-slate-800 dark:text-gray-100 text-xs">{srv.name}</div>
                                <div className="text-[10px] text-slate-400">{srv.category || 'Ek Paket'}</div>
                              </div>
                            </div>
                            <span className="font-mono font-bold text-amber-600 text-xs">{formatCurrency(srv.price || 0)}</span>
                          </label>
                        );
                      })}
                    </div>
                  </div>

                  {/* SECTION 4: KAMPANYA & İNDİRİM KODU */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">🏷️ 4. Özel Kampanya & İndirim Kodu:</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Aktif Kampanya Uygula:</label>
                        <select
                          value={editForm.campaignCode || ''}
                          onChange={e => {
                            const code = e.target.value;
                            const cmp = (campaigns || []).find(c => c.code === code);
                            setEditForm({
                              ...editForm,
                              campaignCode: code,
                              discountAmount: cmp ? cmp.discountValue : editForm.discountAmount || 0
                            });
                          }}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        >
                          <option value="">Kampanya Seçilmedi (İndirimsiz)</option>
                          {(campaigns || []).map(c => (
                            <option key={c.id || c.code} value={c.code}>
                              {c.code} - {c.title} ({formatCurrency(c.discountValue)})
                            </option>
                          ))}
                        </select>
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Özel İndirim Tutarı (TL):</label>
                        <input
                          type="number"
                          value={editForm.discountAmount || 0}
                          onChange={e => setEditForm({ ...editForm, discountAmount: Number(e.target.value) })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-red-500 font-mono"
                        />
                      </div>
                    </div>
                  </div>

                  {/* SECTION 5: MÜŞTERİ İLETİŞİM, ADRES & FATURA BİLGİLERİ */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider">👤 5. Müşteri İletişim, Adres & Fatura Bilgileri:</span>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Müşteri / Çift Adı Soyadı <span className="text-red-500">*</span>:</label>
                        <input
                          type="text"
                          value={editForm.customerName || ''}
                          onChange={e => setEditForm({ ...editForm, customerName: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">E-posta Adresi:</label>
                        <input
                          type="email"
                          value={editForm.customerEmail || ''}
                          onChange={e => setEditForm({ ...editForm, customerEmail: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Birincil Telefon <span className="text-red-500">*</span>:</label>
                        <input
                          type="text"
                          value={editForm.customerPhone || ''}
                          onChange={e => setEditForm({ ...editForm, customerPhone: formatPhoneNumber(e.target.value) })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold font-mono"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">İkinci İletişim Telefonu:</label>
                        <input
                          type="text"
                          value={editForm.customerSecondaryPhone || ''}
                          onChange={e => setEditForm({ ...editForm, customerSecondaryPhone: formatPhoneNumber(e.target.value) })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold font-mono"
                        />
                      </div>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Fatura Türü:</label>
                        <select
                          value={editForm.taxType || 'Bireysel'}
                          onChange={e => setEditForm({ ...editForm, taxType: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        >
                          <option value="Bireysel">Bireysel (TC Kimlik)</option>
                          <option value="Kurumsal">Kurumsal (Şirket VKN)</option>
                        </select>
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">TC No / VKN No:</label>
                        <input
                          type="text"
                          value={editForm.tcNo || editForm.vknNo || ''}
                          onChange={e => setEditForm({ ...editForm, tcNo: e.target.value, vknNo: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold"
                          placeholder="11 haneli TC veya VKN"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Vergi Dairesi:</label>
                        <input
                          type="text"
                          value={editForm.taxOffice || ''}
                          onChange={e => setEditForm({ ...editForm, taxOffice: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                          placeholder="Örn: Sakarya VD"
                        />
                      </div>
                    </div>
                  </div>

                  {/* SECTION 6: FİNANS, KAPORA & FATURA KESİLDİ BİLGİSİ */}
                  <div className="p-4 bg-amber-50/60 dark:bg-amber-950/20 rounded-2xl border border-amber-300 dark:border-amber-700/50 space-y-3">
                    <span className="text-amber-900 dark:text-amber-300 font-bold block text-[11px] uppercase tracking-wider">💰 6. Finans, Kapora, Ödeme Statüsü & Fatura Kesildi Bilgisi:</span>
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Tahsil Edilen Kapora (TL):</label>
                        <input
                          type="number"
                          value={editForm.depositPaid || 0}
                          onChange={e => {
                            const dep = Number(e.target.value);
                            const venueCost = Number(editForm.venuePrice || 85000);
                            const srvCost = (editForm.selectedServices || []).reduce((sum, s) => {
                              const p = typeof s === 'object' ? (s.customUnitPrice || s.price || 5000) : 5000;
                              return sum + p;
                            }, 0);
                            const disc = Number(editForm.discountAmount || 0);
                            const tot = Math.max(0, venueCost + srvCost - disc);
                            const rem = Math.max(0, tot - dep);
                            setEditForm({
                              ...editForm,
                              depositPaid: dep,
                              totalAmount: tot,
                              remainingBalance: rem,
                              paymentStatus: rem === 0 ? 'Ödendi' : dep > 0 ? 'Kapora Alındı' : 'Bekliyor'
                            });
                          }}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-emerald-600 font-mono"
                        />
                      </div>
                      <div>
                        <label className="font-bold block mb-1 text-slate-700 dark:text-gray-200">Ödeme Durumu:</label>
                        <select
                          value={editForm.paymentStatus || 'Bekliyor'}
                          onChange={e => setEditForm({ ...editForm, paymentStatus: e.target.value })}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                        >
                          <option value="Bekliyor">Bekliyor (Ödeme Bekleniyor)</option>
                          <option value="Kapora Alındı">Kapora Alındı</option>
                          <option value="Ödendi">Ödendi / Tamamlandı</option>
                        </select>
                      </div>
                      <div className="flex items-center pt-5">
                        <label className="flex items-center space-x-2 cursor-pointer font-bold bg-white dark:bg-brand-card p-2.5 rounded-xl border border-slate-200 dark:border-brand-border w-full">
                          <input
                            type="checkbox"
                            checked={editForm.isInvoiced || false}
                            onChange={e => setEditForm({ ...editForm, isInvoiced: e.target.checked })}
                            className="w-4 h-4 rounded text-amber-600"
                          />
                          <span className="text-slate-800 dark:text-gray-200">📄 Faturası Kesildi mi?</span>
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* SECTION 7: DÜĞÜN & ETKİNLİK AKIŞ PLANLAMASI */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider flex items-center space-x-1">
                        <ThemeIcon icon="flow" fallbackEmoji="📜" className="w-3.5 h-3.5 shrink-0" />
                        <span>7. Düğün & Etkinlik Akış Planlaması:</span>
                      </span>
                      <button
                        type="button"
                        onClick={() => {
                          const newPlan = [...(editForm.flowPlan || [])];
                          newPlan.push({ time: '20:00', title: 'Yeni Akış Maddesi', description: 'Açıklama giriniz', responsible: 'Müdür' });
                          setEditForm({ ...editForm, flowPlan: newPlan });
                        }}
                        className="px-2.5 py-1 bg-amber-500/20 text-amber-800 dark:text-gold-400 font-bold rounded-lg text-[11px] hover:bg-amber-500/30 transition flex items-center space-x-1"
                      >
                        <ThemeIcon icon="plus" fallbackEmoji="" className="w-3 h-3 shrink-0" />
                        <span>Yeni Akış Maddesi Ekle</span>
                      </button>
                    </div>

                    <div className="space-y-2">
                      {(!editForm.flowPlan || editForm.flowPlan.length === 0) ? (
                        <div className="text-slate-400 italic text-[11px]">Akış planı eklenmedi. Yukarıdaki butonla yeni saat maddesi ekleyebilirsiniz.</div>
                      ) : (
                        editForm.flowPlan.map((step, idx) => (
                          <div key={idx} className="flex gap-2 items-center bg-white dark:bg-brand-card p-2 rounded-xl border border-slate-200 dark:border-brand-border">
                            <input
                              type="time"
                              value={step.time || '18:00'}
                              onChange={e => {
                                const updated = [...editForm.flowPlan];
                                updated[idx].time = e.target.value;
                                setEditForm({ ...editForm, flowPlan: updated });
                              }}
                              className="w-24 bg-slate-50 dark:bg-brand-dark p-1 rounded font-mono font-bold text-[11px] border"
                            />
                            <input
                              type="text"
                              placeholder="Akış Başlığı"
                              value={step.title || ''}
                              onChange={e => {
                                const updated = [...editForm.flowPlan];
                                updated[idx].title = e.target.value;
                                setEditForm({ ...editForm, flowPlan: updated });
                              }}
                              className="flex-1 bg-slate-50 dark:bg-brand-dark p-1 rounded font-bold text-[11px] border"
                            />
                            <button
                              type="button"
                              onClick={() => {
                                const updated = editForm.flowPlan.filter((_, i) => i !== idx);
                                setEditForm({ ...editForm, flowPlan: updated });
                              }}
                              className="text-red-500 font-bold px-2 py-1 hover:bg-red-50 rounded text-xs"
                            >
                              ✕
                            </button>
                          </div>
                        ))
                      )}
                    </div>
                  </div>

                  {/* SECTION 8: OPERASYONEL NOTLAR */}
                  <div className="p-4 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border space-y-2">
                    <span className="text-amber-700 dark:text-gold-400 font-bold block text-[11px] uppercase tracking-wider flex items-center space-x-1">
                      <ThemeIcon icon="notes" fallbackEmoji="📝" className="w-3.5 h-3.5 shrink-0" />
                      <span>8. Operasyonel Ek Notlar & Özel İstekler:</span>
                    </span>
                    <textarea
                      rows="3"
                      value={editForm.notes || ''}
                      onChange={e => setEditForm({ ...editForm, notes: e.target.value })}
                      placeholder="Müşterinin özel istekleri, organizasyon detayları..."
                      className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-medium"
                    />
                  </div>

                </div>

                {/* EDIT MODAL FOOTER */}
                <div className="pt-3 border-t flex justify-between items-center text-xs font-bold">
                  {editError && (
                    <span className="text-red-500 font-bold flex items-center space-x-1">
                      <ThemeIcon icon="warning" fallbackEmoji="⚠️" className="w-3.5 h-3.5 shrink-0 text-red-500" />
                      <span>Müşteri adı ve telefonu zorunludur!</span>
                    </span>
                  )}
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
                      className="gold-button px-6 py-2.5 rounded-xl shadow inline-flex items-center space-x-1.5"
                    >
                      <ThemeIcon icon="check" fallbackEmoji="💾" className="w-4 h-4 shrink-0" />
                      <span>Değişiklikleri Kaydet</span>
                    </button>
                  </div>
                </div>
              </div>
            </div>,
            document.body
          )}

        </div>
      );
    }

// --- USERS COMPONENT ---
