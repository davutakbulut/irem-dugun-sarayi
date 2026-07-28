import React from 'react';

export default function CampaignsPageComponent({ campaigns, onAddClick, onEditClick, onDeleteClick }) {
  return (
    <div className="space-y-6 animate-fade-in pb-12">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Özel Kampanyalar & İndirim Kodu Yönetimi</h2>
          <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Düğün ve kiralama rezervasyonlarında geçerli promosyon ve indirim kodları</p>
        </div>
        <button
          onClick={onAddClick}
          className="gold-button font-bold text-xs py-2.5 px-4 rounded-2xl shadow-lg flex items-center justify-center space-x-1"
        >
          <span>➕</span>
          <span>Yeni Özel Kampanya Ekle</span>
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {campaigns.map(c => (
          <div key={c.id} className="glass-panel p-5 rounded-3xl space-y-3 border border-amber-500/30 flex flex-col justify-between shadow-md hover:scale-[1.02] transition">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="font-mono font-bold text-xs text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2.5 py-1 rounded-xl border border-amber-500/20">
                  {c.code}
                </span>
                <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-lg">
                  {c.type === 'percent' ? `%${c.value} İndirim` : c.type === 'amount' ? `${c.value} TL İndirim` : 'Hediye Paket'}
                </span>
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
  );
}
