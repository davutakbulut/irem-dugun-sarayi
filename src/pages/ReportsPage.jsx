import React from 'react';
import { formatCurrency, AI_RECOMMENDATIONS } from '../constants';

export default function ReportsPageComponent({ reservations, onAddCampaignFromAI, showToast, navigateTo }) {
  const totalRevenue = reservations.reduce((sum, r) => sum + r.totalAmount, 0);

  const handleConvertCampaign = (aiItem) => {
    const newCamp = {
      id: `c-ai-${Date.now()}`,
      code: aiItem.code || `AI-${Math.floor(1000 + Math.random() * 9000)}`,
      title: aiItem.title,
      type: aiItem.type || 'percent',
      value: aiItem.value || 15,
      description: aiItem.description
    };

    if (onAddCampaignFromAI) {
      onAddCampaignFromAI(newCamp);
    }
    showToast(`🚀 AI Önerisi Başarıyla Kampanyaya Dönüştürüldü! Kod: ${newCamp.code}`);
    navigateTo('campaigns');
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Raporlar & Yapay Zeka (AI) Gelir Optimizasyonu</h2>
        <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün salonlarınızın doluluk ve ciro verilerinden öğrenen AI tahmin motoru</p>
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
        <div className="flex items-center space-x-3 border-b border-amber-500/20 pb-3">
          <div className="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center text-xl">
            🧠
          </div>
          <div>
            <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">Yapay Zeka (AI) Akıllı Kampanya & Fiyatlandırma Önerileri</h3>
            <p className="text-xs text-slate-500 dark:text-gray-400">Canlı rezervasyon trendlerini analiz eden otomatik gelir artırma teklifleri</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
          {AI_RECOMMENDATIONS.map(ai => (
            <div key={ai.id} className="bg-white dark:bg-brand-card p-5 rounded-2xl border border-amber-500/30 flex flex-col justify-between space-y-3 shadow-md hover:scale-[1.02] transition">
              <div className="space-y-2">
                <div className="font-bold text-sm text-slate-800 dark:text-gray-100">{ai.title}</div>
                <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed">{ai.description}</p>
              </div>
              <button
                onClick={() => handleConvertCampaign(ai)}
                className="w-full gold-button font-bold text-xs py-2.5 px-4 rounded-xl shadow inline-flex items-center justify-center space-x-1"
              >
                <span>{ai.actionText}</span>
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
