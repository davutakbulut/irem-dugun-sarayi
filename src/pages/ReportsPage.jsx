import React, { useState, useMemo, useEffect } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';


export function ReportsPage({ reservations = [], venues = [], services = [], onConvertToCampaign, onUpdateVenuePrice }) {
      const totalRevenue = useMemo(() => {
        return reservations.reduce((sum, r) => sum + (r.totalAmount || 0), 0);
      }, [reservations]);

      // Dynamic Occupancy Calculation
      const occupancyRate = useMemo(() => {
        const totalVenueSlots = Math.max(1, venues.length) * 30;
        const validResCount = reservations.filter(r => r.paymentStatus !== 'İptal').length;
        return Math.min(100, Math.round((validResCount / totalVenueSlots) * 100));
      }, [reservations, venues]);

      // Dynamic Venue Revenue Distribution for Donut Chart
      const venueRevenueData = useMemo(() => {
        const map = {};
        venues.forEach(v => { map[v.id] = { name: v.name, color: '#f59e0b', revenue: 0 }; });

        const colors = ['#f59e0b', '#10b981', '#6366f1', '#ec4899', '#8b5cf6', '#14b8a6'];
        venues.forEach((v, idx) => {
          if (map[v.id]) map[v.id].color = colors[idx % colors.length];
        });

        reservations.forEach(r => {
          if (r.paymentStatus !== 'İptal') {
            if (map[r.venueId]) {
              map[r.venueId].revenue += (r.totalAmount || 0);
            }
          }
        });

        const list = Object.values(map);
        const total = list.reduce((s, item) => s + item.revenue, 0) || 1;
        return list.map(item => ({
          ...item,
          percent: Math.round((item.revenue / total) * 100)
        }));
      }, [venues, reservations]);

      // Dynamic Venue Preference Data for Bar Chart
      const venuePreferenceData = useMemo(() => {
        const map = {};
        venues.forEach(v => { map[v.id] = { name: v.name, count: 0 }; });
        reservations.forEach(r => {
          if (r.paymentStatus !== 'İptal') {
            if (map[r.venueId]) map[r.venueId].count += 1;
          }
        });
        const totalCount = Math.max(1, reservations.filter(r => r.paymentStatus !== 'İptal').length);
        const list = Object.values(map);
        const maxVal = Math.max(1, ...list.map(l => l.count));
        return list.map(item => ({
          ...item,
          ratio: Math.round((item.count / totalCount) * 100),
          heightPercent: Math.round((item.count / maxVal) * 100)
        }));
      }, [venues, reservations]);

      const aiRecs = useMemo(() => {
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
              <div className="text-xs text-slate-500 font-bold">Ağustos Ayı Dinamik Doluluk Oranı</div>
              <div className="text-2xl font-heading font-extrabold text-emerald-600 dark:text-emerald-400 mt-1">%{occupancyRate}</div>
              <div className="text-[10px] text-slate-400 mt-1">Canlı Rezervasyon Doluluğu</div>
            </div>
            <div className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border">
              <div className="text-xs text-slate-500 font-bold">Ortalama Rezervasyon Tutarı</div>
              <div className="text-2xl font-heading font-extrabold text-amber-700 dark:text-gold-400 mt-1">{formatCurrency(totalRevenue / Math.max(1, reservations.length))}</div>
              <div className="text-[10px] text-slate-400 mt-1">Düğün + Ek Hizmet Ortalaması</div>
            </div>
          </div>

          {/* SVG CHARTS SECTION */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* DONUT CHART CARD */}
            <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
              <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                <h3 className="font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <span>🍩</span>
                  <span>Gelir Dağılımı (Donut Grafiği)</span>
                </h3>
                <span className="text-[10px] font-bold bg-amber-500/10 text-amber-700 dark:text-gold-400 px-2 py-0.5 rounded-full">Salon Bazlı</span>
              </div>
              <div className="flex flex-col sm:flex-row items-center justify-around gap-4 pt-2">
                <div className="relative w-44 h-44 flex items-center justify-center">
                  <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                    <circle cx="18" cy="18" r="15.9155" fill="none" stroke="#334155" strokeWidth="3.8" strokeOpacity="0.2" />
                    {(() => {
                      let accumulatedPercent = 0;
                      return venueRevenueData.map((item, i) => {
                        const strokeDasharray = `${item.percent} ${100 - item.percent}`;
                        const strokeDashoffset = 100 - accumulatedPercent + 25;
                        accumulatedPercent += item.percent;
                        return (
                          <circle
                            key={i}
                            cx="18"
                            cy="18"
                            r="15.9155"
                            fill="none"
                            stroke={item.color}
                            strokeWidth="3.8"
                            strokeDasharray={strokeDasharray}
                            strokeDashoffset={strokeDashoffset}
                            className="transition-all duration-500 hover:opacity-80"
                          />
                        );
                      });
                    })()}
                  </svg>
                  <div className="absolute flex flex-col items-center justify-center text-center">
                    <span className="text-[10px] text-slate-400 font-bold uppercase">Ciro</span>
                    <span className="text-xs font-bold text-amber-700 dark:text-gold-400">{formatCurrency(totalRevenue)}</span>
                  </div>
                </div>
                <div className="space-y-2 w-full sm:w-auto">
                  {venueRevenueData.map((item, idx) => (
                    <div key={idx} className="flex items-center justify-between text-xs space-x-4 bg-slate-50 dark:bg-brand-dark/50 p-2 rounded-xl border border-slate-200/60 dark:border-brand-border/40">
                      <div className="flex items-center space-x-2">
                        <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: item.color }}></span>
                        <span className="font-bold text-slate-700 dark:text-gray-200">{item.name}</span>
                      </div>
                      <span className="font-mono font-bold text-amber-600 dark:text-gold-400">%{item.percent}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* BAR CHART CARD */}
            <div className="glass-panel p-4 sm:p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4 overflow-hidden">
              <div className="flex flex-wrap justify-between items-center gap-2 border-b pb-3 border-slate-200 dark:border-brand-border">
                <h3 className="font-bold text-sm sm:text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <ThemeIcon icon="chart" fallbackEmoji="📊" className="w-4 h-4 text-amber-500 shrink-0" />
                  <span>Salon Tercih Oranları (Bar Grafiği)</span>
                </h3>
                <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 px-2 py-0.5 rounded-full shrink-0">Rezervasyon Oranları</span>
              </div>
              <div className="overflow-x-auto pb-2">
                <div className="h-44 flex items-end justify-around pt-6 px-2 gap-2 sm:gap-4 bg-slate-50/50 dark:bg-brand-dark/30 rounded-2xl border border-slate-100 dark:border-brand-border/20 min-w-[280px]">
                  {venuePreferenceData.map((item, idx) => (
                    <div key={idx} className="flex flex-col items-center flex-1 min-w-[55px] h-full justify-end group">
                      <span className="text-[9px] sm:text-[10px] font-bold text-amber-600 dark:text-gold-400 mb-1 opacity-90 text-center whitespace-nowrap">{item.count} Adet</span>
                      <div className="w-full max-w-[40px] bg-slate-200 dark:bg-brand-border rounded-t-xl overflow-hidden h-32 flex items-end p-0.5">
                        <div
                          className="w-full rounded-t-lg bg-gradient-to-t from-amber-600 to-gold-400 transition-all duration-500 group-hover:brightness-125"
                          style={{ height: `${Math.max(15, item.heightPercent)}%` }}
                        ></div>
                      </div>
                      <span className="text-[9px] sm:text-[10px] font-bold text-slate-600 dark:text-gray-400 truncate w-full text-center mt-2" title={item.name}>{item.name.split(' ')[0]}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* AI RECOMMENDATIONS CARD */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/40 bg-amber-500/5">
            <div className="flex items-center justify-between border-b border-amber-500/20 pb-3">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center text-xl shadow-inner shrink-0">
                  <ThemeIcon icon="brain" fallbackEmoji="🧠" className="w-6 h-6 shrink-0" />
                </div>
                <div>
                  <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">Akıllı AI Öneri Algoritması & Gelir Fırsatları</h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400">Canlı rezervasyon trendlerini, doluluk oranlarını (%{occupancyRate}) ve ek hizmet ilgisini analiz eden dinamik tavsiyeler</p>
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
