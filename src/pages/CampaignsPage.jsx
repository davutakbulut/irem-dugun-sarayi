import React, { useMemo } from 'react';
import { formatCurrency, generateSmartAIRecommendations } from '../constants';

export default function CampaignsPageComponent({ campaigns = [], venues = [], services = [], reservations = [], onAddClick, onEditClick, onDeleteClick, onAddCampaignFromAI, onUpdateVenuePriceFromAI, showToast }) {

  const aiRecommendations = useMemo(() => {
    return generateSmartAIRecommendations(reservations, venues, services);
  }, [reservations, venues, services]);

  const handleConvertFromAI = (aiItem) => {
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
      showToast(`🚀 AI Önerisi Anında Kampanyalar Listesine Ekledi! Kod: ${newCamp.code}`);
    }
  };

  const handleUpdatePriceFromAI = (aiItem) => {
    if (onUpdateVenuePriceFromAI && aiItem.venueId && aiItem.suggestedPrice) {
      onUpdateVenuePriceFromAI(aiItem.venueId, aiItem.suggestedPrice);
      if (showToast) {
        showToast(`💰 ${aiItem.venueName || 'Salon'} Fiyatı AI Tarafından Güncellendi: ${formatCurrency(aiItem.suggestedPrice)}`);
      }
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      {/* HEADER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Özel Kampanyalar & İndirim Kodu Yönetimi</h2>
          <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün ve kiralama rezervasyonlarında geçerli promosyon, indirim ve AI destekli kampanyalar</p>
        </div>
        <button
          onClick={onAddClick}
          className="gold-button font-bold text-xs py-2.5 px-4 rounded-2xl shadow-lg flex items-center justify-center space-x-1"
        >
          <span>➕</span>
          <span>Yeni Özel Kampanya Ekle</span>
        </button>
      </div>

      {/* AI RECOMMENDATION LIVE FEED ON CAMPAIGNS PAGE */}
      <div className="glass-panel p-5 rounded-3xl space-y-4 border border-amber-500/40 bg-gradient-to-r from-amber-500/10 via-amber-500/5 to-transparent shadow-md">
        <div className="flex items-center justify-between border-b border-amber-500/20 pb-3">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-2xl bg-amber-500/20 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center text-lg">
              🧠
            </div>
            <div>
              <h3 className="font-heading font-bold text-sm text-slate-800 dark:text-gray-100">AI Akıllı Öneri Akışı – Canlı Kampanya Önerileri</h3>
              <p className="text-[11px] text-slate-500 dark:text-gray-400">Tek tıkla önerileri canlı kampanya listesine dahil edin</p>
            </div>
          </div>
          <span className="text-[10px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2.5 py-1 rounded-full border border-amber-500/30">
            Canlı AI Algoritması
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {aiRecommendations.map(ai => (
            <div key={ai.id} className="bg-white dark:bg-brand-card p-4 rounded-2xl border border-amber-500/30 flex flex-col justify-between space-y-3 shadow hover:shadow-lg transition">
              <div className="space-y-1.5">
                <div className="flex justify-between items-center">
                  <span className="font-mono font-bold text-[11px] text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-lg border border-amber-500/20">
                    {ai.code}
                  </span>
                  <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-md">
                    {ai.badge || '✨ AI Teklifi'}
                  </span>
                </div>
                <div className="font-bold text-xs text-slate-800 dark:text-gray-100">{ai.title}</div>
                <p className="text-[11px] text-slate-600 dark:text-gray-300 leading-tight">{ai.description}</p>
              </div>

              <div className="space-y-1.5 pt-2 border-t border-slate-100 dark:border-brand-border/40">
                <button
                  onClick={() => handleConvertFromAI(ai)}
                  className="w-full gold-button font-bold text-[11px] py-2 px-3 rounded-xl shadow inline-flex items-center justify-center space-x-1"
                >
                  <span>Tek Tıkla Kampanyaya Dönüştür 🚀</span>
                </button>

                {ai.canUpdatePrice && (
                  <button
                    onClick={() => handleUpdatePriceFromAI(ai)}
                    className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-[11px] py-1.5 px-3 rounded-xl shadow transition inline-flex items-center justify-center space-x-1"
                  >
                    <span>Fiyatı Güncelle & Uygula 💰</span>
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ACTIVE CAMPAIGNS GRID */}
      <div>
        <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 mb-3 flex items-center space-x-2">
          <span>🎁 Aktif Promosyon ve Kampanyalar ({campaigns.length})</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {campaigns.map(c => (
            <div
              key={c.id}
              className={`glass-panel p-5 rounded-3xl space-y-3 flex flex-col justify-between shadow-md hover:scale-[1.01] transition border ${
                c.isAiGenerated ? 'border-amber-500/60 bg-amber-500/5' : 'border-amber-500/30'
              }`}
            >
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-mono font-bold text-xs text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2.5 py-1 rounded-xl border border-amber-500/20">
                    {c.code}
                  </span>
                  <div className="flex items-center space-x-1">
                    {c.isAiGenerated && (
                      <span className="text-[10px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/20 px-2 py-0.5 rounded-lg border border-amber-500/40">
                        ✨ AI Üretimi
                      </span>
                    )}
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-lg">
                      {c.type === 'percent' ? `%${c.value} İndirim` : c.type === 'amount' ? `${c.value} TL İndirim` : 'Hediye Paket'}
                    </span>
                  </div>
                </div>
                <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{c.title}</h3>
                <p className="text-xs text-slate-500 dark:text-gray-400 leading-relaxed">{c.description}</p>
              </div>

              <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border/40 text-xs">
                <button onClick={() => onEditClick(c)} className="px-3 py-1.5 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-300 rounded-xl font-bold hover:bg-amber-500/20">Düzenle</button>
                <button onClick={() => onDeleteClick(c.id)} className="px-3 py-1.5 bg-red-500/10 text-red-600 rounded-xl font-bold hover:bg-red-500 hover:text-white transition">Sil</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

