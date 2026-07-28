import React, { useState } from 'react';
import { THEME_PALETTES, ROLE_NAMES } from '../constants';

export default function SettingsPageComponent({ activeRole, rolesState, tabPermissionsState, onTogglePermission, isCacheEnabled, onToggleCache, showToast, activePalette, onSelectPalette, initialSubTab = 'appearance' }) {
  const [activeSubTab, setActiveSubTab] = useState(initialSubTab);

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      <div>
        <h2 className="text-2xl font-heading font-extrabold gold-gradient-text">Sistem Ayarları & Konfigürasyon</h2>
        <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">Görünüm temaları, önbellekleme performansı ve RBAC rol izinlerini yönetin</p>
      </div>

      {/* SUB-TAB NAV */}
      <div className="flex space-x-2 border-b border-slate-200 dark:border-brand-border pb-2 text-xs font-bold">
        <button
          onClick={() => setActiveSubTab('appearance')}
          className={`px-4 py-2 rounded-xl transition ${activeSubTab === 'appearance' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-card text-slate-600 dark:text-gray-400'}`}
        >
          🎨 Görünüm & Tema Paletleri ({THEME_PALETTES.length} Tema)
        </button>
        <button
          onClick={() => setActiveSubTab('performance')}
          className={`px-4 py-2 rounded-xl transition ${activeSubTab === 'performance' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-card text-slate-600 dark:text-gray-400'}`}
        >
          ⚡ Önbellekleme & Performans
        </button>
        <button
          onClick={() => setActiveSubTab('rbac')}
          className={`px-4 py-2 rounded-xl transition ${activeSubTab === 'rbac' ? 'gold-button shadow' : 'bg-slate-100 dark:bg-brand-card text-slate-600 dark:text-gray-400'}`}
        >
          🛡️ Rol & Sayfa İzin Matrisi
        </button>
      </div>

      {/* TAB 1: APPEARANCE & 10 CORPORATE THEMES */}
      {activeSubTab === 'appearance' && (
        <div className="glass-panel p-6 rounded-3xl space-y-4 border border-amber-500/30">
          <div className="flex items-center space-x-3 border-b border-slate-200 dark:border-brand-border pb-3">
            <span className="text-2xl">🎨</span>
            <div>
              <h3 className="font-heading font-bold text-base text-slate-800 dark:text-gray-100">Kurumsal Tema & Stil Geometrisi Seçimi</h3>
              <p className="text-xs text-slate-500 dark:text-gray-400">Tek tıkla tüm buton, kart ve renk paleti çizgisini kurumsal olarak güncelleyin</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            {THEME_PALETTES.map(p => {
              const isSelected = activePalette === p.id;
              return (
                <div
                  key={p.id}
                  onClick={() => {
                    onSelectPalette(p.id);
                    showToast(`🎨 Tema Değiştirildi: ${p.name}`);
                  }}
                  className={`p-4 rounded-2xl border cursor-pointer transition-all duration-200 flex items-center justify-between space-x-3 ${
                    isSelected
                      ? 'border-amber-500 bg-amber-500/10 ring-2 ring-amber-500/50 scale-[1.01]'
                      : 'border-slate-200 dark:border-brand-border/60 bg-white dark:bg-brand-card hover:border-amber-500/50'
                  }`}
                >
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-white shadow-md flex-shrink-0" style={{ backgroundColor: p.primaryColor }}>
                      {p.id.includes('obsidian') ? '🖤' : p.id.includes('gold') ? '👑' : p.id.includes('emerald') ? '🌿' : p.id.includes('sapphire') ? '🔷' : p.id.includes('rose') ? '🌹' : p.id.includes('platinum') ? '🩶' : '⚡'}
                    </div>
                    <div>
                      <div className="font-bold text-xs text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                        <span>{p.name}</span>
                        {isSelected && <span className="text-[10px] bg-amber-500 text-white font-bold px-1.5 py-0.2 rounded">AKTİF TEMA</span>}
                      </div>
                      <div className="text-[10px] text-slate-500 dark:text-gray-400 mt-0.5">{p.description}</div>
                      <div className="text-[9px] font-mono text-amber-700 dark:text-gold-400 font-bold mt-1 flex items-center space-x-2">
                        <span>Keskinlik:</span>
                        <code className="bg-slate-100 dark:bg-brand-dark px-1.5 py-0.5 rounded text-[10px] border border-amber-500/30">{p.geometry || 'rounded-2xl'}</code>
                      </div>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectPalette(p.id);
                      showToast(`🎨 Tema Değiştirildi: ${p.name}`);
                    }}
                    className={`px-3 py-1.5 rounded-xl text-xs font-bold transition flex items-center space-x-1 flex-shrink-0 ${
                      isSelected ? 'gold-button shadow-md' : 'bg-slate-100 dark:bg-brand-dark text-slate-700 dark:text-gray-300 hover:bg-amber-500/20'
                    }`}
                  >
                    <span>{isSelected ? '✓ Aktif' : 'Temayı Uygula'}</span>
                  </button>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 2: PERFORMANCE */}
      {activeSubTab === 'performance' && (
        <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border text-xs">
          <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">⚡ LocalStorage Önbellekleme Motoru</h3>
          <p className="text-slate-500">Sistem verilerini tarayıcı hafızasına alarak 0ms sayfa yükleme hızı sağlar.</p>
          <div className="flex items-center space-x-3 bg-slate-50 dark:bg-brand-dark p-4 rounded-2xl border border-slate-200 dark:border-brand-border">
            <input
              type="checkbox"
              checked={isCacheEnabled}
              onChange={e => {
                onToggleCache(e.target.checked);
                showToast(e.target.checked ? '⚡ Önbellekleme Etkinleştirildi' : '⚠️ Önbellekleme Devre Dışı');
              }}
              className="w-5 h-5 accent-amber-600"
            />
            <div>
              <div className="font-bold text-slate-800 dark:text-gray-200">Anlık Önbellek Kaydı (Instant Cache Persistence)</div>
              <div className="text-[10px] text-slate-400">Son yapılan değişiklikleri belleğe kaydeder</div>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: RBAC MATRIX */}
      {activeSubTab === 'rbac' && (
        <div className="glass-panel p-6 rounded-3xl space-y-4 border border-slate-200 dark:border-brand-border text-xs">
          <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">🛡️ Dinamik Rol & Sayfa İzin Matrisi</h3>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-slate-200 dark:border-brand-border text-slate-400">
                  <th className="p-2">Sayfa / Rota</th>
                  {Object.entries(rolesState).map(([rKey, rName]) => (
                    <th key={rKey} className="p-2 text-center">{rName}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {Object.keys(tabPermissionsState).map(tabKey => (
                  <tr key={tabKey} className="border-b border-slate-200/50 dark:border-brand-border/40 hover:bg-slate-50 dark:hover:bg-brand-dark/50">
                    <td className="p-2.5 font-bold text-slate-800 dark:text-gray-200 capitalize">{tabKey} Sayfası</td>
                    {Object.keys(rolesState).map(rKey => {
                      const isAllowed = (tabPermissionsState[tabKey] || []).includes(rKey);
                      return (
                        <td key={rKey} className="p-2.5 text-center">
                          <input
                            type="checkbox"
                            checked={isAllowed}
                            onChange={() => onTogglePermission(tabKey, rKey)}
                            className="w-4 h-4 accent-amber-600 cursor-pointer"
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
      )}
    </div>
  );
}
