import React, { useState, useEffect, useRef, useMemo } from 'react';
import { formatCurrency } from '../utils/formatters.js';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function ServicesComponent({ services, onAddClick, onEditClick, onDeleteClick }) {
      const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'table'
      const [searchTerm, setSearchTerm] = useState('');
      const [categoryFilter, setCategoryFilter] = useState('ALL');

      const categories = useMemo(() => {
        const set = new Set(services.map(s => s.category).filter(Boolean));
        return ['ALL', ...Array.from(set)];
      }, [services]);

      const filteredServices = useMemo(() => {
        return services.filter(s => {
          const matchesCategory = categoryFilter === 'ALL' || s.category === categoryFilter;
          const matchesSearch = !searchTerm || (
            s.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            s.category?.toLowerCase().includes(searchTerm.toLowerCase())
          );
          return matchesCategory && matchesSearch;
        });
      }, [services, categoryFilter, searchTerm]);

      return (
        <div className="space-y-6">
          {/* HEADER & PRIMARY ACTION */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200 dark:border-brand-border/40">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
                <ThemeIcon icon="gift" fallbackEmoji="" className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-gray-100 gold-gradient-text">
                  Ek Hizmetlerim
                </h2>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  Toplam {filteredServices.length} ek hizmet seçeneği tanımlı
                </p>
              </div>
            </div>

            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center justify-center space-x-1.5 self-start sm:self-auto">
              <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 shrink-0" />
              <span>Yeni Ek Hizmet Ekle</span>
            </button>
          </div>

          {/* FILTER TOOLBAR & VIEW MODE SWITCHER */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 shadow-sm">
            
            {/* SEARCH INPUT */}
            <div className="flex-1 relative min-w-[200px]">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4" />
              </span>
              <input
                type="text"
                placeholder="Hizmet adı veya açıklamasında ara..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border text-xs text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500 transition"
              />
              {searchTerm && (
                <button onClick={() => setSearchTerm('')} className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-gray-200 text-xs">
                  ✕
                </button>
              )}
            </div>

            {/* CATEGORY FILTER */}
            {categories.length > 1 && (
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-slate-500 dark:text-gray-400 shrink-0">Kategori:</span>
                <select
                  value={categoryFilter}
                  onChange={e => setCategoryFilter(e.target.value)}
                  className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-2 text-xs font-bold text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500"
                >
                  {categories.map(c => (
                    <option key={c} value={c}>
                      {c === 'ALL' ? 'Tüm Kategoriler' : c}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* VIEW MODE TOGGLE BUTTONS */}
            <div className="flex items-center p-1 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border shrink-0 self-end md:self-auto">
              <button
                onClick={() => setViewMode('grid')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                  viewMode === 'grid'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-gray-100'
                }`}
                title="Kart Izgara Görünümü"
              >
                <ThemeIcon icon="grid" fallbackEmoji="🎴" className="w-4 h-4 shrink-0" />
                <span>Kart Görünümü</span>
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                  viewMode === 'table'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-gray-100'
                }`}
                title="Detaylı Tablo Görünümü"
              >
                <ThemeIcon icon="list" fallbackEmoji="📋" className="w-4 h-4 shrink-0" />
                <span>Tablo Görünümü</span>
              </button>
            </div>

          </div>

          {/* CONTENT: GRID MODE vs TABLE MODE */}
          {filteredServices.length === 0 ? (
            <div className="glass-panel p-12 text-center rounded-3xl border border-dashed border-slate-300 dark:border-brand-border space-y-3">
              <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-10 h-10 mx-auto text-slate-400 opacity-60" />
              <div className="font-bold text-slate-700 dark:text-gray-300 text-sm">Aramanızla Eşleşen Ek Hizmet Bulunamadı</div>
              <p className="text-xs text-slate-500 dark:text-gray-400">Filtre kriterlerinizi temizleyerek tekrar arayabilirsiniz.</p>
              <button onClick={() => { setSearchTerm(''); setCategoryFilter('ALL'); }} className="px-4 py-2 rounded-xl bg-amber-500/10 text-amber-600 font-bold text-xs border border-amber-500/30">
                Filtreleri Temizle
              </button>
            </div>
          ) : viewMode === 'grid' ? (
            /* --- KART IZGARA GÖRÜNÜMÜ --- */
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
              {filteredServices.map(s => (
                <div key={s.id} className="glass-panel p-4 rounded-2xl space-y-3 shadow-sm flex flex-col justify-between border border-slate-200 dark:border-brand-border/40 hover:border-amber-500/50 transition">
                  <div>
                    <OptimizedImage src={s.image} alt={`${s.name} Görseli`} className="w-full h-36 object-cover rounded-xl border border-slate-200 dark:border-brand-border" />
                    <div className="flex justify-between items-center pt-3">
                      <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{s.name}</h3>
                      <span className="font-mono font-extrabold text-xs text-amber-600 dark:text-gold-400">{formatCurrency(s.price)}</span>
                    </div>
                    {s.category && (
                      <span className="text-[10px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-full inline-block mt-1">
                        {s.category}
                      </span>
                    )}
                    <p className="text-xs text-slate-500 dark:text-gray-400 pt-2 line-clamp-2">{s.description}</p>
                  </div>

                  <div className="flex space-x-2 pt-3 border-t border-slate-200 dark:border-brand-border/40">
                    <button onClick={() => onEditClick(s)} className="flex-1 py-1.5 rounded-xl bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/30 flex items-center justify-center space-x-1 hover:bg-amber-500/20 transition">
                      <span>Düzenle</span>
                      <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                    </button>
                    <button onClick={() => onDeleteClick(s.id)} className="px-3 py-1.5 rounded-xl bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-xs uppercase border border-red-500/30 inline-flex items-center space-x-1 transition">
                      <span>SİL</span>
                      <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* --- TABLO GÖRÜNÜMÜ --- */
            <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden shadow-sm">
              <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-200 dark:border-brand-border/60 bg-slate-50/80 dark:bg-brand-dark/80 text-[11px] font-extrabold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
                      <th className="py-3.5 px-4">Görsel</th>
                      <th className="py-3.5 px-4">Hizmet Adı</th>
                      <th className="py-3.5 px-4">Kategori</th>
                      <th className="py-3.5 px-4">Paket / Ek Fiyat</th>
                      <th className="py-3.5 px-4">Açıklama</th>
                      <th className="py-3.5 px-4 text-right">Aksiyonlar</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/30 text-xs font-semibold text-slate-700 dark:text-gray-200">
                    {filteredServices.map(s => (
                      <tr key={s.id} className="hover:bg-amber-500/5 transition">
                        <td className="py-3 px-4">
                          <div className="w-12 h-10 rounded-xl overflow-hidden border border-amber-500/30 shrink-0">
                            <OptimizedImage src={s.image} alt={s.name} className="w-full h-full object-cover" />
                          </div>
                        </td>
                        <td className="py-3 px-4 font-bold text-slate-900 dark:text-gray-100">
                          {s.name}
                        </td>
                        <td className="py-3 px-4">
                          <span className="text-[10px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2.5 py-1 rounded-full">
                            {s.category || 'Genel Hizmet'}
                          </span>
                        </td>
                        <td className="py-3 px-4 font-mono font-extrabold text-amber-600 dark:text-gold-400">
                          {formatCurrency(s.price)}
                        </td>
                        <td className="py-3 px-4 max-w-xs truncate text-slate-500 dark:text-gray-400">
                          {s.description}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end space-x-1.5">
                            <button
                              onClick={() => onEditClick(s)}
                              className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-[11px] border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center space-x-1"
                              title="Hizmeti Düzenle"
                            >
                              <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                              <span>Düzenle</span>
                            </button>
                            <button
                              onClick={() => onDeleteClick(s.id)}
                              className="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-[11px] border border-red-500/30 transition flex items-center justify-center"
                              title="Hizmeti Sil"
                            >
                              <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                            </button>
                          </div>
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

    // --- UNIFIED RESERVATIONS & MASTER CALENDAR COMPONENT ---
