import React, { useState, useEffect, useRef, useMemo } from 'react';
import { formatCurrency, formatDate } from '../utils/formatters.js';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function DashboardComponent({ activeRole, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {
      const totalRevenue = useMemo(() => {
        return reservations.reduce((sum, r) => sum + (r.totalAmount || 0), 0);
      }, [reservations]);

      const occupancyRate = useMemo(() => {
        const totalVenueSlots = Math.max(1, venues.length) * 30;
        const validResCount = reservations.filter(r => r.paymentStatus !== 'İptal').length;
        return Math.min(100, Math.round((validResCount / totalVenueSlots) * 100));
      }, [reservations, venues]);

      const venueRevenueData = useMemo(() => {
        const map = {};
        venues.forEach(v => { map[v.id] = { name: v.name, color: '#f59e0b', revenue: 0 }; });
        const colors = ['#f59e0b', '#10b981', '#6366f1', '#ec4899', '#8b5cf6', '#14b8a6'];
        venues.forEach((v, idx) => {
          if (map[v.id]) map[v.id].color = colors[idx % colors.length];
        });
        reservations.forEach(r => {
          if (r.paymentStatus !== 'İptal' && map[r.venueId]) {
            map[r.venueId].revenue += (r.totalAmount || 0);
          }
        });
        const list = Object.values(map);
        const total = list.reduce((s, item) => s + item.revenue, 0) || 1;
        return list.map(item => ({
          ...item,
          percent: Math.round((item.revenue / total) * 100)
        }));
      }, [venues, reservations]);

      const venuePreferenceData = useMemo(() => {
        const map = {};
        venues.forEach(v => { map[v.id] = { name: v.name, count: 0 }; });
        reservations.forEach(r => {
          if (r.paymentStatus !== 'İptal' && map[r.venueId]) {
            map[r.venueId].count += 1;
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
        return generateSmartAIRecommendations(reservations, venues, []);
      }, [reservations, venues]);

      return (
        <div className="space-y-6 pb-12 animate-fade-in">
          {/* HEADER BANNER */}
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
                <span>
                  {activeRole === 'admin' && 'Hoş Geldiniz, İrem Hanım (Admin)'}
                  {activeRole === 'satisci' && 'Satış Operasyon Paneli - İrem Düğün Sarayı'}
                  {activeRole === 'sosyal_medyaci' && 'Medya & Fotoğraf Yönetim Ekranı'}
                  {activeRole === 'musteri' && 'Değerli Müşterimiz, Hoş Geldiniz! 💍'}
                </span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                {activeRole === 'admin' && 'İrem Düğün Sarayı genel finansal ciro verileri, canlı analiz grafikleri ve yapay zeka önerileri.'}
                {activeRole === 'satisci' && 'Düğün salonu kiralama durumları, boş gün takvimi ve aktif rezervasyon satış süreçleri.'}
                {activeRole === 'sosyal_medyaci' && 'Salon galerisi görselleri, medya yükleme alanı ve içerik takvimi takibi.'}
                {activeRole === 'musteri' && 'Düğün organizasyonunuzun canlı detayları, salon bilgileri ve kalan ödeme bakiyeniz.'}
              </p>
            </div>

            {(activeRole === 'admin' || activeRole === 'satisci') && (
              <button onClick={onNewResClick} className="gold-button font-bold px-6 py-3 rounded-2xl shadow-lg flex items-center space-x-2 text-xs cursor-pointer hover:scale-105 transition">
                <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 shrink-0" />
                <span>Yeni Rezervasyon Oluştur</span>
              </button>
            )}
            {activeRole === 'sosyal_medyaci' && (
              <button onClick={() => onTabChange && onTabChange('media')} className="gold-button font-bold px-6 py-3 rounded-2xl shadow-lg flex items-center space-x-2 text-xs cursor-pointer hover:scale-105 transition">
                <ThemeIcon icon="camera" fallbackEmoji="📸" className="w-4 h-4 shrink-0" />
                <span>Fotoğraf & Medya Yükle</span>
              </button>
            )}
            {activeRole === 'musteri' && (
              <button onClick={() => onTabChange && onTabChange('reservations')} className="gold-button font-bold px-6 py-3 rounded-2xl shadow-lg flex items-center space-x-2 text-xs cursor-pointer hover:scale-105 transition">
                <ThemeIcon icon="list" fallbackEmoji="📋" className="w-4 h-4 shrink-0" />
                <span>Rezervasyon Detaylarımı Gör</span>
              </button>
            )}
          </div>

          {/* ========================================================================= */}
          {/* 👑 ADMIN EXCLUSIVE DASHBOARD: FINANCIAL CHARTS, AI ENGINE & FULL METRICS */}
          {/* ========================================================================= */}
          {activeRole === 'admin' && (
            <>
              {/* TOP FINANCIAL KPI METRICS */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Toplam Etkinlik Mekanı</div>
                  <div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length} Mekan</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Canlı Doluluk Oranı</div>
                  <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">%{occupancyRate}</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Son Ay Toplam Kazanç</div>
                  <div className="text-2xl font-bold gold-gradient-text mt-1">{formatCurrency(financialStats?.totalRev || totalRevenue)}</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-red-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Bekleyen Ödemeler</div>
                  <div className="text-2xl font-bold text-red-500 dark:text-red-400 mt-1">{formatCurrency(financialStats?.totalPending || 0)}</div>
                </div>
              </div>

              {/* INTERACTIVE SVG CHARTS SECTION */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* DONUT CHART CARD */}
                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
                  <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                    <h3 className="font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <ThemeIcon icon="chart" fallbackEmoji="🍩" className="w-4 h-4 text-amber-500 shrink-0" />
                      <span>Gelir Dağılımı (Donut Grafiği)</span>
                    </h3>
                    <span className="text-[10px] font-bold bg-amber-500/10 text-amber-700 dark:text-gold-400 px-2.5 py-1 rounded-full">Salon Bazlı</span>
                  </div>
                  <div className="flex flex-col sm:flex-row items-center justify-around gap-4 pt-2">
                    <div className="relative w-44 h-44 flex items-center justify-center shrink-0">
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
                        <span className="text-[10px] text-slate-400 font-bold">Toplam Ciro</span>
                        <span className="text-xs font-black gold-gradient-text">{formatCurrency(totalRevenue)}</span>
                      </div>
                    </div>
                    <div className="space-y-2 text-xs w-full max-w-[200px]">
                      {venueRevenueData.map((item, i) => (
                        <div key={i} className="flex justify-between items-center text-slate-700 dark:text-gray-300">
                          <div className="flex items-center space-x-2">
                            <span className="w-3 h-3 rounded-full shrink-0" style={{ backgroundColor: item.color }} />
                            <span className="truncate max-w-[110px] font-bold text-[11px]">{item.name}</span>
                          </div>
                          <span className="font-extrabold text-[11px]">%{item.percent}</span>
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
                    <span className="text-[10px] font-bold bg-amber-500/10 text-amber-700 dark:text-gold-400 px-2.5 py-1 rounded-full shrink-0">Kiralama Sayısı</span>
                  </div>
                  <div className="overflow-x-auto pb-2">
                    <div className="h-44 flex items-end justify-between gap-2 sm:gap-3 pt-6 px-1 min-w-[280px]">
                      {venuePreferenceData.map((item, i) => (
                        <div key={i} className="flex-1 min-w-[55px] flex flex-col items-center h-full justify-end group relative">
                          <div className="text-[9px] sm:text-[10px] font-bold text-amber-700 dark:text-gold-400 mb-1 text-center whitespace-nowrap">{item.count} Etkinlik</div>
                          <div
                            className="w-full bg-gradient-to-t from-amber-600 to-amber-400 rounded-t-xl transition-all duration-500 group-hover:brightness-125 min-h-[16px]"
                            style={{ height: `${Math.max(15, item.heightPercent)}%` }}
                          />
                          <span className="text-[9px] sm:text-[10px] font-bold text-slate-600 dark:text-gray-400 mt-2 truncate w-full text-center" title={item.name}>{item.name.replace('Salon', '').trim()}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* AI RECOMMENDATIONS BANNER */}
              {aiRecs && aiRecs.length > 0 && (
                <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 space-y-4 shadow-sm">
                  <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                    <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <ThemeIcon icon="sparkles" fallbackEmoji="🎯" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Yapay Zeka (AI) Akıllı Fiyat & Kampanya Önerileri</span>
                    </h3>
                    <button onClick={() => onTabChange && onTabChange('reports')} className="text-xs text-amber-600 font-bold hover:underline cursor-pointer">Tüm Raporlar →</button>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {aiRecs.slice(0, 2).map((rec, i) => (
                      <div key={i} className="p-4 rounded-2xl bg-white/60 dark:bg-brand-card/60 border border-slate-200 dark:border-brand-border space-y-3">
                        <div className="flex justify-between items-start">
                          <h4 className="font-bold text-xs text-amber-800 dark:text-gold-400 flex items-center space-x-1.5">
                            <span>{rec.title}</span>
                          </h4>
                          <span className="text-[9px] font-extrabold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-800 dark:text-gold-400">{rec.badge}</span>
                        </div>
                        <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed font-medium">{rec.description}</p>
                        <div className="pt-1 flex items-center space-x-2">
                          {rec.actionType === 'create_campaign' && (
                            <button
                              onClick={() => onConvertToCampaign && onConvertToCampaign(rec)}
                              className="gold-button px-3.5 py-1.5 rounded-xl text-[11px] font-bold shadow hover:scale-105 transition cursor-pointer"
                            >
                              🎁 Tek Tıkla Kampanyaya Dönüştür
                            </button>
                          )}
                          {rec.actionType === 'update_price' && (
                            <button
                              onClick={() => onUpdateVenuePrice && onUpdateVenuePrice(rec.venueId, rec.suggestedPrice)}
                              className="px-3.5 py-1.5 rounded-xl text-[11px] font-bold bg-emerald-600 hover:bg-emerald-500 text-white shadow hover:scale-105 transition cursor-pointer"
                            >
                              💰 Fiyatı Güncelle & Uygula
                            </button>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          )}

          {/* ========================================================================= */}
          {/* 💼 SATIŞÇI OPERASYON PANELİ (SALES SPECIALIST DASHBOARD) */}
          {/* ========================================================================= */}
          {activeRole === 'satisci' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Aktif Salon Sayısı</div>
                  <div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">{venues.length} Salon</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Bu Ayın Boş Günleri</div>
                  <div className="text-2xl font-bold gold-gradient-text mt-1">12 Gün</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-emerald-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Kapora Alınan Rezervasyon</div>
                  <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">{reservations.filter(r => r.depositPaid > 0).length} Adet</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-indigo-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Satış Dönüşüm Oranı</div>
                  <div className="text-2xl font-bold text-indigo-600 dark:text-indigo-400 mt-1">%84</div>
                </div>
              </div>

              <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border/40 space-y-4">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-5 h-5 text-amber-500 shrink-0" />
                    <span>Satışçı Hızlı Çalışma Masası & Randevular</span>
                  </h3>
                  <button onClick={onNewResClick} className="gold-button px-4 py-2 rounded-xl text-xs font-bold shadow hover:scale-105 transition cursor-pointer">
                    ➕ Yeni Rezervasyon Kaydı
                  </button>
                </div>
                <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-900 dark:text-gold-300 font-medium">
                  💡 <strong>Satış İpucu:</strong> Ağutos ve Eylül aylarındaki son 12 boş gün için özel %10 indirim kuponunu müşterilerinize teklif edebilirsiniz.
                </div>
              </div>
            </div>
          )}

          {/* ========================================================================= */}
          {/* 📸 SOSYAL MEDYACI İÇERİK PANELİ (MEDIA SPECIALIST DASHBOARD) */}
          {/* ========================================================================= */}
          {activeRole === 'sosyal_medyaci' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="glass-panel p-5 rounded-2xl border border-slate-200 dark:border-brand-border/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Toplam Yüklenen Medya</div>
                  <div className="text-2xl font-bold text-slate-800 dark:text-gray-100 mt-1">48 Dosya</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-amber-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Yayındaki Galeri Görselleri</div>
                  <div className="text-2xl font-bold gold-gradient-text mt-1">36 Görsel</div>
                </div>
                <div className="glass-panel p-5 rounded-2xl border border-purple-500/40 shadow-sm">
                  <div className="text-xs text-slate-500 dark:text-gray-400">Onay Bekleyen Medyalar</div>
                  <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">12 Adet</div>
                </div>
              </div>

              <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-4">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="camera" fallbackEmoji="📸" className="w-5 h-5 text-amber-500 shrink-0" />
                    <span>Salon Görsel Galerisi & Medya Yükleme</span>
                  </h3>
                  <button onClick={() => onTabChange && onTabChange('media')} className="gold-button px-4 py-2 rounded-xl text-xs font-bold shadow hover:scale-105 transition cursor-pointer">
                    📷 Hızlı Medya Yükleme Paneli
                  </button>
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
                  {venues.map(v => (
                    <div key={v.id} className="relative rounded-2xl overflow-hidden border border-slate-200 dark:border-brand-border/40 group">
                      <img src={v.image} alt={v.name} className="w-full h-24 object-cover group-hover:scale-110 transition duration-300" />
                      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent p-2 flex flex-col justify-end">
                        <span className="text-[11px] font-bold text-white truncate">{v.name}</span>
                        <span className="text-[9px] text-gold-400 font-bold">{v.category}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ========================================================================= */}
          {/* 💍 MÜŞTERİ ÖZEL DÜĞÜN PORTALI (CUSTOMER PORTAL DASHBOARD) */}
          {/* ========================================================================= */}
          {activeRole === 'musteri' && (
            <div className="space-y-6">
              {/* DÜĞÜN KONTROL & SAYAC BANNER */}
              <div className="glass-panel p-6 rounded-3xl border-2 border-amber-500/50 bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent space-y-4 shadow-lg">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                  <div>
                    <span className="bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-[10px] font-extrabold px-3 py-1 rounded-full border border-emerald-500/30">
                      ✓ Rezervasyonunuz Onaylandı
                    </span>
                    <h3 className="text-xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2">
                      Düğün Gününüze Son <span className="gold-gradient-text text-2xl">24 GÜN</span> Kaldı! 🎉
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      Sayın <strong>Ahmet Yılmaz & Elif Kaya</strong>, İrem Düğün Sarayı Safir Balo Salonu'nda rüya gibi bir gece sizi bekliyor.
                    </p>
                  </div>
                  <WhatsAppButton phone="05321234567" customerName="Ahmet Yılmaz" text="Organizatör İle WhatsApp'tan Görüş" />
                </div>
              </div>

              {/* EVENT DETAILS & BALANCE CARDS */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3">
                  <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2 border-b pb-2 border-slate-200 dark:border-brand-border">
                    <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-4 h-4 text-amber-500 shrink-0" />
                    <span>Etkinlik & Salon Bilgileriniz</span>
                  </h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Kiralanan Salon:</span>
                      <span className="font-bold">Safir Balo Salonu (750 Kişi)</span>
                    </div>
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Etkinlik Tarihi:</span>
                      <span className="font-bold text-amber-700 dark:text-gold-400">15 Ağustos 2026</span>
                    </div>
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Saat Dilimi:</span>
                      <span className="font-bold">19:00 - 23:30 (Akşam Seansı)</span>
                    </div>
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Dahil Hizmetler:</span>
                      <span className="font-bold text-emerald-600 dark:text-emerald-400">Orkestra, HD Video, VIP Süsleme</span>
                    </div>
                  </div>
                </div>

                <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3">
                  <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2 border-b pb-2 border-slate-200 dark:border-brand-border">
                    <ThemeIcon icon="money" fallbackEmoji="💰" className="w-4 h-4 text-amber-500 shrink-0" />
                    <span>Ödeme & Bakiye Özeti</span>
                  </h4>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Toplam Anlaşma Tutarı:</span>
                      <span className="font-bold">75.000 ₺</span>
                    </div>
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Ödenen Kapora:</span>
                      <span className="font-bold text-emerald-600 dark:text-emerald-400">25.000 ₺ (Ödendi ✓)</span>
                    </div>
                    <div className="flex justify-between text-slate-700 dark:text-gray-300">
                      <span className="text-slate-400">Kalan Net Bakiye:</span>
                      <span className="font-extrabold text-amber-700 dark:text-gold-400 text-sm">50.000 ₺</span>
                    </div>
                    <div className="pt-2">
                      <button onClick={() => onTabChange && onTabChange('reservations')} className="w-full py-2 rounded-xl gold-button text-xs font-bold shadow hover:scale-102 transition cursor-pointer">
                        📄 Sözleşme & Fatura Özetini İndir (PDF)
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* ========================================================================= */}
          {/* RECENT RESERVATIONS SUMMARY TABLE (ADMIN & SATIŞÇI ROLES ONLY) */}
          {/* ========================================================================= */}
          {(activeRole === 'admin' || activeRole === 'satisci') && (
            <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border/40 space-y-4">
              <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                <h3 className="font-bold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <ThemeIcon icon="list" fallbackEmoji="📋" className="w-5 h-5 text-amber-500 shrink-0" />
                  <span>Son Rezervasyon Hareketleri</span>
                </h3>
                <button onClick={() => onTabChange && onTabChange('reservations')} className="text-xs text-amber-600 font-bold hover:underline cursor-pointer">Tüm Listeyi Gör →</button>
              </div>

              <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-slate-200 dark:border-brand-border text-slate-400 uppercase tracking-wider text-[10px]">
                      <th className="py-2.5 px-3">Kod</th>
                      <th className="py-2.5 px-3">Müşteri</th>
                      <th className="py-2.5 px-3">Tarih</th>
                      <th className="py-2.5 px-3">Tutar</th>
                      <th className="py-2.5 px-3">Durum</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/30">
                    {reservations.slice(0, 5).map(r => (
                      <tr key={r.id} className="hover:bg-slate-50 dark:hover:bg-brand-dark/50 transition">
                        <td className="py-2.5 px-3 font-mono font-bold text-amber-700 dark:text-gold-400">{r.id}</td>
                        <td className="py-2.5 px-3 font-bold text-slate-800 dark:text-gray-200">{r.customerName}</td>
                        <td className="py-2.5 px-3 text-slate-600 dark:text-gray-400">{formatDate(r.date)} ({r.timeSlot})</td>
                        <td className="py-2.5 px-3 font-bold text-slate-800 dark:text-gray-100">{formatCurrency(r.totalAmount)}</td>
                        <td className="py-2.5 px-3">
                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold ${
                            r.paymentStatus === 'Tamamlandı' ? 'bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30' :
                            r.paymentStatus === 'Kapora Alındı' ? 'bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30' :
                            'bg-red-500/20 text-red-600 border border-red-500/30'
                          }`}>
                            {r.paymentStatus}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      );
    }

    // --- VENUE MODAL COMPONENT ---
