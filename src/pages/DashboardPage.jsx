import React from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';

export function DashboardPage({ activeRole, venues = [], reservations = [], onNewResClick, onTabChange }) {
  const totalRevenue = reservations.reduce((acc, r) => acc + (Number(r.totalAmount) || 0), 0);
  const totalDeposit = reservations.reduce((acc, r) => acc + (Number(r.depositPaid) || 0), 0);
  const totalRemaining = reservations.reduce((acc, r) => acc + (Number(r.remainingBalance) || 0), 0);
  const upcomingCount = reservations.filter(r => r.paymentStatus !== 'İptal').length;

  return (
    <div className="space-y-6 animate-fade-in max-w-7xl mx-auto">
      {/* WELCOME BANNER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm relative overflow-hidden">
        <div className="space-y-1 z-10">
          <span className="text-xs font-bold text-amber-600 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
            👋 Hoş Geldiniz!
          </span>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text pt-1">
            İrem Düğün Sarayı Yönetim Paneli
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Salon dolulukları, anlık rezervasyonlar ve finansal raporları tek bakışta izleyin.
          </p>
        </div>

        <div className="flex space-x-2 z-10 w-full sm:w-auto">
          <button onClick={onNewResClick} className="w-full sm:w-auto gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center justify-center space-x-2">
            <span>✨</span>
            <span>Hızlı Rezervasyon Gir</span>
          </button>
        </div>
      </div>

      {/* KPI METRIC CARDS */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
            <span>Toplam Ciro (Sözleşmeli)</span>
            <span className="text-base">💰</span>
          </div>
          <div className="text-xl font-extrabold font-mono text-slate-800 dark:text-gray-100">
            {formatCurrency(totalRevenue)}
          </div>
          <div className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
            ↑ Toplam {reservations.length} Kayıtlı Etkinlik
          </div>
        </div>

        <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
            <span>Tahsil Edilen Kaporalar</span>
            <span className="text-base">💳</span>
          </div>
          <div className="text-xl font-extrabold font-mono text-emerald-600 dark:text-emerald-400">
            {formatCurrency(totalDeposit)}
          </div>
          <div className="text-[10px] text-slate-500 font-bold">
            Nakit & Banka Havalesi Alındı
          </div>
        </div>

        <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
            <span>Bekleyen Alacak (Net Bakiye)</span>
            <span className="text-base">⏳</span>
          </div>
          <div className="text-xl font-extrabold font-mono text-amber-600 dark:text-gold-400">
            {formatCurrency(totalRemaining)}
          </div>
          <div className="text-[10px] text-amber-600 font-bold">
            Etkinlik Günü Tahsil Edilecek
          </div>
        </div>

        <div className="glass-panel p-5 rounded-3xl space-y-2 border border-slate-200 dark:border-brand-border shadow-sm">
          <div className="flex justify-between items-center text-slate-500 dark:text-gray-400 text-xs font-bold">
            <span>Aktif Rezervasyonlar</span>
            <span className="text-base">📅</span>
          </div>
          <div className="text-xl font-extrabold text-slate-800 dark:text-gray-100">
            {upcomingCount} Adet
          </div>
          <div className="text-[10px] text-indigo-500 font-bold">
            Yaklaşan Düğün & Nişanlar
          </div>
        </div>
      </div>

      {/* RECENT RESERVATIONS & QUICK ACTION TABLE */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border pb-3">
          <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
            <span>📋</span>
            <span>Son Eklenen Rezervasyonlar</span>
          </h3>
          <button onClick={() => onTabChange('reservations')} className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline">
            Tümünü Gör (Takvim) →
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                <th className="py-2.5 px-3">Kod</th>
                <th className="py-2.5 px-3">Müşteri / Çift</th>
                <th className="py-2.5 px-3">Salon</th>
                <th className="py-2.5 px-3">Tarih & Seans</th>
                <th className="py-2.5 px-3">Toplam Tutar</th>
                <th className="py-2.5 px-3">Durum</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-brand-border">
              {reservations.slice(0, 5).map(res => {
                const vObj = venues.find(v => v.id === res.venueId);
                return (
                  <tr key={res.id} className="hover:bg-slate-50 dark:hover:bg-brand-dark/50 font-medium text-slate-800 dark:text-gray-200">
                    <td className="py-3 px-3 font-mono font-bold text-amber-700 dark:text-gold-400">{res.id}</td>
                    <td className="py-3 px-3 font-bold">{res.customerName}</td>
                    <td className="py-3 px-3">{vObj?.name || res.venueId}</td>
                    <td className="py-3 px-3 font-mono">{formatDate(res.eventDate)} ({res.timeSlot || 'Akşam'})</td>
                    <td className="py-3 px-3 font-mono font-bold">{formatCurrency(res.totalAmount)}</td>
                    <td className="py-3 px-3">
                      <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                        res.paymentStatus === 'Tamamlandı' ? 'bg-emerald-500/20 text-emerald-600' :
                        res.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-600' :
                        'bg-slate-200 text-slate-700'
                      }`}>
                        {res.paymentStatus}
                      </span>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
