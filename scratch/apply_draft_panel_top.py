import re

draft_block = """
          {/* DRAFT / UNCOMPLETED RESERVATIONS DEDICATED PANEL (TOP OF PAGE) */}
          <div className="glass-panel p-5 sm:p-6 rounded-3xl border-2 border-amber-500/40 bg-amber-500/5 dark:bg-amber-950/20 space-y-4 shadow-lg animate-fade-in">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 border-b border-amber-500/20 pb-3">
              <div className="flex items-center space-x-2.5">
                <div className="w-10 h-10 rounded-2xl bg-amber-500/20 border border-amber-500/40 text-amber-700 dark:text-gold-400 flex items-center justify-center font-bold text-lg shrink-0">
                  <ThemeIcon icon="sparkles" fallbackEmoji="⏳" className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-heading font-extrabold text-base text-slate-900 dark:text-white flex items-center space-x-2">
                    <span>Tamamlanmamış Taslak Rezervasyonlar</span>
                    <span className="bg-amber-500 text-white font-mono text-xs px-2.5 py-0.5 rounded-full font-bold">
                      {(draftReservations || []).length} Adet
                    </span>
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-gray-400 font-medium">
                    Form doldurulurken otomatik kaydedilmiş, yarım kalmış veya onay bekleyen taslaklar.
                  </p>
                </div>
              </div>

              <button
                type="button"
                onClick={() => setIsDraftPanelOpen(!isDraftPanelOpen)}
                className="text-xs font-bold text-amber-700 dark:text-gold-400 hover:underline inline-flex items-center space-x-1 shrink-0 cursor-pointer"
              >
                <span>{isDraftPanelOpen ? 'Taslak Paneli Gizle ▲' : 'Taslak Paneli Göster ▼'}</span>
              </button>
            </div>

            {isDraftPanelOpen && (
              <>
                {(!draftReservations || draftReservations.length === 0) ? (
                  <div className="bg-white/60 dark:bg-brand-dark/40 p-4 rounded-2xl border border-dashed border-amber-500/30 text-center space-y-2">
                    <p className="text-xs text-slate-600 dark:text-gray-300 font-semibold">
                      Henüz yarım kalmış bir taslak rezervasyonunuz bulunmuyor.
                    </p>
                    <button
                      type="button"
                      onClick={() => navigateTo && navigateTo('create-reservation')}
                      className="gold-button font-bold text-xs px-3.5 py-1.5 rounded-xl shadow-sm inline-flex items-center space-x-1 cursor-pointer"
                    >
                      <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 mr-1" />
                      <span>Yeni Rezervasyon Başlat</span>
                    </button>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pt-1">
                    {draftReservations.map((draft, idx) => {
                      const custName = draft.customerInfo?.name || draft.formData?.newCustName || 'İsimsiz Müşteri';
                      const custPhone = draft.customerInfo?.phone || draft.formData?.newCustPhone || '-';
                      const venueName = draft.customerInfo?.venueName || (venues.find(v => v.id === draft.formData?.venueId)?.name) || 'Salon Seçilmedi';
                      const eventDate = draft.customerInfo?.date || draft.formData?.startDate || 'Tarih Belirtilmedi';
                      const percentage = draft.completionPercentage || 0;
                      const updatedAtFormatted = draft.updatedAt ? new Date(draft.updatedAt).toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' }) : '-';
                      const lastLogger = draft.accessLogs && draft.accessLogs.length > 0 ? draft.accessLogs[draft.accessLogs.length - 1].userName : 'Sistem';

                      return (
                        <div key={draft.refKey || idx} className="bg-white dark:bg-brand-card border border-amber-500/30 rounded-2xl p-4 space-y-3 shadow-md hover:shadow-lg transition flex flex-col justify-between">
                          <div className="space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="font-mono text-xs font-extrabold bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/30 px-2.5 py-1 rounded-lg inline-flex items-center">
                                <ThemeIcon icon="shield" fallbackEmoji="🔑" className="w-3.5 h-3.5 mr-1 shrink-0 text-amber-600 dark:text-gold-400" />
                                <span>{draft.refKey}</span>
                              </span>
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-gold-400">
                                TASLAK (%{percentage})
                              </span>
                            </div>

                            <div>
                              <h4 className="font-bold text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-1.5">
                                <ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 text-amber-700 dark:text-gold-400 shrink-0" />
                                <span>{custName}</span>
                              </h4>
                              <p className="text-xs text-slate-500 dark:text-gray-400 font-mono mt-0.5 flex items-center space-x-1">
                                <ThemeIcon icon="phone" fallbackEmoji="📞" className="w-3.5 h-3.5 text-slate-400 shrink-0" />
                                <span>{custPhone}</span>
                              </p>
                            </div>

                            <div className="text-xs text-slate-600 dark:text-gray-300 space-y-1 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border">
                              <div className="flex justify-between items-center">
                                <span className="text-slate-400">Salon:</span>
                                <span className="font-semibold">{venueName}</span>
                              </div>
                              <div className="flex justify-between items-center">
                                <span className="text-slate-400">Tarih:</span>
                                <span className="font-semibold">{eventDate}</span>
                              </div>
                              <div className="flex justify-between items-center text-[11px] pt-1 border-t border-slate-200/50 dark:border-brand-border">
                                <span className="text-slate-400">Son İşlem:</span>
                                <span className="font-mono">{updatedAtFormatted} ({lastLogger})</span>
                              </div>
                            </div>

                            <div>
                              <div className="flex justify-between text-[10px] font-bold text-slate-500 mb-1">
                                <span>Form Doluluğu</span>
                                <span>%{percentage}</span>
                              </div>
                              <div className="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
                                <div
                                  className="bg-amber-500 h-full rounded-full transition-all duration-500"
                                  style={{ width: `${percentage}%` }}
                                ></div>
                              </div>
                            </div>
                          </div>

                          <div className="pt-2 flex items-center gap-2 border-t border-slate-100 dark:border-brand-border">
                            <button
                              type="button"
                              onClick={() => {
                                window.location.hash = `#/rezervasyon-olustur?ref=${draft.refKey}`;
                                if (navigateTo) navigateTo('create-reservation', { ref: draft.refKey });
                              }}
                              className="flex-1 gold-button font-bold py-2.5 px-3 rounded-xl text-xs shadow text-center flex items-center justify-center space-x-1.5 cursor-pointer"
                            >
                              <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3.5 h-3.5 shrink-0" />
                              <span>Devam Et & Tamamla</span>
                            </button>
                            
                            <button
                              type="button"
                              onClick={() => {
                                if (window.confirm(`${draft.refKey} referanslı taslağı silmek istediğinize emin misiniz?`)) {
                                  if (setDraftReservations) {
                                    setDraftReservations(prev => prev.filter(d => d.refKey !== draft.refKey));
                                  }
                                }
                              }}
                              className="p-2.5 bg-red-100 dark:bg-red-950/40 text-red-600 dark:text-red-400 hover:bg-red-200 rounded-xl text-xs transition flex items-center justify-center cursor-pointer"
                              title="Taslağı Sil"
                            >
                              <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                            </button>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            )}
          </div>
"""

# Update src/pages/ReservationsListPage.jsx
with open('src/pages/ReservationsListPage.jsx', 'r', encoding='utf-8') as f:
    code = f.read()

# Remove old draft block from bottom
old_draft_pattern = r'\{/\* DRAFT / UNCOMPLETED RESERVATIONS DEDICATED PANEL.*?\n\s*\}\)'
code_cleaned = re.sub(old_draft_pattern, '', code, flags=re.DOTALL)

# Insert draft_block right after header area (before {/* COLLAPSIBLE FILTER PANEL */})
header_end_target = '{/* COLLAPSIBLE FILTER PANEL */}'
if header_end_target in code_cleaned:
    new_code = code_cleaned.replace(header_end_target, draft_block + "\n\n          " + header_end_target)
    with open('src/pages/ReservationsListPage.jsx', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print("Successfully updated src/pages/ReservationsListPage.jsx with TOP Draft Panel!")
else:
    print("Error: header end target not found in ReservationsListPage.jsx")

# Now update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove export and sync ReservationsListComponent into index.html
res_comp_code = new_code.replace('export function ReservationsListPage(', 'function ReservationsListComponent(')
res_comp_code = res_comp_code.replace('export function ReservationsListPage', 'function ReservationsListComponent')

# Remove import lines
lines = res_comp_code.split('\n')
clean_lines = [l for l in lines if not l.strip().startswith('import ')]
clean_code = '\n'.join(clean_lines)

p_start = html.find('// --- RESERVATIONS LIST COMPONENT ---')
p_end = html.find('// --- USERS COMPONENT ---')

if p_start != -1 and p_end != -1:
    new_html = html[:p_start] + '// --- RESERVATIONS LIST COMPONENT ---\n' + clean_code + '\n\n' + html[p_end:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully synced ReservationsListComponent with TOP Draft Panel to index.html!")
else:
    print("Error: markers not found in index.html", p_start, p_end)

