import React, { useState, useEffect, useRef, useMemo } from 'react';
import { RedAlertConfirmModal } from '../components/Modals.jsx';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function RolesPageComponent({ activeRole, roles, users = [], tabPermissions, onAddRole, onEditRole, onDeleteRole, onToggleTabPermission, showToast, navigateTo }) {
      const [newRoleId, setNewRoleId] = useState('');
      const [newRoleName, setNewRoleName] = useState('');
      const [editingRole, setEditingRole] = useState(null); // { id, name }
      const [deletingRole, setDeletingRole] = useState(null); // { id, name }
      const [searchQuery, setSearchQuery] = useState('');

      const filteredRoles = useMemo(() => {
        if (!searchQuery.trim()) return Object.keys(roles);
        const q = searchQuery.toLowerCase();
        return Object.keys(roles).filter(rId => 
          rId.toLowerCase().includes(q) || (roles[rId] || '').toLowerCase().includes(q)
        );
      }, [roles, searchQuery]);

      const handleCreateRoleSubmit = (e) => {
        e.preventDefault();
        const cleanId = newRoleId.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!cleanId || !newRoleName.trim()) {
          showToast('⚠️ Lütfen rol kodu ve rol adını eksiksiz giriniz!');
          return;
        }
        if (roles[cleanId]) {
          showToast(`⚠️ "${cleanId}" kodlu bir rol zaten mevcut! Lütfen farklı bir rol kodu belirleyin.`);
          return;
        }
        onAddRole(cleanId, newRoleName);
        setNewRoleId('');
        setNewRoleName('');
      };

      const handleSaveEditedRole = () => {
        if (!editingRole || !editingRole.name.trim()) return;
        onEditRole(editingRole.id, editingRole.name.trim());
        setEditingRole(null);
      };

      return (
        <div className="w-full space-y-6 animate-fade-in pb-16">
          {/* HEADER BANNER */}
          <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 shadow-sm">
            <div>
              <div className="flex items-center space-x-2">
                <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-6 h-6 text-amber-500 shrink-0" />
                <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text">
                  Sistem Rol Yönetimi & Sayfa İzin Matrisi
                </h2>
                <span className="text-[10px] font-black px-2.5 py-0.5 rounded-full bg-amber-500 text-white shrink-0">
                  SADECE ADMİN
                </span>
              </div>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1 font-medium">
                Yeni rol ekleyin, mevcut rolleri düzenleyin/silin ve sayfa bazlı erişim yetkilerini tek ekrandan canlı yönetin.
              </p>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                type="button"
                onClick={() => navigateTo('users')}
                className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-200 dark:hover:bg-brand-border transition flex items-center space-x-1.5"
              >
                <ThemeIcon icon="user" fallbackEmoji="👥" className="w-4 h-4 shrink-0" />
                <span>Kullanıcı Yönetimi →</span>
              </button>
            </div>
          </div>

          {/* SECTION 1: CREATE NEW ROLE FORM */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/20 shadow-sm">
            <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
              <ThemeIcon icon="plus" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Yeni Sistem Rolü Tanımla</span>
            </h3>

            <form onSubmit={handleCreateRoleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Rol Kodu (Sistem Kodu):</label>
                <input
                  type="text"
                  placeholder="Örn: muhasebe, vale, mudur"
                  value={newRoleId}
                  onChange={e => setNewRoleId(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold text-amber-700"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Rol Görünen Adı:</label>
                <input
                  type="text"
                  placeholder="Örn: Muhasebe Sorumlusu 📊"
                  value={newRoleName}
                  onChange={e => setNewRoleName(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                  required
                />
              </div>

              <div className="flex items-end">
                <button type="submit" className="w-full gold-button font-bold py-2.5 rounded-xl text-xs shadow hover:scale-[1.02] transition flex items-center justify-center space-x-1">
                  <span>Sisteme Yeni Rolü Ekle</span>
                </button>
              </div>
            </form>
          </div>

          {/* SECTION 2: ROLES LIST & MANAGEMENT CARDS */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40 shadow-sm">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 border-b pb-3 border-slate-200 dark:border-brand-border/40">
              <div>
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                  <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-5 h-5 text-amber-500 shrink-0" />
                  <span>Aktif Sistem Roller ({Object.keys(roles).length})</span>
                </h3>
              </div>

              <input
                type="text"
                placeholder="Rollerde ara..."
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-1.5 text-xs font-bold w-full sm:w-64"
              />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {filteredRoles.map(roleId => {
                const assignedUsersCount = (users || []).filter(u => u.role === roleId).length;
                const isSystemAdmin = roleId === 'admin';

                return (
                  <div key={roleId} className="bg-slate-50/80 dark:bg-brand-dark/60 p-4 rounded-2xl border border-slate-200 dark:border-brand-border/60 space-y-3 relative hover:border-amber-500/50 transition">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-bold text-sm text-slate-900 dark:text-gray-100 flex items-center space-x-1">
                          <span>{roles[roleId]}</span>
                        </div>
                        <div className="text-[10px] font-mono text-amber-700 dark:text-gold-400 font-bold mt-0.5">
                          ID: {roleId}
                        </div>
                      </div>
                      <span className={`text-[10px] font-black px-2 py-0.5 rounded-full ${isSystemAdmin ? 'bg-red-500 text-white' : 'bg-amber-500/20 text-amber-700 dark:text-gold-400'}`}>
                        {assignedUsersCount} Kullanıcı
                      </span>
                    </div>

                    <div className="pt-2 border-t border-slate-200 dark:border-brand-border/40 flex items-center justify-between gap-2 text-xs">
                      <button
                        type="button"
                        onClick={() => setEditingRole({ id: roleId, name: roles[roleId] })}
                        className="px-2.5 py-1 bg-blue-500/10 text-blue-600 dark:text-blue-400 hover:bg-blue-500 hover:text-white rounded-lg font-bold transition flex items-center space-x-1"
                      >
                        <ThemeIcon icon="edit" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Düzenle</span>
                      </button>

                      {isSystemAdmin ? (
                        <span className="text-[10px] text-slate-400 font-bold italic px-2 py-1">Korunan Admin</span>
                      ) : (
                        <button
                          type="button"
                          onClick={() => setDeletingRole({ id: roleId, name: roles[roleId] })}
                          className="px-2.5 py-1 bg-red-500/10 text-red-600 dark:text-red-400 hover:bg-red-500 hover:text-white rounded-lg font-bold transition flex items-center space-x-1 cursor-pointer"
                        >
                          <ThemeIcon icon="trash" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Sil</span>
                        </button>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* EDIT ROLE MODAL */}
          {editingRole && (
            <div className="fixed inset-0 z-50 bg-slate-950/75 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in" onClick={() => setEditingRole(null)}>
              <div className="glass-panel bg-white/95 dark:bg-brand-card/95 border-2 border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl relative overflow-hidden" onClick={e => e.stopPropagation()}>
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border/60">
                  <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-5 h-5 text-amber-500 shrink-0" />
                    <span>Rol Unvanını Güncelle</span>
                  </h3>
                  <button
                    onClick={() => setEditingRole(null)}
                    className="w-8 h-8 rounded-full bg-slate-100 dark:bg-brand-dark flex items-center justify-center text-slate-500 hover:text-amber-500 transition font-bold"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-4 text-xs">
                  <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-700 dark:text-gold-400 font-mono font-bold">
                    Sistem Rol Kodu (Değiştirilemez): <span className="underline">{editingRole.id}</span>
                  </div>

                  <div>
                    <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1.5">
                      Yeni Rol Görünen Adı / Unvanı:
                    </label>
                    <input
                      type="text"
                      value={editingRole.name}
                      onChange={e => setEditingRole({ ...editingRole, name: e.target.value })}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-3 font-bold text-slate-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-amber-500"
                      required
                      autoFocus
                    />
                  </div>

                  <div className="flex justify-end space-x-2 pt-3 border-t border-slate-200 dark:border-brand-border/60">
                    <button
                      type="button"
                      onClick={() => setEditingRole(null)}
                      className="px-4 py-2.5 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold hover:bg-slate-200 transition cursor-pointer"
                    >
                      İptal
                    </button>
                    <button
                      type="button"
                      onClick={handleSaveEditedRole}
                      className="gold-button font-extrabold px-5 py-2.5 rounded-xl shadow-md hover:scale-105 transition cursor-pointer"
                    >
                      Değişiklikleri Kaydet ✓
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* RED ALERT CONFIRMATION MODAL FOR DELETING ROLE */}
          <RedAlertConfirmModal
            isOpen={!!deletingRole}
            title="Sistem Rolü Silme Onayı 🚨"
            message={deletingRole ? `"${deletingRole.name}" (${deletingRole.id}) rolünü ve bağlı tüm erişim yetkilerini sistemden tamamen silmek istediğinize emin misiniz? Bu işlem geri alınamaz!` : ''}
            confirmText="Evet, Rolü Sil"
            cancelText="Vazgeç"
            onConfirm={() => {
              if (deletingRole) {
                onDeleteRole(deletingRole.id);
                if (showToast) showToast(`🗑️ "${deletingRole.name}" rolü sistemden silindi.`);
                setDeletingRole(null);
              }
            }}
            onClose={() => setDeletingRole(null)}
          />

          {/* SECTION 3: PERMISSIONS MATRIX TABLE */}
          <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border/40 shadow-sm overflow-x-auto">
            <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border/40">
              <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                <ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-5 h-5 text-amber-500 shrink-0" />
                <span>Sayfa Bazlı Rol İzin Matrisi (Live RBAC Matrix)</span>
              </h3>
              <span className="text-[10px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/30">
                Canlı Kaydedilir
              </span>
            </div>

            <table className="w-full text-left border-collapse text-xs">
              <thead>
                <tr className="border-b border-slate-200 dark:border-brand-border/40 bg-slate-50 dark:bg-brand-dark text-slate-700 dark:text-gray-300">
                  <th className="p-3 font-extrabold rounded-l-xl">Sistem Paneli / Sayfa Modülü</th>
                  {Object.keys(roles).map(roleId => (
                    <th key={roleId} className="p-3 font-extrabold text-center whitespace-nowrap border-l border-slate-200 dark:border-brand-border/40">
                      <div className="flex flex-col items-center space-y-0.5">
                        <span className="text-xs">{roles[roleId]}</span>
                        <span className="text-[9px] font-mono text-slate-400">({roleId})</span>
                      </div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.keys(TAB_LABELS).map(tabId => (
                  <tr key={tabId} className="border-b border-slate-100 dark:border-brand-border/30 hover:bg-slate-500/5 transition">
                    <td className="p-3 font-bold text-slate-800 dark:text-gray-200">
                      {TAB_LABELS[tabId]}
                    </td>
                    {Object.keys(roles).map(roleId => {
                      const isAllowed = (tabPermissions[tabId] || []).includes(roleId);
                      return (
                        <td key={roleId} className="p-3 text-center border-l border-slate-100 dark:border-brand-border/20">
                          <input
                            type="checkbox"
                            checked={isAllowed}
                            onChange={() => onToggleTabPermission(tabId, roleId)}
                            className="w-4 h-4 accent-amber-600 rounded cursor-pointer"
                          />
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      );
    }
