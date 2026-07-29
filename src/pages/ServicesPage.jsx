import React, { useState } from 'react';
import { formatCurrency } from '../utils/formatters';
import { ServiceModalComponent } from '../components/Modals';

export function ServicesPage({ services = [], onAddService, onEditService }) {
  const [editingService, setEditingService] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* MODAL */}
      {isModalOpen && (
        <ServiceModalComponent
          service={editingService}
          onClose={() => { setIsModalOpen(false); setEditingService(null); }}
          onSave={(sObj) => {
            if (editingService) {
              onEditService(sObj);
            } else {
              onAddService(sObj);
            }
            setIsModalOpen(false);
            setEditingService(null);
          }}
        />
      )}

      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            🎁 Ek Hizmetler & Birim Fiyat Kataloğu
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Catering, orkestra, video çekimi ve şov ikram paketlerinin birim fiyatlarını yönetin.
          </p>
        </div>

        <button
          onClick={() => { setEditingService(null); setIsModalOpen(true); }}
          className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1"
        >
          <span>➕ Yeni Hizmet Ekle</span>
        </button>
      </div>

      {/* SERVICES GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map(s => (
          <div key={s.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3 shadow-sm flex flex-col justify-between">
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 bg-amber-500/10 px-2.5 py-0.5 rounded-full border border-amber-500/20">
                  {s.category}
                </span>
                <span className="text-[10px] text-slate-400 font-bold">
                  {s.pricingType === 'per_person' ? 'Kişi Başı' : 'Sabit Paket'}
                </span>
              </div>

              <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">
                {s.name}
              </h4>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">{s.description}</p>
            </div>

            <div className="pt-3 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
              <div className="font-mono font-extrabold text-slate-900 dark:text-white text-sm">
                {formatCurrency(s.price)} {s.pricingType === 'per_person' ? '/Kişi' : '/Paket'}
              </div>
              <button
                onClick={() => { setEditingService(s); setIsModalOpen(true); }}
                className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline"
              >
                Düzenle ✏️
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
