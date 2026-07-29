import React, { useState } from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';

export function ReservationsListPage({ reservations = [], venues = [], onNewResClick }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [viewMode, setViewMode] = useState('table'); // 'table' or 'calendar'

  const filteredReservations = reservations.filter(r => {
    const matchesSearch = !searchQuery.trim() ||
      (r.customerName || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (r.id || '').toLowerCase().includes(searchQuery.toLowerCase()) ||
      (r.customerPhone || '').includes(searchQuery);

    const matchesStatus = statusFilter === 'ALL' || r.paymentStatus === statusFilter;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* HEADER & CONTROLS */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            📅 Rezervasyon Yönetimi & Master Takvim
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Tüm düğün ve organizasyon sözleşmelerini filtreleyin veya takvim üzerinde inceleyin.
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
          <div className="flex bg-slate-100 dark:bg-brand-dark p-1 rounded-xl border border-slate-200 dark:border-brand-border">
            <button
              onClick={() => setViewMode('table')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${viewMode === 'table' ? 'bg-white dark:bg-brand-card text-slate-800 dark:text-gray-100 shadow' : 'text-slate-500'}`}
            >
              📋 Liste Görünümü
            </button>
            <button
              onClick={() => setViewMode('calendar')}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold transition ${viewMode === 'calendar' ? 'bg-white dark:bg-brand-card text-slate-800 dark:text-gray-100 shadow' : 'text-slate-500'}`}
            >
              🗓️ Canlı Takvim Görünümü
            </button>
          </div>

          <button onClick={onNewResClick} className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1">
            <span>➕ Yeni Rezervasyon</span>
          </button>
        </div>
      </div>

      {/* FILTERS BAR */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
        <input
          type="text"
          placeholder="🔍 Müşteri Adı, Sözleşme Kodu veya Telefon ile Ara..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full sm:w-80 bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-medium text-slate-800 dark:text-gray-200"
        />

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <span className="font-bold text-slate-600 dark:text-gray-400">Durum Filtresi:</span>
          <select
            value={statusFilter}
            onChange={e => setStatusFilter(e.target.value)}
            className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200"
          >
            <option value="ALL">Tümü ({reservations.length})</option>
            <option value="Kapora Alındı">Kapora Alındı</option>
            <option value="Tamamlandı">Tamamlandı / Ödendi</option>
            <option value="Bekliyor">Bekliyor</option>
            <option value="İptal">İptal Edilenler</option>
          </select>
        </div>
      </div>

      {/* VIEW: TABLE OR CALENDAR */}
      {viewMode === 'table' ? (
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                  <th className="py-3 px-3">Sözleşme Kodu</th>
                  <th className="py-3 px-3">Müşteri / Çift</th>
                  <th className="py-3 px-3">Düğün Salonu</th>
                  <th className="py-3 px-3">Tarih & Seans</th>
                  <th className="py-3 px-3">Davetli</th>
                  <th className="py-3 px-3">Toplam Tutar</th>
                  <th className="py-3 px-3">Kalan Bakiye</th>
                  <th className="py-3 px-3">Ödeme Durumu</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-brand-border">
                {filteredReservations.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="py-8 text-center text-slate-400 font-bold">
                      Kayıtlı rezervasyon bulunamadı.
                    </td>
                  </tr>
                ) : (
                  filteredReservations.map(res => {
                    const vObj = venues.find(v => v.id === res.venueId);
                    return (
                      <tr key={res.id} className="hover:bg-slate-50 dark:hover:bg-brand-dark/50 font-medium text-slate-800 dark:text-gray-200">
                        <td className="py-3.5 px-3 font-mono font-bold text-amber-700 dark:text-gold-400">{res.id}</td>
                        <td className="py-3.5 px-3">
                          <div className="font-bold">{res.customerName}</div>
                          <div className="text-[10px] text-slate-400">{res.customerPhone}</div>
                        </td>
                        <td className="py-3.5 px-3 font-bold">{vObj?.name || res.venueId}</td>
                        <td className="py-3.5 px-3 font-mono">
                          <div>{formatDate(res.eventDate)}</div>
                          <div className="text-[10px] text-slate-500">{res.timeSlot || '19:00 - 23:30'}</div>
                        </td>
                        <td className="py-3.5 px-3 font-bold">{res.guestCount} Kişi</td>
                        <td className="py-3.5 px-3 font-mono font-bold">{formatCurrency(res.totalAmount)}</td>
                        <td className="py-3.5 px-3 font-mono font-bold text-red-600 dark:text-red-400">
                          {res.remainingBalance === 0 ? '₺0 (Ödendi)' : formatCurrency(res.remainingBalance)}
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
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* CALENDAR TIMELINE VIEW */
        <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
          <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
            <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">
              🗓️ Ağustos 2026 Master Etkinlik Çizelgesi
            </h3>
            <span className="text-xs text-slate-500 font-bold">14 Günlük Görünüm</span>
          </div>

          <div className="grid grid-cols-7 gap-2 text-center font-bold text-xs text-slate-500 pb-2 border-b">
            <span>Pzt</span><span>Sal</span><span>Çar</span><span>Per</span><span>Cum</span><span>Cmt</span><span>Paz</span>
          </div>

          <div className="grid grid-cols-7 gap-2 text-xs">
            {[...Array(14)].map((_, i) => {
              const dayDate = new Date(2026, 7, 20 + i);
              const dateStr = dayDate.toISOString().split('T')[0];
              const dayResList = reservations.filter(r => r.eventDate === dateStr && r.paymentStatus !== 'İptal');

              return (
                <div key={dateStr} className="min-h-[90px] bg-slate-50 dark:bg-brand-dark p-2 rounded-2xl border border-slate-200 dark:border-brand-border space-y-1.5 flex flex-col justify-between">
                  <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-1 text-[11px] font-bold">
                    <span className="text-slate-700 dark:text-gray-300">{dayDate.getDate()} Ağu</span>
                    <span className="text-[9px] bg-slate-200 dark:bg-brand-card px-1.5 rounded text-slate-600">{dayResList.length} Düğün</span>
                  </div>

                  <div className="space-y-1">
                    {dayResList.map(r => {
                      const vObj = venues.find(v => v.id === r.venueId);
                      return (
                        <div key={r.id} className="p-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-[10px] font-bold text-amber-900 dark:text-gold-400">
                          <div className="truncate">{r.customerName}</div>
                          <div className="text-[9px] opacity-80">{vObj?.name?.split(' ')[0]}</div>
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
    </div>
  );
}
