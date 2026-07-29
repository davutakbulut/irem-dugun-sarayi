import React, { useState } from 'react';
import { formatCurrency } from '../utils/formatters';
import { VenueModalComponent } from '../components/Modals';

export function VenuesPage({ venues = [], onAddVenue, onEditVenue }) {
  const [editingVenue, setEditingVenue] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* MODAL */}
      {isModalOpen && (
        <VenueModalComponent
          venue={editingVenue}
          onClose={() => { setIsModalOpen(false); setEditingVenue(null); }}
          onSave={(vObj) => {
            if (editingVenue) {
              onEditVenue(vObj);
            } else {
              onAddVenue(vObj);
            }
            setIsModalOpen(false);
            setEditingVenue(null);
          }}
        />
      )}

      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            🏰 Düğün Salonları & Kapasite Bilgileri
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Tüm balo salonları ve kır bahçelerinin liste fiyatlarını, görsellerini ve kaporalarını yönetin.
          </p>
        </div>

        <button
          onClick={() => { setEditingVenue(null); setIsModalOpen(true); }}
          className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1"
        >
          <span>➕ Yeni Salon Ekle</span>
        </button>
      </div>

      {/* VENUES GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        {venues.map(v => (
          <div key={v.id} className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border overflow-hidden shadow-sm flex flex-col justify-between">
            <div className="relative h-44 w-full bg-slate-200 dark:bg-brand-dark">
              <img src={v.image} alt={v.name} className="w-full h-full object-cover" />
              <div className="absolute top-3 right-3 bg-slate-900/80 backdrop-blur-md text-white text-xs font-bold px-3 py-1 rounded-full border border-white/20">
                {v.capacity} Kişi
              </div>
            </div>

            <div className="p-5 space-y-3 flex-1 flex flex-col justify-between">
              <div>
                <span className="text-[10px] font-bold text-amber-600 dark:text-gold-400 uppercase tracking-wider">
                  {v.category}
                </span>
                <h4 className="font-heading font-extrabold text-base text-slate-900 dark:text-white mt-1">
                  {v.name}
                </h4>
                <p className="text-xs text-slate-500 dark:text-gray-400 mt-1 line-clamp-2">{v.description}</p>
              </div>

              <div className="pt-3 border-t border-slate-100 dark:border-brand-border flex justify-between items-center text-xs">
                <div>
                  <span className="text-[10px] text-slate-400 font-bold block">Liste Fiyatı:</span>
                  <span className="font-extrabold text-sm text-slate-900 dark:text-white">{formatCurrency(v.price)}</span>
                </div>
                <button
                  onClick={() => { setEditingVenue(v); setIsModalOpen(true); }}
                  className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline"
                >
                  Düzenle ✏️
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
