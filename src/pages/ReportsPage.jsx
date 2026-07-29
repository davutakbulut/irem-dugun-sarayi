import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

export function ReportsPage({ reservations = [], venues = [], onConvertToCampaign }) {
  const totalRevenue = reservations.reduce((acc, r) => acc + (Number(r.totalAmount) || 0), 0);
  const totalDeposit = reservations.reduce((acc, r) => acc + (Number(r.depositPaid) || 0), 0);
  const totalRemaining = reservations.reduce((acc, r) => acc + (Number(r.remainingBalance) || 0), 0);

  const aiInsights = [
    {
      id: 'ai1',
      title: 'Hafta İçi Salı/Çarşamba Doluluk Fırsatı',
      recommendation: 'Ağustos ayında Salı ve Çarşamba günlerinde %40 boşluk bulunmaktadır. %15 İndirimli hafta içi paketi oluşturulabilir.',
      code: 'HAFTAICI15',
      discountType: 'percent',
      discountValue: 15
    },
    {
      id: 'ai2',
      title: 'Yakut Kır Bahçesi Yüksek Talep Kampanyası',
      recommendation: 'Kır bahçesine 500+ kişilik rezervasyon talebi yoğunlaşmaktadır. 10.000 ₺ kapora avantajlı düğün paketi başlatabilirsiniz.',
      code: 'KIRBAHCE2026',
      discountType: 'fixed',
      discountValue: 10000
    }
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
            <ThemeIcon icon="chart" fallbackEmoji="📈" className="w-6 h-6 text-amber-500 shrink-0" />
            <span>Finansal Raporlar & AI Akıllı Analizler</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Aylık gelir dağılımı, net kalan alacaklar ve yapay zeka tarafından üretilen otomasyon önerileri.
          </p>
        </div>
      </div>

      {/* SUMMARY STATS */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-1 shadow-sm">
          <div className="text-xs font-bold text-slate-500">Toplam Sözleşme Tutarı</div>
          <div className="text-2xl font-extrabold font-mono text-slate-900 dark:text-white">{formatCurrency(totalRevenue)}</div>
        </div>
        <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-1 shadow-sm">
          <div className="text-xs font-bold text-slate-500">Tahsil Edilen Kaporalar</div>
          <div className="text-2xl font-extrabold font-mono text-emerald-600 dark:text-emerald-400">{formatCurrency(totalDeposit)}</div>
        </div>
        <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-1 shadow-sm">
          <div className="text-xs font-bold text-slate-500">Kalan Net Alacaklar</div>
          <div className="text-2xl font-extrabold font-mono text-amber-600 dark:text-gold-400">{formatCurrency(totalRemaining)}</div>
        </div>
      </div>

      {/* AI INSIGHTS & ONE-CLICK CAMPAIGN AUTOMATION */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 shadow-sm">
        <h3 className="font-heading font-bold text-base text-slate-900 dark:text-white flex items-center space-x-2">
          <ThemeIcon icon="brain" fallbackEmoji="🤖" className="w-5 h-5 text-amber-500 shrink-0" />
          <span>Yapay Zeka (AI) Otomatik Satış & Kampanya Önerileri</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {aiInsights.map(ai => (
            <div key={ai.id} className="bg-amber-500/10 border border-amber-500/30 p-5 rounded-2xl space-y-3">
              <div>
                <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">{ai.title}</h4>
                <p className="text-xs text-slate-600 dark:text-gray-300 mt-1">{ai.recommendation}</p>
              </div>

              <button
                onClick={() => onConvertToCampaign(ai)}
                className="gold-button font-bold text-xs px-4 py-2 rounded-xl shadow w-full text-center flex items-center justify-center space-x-1"
              >
                <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-4 h-4 shrink-0" />
                <span>Tek Tıkla Kampanyaya Dönüştür ({ai.code})</span>
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
