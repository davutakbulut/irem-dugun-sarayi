import React, { useState, useEffect, useRef, useMemo } from 'react';
import { VenueDetailModalComponent } from '../components/Modals.jsx';
import { OptimizedImage } from '../components/OptimizedImage.jsx';
import { formatCurrency } from '../utils/formatters.js';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function VenuesComponent({ venues, services = [], onAddClick, onEditClick, onDeleteClick }) {
      const [selectedVenueDetail, setSelectedVenueDetail] = useState(null);
      const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'table'
      const [searchTerm, setSearchTerm] = useState('');
      const [categoryFilter, setCategoryFilter] = useState('ALL');

      const categories = useMemo(() => {
        const set = new Set(venues.map(v => v.category).filter(Boolean));
        return ['ALL', ...Array.from(set)];
      }, [venues]);

      const filteredVenues = useMemo(() => {
        return venues.filter(v => {
          const matchesCategory = categoryFilter === 'ALL' || v.category === categoryFilter;
          const matchesSearch = !searchTerm || (
            v.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            v.description?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            v.category?.toLowerCase().includes(searchTerm.toLowerCase())
          );
          return matchesCategory && matchesSearch;
        });
      }, [venues, categoryFilter, searchTerm]);

      return (
        <div className="space-y-6">
          {/* VENUE DETAIL MODAL */}
          {selectedVenueDetail && (
            <VenueDetailModalComponent
              venue={selectedVenueDetail}
              services={services}
              onClose={() => setSelectedVenueDetail(null)}
              onSelectVenue={(v) => {
                setSelectedVenueDetail(null);
                if (onEditClick) onEditClick(v);
              }}
            />
          )}

          {/* PAGE TOP HEADER & PRIMARY ACTION */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200 dark:border-brand-border/40">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
                <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-gray-100 gold-gradient-text">
                  Etkinlik Mekanları & Balo Salonları
                </h2>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  Toplam {filteredVenues.length} konsept salon ve etkinlik mekanı listeleniyor
                </p>
              </div>
            </div>

            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center justify-center space-x-1.5 self-start sm:self-auto">
              <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 shrink-0" />
              <span>Yeni Mekan Ekle</span>
            </button>
          </div>

          {/* FILTER & VIEW MODE TOGGLE TOOLBAR */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 shadow-sm">
            
            {/* LEFT: SEARCH INPUT */}
            <div className="flex-1 relative min-w-[200px]">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4" />
              </span>
              <input
                type="text"
                placeholder="Salon adı veya açıklamasında ara..."
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

            {/* CENTER: CATEGORY FILTER */}
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

            {/* RIGHT: VIEW MODE BUTTON TOGGLE */}
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

          {/* DATA PRESENTATION: GRID MODE vs TABLE MODE */}
          {filteredVenues.length === 0 ? (
            <div className="glass-panel p-12 text-center rounded-3xl border border-dashed border-slate-300 dark:border-brand-border space-y-3">
              <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-10 h-10 mx-auto text-slate-400 opacity-60" />
              <div className="font-bold text-slate-700 dark:text-gray-300 text-sm">Aramanızla Eşleşen Düğün Salonu Bulunamadı</div>
              <p className="text-xs text-slate-500 dark:text-gray-400">Filtre kriterlerini temizleyerek veya yeni bir arama yaparak tekrar deneyebilirsiniz.</p>
              <button onClick={() => { setSearchTerm(''); setCategoryFilter('ALL'); }} className="px-4 py-2 rounded-xl bg-amber-500/10 text-amber-600 font-bold text-xs border border-amber-500/30">
                Filtreleri Temizle
              </button>
            </div>
          ) : viewMode === 'grid' ? (
            /* --- KART IZGARA GÖRÜNÜMÜ --- */
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {filteredVenues.map(v => (
                <div key={v.id} className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden space-y-3 shadow-sm flex flex-col justify-between hover:border-amber-500/50 transition group">
                  <div>
                    <div className="cursor-pointer overflow-hidden relative" onClick={() => setSelectedVenueDetail(v)}>
                      <OptimizedImage src={v.image || v.images[0]} alt={`${v.name} Görseli`} className="w-full h-48 object-cover group-hover:scale-105 transition duration-300" />
                      <span className="absolute top-3 right-3 text-[10px] text-amber-950 font-black bg-amber-400 px-2.5 py-1 rounded-full shadow-md">
                        {v.category}
                      </span>
                    </div>
                    <div className="p-4 space-y-2">
                      <h3
                        onClick={() => setSelectedVenueDetail(v)}
                        className="font-bold text-base text-slate-800 dark:text-gray-100 cursor-pointer hover:text-amber-500 transition"
                      >
                        {v.name}
                      </h3>
                      <div className="flex justify-between items-center text-xs text-slate-600 dark:text-gray-300 font-bold border-b border-slate-100 dark:border-brand-border/30 pb-2">
                        <span className="flex items-center space-x-1">
                          <ThemeIcon icon="user" fallbackEmoji="👥" className="w-3.5 h-3.5 shrink-0 text-amber-500" />
                          <span>Kapasite: {v.capacity} Kişi</span>
                        </span>
                        <span className="text-amber-600 dark:text-gold-400 font-extrabold">{formatCurrency(v.price)}</span>
                      </div>
                      <p className="text-xs text-slate-500 dark:text-gray-400 line-clamp-2">{v.description}</p>
                    </div>
                  </div>

                  <div className="p-4 pt-0 flex space-x-2">
                    <button
                      onClick={() => setSelectedVenueDetail(v)}
                      className="flex-1 py-2 rounded-xl bg-amber-500 text-slate-950 font-bold text-xs shadow hover:bg-amber-400 transition flex items-center justify-center space-x-1.5"
                    >
                      <ThemeIcon icon="preview" fallbackEmoji="👁️" className="w-3.5 h-3.5 shrink-0" />
                      <span>Detay İncele</span>
                    </button>
                    <button onClick={() => onEditClick(v)} className="py-2 px-3 rounded-xl bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/30 flex items-center justify-center space-x-1 hover:bg-amber-500/20 transition">
                      <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                      <span>Düzenle</span>
                    </button>
                    <button onClick={() => onDeleteClick(v.id)} className="px-3 py-2 rounded-xl bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-xs uppercase border border-red-500/30 inline-flex items-center space-x-1 transition">
                      <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                      <span>SİL</span>
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
                      <th className="py-3.5 px-4">Salon Görseli</th>
                      <th className="py-3.5 px-4">Salon Adı & Konsept</th>
                      <th className="py-3.5 px-4">Kapasite</th>
                      <th className="py-3.5 px-4">Başlangıç Fiyatı</th>
                      <th className="py-3.5 px-4">Açıklama</th>
                      <th className="py-3.5 px-4 text-right">Aksiyonlar</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/30 text-xs font-semibold text-slate-700 dark:text-gray-200">
                    {filteredVenues.map(v => (
                      <tr key={v.id} className="hover:bg-amber-500/5 transition">
                        <td className="py-3 px-4">
                          <div className="w-14 h-10 rounded-xl overflow-hidden cursor-pointer border border-amber-500/30 shrink-0" onClick={() => setSelectedVenueDetail(v)}>
                            <OptimizedImage src={v.image || v.images[0]} alt={v.name} className="w-full h-full object-cover hover:scale-110 transition" />
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <div className="font-bold text-slate-900 dark:text-gray-100 cursor-pointer hover:text-amber-500 transition" onClick={() => setSelectedVenueDetail(v)}>
                            {v.name}
                          </div>
                          <span className="text-[10px] font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-2 py-0.5 rounded-full inline-block mt-0.5">
                            {v.category}
                          </span>
                        </td>
                        <td className="py-3 px-4 font-mono font-bold text-slate-800 dark:text-gray-200 flex items-center space-x-1">
                          <ThemeIcon icon="user" fallbackEmoji="👥" className="w-3.5 h-3.5 shrink-0 text-amber-500" />
                          <span>{v.capacity} Kişi</span>
                        </td>
                        <td className="py-3 px-4 font-mono font-extrabold text-amber-600 dark:text-gold-400">
                          {formatCurrency(v.price)}
                        </td>
                        <td className="py-3 px-4 max-w-xs truncate text-slate-500 dark:text-gray-400">
                          {v.description}
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end space-x-1.5">
                            <button
                              onClick={() => setSelectedVenueDetail(v)}
                              className="px-2.5 py-1 rounded-lg bg-amber-500 text-slate-950 font-bold text-[11px] shadow hover:bg-amber-400 transition flex items-center space-x-1"
                              title="Salon Detayını İncele"
                            >
                              <ThemeIcon icon="preview" fallbackEmoji="👁️" className="w-3 h-3 shrink-0" />
                              <span>Detay</span>
                            </button>
                            <button
                              onClick={() => onEditClick(v)}
                              className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-[11px] border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center space-x-1"
                              title="Salonu Düzenle"
                            >
                              <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                              <span>Düzenle</span>
                            </button>
                            <button
                              onClick={() => onDeleteClick(v.id)}
                              className="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-[11px] border border-red-500/30 transition flex items-center justify-center"
                              title="Salonu Sil"
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

    // --- SERVICES COMPONENT ---
