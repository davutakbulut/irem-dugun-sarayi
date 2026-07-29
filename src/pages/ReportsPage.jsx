import React from 'react';
import { formatCurrency, formatDate } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

    export function ReportsPage({ reservations = [], venues = [], services = [], onConvertToCampaign, onUpdateVenuePrice }) {
      const totalRevenue = reservations.reduce((sum, r) => sum + (r.totalAmount || 0), 0);

      const aiRecs = React.useMemo(() => {
        return generateSmartAIRecommendations(reservations, venues, services);
      }, [reservations, venues, services]);

      return (
        <div className="space-y-6 animate-fade-in pb-12">
          <div>
            <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Yapay Zeka (AI) Gelir Optimizasyonu & Raporlar</h2>
            <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün salonlarınızın doluluk ve ciro verilerinden öğrenen Akıllı AI Tahmin Motoru</p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div className="glass-panel p-5 rounded-3xl border border-amber-500/30">
              <div className="text-xs text-slate-500 font-bold">Toplam Ciro Hacmi</div>
              <div className="text-2xl font-heading font-extrabold gold-gradient-text mt-1">{formatCurrency(totalRevenue)}</div>
              <div className="text-[10px] text-emerald-600 font-bold mt-1">↑ %18 Geçen Sezona Göre Artış</div>
            </div>
            <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border">
              <div className="text-xs text-slate-500 font-bold">Ağustos Ayı Doluluk Oranı</div>
              <div className="text-2xl font-heading font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">%92</div>
              <div className="text-[10px] text-slate-400 mt-1">Kır Bahçesi VİP Zirvede</div>
            </div>
            <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border">
              <div className="text-xs text-slate-500 font-bold">Ortalama Rezervasyon Tutarı</div>
              <div className="text-2xl font-heading font-extrabold text-amber-700 dark:text-gold-400 mt-1">{formatCurrency(totalRevenue / Math.max(1, reservations.length))}</div>
              <div className="text-[10px] text-slate-400 mt-1">Düğün + Ek Hizmet Ortalaması</div>
            </div>
          </div>

          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/40 bg-amber-500/5">
            <div className="flex items-center justify-between border-b border-amber-500/20 pb-3">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center text-xl shadow-inner shrink-0">
                  <ThemeIcon icon="brain" fallbackEmoji="🧠" className="w-6 h-6 shrink-0" />
                </div>
                <div>
                  <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">Akıllı AI Öneri Algoritması & Gelir Fırsatları</h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400">Canlı rezervasyon trendlerini, doluluk oranlarını (%92) ve ek hizmet ilgisini analiz eden dinamik tavsiyeler</p>
                </div>
              </div>
              <span className="text-xs font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
                Otomatik Canlı Analiz
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              {aiRecs.map(rec => (
                <div key={rec.id} className="bg-white dark:bg-brand-card p-5 rounded-2xl border border-amber-500/30 flex flex-col justify-between space-y-4 shadow-md hover:scale-[1.02] transition">
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-2.5 py-0.5 rounded-full border border-amber-500/20">
                        {rec.code}
                      </span>
                      <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-lg">
                        {rec.badge || '✨ AI Önerisi'}
                      </span>
                    </div>
                    <div className="font-bold text-sm text-slate-800 dark:text-gray-100">{rec.title}</div>
                    <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed">{rec.description}</p>
                    {rec.canUpdatePrice && (
                      <div className="bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/20 text-xs font-medium space-y-0.5">
                        <div className="text-slate-500 dark:text-gray-400">Mevcut Fiyat: <strong>{formatCurrency(rec.currentPrice)}</strong></div>
                        <div className="text-emerald-600 dark:text-emerald-400 font-bold">Önerilen Fiyat: {formatCurrency(rec.suggestedPrice)}</div>
                      </div>
                    )}
                  </div>

                  <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-brand-border/40">
                    <button
                      onClick={() => onConvertToCampaign && onConvertToCampaign(rec)}
                      className="w-full gold-button font-bold text-xs py-2.5 px-4 rounded-xl shadow inline-flex items-center justify-center space-x-1.5 hover:scale-[1.01] transition"
                    >
                      <ThemeIcon icon="sparkles" fallbackEmoji="🚀" className="w-4 h-4 shrink-0" />
                      <span>Tek Tıkla Kampanyaya Dönüştür</span>
                    </button>

                    {rec.canUpdatePrice && (
                      <button
                        onClick={() => onUpdateVenuePrice && onUpdateVenuePrice(rec.venueId, rec.suggestedPrice)}
                        className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs py-2 px-4 rounded-xl shadow transition inline-flex items-center justify-center space-x-1.5"
                      >
                        <ThemeIcon icon="money" fallbackEmoji="💰" className="w-4 h-4 shrink-0" />
                        <span>Fiyatı Güncelle & Uygula</span>
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      );
    }

    // --- FINANCE COMPONENT ---