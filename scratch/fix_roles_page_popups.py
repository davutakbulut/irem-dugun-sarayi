import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_roles_component = """    function RolesPageComponent({ activeRole, roles, users = [], tabPermissions, onAddRole, onEditRole, onDeleteRole, onToggleTabPermission, showToast, navigateTo }) {
      const [newRoleId, setNewRoleId] = useState('');
      const [newRoleName, setNewRoleName] = useState('');
      const [editingRole, setEditingRole] = useState(null); // { id, name }
      const [searchQuery, setSearchQuery] = useState('');"""

new_roles_component = """    function RolesPageComponent({ activeRole, roles, users = [], tabPermissions, onAddRole, onEditRole, onDeleteRole, onToggleTabPermission, showToast, navigateTo }) {
      const [newRoleId, setNewRoleId] = useState('');
      const [newRoleName, setNewRoleName] = useState('');
      const [editingRole, setEditingRole] = useState(null); // { id, name }
      const [deletingRole, setDeletingRole] = useState(null); // { id, name }
      const [searchQuery, setSearchQuery] = useState('');"""

old_delete_btn = """                      {isSystemAdmin ? (
                        <span className="text-[10px] text-slate-400 font-bold italic px-2 py-1">Korunan Admin</span>
                      ) : (
                        <button
                          type="button"
                          onClick={() => {
                            if (confirm(`"${roles[roleId]}" (${roleId}) rolünü ve tüm yetkilerini sistemden silmek istediğinize emin misiniz?`)) {
                              onDeleteRole(roleId);
                            }
                          }}
                          className="px-2.5 py-1 bg-red-500/10 text-red-600 dark:text-red-400 hover:bg-red-500 hover:text-white rounded-lg font-bold transition flex items-center space-x-1"
                        >
                          <ThemeIcon icon="trash" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Sil</span>
                        </button>
                      )}"""

new_delete_btn = """                      {isSystemAdmin ? (
                        <span className="text-[10px] text-slate-400 font-bold italic px-2 py-1">Korunan Admin</span>
                      ) : (
                        <button
                          type="button"
                          onClick={() => setDeletingRole({ id: roleId, name: roles[roleId] })}
                          className="px-2.5 py-1 bg-red-500/10 text-red-600 dark:text-red-400 hover:bg-red-500 hover:text-white rounded-lg font-bold transition flex items-center space-x-1 cursor-pointer"
                        >
                          <ThemeIcon icon="trash" fallbackEmoji="" className="w-3.5 h-3.5 inline-block mr-1" /><span>Sil</span>
                        </button>
                      )}"""

old_edit_modal = """          {/* EDIT ROLE MODAL */}
          {editingRole && (
            <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl">
                <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
                  <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                    <ThemeIcon icon="edit" fallbackEmoji="" className="w-4 h-4 text-amber-500 inline-block mr-1.5" /><span>Rol Unvanını Güncelle ({editingRole.id})</span>
                  </h3>
                  <button onClick={() => setEditingRole(null)} className="text-slate-400 hover:text-white">✕</button>
                </div>

                <div className="space-y-3 text-xs">
                  <div>
                    <label className="font-bold block mb-1">Yeni Rol Unvanı:</label>
                    <input
                      type="text"
                      value={editingRole.name}
                      onChange={e => setEditingRole({ ...editingRole, name: e.target.value })}
                      className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold"
                      required
                    />
                  </div>

                  <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
                    <button type="button" onClick={() => setEditingRole(null)} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold">İptal</button>
                    <button type="button" onClick={handleSaveEditedRole} className="gold-button font-bold px-5 py-2 rounded-xl">Değişiklikleri Kaydet ✓</button>
                  </div>
                </div>
              </div>
            </div>
          )}"""

new_edit_modal = """          {/* EDIT ROLE MODAL */}
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
          />"""

if old_roles_component in html and old_delete_btn in html and old_edit_modal in html:
    html = html.replace(old_roles_component, new_roles_component)
    html = html.replace(old_delete_btn, new_delete_btn)
    html = html.replace(old_edit_modal, new_edit_modal)
    print("Updated RolesPageComponent popups to strict system rules successfully!")
else:
    print("Could not match all snippets in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html RolesPageComponent popups fix successfully!")
