import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------
# FIX 1 & 2 & 5: CreateReservationPageComponent
# ---------------------------------------------------------

# Add todayDateStr helper inside CreateReservationPageComponent
old_create_res_header = "function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations = [], draftReservations = [], setDraftReservations, currentUser, prefilledDate, onSaveReservation, onCancel, showToast, navigateTo }) {"
new_create_res_header = """function CreateReservationPageComponent({ venues, services, customers, campaigns, reservations = [], draftReservations = [], setDraftReservations, currentUser, prefilledDate, onSaveReservation, onCancel, showToast, navigateTo }) {
      const todayDateStr = useMemo(() => {
        const now = new Date();
        const y = now.getFullYear();
        const m = String(now.getMonth() + 1).padStart(2, '0');
        const d = String(now.getDate()).padStart(2, '0');
        return `${y}-${m}-${d}`;
      }, []);"""

if old_create_res_header in html:
    html = html.replace(old_create_res_header, new_create_res_header)
    print("Fix 1/2/5: Added todayDateStr to CreateReservationPageComponent")

# Sanitize guestCount and monetary calculations inside CreateReservationPageComponent
# Fix calculation of sub, disc, grandTotal, remaining
old_calc_block = """        const sub = vPrice + servTotal;
        let disc = 0;"""
new_calc_block = """        const vPriceClean = Math.max(0, vPrice);
        const servTotalClean = Math.max(0, servTotal);
        const sub = vPriceClean + servTotalClean;
        let disc = 0;"""

if old_calc_block in html:
    html = html.replace(old_calc_block, new_calc_block)
    print("Fix 2: Sanitized subtotal vPrice & servTotal calculation")

old_disc_calc = """        const afterDisc = Math.max(0, sub - disc);"""
new_disc_calc = """        disc = Math.max(0, Math.min(sub, disc));
        const afterDisc = Math.max(0, sub - disc);"""

if old_disc_calc in html:
    html = html.replace(old_disc_calc, new_disc_calc)
    print("Fix 2: Ensured discount cannot exceed subtotal or be negative")

# Add past date check in handleSubmit of CreateReservationPageComponent
old_handle_submit_start = "const handleSubmit = () => {"
new_handle_submit_start = """const handleSubmit = () => {
        // Prevent Past Date Reservation
        if (startDate && startDate < todayDateStr) {
          showAlertModal('⚠️ GEÇMİŞ TARİH SEÇİLDİ', `Geçmiş bir tarihe (${startDate}) rezervasyon oluşturulamaz! Lütfen bugün (${todayDateStr}) veya gelecekte bir tarih seçiniz.`, 'start-date-input');
          return;
        }

        // Prevent Negative or Zero Guest Count
        if (Number(guestCount) < 1) {
          showAlertModal('⚠️ KATILIMCI SIKINTISI', 'Kişi sayısı en az 1 olmalıdır! Negatif veya sıfır kişi sayısı girilemez.', 'guest-count-input');
          return;
        }

        // Prevent Negative Deposit
        if (Number(depositPaid) < 0) {
          showAlertModal('⚠️ GEÇERSİZ KAPORA', 'Kapora miktarı negatif olamaz! Lütfen 0 veya pozitif bir tutar giriniz.', 'deposit-paid-input');
          return;
        }"""

if old_handle_submit_start in html:
    html = html.replace(old_handle_submit_start, new_handle_submit_start, 1)
    print("Fix 1 & 2 & 5: Added validations to handleSubmit")

# Update date picker input min attribute to todayDateStr
html = html.replace(
    'type="date" value={startDate} onChange={e => setStartDate(e.target.value)}',
    'type="date" min={todayDateStr} value={startDate} id="start-date-input" onChange={e => setStartDate(e.target.value)}'
)
html = html.replace(
    'type="date" value={endDate} onChange={e => setEndDate(e.target.value)}',
    'type="date" min={startDate || todayDateStr} onChange={e => setEndDate(e.target.value)}'
)

# Update guestCount input to enforce min 1 and sanitize onChange
html = html.replace(
    'type="number" value={guestCount} onChange={e => setGuestCount(Number(e.target.value))}',
    'type="number" min="1" id="guest-count-input" value={guestCount} onChange={e => setGuestCount(Math.max(1, parseInt(e.target.value) || 1))}'
)

# Update depositPaid input to enforce min 0 and sanitize onChange
html = html.replace(
    'type="number" value={depositPaid} onChange={e => setDepositPaid(Number(e.target.value))}',
    'type="number" min="0" id="deposit-paid-input" value={depositPaid} onChange={e => setDepositPaid(Math.max(0, parseFloat(e.target.value) || 0))}'
)


# ---------------------------------------------------------
# FIX 3: CampaignModalComponent (Prevent Duplicate Campaign Codes)
# ---------------------------------------------------------
old_campaign_modal = """function CampaignModalComponent({ campaign, onClose, onSave }) {
      const [code, setCode] = useState(campaign?.code || '');
      const [title, setTitle] = useState(campaign?.title || '');
      const [type, setType] = useState(campaign?.type || 'percent');
      const [value, setValue] = useState(campaign?.value || 15);
      const [description, setDescription] = useState(campaign?.description || '');

      const handleSubmit = (e) => {
        e.preventDefault();
        onSave({
          id: campaign?.id || `c-${Date.now()}`,
          code: code.toUpperCase(),
          title,
          type,
          value: Number(value),
          description
        });
      };"""

new_campaign_modal = """function CampaignModalComponent({ campaign, onClose, onSave, campaigns = [] }) {
      const [code, setCode] = useState(campaign?.code || '');
      const [title, setTitle] = useState(campaign?.title || '');
      const [type, setType] = useState(campaign?.type || 'percent');
      const [value, setValue] = useState(campaign?.value || 15);
      const [description, setDescription] = useState(campaign?.description || '');
      const [codeError, setCodeError] = useState('');

      const handleSubmit = (e) => {
        e.preventDefault();
        const cleanCode = code.trim().toUpperCase();
        if (!cleanCode) {
          setCodeError('Kampanya indirim kodu boş olamaz!');
          return;
        }
        const isDuplicate = (campaigns || []).some(c => c.id !== campaign?.id && (c.code || '').trim().toUpperCase() === cleanCode);
        if (isDuplicate) {
          setCodeError(`" ${cleanCode} " kodlu bir kampanya zaten mevcut! Lütfen benzersiz bir kupon kodu yazınız.`);
          return;
        }
        setCodeError('');
        onSave({
          id: campaign?.id || `c-${Date.now()}`,
          code: cleanCode,
          title,
          type,
          value: Math.max(0, Number(value)),
          description
        });
      };"""

if old_campaign_modal in html:
    html = html.replace(old_campaign_modal, new_campaign_modal)
    print("Fix 3: Updated CampaignModalComponent to prevent duplicate codes")

# Add codeError alert below code input in CampaignModalComponent
old_code_input = """<div><label className="font-bold block mb-1">Referans / İndirim Kodu:</label><input type="text" placeholder="Örn: YAZ2026" value={code} onChange={e => setCode(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold uppercase text-amber-700" /></div>"""
new_code_input = """<div><label className="font-bold block mb-1">Referans / İndirim Kodu:</label><input type="text" placeholder="Örn: YAZ2026" value={code} onChange={e => { setCode(e.target.value); setCodeError(''); }} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold uppercase text-amber-700" />{codeError && <p className="text-[10px] text-red-500 font-bold mt-1">{codeError}</p>}</div>"""

if old_code_input in html:
    html = html.replace(old_code_input, new_code_input)
    print("Fix 3: Added codeError text below campaign code input")

# Pass campaigns to CampaignModalComponent call in index.html
html = html.replace(
    "<CampaignModalComponent\n              campaign={campaignModalData === 'new' ? null : campaignModalData}\n              onClose={() => setCampaignModalData(null)}\n              onSave={handleSaveCampaign}\n            />",
    "<CampaignModalComponent\n              campaign={campaignModalData === 'new' ? null : campaignModalData}\n              onClose={() => setCampaignModalData(null)}\n              onSave={handleSaveCampaign}\n              campaigns={campaigns}\n            />"
)


# ---------------------------------------------------------
# FIX 4: RBAC Role Management (Edit Role, Delete Role & Persistence)
# ---------------------------------------------------------

# Add handleEditRole & handleDeleteRole in main App component
old_role_handlers = """      const handleAddRole = (roleId, roleName) => {
        setRolesState(prev => ({ ...prev, [roleId]: roleName }));
        setTabPermissionsState(prev => ({
          ...prev,
          dashboard: [...(prev['dashboard'] || []), roleId],
          profile: [...(prev['profile'] || []), roleId]
        }));
      };"""

new_role_handlers = """      const handleAddRole = (roleId, roleName) => {
        const cleanId = roleId.trim().toLowerCase().replace(/[^a-z0-9_]/g, '_');
        if (!cleanId || !roleName.trim()) return;
        setRolesState(prev => ({ ...prev, [cleanId]: roleName }));
        setTabPermissionsState(prev => {
          const updated = { ...prev };
          Object.keys(updated).forEach(t => {
            if (!updated[t].includes(cleanId)) {
              updated[t] = [...updated[t], cleanId];
            }
          });
          return updated;
        });
        showToast(`🛡️ Yeni "${roleName}" Rolü Başarıyla Tanımlandı!`);
      };

      const handleEditRole = (roleId, newRoleName) => {
        if (!newRoleName.trim()) return;
        setRolesState(prev => ({ ...prev, [roleId]: newRoleName }));
        showToast(`✏️ "${newRoleName}" Rol Unvanı Güncellendi!`);
      };

      const handleDeleteRole = (roleId) => {
        if (roleId === 'admin') {
          showToast('⚠️ Admin rolü sistemin ana rolüdür, silinemez!');
          return;
        }
        setRolesState(prev => {
          const copy = { ...prev };
          delete copy[roleId];
          return copy;
        });
        setTabPermissionsState(prev => {
          const updated = { ...prev };
          Object.keys(updated).forEach(t => {
            updated[t] = (updated[t] || []).filter(r => r !== roleId);
          });
          return updated;
        });
        showToast(`🗑️ Rol (${roleId}) ve İzinleri Başarıyla Silindi!`);
      };"""

if old_role_handlers in html:
    html = html.replace(old_role_handlers, new_role_handlers)
    print("Fix 4: Added handleEditRole and handleDeleteRole functions")

# Pass onEditRole and onDeleteRole to SettingsComponent
html = html.replace(
    "onAddRole={handleAddRole}",
    "onAddRole={handleAddRole}\n                      onEditRole={handleEditRole}\n                      onDeleteRole={handleDeleteRole}"
)

# Update SettingsComponent signature and RBAC table header to include Edit & Delete buttons
old_settings_sig = "function SettingsComponent({ activeRole, roles, tabPermissions, onAddRole, onToggleTabPermission, themeColor, onThemeColorChange, menuLayout, onMenuLayoutChange, isCacheEnabled, onToggleCache, onClearCache, onSeedDatabase, showToast, onNavigate, initialSubTab }) {"
new_settings_sig = "function SettingsComponent({ activeRole, roles, tabPermissions, onAddRole, onEditRole, onDeleteRole, onToggleTabPermission, themeColor, onThemeColorChange, menuLayout, onMenuLayoutChange, isCacheEnabled, onToggleCache, onClearCache, onSeedDatabase, showToast, onNavigate, initialSubTab }) {"

if old_settings_sig in html:
    html = html.replace(old_settings_sig, new_settings_sig)
    print("Fix 4: Updated SettingsComponent signature")

# Update RBAC table header in SettingsComponent
old_table_header = """                      {Object.keys(roles).map(roleId => (
                        <th key={roleId} className="p-3 font-extrabold text-center whitespace-nowrap">
                          {roles[roleId]}
                        </th>
                      ))}"""

new_table_header = """                      {Object.keys(roles).map(roleId => (
                        <th key={roleId} className="p-3 font-extrabold text-center whitespace-nowrap border-l border-slate-200 dark:border-brand-border/40">
                          <div className="flex flex-col items-center space-y-1">
                            <span className="text-xs">{roles[roleId]}</span>
                            <span className="text-[9px] font-mono text-slate-400">({roleId})</span>
                            <div className="flex items-center space-x-1 pt-1">
                              <button
                                type="button"
                                title="Rol Adını Düzenle"
                                onClick={() => {
                                  const name = prompt(`"${roles[roleId]}" rolü için yeni unvan yazınız:`, roles[roleId]);
                                  if (name && onEditRole) onEditRole(roleId, name);
                                }}
                                className="p-1 text-blue-500 hover:text-blue-700 hover:bg-blue-500/10 rounded transition"
                              >
                                ✏️
                              </button>
                              {roleId !== 'admin' && (
                                <button
                                  type="button"
                                  title="Rolü Sil"
                                  onClick={() => {
                                    if (confirm(`"${roles[roleId]}" (${roleId}) rolünü ve tüm izinlerini silmek istediğinize emin misiniz?`)) {
                                      if (onDeleteRole) onDeleteRole(roleId);
                                    }
                                  }}
                                  className="p-1 text-red-500 hover:text-red-700 hover:bg-red-500/10 rounded transition"
                                >
                                  🗑️
                                </button>
                              )}
                            </div>
                          </div>
                        </th>
                      ))}"""

if old_table_header in html:
    html = html.replace(old_table_header, new_table_header)
    print("Fix 4: Updated RBAC table headers with Edit & Delete action buttons")

# Update UserModalComponent roles dropdown to be dynamic
old_user_modal_roles = """<div>
                  <label className="font-bold block mb-1">Sistem Kullanıcı Rolü:</label>
                  <select value={role} onChange={e => setRole(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold">
                    <option value="admin">Admin (Tam Yetki)</option>
                    <option value="satisci">Satış Temsilcisi</option>
                    <option value="sosyal_medyaci">Sosyal Medya Uzmanı</option>
                    <option value="musteri">Müşteri / Misafir</option>
                  </select>
                </div>"""

new_user_modal_roles = """<div>
                  <label className="font-bold block mb-1">Sistem Kullanıcı Rolü:</label>
                  <select value={role} onChange={e => setRole(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold">
                    {Object.keys(roles || { admin: 'Admin', satisci: 'Satış Temsilcisi', sosyal_medyaci: 'Sosyal Medya', musteri: 'Müşteri' }).map(rId => (
                      <option key={rId} value={rId}>
                        {(roles && roles[rId]) || rId} ({rId})
                      </option>
                    ))}
                  </select>
                </div>"""

if old_user_modal_roles in html:
    html = html.replace(old_user_modal_roles, new_user_modal_roles)
    print("Fix 4: Updated UserModalComponent role options to be dynamic")

# Pass roles to UserModalComponent
old_user_modal_signature = "function UserModalComponent({ user, onClose, onSave }) {"
new_user_modal_signature = "function UserModalComponent({ user, onClose, onSave, roles }) {"
if old_user_modal_signature in html:
    html = html.replace(old_user_modal_signature, new_user_modal_signature)

html = html.replace(
    "<UserModalComponent\n              user={userModalData === 'new' ? null : userModalData}\n              onClose={() => setUserModalData(null)}\n              onSave={handleSaveUser}\n            />",
    "<UserModalComponent\n              user={userModalData === 'new' ? null : userModalData}\n              onClose={() => setUserModalData(null)}\n              onSave={handleSaveUser}\n              roles={rolesState}\n            />"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Applied all 5 fixes to index.html successfully!")
