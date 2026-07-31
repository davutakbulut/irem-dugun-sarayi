import React, { useState, useMemo } from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

function WhatsAppButton({ phone, customerName }) {
  if (!phone) return null;
  const cleanPhone = phone.replace(/[^0-9]/g, '');
  const message = encodeURIComponent(`Merhaba Sayın ${customerName}, İrem Düğün Sarayı rezervasyonunuz ile ilgili sizinle iletişime geçiyoruz.`);
  const whatsappUrl = `https://wa.me/${cleanPhone.startsWith('90') ? cleanPhone : '90' + cleanPhone}?text=${message}`;

  return (
    <a
      href={whatsappUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center space-x-1.5 px-2.5 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-[11px] shadow transition"
    >
      <span>💬 WhatsApp</span>
    </a>
  );
}

export function CustomersPage({ customers = [], onAddClick, onEditClick, onDeleteClick }) {
  const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'table'
  const [searchTerm, setSearchTerm] = useState('');
  const [taxTypeFilter, setTaxTypeFilter] = useState('ALL'); // 'ALL' | 'individual' | 'corporate'

  const filteredCustomers = useMemo(() => {
    return customers.filter(c => {
      const matchesTaxType = taxTypeFilter === 'ALL' || c.taxType === taxTypeFilter;
      const matchesSearch = !searchTerm || (
        c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.phone?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.tcNo?.includes(searchTerm) ||
        c.vknNo?.includes(searchTerm)
      );
      return matchesTaxType && matchesSearch;
    });
  }, [customers, taxTypeFilter, searchTerm]);

  return (
    <div className="space-y-6">
      {/* HEADER & PRIMARY ACTION */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200 dark:border-brand-border/40">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
            <ThemeIcon icon="user" fallbackEmoji="👥" className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-gray-100 gold-gradient-text">
              Müşteri Rehberi
            </h2>
            <p className="text-xs text-slate-500 dark:text-gray-400">
              Toplam {filteredCustomers.length} kayıtlı müşteri rehberde listeleniyor
            </p>
          </div>
        </div>

        <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center justify-center space-x-1.5 self-start sm:self-auto">
          <ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 shrink-0" />
          <span>Yeni Müşteri Ekle</span>
        </button>
      </div>

      {/* FILTER TOOLBAR & VIEW MODE SWITCHER */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 shadow-sm">
        <div className="flex-1 relative min-w-[200px]">
          <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
            <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4" />
          </span>
          <input
            type="text"
            placeholder="Müşteri adı, telefon, e-posta veya TC/VKN no ara..."
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

        <div className="flex items-center space-x-2">
          <span className="text-xs font-bold text-slate-500 dark:text-gray-400 shrink-0">Müşteri Türü:</span>
          <select
            value={taxTypeFilter}
            onChange={e => setTaxTypeFilter(e.target.value)}
            className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-2 text-xs font-bold text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500"
          >
            <option value="ALL">Tümü (Bireysel & Kurumsal)</option>
            <option value="individual">Bireysel Müşteriler</option>
            <option value="corporate">Kurumsal Müşteriler</option>
          </select>
        </div>

        <div className="flex items-center p-1 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border shrink-0 self-end md:self-auto">
          <button
            onClick={() => setViewMode('grid')}
            className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
              viewMode === 'grid'
                ? 'bg-amber-500 text-slate-950 shadow-sm'
                : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-gray-100'
            }`}
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
          >
            <ThemeIcon icon="list" fallbackEmoji="📋" className="w-4 h-4 shrink-0" />
            <span>Tablo Görünümü</span>
          </button>
        </div>
      </div>

      {/* CONTENT */}
      {filteredCustomers.length === 0 ? (
        <div className="glass-panel p-12 text-center rounded-3xl border border-dashed border-slate-300 dark:border-brand-border space-y-3">
          <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-10 h-10 mx-auto text-slate-400 opacity-60" />
          <div className="font-bold text-slate-700 dark:text-gray-300 text-sm">Aramanızla Eşleşen Müşteri Bulunamadı</div>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredCustomers.map(c => (
            <div key={c.id} className="glass-panel p-5 rounded-2xl flex items-start space-x-4 shadow-sm border border-slate-200 dark:border-brand-border/40 hover:border-amber-500/50 transition">
              <img src={c.avatar} alt={`${c.name} Avatarı`} className="w-14 h-14 rounded-2xl object-cover border border-amber-500/40 shrink-0" />
              <div className="flex-1 space-y-2">
                <div className="flex justify-between items-start">
                  <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{c.name}</h3>
                  <div className="flex space-x-1.5 items-center">
                    <button onClick={() => onEditClick(c)} className="text-[11px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-500/30 flex items-center space-x-1 hover:bg-amber-500/20 transition">
                      <span>Düzenle</span>
                      <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                    </button>
                    <button onClick={() => onDeleteClick(c.id)} className="px-2.5 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-xs uppercase border border-red-500/30 inline-flex items-center space-x-1.5 transition shadow-2xs">
                      <span>SİL</span>
                      <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                    </button>
                  </div>
                </div>
                <div className="text-xs text-slate-500 dark:text-gray-400">{c.phone} | {c.email}</div>
                <div className="text-[11px] text-slate-600 dark:text-gray-400">
                  <span className="font-bold text-amber-600 dark:text-gold-400 inline-flex items-center space-x-1">
                    {c.taxType === 'corporate' ? (
                      <>
                        <ThemeIcon icon="briefcase" fallbackEmoji="🏢" className="w-3.5 h-3.5 shrink-0" />
                        <span>Kurumsal</span>
                      </>
                    ) : (
                      <>
                        <ThemeIcon icon="user" fallbackEmoji="👤" className="w-3.5 h-3.5 shrink-0" />
                        <span>Bireysel</span>
                      </>
                    )}
                  </span>
                  <span> - </span>
                  <span>{c.taxType === 'corporate' ? `VKN: ${c.vknNo || c.tcNo || '-'}` : `TC: ${c.tcNo || '-'}`} ({c.taxOffice || 'Sapanca VD'})</span>
                </div>
                <div className="pt-1">
                  <WhatsAppButton phone={c.phone} customerName={c.name} />
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden shadow-sm">
          <div className="overflow-x-auto custom-scrollbar">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 dark:border-brand-border/60 bg-slate-50/80 dark:bg-brand-dark/80 text-[11px] font-extrabold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
                  <th className="py-3.5 px-4">Müşteri</th>
                  <th className="py-3.5 px-4">İletişim Bilgileri</th>
                  <th className="py-3.5 px-4">Müşteri Türü & Kimlik / Vergi No</th>
                  <th className="py-3.5 px-4">Vergi Dairesi & Adres</th>
                  <th className="py-3.5 px-4 text-right">Aksiyonlar</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 dark:divide-brand-border/30 text-xs font-semibold text-slate-700 dark:text-gray-200">
                {filteredCustomers.map(c => (
                  <tr key={c.id} className="hover:bg-amber-500/5 transition">
                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-3">
                        <img src={c.avatar} alt={c.name} className="w-9 h-9 rounded-xl object-cover border border-amber-500/30 shrink-0" />
                        <div>
                          <div className="font-bold text-slate-900 dark:text-gray-100">{c.name}</div>
                          <div className="text-[10px] text-slate-400">ID: #{c.id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-mono text-slate-800 dark:text-gray-200 font-bold">{c.phone}</div>
                      <div className="text-[11px] text-slate-500 dark:text-gray-400">{c.email}</div>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full inline-flex items-center space-x-1 ${
                        c.taxType === 'corporate'
                          ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20'
                          : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
                      }`}>
                        {c.taxType === 'corporate' ? (
                          <>
                            <ThemeIcon icon="briefcase" fallbackEmoji="🏢" className="w-3 h-3 shrink-0" />
                            <span>Kurumsal</span>
                          </>
                        ) : (
                          <>
                            <ThemeIcon icon="user" fallbackEmoji="👤" className="w-3 h-3 shrink-0" />
                            <span>Bireysel</span>
                          </>
                        )}
                      </span>
                      <div className="text-[11px] font-mono text-slate-600 dark:text-gray-300 mt-1">
                        {c.taxType === 'corporate' ? `VKN: ${c.vknNo || '-'}` : `TC: ${c.tcNo || '-'}`}
                      </div>
                    </td>
                    <td className="py-3 px-4 text-slate-500 dark:text-gray-400">
                      <div>{c.taxOffice || 'Sapanca VD'}</div>
                      <div className="text-[10px] truncate max-w-xs">{c.address || 'Sakarya / Sapanca'}</div>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end space-x-1.5">
                        <WhatsAppButton phone={c.phone} customerName={c.name} />
                        <button
                          onClick={() => onEditClick(c)}
                          className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-[11px] border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center space-x-1"
                        >
                          <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                        </button>
                        <button
                          onClick={() => onDeleteClick(c.id)}
                          className="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-[11px] border border-red-500/30 transition flex items-center justify-center"
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

    // --- USERS COMPONENT ---