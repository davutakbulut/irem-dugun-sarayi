import React from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

    export export function CustomersPage({ customers, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ThemeIcon icon="user" fallbackEmoji="👥" className="w-6 h-6 text-amber-500 shrink-0" />
              <span>Müşteri Rehberi</span>
            </h2>
            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2 rounded-xl text-xs flex items-center space-x-1">
              <ThemeIcon icon="user" fallbackEmoji="👤" className="w-3.5 h-3.5 shrink-0" />
              <span>Yeni Müşteri Ekle</span>
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {customers.map(c => (
              <div key={c.id} className="glass-panel p-5 rounded-2xl flex items-start space-x-4 shadow-sm">
                <img src={c.avatar} alt={`${c.name} Avatarı`} className="w-14 h-14 rounded-2xl object-cover border border-amber-500/40" />
                <div className="flex-1 space-y-2">
                  <div className="flex justify-between items-start">
                    <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{c.name}</h3>
                    <div className="flex space-x-1.5 items-center">
                      <button onClick={() => onEditClick(c)} className="text-[11px] text-amber-700 font-bold bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-500/30 flex items-center space-x-1">
                        <span>Düzenle</span>
                        <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                      </button>
                      <button onClick={() => onDeleteClick(c.id)} className="px-2.5 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 font-extrabold text-xs uppercase tracking-wider border border-red-500/30 inline-flex items-center space-x-1.5 transition shadow-2xs group">
                        <span className="group-hover:text-white transition">SİL</span>
                        <ThemeIcon icon="delete" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0 text-red-600 dark:text-red-400 group-hover:text-white transition" />
                      </button>
                    </div>
                  </div>
                  <div className="text-xs text-slate-500 dark:text-gray-400">{c.phone} | {c.email}</div>
                  <div className="text-[11px] text-slate-600 dark:text-gray-400">{c.taxType === 'corporate' ? `Kurumsal VKN: ${c.vknNo || c.tcNo || '-'}` : `Bireysel TC: ${c.tcNo || '-'}`} ({c.taxOffice || 'Sapanca VD'})</div>
                  <div className="pt-1">
                    <WhatsAppButton phone={c.phone} customerName={c.name} />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }

    // --- USERS COMPONENT ---