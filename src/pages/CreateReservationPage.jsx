import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations = [], draftReservations = [], setDraftReservations, currentUser, prefilledDate, onSaveReservation, onCancel, showToast, navigateTo }) {
      const todayDateStr = useMemo(() => {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      }, []);
      // 1. Venue, Start/End Date & Time
      const venueCarouselRef = useRef(null);
      const [selectedVenueForDetail, setSelectedVenueForDetail] = useState(null);
      const [isMobileSummaryDrawerOpen, setIsMobileSummaryDrawerOpen] = useState(false);
      const [alertModal, setAlertModal] = useState({ isOpen: false, title: '', message: '', targetInputId: null });

      // DRAFT AUTOMATION & AUTO-SAVE (650ms DEBOUNCE, 12-CHAR REFKEY, USER AUDIT LOGS, CONFLICT MODAL)
      const initialRefKey = useMemo(() => {
        const hashData = parseHashRoute();
        return hashData.refKey || generateDraftRefKey();
      }, []);

      const [activeRefKey, setActiveRefKey] = useState(initialRefKey);
      const [lastSavedTime, setLastSavedTime] = useState(null);
      const [conflictModal, setConflictModal] = useState({ isOpen: false, draft: null });
      const autoSaveTimerRef = useRef(null);
      const isInitialMountRef = useRef(true);

      // Synchronize activeRefKey with URL hash and preserve existing draft refKeys
      useEffect(() => {
        const syncRef = () => {
          const hashData = parseHashRoute();
          if (hashData.tab !== 'create-reservation') return;
          if (hashData.refKey && hashData.refKey !== activeRefKey) {
            setActiveRefKey(hashData.refKey);
          } else if (!hashData.refKey && activeRefKey && !hashData.editId) {
            const tabSlug = TAB_TO_SLUG['create-reservation'] || 'rezervasyon-olustur';
            const newUrl = `${window.location.pathname}#/${tabSlug}?ref=${activeRefKey}`;
            window.history.replaceState({ tab: 'create-reservation', refKey: activeRefKey }, '', newUrl);
          }
        };

        syncRef();
        window.addEventListener('hashchange', syncRef);
        window.addEventListener('popstate', syncRef);
        return () => {
          window.removeEventListener('hashchange', syncRef);
          window.removeEventListener('popstate', syncRef);
        };
      }, [activeRefKey]);

      const [venueId, setVenueId] = useState(venues[0]?.id || '');
      const [customVenuePrice, setCustomVenuePrice] = useState(venues[0]?.price || 0);
      const [startDate, setStartDate] = useState(prefilledDate || '2026-08-25');
      const [startTime, setStartTime] = useState('19:00');
      const [endDate, setEndDate] = useState(prefilledDate || '2026-08-25');
      const [endTime, setEndTime] = useState('23:00');

      const editingResFromUrl = useMemo(() => {
        const hashData = parseHashRoute();
        if (!hashData.editId) return null;
        return (reservations || []).find(r => r.id === hashData.editId || r.contractNo === hashData.editId);
      }, [reservations, window.location.hash]);

      const isEditMode = !!editingResFromUrl;

      // Pre-fill form when editingResFromUrl is detected
      useEffect(() => {
        if (editingResFromUrl) {
          setVenueId(editingResFromUrl.venueId || venues[0]?.id || '');
          setCustomVenuePrice(editingResFromUrl.venuePrice || editingResFromUrl.customVenuePrice || venues[0]?.price || 0);
          setStartDate(editingResFromUrl.startDate || editingResFromUrl.eventDate || editingResFromUrl.date || '2026-08-25');
          setEndDate(editingResFromUrl.endDate || editingResFromUrl.eventDate || editingResFromUrl.date || '2026-08-25');

          const timeParts = (editingResFromUrl.timeSlot || '').split('-');
          if (timeParts.length === 2) {
            setStartTime(timeParts[0].trim() || '19:00');
            setEndTime(timeParts[1].trim() || '23:00');
          } else {
            setStartTime(editingResFromUrl.startTime || '19:00');
            setEndTime(editingResFromUrl.endTime || '23:00');
          }

          setGuestCount(editingResFromUrl.guestCount || 500);

          if (editingResFromUrl.customerId && customers.some(c => c.id === editingResFromUrl.customerId)) {
            setCustomerMode('existing');
            setSelectedCustomerId(editingResFromUrl.customerId);
          } else {
            setCustomerMode('new');
            setNewCustName(editingResFromUrl.customerName || '');
            setNewCustPhone(editingResFromUrl.customerPhone || '');
            setNewCustSecondaryPhone(editingResFromUrl.customerSecondaryPhone || editingResFromUrl.secondaryPhone || '');
            setNewCustEmail(editingResFromUrl.customerEmail || '');
          }

          if (editingResFromUrl.selectedServices && Array.isArray(editingResFromUrl.selectedServices)) {
            setSelectedServices([...editingResFromUrl.selectedServices]);
          }

          setReferrerName(editingResFromUrl.referrerName || '');
          setCampaignCode(editingResFromUrl.campaignCode || '');
          setHasDeposit((editingResFromUrl.depositPaid || 0) > 0);
          setDepositPaid(editingResFromUrl.depositPaid || 0);
          setPaymentStatus(editingResFromUrl.paymentStatus || 'Bekliyor');

          setIsInvoiced(editingResFromUrl.isInvoiced || false);
          setInvoiceType(editingResFromUrl.invoiceType || 'individual');
          if (editingResFromUrl.tcNo) setTcNo(editingResFromUrl.tcNo);
          if (editingResFromUrl.vknNo) setVknNo(editingResFromUrl.vknNo);
          if (editingResFromUrl.taxOffice) setTaxOffice(editingResFromUrl.taxOffice);
          if (editingResFromUrl.invoiceAddress) setInvoiceAddress(editingResFromUrl.invoiceAddress);

          if (editingResFromUrl.flowPlan && Array.isArray(editingResFromUrl.flowPlan) && editingResFromUrl.flowPlan.length > 0) {
            setFlowPlan(JSON.parse(JSON.stringify(editingResFromUrl.flowPlan)));
          }
          if (editingResFromUrl.notes) {
            setNotes(editingResFromUrl.notes);
          }
        }
      }, [editingResFromUrl, venues, customers]);

      // Load existing draft if present for activeRefKey
      useEffect(() => {
        if (!activeRefKey) return;
        const existing = (draftReservations || []).find(d => d.refKey === activeRefKey);
        if (existing && existing.formData) {
          const f = existing.formData;
          if (f.venueId) setVenueId(f.venueId);
          if (f.customVenuePrice !== undefined) setCustomVenuePrice(f.customVenuePrice);
          if (f.startDate) setStartDate(f.startDate);
          if (f.startTime) setStartTime(f.startTime);
          if (f.endDate) setEndDate(f.endDate);
          if (f.endTime) setEndTime(f.endTime);
          if (f.guestCount !== undefined) setGuestCount(f.guestCount);
          if (f.customerMode) setCustomerMode(f.customerMode);
          if (f.selectedCustomerId) setSelectedCustomerId(f.selectedCustomerId);
          if (f.newCustName !== undefined) setNewCustName(f.newCustName);
          if (f.newCustEmail !== undefined) setNewCustEmail(f.newCustEmail);
          if (f.newCustPhone !== undefined) setNewCustPhone(f.newCustPhone);
          if (f.newCustSecondaryPhone !== undefined) setNewCustSecondaryPhone(f.newCustSecondaryPhone);
          if (f.selectedServices) setSelectedServices(f.selectedServices);
          if (f.referrerName !== undefined) setReferrerName(f.referrerName);
          if (f.campaignCode !== undefined) setCampaignCode(f.campaignCode);
          if (f.hasDeposit !== undefined) setHasDeposit(f.hasDeposit);
          if (f.depositPaid !== undefined) setDepositPaid(f.depositPaid);
          if (f.paymentStatus) setPaymentStatus(f.paymentStatus);
          if (f.notes !== undefined) setNotes(f.notes);
          if (f.flowPlan) setFlowPlan(f.flowPlan);
          if (existing.updatedAt) {
            const dt = new Date(existing.updatedAt);
            setLastSavedTime(`${String(dt.getHours()).padStart(2, '0')}:${String(dt.getMinutes()).padStart(2, '0')}:${String(dt.getSeconds()).padStart(2, '0')}`);
          }
        }
      }, [activeRefKey, draftReservations]);

      // Dynamic 14-day preview offset around selected startDate
      const [calendarOffsetDays, setCalendarOffsetDays] = useState(0);

      // Calculate 14-day preview window dynamically centered on startDate
      const preview14Days = useMemo(() => {
        const parts = (startDate || '2026-08-25').split('-');
        const selYear = Number(parts[0]) || 2026;
        const selMonth = (Number(parts[1]) || 8) - 1;
        const selDay = Number(parts[2]) || 25;
        const selected = new Date(selYear, selMonth, selDay);

        const dayOfWeek = selected.getDay(); // 0 is Sun, 1 is Mon...
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
      }, [startDate, calendarOffsetDays]);
      const [guestCount, setGuestCount] = useState(500);

      const showAlertModal = (title, message, targetInputId = null) => {
        if (window.showGlobalAlert) {
          window.showGlobalAlert(title, message, targetInputId);
        } else {
          setAlertModal({
            isOpen: true,
            title: title || '⚠️ LÜTFEN EKSİKSİZ DOLDURUNUZ',
            message: message || 'Müşteri Adı Soyadı ve İletişim Telefon Numarası zorunludur.',
            targetInputId
          });
        }
      };

      const closeAlertModal = () => {
        const targetId = alertModal.targetInputId;
        setAlertModal({ isOpen: false, title: '', message: '', targetInputId: null });
        if (targetId) {
          const el = document.getElementById(targetId);
          if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            el.focus();
          }
        }
      };

      const eventDate = startDate;
      const activeSlot = `${startTime} - ${endTime}`;

      const scrollVenueCarouselLeft = () => {
        if (venueCarouselRef.current) {
          venueCarouselRef.current.scrollBy({ left: -260, behavior: 'smooth' });
        }
      };
      const scrollVenueCarouselRight = () => {
        if (venueCarouselRef.current) {
          venueCarouselRef.current.scrollBy({ left: 260, behavior: 'smooth' });
        }
      };

      // Update customVenuePrice when venueId changes
      useEffect(() => {
        const v = venues.find(x => x.id === venueId);
        if (v) setCustomVenuePrice(v.price);
      }, [venueId]);

      // Collision Check Logic & Same Date Reservations
      const conflictInfo = useMemo(() => {
        const sameVenueDateRes = (reservations || []).filter(r => r.venueId === venueId && r.date === startDate && r.paymentStatus !== 'İptal');
        if (sameVenueDateRes.length === 0) {
          return { hasConflict: false, conflictingRes: null, sameDateResCount: (reservations || []).filter(r => r.date === startDate).length };
        }

        const isSelectedAllDay = activeSlot.includes('Tüm Gün') || (startTime === '09:00' && endTime === '23:30') || (startTime === '08:00' && endTime === '23:59');

        // Check if time slot overlaps
        const conflictingRes = sameVenueDateRes.find(r => {
          if (isSelectedAllDay) return true;
          if ((r.timeSlot || '').includes('Tüm Gün') || (r.timeSlot || '').includes('09:00 - 23:30')) return true;
          if (r.timeSlot === activeSlot) return true;
          
          const parseHour = (str) => {
            const match = (str || '').match(/(\d{1,2}):(\d{2})/);
            return match ? parseInt(match[1]) : 12;
          };
          const rStart = parseHour(r.timeSlot);
          const currStart = parseHour(activeSlot);
          return Math.abs(rStart - currStart) < 4;
        });

        return {
          hasConflict: !!conflictingRes,
          conflictingRes: conflictingRes || (isSelectedAllDay ? sameVenueDateRes[0] : null),
          sameDateResCount: (reservations || []).filter(r => r.date === startDate).length
        };
      }, [reservations, venueId, startDate, activeSlot, startTime, endTime]);

      // 2. Customer & Auto-Membership (DEFAULT TO NEW MEMBER)
      const [customerMode, setCustomerMode] = useState('new'); // 'new' or 'existing'
      const [selectedCustomerId, setSelectedCustomerId] = useState(customers[0]?.id || 'cust1');
      const [isAutoSelectedFromPhone, setIsAutoSelectedFromPhone] = useState(false);
      const [customerSearchQuery, setCustomerSearchQuery] = useState('');
      const [newCustName, setNewCustName] = useState('');
      const [newCustEmail, setNewCustEmail] = useState('');
      const [newCustPhone, setNewCustPhone] = useState('');
      const [newCustSecondaryPhone, setNewCustSecondaryPhone] = useState('');
      const [customerError, setCustomerError] = useState(false);

      // 3. Services & Per-service Guest Quantities & Paid status & Custom Unit Prices (DEFAULT TO UNCHECKED)
      const [selectedServices, setSelectedServices] = useState([]);

      // 4. Financials, Referrer, Deposit & Promo (DEFAULT HASDEPOSIT TO FALSE)
      const [referrerName, setReferrerName] = useState('');
      const [campaignCode, setCampaignCode] = useState('');
      const [hasDeposit, setHasDeposit] = useState(false); // Default: Hayır
      const [depositPaid, setDepositPaid] = useState(0); // Default: 0 TL
      const [paymentStatus, setPaymentStatus] = useState('Bekliyor'); // Default: Bekliyor

      // 5. Invoicing Details (Bireysel / Tüzel) - DEFAULT TO UNCHECKED
      const [isInvoiced, setIsInvoiced] = useState(false);
      const [invoiceType, setInvoiceType] = useState('individual'); // 'individual' or 'corporate'
      const [tcNo, setTcNo] = useState('12345678901');
      const [vknNo, setVknNo] = useState('9876543210');
      const [taxOffice, setTaxOffice] = useState('Sapanca VD');
      const [invoiceAddress, setInvoiceAddress] = useState('Atatürk Mah. Sapanca / Sakarya');

      // 6. Flow Planning & Notes (Draggable & Reorderable, Default Finish Step)
      const [flowPlan, setFlowPlan] = useState([
        { time: '19:00', title: 'Misafir Karşılama & Kokteyl' },
        { time: '19:30', title: 'Gelin Damat Giriş & İlk Dans' },
        { time: '20:15', title: 'Yemek Servisi' },
        { time: '21:30', title: 'Pasta Kesimi & Şov' },
        { time: '22:00', title: 'Takı & Eğlence' },
        { time: endTime || '23:00', title: 'Etkinlik Bitişi & Kapanış' }
      ]);

      // Keep last flow step time synced with endTime
      useEffect(() => {
        setFlowPlan(prev => {
          if (!prev || prev.length === 0) return prev;
          const updated = [...prev];
          const lastIdx = updated.length - 1;
          if (updated[lastIdx].title.includes('Bitişi')) {
            updated[lastIdx] = { ...updated[lastIdx], time: endTime };
          }
          return updated;
        });
      }, [endTime]);

      const [draggedIdx, setDraggedIdx] = useState(null);
      const [dragOverIdx, setDragOverIdx] = useState(null);
      const [notes, setNotes] = useState('Özel çiçek süslemeleri ve gelin odası ikramları dahildir.');

      const handleDragStart = (e, index) => {
        setDraggedIdx(index);
        e.dataTransfer.effectAllowed = "move";
        e.dataTransfer.setData("text/plain", index.toString());
      };

      const handleDragOver = (e, index) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = "move";
        if (dragOverIdx !== index) {
          setDragOverIdx(index);
        }
      };

      const handleDrop = (e, index) => {
        e.preventDefault();
        if (draggedIdx === null || draggedIdx === index) return;
        setFlowPlan(prev => {
          const list = [...prev];
          const [removed] = list.splice(draggedIdx, 1);
          list.splice(index, 0, removed);
          return list;
        });
        setDraggedIdx(null);
        setDragOverIdx(null);
      };

      const handleDragEnd = () => {
        setDraggedIdx(null);
        setDragOverIdx(null);
      };

      const moveFlowItemUp = (index) => {
        if (index <= 0) return;
        setFlowPlan(prev => {
          const list = [...prev];
          const temp = list[index - 1];
          list[index - 1] = list[index];
          list[index] = temp;
          return list;
        });
      };

      const moveFlowItemDown = (index) => {
        setFlowPlan(prev => {
          if (index >= prev.length - 1) return prev;
          const list = [...prev];
          const temp = list[index + 1];
          list[index + 1] = list[index];
          list[index] = temp;
          return list;
        });
      };

      // Collision Check Logic
      const collisionDetected = useMemo(() => {
        return reservations.some(r => r.venueId === venueId && r.date === eventDate && r.timeSlot === activeSlot);
      }, [reservations, venueId, eventDate, activeSlot]);

      // 650ms DEBOUNCED LIVE AUTO-SAVE EFFECT
      useEffect(() => {
        if (isInitialMountRef.current) {
          isInitialMountRef.current = false;
          return;
        }

        if (autoSaveTimerRef.current) clearTimeout(autoSaveTimerRef.current);

        autoSaveTimerRef.current = setTimeout(() => {
          let filledCount = 0;
          let totalCount = 8;
          const currentCustName = customerMode === 'existing'
            ? (customers.find(c => c.id === selectedCustomerId)?.name || '')
            : newCustName;
          const currentPhone = customerMode === 'existing'
            ? (customers.find(c => c.id === selectedCustomerId)?.phone || '')
            : newCustPhone;

          if (currentCustName) filledCount++;
          if (currentPhone && currentPhone.replace(/\D/g, '').length >= 10) filledCount++;
          if (venueId) filledCount++;
          if (startDate) filledCount++;
          if (guestCount > 0) filledCount++;
          if (depositPaid > 0) filledCount++;
          if (selectedServices && selectedServices.length > 0) filledCount++;
          if (notes && notes.length > 5) filledCount++;

          const percentage = Math.min(100, Math.round((filledCount / totalCount) * 100));

          const updatedDraft = {
            refKey: activeRefKey,
            status: 'DRAFT',
            updatedAt: new Date().toISOString(),
            createdAt: new Date().toISOString(),
            completionPercentage: percentage,
            createdBy: {
              id: currentUser?.id || 'u-admin',
              name: currentUser?.name || 'Davut Akbulut',
              role: currentUser?.role || 'admin'
            },
            customerInfo: {
              name: currentCustName || 'İsimsiz Müşteri',
              phone: currentPhone || '',
              venueName: venues.find(v => v.id === venueId)?.name || 'Salon Seçilmedi',
              date: startDate
            },
            accessLogs: [
              {
                userId: currentUser?.id || 'u-admin',
                userName: currentUser?.name || 'Davut Akbulut',
                action: 'AUTO_SAVE',
                timestamp: new Date().toISOString()
              }
            ],
            formData: {
              venueId, customVenuePrice, startDate, startTime, endDate, endTime, guestCount,
              customerMode, selectedCustomerId, newCustName, newCustEmail, newCustPhone,
              newCustSecondaryPhone, selectedServices, referrerName, campaignCode,
              hasDeposit, depositPaid, paymentStatus, isInvoiced, invoiceType, tcNo, vknNo,
              taxOffice, invoiceAddress, notes, flowPlan
            }
          };

          if (setDraftReservations) {
            setDraftReservations(prev => {
              const existingIdx = (prev || []).findIndex(d => d.refKey === activeRefKey);
              if (existingIdx >= 0) {
                const copy = [...prev];
                const existing = copy[existingIdx];
                const combinedLogs = [
                  ...(existing.accessLogs || []),
                  {
                    userId: currentUser?.id || 'u-admin',
                    userName: currentUser?.name || 'Davut Akbulut',
                    action: 'AUTO_SAVE',
                    timestamp: new Date().toISOString()
                  }
                ].slice(-25);

                copy[existingIdx] = {
                  ...updatedDraft,
                  createdAt: existing.createdAt || updatedDraft.createdAt,
                  createdBy: existing.createdBy || updatedDraft.createdBy,
                  accessLogs: combinedLogs
                };
                return copy;
              }
              return [updatedDraft, ...(prev || [])];
            });
          }

          const now = new Date();
          const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`;
          setLastSavedTime(timeStr);
        }, 650);

        return () => {
          if (autoSaveTimerRef.current) clearTimeout(autoSaveTimerRef.current);
        };
      }, [
        activeRefKey, venueId, customVenuePrice, startDate, startTime, endDate, endTime,
        guestCount, customerMode, selectedCustomerId, newCustName, newCustEmail,
        newCustPhone, newCustSecondaryPhone, selectedServices, referrerName,
        campaignCode, hasDeposit, depositPaid, paymentStatus, isInvoiced, invoiceType,
        tcNo, vknNo, taxOffice, invoiceAddress, notes, flowPlan
      ]);

      // CUSTOMER DRAFT CONFLICT POPUP DETECTOR
      useEffect(() => {
        const checkPhone = customerMode === 'existing'
          ? (customers.find(c => c.id === selectedCustomerId)?.phone || '')
          : newCustPhone;
        const cleanPhone = checkPhone ? checkPhone.replace(/\D/g, '') : '';

        if ((cleanPhone.length >= 10 || (customerMode === 'existing' && selectedCustomerId)) && draftReservations) {
          const matchingConflict = draftReservations.find(d => 
            d.status === 'DRAFT' &&
            d.refKey !== activeRefKey &&
            ((cleanPhone && d.customerInfo?.phone && d.customerInfo.phone.replace(/\D/g, '') === cleanPhone) ||
             (cleanPhone && d.formData?.newCustPhone && d.formData.newCustPhone.replace(/\D/g, '') === cleanPhone) ||
             (customerMode === 'existing' && d.formData?.selectedCustomerId === selectedCustomerId))
          );

          if (matchingConflict && (!conflictModal.isOpen || conflictModal.draft?.refKey !== matchingConflict.refKey)) {
            setConflictModal({ isOpen: true, draft: matchingConflict });
          }
        }
      }, [newCustPhone, selectedCustomerId, customerMode]);

      const selectedVenue = venues.find(v => v.id === venueId);
      const existingCustomer = customers.find(c => c.id === selectedCustomerId);

      // Filter available extra services based on selected venue (Etkinlik Mekanı)
      const availableServicesForVenue = useMemo(() => {
        if (!selectedVenue) return services;
        if (!selectedVenue.availableServices || selectedVenue.availableServices.length === 0) {
          return services;
        }
        return services.filter(s => selectedVenue.availableServices.includes(s.id));
      }, [selectedVenue, services]);

      // Financial Calculation with Paid Services Breakdown & Deduction
      const calculations = useMemo(() => {
        const vPrice = Number(customVenuePrice) || 0;
        let servTotal = 0;
        let paidServicesTotal = 0;
        const paidServicesList = [];

        const mappedServices = selectedServices.map(item => {
          const s = services.find(x => x.id === item.serviceId);
          if (!s) return null;
          const unitPrice = item.customUnitPrice !== undefined ? Number(item.customUnitPrice) : s.price;
          const defaultQty = s.pricingType === 'per_person' ? guestCount : 1;
          const qty = item.quantity !== undefined ? Number(item.quantity) : defaultQty;
          const cost = unitPrice * qty;
          servTotal += cost;

          if (item.isPaid) {
            paidServicesTotal += cost;
            paidServicesList.push({ ...s, quantity: qty, unitPrice, cost });
          }

          return { serviceId: s.id, quantity: qty, unitPrice, isPaid: item.isPaid, cost };
        }).filter(Boolean);

        const vPriceClean = Math.max(0, vPrice);
        const servTotalClean = Math.max(0, servTotal);
        const sub = vPriceClean + servTotalClean;
        let disc = 0;
        const activeCampaign = (campaigns || []).find(c =>
          (c.code || '').toUpperCase() === campaignCode.trim().toUpperCase() && c.status === 'Aktif'
        );
        if (activeCampaign) {
          if (activeCampaign.discountType === 'percent' || activeCampaign.discountRate || activeCampaign.discountPercent) {
            const rate = activeCampaign.discountRate || activeCampaign.discountPercent || 0;
            disc = sub * (rate / 100);
          } else if (activeCampaign.discountAmount) {
            disc = Number(activeCampaign.discountAmount);
          } else if (typeof activeCampaign.discount === 'number') {
            disc = activeCampaign.discount;
          }
        } else if (campaignCode.trim().toUpperCase() === 'IREM2026') {
          disc = sub * 0.10;
        } else if (campaignCode.trim().toUpperCase() === 'VIP5000') {
          disc = 5000;
        }

        disc = Math.max(0, Math.min(sub, disc));
        const afterDisc = Math.max(0, sub - disc);
        const vat = isInvoiced ? afterDisc * 0.20 : 0;
        const grandTotal = afterDisc + vat;

        const isFullyPaid = (paymentStatus === 'Ödendi' || paymentStatus === 'Tamamlandı');
        const dep = (hasDeposit || paymentStatus === 'Kapora Alındı') ? (Number(depositPaid) || 0) : 0;
        const netDeductions = isFullyPaid ? grandTotal : (dep + paidServicesTotal);
        const remaining = isFullyPaid ? 0 : Math.max(0, grandTotal - netDeductions);

        return { vPrice, servTotal, sub, disc, vat, grandTotal, dep, paidServicesTotal, paidServicesList, netDeductions, remaining, isFullyPaid, mappedServices };
      }, [customVenuePrice, selectedServices, campaignCode, hasDeposit, depositPaid, paymentStatus, isInvoiced, services]);

      const handleAddFlowItem = () => {
        setFlowPlan(prev => [...prev, { time: '22:30', title: 'Yeni Akış Adımı' }]);
      };
      const handleRemoveFlowItem = (index) => {
        setFlowPlan(prev => prev.filter((_, i) => i !== index));
      };

      const handleSubmit = () => {
        // Prevent Past Date Reservation
        if (startDate && startDate < todayDateStr) {
          showAlertModal('⚠️ GEÇMİŞ TARİH SEÇİLDİ', `Geçmiş bir tarihe (${startDate}) rezervasyon oluşturulamaz! Lütfen bugün (${todayDateStr}) veya gelecekte bir tarih seçiniz.`, 'start-date-input');
          return;
        }

        // Prevent Negative or Zero Guest Count
        if (Number(guestCount) < 1) {
          showAlertModal('⚠️ KATILIMCI SIKINTISI', 'Kişi sayısı en az 1 olmalıdır! Negatif veya sıfır kişi sayısı girilemez.', 'guest-count-input');
          return;
        }

        // Prevent Negative Deposit
        if (Number(depositPaid) < 0) {
          showAlertModal('⚠️ GEÇERSİZ KAPORA', 'Kapora miktarı negatif olamaz! Lütfen 0 veya pozitif bir tutar giriniz.', 'deposit-paid-input');
          return;
        }
        // Customer validation check with smooth scroll & focus
        if (customerMode === 'new') {
          if (!newCustName.trim() || !newCustPhone.trim()) {
            setCustomerError(true);
            showAlertModal('⚠️ MÜŞTERİ BİLGİLERİ EKSİK', 'Müşteri Adı Soyadı ve İletişim Telefon Numarası zorunludur. Lütfen kırmızı ile işaretlenen alanları doldurunuz.', !newCustName.trim() ? 'new-cust-name-input' : 'new-cust-phone-input');
            return;
          }
          if (!isValidPhoneNumber(newCustPhone)) {
            setCustomerError(true);
            showAlertModal('⚠️ GEÇERSİZ TELEFON NUMARASI', 'Telefon numarası 11 hane (05XX XXX XX XX) formatında olmalıdır.', 'new-cust-phone-input');
            return;
          }
          const p1 = newCustPhone.replace(/\D/g, '');
          const p2 = newCustSecondaryPhone.replace(/\D/g, '');
          if (p1 && p2 && p1 === p2) {
            setCustomerError(true);
            showAlertModal('⚠️ ÇİFT TELEFON NUMARASI', 'Birincil ve ikincil telefon numarası aynı olamaz! Lütfen farklı bir numara giriniz.', 'new-cust-sec-phone-input');
            return;
          }
        } else if (customerMode === 'existing') {
          if (!selectedCustomerId) {
            setCustomerError(true);
            showAlertModal('⚠️ MÜŞTERİ SEÇİLMEDİ', 'Lütfen sistemde kayıtlı müşteriler arasından bir müşteri seçiniz.', 'customer-section');
            return;
          }
        }
        setCustomerError(false);

        if (conflictInfo.hasConflict) {
          showAlertModal('⛔ SEANS ÇAKIŞMA UYARISI', `${selectedVenue?.name} salonunda ${formatDate(startDate)} tarihinde (${conflictInfo.conflictingRes?.timeSlot}) aktif bir rezervasyon bulunmaktadır! Lütfen başka bir saat seansı veya başka bir salon seçiniz.`);
          return;
        }
        
        let custId = selectedCustomerId;
        let custName = existingCustomer?.name || 'Müşteri';
        let custEmail = existingCustomer?.email || '';
        let custPhone = existingCustomer?.phone || '';
        let custSecondaryPhone = existingCustomer?.secondaryPhone || '';
        let newCustomerObj = null;

        if (customerMode === 'new') {
          custId = 'cust-' + Date.now();
          custName = newCustName || 'Yeni Müşteri';
          custEmail = newCustEmail;
          custPhone = newCustPhone;
          custSecondaryPhone = newCustSecondaryPhone;
          newCustomerObj = {
            id: custId,
            name: custName,
            email: custEmail,
            phone: custPhone,
            secondaryPhone: custSecondaryPhone,
            address: invoiceAddress,
            taxType: invoiceType,
            tcNo: invoiceType === 'individual' ? tcNo : '',
            vknNo: invoiceType === 'corporate' ? vknNo : '',
            taxOffice,
            followUp: false,
            followUpNote: 'Otomatik kayıt oluşturan üye',
            avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
          };
        }

        const newRes = {
          id: editingResFromUrl?.id || `RES-${new Date().getFullYear()}-${Math.floor(1000 + Math.random() * 9000)}`,
          venueId,
          customerId: custId,
          customerName: custName,
          customerEmail: custEmail,
          customerPhone: custPhone,
          secondaryPhone: custSecondaryPhone,
          date: eventDate,
          eventDate,
          startDate,
          endDate,
          startTime,
          endTime,
          timeSlot: activeSlot,
          guestCount,
          selectedServices: calculations.mappedServices,
          venuePrice: calculations.vPrice,
          subtotal: calculations.sub,
          campaignCode,
          discountAmount: calculations.disc,
          vatAmount: calculations.vat,
          totalAmount: calculations.grandTotal,
          depositPaid: calculations.dep,
          remainingBalance: calculations.remaining,
          paymentStatus: paymentStatus,
          isInvoiced,
          invoiceType,
          tcNo: invoiceType === 'individual' ? tcNo : '',
          vknNo: invoiceType === 'corporate' ? vknNo : '',
          taxOffice,
          invoiceAddress,
          notes,
          flowPlan,
          mediaGallery: editingResFromUrl?.mediaGallery || []
        };

        onSaveReservation(newRes, newCustomerObj, isEditMode ? null : activeRefKey, isEditMode);
      };

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
        <div className="space-y-6 max-w-7xl mx-auto pb-24 sm:pb-12 relative">
          
          {/* CUSTOMER DRAFT CONFLICT POPUP WARNING MODAL */}
          {conflictModal.isOpen && conflictModal.draft && (
            <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[999999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 overflow-hidden animate-fade-in">
              <div className="bg-white dark:bg-brand-card border-2 border-amber-500/80 w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden p-6 space-y-4 animate-scale-up text-left">
                
                {/* Header */}
                <div className="flex items-center space-x-3 text-amber-600 dark:text-amber-400 border-b border-slate-200 dark:border-brand-border pb-3">
                  <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-2xl shrink-0">
                    ⚠️
                  </div>
                  <div>
                    <h3 className="font-heading font-extrabold text-base sm:text-lg text-slate-900 dark:text-white">
                      Müşteriye Ait Tamamlanmamış Taslak Bulundu!
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400">
                      Bu müşteriye ait arka planda otomatik kaydedilmiş yarım kalan bir rezervasyon mevcut.
                    </p>
                  </div>
                </div>

                {/* Draft Card Info */}
                <div className="bg-amber-500/5 dark:bg-amber-950/20 border border-amber-500/20 rounded-2xl p-4 space-y-2 text-xs text-slate-700 dark:text-gray-200">
                  <div className="flex justify-between items-center font-bold">
                    <span>Müşteri: {conflictModal.draft.customerInfo?.name || conflictModal.draft.formData?.newCustName || 'Müşteri'}</span>
                    <span className="font-mono bg-amber-500/20 text-amber-700 dark:text-amber-300 px-2 py-0.5 rounded text-[11px]">
                      Ref: {conflictModal.draft.refKey}
                    </span>
                  </div>
                  <div className="flex justify-between items-center text-slate-500 dark:text-gray-400">
                    <span>Salon: {conflictModal.draft.customerInfo?.venueName || 'Seçilen Salon'}</span>
                    <span>Tarih: {conflictModal.draft.customerInfo?.date || 'Belirtilmedi'}</span>
                  </div>
                  
                  {/* Completion Bar */}
                  <div className="pt-2">
                    <div className="flex justify-between text-[11px] font-bold mb-1">
                      <span>Form Doluluk Oranı</span>
                      <span>%{conflictModal.draft.completionPercentage || 0}</span>
                    </div>
                    <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                      <div
                        className="bg-amber-500 h-full rounded-full transition-all duration-500"
                        style={{ width: `${conflictModal.draft.completionPercentage || 0}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="pt-2 flex flex-col sm:flex-row gap-3">
                  <button
                    onClick={() => {
                      const d = conflictModal.draft;
                      if (d && d.formData) {
                        const f = d.formData;
                        if (f.venueId) setVenueId(f.venueId);
                        if (f.customVenuePrice !== undefined) setCustomVenuePrice(f.customVenuePrice);
                        if (f.startDate) setStartDate(f.startDate);
                        if (f.startTime) setStartTime(f.startTime);
                        if (f.endDate) setEndDate(f.endDate);
                        if (f.endTime) setEndTime(f.endTime);
                        if (f.guestCount !== undefined) setGuestCount(f.guestCount);
                        if (f.customerMode) setCustomerMode(f.customerMode);
                        if (f.selectedCustomerId) setSelectedCustomerId(f.selectedCustomerId);
                        if (f.newCustName !== undefined) setNewCustName(f.newCustName);
                        if (f.newCustEmail !== undefined) setNewCustEmail(f.newCustEmail);
                        if (f.newCustPhone !== undefined) setNewCustPhone(f.newCustPhone);
                        if (f.newCustSecondaryPhone !== undefined) setNewCustSecondaryPhone(f.newCustSecondaryPhone);
                        if (f.selectedServices) setSelectedServices(f.selectedServices);
                        if (f.referrerName !== undefined) setReferrerName(f.referrerName);
                        if (f.campaignCode !== undefined) setCampaignCode(f.campaignCode);
                        if (f.hasDeposit !== undefined) setHasDeposit(f.hasDeposit);
                        if (f.depositPaid !== undefined) setDepositPaid(f.depositPaid);
                        if (f.paymentStatus) setPaymentStatus(f.paymentStatus);
                        if (f.notes !== undefined) setNotes(f.notes);
                        if (f.flowPlan) setFlowPlan(f.flowPlan);
                      }
                      setActiveRefKey(d.refKey);
                      setConflictModal({ isOpen: false, draft: null });
                      showToast(`📂 ${d.refKey} Referanslı Tamamlanmamış Taslak Yüklendi!`);
                    }}
                    className="flex-1 gold-button font-extrabold py-3 px-4 rounded-xl text-xs shadow-lg text-center flex items-center justify-center space-x-2"
                  >
                    <span>📂 Kaldığı Yerden Devam Et</span>
                  </button>

                  <button
                    onClick={() => setConflictModal({ isOpen: false, draft: null })}
                    className="py-3 px-4 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 font-bold rounded-xl text-xs hover:bg-slate-300 text-center"
                  >
                    ✨ Yeni Rezervasyona Devam Et
                  </button>
                </div>

              </div>
            </div>
          )}

          {/* STANDALONE FLOATING TOP-RIGHT NOTIFICATION POPUP */}
          {alertModal.isOpen && (
            <div className="fixed top-5 right-4 sm:right-6 left-4 sm:left-auto z-[99999] max-w-md w-full animate-slide-down sm:animate-slide-left">
              <div className="bg-white/95 dark:bg-slate-900/95 border-2 border-red-500/70 rounded-2xl p-4 sm:p-5 shadow-[0_20px_50px_rgba(239,68,68,0.35)] backdrop-blur-xl flex items-start space-x-3.5 relative border-l-8 border-l-red-600">
                {/* Red Pulse Warning Icon */}
                <div className="w-10 h-10 rounded-xl bg-red-500/20 text-red-600 dark:text-red-400 flex items-center justify-center text-xl font-bold shrink-0 border border-red-500/30 animate-pulse mt-0.5">
                  ⚠️
                </div>

                {/* Content Area */}
                <div className="flex-1 space-y-1 pr-6 text-left">
                  <h4 className="font-heading font-extrabold text-sm sm:text-base text-slate-900 dark:text-white flex items-center space-x-1.5">
                    <span>{alertModal.title}</span>
                  </h4>
                  <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed font-semibold">
                    {alertModal.message}
                  </p>
                  
                  {/* Action Button */}
                  <div className="pt-2">
                    <button
                      onClick={closeAlertModal}
                      className="px-4 py-1.5 rounded-xl bg-red-600 hover:bg-red-500 text-white font-bold text-xs shadow-md transition hover:scale-[1.02] active:scale-[0.98] inline-flex items-center space-x-1"
                    >
                      <span>Anladım, Düzelt ✓</span>
                    </button>
                  </div>
                </div>

                {/* Close X Button */}
                <button
                  onClick={closeAlertModal}
                  className="absolute top-3 right-3 text-slate-400 hover:text-slate-700 dark:hover:text-white transition p-1"
                  aria-label="Kapat"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </div>
            </div>
          )}

          {/* VENUE DETAIL POPUP MODAL */}
          {selectedVenueForDetail && (
            <VenueDetailModalComponent
              venue={selectedVenueForDetail}
              services={services}
              onClose={() => setSelectedVenueForDetail(null)}
              onSelectVenue={(v) => {
                setVenueId(v.id);
                setCustomVenuePrice(v.price);
              }}
            />
          )}

          {/* PAGE HEADER (STRICTLY CONTAINER BOUNDED WITH NO OVERFLOW) */}
          <div className="glass-panel p-4 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm overflow-hidden w-full max-w-full">
            <div className="flex flex-col items-start gap-2 min-w-0 flex-1 max-w-full">
              
              {/* BADGES ROW HORIZONTALLY SCROLLABLE ON MOBILE */}
              <div className="w-full flex items-center space-x-2 overflow-x-auto whitespace-nowrap no-scrollbar snap-x snap-mandatory py-1 max-w-full shrink-0">
                <span className="inline-flex items-center space-x-1.5 bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 text-xs font-bold px-3 py-1 rounded-full border border-slate-200 dark:border-brand-border shrink-0 whitespace-nowrap snap-start">
                  <svg className="w-3.5 h-3.5 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path></svg>
                  <span>Rezervasyon Oluşturma & Kiralama</span>
                </span>

                {/* DRAFT REF KEY BADGE WITH CLICK TO COPY */}
                <button
                  type="button"
                  onClick={() => {
                    if (activeRefKey && navigator.clipboard) {
                      navigator.clipboard.writeText(activeRefKey);
                      if (showToast) showToast('Sözleşme referans kodu kopyalandı! 🔑', 'success');
                    }
                  }}
                  className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition whitespace-nowrap snap-start"
                  title="Referans kodunu kopyalamak için tıklayın"
                >
                  <span>🔑 Ref:</span>
                  <span className="tracking-wider">{activeRefKey}</span>
                  <span className="text-[10px] text-amber-500">📋</span>
                </button>

                {lastSavedTime ? (
                  <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">
                    <span>💾 Taslak Kaydedildi</span>
                    <span className="text-[10px] font-mono">({lastSavedTime})</span>
                  </span>
                ) : (
                  <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">
                    <span>⏱️ Canlı Otomatik Kayıt</span>
                  </span>
                )}
              </div>

              <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text mt-0.5 break-words max-w-full">
                Hayalinizdeki Düğünü Birlikte Planlayalım!
              </h2>
              <p className="text-[11px] sm:text-xs text-slate-500 dark:text-gray-400 leading-relaxed break-words max-w-2xl">
                Salon kiralama, hizmet adetleri, müşteri üyelik kaydı, fatura ve etkinlik akışını tek ekranda yönetin.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-center gap-2 w-full md:w-auto shrink-0">
              <button
                type="button"
                onClick={onCancel}
                className="w-full sm:w-auto px-4 py-2.5 bg-slate-100 dark:bg-brand-card hover:bg-slate-200 dark:hover:bg-slate-800 text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold transition text-center whitespace-nowrap cursor-pointer shadow-xs border border-slate-200 dark:border-brand-border"
              >
                ← Rezervasyon Listesine Dön
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            
            {/* LEFT COLUMN: FORM SECTIONS (8 Cols) */}
            <div className="lg:col-span-8 space-y-6">
              
              {/* SECTION 1: ETKİNLİK MEKANI SEÇİN (TAKVİM & SEANS SEÇİMİ İLE) */}
              <div className="glass-panel p-3.5 sm:p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">

                {/* VISUAL HORIZONTAL SCROLLABLE VENUE CAROUSEL WITH ARROW CONTROLS */}
                <div>
                  <div className="flex justify-between items-center mb-2 px-1">
                    <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5m0 0h4m-4 0V11m0 0h4m-4 0H7m4 0v5"></path></svg>
                      <span>1. Etkinlik Mekanı Seçin:</span>
                    </h3>
                    
                    {/* Interactive Arrow Navigation Buttons */}
                    <div className="flex items-center space-x-1.5">
                      <button
                        type="button"
                        onClick={scrollVenueCarouselLeft}
                        className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                        title="Sola Kaydır"
                        aria-label="Etkinlik Mekanlarını Sola Kaydır"
                      >
                        ❮
                      </button>
                      <button
                        type="button"
                        onClick={scrollVenueCarouselRight}
                        className="w-7 h-7 rounded-full border border-amber-500/40 bg-white dark:bg-brand-card text-amber-800 dark:text-gold-400 hover:bg-amber-500 hover:text-white font-bold text-xs shadow flex items-center justify-center transition active:scale-95 cursor-pointer"
                        title="Sağa Kaydır"
                        aria-label="Etkinlik Mekanlarını Sağa Kaydır"
                      >
                        ❯
                      </button>
                    </div>
                  </div>

                  <div ref={venueCarouselRef} className="flex overflow-x-auto gap-3.5 pb-3 pt-1 no-scrollbar snap-x snap-mandatory scroll-smooth px-1">
                    {venues.length === 0 ? (
                      <div className="p-6 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-800 dark:text-gold-400 text-xs font-bold text-center space-y-2.5 w-full">
                        <div>⚠️ Sistemde henüz tanımlı bir etkinlik mekanı bulunmamaktadır.</div>
                        <button
                          type="button"
                          onClick={() => navigateTo && navigateTo('dugun-salonlari')}
                          className="gold-button px-4 py-2 rounded-xl font-extrabold shadow hover:scale-105 transition cursor-pointer inline-flex items-center space-x-2"
                        >
                          <span>🏰 Yeni Düğün Salonu Ekle</span>
                        </button>
                      </div>
                    ) : (
                      venues.map(v => {
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
                            <OptimizedImage src={v.image} alt={v.name} className="w-full h-full" priority={isSelected} />
                            
                            <div className="absolute top-2 right-2 bg-slate-900/80 backdrop-blur-md text-white text-[10px] font-bold px-2 py-0.5 rounded-full border border-white/20 z-10 flex items-center space-x-1">
                              <svg className="w-3 h-3 text-white inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
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
                              title="Mekan Detaylarını Göster"
                            >
                              <svg className="w-3 h-3 text-white inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
                              <span>Mekan Detayları</span>
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
                    }))}
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Bu Rezervasyona Özel Mekan Kiralama Fiyatı (TL):</label>
                    <input
                      type="number"
                      value={customVenuePrice}
                      onChange={e => setCustomVenuePrice(Number(e.target.value))}
                      className="w-full bg-amber-500/10 border border-amber-500/40 rounded-xl p-2.5 text-amber-800 dark:text-gold-400 font-extrabold"
                    />
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Davetli Sayısı (Kişi):</label>
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
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                    />
                  </div>
                </div>

                {/* QUICK TIME SLOT SEANSLARI PRESETS */}
                <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-brand-border">
                  <label className="font-bold text-slate-800 dark:text-gray-200 text-xs flex items-center space-x-1.5">
                    <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <span>Hızlı Seans Seçimi (Aynı Gün Farklı Seans Rezerve Edilebilir):</span>
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
                      <span className="flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
                        <span>Gündüz Seansı</span>
                      </span>
                      <span className="text-[10px] opacity-80 font-mono font-bold">10:00 - 15:00</span>
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
                      <span className="flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
                        <span>Gece Balo Seansı</span>
                      </span>
                      <span className="text-[10px] opacity-80 font-mono font-bold">18:00 - 23:00</span>
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
                      <span className="flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline text-amber-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
                        <span>Tüm Gün Kiralama</span>
                      </span>
                      <span className="text-[10px] opacity-80 font-mono font-bold">09:00 - 23:30</span>
                    </button>
                  </div>
                </div>

                {/* START AND END DATE & TIME SELECTION */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-1">
                  <div className="space-y-2">
                    <label className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1.5">
                      <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                      <span>Etkinlik Başlangıç Tarihi & Saati:</span>
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <input type="date" min={todayDateStr} value={startDate} id="start-date-input" onChange={e => setStartDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                      <input type="time" value={startTime} onChange={e => setStartTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1.5">
                      <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 21v-4m0 0V5a2 2 0 012-2h6.5l1 1H21l-3 6 3 6h-8.5l-1-1H5a2 2 0 00-2 2zm9-13.5V9"></path></svg>
                      <span>Etkinlik Bitiş Tarihi & Saati:</span>
                    </label>
                    <div className="grid grid-cols-2 gap-2">
                      <input type="date" min={startDate || todayDateStr} onChange={e => setEndDate(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                      <input type="time" value={endTime} onChange={e => setEndTime(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
                    </div>
                  </div>
                </div>

                {/* REAL-TIME CONFLICT / AVAILABILITY WARNING BANNER */}
                {conflictInfo.hasConflict ? (
                  <div className="p-4 rounded-2xl border-2 border-red-500/60 bg-red-500/10 text-red-700 dark:text-red-300 space-y-2.5 shadow-xl animate-fade-in">
                    <div className="flex items-center space-x-3">
                      <div className="w-10 h-10 rounded-2xl bg-red-500 text-white font-extrabold flex items-center justify-center text-xl shrink-0 shadow-md">
                        <svg className="w-6 h-6 text-white inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      </div>
                      <div>
                        <h4 className="font-heading font-extrabold text-sm text-red-600 dark:text-red-400">
                          ÇAKIŞMA ENGELLENDİ: SEÇİLEN SALON VE SEANS ZATEN REZERVE EDİLMİŞ!
                        </h4>
                        <p className="text-xs text-red-700 dark:text-red-300 leading-normal">
                          <strong>{selectedVenue?.name}</strong> salonunda <strong>{formatDate(startDate)}</strong> tarihinde <strong>{conflictInfo.conflictingRes?.timeSlot}</strong> seansı için onaylı bir rezervasyon bulunmaktadır.
                        </p>
                      </div>
                    </div>
                    <div className="bg-white/90 dark:bg-brand-card/90 p-3 rounded-xl border border-red-500/30 text-xs flex justify-between items-center shadow-sm">
                      <div className="space-x-2">
                        <span className="font-bold text-slate-800 dark:text-gray-100">Dolu Rezervasyon: </span>
                        <span className="font-mono text-slate-900 dark:text-white font-bold">{conflictInfo.conflictingRes?.id}</span>
                        <span className="text-slate-600 dark:text-gray-300">• {conflictInfo.conflictingRes?.customerName}</span>
                      </div>
                      <span className="text-[10px] font-extrabold bg-red-500/20 text-red-600 dark:text-red-400 px-2.5 py-1 rounded-md uppercase tracking-wider">
                        SEANS DOLU
                      </span>
                    </div>
                  </div>
                ) : (
                  <div className="p-3.5 rounded-2xl border border-emerald-500/40 bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 flex items-center justify-between shadow-sm">
                    <div className="flex items-center space-x-2.5">
                      <svg className="w-5 h-5 text-emerald-600 dark:text-emerald-400 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
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
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-200 dark:border-brand-border pb-3 gap-2">
                  <div className="flex items-center space-x-2">
                    <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
                    <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">2. Ek Hizmetler:</h3>
                  </div>
                  {selectedVenue && (
                    <span className="text-xs font-bold text-amber-800 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
                      🎯 {selectedVenue.name} Mekanıyla Uyumlu ({availableServicesForVenue.length} Hizmet)
                    </span>
                  )}
                </div>

                <div className="space-y-3">
                  {availableServicesForVenue.length === 0 ? (
                    <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-800 dark:text-gold-400 text-xs font-bold text-center">
                      Bu etkinlik mekanı için seçilebilir ek hizmet bulunmamaktadır.
                    </div>
                  ) : (
                    availableServicesForVenue.map(s => {
                    const found = selectedServices.find(x => x.serviceId === s.id);
                    const isSelected = !!found;
                    const unitPrice = found && found.customUnitPrice !== undefined ? Number(found.customUnitPrice) : s.price;
                    const defaultQty = s.pricingType === 'per_person' ? guestCount : 1;
                    const qty = found && found.quantity !== undefined ? Number(found.quantity) : defaultQty;
                    const isPaid = found ? found.isPaid : false;

                    const isPerPerson = s.pricingType === 'per_person';
                    const isPerUnit = s.pricingType === 'per_unit' || s.pricingType === 'unit';
                    const isFlat = !isPerPerson && !isPerUnit;

                    const calculatedCost = unitPrice * qty;

                    return (
                      <div key={s.id} className={`p-4 rounded-2xl border transition space-y-3 ${isSelected ? 'bg-amber-500/10 border-amber-500/50 shadow-sm' : 'bg-slate-50 dark:bg-brand-dark border-slate-200 dark:border-brand-border'}`}>
                        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                          <label className="flex items-start sm:items-center space-x-3 cursor-pointer">
                            <input
                              type="checkbox"
                              checked={isSelected}
                              onChange={e => {
                                if (e.target.checked) {
                                  setSelectedServices(prev => [...prev, { serviceId: s.id, quantity: defaultQty, isPaid: false }]);
                                } else {
                                  setSelectedServices(prev => prev.filter(x => x.serviceId !== s.id));
                                }
                              }}
                              className="w-5 h-5 accent-amber-600 rounded mt-0.5 sm:mt-0 shrink-0"
                            />
                            <div>
                              <div className="flex items-center space-x-2">
                                <span className="font-bold text-xs text-slate-800 dark:text-gray-200">{s.name}</span>
                                <span className={`text-[10px] font-extrabold px-2 py-0.5 rounded-full border ${
                                  isPerPerson ? 'bg-indigo-500/10 text-indigo-700 dark:text-indigo-300 border-indigo-500/30' :
                                  isPerUnit ? 'bg-purple-500/10 text-purple-700 dark:text-purple-300 border-purple-500/30' :
                                  'bg-amber-500/10 text-amber-800 dark:text-gold-400 border-amber-500/30'
                                }`}>
                                  {isPerPerson ? '👥 Kişi Başı' : isPerUnit ? '🔢 Adet Başı' : '📦 Sabit Paket'}
                                </span>
                              </div>
                              <div className="text-[10px] text-slate-500 dark:text-gray-400 mt-0.5">{s.description} | Birim: {formatCurrency(s.price)} {isPerPerson ? '/Kişi' : isPerUnit ? '/Adet' : '/Paket'}</div>
                            </div>
                          </label>

                          {isSelected && (
                            <div className="flex flex-wrap items-center gap-3 text-xs w-full sm:w-auto justify-end">
                              <div className="flex items-center space-x-1">
                                <span className="font-bold text-slate-700 dark:text-gray-300">Özel Birim Fiyat:</span>
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

                              <div className="flex items-center space-x-1">
                                <span className="font-bold text-slate-700 dark:text-gray-300">
                                  {isPerPerson ? 'Kişi Sayısı:' : isPerUnit ? 'Adet Sayısı:' : 'Paket Adedi:'}
                                </span>
                                <input
                                  type="number"
                                  min="1"
                                  value={qty}
                                  onChange={e => {
                                    const val = Math.max(1, Number(e.target.value));
                                    setSelectedServices(prev => prev.map(x => x.serviceId === s.id ? { ...x, quantity: val } : x));
                                  }}
                                  className="w-20 bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-lg p-1 font-bold text-center"
                                />
                              </div>

                              <label className={`flex items-center space-x-1 font-bold cursor-pointer select-none ${isPaid ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-500 dark:text-gray-400'}`}>
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

                        {isSelected && (
                          <div className="pt-2 border-t border-amber-500/20 flex flex-wrap justify-between items-center text-xs">
                            <div className="flex items-center space-x-1.5 text-[11px] text-slate-600 dark:text-gray-300">
                              <span className="font-bold text-amber-700 dark:text-gold-400">⚡ Hesaplama Formülü:</span>
                              <span className="font-mono">
                                {isPerPerson
                                  ? `${qty} Kişi × ${formatCurrency(unitPrice)}/Kişi`
                                  : isPerUnit
                                  ? `${qty} Adet × ${formatCurrency(unitPrice)}/Adet`
                                  : `${qty} Paket × ${formatCurrency(unitPrice)} (Sabit Paket)`}
                              </span>
                            </div>
                            <div className="flex items-center space-x-1.5 font-extrabold text-xs text-emerald-700 dark:text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-lg border border-emerald-500/30">
                              <span>Hizmet Tutarı:</span>
                              <span className="text-sm">{formatCurrency(calculatedCost)}</span>
                            </div>
                          </div>
                        )}
                      </div>
                    );
                  }))}
                </div>
              </div>

              {/* SECTION 3: ÖDEME, KAPORA & İNDİRİM KODU BİLGİLERİ */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border">
                <div className="flex items-center space-x-2 border-b border-slate-200 dark:border-brand-border pb-3">
                  <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
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
                      <input type="number" min="0" id="deposit-paid-input" value={depositPaid} onChange={e => setDepositPaid(Math.max(0, parseFloat(e.target.value) || 0))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-emerald-600" />
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
                </div>
              </div>

              {/* SECTION 4: MÜŞTERİ İLETİŞİM BİLGİLERİ (Z-30 STACKING LAYER TO FLOAT OVER SECTION 5) */}
              <div id="customer-section" className={`glass-panel p-6 rounded-3xl space-y-4 shadow-sm border transition relative z-30 ${customerError ? 'border-2 border-red-500 shadow-red-500/20 bg-red-500/5' : 'border-slate-200 dark:border-brand-border'}`}>
                <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
                      <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">4. Müşteri İletişim Bilgileri:</h3>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-xs font-bold w-full">
                    <button
                      type="button"
                      onClick={() => { setCustomerMode('new'); setIsAutoSelectedFromPhone(false); setCustomerError(false); }}
                      className={`py-2.5 px-2 rounded-xl border text-center transition flex items-center justify-center space-x-1.5 ${customerMode === 'new' ? 'gold-button shadow font-extrabold' : 'bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 border-slate-200 dark:border-slate-800'}`}
                    >
                      <span>+ Yeni Müşteri</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => { setCustomerMode('existing'); setIsAutoSelectedFromPhone(false); setCustomerError(false); }}
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
                      onChange={e => { setSelectedCustomerId(e.target.value); setIsAutoSelectedFromPhone(false); setCustomerError(false); }}
                      className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold ${customerError && !selectedCustomerId ? 'border-2 border-red-500 bg-red-500/10 ring-2 ring-red-500/30' : 'border-slate-200 dark:border-brand-border'}`}
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

                    {selectedCustomerId && isAutoSelectedFromPhone && (
                      <div className="mt-2.5 bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1 border border-emerald-500/20 shadow-sm animate-fade-in">
                        <svg className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>VAROLAN MÜŞTERİ SEÇİLDİ</span>
                        <span className="font-semibold text-slate-500 dark:text-gray-400 ml-1 truncate max-w-[200px]">
                          ({customers.find(c => c.id === selectedCustomerId)?.name || 'Kayıtlı Müşteri'})
                        </span>
                      </div>
                    )}
                    {customerError && !selectedCustomerId && (
                      <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>⚠️ Müşteri seçimi yapılması zorunludur.</span>
                      </p>
                    )}
                  </div>
                ) : (
                  <div className="space-y-3 text-xs">
                    <div className="bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-2.5 rounded-xl text-slate-700 dark:text-gray-300 font-bold flex items-center space-x-1.5">
                      <svg className="w-4 h-4 text-slate-500 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      <span>Bu kişi için sistemde otomatik olarak yeni üye ve müşteri kartı oluşturulacaktır.</span>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="font-bold block mb-1">Adı Soyadı / Firma Unvanı <span className="text-red-500">*</span>:</label>
                        <input
                          id="new-cust-name-input"
                          type="text"
                          placeholder="Örn: Mehmet Yılmaz & Zeynep Can"
                          value={newCustName}
                          onChange={e => { setNewCustName(e.target.value); setCustomerError(false); }}
                          className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 ${customerError && !newCustName.trim() ? 'border-2 border-red-500 bg-red-500/10 ring-2 ring-red-500/30 font-bold' : 'border-slate-200 dark:border-brand-border'}`}
                        />
                        {customerError && !newCustName.trim() && (
                          <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span>⚠️ Doldurulması zorunludur.</span>
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
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span>⚠️ Geçerli bir e-posta adresi zorunludur.</span>
                          </p>
                        )}
                      </div>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div className="relative z-50">
                        <label className="font-bold block mb-1">Birincil Telefon (+90) <span className="text-red-500">*</span>:</label>
                        <input
                          id="new-cust-phone-input"
                          type="text"
                          placeholder="0 (5XX) XXX XX XX"
                          value={newCustPhone}
                          onChange={e => { setNewCustPhone(formatPhoneNumber(e.target.value)); setCustomerError(false); }}
                          className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold ${
                            customerError && (!newCustPhone.trim() || !isValidPhoneNumber(newCustPhone))
                              ? 'border-2 border-red-500 bg-red-500/10 ring-2 ring-red-500/30 text-red-600'
                              : isValidPhoneNumber(newCustPhone)
                              ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                              : 'border-slate-200 dark:border-brand-border text-slate-800 dark:text-gray-200'
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
                            <div className="absolute left-0 right-0 top-full mt-1.5 z-[9999] bg-white dark:bg-slate-900 border-2 border-amber-500 rounded-2xl shadow-2xl overflow-hidden animate-slide-down">
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
                                      setIsAutoSelectedFromPhone(true);
                                      setCustomerSearchQuery('');
                                      setCustomerMode('existing');
                                      setCustomerError(false);
                                      if (showToast) showToast(`👥 "${cust.name}" Kayıtlı Müşteri Olarak Seçildi ve Aktarıldı!`);
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
                        {customerError && (!newCustPhone.trim() || !isValidPhoneNumber(newCustPhone)) && (
                          <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span>{!newCustPhone.trim() ? '⚠️ Doldurulması zorunludur.' : '⚠️ Geçerli bir telefon numarası giriniz (05XX XXX XX XX).'}</span>
                          </p>
                        )}
                        {newCustPhone && isValidPhoneNumber(newCustPhone) && (
                          <div className="mt-1 text-[10px] font-bold">
                            <span className="text-emerald-600 dark:text-emerald-400 flex items-center space-x-1">
                              <svg className="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                              <span>Geçerli Telefon Numarası</span>
                            </span>
                          </div>
                        )}
                      </div>
                      <div>
                        <label className="font-bold block mb-1">İkinci İletişim / Yakın Telefonu <span className="text-red-500">*</span>:</label>
                        <input
                          id="new-cust-sec-phone-input"
                          type="text"
                          placeholder="0 (5XX) XXX XX XX (Anne/Baba Tel)"
                          value={newCustSecondaryPhone}
                          onChange={e => { setNewCustSecondaryPhone(formatPhoneNumber(e.target.value)); setCustomerError(false); }}
                          className={`w-full bg-slate-50 dark:bg-brand-dark border rounded-xl p-2.5 font-bold ${
                            customerError && (!newCustSecondaryPhone.trim() || !isValidPhoneNumber(newCustSecondaryPhone))
                              ? 'border-2 border-red-500 bg-red-500/10 ring-2 ring-red-500/30 text-red-600'
                              : newCustPhone && newCustSecondaryPhone && newCustPhone.replace(/\D/g, '') === newCustSecondaryPhone.replace(/\D/g, '')
                              ? 'border-2 border-red-500 bg-red-500/10 text-red-600'
                              : newCustSecondaryPhone && isValidPhoneNumber(newCustSecondaryPhone)
                              ? 'border-emerald-500 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300'
                              : 'border-slate-200 dark:border-brand-border text-slate-800 dark:text-gray-200'
                          }`}
                        />
                        {customerError && (!newCustSecondaryPhone.trim() || !isValidPhoneNumber(newCustSecondaryPhone)) && (
                          <p className="text-[11px] font-bold text-red-600 dark:text-red-400 mt-1 flex items-center space-x-1">
                            <svg className="w-3.5 h-3.5 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                            <span>⚠️ İkinci iletişim telefonu zorunludur.</span>
                          </p>
                        )}
                        {newCustSecondaryPhone && (
                          <div className="mt-1 text-[10px] font-bold">
                            {newCustPhone && newCustPhone.replace(/\D/g, '') === newCustSecondaryPhone.replace(/\D/g, '') ? (
                              <span className="text-red-600 dark:text-red-400 flex items-center space-x-1">
                                <svg className="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                                <span>Birincil ve ikincil telefon aynı olamaz!</span>
                              </span>
                            ) : isValidPhoneNumber(newCustSecondaryPhone) ? (
                              <span className="text-emerald-600 dark:text-emerald-400 flex items-center space-x-1">
                                <svg className="w-3 h-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                                <span>Geçerli Telefon Numarası</span>
                              </span>
                            ) : (
                              <span className="text-amber-600 dark:text-amber-400">
                                ⏳ Eksik Telefon Numarası
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* SECTION 5: FATURA BİLGİLERİ (Z-10 LOWER STACKING LAYER) */}
              <div className="glass-panel p-6 rounded-3xl space-y-4 shadow-sm border border-slate-200 dark:border-brand-border relative z-10">
                <div className="border-b border-slate-200 dark:border-brand-border pb-3 space-y-2">
                  <div className="flex items-center space-x-2">
                    <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">5. Fatura Bilgileri</h3>
                  </div>
                  
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
                  <div className="flex items-center space-x-2">
                    <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                    <div>
                      <h3 className="font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100">6. Organizasyon & Etkinlik Akış Planlaması</h3>
                      <p className="text-[11px] text-slate-500 dark:text-gray-400 font-medium">Masaüstünde (⋮⋮) simgesiyle sürükleyebilir veya mobilde (▲/▼) oklarıyla sırasını değiştirebilirsiniz.</p>
                    </div>
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
                      <div className="hidden sm:flex items-center cursor-grab active:cursor-grabbing text-slate-400 hover:text-amber-600 font-bold px-1 text-sm select-none" title="Masaüstünde Sürükle ve Sıralamayı Değiştir">
                        ⋮⋮
                      </div>

                      <div className="flex flex-col space-y-0.5 shrink-0">
                        <button
                          type="button"
                          onClick={() => moveFlowItemUp(idx)}
                          disabled={idx === 0}
                          className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                          title="Yukarı Taşı"
                        >
                          ▲
                        </button>
                        <button
                          type="button"
                          onClick={() => moveFlowItemDown(idx)}
                          disabled={idx === flowPlan.length - 1}
                          className="w-5 h-4 flex items-center justify-center bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded text-[9px] font-bold disabled:opacity-20 hover:bg-amber-500 hover:text-white"
                          title="Aşağı Taşı"
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
                      <button onClick={() => handleRemoveFlowItem(idx)} className="text-red-500 hover:text-red-700 font-bold px-1.5 text-sm shrink-0" title="Adımı Sil">✕</button>
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
                    <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                    <span>Takvim Canlı Ön İzlemesi</span>
                  </span>
                  <span className="text-[10px] bg-slate-100 dark:bg-brand-dark text-slate-800 dark:text-gray-200 font-mono font-bold px-2 py-0.5 rounded border border-slate-200 dark:border-brand-border">{eventDate}</span>
                </div>
                
                <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border text-center space-y-2 text-xs">
                  <div className="font-bold text-slate-800 dark:text-gray-100">{formatDate(eventDate)}</div>
                  <div className="text-slate-900 dark:text-white font-extrabold">{selectedVenue?.name}</div>
                  <div className="text-[11px] font-mono text-slate-600 dark:text-gray-300 bg-white dark:bg-brand-card py-1 px-2 rounded-lg border border-slate-200 dark:border-brand-border">{activeSlot}</div>
                  {collisionDetected ? (
                    <div className="bg-red-500/10 text-red-600 dark:text-red-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1">
                      <svg className="w-3.5 h-3.5 text-red-600 dark:text-red-400 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      <span>BU SAAT DİLİMİ DOLUDUR</span>
                    </div>
                  ) : (
                    <div className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 font-bold p-2 rounded-lg text-[10px] flex items-center justify-center space-x-1">
                      <svg className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 inline shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      <span>BU SAAT DİLİMİ MÜSAİTTİR</span>
                    </div>
                  )}
                </div>
              </div>

              {/* DESKTOP SIDEBAR CANLI FİNANSAL ÖZET & SÖZLEŞME ONAY KARTI */}
              <div className="hidden sm:block glass-panel p-6 rounded-3xl space-y-4 shadow-xl border-2 border-slate-200 dark:border-brand-border sticky top-24">
                <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 border-b border-slate-200 dark:border-brand-border pb-2 flex items-center space-x-2">
                  <svg className="w-5 h-5 text-slate-700 dark:text-gray-300 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path></svg>
                  <span>Canlı Hesaplama & Sözleşme Kartı</span>
                </h3>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between"><span>Salon Bedeli:</span><span className="font-bold">{formatCurrency(calculations.vPrice)}</span></div>
                  <div className="flex justify-between"><span>Seçilen Ek Hizmetler:</span><span className="font-bold">{formatCurrency(calculations.servTotal)}</span></div>
                  <div className="flex justify-between border-t border-slate-200 dark:border-brand-border pt-1"><span>Ara Toplam:</span><span className="font-bold">{formatCurrency(calculations.sub)}</span></div>
                  {calculations.disc > 0 && <div className="flex justify-between text-red-500"><span>Referans / İndirim:</span><span className="font-bold">-{formatCurrency(calculations.disc)}</span></div>}
                  {isInvoiced && <div className="flex justify-between text-slate-600 dark:text-gray-300"><span>Hesaplanan KDV (%20):</span><span className="font-bold">{formatCurrency(calculations.vat)}</span></div>}
                  
                  <div className="flex justify-between text-base font-bold text-amber-700 dark:text-gold-400 border-t border-slate-200 dark:border-brand-border pt-2">
                    <span>Genel Toplam Tutar:</span>
                    <span>{formatCurrency(calculations.grandTotal)}</span>
                  </div>

                  {/* DÜŞÜLEN HİZMETLER SATIR SATIR */}
                  {calculations.paidServicesList && calculations.paidServicesList.length > 0 && (
                    <div className="space-y-1 pt-1">
                      <div className="text-[11px] font-bold text-emerald-700 dark:text-emerald-400 flex items-center space-x-1">
                        <svg className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                        <span>Ödendi İşaretlenen ve Düşülen Hizmetler:</span>
                      </div>
                      {calculations.paidServicesList.map(ps => (
                        <div key={ps.id} className="flex justify-between items-center text-[11px] text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-500/10 p-1.5 rounded-lg border border-emerald-500/20">
                          <span className="flex items-center space-x-1">
                            <svg className="w-3 h-3 text-emerald-600 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path></svg>
                            <span>{ps.name} (Tahsil Edildi)</span>
                          </span>
                          <span className="font-mono">-{formatCurrency(ps.cost)}</span>
                        </div>
                      ))}
                    </div>
                  )}

                  {calculations.isFullyPaid ? (
                    <div className="flex justify-between items-center text-xs text-emerald-600 dark:text-emerald-400 font-bold bg-emerald-500/10 p-2.5 rounded-xl border border-emerald-500/30 mt-2">
                      <span className="flex items-center space-x-1.5">
                        <svg className="w-4 h-4 text-emerald-600 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>Genel Ödeme ({paymentStatus}):</span>
                      </span>
                      <span className="font-mono text-sm">-{formatCurrency(calculations.grandTotal)}</span>
                    </div>
                  ) : (
                    hasDeposit && (
                      <div className="flex justify-between text-emerald-600 dark:text-emerald-400 pt-1 font-bold">
                        <span>Tahsil Edilen Kapora:</span>
                        <span className="font-mono">-{formatCurrency(calculations.dep)}</span>
                      </div>
                    )
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

    // --- CUSTOMER FORM MODAL ---
