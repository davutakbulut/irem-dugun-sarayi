import React from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

    export function DashboardPage({ activeRole, venues, reservations, financialStats, onNewResClick, onTabChange }) {
      return (
        <div className="space-y-6">
          <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-sm">
            <div>
              <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 text-xs font-bold px-3 py-1 rounded-full border border-amber-500/20 flex items-center space-x-1.5 w-fit">
                {activeRole === 'admin' && <><ThemeIcon icon="crown" fallbackEmoji="👑" className="w-3.5 h-3.5 shrink-0" /><span>Admin Kurumsal Yönetim Paneli</span></>}
                {activeRole === 'satisci' && <><ThemeIcon icon="venue" fallbackEmoji="💼" className="w-3.5 h-3.5 shrink-0" /><span>Satış & Doluluk Ekranı</span></>}
                {activeRole === 'sosyal_medyaci' && <><ThemeIcon icon="preview" fallbackEmoji="📸" className="w-3.5 h-3.5 shrink-0" /><span>Medya Yükleme Paneli</span></>}
                {activeRole === 'musteri' && <><ThemeIcon icon="user" fallbackEmoji="💖" className="w-3.5 h-3.5 shrink-0" /><span>Özel Müşteri Portalı</span></>}
              </span>
              <h2 className="text-2xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2 flex items-center space-x-2">
                <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-5 h-5 text-amber-500 shrink-0" />
                <span>Hoş Geldiniz, İrem Hanım</span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">İrem Düğün Sarayı güncel rezervasyon durumu ve organizasyon hareketleri.</p>
            </div>

            {(activeRole === 'admin' || activeRole === 'satisci') && (
              <button onClick={onNewResClick} className="gold-button font-bold px-6 py-3 rounded-2xl shadow-lg flex items-center space-x-2 text-xs">
                <span>➕</span><span>Tam Sayfa Yeni Rezervasyon Çalışma Alanı</span>
              </button>
            )}
          </div>

          {activeRole === 'admin' && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Toplam Düğün Salonu</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length}</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Bu Ayın Boş Günleri</div><div className="text-2xl font-bold gold-gradient-text mt-1">12 Gün</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Son Ay Toplam Kazanç</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{formatCurrency(financialStats.totalRev)}</div></div>
              <div className="glass-panel p-5 rounded-2xl border border-red-500/40 shadow-sm"><div className="text-xs text-slate-500 dark:text-gray-400">Bekleyen Ödemeler</div><div className="text-2xl font-bold text-red-500 dark:text-red-400 mt-1">{formatCurrency(financialStats.totalPending)}</div></div>
            </div>
          )}

          {activeRole === 'satisci' && (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="glass-panel p-5 rounded-2xl"><div className="text-xs text-slate-500 dark:text-gray-400">Salon Sayısı</div><div className="text-2xl font-bold text-slate-800 dark:text-gray-100">{venues.length}</div></div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40"><div className="text-xs text-slate-500 dark:text-gray-400">Ayın Boş Günleri</div><div className="text-2xl font-bold gold-gradient-text">12 Gün</div></div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40"><div className="text-xs text-slate-500 dark:text-gray-400">Kapora Alınanlar</div><div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{reservations.filter(r => r.depositPaid > 0).length}</div></div>
              </div>
            </div>
          )}

        </div>
      );
    }

    // --- VENUE MODAL COMPONENT ---