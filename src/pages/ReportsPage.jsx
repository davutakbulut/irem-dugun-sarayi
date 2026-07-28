import React, { useMemo } from 'react';
import { formatCurrency, generateSmartAIRecommendations } from '../constants';

export default function ReportsPageComponent({ reservations = [], venues = [], services = [], onAddCampaignFromAI, onUpdateVenuePriceFromAI, showToast, navigateTo }) {
  const totalRevenue = reservations.reduce((sum, r) => sum + (r.totalAmount || 0), 0);

  const aiRecommendations = useMemo(() => {
    return generateSmartAIRecommendations(reservations, venues, services);
  }, [reservations, venues, services]);

  const handleConvertCampaign = (aiItem) => {
    const newCamp = {
      id: `c-ai-${Date.now()}`,
      code: aiItem.code || `AI-${Math.floor(1000 + Math.random() * 9000)}`,
      title: aiItem.title.replace(/^[🎯💡🍂⚡]\s*/, ''),
      type: aiItem.type || 'percent',
      value: aiItem.value || 15,
      description: aiItem.description,
      isAiGenerated: true,
      badge: '✨ AI Üretimi',
      active: true
    };

    if (onAddCampaignFromAI) {
      onAddCampaignFromAI(newCamp);
    }
    if (showToast) {
      showToast(`🚀 AI Önerisi Canlı Kampanyalar Sayfasına Enjekte Edildi! Kod: ${newCamp.code}`);
    }
    if (navigateTo) {
      navigateTo('campaigns');
    }
  };

  const handleUpdatePrice = (aiItem) => {
    if (onUpdateVenuePriceFromAI && aiItem.venueId && aiItem.suggestedPrice) {
      onUpdateVenuePriceFromAI(aiItem.venueId, aiItem.suggestedPrice);
      if (showToast) {
        showToast(`💰 ${aiItem.venueName || 'Salon'} Fiyatı AI Tarafından ${formatCurrency(aiItem.suggestedPrice)} Olarak Güncellendi!`);
      }
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Raporlar & Yapay Zeka (AI) Gelir Optimizasyonu</h2>
        <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün salonlarınızın doluluk ve ciro verilerinden öğrenen Akıllı AI Tahmin Motoru</p>
      </div>

      {/* METRIC SUMMARY */}
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

      {/* AI RECOMMENDATION SECTION */}
      <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/40 bg-amber-500/5">
        <div className="flex items-center justify-between border-b border-amber-500/20 pb-3">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center text-xl shadow-inner">
              🧠
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
          {aiRecommendations.map(ai => (
            <div key={ai.id} className="bg-white dark:bg-brand-card p-5 rounded-2xl border border-amber-500/30 flex flex-col justify-between space-y-4 shadow-md hover:scale-[1.02] transition">
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 font-mono font-bold text-xs px-2.5 py-0.5 rounded-full border border-amber-500/20">
                    {ai.code}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-lg">
                    {ai.badge || '✨ AI Önerisi'}
                  </span>
                </div>
                <div className="font-bold text-sm text-slate-800 dark:text-gray-100">{ai.title}</div>
                <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed">{ai.description}</p>
                {ai.canUpdatePrice && (
                  <div className="bg-amber-500/10 p-2.5 rounded-xl border border-amber-500/20 text-xs font-medium space-y-0.5">
                    <div className="text-slate-500 dark:text-gray-400">Mevcut Fiyat: <strong>{formatCurrency(ai.currentPrice)}</strong></div>
                    <div className="text-emerald-600 dark:text-emerald-400 font-bold">Önerilen Fiyat: {formatCurrency(ai.suggestedPrice)}</div>
                  </div>
                )}
              </div>

              <div className="space-y-2 pt-2 border-t border-slate-100 dark:border-brand-border/40">
                <button
                  onClick={() => handleConvertCampaign(ai)}
                  className="w-full gold-button font-bold text-xs py-2.5 px-4 rounded-xl shadow inline-flex items-center justify-center space-x-1 hover:scale-[1.01] transition"
                >
                  <span>Tek Tıkla Kampanyaya Dönüştür 🚀</span>
                </button>

                {ai.canUpdatePrice && (
                  <button
                    onClick={() => handleUpdatePrice(ai)}
                    className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs py-2 px-4 rounded-xl shadow transition inline-flex items-center justify-center space-x-1"
                  >
                    <span>Fiyatı Güncelle & Uygula 💰</span>
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

