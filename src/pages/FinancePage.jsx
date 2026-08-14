import React, { useState, useEffect, useMemo } from 'react';
import ReactDOM from 'react-dom';
import { formatCurrency, formatDate } from '../utils/formatters.js';
import { ThemeIcon } from '../components/ThemeIcon.jsx';
import { Pagination } from '../components/Pagination.jsx';

export function FinanceComponent({
  financialStats,
  reservations = [],
  setReservations = () => {},
  venues = [],
  services = [],
  expenses = [],
  setExpenses = () => {},
  onUpdateReservation = () => {},
  showToast = () => {}
}) {
  const [expandedResIds, setExpandedResIds] = useState({});
  const toggleExpandRes = (resId) => {
    setExpandedResIds(prev => ({
      ...prev,
      [resId]: !prev[resId]
    }));
  };

  const [activeSubTab, setActiveSubTab] = useState('profitability'); // 'profitability' | 'kasa' | 'monthly'
  const [filterTab, setFilterTab] = useState('all'); // 'all' | 'income' | 'expense'
  const [searchQuery, setSearchQuery] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Selected Reservation for Custom Expense / Income Modal
  const [customExpenseModalRes, setCustomExpenseModalRes] = useState(null);
  const [resModalTab, setResModalTab] = useState('gider'); // 'gider' | 'gelir'
  const [newResExpTitle, setNewResExpTitle] = useState('');
  const [newResExpAmount, setNewResExpAmount] = useState('');
  const [newResExpCategory, setNewResExpCategory] = useState('Personel & Yevmiye');
  const [newResPayMethod, setNewResPayMethod] = useState('Nakit Kasa');
  const [newResPayType, setNewResPayType] = useState('Kısmi Ara Ödeme');
  const [newResPayDate, setNewResPayDate] = useState(new Date().toISOString().split('T')[0]);

  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  // Selected Month for Monthly Cashflow Report
  const [selectedReportMonth, setSelectedReportMonth] = useState('2026-08');

  useEffect(() => {
    setCurrentPage(1);
  }, [filterTab, searchQuery, activeSubTab, selectedReportMonth]);

  // Direct MariaDB sync on Finance tab mount
  useEffect(() => {
    try {
      const fetchFn = window.fetchWithRetry || fetch;
      fetchFn('/api/expenses')
        .then(res => res.json())
        .then(data => {
          if (Array.isArray(data)) {
            setExpenses(data);
          }
        })
        .catch(() => {});
    } catch(e) {}
  }, []);

  // General Cashflow Transaction Modal State (Income vs Expense)
  const [transType, setTransType] = useState('gider'); // 'gelir' | 'gider'
  const [incomeSource, setIncomeSource] = useState('reservation'); // 'reservation' | 'external'
  const [selectedResId, setSelectedResId] = useState('');
  const [paymentMethod, setPaymentMethod] = useState('Nakit Kasa');
  const [paymentType, setPaymentType] = useState('Kısmi Ara Ödeme');
  const [newTitle, setNewTitle] = useState('');
  const [newCategory, setNewCategory] = useState('Faturalar & Enerji');
  const [newAmount, setNewAmount] = useState('');
  const [newDate, setNewDate] = useState(new Date().toISOString().split('T')[0]);
  const [newStatus, setNewStatus] = useState('Tamamlandı');

  // Update default category when transType changes
  useEffect(() => {
    if (transType === 'gelir') {
      setNewCategory('Dış Çekim & Plato');
    } else {
      setNewCategory('Faturalar & Enerji');
    }
  }, [transType]);

  // 1. RESERVATION ITEMIZED FINANCIAL & PROFITABILITY CALCULATION
  const reservationFinancials = useMemo(() => {
    return (reservations || []).map(r => {
      const vObj = (venues || []).find(v => v.id === r.venueId);
      // 1. ÖNCELİK: Mekan Kartına Tanımlı Gerçek Maliyet Bedeli
      const venueCost = (vObj && vObj.costPrice !== undefined && Number(vObj.costPrice) > 0)
        ? Number(vObj.costPrice)
        : (r.venueCost !== undefined && Number(r.venueCost) > 0
            ? Number(r.venueCost)
            : Math.round(Number(r.venuePrice || r.customVenuePrice || 60000) * 0.55));

      // 1. ÖNCELİK: Ek Hizmet Kartına Tanımlı Gerçek Birim Maliyeti
      const servicesCost = (r.selectedServices || []).reduce((sum, s) => {
        const sObj = (services || []).find(srv => srv.id === s.serviceId);
        const uCost = (sObj && sObj.costPrice !== undefined && Number(sObj.costPrice) > 0)
          ? Number(sObj.costPrice)
          : (s.costPrice !== undefined && Number(s.costPrice) > 0
              ? Number(s.costPrice)
              : Math.round(Number(s.unitPrice || s.price || 250) * 0.6));
        return sum + (uCost * Number(s.quantity || 1));
      }, 0);

      const customExpensesList = r.customExpenses || [];
      const customExpensesTotal = customExpensesList.reduce((sum, exp) => sum + Number(exp.amount || 0), 0);

      const grossIncome = Number(r.totalAmount || 0);
      const totalCost = Math.round(venueCost + servicesCost + customExpensesTotal);
      const netProfit = Math.round(grossIncome - totalCost);
      const profitMargin = grossIncome > 0 ? ((netProfit / grossIncome) * 100).toFixed(1) : '0.0';

      return {
        reservation: r,
        created_at: r.created_at || r.createdAt || '',
        createdAt: r.createdAt || r.created_at || '',
        venueName: vObj?.name || r.venueName || r.venueId,
        grossIncome,
        venueCost,
        servicesCost,
        customExpensesList,
        customExpensesTotal,
        totalCost,
        netProfit,
        profitMargin: Number(profitMargin)
      };
    });
  }, [reservations, venues, services]);

  // Global Summary Totals for Contracts
  const totalGrossRevenue = useMemo(() => {
    return reservationFinancials.reduce((sum, rf) => sum + rf.grossIncome, 0);
  }, [reservationFinancials]);

  const totalCalculatedCosts = useMemo(() => {
    return reservationFinancials.reduce((sum, rf) => sum + rf.totalCost, 0);
  }, [reservationFinancials]);

  const totalNetProfit = totalGrossRevenue - totalCalculatedCosts;
  const avgProfitMargin = totalGrossRevenue > 0 ? ((totalNetProfit / totalGrossRevenue) * 100).toFixed(1) : '0.0';

  // Helper to extract system creation timestamp strictly based on created_at / system entry time
  const extractSystemTimestamp = (item) => {
    if (!item) return 0;
    if (item.recordTimestamp && Number(item.recordTimestamp) > 0) return Number(item.recordTimestamp);
    if (item.created_at) {
      const t = new Date(item.created_at).getTime();
      if (!isNaN(t) && t > 0) return t;
    }
    if (item.createdAt) {
      const t = new Date(item.createdAt).getTime();
      if (!isNaN(t) && t > 0) return t;
    }
    if (typeof item.id === 'string') {
      const match = item.id.match(/\d{10,13}/);
      if (match) {
        const num = Number(match[0]);
        if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
      }
    }
    return 0;
  };

  // 2. UNIFIED CASH INFLOWS (Rezervasyon Parçalı Tahsilatları + Harici Gelirler)
  const incomeTransactions = useMemo(() => {
    const list = [];
    (reservations || []).forEach(r => {
      if (Array.isArray(r.payments) && r.payments.length > 0) {
        r.payments.forEach(p => {
          const ts = extractSystemTimestamp(p) || extractSystemTimestamp(r);
          list.push({
            id: p.id || `pay-${r.id}-${Math.random()}`,
            resId: r.id,
            title: `${r.customerName} - ${p.type || 'Tahsilat'} (${p.method || 'Kasa'})`,
            category: 'Rezervasyon Tahsilatı',
            type: 'gelir',
            amount: Number(p.amount || 0),
            date: p.date || r.date || '2026-08-01',
            recordTimestamp: ts,
            status: 'Tahsil Edildi',
            isReservationPayment: true
          });
        });
      } else if (Number(r.depositPaid || 0) > 0) {
        const ts = extractSystemTimestamp(r);
        list.push({
          id: `inc-${r.id}-deposit`,
          resId: r.id,
          title: `${r.customerName} - Kapora / Ödeme`,
          category: 'Rezervasyon Tahsilatı',
          type: 'gelir',
          amount: Number(r.depositPaid || 0),
          date: r.date || '2026-08-01',
          recordTimestamp: ts,
          status: 'Tahsil Edildi',
          isReservationPayment: true
        });
      }
    });

    (expenses || []).filter(e => e.type === 'gelir' || e.type === 'income').forEach(e => {
      const ts = extractSystemTimestamp(e);
      list.push({
        id: e.id,
        title: e.title,
        category: e.category || 'Harici Gelir',
        type: 'gelir',
        amount: Number(e.amount || 0),
        date: e.date || '2026-08-01',
        recordTimestamp: ts,
        status: 'Tahsil Edildi',
        isExternal: true
      });
    });

    return list;
  }, [reservations, expenses]);

  // 3. UNIFIED CASH OUTFLOWS (Harici Giderler + Rezervasyon Özel Harcamaları)
  const expenseTransactions = useMemo(() => {
    const list = [];
    (expenses || []).filter(e => e.type !== 'gelir' && e.type !== 'income').forEach(e => {
      const ts = extractSystemTimestamp(e);
      list.push({
        id: e.id,
        title: e.title,
        category: e.category || 'Genel Gider',
        type: 'gider',
        amount: Number(e.amount || 0),
        date: e.date || '2026-08-01',
        recordTimestamp: ts,
        status: e.status || 'Ödendi',
        isExternal: true
      });
    });

    (reservations || []).forEach(r => {
      if (Array.isArray(r.customExpenses)) {
        r.customExpenses.forEach(exp => {
          const ts = extractSystemTimestamp(exp) || extractSystemTimestamp(r);
          list.push({
            id: exp.id || `resexp-${r.id}-${Math.random()}`,
            resId: r.id,
            title: `${r.customerName} - ${exp.title}`,
            category: exp.category || 'Etkinlik Özel Gideri',
            type: 'gider',
            amount: Number(exp.amount || 0),
            date: exp.date || r.date || '2026-08-01',
            recordTimestamp: ts,
            status: 'Ödendi',
            isReservationCustomExpense: true
          });
        });
      }
    });

    return list;
  }, [expenses, reservations]);

  // Unified Ledger
  const allTransactions = useMemo(() => {
    return [...incomeTransactions, ...expenseTransactions].sort((a, b) => {
      const tsA = a.recordTimestamp || 0;
      const tsB = b.recordTimestamp || 0;
      if (tsB !== tsA) {
        return tsB - tsA;
      }
      return String(b.id || '').localeCompare(String(a.id || ''));
    });
  }, [incomeTransactions, expenseTransactions]);

  const totalCashInflow = useMemo(() => incomeTransactions.reduce((sum, t) => sum + t.amount, 0), [incomeTransactions]);
  const totalCashOutflow = useMemo(() => expenseTransactions.reduce((sum, t) => sum + t.amount, 0), [expenseTransactions]);
  const netCashBalance = totalCashInflow - totalCashOutflow;

  const filteredTransactions = useMemo(() => {
    return allTransactions.filter(t => {
      if (filterTab === 'income' && t.type !== 'gelir') return false;
      if (filterTab === 'expense' && t.type !== 'gider') return false;

      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = (t.title || '').toLowerCase().includes(q);
        const matchCategory = (t.category || '').toLowerCase().includes(q);
        const matchAmount = String(t.amount).includes(q);
        if (!matchTitle && !matchCategory && !matchAmount) return false;
      }
      return true;
    });
  }, [allTransactions, filterTab, searchQuery]);

  const filteredProfitabilityRows = useMemo(() => {
    const getTs = (obj) => {
      const r = obj.reservation || obj;
      if (!r) return 0;
      if (r.created_at) {
        const t = new Date(r.created_at).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      if (r.createdAt) {
        const t = new Date(r.createdAt).getTime();
        if (!isNaN(t) && t > 0) return t;
      }
      if (typeof r.id === 'string') {
        const m = r.id.match(/\d{10,13}/);
        if (m) {
          const num = Number(m[0]);
          if (num > 1000000000) return num > 100000000000 ? num : num * 1000;
        }
      }
      return 0;
    };

    return reservationFinancials
      .filter(rf => {
        if (!searchQuery.trim()) return true;
        const q = searchQuery.toLowerCase();
        const r = rf.reservation;
        return (r.customerName || '').toLowerCase().includes(q) ||
               (r.id || '').toLowerCase().includes(q) ||
               (rf.venueName || '').toLowerCase().includes(q);
      })
      .sort((a, b) => {
        const tsA = getTs(a);
        const tsB = getTs(b);
        if (tsB !== tsA) return tsB - tsA;
        return String(b.reservation?.id || '').localeCompare(String(a.reservation?.id || ''));
      });
  }, [reservationFinancials, searchQuery]);

  const monthlyReportData = useMemo(() => {
    const monthPrefix = selectedReportMonth;
    const monthInflows = incomeTransactions.filter(t => (t.date || '').startsWith(monthPrefix));
    const monthOutflows = expenseTransactions.filter(t => (t.date || '').startsWith(monthPrefix));

    const sumInflow = monthInflows.reduce((sum, t) => sum + t.amount, 0);
    const sumOutflow = monthOutflows.reduce((sum, t) => sum + t.amount, 0);
    const netDiff = sumInflow - sumOutflow;

    const categoryMap = {};
    monthOutflows.forEach(t => {
      const cat = t.category || 'Diğer';
      categoryMap[cat] = (categoryMap[cat] || 0) + t.amount;
    });

    const incomeCategoryMap = {};
    monthInflows.forEach(t => {
      const cat = t.category || 'Diğer';
      incomeCategoryMap[cat] = (incomeCategoryMap[cat] || 0) + t.amount;
    });

    const monthEventsCount = (reservations || []).filter(r => (r.date || r.eventDate || '').startsWith(monthPrefix)).length;

    return {
      monthInflows,
      monthOutflows,
      sumInflow,
      sumOutflow,
      netDiff,
      categoryMap,
      incomeCategoryMap,
      monthEventsCount
    };
  }, [incomeTransactions, expenseTransactions, selectedReportMonth, reservations]);

  const handleAddGeneralTransaction = async (e) => {
    e.preventDefault();
    if (!newAmount || Number(newAmount) <= 0) return;

    if (transType === 'gelir' && incomeSource === 'reservation') {
      if (!selectedResId) {
        alert('Lütfen tahsilat yapılacak rezervasyonu seçiniz.');
        return;
      }
      const curRes = (reservations || []).find(r => r.id === selectedResId);
      if (!curRes) return;

      try {
        const fetchFn = window.fetchWithRetry || fetch;
        const resp = await fetchFn(`/api/reservations/${selectedResId}/payments`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            amount: Number(newAmount),
            date: newDate || new Date().toISOString().split('T')[0],
            method: paymentMethod,
            type: paymentType,
            note: newTitle.trim() || `${curRes.customerName} - ${paymentType} (${paymentMethod})`,
            recordedBy: 'Sistem Yöneticisi'
          })
        });
        const data = await resp.json();
        if (data && data.success) {
          if (typeof setReservations === 'function') {
            setReservations(prev => {
              const updated = (prev || []).map(r => {
                if (r.id === selectedResId) {
                  return {
                    ...r,
                    payments: data.payments,
                    depositPaid: data.depositPaid,
                    remainingBalance: data.remainingBalance,
                    paymentStatus: data.paymentStatus
                  };
                }
                return r;
              });
              try { localStorage.setItem('reservations', JSON.stringify(updated)); } catch(e){}
              return updated;
            });
          }
          if (typeof showToast === 'function') {
            showToast(`${curRes.customerName} için ${formatCurrency(newAmount)} tahsilat alındı! Kalan Bakiye: ${formatCurrency(data.remainingBalance)}`);
          }
        }
      } catch(err) {
        console.error('Reservation payment error:', err);
      }

      setNewTitle('');
      setNewAmount('');
      setSelectedResId('');
      setIsModalOpen(false);
      return;
    }

    if (!newTitle.trim()) return;

    const newTrans = {
      id: `trans-${Date.now()}`,
      title: newTitle.trim(),
      category: newCategory,
      type: transType,
      amount: Number(newAmount),
      createdAt: new Date().toISOString(),
      recordTimestamp: Date.now(),
      date: newDate || new Date().toISOString().split('T')[0],
      description: `Kasa Hareketi (${transType === 'gelir' ? 'Harici Gelir' : 'Harici Gider'})`,
      status: newStatus
    };

    try {
      const fetchFn = window.fetchWithRetry || fetch;
      const resp = await fetchFn('/api/expenses', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newTrans)
      });
      const data = await resp.json();
      if (data.success && data.item) {
        setExpenses(prev => [data.item, ...prev.filter(x => x.id !== data.item.id)]);
      } else {
        setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
      }
      if (typeof showToast === 'function') {
        showToast(`${newTrans.title} kasa hareketi kaydedildi.`);
      }
    } catch(err) {
      console.error('Add expense error:', err);
      setExpenses(prev => [newTrans, ...prev.filter(x => x.id !== newTrans.id)]);
    }

    setNewTitle('');
    setNewAmount('');
    setIsModalOpen(false);
  };

  const handleDeleteGeneralExpense = (expId) => {
    if (!confirm('Bu kasa hareketini silmek istediğinize emin misiniz?')) return;
    setExpenses(prev => {
      const updated = prev.filter(e => e.id !== expId);
      try {
        const fetchFn = window.fetchWithRetry || fetch;
        fetchFn(`/api/expenses/${expId}`, {
          method: 'DELETE'
        }).catch(() => {});
      } catch(err) {}
      return updated;
    });
  };

  const handleAddCustomExpenseToRes = (e) => {
    e.preventDefault();
    if (!customExpenseModalRes || !newResExpTitle.trim() || !newResExpAmount) return;

    const existingExpenses = customExpenseModalRes.customExpenses || [];
    const newExpItem = {
      id: `res-exp-${Date.now()}`,
      title: newResExpTitle.trim(),
      amount: Number(newResExpAmount),
      category: newResExpCategory,
      date: new Date().toISOString().split('T')[0]
    };

    const updatedCustomExpenses = [newExpItem, ...existingExpenses];
    const updatedReservation = { ...customExpenseModalRes, customExpenses: updatedCustomExpenses };

    if (onUpdateReservation) {
      onUpdateReservation(updatedReservation);
    }

    setCustomExpenseModalRes(updatedReservation);
    setNewResExpTitle('');
    setNewResExpAmount('');
  };

  const handleAddPaymentToResInModal = async (e) => {
    e.preventDefault();
    if (!customExpenseModalRes || !newResExpAmount || Number(newResExpAmount) <= 0) return;
    const resId = customExpenseModalRes.id;
    try {
      const fetchFn = window.fetchWithRetry || fetch;
      const resp = await fetchFn(`/api/reservations/${resId}/payments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          amount: Number(newResExpAmount),
          date: newResPayDate || new Date().toISOString().split('T')[0],
          method: newResPayMethod,
          type: newResPayType,
          note: newResExpTitle.trim() || `${customExpenseModalRes.customerName} - ${newResPayType}`,
          recordedBy: 'Sistem Yöneticisi'
        })
      });
      const data = await resp.json();
      if (data && data.success) {
        setCustomExpenseModalRes(prev => prev ? ({
          ...prev,
          payments: data.payments,
          depositPaid: data.depositPaid,
          remainingBalance: data.remainingBalance,
          paymentStatus: data.paymentStatus
        }) : null);

        if (typeof setReservations === 'function') {
          setReservations(prev => {
            const updated = (prev || []).map(r => {
              if (r.id === resId) {
                return {
                  ...r,
                  payments: data.payments,
                  depositPaid: data.depositPaid,
                  remainingBalance: data.remainingBalance,
                  paymentStatus: data.paymentStatus
                };
              }
              return r;
            });
            try { localStorage.setItem('reservations', JSON.stringify(updated)); } catch(e){}
            return updated;
          });
        }
        if (typeof showToast === 'function') {
          showToast(`${formatCurrency(newResExpAmount)} tahsilat alındı! Kalan: ${formatCurrency(data.remainingBalance)}`);
        }
        setNewResExpAmount('');
        setNewResExpTitle('');
      }
    } catch(err) {
      console.error('Add payment error:', err);
    }
  };

  const handleDeletePaymentFromRes = async (paymentId) => {
    if (!customExpenseModalRes) return;
    const resId = customExpenseModalRes.id;
    try {
      const fetchFn = window.fetchWithRetry || fetch;
      const resp = await fetchFn(`/api/reservations/${resId}/payments/${paymentId}`, { method: 'DELETE' });
      const data = await resp.json();
      if (data && data.success) {
        setCustomExpenseModalRes(prev => prev ? ({
          ...prev,
          payments: data.payments,
          depositPaid: data.depositPaid,
          remainingBalance: data.remainingBalance,
          paymentStatus: data.paymentStatus
        }) : null);

        if (typeof setReservations === 'function') {
          setReservations(prev => {
            const updated = (prev || []).map(r => {
              if (r.id === resId) {
                return {
                  ...r,
                  payments: data.payments,
                  depositPaid: data.depositPaid,
                  remainingBalance: data.remainingBalance,
                  paymentStatus: data.paymentStatus
                };
              }
              return r;
            });
            try { localStorage.setItem('reservations', JSON.stringify(updated)); } catch(e){}
            return updated;
          });
        }
        if (typeof showToast === 'function') {
          showToast('Tahsilat kaydı silindi ve bakiye güncellendi.');
        }
      }
    } catch(err) {
      console.error('Delete payment error:', err);
    }
  };

  const handleDeleteCustomExpenseFromRes = (expId) => {
    if (!customExpenseModalRes) return;
    const updatedCustomExpenses = (customExpenseModalRes.customExpenses || []).filter(e => e.id !== expId);
    const updatedReservation = { ...customExpenseModalRes, customExpenses: updatedCustomExpenses };

    if (onUpdateReservation) {
      onUpdateReservation(updatedReservation);
    }
    setCustomExpenseModalRes(updatedReservation);
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      {/* HEADER & MAIN TAB SWITCHER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col md:flex-row justify-between items-start md:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text flex items-center space-x-2">
            <span><ThemeIcon icon="money" className="w-5 h-5 inline-block shrink-0" /></span>
            <span>Finans Yönetimi & Kasa Nakit Akışı</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
            Sözleşme kârlılığı, parçalı tahsilatlar, harici gelir/giderler ve ay bazlı kasa nakit raporu.
          </p>
        </div>

        <div className="flex items-center space-x-2 w-full md:w-auto">
          <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-2xl border border-slate-200 dark:border-brand-border w-full sm:w-auto justify-between sm:justify-start">
            <button
              onClick={() => setActiveSubTab('profitability')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                activeSubTab === 'profitability'
                  ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                  : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span><ThemeIcon icon="chart" className="w-4 h-4 inline-block shrink-0" /></span>
              <span>Sözleşme Kârlılığı</span>
            </button>
            <button
              onClick={() => setActiveSubTab('kasa')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                activeSubTab === 'kasa'
                  ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                  : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span><ThemeIcon icon="card" className="w-4 h-4 inline-block shrink-0" /></span>
              <span>Kasa & Harcama Akışı</span>
            </button>
            <button
              onClick={() => setActiveSubTab('monthly')}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition flex items-center space-x-1.5 cursor-pointer ${
                activeSubTab === 'monthly'
                  ? 'bg-amber-500 text-slate-950 shadow-md font-extrabold'
                  : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <span><ThemeIcon icon="calendar" className="w-4 h-4 inline-block shrink-0" /></span>
              <span>Aylık Nakit Raporu</span>
            </button>
          </div>
        </div>
      </div>

      {/* 3 TOP KPI CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-panel p-5 rounded-3xl border border-emerald-500/30 bg-emerald-500/5 space-y-1 shadow-sm">
          <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
            <span>{activeSubTab === 'profitability' ? 'Toplam Ciro (Sözleşmeler)' : 'Fiili Kasa Girişi (+)'}</span>
            <svg className="w-5 h-5 text-emerald-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 17L17 7M17 7H7M17 7V17" /></svg>
          </div>
          <div className="text-2xl font-mono font-extrabold text-emerald-600 dark:text-emerald-400">
            {formatCurrency(activeSubTab === 'profitability' ? totalGrossRevenue : totalCashInflow)}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">
            {activeSubTab === 'profitability' ? `${reservations.length} Adet Rezervasyon` : `${incomeTransactions.length} Adet Gelir / Tahsilat`}
          </div>
        </div>

        <div className="glass-panel p-5 rounded-3xl border border-red-500/30 bg-red-500/5 space-y-1 shadow-sm">
          <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
            <span>{activeSubTab === 'profitability' ? 'Toplam Maliyet (Etkinlikler)' : 'Fiili Kasa Çıkışı (-)'}</span>
            <svg className="w-5 h-5 text-red-500 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7l10 10M17 17H7M17 17V7" /></svg>
          </div>
          <div className="text-2xl font-mono font-extrabold text-red-600 dark:text-red-400">
            {formatCurrency(activeSubTab === 'profitability' ? totalCalculatedCosts : totalCashOutflow)}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">
            {activeSubTab === 'profitability' ? 'Salon + Hizmet + Özel Giderler' : `${expenseTransactions.length} Adet Gider Kalemi`}
          </div>
        </div>

        <div className="glass-panel p-5 rounded-3xl border border-amber-500/40 bg-amber-500/5 space-y-1 shadow-sm">
          <div className="flex justify-between items-center text-xs font-bold text-slate-500 dark:text-gray-400">
            <span>{activeSubTab === 'profitability' ? 'Net Kâr (Kâr Marjı %' + avgProfitMargin + ')' : 'Net Kasa Dengesi (+/-)'}</span>
            <ThemeIcon icon="star" className="w-5 h-5 text-amber-500 shrink-0" />
          </div>
          <div className={`text-2xl font-mono font-extrabold ${(activeSubTab === 'profitability' ? totalNetProfit : netCashBalance) >= 0 ? 'text-emerald-600 dark:text-gold-400' : 'text-red-600'}`}>
            {formatCurrency(activeSubTab === 'profitability' ? totalNetProfit : netCashBalance)}
          </div>
          <div className="text-[11px] text-slate-400 font-medium">
            {activeSubTab === 'profitability' ? 'Sözleşme Bazlı Net Kârlılık' : 'Kasada Kalan Net Nakit'}
          </div>
        </div>
      </div>

      {/* TAB 1: SÖZLEŞME BAZLI KÂRLILIK VE DETAY DÖKÜMÜ */}
      {activeSubTab === 'profitability' && (
        <div className="space-y-4">
          <div className="glass-panel p-4 rounded-3xl flex justify-between items-center gap-4 border border-slate-200 dark:border-brand-border">
            <div className="relative w-full md:w-80">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"><ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /></span>
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Müşteri, salon veya sözleşme ara..."
                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
              />
            </div>
          </div>

          <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm">
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-100/80 dark:bg-brand-card/80 border-b border-slate-200 dark:border-brand-border text-slate-600 dark:text-gray-300 font-bold uppercase tracking-wider">
                    <th className="p-3.5">Sözleşme & Müşteri</th>
                    <th className="p-3.5">Etkinlik Tarihi</th>
                    <th className="p-3.5 text-right">Ciro (Gelir)</th>
                    <th className="p-3.5 text-right">Maliyet</th>
                    <th className="p-3.5 text-right">Özel Gider</th>
                    <th className="p-3.5 text-right">Net Kâr</th>
                    <th className="p-3.5 text-center">Kâr %</th>
                    <th className="p-3.5 text-center">İşlem</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40 font-medium">
                  {filteredProfitabilityRows.length === 0 ? (
                    <tr>
                      <td colSpan="8" className="text-center py-8 text-slate-400 font-bold">
                        Kayıtlı rezervasyon finansmanı bulunamadı.
                      </td>
                    </tr>
                  ) : (
                    filteredProfitabilityRows
                      .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                      .map(rf => {
                        const r = rf.reservation;
                        const isExpanded = !!expandedResIds[r.id];
                        return (
                          <React.Fragment key={r.id}>
                            <tr className="hover:bg-slate-50/60 dark:hover:bg-brand-card/50 transition">
                              <td className="p-3.5">
                                <div className="font-bold text-slate-800 dark:text-gray-100">{r.customerName}</div>
                                <div className="text-[10px] text-slate-400 font-mono">{r.id} • {rf.venueName}</div>
                              </td>
                              <td className="p-3.5 whitespace-nowrap font-mono text-slate-600 dark:text-gray-300">
                                {formatDate(r.date || r.eventDate)}
                              </td>
                              <td className="p-3.5 text-right font-mono font-bold text-slate-800 dark:text-gray-100">
                                {formatCurrency(rf.grossIncome)}
                              </td>
                              <td className="p-3.5 text-right font-mono text-red-500 dark:text-red-400 font-bold">
                                {formatCurrency(rf.venueCost + rf.servicesCost)}
                              </td>
                              <td className="p-3.5 text-right font-mono font-bold">
                                {rf.customExpensesTotal > 0 ? (
                                  <button
                                    type="button"
                                    onClick={() => setCustomExpenseModalRes(r)}
                                    className="text-amber-600 dark:text-gold-400 hover:underline cursor-pointer flex items-center justify-end space-x-1 ml-auto"
                                    title="Ek giderleri yönet"
                                  >
                                    <span>{formatCurrency(rf.customExpensesTotal)}</span>
                                    <span className="text-[9px] font-extrabold bg-amber-500/10 px-1 rounded">({rf.customExpensesList.length})</span>
                                  </button>
                                ) : (
                                  <button
                                    type="button"
                                    onClick={() => setCustomExpenseModalRes(r)}
                                    className="text-[10px] text-slate-400 hover:text-amber-500 hover:underline cursor-pointer"
                                  >
                                    + Gider Ekle
                                  </button>
                                )}
                              </td>
                              <td className={`p-3.5 text-right font-mono font-extrabold ${rf.netProfit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600'}`}>
                                {formatCurrency(rf.netProfit)}
                              </td>
                              <td className="p-3.5 text-center whitespace-nowrap">
                                <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold ${rf.profitMargin >= 35 ? 'bg-emerald-500/10 text-emerald-600' : (rf.profitMargin > 0 ? 'bg-amber-500/10 text-amber-600' : 'bg-red-500/10 text-red-600')}`}>
                                  %{rf.profitMargin}
                                </span>
                              </td>
                              <td className="p-3.5 text-center whitespace-nowrap">
                                <div className="flex items-center justify-center space-x-1.5">
                                  <button
                                    type="button"
                                    onClick={() => toggleExpandRes(r.id)}
                                    className="px-2 py-1 bg-slate-100 dark:bg-brand-dark hover:bg-slate-200 text-slate-600 dark:text-gray-300 rounded-lg text-[10px] font-bold transition cursor-pointer"
                                  >
                                    {isExpanded ? '▲ Kapat' : '▼ Detay'}
                                  </button>
                                  <button
                                    type="button"
                                    onClick={() => setCustomExpenseModalRes(r)}
                                    className="px-2 py-1 bg-amber-500/10 hover:bg-amber-500 text-amber-700 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-amber-500/30"
                                  >
                                    + Ek Gider
                                  </button>
                                </div>
                              </td>
                            </tr>

                            {isExpanded && (
                              <tr className="bg-slate-50/80 dark:bg-brand-dark/70 border-b border-amber-500/20">
                                <td colSpan="8" className="p-4 sm:p-6 space-y-4">
                                  <div className="flex justify-between items-center pb-2 border-b border-slate-200 dark:border-brand-border">
                                    <div className="flex items-center space-x-2">
                                      <span className="w-2.5 h-2.5 rounded-full bg-amber-500 animate-pulse"></span>
                                      <span className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                                        {r.customerName} — Sözleşme & Maliyet Detay Dökümü ({r.id})
                                      </span>
                                    </div>
                                    <button
                                      type="button"
                                      onClick={() => setCustomExpenseModalRes(r)}
                                      className="px-3 py-1.5 gold-button font-bold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1"
                                    >
                                      <span>+ Bu Düğüne Ek Gider / Harcama Gir</span>
                                    </button>
                                  </div>

                                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 text-xs">
                                    {/* 1. MEKAN & BALO SALONU MALİYETİ */}
                                    <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                      <div className="flex justify-between items-center">
                                        <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                          <ThemeIcon icon="venue" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Mekan & Salon Maliyeti</span>
                                        </span>
                                        <span className="font-mono font-extrabold text-red-500 dark:text-red-400">{formatCurrency(rf.venueCost)}</span>
                                      </div>
                                      <div className="p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl text-[11px] space-y-1 text-slate-600 dark:text-gray-300 border border-slate-200/60 dark:border-brand-border/40">
                                        <div className="flex justify-between font-medium">
                                          <span>Salon Adı:</span>
                                          <span className="font-bold text-slate-800 dark:text-gray-100">{rf.venueName}</span>
                                        </div>
                                        <div className="flex justify-between font-medium">
                                          <span>Sözleşme Salon Fiyatı:</span>
                                          <span className="font-bold font-mono">{formatCurrency(r.venuePrice || r.customVenuePrice || 0)}</span>
                                        </div>
                                        <div className="flex justify-between font-medium">
                                          <span>Temel İşletme Maliyeti:</span>
                                          <span className="font-bold font-mono text-red-500">{formatCurrency(rf.venueCost)}</span>
                                        </div>
                                      </div>
                                    </div>

                                    {/* 2. SEÇİLİ EK HİZMETLER VE BİRİM MALİYETLERİ */}
                                    <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                      <div className="flex justify-between items-center">
                                        <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                          <ThemeIcon icon="gift" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Seçili Ek Hizmetler ({(r.selectedServices || []).length})</span>
                                        </span>
                                        <span className="font-mono font-extrabold text-red-500 dark:text-red-400">{formatCurrency(rf.servicesCost)}</span>
                                      </div>
                                      <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                        {(r.selectedServices || []).length === 0 ? (
                                          <div className="text-center py-3 text-slate-400 text-[11px] bg-slate-50 dark:bg-brand-dark rounded-xl border border-dashed border-slate-200 dark:border-brand-border">
                                            Ekstra hizmet seçilmemiş.
                                          </div>
                                        ) : (
                                          (r.selectedServices || []).map((s, idx) => {
                                            const sObj = (services || []).find(srv => srv.id === s.serviceId);
                                            const sName = s.name || sObj?.name || `Hizmet (${s.serviceId})`;
                                            const sQty = Number(s.quantity || 1);
                                            const sCost = (sObj && sObj.costPrice !== undefined && Number(sObj.costPrice) > 0)
                                              ? Number(sObj.costPrice)
                                              : (s.costPrice !== undefined && Number(s.costPrice) > 0
                                                  ? Number(s.costPrice)
                                                  : Math.round(Number(s.unitPrice || s.price || 250) * 0.6));
                                            const totalItemCost = sCost * sQty;
                                            return (
                                              <div key={idx} className="p-2 bg-slate-50 dark:bg-brand-dark rounded-xl flex justify-between items-center text-[11px] border border-slate-200/60 dark:border-brand-border/40">
                                                <div>
                                                  <div className="font-bold text-slate-800 dark:text-gray-200">{sName}</div>
                                                  <div className="text-[10px] text-slate-400 font-medium">{sQty} Adet / Kişi × {formatCurrency(sCost)}</div>
                                                </div>
                                                <span className="font-mono font-bold text-red-500 dark:text-red-400">{formatCurrency(totalItemCost)}</span>
                                              </div>
                                            );
                                          })
                                        )}
                                      </div>
                                    </div>

                                    {/* 3. REZERVASYONA ÖZEL EK HARCAMALAR VE YEVMİYELER */}
                                    <div className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-slate-200 dark:border-brand-border space-y-2.5 shadow-xs">
                                      <div className="flex justify-between items-center">
                                        <span className="font-bold text-slate-700 dark:text-gray-200 flex items-center space-x-1">
                                          <ThemeIcon icon="notes" className="w-4 h-4 text-amber-500 shrink-0 inline-block mr-1.5" /><span>Düğüne Özel Giderler ({rf.customExpensesList.length})</span>
                                        </span>
                                        <span className="font-mono font-extrabold text-amber-600 dark:text-gold-400">{formatCurrency(rf.customExpensesTotal)}</span>
                                      </div>
                                      <div className="space-y-1.5 max-h-36 overflow-y-auto custom-scrollbar">
                                        {rf.customExpensesList.length === 0 ? (
                                          <div className="text-center py-3 text-slate-400 text-[11px] bg-slate-50 dark:bg-brand-dark rounded-xl border border-dashed border-slate-200 dark:border-brand-border">
                                            Özel harcama girilmemiş.
                                          </div>
                                        ) : (
                                          rf.customExpensesList.map((exp, idx) => (
                                            <div key={exp.id || idx} className="p-2 bg-slate-50 dark:bg-brand-dark rounded-xl flex justify-between items-center text-[11px] border border-slate-200/60 dark:border-brand-border/40">
                                              <div>
                                                <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                                                <div className="text-[10px] text-slate-400 font-medium">{exp.category} {exp.date ? `• ${formatDate(exp.date)}` : ''}</div>
                                              </div>
                                              <div className="flex items-center space-x-2">
                                                <span className="font-mono font-bold text-amber-600 dark:text-gold-400">{formatCurrency(exp.amount)}</span>
                                                <button
                                                  type="button"
                                                  onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                                                  className="text-red-500 hover:text-red-700 w-4 h-4 rounded bg-red-500/10 hover:bg-red-500/20 flex items-center justify-center text-[10px]"
                                                  title="Gideri Sil"
                                                >
                                                  ✕
                                                </button>
                                              </div>
                                            </div>
                                          ))
                                        )}
                                      </div>
                                    </div>
                                  </div>

                                  {/* BOTTOM CONTRACT PROFIT RECAP BAR */}
                                  <div className="p-3.5 bg-gradient-to-r from-amber-500/10 via-emerald-500/10 to-transparent rounded-2xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-center gap-3 text-xs">
                                    <div className="flex items-center space-x-4">
                                      <div>
                                        <span className="text-[10px] text-slate-500 block">Sözleşme Cirosu:</span>
                                        <span className="font-mono font-extrabold text-slate-900 dark:text-white text-sm">{formatCurrency(rf.grossIncome)}</span>
                                      </div>
                                      <div className="text-slate-400 font-bold">-</div>
                                      <div>
                                        <span className="text-[10px] text-slate-500 block">Toplam Maliyet:</span>
                                        <span className="font-mono font-extrabold text-red-500 text-sm">{formatCurrency(rf.totalCost)}</span>
                                      </div>
                                      <div className="text-slate-400 font-bold">=</div>
                                      <div>
                                        <span className="text-[10px] text-slate-500 block">Net Kâr:</span>
                                        <span className={`font-mono font-extrabold text-sm ${rf.netProfit >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600'}`}>{formatCurrency(rf.netProfit)}</span>
                                      </div>
                                    </div>

                                    <div className="flex items-center space-x-2">
                                      <span className="text-slate-500 text-[11px] font-bold">Kâr Marjı:</span>
                                      <span className={`px-3 py-1 rounded-xl font-extrabold text-xs shadow-xs ${rf.profitMargin >= 35 ? 'bg-emerald-600 text-white' : (rf.profitMargin > 0 ? 'bg-amber-500 text-slate-950' : 'bg-red-600 text-white')}`}>
                                        %{rf.profitMargin}
                                      </span>
                                    </div>
                                  </div>
                                </td>
                              </tr>
                            )}
                          </React.Fragment>
                        );
                      })
                  )}
                </tbody>
              </table>
            </div>

            <Pagination
              currentPage={currentPage}
              totalItems={filteredProfitabilityRows.length}
              pageSize={pageSize}
              onPageChange={setCurrentPage}
              onPageSizeChange={setPageSize}
            />
          </div>
        </div>
      )}

      {/* TAB 2: KASA VE HARCAMA AKIŞI */}
      {activeSubTab === 'kasa' && (
        <div className="space-y-4">
          <div className="glass-panel p-4 rounded-3xl flex flex-col lg:flex-row justify-between items-stretch lg:items-center gap-3 border border-slate-200 dark:border-brand-border shadow-sm">
            <div className="flex bg-slate-100 dark:bg-brand-card p-1 rounded-2xl border border-slate-200 dark:border-brand-border/60 w-full lg:w-auto">
              <button
                onClick={() => setFilterTab('all')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                  filterTab === 'all' ? 'bg-amber-500 text-slate-950 shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Tümü ({allTransactions.length})
              </button>
              <button
                onClick={() => setFilterTab('income')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                  filterTab === 'income' ? 'bg-emerald-600 text-white shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Gelirler (+) ({incomeTransactions.length})
              </button>
              <button
                onClick={() => setFilterTab('expense')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 lg:flex-none cursor-pointer ${
                  filterTab === 'expense' ? 'bg-red-600 text-white shadow font-extrabold' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Giderler (-) ({expenseTransactions.length})
              </button>
            </div>

            <div className="flex items-center space-x-2.5 w-full lg:w-auto">
              <div className="relative flex-1 lg:w-72">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"><ThemeIcon icon="search" className="w-4 h-4 inline-block shrink-0" /></span>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={e => setSearchQuery(e.target.value)}
                  placeholder="Kasa hareketlerinde ara..."
                  className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
                />
              </div>
              <button
                onClick={() => {
                  setTransType('gider');
                  setIsModalOpen(true);
                }}
                className="px-4 py-2 gold-button font-extrabold text-xs rounded-xl shadow cursor-pointer flex items-center space-x-1.5 shrink-0 hover:scale-[1.02] transition"
              >
                <span>+ Kasa Hareketi Ekle</span>
              </button>
            </div>
          </div>

          <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm">
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-100/80 dark:bg-brand-card/80 border-b border-slate-200 dark:border-brand-border text-slate-600 dark:text-gray-300 font-bold uppercase tracking-wider">
                    <th className="p-3.5"><ThemeIcon icon="calendar" className="w-3.5 h-3.5 inline mr-1 text-amber-500" />İşlem Tarihi</th>
                    <th className="p-3.5">Açıklama & Hareket</th>
                    <th className="p-3.5">Kategori</th>
                    <th className="p-3.5 text-center">Tür</th>
                    <th className="p-3.5 text-right">Tutar</th>
                    <th className="p-3.5 text-center">Durum</th>
                    <th className="p-3.5 text-center">İşlem</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40 font-medium">
                  {filteredTransactions.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="text-center py-8 text-slate-400 font-bold">
                        Kasa hareketi bulunamadı.
                      </td>
                    </tr>
                  ) : (
                    filteredTransactions
                      .slice((currentPage - 1) * pageSize, currentPage * pageSize)
                      .map(t => (
                      <tr key={t.id} className="hover:bg-slate-50/60 dark:hover:bg-brand-card/50 transition">
                        <td className="p-3.5 whitespace-nowrap font-mono text-slate-600 dark:text-gray-400">{formatDate(t.date)}</td>
                        <td className="p-3.5 font-bold text-slate-800 dark:text-gray-100">
                          <div>{t.title}</div>
                          {t.resId && <span className="text-[10px] text-amber-600 dark:text-gold-400 font-mono">{t.resId}</span>}
                        </td>
                        <td className="p-3.5">
                          <span className="bg-slate-100 dark:bg-brand-dark px-2.5 py-1 rounded-lg text-[10px] font-bold text-slate-600 dark:text-gray-300 border border-slate-200 dark:border-brand-border">
                            {t.category}
                          </span>
                        </td>
                        <td className="p-3.5 text-center whitespace-nowrap">
                          {t.type === 'gelir' ? (
                            <span className="bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20 font-bold text-[10px] px-2.5 py-1 rounded-full">
                              + Gelir
                            </span>
                          ) : (
                            <span className="bg-red-500/10 text-red-600 dark:text-red-400 border border-red-500/20 font-bold text-[10px] px-2.5 py-1 rounded-full">
                              - Gider
                            </span>
                          )}
                        </td>
                        <td className={`p-3.5 text-right font-bold text-sm whitespace-nowrap ${t.type === 'gelir' ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                          {t.type === 'gelir' ? '+' : '-'}{formatCurrency(t.amount)}
                        </td>
                        <td className="p-3.5 text-center whitespace-nowrap">
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                            {t.status}
                          </span>
                        </td>
                        <td className="p-3.5 text-center whitespace-nowrap">
                          {t.isExternal ? (
                            <button
                              type="button"
                              onClick={() => handleDeleteGeneralExpense(t.id)}
                              className="px-2 py-1 bg-red-500/10 hover:bg-red-500 text-red-600 hover:text-white rounded-lg text-[10px] font-bold transition cursor-pointer border border-red-500/20"
                              title="Bu kasa hareketini sil"
                            >
                              Sil
                            </button>
                          ) : (
                            <span className="text-[10px] text-slate-400 font-mono" title="Rezervasyon üzerinden yönetilir">Sözleşmeli</span>
                          )}
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>

            <Pagination
              currentPage={currentPage}
              totalItems={filteredTransactions.length}
              pageSize={pageSize}
              onPageChange={setCurrentPage}
              onPageSizeChange={setPageSize}
            />
          </div>
        </div>
      )}

      {/* TAB 3: AYLIK NAKİT AKIŞI VE KASA RAPORU */}
      {activeSubTab === 'monthly' && (
        <div className="space-y-6">
          {/* MONTH PICKER & QUICK STATS */}
          <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-amber-500/10 text-amber-600 font-bold flex items-center justify-center text-lg">
                <ThemeIcon icon="calendar" className="w-5 h-5 shrink-0" />
              </div>
              <div>
                <h3 className="font-extrabold text-base text-slate-800 dark:text-gray-100">Raporlanacak Ayı Seçin</h3>
                <p className="text-xs text-slate-400">Kasaya fiilen giren ve çıkan nakit hareketleri</p>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <select
                value={selectedReportMonth}
                onChange={e => setSelectedReportMonth(e.target.value)}
                className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-xl px-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 cursor-pointer shadow-xs focus:outline-none"
              >
                <option value="2026-05">Mayıs 2026</option>
                <option value="2026-06">Haziran 2026</option>
                <option value="2026-07">Temmuz 2026</option>
                <option value="2026-08">Ağustos 2026</option>
                <option value="2026-09">Eylül 2026</option>
                <option value="2026-10">Ekim 2026</option>
                <option value="2026-11">Kasım 2026</option>
                <option value="2026-12">Aralık 2026</option>
              </select>
            </div>
          </div>

          {/* MONTHLY KPI 4-GRID */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-3xl border border-emerald-500/30 bg-emerald-500/5 space-y-1">
              <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ay Kasa Girişi (+)</span>
              <div className="text-2xl font-mono font-extrabold text-emerald-600 dark:text-emerald-400">
                {formatCurrency(monthlyReportData.sumInflow)}
              </div>
              <div className="text-[10px] text-slate-400">{monthlyReportData.monthInflows.length} Adet Tahsilat / Gelir</div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-red-500/30 bg-red-500/5 space-y-1">
              <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ay Kasa Çıkışı (-)</span>
              <div className="text-2xl font-mono font-extrabold text-red-600 dark:text-red-400">
                {formatCurrency(monthlyReportData.sumOutflow)}
              </div>
              <div className="text-[10px] text-slate-400">{monthlyReportData.monthOutflows.length} Adet Gider / Harcama</div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-amber-500/40 bg-amber-500/5 space-y-1">
              <span className="text-[11px] font-bold text-slate-500 uppercase">Net Kasa Farkı (+ / -)</span>
              <div className={`text-2xl font-mono font-extrabold ${monthlyReportData.netDiff >= 0 ? 'text-emerald-600 dark:text-gold-400' : 'text-red-600'}`}>
                {formatCurrency(monthlyReportData.netDiff)}
              </div>
              <div className="text-[10px] text-slate-400">Seçili Ayın Net Kasa Biyesi</div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-1">
              <span className="text-[11px] font-bold text-slate-500 uppercase">Bu Ayki Düğün / Etkinlik</span>
              <div className="text-2xl font-mono font-extrabold text-slate-800 dark:text-gray-100">
                {monthlyReportData.monthEventsCount} Adet
              </div>
              <div className="text-[10px] text-slate-400">Bu ay salonlarda icra edilen</div>
            </div>
          </div>

          {/* MONTHLY EXPENSES CATEGORY BREAKDOWN CARDS */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
              <h4 className="font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <svg className="w-4 h-4 text-red-500 shrink-0 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 7l10 10M17 17H7M17 17V7" /></svg>
                <span>Seçili Ay Gider Dağılımı (Kategori Bazlı)</span>
              </h4>
              <div className="space-y-2.5">
                {Object.keys(monthlyReportData.categoryMap).length === 0 ? (
                  <div className="text-center py-6 text-slate-400 text-xs font-medium">Bu ay için henüz gider kaydı bulunmuyor.</div>
                ) : (
                  Object.entries(monthlyReportData.categoryMap).map(([cat, amt]) => {
                    const pct = monthlyReportData.sumOutflow > 0 ? Math.round((amt / monthlyReportData.sumOutflow) * 100) : 0;
                    return (
                      <div key={cat} className="space-y-1">
                        <div className="flex justify-between items-center text-xs font-bold">
                          <span className="text-slate-700 dark:text-gray-300">{cat}</span>
                          <span className="font-mono text-red-500">{formatCurrency(amt)} (%{pct})</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-100 dark:bg-brand-dark rounded-full overflow-hidden">
                          <div className="h-full bg-red-500 rounded-full" style={{ width: `${pct}%` }}></div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>

            <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
              <h4 className="font-extrabold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <svg className="w-4 h-4 text-emerald-500 shrink-0 inline-block" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth="2.5"><path strokeLinecap="round" strokeLinejoin="round" d="M7 17L17 7M17 7H7M17 7V17" /></svg>
                <span>Seçili Ay Gelir Dağılımı (Kategori Bazlı)</span>
              </h4>
              <div className="space-y-2.5">
                {Object.keys(monthlyReportData.incomeCategoryMap).length === 0 ? (
                  <div className="text-center py-6 text-slate-400 text-xs font-medium">Bu ay için henüz tahsilat kaydı bulunmuyor.</div>
                ) : (
                  Object.entries(monthlyReportData.incomeCategoryMap).map(([cat, amt]) => {
                    const pct = monthlyReportData.sumInflow > 0 ? Math.round((amt / monthlyReportData.sumInflow) * 100) : 0;
                    return (
                      <div key={cat} className="space-y-1">
                        <div className="flex justify-between items-center text-xs font-bold">
                          <span className="text-slate-700 dark:text-gray-300">{cat}</span>
                          <span className="font-mono text-emerald-600 dark:text-emerald-400">{formatCurrency(amt)} (%{pct})</span>
                        </div>
                        <div className="w-full h-1.5 bg-slate-100 dark:bg-brand-dark rounded-full overflow-hidden">
                          <div className="h-full bg-emerald-500 rounded-full" style={{ width: `${pct}%` }}></div>
                        </div>
                      </div>
                    );
                  })
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* DEDICATED RESERVATION CUSTOM EXPENSE & INCOME (PAYMENT) MANAGEMENT MODAL */}
      {customExpenseModalRes && typeof document !== 'undefined' && ReactDOM.createPortal(
        <div className="fixed inset-0 z-[999999] bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in" onClick={() => setCustomExpenseModalRes(null)}>
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[92vh] overflow-y-auto custom-scrollbar my-auto relative" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
              <div>
                <span className="text-[10px] font-mono font-extrabold text-amber-600 dark:text-gold-400 uppercase tracking-wider">Rezervasyon Özel Gelir & Gider Yönetimi</span>
                <h3 className="text-base font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-1.5">
                  <ThemeIcon icon="document" className="w-4 h-4 inline-block text-amber-500 shrink-0" />
                  <span>{customExpenseModalRes.id} — {customExpenseModalRes.customerName}</span>
                </h3>
              </div>
              <button onClick={() => setCustomExpenseModalRes(null)} className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 font-bold flex items-center justify-center hover:bg-slate-200 cursor-pointer">✕</button>
            </div>

            {/* RESERVATION QUICK FINANCIAL SUMMARY BAR */}
            {(() => {
              const cur = (reservations || []).find(r => r.id === customExpenseModalRes.id) || customExpenseModalRes;
              const curTotal = Number(cur.totalAmount || 0);
              const curPaid = Number(cur.depositPaid || (cur.payments || []).reduce((s, p) => s + Number(p.amount || 0), 0));
              const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));

              return (
                <div className="p-3 bg-slate-50 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border grid grid-cols-3 gap-2 text-center text-[10px]">
                  <div>
                    <span className="text-slate-400 block font-medium">Sözleşme Tutarı:</span>
                    <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(curTotal)}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block font-medium">Ödenen (Tahsilat):</span>
                    <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(curPaid)}</span>
                  </div>
                  <div>
                    <span className="text-slate-400 block font-medium">Kalan Bakiye:</span>
                    <span className="font-mono font-extrabold text-red-500">{formatCurrency(curRemaining)}</span>
                  </div>
                </div>
              );
            })()}

            {/* MODAL ACTION TYPE TABS: GİDER (-) vs GELİR / TAHSİLAT (+) */}
            <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
              <button
                type="button"
                onClick={() => {
                  setResModalTab('gider');
                  setNewResExpTitle('');
                  setNewResExpAmount('');
                }}
                className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                  resModalTab === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                }`}
              >
                <span>- Düğüne Ek Gider Ekle (-)</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setResModalTab('gelir');
                  setNewResExpTitle('');
                  setNewResExpAmount('');
                }}
                className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                  resModalTab === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                }`}
              >
                <span>+ Tahsilat / Gelir Al (+)</span>
              </button>
            </div>

            {/* TAB 1: ADD EXPENSE TO RESERVATION */}
            {resModalTab === 'gider' && (
              <div className="space-y-4">
                <form onSubmit={handleAddCustomExpenseToRes} className="p-4 bg-red-500/10 rounded-2xl border border-red-500/30 space-y-3 text-xs">
                  <span className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                    <ThemeIcon icon="plus" className="w-4 h-4 inline-block text-red-500 shrink-0" />
                    <span>Bu Düğüne Özel Harcama / Maliyet Ekle:</span>
                  </span>

                  <div className="space-y-2">
                    <input
                      type="text"
                      placeholder="Gider Açıklaması (Örn: Ekstra Orkestra, Garson Mesai, Sürpriz Volkan)"
                      value={newResExpTitle}
                      onChange={e => setNewResExpTitle(e.target.value)}
                      required
                      className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-medium"
                    />

                    <div className="grid grid-cols-2 gap-2">
                      <div>
                        <select
                          value={newResExpCategory}
                          onChange={e => setNewResExpCategory(e.target.value)}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs text-slate-800 dark:text-gray-100 font-bold"
                        >
                          <option value="Personel & Yevmiye">Personel & Yevmiye</option>
                          <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                          <option value="Ses, Sahne & Sanatçı">Ses, Sahne & Sanatçı</option>
                          <option value="Mutfak & İkram">Mutfak & İkram</option>
                          <option value="Fotoğraf & Video Ekstra">Fotoğraf & Video Ekstra</option>
                          <option value="Diğer Özel Harcama">Diğer Özel Harcama</option>
                        </select>
                      </div>
                      <div>
                        <input
                          type="number"
                          placeholder="Tutar (TL)"
                          value={newResExpAmount}
                          onChange={e => setNewResExpAmount(e.target.value)}
                          required
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                        />
                      </div>
                    </div>

                    <button
                      type="submit"
                      className="w-full bg-red-600 hover:bg-red-500 text-white font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition cursor-pointer"
                    >
                      - Gideri Düğün Maliyetine Ekle
                    </button>
                  </div>
                </form>

                {/* CURRENT CUSTOM EXPENSES LIST */}
                <div className="space-y-2">
                  <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                    Kayıtlı Özel Ek Giderler ({(customExpenseModalRes.customExpenses || []).length}):
                  </span>
                  {(!customExpenseModalRes.customExpenses || customExpenseModalRes.customExpenses.length === 0) ? (
                    <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                      Bu rezervasyona ait özel ek harcama girilmemiş.
                    </div>
                  ) : (
                    <div className="space-y-1.5 max-h-40 overflow-y-auto custom-scrollbar">
                      {customExpenseModalRes.customExpenses.map(exp => (
                        <div key={exp.id} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                          <div>
                            <div className="font-bold text-slate-800 dark:text-gray-200">{exp.title}</div>
                            <div className="text-[10px] text-slate-400">{exp.category}</div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="font-mono font-bold text-red-500">{formatCurrency(exp.amount)}</span>
                            <button
                              type="button"
                              onClick={() => handleDeleteCustomExpenseFromRes(exp.id)}
                              className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs cursor-pointer"
                              title="Gideri Sil"
                            >
                              ✕
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* TAB 2: ADD PAYMENT / INCOME (BAKİYE DÜŞ) */}
            {resModalTab === 'gelir' && (() => {
              const cur = (reservations || []).find(r => r.id === customExpenseModalRes.id) || customExpenseModalRes;
              const curTotal = Number(cur.totalAmount || 0);
              const curPaid = Number(cur.depositPaid || (cur.payments || []).reduce((s, p) => s + Number(p.amount || 0), 0));
              const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));
              const afterRemaining = Math.max(0, curRemaining - Number(newResExpAmount || 0));

              return (
                <div className="space-y-4">
                  <form onSubmit={handleAddPaymentToResInModal} className="p-4 bg-emerald-500/10 rounded-2xl border border-emerald-500/30 space-y-3 text-xs">
                    <div className="flex justify-between items-center">
                      <span className="font-extrabold text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                        <ThemeIcon icon="money" className="w-4 h-4 inline-block text-emerald-500 shrink-0" />
                        <span>Tahsilat Al & Kalan Bakiyeden Düş:</span>
                      </span>
                      {curRemaining > 0 && (
                        <button
                          type="button"
                          onClick={() => setNewResExpAmount(String(curRemaining))}
                          className="text-emerald-700 dark:text-gold-400 font-bold hover:underline cursor-pointer text-[10px]"
                        >
                          ⚡ Tüm Bakiyeyi Doldur ({formatCurrency(curRemaining)})
                        </button>
                      )}
                    </div>

                    <div className="space-y-2">
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className="font-bold block mb-0.5 text-[11px]">Tahsilat Türü:</label>
                          <select
                            value={newResPayType}
                            onChange={e => setNewResPayType(e.target.value)}
                            className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                          >
                            <option value="Kısmi Ara Ödeme">Kısmi Ara Ödeme / Taksit</option>
                            <option value="Kapora Tahsilatı">Kapora Tahsilatı</option>
                            <option value="Kalan Bakiyenin Kapatılması">Kalan Bakiyenin Kapatılması</option>
                            <option value="Ekstra Hizmet Tahsilatı">Ekstra Hizmet Tahsilatı</option>
                          </select>
                        </div>
                        <div>
                          <label className="font-bold block mb-0.5 text-[11px]">Ödeme Yöntemi:</label>
                          <select
                            value={newResPayMethod}
                            onChange={e => setNewResPayMethod(e.target.value)}
                            className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                          >
                            <option value="Nakit Kasa">Nakit Kasa</option>
                            <option value="Banka Havalesi & EFT">Banka Havalesi & EFT</option>
                            <option value="Kredi Kartı / POS">Kredi Kartı / POS</option>
                          </select>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <label className="font-bold block mb-0.5 text-[11px]">Tahsil Edilen Tutar (TL):</label>
                          <input
                            type="number"
                            placeholder="0"
                            value={newResExpAmount}
                            onChange={e => setNewResExpAmount(e.target.value)}
                            required
                            className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-mono font-bold text-slate-800 dark:text-gray-100"
                          />
                        </div>
                        <div>
                          <label className="font-bold block mb-0.5 text-[11px]">Tahsilat Tarihi:</label>
                          <input
                            type="date"
                            value={newResPayDate}
                            onChange={e => setNewResPayDate(e.target.value)}
                            required
                            className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-bold"
                          />
                        </div>
                      </div>

                      <div>
                        <input
                          type="text"
                          placeholder="Makbuz / Not (Örn: Damat Bey Nakit Ödedi)"
                          value={newResExpTitle}
                          onChange={e => setNewResExpTitle(e.target.value)}
                          className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl p-2 text-xs font-medium"
                        />
                      </div>

                      {Number(newResExpAmount) > 0 && (
                        <div className="p-2 bg-emerald-500/20 rounded-xl text-center text-[11px] font-bold text-emerald-800 dark:text-emerald-300">
                          Tahsilat Sonrası Yeni Kalan Bakiye: <b className="font-mono text-red-500">{formatCurrency(afterRemaining)}</b>
                        </div>
                      )}

                      <button
                        type="submit"
                        className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 rounded-xl text-xs shadow-sm hover:scale-[1.01] transition cursor-pointer"
                      >
                        + Tahsilatı Al & Bakiyeden Düş
                      </button>
                    </div>
                  </form>

                  {/* CURRENT PAYMENTS LIST FOR THIS RESERVATION */}
                  <div className="space-y-2">
                    <span className="font-extrabold text-xs block text-slate-700 dark:text-gray-300">
                      Alınan Tahsilat Geçmişi ({(cur.payments || []).length}):
                    </span>
                    {(!cur.payments || cur.payments.length === 0) ? (
                      <div className="text-center py-4 text-slate-400 text-xs border border-dashed rounded-xl border-slate-200 dark:border-brand-border">
                        Bu sözleşmeye ait henüz tahsilat kaydı bulunmuyor.
                      </div>
                    ) : (
                      <div className="space-y-1.5 max-h-40 overflow-y-auto custom-scrollbar">
                        {cur.payments.map((p, idx) => (
                          <div key={p.id || idx} className="flex justify-between items-center p-2.5 bg-slate-50 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-xs">
                            <div>
                              <div className="font-bold text-slate-800 dark:text-gray-200">{p.type || 'Tahsilat'} — {p.method || 'Kasa'}</div>
                              <div className="text-[10px] text-slate-400">{p.note || ''} {p.date ? `• ${formatDate(p.date)}` : ''}</div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">+{formatCurrency(p.amount)}</span>
                              {p.id && (
                                <button
                                  type="button"
                                  onClick={() => handleDeletePaymentFromRes(p.id)}
                                  className="text-red-500 hover:text-red-700 w-5 h-5 flex items-center justify-center rounded bg-red-500/10 hover:bg-red-500/20 text-xs cursor-pointer"
                                  title="Tahsilatı Sil"
                                >
                                  ✕
                                </button>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              );
            })()}

            <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-end">
              <button
                type="button"
                onClick={() => setCustomExpenseModalRes(null)}
                className="px-5 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold text-xs cursor-pointer"
              >
                Kapat
              </button>
            </div>
          </div>
        </div>,
        document.body
      )}

      {/* GENERAL CASHFLOW TRANSACTION MODAL (GELİR / GİDER SEÇİMLİ - GLOBAL BODY PORTAL) */}
      {isModalOpen && typeof document !== 'undefined' && ReactDOM.createPortal(
        <div className="fixed inset-0 z-[999999] bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 overflow-y-auto animate-fade-in" onClick={() => setIsModalOpen(false)}>
          <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl my-auto max-h-[92vh] overflow-y-auto custom-scrollbar relative" onClick={e => e.stopPropagation()}>
            <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
              <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <span><ThemeIcon icon="money" className="w-5 h-5 inline-block shrink-0" /></span>
                <span>Yeni Kasa Hareketi Ekle</span>
              </h3>
              <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white font-bold cursor-pointer">✕</button>
            </div>

            {/* TYPE SWITCHER: GELİR (+) vs GİDER (-) */}
            <div className="grid grid-cols-2 gap-2 p-1 bg-slate-100 dark:bg-brand-dark rounded-2xl border border-slate-200 dark:border-brand-border">
              <button
                type="button"
                onClick={() => {
                  setTransType('gelir');
                }}
                className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                  transType === 'gelir' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                }`}
              >
                <span>+ Kasa Geliri / Tahsilat (+)</span>
              </button>
              <button
                type="button"
                onClick={() => {
                  setTransType('gider');
                }}
                className={`py-2 rounded-xl text-xs font-extrabold transition cursor-pointer flex items-center justify-center space-x-1.5 ${
                  transType === 'gider' ? 'bg-red-600 text-white shadow-md' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900'
                }`}
              >
                <span>- İşletme Gideri (-)</span>
              </button>
            </div>

            {/* IF GELIR: SUB-TOGGLE FOR RESERVATION PAYMENT VS EXTERNAL INCOME */}
            {transType === 'gelir' && (
              <div className="grid grid-cols-2 gap-2 p-1 bg-emerald-500/10 rounded-2xl border border-emerald-500/30">
                <button
                  type="button"
                  onClick={() => setIncomeSource('reservation')}
                  className={`py-1.5 rounded-xl text-[11px] font-extrabold transition cursor-pointer flex items-center justify-center space-x-1 ${
                    incomeSource === 'reservation' ? 'bg-emerald-600 text-white shadow-sm' : 'text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20'
                  }`}
                >
                  <ThemeIcon icon="calendar" className="w-3.5 h-3.5 inline mr-1" />
                  <span>Rezervasyon Tahsilatı (Bakiye Düş)</span>
                </button>
                <button
                  type="button"
                  onClick={() => setIncomeSource('external')}
                  className={`py-1.5 rounded-xl text-[11px] font-extrabold transition cursor-pointer flex items-center justify-center space-x-1 ${
                    incomeSource === 'external' ? 'bg-emerald-600 text-white shadow-sm' : 'text-emerald-800 dark:text-emerald-300 hover:bg-emerald-500/20'
                  }`}
                >
                  <ThemeIcon icon="money" className="w-3.5 h-3.5 inline mr-1" />
                  <span>Harici Gelir (Plato vb.)</span>
                </button>
              </div>
            )}

            <form onSubmit={handleAddGeneralTransaction} className="space-y-3 text-xs">
              {/* RESERVATION SELECTOR & REMAINING BALANCE CARD */}
              {transType === 'gelir' && incomeSource === 'reservation' ? (
                <>
                  <div>
                    <label className="font-bold block mb-1">Tahsilat Yapılacak Rezervasyon / Sözleşme:</label>
                    <select
                      value={selectedResId}
                      onChange={e => {
                        const rId = e.target.value;
                        setSelectedResId(rId);
                        const found = (reservations || []).find(r => r.id === rId);
                        if (found) {
                          setNewTitle(`${found.customerName} - ${paymentType}`);
                        }
                      }}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    >
                      <option value="">-- Lütfen Sözleşme / Müşteri Seçiniz --</option>
                      {(reservations || []).map(r => (
                        <option key={r.id} value={r.id}>
                          {r.customerName} ({r.id}) - Düğün: {formatDate(r.date || r.eventDate)} | Kalan: {formatCurrency(r.remainingBalance !== undefined ? r.remainingBalance : (r.totalAmount - (r.depositPaid || 0)))}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* LIVE SELECTED RESERVATION BALANCE INFO CARD */}
                  {selectedResId && (() => {
                    const cur = (reservations || []).find(r => r.id === selectedResId);
                    if (!cur) return null;
                    const vObj = (venues || []).find(v => v.id === cur.venueId);
                    const curTotal = Number(cur.totalAmount || 0);
                    const curPaid = Number(cur.depositPaid || 0);
                    const curRemaining = Number(cur.remainingBalance !== undefined ? cur.remainingBalance : Math.max(0, curTotal - curPaid));
                    const afterRemaining = Math.max(0, curRemaining - Number(newAmount || 0));

                    return (
                      <div className="p-3.5 bg-emerald-500/10 rounded-2xl border border-emerald-500/30 space-y-2">
                        <div className="flex justify-between items-center text-[11px]">
                          <span className="font-bold text-slate-700 dark:text-gray-200">{cur.customerName} ({vObj?.name || cur.venueName})</span>
                          <span className="px-2 py-0.5 rounded-lg text-[10px] font-extrabold bg-emerald-600 text-white">{cur.paymentStatus || 'Aktif'}</span>
                        </div>
                        <div className="grid grid-cols-3 gap-2 text-center text-[10px]">
                          <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                            <span className="text-slate-400 block">Sözleşme:</span>
                            <span className="font-mono font-bold text-slate-800 dark:text-gray-100">{formatCurrency(curTotal)}</span>
                          </div>
                          <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                            <span className="text-slate-400 block">Ödenen:</span>
                            <span className="font-mono font-bold text-emerald-600 dark:text-emerald-400">{formatCurrency(curPaid)}</span>
                          </div>
                          <div className="p-1.5 bg-white/60 dark:bg-brand-dark/60 rounded-xl">
                            <span className="text-slate-400 block">Kalan Bakiye:</span>
                            <span className="font-mono font-extrabold text-red-500">{formatCurrency(curRemaining)}</span>
                          </div>
                        </div>
                        {curRemaining > 0 && (
                          <div className="flex justify-between items-center pt-1 border-t border-emerald-500/20 text-[11px]">
                            <button
                              type="button"
                              onClick={() => setNewAmount(String(curRemaining))}
                              className="text-emerald-700 dark:text-gold-400 font-bold hover:underline cursor-pointer text-[10px]"
                            >
                              ⚡ Tüm Kalan Bakiyeyi Doldur ({formatCurrency(curRemaining)})
                            </button>
                            {Number(newAmount) > 0 && (
                              <span className="text-slate-600 dark:text-gray-300 text-[10px] font-bold">
                                Yeni Kalan: <b className="font-mono text-red-500">{formatCurrency(afterRemaining)}</b>
                              </span>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })()}

                  <div className="grid grid-cols-2 gap-2.5">
                    <div>
                      <label className="font-bold block mb-1">Tahsilat Türü:</label>
                      <select
                        value={paymentType}
                        onChange={e => {
                          setPaymentType(e.target.value);
                          const cur = (reservations || []).find(r => r.id === selectedResId);
                          if (cur) setNewTitle(`${cur.customerName} - ${e.target.value}`);
                        }}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      >
                        <option value="Kısmi Ara Ödeme">Kısmi Ara Ödeme / Taksit</option>
                        <option value="Kapora Tahsilatı">Kapora Tahsilatı</option>
                        <option value="Kalan Bakiyenin Kapatılması">Kalan Bakiyenin Kapatılması</option>
                        <option value="Ekstra Hizmet Tahsilatı">Ekstra Hizmet Tahsilatı</option>
                      </select>
                    </div>
                    <div>
                      <label className="font-bold block mb-1">Ödeme Yöntemi:</label>
                      <select
                        value={paymentMethod}
                        onChange={e => setPaymentMethod(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                      >
                        <option value="Nakit Kasa">Nakit Kasa</option>
                        <option value="Banka Havalesi & EFT">Banka Havalesi & EFT</option>
                        <option value="Kredi Kartı / POS">Kredi Kartı / POS</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="font-bold block mb-1">Makbuz / İşlem Notu:</label>
                    <input
                      type="text"
                      value={newTitle}
                      onChange={e => setNewTitle(e.target.value)}
                      placeholder="Örn: 2. Taksit Nakit Tahsilatı Yapıldı"
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>
                </>
              ) : (
                <>
                  <div>
                    <label className="font-bold block mb-1">Harcama / Gelir Açıklaması:</label>
                    <input
                      type="text"
                      value={newTitle}
                      onChange={e => setNewTitle(e.target.value)}
                      placeholder={transType === 'gelir' ? 'Örn: Dış Fotoğraf Çekim Alanı Kiralama' : 'Örn: Temmuz Ayı Elektrik Faturası Ödemesi'}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>

                  <div>
                    <label className="font-bold block mb-1">Kategori:</label>
                    <select
                      value={newCategory}
                      onChange={e => setNewCategory(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    >
                      {transType === 'gelir' ? (
                        <>
                          <option value="Dış Çekim & Plato">Dış Çekim & Plato Kiralama Geliri</option>
                          <option value="Kafeterya & Mutfak Satışı">Kafeterya & Mutfak Günlük Satış Geliri</option>
                          <option value="Ses & Işık Kiralama">Ses & Işık Ekipman Dış Kiralama</option>
                          <option value="Sponsorluk & Reklam">Sponsorluk & Reklam Geliri</option>
                          <option value="Ekipman & Hurda Satışı">Eski Ekipman / Hurda Satış Geliri</option>
                          <option value="Muhtelif Gelir">Diğer Muhtelif Kasa Geliri</option>
                        </>
                      ) : (
                        <>
                          <option value="Faturalar & Enerji">Faturalar & Enerji (Elektrik, Su, Doğalgaz, İnternet)</option>
                          <option value="Yemek & Mutfak & İkram">Yemek & Mutfak & İkram Alımları</option>
                          <option value="Keyfi & Temsil Ağırlama">Keyfi & Temsil Ağırlama (Kahve, Yemek vb.)</option>
                          <option value="Personel & Yevmiye">Personel Maaş, Yevmiye & SGK</option>
                          <option value="Dekorasyon & Çiçek">Dekorasyon, Çiçek & Sahne Süsleme</option>
                          <option value="Ekipman & Bakım">Ekipman, Ses, Işık & Bakım Onarım</option>
                          <option value="Ofis & Kırtasiye & Sarf">Ofis, Kırtasiye & Sarf Malzeme</option>
                          <option value="Vergi & Muhasebe">Vergi, Harç & Muhasebe Ödemeleri</option>
                          <option value="Genel Harcama">Diğer Genel İşletme Giderleri</option>
                        </>
                      )}
                    </select>
                  </div>
                </>
              )}

              <div className="grid grid-cols-2 gap-2.5">
                <div>
                  <label className="font-bold block mb-1">Tahsil Edilen / Ödenen Tutar (TL):</label>
                  <input
                    type="number"
                    value={newAmount}
                    onChange={e => setNewAmount(e.target.value)}
                    placeholder="0"
                    required
                    className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold text-slate-800 dark:text-gray-100"
                  />
                </div>
                <div>
                  <label className="font-bold block mb-1">İşlem Tarihi:</label>
                  <input
                    type="date"
                    value={newDate}
                    onChange={e => setNewDate(e.target.value)}
                    required
                    className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                  />
                </div>
              </div>

              <div className="pt-2 flex justify-end space-x-2 border-t border-slate-200 dark:border-brand-border">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl font-bold cursor-pointer"
                >
                  İptal
                </button>
                <button
                  type="submit"
                  className={`font-bold px-5 py-2 rounded-xl text-white shadow cursor-pointer ${transType === 'gelir' ? 'bg-emerald-600 hover:bg-emerald-500' : 'bg-red-600 hover:bg-red-500'}`}
                >
                  {transType === 'gelir' ? '+ Geliri Kaydet' : '- Gideri Kaydet'}
                </button>
              </div>
            </form>
          </div>
        </div>,
        document.body
      )}
    </div>
  );
}

export default FinanceComponent;
