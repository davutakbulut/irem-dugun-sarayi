import React, { useState, useEffect, useRef } from 'react';
import { formatCurrency, formatDate, formatPhoneNumber, isValidPhoneNumber, calculateReservationTotals } from '../utils/formatters';
import { DEFAULT_FLOW_PLAN } from '../constants/mockData';
import { VenueDetailModalComponent } from '../components/Modals';

export function CreateReservationPage({ venues = [], services = [], customers = [], campaigns = [], reservations = [], prefilledDate, onSaveReservation, onCancel }) {
  const [venueId, setVenueId] = useState(venues[0]?.id || 'v1');
  const [customVenuePrice, setCustomVenuePrice] = useState(venues[0]?.price || 85000);
  const [guestCount, setGuestCount] = useState(500);

  const todayStr = new Date().toISOString().split('T')[0];
  const [startDate, setStartDate] = useState(prefilledDate || todayStr);
  const [endDate, setEndDate] = useState(prefilledDate || todayStr);
  const [startTime, setStartTime] = useState('18:00');
  const [endTime, setEndTime] = useState('23:00');

  const [calendarOffsetDays, setCalendarOffsetDays] = useState(0);

  const preview14Days = React.useMemo(() => {
    const parts = (startDate || todayStr).split('-');
    const selYear = Number(parts[0]) || 2026;
    const selMonth = (Number(parts[1]) || 8) - 1;
    const selDay = Number(parts[2]) || 25;
    const selected = new Date(selYear, selMonth, selDay);

    const dayOfWeek = selected.getDay();
    const distanceToMonday = (dayOfWeek + 6) % 7;
    const monday = new Date(selected);
    monday.setDate(selected.getDate() - distanceToMonday + calendarOffsetDays);

    const days = [];
    for (let i = 0; i < 14; i++) {
      const d = new Date(monday);
      d.setDate(monday.getDate() + i);
      days.push(d);
    }
    return days;
  }, [startDate, calendarOffsetDays, todayStr]);

  const [selectedServices, setSelectedServices] = useState([]); // Default empty [] as requested
  const [campaignCode, setCampaignCode] = useState('');
  const [hasDeposit, setHasDeposit] = useState(true);
  const [depositPaid, setDepositPaid] = useState(15000);
  const [paymentStatus, setPaymentStatus] = useState('Kapora Alındı');

  // Customer Mode & Form
  const [customerMode, setCustomerMode] = useState('new');
  const [selectedCustomerId, setSelectedCustomerId] = useState(customers[0]?.id || '');
  const [customerSearchQuery, setCustomerSearchQuery] = useState('');
  const [newCustName, setNewCustName] = useState('');
  const [newCustPhone, setNewCustPhone] = useState('');
  const [newCustSecondaryPhone, setNewCustSecondaryPhone] = useState('');
  const [newCustEmail, setNewCustEmail] = useState('');
  const [customerError, setCustomerError] = useState(false);

  // Invoice & Notes & Flow
  const [referrerName, setReferrerName] = useState('');
  const [isInvoiced, setIsInvoiced] = useState(false);
  const [invoiceType, setInvoiceType] = useState('individual');
  const [tcNo, setTcNo] = useState('');
  const [vknNo, setVknNo] = useState('');
  const [taxOffice, setTaxOffice] = useState('');
  const [invoiceAddress, setInvoiceAddress] = useState('');
  const [notes, setNotes] = useState('');
  const [flowPlan, setFlowPlan] = useState(DEFAULT_FLOW_PLAN);
  const [draggedIdx, setDraggedIdx] = useState(null);
  const [dragOverIdx, setDragOverIdx] = useState(null);
  const [selectedVenueForDetail, setSelectedVenueForDetail] = useState(null);

  const venueCarouselRef = useRef(null);

  // Carousel Arrow Controls
  const scrollVenueCarouselLeft = () => {
    if (venueCarouselRef.current) {
      venueCarouselRef.current.scrollBy({ left: -280, behavior: 'smooth' });
    }
  };

  const scrollVenueCarouselRight = () => {
    if (venueCarouselRef.current) {
      venueCarouselRef.current.scrollBy({ left: 280, behavior: 'smooth' });
    }
  };

  // Sync venue price on change
  const selectedVenue = venues.find(v => v.id === venueId) || venues[0];
  useEffect(() => {
    if (selectedVenue) {
      setCustomVenuePrice(selectedVenue.price);
    }
  }, [venueId]);

  // Real-time Conflict Detection
  const activeSlot = `${startTime} - ${endTime}`;
  const checkConflict = () => {
    const conflictingRes = reservations.find(r => {
      if (r.venueId !== venueId || r.paymentStatus === 'İptal') return false;
      const resDate = r.eventDate || r.startDate;
      if (resDate === startDate) {
        return true;
      }
      return false;
    });

    return {
      hasConflict: !!conflictingRes,
      conflictingRes
    };
  };

  const conflictInfo = checkConflict();

  // Calculations
  const calculations = calculateReservationTotals({
    venuePrice: customVenuePrice,
    guestCount,
    selectedServices,
    allServices: services,
    campaignCode,
    campaigns,
    isInvoiced,
    hasDeposit,
    depositPaid,
    paymentStatus
  });

  // Flow Plan Actions
  const handleAddFlowItem = () => {
    setFlowPlan(prev => [...prev, { time: '20:00', title: 'Yeni Akış Adımı' }]);
  };

  const handleRemoveFlowItem = (idx) => {
    setFlowPlan(prev => prev.filter((_, i) => i !== idx));
  };

  const moveFlowItemUp = (idx) => {
    if (idx <= 0) return;
    setFlowPlan(prev => {
      const arr = [...prev];
      const temp = arr[idx];
      arr[idx] = arr[idx - 1];
      arr[idx - 1] = temp;
      return arr;
    });
  };

  const moveFlowItemDown = (idx) => {
    if (idx >= flowPlan.length - 1) return;
    setFlowPlan(prev => {
      const arr = [...prev];
      const temp = arr[idx];
      arr[idx] = arr[idx + 1];
      arr[idx + 1] = temp;
      return arr;
    });
  };

  const handleDragStart = (e, idx) => {
    setDraggedIdx(idx);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e, idx) => {
    e.preventDefault();
    if (draggedIdx !== idx) setDragOverIdx(idx);
  };

  const handleDrop = (e, idx) => {
    e.preventDefault();
    if (draggedIdx === null || draggedIdx === idx) return;
    setFlowPlan(prev => {
      const arr = [...prev];
      const draggedItem = arr[draggedIdx];
      arr.splice(draggedIdx, 1);
      arr.splice(idx, 0, draggedItem);
      return arr;
    });
    setDraggedIdx(null);
    setDragOverIdx(null);
  };

  const handleDragEnd = () => {
    setDraggedIdx(null);
    setDragOverIdx(null);
  };

  // Submit Handler
  const handleSubmit = () => {
    if (conflictInfo.hasConflict) {
      alert(`⚠️ ÇAKIŞMA ENGELLENDİ!\n\n${selectedVenue?.name} salonunda ${formatDate(startDate)} tarihinde dolu rezervasyon bulunmaktadır.`);
      return;
    }

    let customerId = selectedCustomerId;
    let customerName = '';
    let customerPhone = '';
    let customerEmail = '';
    let newCustomerObj = null;

    if (customerMode === 'existing') {
      const existingCust = customers.find(c => c.id === selectedCustomerId);
      if (!existingCust) {
        setCustomerError(true);
        return;
      }
      customerName = existingCust.name;
      customerPhone = existingCust.phone;
      customerEmail = existingCust.email;
    } else {
      if (!newCustName.trim() || !newCustPhone.trim() || !isValidPhoneNumber(newCustPhone)) {
        setCustomerError(true);
        return;
      }
      customerId = 'c-' + Date.now();
      customerName = newCustName.trim();
      customerPhone = newCustPhone.trim();
      customerEmail = newCustEmail.trim();

      newCustomerObj = {
        id: customerId,
        name: customerName,
        phone: customerPhone,
        secondaryPhone: newCustSecondaryPhone,
        email: customerEmail,
        tcNo: invoiceType === 'individual' ? tcNo : '',
        address: invoiceAddress,
        totalBookings: 1,
        registryDate: todayStr
      };
    }

    const newRes = {
      id: `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
      venueId,
      customerId,
      customerName,
      customerPhone,
      customerEmail,
      eventDate: startDate,
      startDate,
      endDate,
      startTime,
      endTime,
      timeSlot: activeSlot,
      guestCount: Number(guestCount),
      venuePrice: Number(customVenuePrice),
      selectedServices,
      subtotal: calculations.subtotal,
      campaignCode,
      discountAmount: calculations.discount,
      vatAmount: calculations.vat,
      totalAmount: calculations.grandTotal,
      depositPaid: calculations.dep,
      remainingBalance: calculations.remaining,
      paymentStatus,
      referrerName,
      isInvoiced,
      invoiceType,
      tcNo: invoiceType === 'individual' ? tcNo : '',
      vknNo: invoiceType === 'corporate' ? vknNo : '',
      taxOffice,
      invoiceAddress,
      notes,
      flowPlan
    };

    onSaveReservation(newRes, newCustomerObj);
  };

  // Sync with mobile summary bar
  useEffect(() => {
    if (window.updateMobileReservationSummary) {
      window.updateMobileReservationSummary({
        remaining: calculations.remaining,
        isFullyPaid: calculations.isFullyPaid,
        calculations,
        isInvoiced,
        paymentStatus,
        hasDeposit,
        hasConflict: conflictInfo.hasConflict,
        onSubmit: handleSubmit
      });
    }
  }, [calculations, isInvoiced, paymentStatus, hasDeposit, conflictInfo, handleSubmit]);

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-24 sm:pb-12 relative animate-fade-in">
      
      {/* VENUE DETAIL POPUP MODAL */}
      {selectedVenueForDetail && (
        <VenueDetailModalComponent
          venue={selectedVenueForDetail}
          onClose={() => setSelectedVenueForDetail(null)}
          onSelectVenue={(v) => {
            setVenueId(v.id);
            setCustomVenuePrice(v.price);
          }}
        />
      )}

      {/* PAGE HEADER */}
      <div className="glass-panel p-4 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
        <div className="flex flex-col items-start gap-1">
          <span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border">
            <svg className="w-3.5 h-3.5 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
            <span>Rezervasyon Oluşturma & Kiralama</span>
          </span>
          <h1 className="font-heading font-extrabold text-xl sm:text-2xl text-slate-900 dark:text-white tracking-tight mt-1">
            Hayalinizdeki Düğünü Birlikte Planlayalım!
          </h1>
          <p className="text-[11px] sm:text-xs text-slate-500 dark:text-gray-400">Salon kiralama, hizmet adetleri, müşteri üyelik kaydı, fatura ve etkinlik akışını tek ekranda yönetin.</p>
        </div>
        <button onClick={onCancel} className="w-full sm:w-auto px-4 py-2.5 bg-slate-100 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-200 text-center whitespace-nowrap shrink-0">
          ← Rezervasyon Listesine Dön
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* LEFT COLUMN: FORM SECTIONS (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          
          {/* SECTION 1: DÜĞÜN SALONU SEÇİN (TAKVİM & SEANS SEÇİMİ İLE) */}
          <div className="glass-panel p-3.5 sm:p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">

            {/* VISUAL HORIZONTAL SCROLLABLE VENUE CAROUSEL WITH ARROW CONTROLS */}
            <div>
              <div className="flex justify-between items-center mb-2 px-1">
                <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0h4m-4 0V11m0 0h4m-4 0H7m4 0v5"></path></svg>
                  <span>1. Düğün Salonu Seçin:</span>
                </h3>
                
                {/* Interactive Arrow Navigation Buttons */}
                <div className="flex items-center space-x-1.5">
                  <button
                    type="button"
                    onClick={scrollVenueCarouselLeft}
                    className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                    title="Sola Kaydır"
                    aria-label="Salonları Sola Kaydır"
                  >
                    ❮
                  </button>
                  <button
                    type="button"
                    onClick={scrollVenueCarouselRight}
                    className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                    title="Sağa Kaydır"
                    aria-label="Salonları Sağa Kaydır"
                  >
                    ❯
                  </button>
                </div>
              </div>

              <div ref={venueCarouselRef} className="flex overflow-x-auto gap-3.5 pb-3 pt-1 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                {venues.map(v => {
                  const isSelected = venueId === v.id;
                  return (
                    <div
                      key={v.id}
                      onClick={() => {
                        setVenueId(v.id);
                        setCustomVenuePrice(v.price);
                      }}
                      className={`shrink-0 w-64 sm:w-68 rounded-2xl border-2 transition-all duration-300 cursor-pointer overflow-hidden snap-start flex flex-col justify-between shadow-sm ${
                        isSelected
                          ? 'border-slate-800 dark:border-white bg-slate-100/80 dark:bg-brand-dark shadow-md ring-2 ring-slate-800/40 dark:ring-white/40'
                          : 'border-slate-200 dark:border-brand-border bg-white dark:bg-brand-card hover:border-slate-400'
                      }`}
                    >
                      <div className="relative h-32 sm:h-36 w-full bg-slate-200 dark:bg-brand-dark overflow-hidden shrink-0">
                        <img src={v.image} alt={v.name} className="w-full h-full object-cover" />
                        
                        <div className="absolute top-2 right-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-bold px-2 py-0.5 rounded-full border border-white/20 z-10 flex items-center space-x-1">
                          <span>{v.capacity} Kişi</span>
                        </div>
                        
                        {isSelected && (
                          <div className="absolute top-2 left-2 gold-button text-[11px] font-extrabold px-2.5 py-0.5 rounded-full shadow z-10">
                            SEÇİLDİ ✓
                          </div>
                        )}

                        <button
                          type="button"
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedVenueForDetail(v);
                          }}
                          className="absolute bottom-2 right-2 bg-slate-900/90 hover:bg-slate-800 text-white text-[10px] font-bold px-2.5 py-1 rounded-lg border border-white/30 transition flex items-center space-x-1 shadow z-10"
                          title="Salon Detaylarını Göster"
                        >
                          <span>Detaylar</span>
                        </button>
                      </div>

                      <div className="p-3 space-y-1.5 flex-1 flex flex-col justify-between bg-white dark:bg-brand-card">
                        <div>
                          <h4 className="font-heading font-extrabold text-xs sm:text-sm text-slate-800 dark:text-gray-100 leading-tight">
                            {v.name}
                          </h4>
                          <p className="text-[10px] text-slate-500 dark:text-gray-400 line-clamp-1 mt-1">{v.description}</p>
                        </div>

                        <div className="pt-2 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
                          <span className="text-[10px] font-bold text-slate-500">Liste Fiyatı:</span>
                          <span className="font-extrabold text-xs text-slate-800 dark:text-gray-200">{formatCurrency(v.price)}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Bu Rezervasyona Özel Salon Kiralama Fiyatı (TL):</label>
                <input
                  type="number"
                  value={customVenuePrice}
                  onChange={e => setCustomVenuePrice(Number(e.target.value))}
                  className="w-full bg-amber-500/10 border border-amber-500/40 rounded-xl p-2.5 text-amber-800 dark:text-gold-400 font-extrabold"
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Davetli Sayısı (Kişi):</label>
                <input type="number" value={guestCount} onChange={e => setGuestCount(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
              </div>
            </div>

            {/* QUICK TIME SLOT SEANSLARI PRESETS */}
            <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-brand-border">
              <label className="font-bold text-slate-800 dark:text-gray-200 text-xs flex items-center space-x-1.5">
                <span>Hızlı Seans Seçimi:</span>
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => { setStartTime('10:00'); setEndTime('15:00'); }}
                  className={`p-2.5 rounded-xl border text-center transition font-bold text-xs flex flex-col items-center justify-center space-y-0.5 ${
                    startTime === '10:00' && endTime === '15:00'
                      ? 'gold-button shadow border-amber-500'
                      : 'bg-slate-50 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border-slate-200 dark:border-brand-border hover:border-amber-500'
                  }`}
                >
                  <span className="font-bold">Gündüz Seansı</span>
                  <span className="text-[10px] opacity-80 font-mono">10:00 - 15:00</span>
                </button>
                <button
                  type="button"
                  onClick={() => { setStartTime('18:00'); setEndTime('23:00'); }}
                  className={`p-2.5 rounded-xl border text-center transition font-bold text-xs flex flex-col items-center justify-center space-y-0.5 ${
                    startTime === '18:00' && endTime === '23:00'
                      ? 'gold-button shadow border-amber-500'
                      : 'bg-slate-50 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border-slate-200 dark:border-brand-border hover:border-amber-500'
                  }`}
                >
                  <span className="font-bold">Gece Balo Seansı</span>
                  <span className="text-[10px] opacity-80 font-mono">18:00 - 23:00</span>
                </button>
                <button
                  type="button"
                  onClick={() => { setStartTime('09:00'); setEndTime('23:30'); }}
                  className={`p-2.5 rounded-xl border text-center transition font-bold text-xs flex flex-col items-center justify-center space-y-0.5 ${
                    startTime === '09:00' && endTime === '23:30'
                      ? 'gold-button shadow border-amber-500'
                      : 'bg-slate-50 dark:bg-brand-dark text-slate-700 dark:text-gray-300 border-slate-200 dark:border-brand-border hover:border-amber-500'
                  }`}
                >
                  <span className="font-bold">Tüm Gün Kiralama</span>
                  <span className="text-[10px] opacity-80 font-mono">09:00 - 23:30</span>
                </button>
              </div>
            </div>

            {/* START AND END DATE & TIME SELECTION */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
              <div className="space-y-2">
                <label className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1.5">
                  <span>Etkinlik Başlangıç Tarihi & Saati:</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" />
                  <input type="time" value={startTime} onChange={e => setStartTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1.5">
                  <span>Etkinlik Bitiş Tarihi & Saati:</span>
                </label>
                <div className="grid grid-cols-2 gap-2">
                  <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" />
                  <input type="time" value={endTime} onChange={e => setEndTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold" />
                </div>
              </div>
            </div>

            {/* REAL-TIME CONFLICT / AVAILABILITY WARNING BANNER */}
            {conflictInfo.hasConflict ? (
              <div className="p-4 rounded-2xl border-2 border-red-500/60 bg-red-500/10 text-red-700 dark:text-red-300 space-y-2.5 shadow-xl animate-fade-in">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 rounded-2xl bg-red-500 text-white font-extrabold flex items-center justify-center text-xl shrink-0 shadow-md">
                    ⚠️
                  </div>
                  <div>
                    <h4 className="font-heading font-extrabold text-sm text-red-600 dark:text-red-400">
                      ÇAKIŞMA ENGELLENDİ: SEÇİLEN SALON VE SEANS ZATEN REZERVE EDİLMİŞ!
                    </h4>
                    <p className="text-xs text-red-700 dark:text-red-300 leading-normal">
                      <strong>{selectedVenue?.name}</strong> salonunda <strong>{formatDate(startDate)}</strong> tarihinde onaylı bir rezervasyon bulunmaktadır.
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="p-3.5 rounded-2xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 flex items-center justify-between shadow-sm">
                <div className="flex items-center space-x-2.5">
                  <span className="text-base">✓</span>
                  <div className="text-xs font-bold">
                    {selectedVenue?.name} • {formatDate(startDate)} ({activeSlot}) — Bu Salon ve Seans Tamamen Müsait!
                  </div>
                </div>
                <span className="text-[10px] font-extrabold text-emerald-700 dark:text-emerald-400 bg-emerald-500/20 px-2.5 py-0.5 rounded-full border border-emerald-500/30 uppercase tracking-wider">
                  MÜSAİT
                </span>
              </div>
            )}

            {/* LIVE CALENDAR PREVIEW & OCCUPANCY TIMELINE (RESTORED INSIDE SECTION 1) */}
            <div className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-4 rounded-2xl space-y-3 text-xs">
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                <span className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1.5">
                  <ThemeIcon icon="calendar" fallbackEmoji="" className="w-4 h-4 text-amber-500 shrink-0" />
                  <span>Canlı Takvim & Çakışma Önizlemesi ({selectedVenue?.name}):</span>
                </span>

                <div className="flex items-center space-x-2 w-full sm:w-auto justify-between sm:justify-end">
                  <span className="text-[10px] bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold px-2.5 py-1 rounded-full border border-amber-500/20 whitespace-nowrap">
                    Seçilen: {formatDate(startDate)} ({startTime} - {endTime})
                  </span>

                  {/* NAV ARROWS FOR 14-DAY CALENDAR SHIFT */}
                  <div className="flex items-center space-x-1 shrink-0">
                    <button
                      type="button"
                      onClick={() => setCalendarOffsetDays(prev => prev - 7)}
                      className="w-7 h-7 rounded-lg bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border text-slate-700 dark:text-gray-200 hover:border-amber-500 flex items-center justify-center font-extrabold text-sm shadow-sm hover:scale-105 transition cursor-pointer"
                      title="Önceki Hafta (-7 Gün)"
                      aria-label="Önceki Hafta"
                    >
                      ‹
                    </button>
                    {calendarOffsetDays !== 0 && (
                      <button
                        type="button"
                        onClick={() => setCalendarOffsetDays(0)}
                        className="px-2 py-0.5 text-[10px] font-extrabold bg-amber-500/20 text-amber-800 dark:text-gold-400 rounded-md border border-amber-500/30 hover:bg-amber-500/30 transition"
                        title="Seçili Tarihe Sıfırla"
                      >
                        Bugün
                      </button>
                    )}
                    <button
                      type="button"
                      onClick={() => setCalendarOffsetDays(prev => prev + 7)}
                      className="w-7 h-7 rounded-lg bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border text-slate-700 dark:text-gray-200 hover:border-amber-500 flex items-center justify-center font-extrabold text-sm shadow-sm hover:scale-105 transition cursor-pointer"
                      title="Sonraki Hafta (+7 Gün)"
                      aria-label="Sonraki Hafta"
                    >
                      ›
                    </button>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-7 gap-1 text-center font-bold text-[10px] text-slate-500 pt-1">
                <span>Pzt</span><span>Sal</span><span>Çar</span><span>Per</span><span>Cum</span><span>Cmt</span><span>Paz</span>
              </div>

              {/* MINI CALENDAR DAYS GRID (DYNAMIC 14 DAYS AROUND SELECTED DATE + OFFSET) */}
              <div className="grid grid-cols-7 gap-1 text-[11px]">
                {preview14Days.map((dayDate) => {
                  const yr = dayDate.getFullYear();
                  const mo = String(dayDate.getMonth() + 1).padStart(2, '0');
                  const dy = String(dayDate.getDate()).padStart(2, '0');
                  const dateStr = `${yr}-${mo}-${dy}`;
                  const isSelectedDate = dateStr === startDate;
                  const hasExistingBooking = (reservations || []).some(r => r.venueId === venueId && r.date === dateStr && r.paymentStatus !== 'İptal');
                  const monthNameShort = dayDate.toLocaleDateString('tr-TR', { month: 'short' });

                  return (
                    <div
                      key={dateStr}
                      onClick={() => {
                        setStartDate(dateStr);
                        setEndDate(dateStr);
                      }}
                      className={`p-1.5 rounded-xl text-center cursor-pointer transition border flex flex-col justify-between h-12 ${
                        isSelectedDate
                          ? 'gold-button shadow font-extrabold border-amber-500'
                          : hasExistingBooking
                          ? 'bg-red-500/10 border-red-500/30 text-red-700 dark:text-red-400 font-bold'
                          : 'bg-white dark:bg-brand-card border-slate-200 dark:border-brand-border text-slate-700 dark:text-gray-300 hover:border-amber-500/50'
                      }`}
                    >
                      <span className="text-[9px] opacity-75">{dayDate.getDate()} {monthNameShort}</span>
                      <span className="text-[9px] font-bold">
                        {isSelectedDate ? 'SEÇİLDİ' : hasExistingBooking ? 'DOLU' : 'BOŞ'}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* SECTION 2: EK HİZMETLER */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
            <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-brand-border pb-3">
              <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">2. Ek Hizmetler:</h3>
            </div>

            <div className="space-y-3">
              {services.map(s => {
                const found = selectedServices.find(x => x.serviceId === s.id);
                const isSelected = !!found;
                const qty = found ? found.quantity : (s.pricingType === 'per_person' ? guestCount : 1);
                const isPaid = found ? found.isPaid : false;

                return (
                  <div key={s.id} className={`p-4 rounded-2xl border transition space-y-2 ${isSelected ? 'bg-amber-500/10 border-amber-500/50' : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'}`}>
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                      <label className="flex items-center space-x-3 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={e => {
                            if (e.target.checked) {
                              setSelectedServices(prev => [...prev, { serviceId: s.id, quantity: s.pricingType === 'per_person' ? guestCount : 1, isPaid: false }]);
                            } else {
                              setSelectedServices(prev => prev.filter(x => x.serviceId !== s.id));
                            }
                          }}
                          className="w-5 h-5 accent-amber-600 rounded"
                        />
                        <div>
                          <div className="font-bold text-xs text-slate-800 dark:text-gray-200">{s.name}</div>
                          <div className="text-[10px] text-slate-500">{s.description} | {formatCurrency(s.price)} {s.pricingType === 'per_person' ? '/Kişi' : '/Paket'}</div>
                        </div>
                      </label>

                      {isSelected && (
                        <div className="flex flex-wrap items-center gap-3 text-xs">
                          <div className="flex items-center space-x-1">
                            <span className="font-bold">Özel Birim Fiyat (TL):</span>
                            <input
                              type="number"
                              value={found.customUnitPrice !== undefined ? found.customUnitPrice : s.price}
                              onChange={e => {
                                const val = Number(e.target.value);
                                setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, customUnitPrice: val } : x));
                              }}
                              className="w-24 bg-amber-500/10 border border-amber-500/40 rounded-lg p-1 font-bold text-center text-amber-800 dark:text-gold-400"
                            />
                          </div>

                          {s.pricingType === 'per_person' && (
                            <div className="flex items-center space-x-1">
                              <span className="font-bold">Kişi Sayısı:</span>
                              <input
                                type="number"
                                value={qty}
                                onChange={e => {
                                  const val = Number(e.target.value);
                                  setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, quantity: val } : x));
                                }}
                                className="w-20 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1 font-bold text-center"
                              />
                            </div>
                          )}

                          <label className={`flex items-center space-x-1 font-bold cursor-pointer ${isPaid ? 'text-emerald-600' : 'text-slate-500 dark:text-gray-400'}`}>
                            <input
                              type="checkbox"
                              checked={isPaid}
                              onChange={e => {
                                const checked = e.target.checked;
                                setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, isPaid: checked } : x));
                              }}
                              className={`w-4 h-4 ${isPaid ? 'accent-emerald-600' : 'accent-slate-400'}`}
                            />
                            <span>{isPaid ? 'Ödendi ✓' : 'Ödenmedi'}</span>
                          </label>
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* SECTION 3: ÖDEME, KAPORA & İNDİRİM KODU BİLGİLERİ */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
            <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-brand-border pb-3">
              <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">3. Ödeme, Kapora & İndirim Kodu Bilgileri</h3>
            </div>

            <div className="text-xs">
              <label className="font-bold block mb-1">Referans / Aracılık Eden (İsim Soyisim):</label>
              <input
                type="text"
                placeholder="Örn: Ahmet Yılmaz (Organizasyon Koçu / Aile Yakını)"
                value={referrerName}
                onChange={e => setReferrerName(e.target.value)}
                className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div>
                <label className="font-bold block mb-1">İndirim Kodu:</label>
                <select value={campaignCode} onChange={e => setCampaignCode(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                  <option value="">İndirim Kodu Yok</option>
                  {campaigns.map(c => <option key={c.id} value={c.code}>{c.code} - {c.title}</option>)}
                </select>
              </div>

              <div>
                <label className="font-bold block mb-1">Kapora Ödendi Mi?</label>
                <select value={hasDeposit ? 'yes' : 'no'} onChange={e => setHasDeposit(e.target.value === 'yes')} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                  <option value="yes">Evet, Kapora Alındı</option>
                  <option value="no">Hayır, Henüz Ödenmedi</option>
                </select>
              </div>

              {hasDeposit && (
                <div>
                  <label className="font-bold block mb-1">Ödenen Kapora Tutarı (TL):</label>
                  <input type="number" value={depositPaid} onChange={e => setDepositPaid(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-emerald-600" />
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
                <option value="Ödendi">Ödendi (Tam ödeme yapıldı - Net Bakiye 0 ₺)</option>
                <option value="Tamamlandı">Tamamlandı (Tam ödeme yapıldı - Net Bakiye 0 ₺)</option>
              </select>
            </div>
          </div>

          {/* SECTION 4: MÜŞTERİ İLETİŞİM BİLGİLERİ */}
          <div id="customer-section" className={`glass-panel p-6 rounded-3xl space-y-4 shadow-sm border transition ${customerError ? 'border-2 border-red-500 bg-red-500/5' : 'border-slate-200 dark:border-brand-border'}`}>
            <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">4. Müşteri İletişim Bilgileri:</h3>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs font-bold w-full">
                <button
                  type="button"
                  onClick={() => { setCustomerMode('new'); setCustomerError(false); }}
                  className={`py-2.5 px-2 rounded-xl border text-center transition flex items-center justify-center space-x-1.5 ${customerMode === 'new' ? 'gold-button shadow font-extrabold' : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 border-slate-200 dark:border-slate-800'}`}
                >
                  <span>+ Yeni Müşteri</span>
                </button>
                <button
                  type="button"
                  onClick={() => { setCustomerMode('existing'); setCustomerError(false); }}
                  className={`py-2.5 px-2 rounded-xl border text-center transition flex items-center justify-center space-x-1.5 ${customerMode === 'existing' ? 'gold-button shadow font-extrabold' : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 border-slate-200 dark:border-slate-800'}`}
                >
                  <ThemeIcon icon="user" fallbackEmoji="👥" className="w-3.5 h-3.5 shrink-0 inline-block" />
                  <span>Müşteri Listesi</span>
                </button>
              </div>
            </div>

            {customerMode === 'existing' ? (
              <div className="text-xs space-y-2">
                <label className="font-bold text-slate-700 dark:text-gray-300 block">Mevcut Müşteri Ara ve Seçin:</label>
                <input
                  type="text"
                  placeholder="🔍 Ad, Soyad, Telefon veya E-posta ile Hızlı Ara..."
                  value={customerSearchQuery}
                  onChange={e => setCustomerSearchQuery(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-amber-500/40 rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-medium shadow-sm focus:ring-2 focus:ring-amber-500"
                />

                <select
                  value={selectedCustomerId}
                  onChange={e => { setSelectedCustomerId(e.target.value); setCustomerError(false); }}
                  className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold ${customerError && !selectedCustomerId ? 'border-2 border-red-500 bg-red-500/10' : 'border-slate-200 dark:border-brand-border'}`}
                >
                  {customers
                    .filter(c => {
                      if (!customerSearchQuery.trim()) return true;
                      const q = customerSearchQuery.toLowerCase();
                      return (c.name || '').toLowerCase().includes(q) || (c.phone || '').includes(q) || (c.email || '').toLowerCase().includes(q);
                    })
                    .map(c => (
                      <option key={c.id} value={c.id}>
                        {c.name} (Tel: {c.phone} | {c.email})
                      </option>
                    ))}
                </select>

                {selectedCustomerId && (
                  <div className="mt-2.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1 border border-emerald-500/20 shadow-sm animate-fade-in">
                    <svg className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span>VAROLAN MÜŞTERİ SEÇİLDİ</span>
                    <span className="font-semibold text-slate-500 dark:text-gray-400 ml-1 truncate max-w-[200px]">
                      ({customers.find(c => c.id === selectedCustomerId)?.name || 'Kayıtlı Müşteri'})
                    </span>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-3 text-xs">
                <div className="bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-2.5 rounded-xl text-slate-700 dark:text-gray-300 font-bold flex items-center space-x-1.5">
                  <span>Bu kişi için sistemde otomatik olarak yeni üye ve müşteri kartı oluşturulacaktır.</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label className="font-bold block mb-1">Adı Soyadı / Firma Unvanı <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      placeholder="Örn: Mehmet Yılmaz & Zeynep Can"
                      value={newCustName}
                      onChange={e => { setNewCustName(e.target.value); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 ${customerError && !newCustName.trim() ? 'border-2 border-red-500 bg-red-500/10 font-bold ring-2 ring-red-500/30' : 'border-slate-200 dark:border-brand-border'}`}
                    />
                    {customerError && !newCustName.trim() && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <span>⚠️ Adı Soyadı alanı zorunludur.</span>
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="font-bold block mb-1">E-posta Adresi <span className="text-red-500">*</span>:</label>
                    <input
                      type="email"
                      placeholder="ornek@domain.com"
                      value={newCustEmail}
                      onChange={e => { setNewCustEmail(e.target.value); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 ${customerError && (!newCustEmail.trim() || !newCustEmail.includes('@')) ? 'border-2 border-red-500 bg-red-500/10 font-bold ring-2 ring-red-500/30' : 'border-slate-200 dark:border-brand-border'}`}
                    />
                    {customerError && (!newCustEmail.trim() || !newCustEmail.includes('@')) && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <span>⚠️ Geçerli bir e-posta adresi zorunludur.</span>
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div className="relative">
                    <label className="font-bold block mb-1">Birincil Telefon (+90) <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      placeholder="0 (5XX) XXX XX XX"
                      value={newCustPhone}
                      onChange={e => { setNewCustPhone(formatPhoneNumber(e.target.value)); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold ${
                        customerError && (!newCustPhone.trim() || !isValidPhoneNumber(newCustPhone))
                          ? 'border-2 border-red-500 bg-red-500/10 text-red-600 ring-2 ring-red-500/30'
                          : isValidPhoneNumber(newCustPhone)
                          ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                          : 'border-slate-200 dark:border-brand-border'
                      }`}
                    />

                    {/* MATCHED EXISTING CUSTOMERS FLOATING DROPDOWN */}
                    {(() => {
                      if (!newCustPhone || customerMode !== 'new') return null;
                      const rawDigits = newCustPhone.replace(/\D/g, '');
                      if (rawDigits.length < 3) return null;
                      const matches = (customers || []).filter(c => {
                        const cDigits = (c.phone || '').replace(/\D/g, '');
                        return cDigits.includes(rawDigits) || (c.name || '').toLowerCase().includes(newCustPhone.toLowerCase());
                      }).slice(0, 4);
                      if (matches.length === 0) return null;
                      return (
                        <div className="absolute left-0 right-0 top-full mt-1.5 z-40 bg-white dark:bg-slate-900 border-2 border-amber-500 rounded-2xl shadow-2xl overflow-hidden animate-slide-down">
                          <div className="bg-amber-500/15 px-3 py-2 border-b border-amber-500/30 text-[11px] font-extrabold text-amber-800 dark:text-gold-400 flex items-center justify-between">
                            <span className="flex items-center space-x-1">
                              <span>⚡ Kayıtlı Müşteri Eşleşti ({matches.length}):</span>
                            </span>
                            <span className="text-[10px] text-slate-500 dark:text-slate-400">Tıklayıp Verileri Doldurun</span>
                          </div>
                          <div className="divide-y divide-slate-100 dark:divide-slate-800 max-h-48 overflow-y-auto">
                            {matches.map(cust => (
                              <div
                                key={cust.id}
                                onClick={() => {
                                  setSelectedCustomerId(cust.id);
                                  setCustomerSearchQuery('');
                                  setCustomerMode('existing');
                                  setCustomerError(false);
                                  showToast(`👥 "${cust.name}" Kayıtlı Müşteri Olarak Seçildi ve Aktarıldı!`);
                                }}
                                className="p-3 hover:bg-amber-500/10 dark:hover:bg-slate-800/80 cursor-pointer transition flex items-center justify-between text-left group"
                              >
                                <div>
                                  <div className="font-extrabold text-xs text-slate-900 dark:text-gray-100 group-hover:text-amber-600 dark:group-hover:text-gold-400">
                                    {cust.name}
                                  </div>
                                  <div className="text-[10px] text-slate-500 dark:text-gray-400 font-mono mt-0.5">
                                    Tel: {cust.phone} {cust.email ? `| ${cust.email}` : ''}
                                  </div>
                                </div>
                                <button
                                  type="button"
                                  className="gold-button text-[10px] font-extrabold px-2.5 py-1 rounded-lg shadow shrink-0 active:scale-95"
                                >
                                  Seç & Doldur ✓
                                </button>
                              </div>
                            ))}
                          </div>
                        </div>
                      );
                    })()}
                      placeholder="0 (5XX) XXX XX XX"
                      value={newCustPhone}
                      onChange={e => { setNewCustPhone(formatPhoneNumber(e.target.value)); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold ${
                        customerError && (!newCustPhone.trim() || !isValidPhoneNumber(newCustPhone))
                          ? 'border-2 border-red-500 bg-red-500/10 text-red-600 ring-2 ring-red-500/30'
                          : isValidPhoneNumber(newCustPhone)
                          ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                          : 'border-slate-200 dark:border-brand-border'
                      }`}
                    />
                    {customerError && (!newCustPhone.trim() || !isValidPhoneNumber(newCustPhone)) && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <span>⚠️ Birincil telefon (05XX) zorunludur.</span>
                      </p>
                    )}
                  </div>
                  <div>
                    <label className="font-bold block mb-1">İkinci İletişim / Yakın Telefonu <span className="text-red-500">*</span>:</label>
                    <input
                      type="text"
                      placeholder="0 (5XX) XXX XX XX"
                      value={newCustSecondaryPhone}
                      onChange={e => { setNewCustSecondaryPhone(formatPhoneNumber(e.target.value)); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold ${
                        customerError && (!newCustSecondaryPhone.trim() || !isValidPhoneNumber(newCustSecondaryPhone))
                          ? 'border-2 border-red-500 bg-red-500/10 text-red-600 ring-2 ring-red-500/30'
                          : isValidPhoneNumber(newCustSecondaryPhone)
                          ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                          : 'border-slate-200 dark:border-brand-border'
                      }`}
                    />
                    {customerError && (!newCustSecondaryPhone.trim() || !isValidPhoneNumber(newCustSecondaryPhone)) && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <span>⚠️ İkinci iletişim telefonu (05XX) zorunludur.</span>
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* SECTION 5: FATURA BİLGİLERİ */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
            <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-2">
              <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">5. Fatura Bilgileri</h3>
              
              <label className="flex items-center space-x-2 text-xs font-bold cursor-pointer pt-1">
                <input type="checkbox" checked={isInvoiced} onChange={e => setIsInvoiced(e.target.checked)} className="w-4 h-4 accent-amber-600" />
                <span>Faturalı İşlem (%20 KDV Hesapla)</span>
              </label>
            </div>

            {isInvoiced && (
              <div className="space-y-4 text-xs">
                <div>
                  <label className="font-bold block mb-1">Fatura Tipi:</label>
                  <div className="flex space-x-4">
                    <label className="flex items-center space-x-2 cursor-pointer font-bold">
                      <input type="radio" name="invType" value="individual" checked={invoiceType === 'individual'} onChange={() => setInvoiceType('individual')} className="accent-amber-600" />
                      <span>Bireysel Fatura (TC Kimlik No)</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-pointer font-bold">
                      <input type="radio" name="invType" value="corporate" checked={invoiceType === 'corporate'} onChange={() => setInvoiceType('corporate')} className="accent-amber-600" />
                      <span>Tüzel / Kurumsal Fatura (VKN)</span>
                    </label>
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {invoiceType === 'individual' ? (
                    <div><label className="font-bold block mb-1">TC Kimlik No:</label><input type="text" value={tcNo} onChange={e => setTcNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                  ) : (
                    <div><label className="font-bold block mb-1">Vergi Kimlik No (VKN):</label><input type="text" value={vknNo} onChange={e => setVknNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                  )}
                  <div><label className="font-bold block mb-1">Vergi Dairesi:</label><input type="text" value={taxOffice} onChange={e => setTaxOffice(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" /></div>
                </div>

                <div>
                  <label className="font-bold block mb-1">Fatura Adresi:</label>
                  <textarea value={invoiceAddress} onChange={e => setInvoiceAddress(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
                </div>
              </div>
            )}
          </div>

          {/* SECTION 6: ORGANİZASYON & ETKİNLİK AKIŞ PLANLAMASI */}
          <div className="glass-panel p-4 sm:p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center border-b border-slate-200 dark:border-brand-border pb-3 gap-2">
              <div>
                <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">6. Organizasyon & Etkinlik Akış Planlaması</h3>
                <p className="text-[11px] text-slate-500 dark:text-gray-400 font-medium">Masaüstünde (⋮⋮) sürükleyebilir veya mobilde (▲/▼) oklarıyla sırasını değiştirebilirsiniz.</p>
              </div>
              <button onClick={handleAddFlowItem} className="w-full sm:w-auto px-3 py-1.5 bg-slate-100 dark:bg-brand-dark hover:bg-slate-200 text-slate-800 dark:text-gray-200 font-bold rounded-xl text-xs border border-slate-200 dark:border-brand-border text-center">➕ Akış Adımı Ekle</button>
            </div>

            <div className="space-y-2 text-xs">
              {flowPlan.map((item, idx) => (
                <div
                  key={idx}
                  draggable={true}
                  onDragStart={(e) => handleDragStart(e, idx)}
                  onDragOver={(e) => handleDragOver(e, idx)}
                  onDrop={(e) => handleDrop(e, idx)}
                  onDragEnd={handleDragEnd}
                  className={`flex items-center space-x-2 sm:space-x-3 p-2 sm:p-2.5 rounded-xl border transition-all cursor-move ${
                    draggedIdx === idx
                      ? 'opacity-40 bg-amber-500/20 border-amber-500 scale-95'
                      : dragOverIdx === idx
                      ? 'bg-amber-500/20 border-amber-500 border-2 scale-[1.02] shadow-md'
                      : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border hover:border-amber-500/50'
                  }`}
                >
                  <div className="hidden sm:flex items-center cursor-grab active:cursor-grabbing text-slate-400 font-bold px-1 text-sm select-none">
                    ⋮⋮
                  </div>

                  <div className="flex flex-col space-y-0.5 shrink-0">
                    <button
                      type="button"
                      onClick={() => moveFlowItemUp(idx)}
                      disabled={idx === 0}
                      className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                    >
                      ▲
                    </button>
                    <button
                      type="button"
                      onClick={() => moveFlowItemDown(idx)}
                      disabled={idx === flowPlan.length - 1}
                      className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                    >
                      ▼
                    </button>
                  </div>

                  <input
                    type="text"
                    value={item.time}
                    onChange={e => {
                      const val = e.target.value;
                      setFlowPlan(prev => prev.map((x, i) => i === idx ? { ...x, time: val } : x));
                    }}
                    className="w-16 sm:w-20 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1.5 font-mono font-bold text-center text-slate-800 dark:text-gray-200 text-xs shrink-0"
                  />
                  <input
                    type="text"
                    value={item.title}
                    onChange={e => {
                      const val = e.target.value;
                      setFlowPlan(prev => prev.map((x, i) => i === idx ? { ...x, title: val } : x));
                    }}
                    className="flex-1 bg-white dark:bg-brand-card border border-slate-200 rounded-lg p-1.5 font-bold text-slate-800 dark:text-gray-200 text-xs min-w-0"
                  />
                  <button onClick={() => handleRemoveFlowItem(idx)} className="text-red-500 hover:text-red-700 font-bold px-1.5 text-sm shrink-0">✕</button>
                </div>
              ))}
            </div>
          </div>

          {/* SECTION 7: OPERASYONEL EK NOTLAR & ÖZEL İSTEKLER */}
          <div className="glass-panel p-6 rounded-3xl space-y-3 shadow-sm border border-slate-200 dark:border-brand-border text-xs">
            <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100 border-b border-slate-200 dark:border-brand-border pb-3">7. Operasyonel Ek Notlar & Özel İstekler:</h3>
            <textarea value={notes} onChange={e => setNotes(e.target.value)} placeholder="Gelin odası ikramları, çiçek renk tercihleri, özel teknik ekipman talepleri..." className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-3 h-20" />
          </div>

        </div>

        {/* RIGHT COLUMN: LIVE INTERACTIVE PREVIEW & SUMMARY CARD (4 Cols) */}
        <div className="lg:col-span-4 space-y-6">
          
          {/* TAKVİM ÖN İZLEME KARTI */}
          <div className="glass-panel p-5 rounded-3xl space-y-3 shadow-sm border border-slate-200 dark:border-brand-border">
            <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-2">
              <span className="font-bold text-xs text-slate-800 dark:text-gray-100 flex items-center space-x-1.5">
                <span>Takvim Canlı Ön İzlemesi</span>
              </span>
              <span className="text-[10px] bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 font-mono font-bold px-2 py-0.5 rounded border border-slate-200 dark:border-brand-border">{startDate}</span>
            </div>
            
            <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border text-center space-y-2 text-xs">
              <div className="font-bold text-slate-800 dark:text-gray-100">{formatDate(startDate)}</div>
              <div className="text-slate-900 dark:text-white font-extrabold">{selectedVenue?.name}</div>
              <div className="text-[11px] font-mono text-slate-600 dark:text-gray-300 bg-white dark:bg-brand-card py-1 px-2 rounded-lg border border-slate-200 dark:border-brand-border">{activeSlot}</div>
              {conflictInfo.hasConflict ? (
                <div className="bg-red-500/10 text-red-600 dark:text-red-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1">
                  <span>⚠️ BU SAAT DİLİMİ DOLUDUR</span>
                </div>
              ) : (
                <div className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1">
                  <span>✓ SALON MÜSAİT</span>
                </div>
              )}
            </div>
          </div>

          {/* DESKTOP LIVE SUMMARY CARD */}
          <div className="hidden sm:block glass-panel p-6 rounded-3xl space-y-4 shadow-xl border-2 border-slate-200 dark:border-brand-border sticky top-24">
            <h3 className="font-heading font-extrabold text-base text-slate-900 dark:text-white border-b border-slate-200 dark:border-brand-border pb-3 flex items-center space-x-2">
              <span>📜</span>
              <span>Canlı Hesaplama & Sözleşme Kartı</span>
            </h3>

            <div className="space-y-2 text-xs">
              <div className="flex justify-between font-bold text-slate-700 dark:text-gray-200">
                <span>Salon Kiralama Bedeli:</span>
                <span className="font-mono">{formatCurrency(calculations.venuePrice)}</span>
              </div>

              {calculations.serviceBreakdown.length > 0 && (
                <div className="pl-2 border-l-2 border-amber-500/40 space-y-1">
                  <div className="text-[10px] font-bold text-slate-500">Ek Hizmetler Dökümü:</div>
                  {calculations.serviceBreakdown.map(sb => (
                    <div key={sb.id} className="flex justify-between text-[11px] text-slate-600 dark:text-gray-400">
                      <span>• {sb.name} ({sb.quantity}x)</span>
                      <span className="font-mono">{formatCurrency(sb.total)}</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="flex justify-between font-extrabold text-sm text-amber-700 dark:text-gold-400 border-t border-slate-200 dark:border-brand-border pt-2">
                <span>Ara Toplam:</span>
                <span className="font-mono">{formatCurrency(calculations.subtotal)}</span>
              </div>

              {calculations.discount > 0 && (
                <div className="flex justify-between text-amber-600 dark:text-gold-400 font-bold">
                  <span>İndirim Kodu ({campaignCode}):</span>
                  <span className="font-mono">-{formatCurrency(calculations.discount)}</span>
                </div>
              )}

              {isInvoiced && (
                <div className="flex justify-between text-slate-600 dark:text-gray-300">
                  <span>KDV (%20):</span>
                  <span className="font-mono">{formatCurrency(calculations.vat)}</span>
                </div>
              )}

              <div className="flex justify-between font-extrabold text-base text-slate-900 dark:text-white pt-2 border-t border-slate-200 dark:border-brand-border">
                <span>Genel Toplam:</span>
                <span className="font-mono text-amber-800 dark:text-gold-400">{formatCurrency(calculations.grandTotal)}</span>
              </div>

              {hasDeposit && (
                <div className="flex justify-between text-emerald-600 dark:text-emerald-400 pt-1 font-bold">
                  <span>Tahsil Edilen Kapora:</span>
                  <span className="font-mono">-{formatCurrency(calculations.dep)}</span>
                </div>
              )}

              <div className={`flex justify-between font-bold text-sm p-2.5 rounded-xl border mt-2 ${
                calculations.isFullyPaid
                  ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-700 dark:text-emerald-300'
                  : 'bg-red-500/10 border-red-500/20 text-red-600 dark:text-red-400'
              }`}>
                <span>Kalan Ödenecek Net Bakiye:</span>
                <span className="font-mono font-extrabold text-base">
                  {calculations.isFullyPaid ? '0 ₺ (Ödendi ✓)' : formatCurrency(calculations.remaining)}
                </span>
              </div>
            </div>

            <div className="pt-2">
              <button
                disabled={conflictInfo.hasConflict}
                onClick={handleSubmit}
                className={`w-full gold-button font-bold py-3.5 rounded-2xl text-xs shadow-xl flex items-center justify-center space-x-2 ${
                  conflictInfo.hasConflict ? 'opacity-50 cursor-not-allowed' : 'hover:scale-[1.02]'
                }`}
              >
                <span>🎉</span><span>Rezervasyonu ve Sözleşmeyi Kaydet</span>
              </button>
            </div>

          </div>

        </div>

      </div>
    </div>
  );
}
