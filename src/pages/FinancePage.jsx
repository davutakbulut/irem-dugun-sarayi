import React, { useState, useEffect, useRef, useMemo } from 'react';
import { formatCurrency, formatDate } from '../utils/formatters.js';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function FinanceComponent({ financialStats, reservations }) {
      const [expenses, setExpenses] = useState([
        { id: 'exp-1', title: 'Orkestra & Ses Sistemi Ödemesi', category: 'Personel & Sanatçı', type: 'gider', amount: 18000, date: '2026-08-01', status: 'Ödendi' },
        { id: 'exp-2', title: 'Salon Garson ve Mutfak Yevmiyeleri', category: 'Personel & Sanatçı', type: 'gider', amount: 24500, date: '2026-08-05', status: 'Ödendi' },
        { id: 'exp-3', title: 'Peyzaj & Çiçek Süsleme Malzemeleri', category: 'Dekorasyon & Çiçek', type: 'gider', amount: 14200, date: '2026-08-10', status: 'Ödendi' },
        { id: 'exp-4', title: 'Elektrik & Jeneratör Yakıt Faturası', category: 'Faturalar & Enerji', type: 'gider', amount: 16800, date: '2026-08-12', status: 'Bekliyor' },
        { id: 'exp-5', title: 'Pasta & Catering Malzeme Alımı', category: 'Yiyecek & İçecek', type: 'gider', amount: 32000, date: '2026-08-15', status: 'Ödendi' }
      ]);

      const [filterTab, setFilterTab] = useState('all');
      const [searchQuery, setSearchQuery] = useState('');
      const [isModalOpen, setIsModalOpen] = useState(false);

      const [newTitle, setNewTitle] = useState('');
      const [newCategory, setNewCategory] = useState('Genel Harcama');
      const [newAmount, setNewAmount] = useState('');
      const [newDate, setNewDate] = useState('2026-08-20');
      const [newStatus, setNewStatus] = useState('Ödendi');

      const incomeTransactions = useMemo(() => {
        return (reservations || []).map(r => ({
          id: `inc-${r.id}`,
          title: `${r.customerName || 'Müşteri'} - ${r.venueName || 'Salon'} Rezervasyonu`,
          category: 'Düğün / Organizasyon',
          type: 'gelir',
          amount: r.totalAmount || 0,
          date: r.date || '2026-08-01',
          status: r.paymentStatus === 'Ödendi' || r.paymentStatus === 'Tamamlandı' ? 'Tahsil Edildi' : (r.paymentStatus === 'Kapora Alındı' ? 'Kapora Alındı' : 'Bekliyor')
        }));
      }, [reservations]);

      const allTransactions = useMemo(() => {
        return [...incomeTransactions, ...expenses].sort((a, b) => new Date(b.date) - new Date(a.date));
      }, [incomeTransactions, expenses]);

      const totalCiro = useMemo(() => {
        return incomeTransactions.reduce((sum, t) => sum + t.amount, 0);
      }, [incomeTransactions]);

      const totalGider = useMemo(() => {
        return expenses.reduce((sum, e) => sum + Number(e.amount || 0), 0);
      }, [expenses]);

      const netKar = totalCiro - totalGider;

      const tahsilEdilenKapora = useMemo(() => {
        return (financialStats?.totalDeposit !== undefined)
          ? financialStats.totalDeposit
          : (reservations || []).reduce((sum, r) => sum + Number(r.depositPaid || 0), 0);
      }, [financialStats, reservations]);

      const filteredTransactions = useMemo(() => {
        return allTransactions.filter(t => {
          if (filterTab === 'income' && t.type !== 'gelir') return false;
          if (filterTab === 'expense' && t.type !== 'gider') return false;

          if (searchQuery.trim()) {
            const q = searchQuery.toLowerCase();
            const matchTitle = t.title.toLowerCase().includes(q);
            const matchCategory = t.category.toLowerCase().includes(q);
            const matchAmount = String(t.amount).includes(q);
            if (!matchTitle && !matchCategory && !matchAmount) return false;
          }
          return true;
        });
      }, [allTransactions, filterTab, searchQuery]);

      const handleAddExpense = (e) => {
        e.preventDefault();
        if (!newTitle.trim() || !newAmount) return;

        const newExp = {
          id: `exp-${Date.now()}`,
          title: newTitle,
          category: newCategory,
          type: 'gider',
          amount: Number(newAmount),
          date: newDate,
          status: newStatus
        };

        setExpenses(prev => [newExp, ...prev]);
        setNewTitle('');
        setNewAmount('');
        setIsModalOpen(false);
      };

      return (
        <div className="space-y-6 animate-fade-in pb-12">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
            <div>
              <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Finans Yönetimi & Kasa Takibi</h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Canlı Gelir / Gider Dengesi, Kapora Durumu ve Harcama Yönetim Paneli</p>
            </div>
            <button
              onClick={() => setIsModalOpen(true)}
              className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center space-x-2"
            >
              <span>➕</span>
              <span>Gider Kaydı Ekle</span>
            </button>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="glass-panel p-5 rounded-3xl border border-amber-500/30">
              <div className="text-xs text-slate-500 dark:text-gray-400 font-bold flex items-center justify-between">
                <span>Toplam Ciro</span>
                <span className="text-amber-500">💰</span>
              </div>
              <div className="text-2xl font-heading font-extrabold gold-gradient-text mt-2">{formatCurrency(totalCiro)}</div>
              <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold mt-1">↑ Tüm Rezervasyon Gelirleri</div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-red-500/30">
              <div className="text-xs text-slate-500 dark:text-gray-400 font-bold flex items-center justify-between">
                <span>Toplam Gider</span>
                <span className="text-red-500">💸</span>
              </div>
              <div className="text-2xl font-heading font-extrabold text-red-600 dark:text-red-400 mt-2">{formatCurrency(totalGider)}</div>
              <div className="text-[10px] text-red-500 font-bold mt-1">↓ Salon & Operasyon Harcamaları</div>
            </div>

            <div className={`glass-panel p-5 rounded-3xl border ${netKar >= 0 ? 'border-emerald-500/30' : 'border-red-500/30'}`}>
              <div className="text-xs text-slate-500 dark:text-gray-400 font-bold flex items-center justify-between">
                <span>Net Kar (Ciro - Gider)</span>
                <span>📈</span>
              </div>
              <div className={`text-2xl font-heading font-extrabold mt-2 ${netKar >= 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                {formatCurrency(netKar)}
              </div>
              <div className="text-[10px] text-slate-400 font-bold mt-1">Net Kar Marjı Denge Hesabı</div>
            </div>

            <div className="glass-panel p-5 rounded-3xl border border-blue-500/30">
              <div className="text-xs text-slate-500 dark:text-gray-400 font-bold flex items-center justify-between">
                <span>Tahsil Edilen Kapora</span>
                <span className="text-blue-500">🛡️</span>
              </div>
              <div className="text-2xl font-heading font-extrabold text-blue-600 dark:text-blue-400 mt-2">{formatCurrency(tahsilEdilenKapora)}</div>
              <div className="text-[10px] text-blue-500 font-bold mt-1">Alınan Ön Ödemeler</div>
            </div>
          </div>

          <div className="glass-panel p-4 rounded-3xl flex flex-col md:flex-row justify-between items-center gap-4 border border-slate-200 dark:border-brand-border">
            <div className="flex bg-slate-100 dark:bg-brand-card p-1 rounded-2xl border border-slate-200 dark:border-brand-border/60 w-full md:w-auto">
              <button
                onClick={() => setFilterTab('all')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none ${
                  filterTab === 'all' ? 'bg-amber-500 text-slate-950 shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Tümü ({allTransactions.length})
              </button>
              <button
                onClick={() => setFilterTab('income')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none ${
                  filterTab === 'income' ? 'bg-emerald-600 text-white shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Gelirler (+) ({incomeTransactions.length})
              </button>
              <button
                onClick={() => setFilterTab('expense')}
                className={`px-4 py-2 text-xs font-bold rounded-xl transition flex-1 md:flex-none ${
                  filterTab === 'expense' ? 'bg-red-600 text-white shadow' : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-white'
                }`}
              >
                Giderler (-) ({expenses.length})
              </button>
            </div>

            <div className="relative w-full md:w-80">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">🔍</span>
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Kasa hareketlerinde ara..."
                className="w-full bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-xl pl-9 pr-4 py-2 text-xs font-bold text-slate-800 dark:text-gray-100 placeholder:text-slate-400 focus:outline-none focus:border-amber-500"
              />
            </div>
          </div>

          <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm">
            <div className="overflow-x-auto custom-scrollbar">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="bg-slate-100/80 dark:bg-brand-card/80 border-b border-slate-200 dark:border-brand-border text-slate-600 dark:text-gray-300 font-bold uppercase tracking-wider">
                    <th className="p-3.5">Tarih</th>
                    <th className="p-3.5">Açıklama</th>
                    <th className="p-3.5">Kategori</th>
                    <th className="p-3.5 text-center">Tür</th>
                    <th className="p-3.5 text-right">Tutar</th>
                    <th className="p-3.5 text-center">Durum</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-brand-border/40 font-medium">
                  {filteredTransactions.length === 0 ? (
                    <tr>
                      <td colSpan="6" className="text-center py-8 text-slate-400 font-bold">
                        Kasa hareketi bulunamadı.
                      </td>
                    </tr>
                  ) : (
                    filteredTransactions.map(t => (
                      <tr key={t.id} className="hover:bg-slate-50/60 dark:hover:bg-brand-card/50 transition">
                        <td className="p-3.5 whitespace-nowrap font-mono text-slate-600 dark:text-gray-400">{formatDate(t.date)}</td>
                        <td className="p-3.5 font-bold text-slate-800 dark:text-gray-100">{t.title}</td>
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
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                            t.status === 'Ödendi' || t.status === 'Tahsil Edildi' || t.status === 'Tamamlandı'
                              ? 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400'
                              : 'bg-amber-500/10 text-amber-600 dark:text-gold-400'
                          }`}>
                            {t.status}
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>

          {isModalOpen && (
            <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <span>💸</span>
                    <span>Yeni Gider Kaydı Ekle</span>
                  </h3>
                  <button onClick={() => setIsModalOpen(false)} className="text-slate-400 hover:text-white">✕</button>
                </div>
                <form onSubmit={handleAddExpense} className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold block mb-1">Harcama Başlığı:</label>
                    <input
                      type="text"
                      value={newTitle}
                      onChange={e => setNewTitle(e.target.value)}
                      placeholder="Örn: Garson Yevmiyeleri Ödemesi"
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
                      <option value="Personel & Sanatçı">Personel & Sanatçı</option>
                      <option value="Dekorasyon & Çiçek">Dekorasyon & Çiçek</option>
                      <option value="Faturalar & Enerji">Faturalar & Enerji</option>
                      <option value="Yiyecek & İçecek">Yiyecek & İçecek</option>
                      <option value="Ekipman & Bakım">Ekipman & Bakım</option>
                      <option value="Genel Harcama">Genel Harcama</option>
                    </select>
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Tutar (TL):</label>
                    <input
                      type="number"
                      value={newAmount}
                      onChange={e => setNewAmount(e.target.value)}
                      placeholder="0"
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Tarih:</label>
                    <input
                      type="date"
                      value={newDate}
                      onChange={e => setNewDate(e.target.value)}
                      required
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    />
                  </div>
                  <div>
                    <label className="font-bold block mb-1">Ödeme Durumu:</label>
                    <select
                      value={newStatus}
                      onChange={e => setNewStatus(e.target.value)}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-100"
                    >
                      <option value="Ödendi">Ödendi</option>
                      <option value="Bekliyor">Bekliyor</option>
                    </select>
                  </div>
                  <div className="flex justify-end space-x-2 pt-3 border-t border-slate-200 dark:border-brand-border">
                    <button
                      type="button"
                      onClick={() => setIsModalOpen(false)}
                      className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold"
                    >
                      İptal
                    </button>
                    <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl">
                      Gider Kaydet ✓
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}
        </div>
      );
    }

    // --- CUSTOMERS COMPONENT ---
    // --- CUSTOMERS COMPONENT ---
