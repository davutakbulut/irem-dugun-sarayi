import React, { useState } from 'react';
import { UserModalComponent } from '../components/Modals';

export function UsersPage({ users = [], onAddUser, onEditUser }) {
  const [editingUser, setEditingUser] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className="space-y-6 max-w-7xl mx-auto animate-fade-in">
      {/* MODAL */}
      {isModalOpen && (
        <UserModalComponent
          user={editingUser}
          onClose={() => { setIsModalOpen(false); setEditingUser(null); }}
          onSave={(uObj) => {
            if (editingUser) {
              onEditUser(uObj);
            } else {
              onAddUser(uObj);
            }
            setIsModalOpen(false);
            setEditingUser(null);
          }}
        />
      )}

      {/* HEADER */}
      <div className="glass-panel p-6 rounded-3xl border border-slate-200 dark:border-brand-border flex justify-between items-center shadow-sm">
        <div>
          <h2 className="text-xl sm:text-2xl font-heading font-extrabold text-slate-900 dark:text-white">
            🛡️ Yetkili Personel Listesi (RBAC Rol Yönetimi)
          </h2>
          <p className="text-xs text-slate-500 dark:text-gray-400">
            Sistem kullanıcılarını, SuperAdmin, Manager ve Staff yetkilerini düzenleyin.
          </p>
        </div>

        <button
          onClick={() => { setEditingUser(null); setIsModalOpen(true); }}
          className="gold-button font-bold text-xs px-4 py-2.5 rounded-xl shadow flex items-center space-x-1"
        >
          <span>➕ Personel Ekle</span>
        </button>
      </div>

      {/* USERS LIST GRID */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {users.map(u => (
          <div key={u.id} className="glass-panel p-5 rounded-3xl border border-slate-200 dark:border-brand-border space-y-3 shadow-sm flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <img src={u.avatar} alt={u.name} className="w-12 h-12 rounded-2xl object-cover border-2 border-amber-500/40 shadow-sm" />
              <div>
                <h4 className="font-heading font-extrabold text-sm text-slate-900 dark:text-white">{u.name}</h4>
                <div className="text-xs text-slate-500">{u.title}</div>
                <div className="text-[10px] text-amber-600 font-bold mt-0.5">{u.role}</div>
              </div>
            </div>

            <button
              onClick={() => { setEditingUser(u); setIsModalOpen(true); }}
              className="text-xs font-bold text-slate-600 dark:text-gray-300 hover:underline"
            >
              Düzenle ✏️
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
