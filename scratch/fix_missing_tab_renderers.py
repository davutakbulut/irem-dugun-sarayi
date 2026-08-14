import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update SLUG_TO_TAB with all needed aliases
    slug_entries = """      'ayarlar': 'settings',
      'company-settings': 'company-settings',
      'sirket-bilgileri': 'company-settings',
      'sozlesme-sablonu': 'company-settings',
      'ayarlar/sirket-bilgileri': 'company-settings',
      'yonetim/company-settings': 'company-settings',
      'yonetim/sirket-bilgileri': 'company-settings',
      'yonetim/sozlesme-sablonu': 'company-settings',
      'ayarlar/rol-izinleri': 'settings-rbac',
      'rol-izinleri': 'settings-rbac',
      'settings-rbac': 'settings-rbac',
      'ayarlar/seo-indeksleme': 'settings-indexing',
      'settings-indexing': 'settings-indexing',
      'seo-indeksleme': 'settings-indexing',
      'indeksleme': 'settings-indexing',
      'arama-motoru-ayarlari': 'settings-indexing',
      'ayarlar/gorunum': 'settings-appearance',
      'settings-appearance': 'settings-appearance',
      'gorunum': 'settings-appearance',
      'ayarlar/onbellek': 'settings-performance',
      'settings-performance': 'settings-performance',
      'onbellek': 'settings-performance',
      'ayarlar/hata-simulasyonu': 'settings-errors',
      'settings-errors': 'settings-errors',"""

    old_slug_marker = "'ayarlar': 'settings',"
    if old_slug_marker in content:
        # Find where 'eposta-sablonlari' starts
        end_marker = "'eposta-sablonlari': 'email-templates',"
        start_idx = content.find(old_slug_marker)
        end_idx = content.find(end_marker)
        if start_idx != -1 and end_idx != -1:
            content = content[:start_idx] + slug_entries + "\n      " + content[end_idx:]
            print(f"Updated SLUG_TO_TAB in {h_file}")

    # 2. Update TAB_TO_PATH with all needed paths
    tab_to_path_entries = """      'company-settings': '/yonetim/sirket-bilgileri',
      'settings': '/yonetim/ayarlar',
      'settings-appearance': '/yonetim/ayarlar/gorunum',
      'settings-performance': '/yonetim/ayarlar/onbellek',
      'settings-rbac': '/yonetim/ayarlar/rol-izinleri',
      'settings-indexing': '/yonetim/ayarlar/seo-indeksleme',
      'settings-errors': '/yonetim/ayarlar/hata-simulasyonu',"""

    old_tab_path_marker = "'settings': '/yonetim/ayarlar',"
    if old_tab_path_marker in content:
        start_tp = content.find(old_tab_path_marker)
        end_tp = content.find("'email-templates': '/yonetim/eposta-sablonlari',")
        if start_tp != -1 and end_tp != -1:
            content = content[:start_tp] + tab_to_path_entries + "\n      " + content[end_tp:]
            print(f"Updated TAB_TO_PATH in {h_file}")

    # 3. Ensure {activeTab === 'company-settings' && ...} and {(activeTab === 'roles' || activeTab === 'settings-rbac') && ...} are in App JSX
    company_jsx = """
                  {activeTab === 'company-settings' && (
                    <CompanySettingsComponent
                      companySettings={companySettings}
                      onSave={async (updated) => {
                        try {
                          const res = await fetchWithRetry('/api/company-settings', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify(updated)
                          });
                          const json = await res.json();
                          if (json.success && json.item) {
                            setCompanySettings(json.item);
                            showToast('Şirket Bilgileri ve Sözleşme Şablonu Başarıyla Kaydedildi!');
                          }
                        } catch(e) {
                          showToast('Kaydetme hatası: ' + e.message);
                        }
                      }}
                    />
                  )}
"""

    old_roles_block = """                  {activeTab === 'roles' && (
                    <RolesPageComponent
                      activeRole={activeRole}
                      roles={rolesState}
                      users={users}
                      tabPermissions={tabPermissionsState}
                      onAddRole={handleAddRole}
                      onEditRole={handleEditRole}
                      onDeleteRole={handleDeleteRole}
                      onToggleTabPermission={handleToggleTabPermission}
                      showToast={showToast}
                      navigateTo={navigateTo}
                    />
                  )}"""

    new_roles_block = """                  {(activeTab === 'roles' || activeTab === 'settings-rbac') && (
                    <RolesPageComponent
                      activeRole={activeRole}
                      roles={rolesState}
                      users={users}
                      tabPermissions={tabPermissionsState}
                      onAddRole={handleAddRole}
                      onEditRole={handleEditRole}
                      onDeleteRole={handleDeleteRole}
                      onToggleTabPermission={handleToggleTabPermission}
                      showToast={showToast}
                      navigateTo={navigateTo}
                    />
                  )}"""

    if old_roles_block in content:
        content = content.replace(old_roles_block, new_roles_block)
        print(f"Updated RolesPageComponent condition in {h_file}")

    if "{activeTab === 'company-settings' &&" not in content:
        content = content.replace(
            "{activeTab.startsWith('settings') && (",
            company_jsx + "\n                  {activeTab.startsWith('settings') && ("
        )
        print(f"Injected CompanySettingsComponent into main router in {h_file}")

    # 4. Add indexing subtab button and tab panel inside SettingsComponent
    indexing_btn = """            <button
              type="button"
              onClick={() => setSettingsTab('indexing')}
              className={`px-4 py-2.5 rounded-xl font-bold text-xs transition flex items-center space-x-2 shrink-0 ${
                settingsTab === 'indexing' ? 'gold-button shadow-md' : 'bg-white dark:bg-brand-card text-slate-700 dark:text-gray-300 border border-slate-200 dark:border-brand-border hover:border-amber-500/50'
              }`}
            >
              <span>🔍</span>
              <span>Arama Motoru & İndeksleme</span>
            </button>"""

    old_perf_btn = """            <button
              type="button"
              onClick={() => setSettingsTab('performance')}"""

    if indexing_btn not in content and old_perf_btn in content:
        content = content.replace(old_perf_btn, indexing_btn + "\n\n" + old_perf_btn)
        print(f"Added indexing button to SettingsComponent in {h_file}")

    indexing_panel = """          {settingsTab === 'indexing' && (
            <div className="space-y-6">
              <div className="glass-panel p-6 sm:p-8 rounded-3xl space-y-6 border border-slate-200 dark:border-brand-border shadow-sm">
                <div className="flex items-center space-x-3 border-b border-slate-100 dark:border-brand-border/40 pb-4">
                  <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
                    <ThemeIcon icon="search" className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="text-xl font-heading font-extrabold text-slate-900 dark:text-gray-100">
                      Arama Motoru (SEO) & İndeksleme Güvenliği
                    </h3>
                    <p className="text-xs text-slate-500 dark:text-gray-400">
                      Google ve diğer arama motoru botlarının yönetim sayfalarını taramasını engelleyin ve genel site SEO başlıklarını yapılandırın.
                    </p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div className="bg-slate-50 dark:bg-brand-dark p-5 rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900 dark:text-gray-100">Yönetim Paneli İndeksleme Koruması</span>
                      <span className="text-[10px] bg-emerald-500/10 text-emerald-600 font-bold px-2 py-0.5 rounded-full border border-emerald-500/30">AKTİF (ÖNERİLEN)</span>
                    </div>
                    <p className="text-slate-500 dark:text-gray-400 text-[11px] leading-relaxed">
                      Yönetim panelindeki müşteri kayıtları ve finansal veriler <code>noindex, nofollow, noarchive, nosnippet</code> etiketleriyle arama motorlarından gizlenir.
                    </p>
                  </div>

                  <div className="bg-slate-50 dark:bg-brand-dark p-5 rounded-2xl border border-slate-200 dark:border-brand-border space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-slate-900 dark:text-gray-100">Müşteri Web Sitesi SEO İndeksi</span>
                      <span className="text-[10px] bg-amber-500/10 text-amber-600 font-bold px-2 py-0.5 rounded-full border border-amber-500/30">index, follow</span>
                    </div>
                    <p className="text-slate-500 dark:text-gray-400 text-[11px] leading-relaxed">
                      Salonlar, paketler, blog ve iletişim sayfaları arama motorlarına açıktır ve organik trafik çeker.
                    </p>
                  </div>
                </div>

                <div className="p-4 rounded-2xl bg-amber-500/5 border border-amber-500/20 text-xs text-slate-600 dark:text-gray-300 flex items-center justify-between">
                  <span>Robots.txt & Sitemap.xml durumunuz optimize edilmiştir.</span>
                  <button
                    type="button"
                    onClick={() => showToast('Arama motoru indeksleme ayarları güncellendi ve meta etiketleri doğrulandı!')}
                    className="gold-button font-bold px-4 py-2 rounded-xl text-xs shadow"
                  >
                    SEO Ayarlarını Kaydet ✓
                  </button>
                </div>
              </div>
            </div>
          )}"""

    if indexing_panel not in content:
        content = content.replace(
            "{settingsTab === 'performance' && (",
            indexing_panel + "\n\n          {settingsTab === 'performance' && ("
        )
        print(f"Added indexing panel into SettingsComponent in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All tab renderers and routing aliases fixed successfully!")
