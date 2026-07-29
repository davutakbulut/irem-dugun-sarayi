import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';
import { OptimizedImage } from '../components/OptimizedImage';

    export function VenuesPage({ venues, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Düğün Salonlarım</h2>
            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow">➕ Yeni Düğün Salonu Ekle</button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {venues.map(v => (
              <div key={v.id} className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden space-y-3 shadow-sm flex flex-col justify-between">
                <div>
                  <OptimizedImage src={v.image || v.images[0]} alt={`${v.name} Görseli`} className="w-full h-44" />
                  <div className="p-4 space-y-2">
                    <div className="flex justify-between items-center">
                      <h3 className="font-bold text-base text-slate-800 dark:text-gray-100">{v.name}</h3>
                      <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-2 py-0.5 rounded-full">{v.category}</span>
                    </div>
                    <div className="text-xs text-slate-600 dark:text-gray-300 font-bold">Kapasite: {v.capacity} Kişi | Fiyat: {formatCurrency(v.price)}</div>
                    <p className="text-xs text-slate-500 dark:text-gray-400">{v.description}</p>
                  </div>
                </div>

                <div className="p-4 pt-0 flex space-x-2">
                  <button onClick={() => onEditClick(v)} className="flex-1 py-1.5 rounded-xl bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/30 flex items-center justify-center space-x-1">
                    <span>Düzenle</span>
                    <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                  </button>
                  <button onClick={() => onDeleteClick(v.id)} className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 font-extrabold text-xs uppercase tracking-wider border border-red-500/30 inline-flex items-center space-x-1.5 transition shadow-2xs group">
                    <span className="group-hover:text-white transition">SİL</span>
                    <ThemeIcon icon="delete" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0 text-red-600 dark:text-red-400 group-hover:text-white transition" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- SERVICES COMPONENT ---