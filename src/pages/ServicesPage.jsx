import React from 'react';
import { formatCurrency } from '../utils/formatters';
import { ThemeIcon } from '../components/ThemeIcon';

    export function ServicesPage({ services, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-6 h-6 text-amber-500 shrink-0" />
              <span>Ek Hizmetlerim</span>
            </h2>
            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center space-x-1">
              <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 shrink-0" />
              <span>Yeni Ek Hizmet Ekle</span>
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map(s => (
              <div key={s.id} className="glass-panel p-4 rounded-2xl space-y-3 shadow-sm flex flex-col justify-between">
                <div>
                  <OptimizedImage src={s.image} alt={`${s.name} Görseli`} className="w-full h-32 rounded-xl border border-slate-200 dark:border-brand-border" />
                  <div className="flex justify-between items-center pt-2">
                    <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{s.name}</h3>
                    <span className="font-bold text-xs text-amber-700 dark:text-gold-400">{formatCurrency(s.price)}</span>
                  </div>
                  <p className="text-xs text-slate-500 dark:text-gray-400 pt-1">{s.description}</p>
                </div>

                <div className="flex space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border/40">
                  <button onClick={() => onEditClick(s)} className="flex-1 py-1.5 rounded-xl bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/30 flex items-center justify-center space-x-1">
                    <span>Düzenle</span>
                    <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                  </button>
                  <button onClick={() => onDeleteClick(s.id)} className="px-3 py-1.5 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 font-extrabold text-xs uppercase tracking-wider border border-red-500/30 inline-flex items-center space-x-1.5 transition shadow-2xs group">
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

    // --- UNIFIED RESERVATIONS & MASTER CALENDAR COMPONENT ---