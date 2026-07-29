import React, { useState } from 'react';
import { CampaignModalComponent } from '../components/Modals';
import { ThemeIcon } from '../components/ThemeIcon';

export function CampaignsPage({ campaigns = [], onAddCampaign, onEditCampaign }) {
  const [editingCampaign, setEditingCampaign] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* MODAL */}
      {isModalOpen && (
        <CampaignModalComponent
          campaign={editingCampaign}
          onClose={() => { setIsModalOpen(false); setEditingCampaign(null); }}
          onSave={(cmpObj) => {
            if (editingCampaign) {
              onEditCampaign(cmpObj);
            } else {
              onAddCampaign(cmpObj);
            }
            setIsModalOpen(false);
            setEditingCampaign(null);
          }}
        />
      )}

      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
            <ThemeIcon icon="campaign" fallbackEmoji="🏷️" className="w-6 h-6 text-amber-500 shrink-0" />
            <span>İndirim Kodu & Akıllı AI Kampanyaları</span>
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Erken rezervasyon indirimleri tanımlayın, yapay zeka önerilerini tek tıkla kampanyaya dönüştürün.
          </p>
        </div>

        <button
          onClick={() => { setEditingCampaign(null); setIsModalOpen(true); }}
          className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1"
        >
          <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-4 h-4 shrink-0" />
          <span>Yeni Kampanya Tanımla</span>
        </button>
      </div>

      {/* CAMPAIGNS GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {campaigns.map(c => (
          <div key={c.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3 shadow-sm flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-mono font-extrabold text-xs bg-amber-500/10 text-amber-700 dark:text-gold-400 px-3 py-1 rounded-full border border-amber-500/20">
                  {c.code}
                </span>
                <span className="text-[10px] font-bold bg-emerald-500/10 text-emerald-600 px-2 py-0.5 rounded-full">
                  AKTİF KAMPANYA
                </span>
              </div>

              <div>
                <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                  {c.title}
                </h4>
                <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">{c.description}</p>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
              <div className="font-mono font-extrabold text-amber-700 dark:text-gold-400 text-sm">
                {c.discountType === 'fixed' ? `${c.discountValue.toLocaleString()} ₺ İndirim` : `%${c.discountValue} İndirim`}
              </div>
              <button
                onClick={() => { setEditingCampaign(c); setIsModalOpen(true); }}
                className="text-xs font-bold text-slate-600 dark:text-gray-300 hover:underline flex items-center space-x-1"
              >
                <span>Düzenle</span>
                <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
