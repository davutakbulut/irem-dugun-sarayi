import React from 'react';
import { ThemeIcon } from '../components/ThemeIcon';

    export export function UsersPage({ users, onAddClick, onEditClick, onDeleteClick }) {
      return (
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-white flex items-center space-x-2">
              <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-6 h-6 text-amber-500 shrink-0" />
              <span>Kullanıcı Yönetimi</span>
            </h2>
            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center space-x-1">
              <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 shrink-0" />
              <span>Yeni Kullanıcı Tanımla</span>
            </button>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {users.map(u => (
              <div key={u.id} className="glass-panel p-5 rounded-2xl text-center space-y-3 shadow-sm flex flex-col justify-between">
                <div>
                  <img src={u.avatar} alt={`${u.name} Profil Resmi`} className="w-16 h-16 rounded-full mx-auto object-cover border-2 border-amber-500/50" />
                  <div className="mt-2">
                    <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{u.name}</h3>
                    <div className="text-xs text-slate-500 dark:text-gray-400 truncate">{u.email}</div>
                  </div>
                  <span className="bg-amber-500/10 text-amber-800 dark:text-gold-400 text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase border border-amber-500/20 inline-block mt-2">{u.role}</span>
                </div>

                <div className="flex space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border/40">
                  <button onClick={() => onEditClick(u)} className="flex-1 py-1.5 rounded-xl bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-xs border border-amber-500/30 flex items-center justify-center space-x-1">
                    <span>Düzenle</span>
                    <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                  </button>
                  <button onClick={() => onDeleteClick(u.id)} className="px-3 py-1.5 rounded-xl bg-red-500/10 text-red-600 font-bold text-xs border border-red-500/20 flex items-center space-x-1">
                    <span>Sil</span>
                    <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      );
    }


    // --- MEDIA COMPONENT ---