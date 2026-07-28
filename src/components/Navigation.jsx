import React, { useState } from 'react';
import { ROLE_NAMES, TAB_TO_SLUG } from '../constants';

export function HeaderComponent({ activeRole, rolesState, onRoleChange, theme, onToggleTheme, isMobileMenuOpen, setIsMobileMenuOpen, navigateTo }) {
  const [isRoleDropdownOpen, setIsRoleDropdownOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 glass-panel border-b border-amber-500/20 px-4 py-3 shadow-md">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        
        {/* LOGO & LEFT SIDE MENU BUTTON */}
        <div className="flex items-center space-x-3">
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-amber-700 dark:text-gold-400 font-bold flex items-center justify-center hover:bg-amber-500 hover:text-white transition shadow-sm"
            aria-label="Tüm Menüyü Aç"
            title="Tüm Gezinti Menüsünü Aç (%90 Genişlik)"
          >
            <span className="text-xl">☰</span>
          </button>

          <a href="#/anasayfa" onClick={(e) => { e.preventDefault(); navigateTo('dashboard'); }} className="flex items-center space-x-2.5">
            <div className="w-10 h-10 rounded-2xl gold-button flex items-center justify-center font-bold text-xl shadow-md">
              👑
            </div>
            <div>
              <h1 className="font-heading font-extrabold text-base tracking-tight text-slate-800 dark:text-gray-100">
                İrem Düğün Sarayı
              </h1>
              <p className="text-[10px] font-bold text-amber-600 dark:text-gold-400">
                Kiralama & Organizasyon Yönetimi
              </p>
            </div>
          </a>
        </div>

        {/* RIGHT CONTROLS */}
        <div className="flex items-center space-x-3">
          
          <button
            onClick={onToggleTheme}
            className="w-9 h-9 rounded-xl bg-slate-100 dark:bg-brand-card border border-slate-200 dark:border-brand-border text-amber-500 flex items-center justify-center hover:scale-105 transition"
            title="Aydınlık/Karanlık Tema Değiştir"
          >
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>

          <div className="relative">
            <button
              onClick={() => setIsRoleDropdownOpen(!isRoleDropdownOpen)}
              className="flex items-center space-x-2.5 bg-slate-100 dark:bg-brand-card p-1.5 pr-3 rounded-2xl border border-slate-200 dark:border-brand-border/60 hover:border-amber-500/50 transition shadow-sm"
            >
              <img
                src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80"
                alt="Profil Avatar"
                className="w-8 h-8 rounded-xl object-cover border border-amber-500"
              />
              <div className="hidden sm:block text-left">
                <div className="text-xs font-bold text-slate-800 dark:text-gray-100">İrem Yılmaz</div>
                <div className="text-[10px] font-bold text-amber-600 dark:text-gold-400">{ROLE_NAMES[activeRole]}</div>
              </div>
              <span className="text-xs text-slate-400">▼</span>
            </button>

            {isRoleDropdownOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-brand-card border border-amber-500/40 rounded-2xl shadow-2xl p-2 z-50 space-y-1 text-xs">
                <a
                  href="#/profil"
                  onClick={(e) => { e.preventDefault(); navigateTo('profile'); setIsRoleDropdownOpen(false); }}
                  className="flex items-center space-x-2.5 p-2 rounded-xl hover:bg-amber-500/10 text-slate-700 dark:text-gray-200 font-bold"
                >
                  <span>👤</span><span>Profilimi Düzenle</span>
                </a>
                <a
                  href="#/ayarlar"
                  onClick={(e) => { e.preventDefault(); navigateTo('settings'); setIsRoleDropdownOpen(false); }}
                  className="flex items-center space-x-2.5 p-2 rounded-xl hover:bg-amber-500/10 text-slate-700 dark:text-gray-200 font-bold"
                >
                  <span>⚙️</span><span>Sistem Ayarları</span>
                </a>
                <div className="border-t border-slate-200 dark:border-brand-border/40 my-1 pt-1">
                  <div className="text-[10px] font-bold text-slate-400 px-2 mb-1">Kullanıcı Rolü Değiştir:</div>
                  {Object.entries(rolesState).map(([roleKey, roleName]) => (
                    <button
                      key={roleKey}
                      onClick={() => { onRoleChange(roleKey); setIsRoleDropdownOpen(false); }}
                      className={`w-full text-left p-1.5 rounded-lg flex items-center justify-between text-[11px] font-bold ${
                        activeRole === roleKey ? 'bg-amber-500/20 text-amber-700 dark:text-gold-400' : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-dark'
                      }`}
                    >
                      <span>{roleName}</span>
                      {activeRole === roleKey && <span>✓</span>}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

        </div>

      </div>
    </header>
  );
}

export function SidebarComponent({ activeTab, activeRole, tabPermissionsState, navigateTo }) {
  return (
    <aside aria-label="Ana Gezinti Menüsü" className="w-64 glass-panel p-4 hidden lg:flex flex-col justify-between border-r border-slate-200 dark:border-brand-border/40">
      <nav className="space-y-1">
        <div className="text-[10px] font-bold text-slate-400 dark:text-gray-400 uppercase tracking-wider px-3 mb-2">Menü</div>
        {[
          { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: '📊' },
          { id: 'create-reservation', label: '➕ Yeni Rezervasyon', icon: '📝' },
          { id: 'venues', label: 'Düğün Salonlarım', icon: '🏛️' },
          { id: 'services', label: 'Ek Hizmetler', icon: '✨' },
          { id: 'reservations', label: 'Rezervasyonlarım', icon: '📋' },
          { id: 'calendar', label: 'Takvim Görünümü', icon: '📅' },
          { id: 'campaigns', label: 'Kampanyalar', icon: '🎁' },
          { id: 'finance', label: 'Finans & Fatura', icon: '💰' },
          { id: 'customers', label: 'Müşteri Rehberi', icon: '👥' },
          { id: 'users', label: 'Kullanıcı Yönetimi', icon: '⚙️' },
          { id: 'reports', label: 'Raporlar & AI Öneri', icon: '📈' },
          { id: 'media', label: 'Medya & Foto Yükle', icon: '📷' }
        ]
        .filter(item => (tabPermissionsState[item.id] || []).includes(activeRole))
        .map(item => (
          <a
            key={item.id}
            href={`#/${TAB_TO_SLUG[item.id]}`}
            onClick={(e) => {
              e.preventDefault();
              navigateTo(item.id);
            }}
            className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-xl font-medium text-xs transition ${
              activeTab === item.id ? 'bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 font-bold shadow-sm' : 'text-slate-600 dark:text-gray-400 hover:bg-slate-100 dark:hover:bg-brand-card hover:text-slate-900'
            }`}
          >
            <span className="text-base">{item.icon}</span>
            <span>{item.label}</span>
          </a>
        ))}

        {(tabPermissionsState['settings'] || []).includes(activeRole) && (
          <div className="pt-2 space-y-1 border-t border-slate-200 dark:border-brand-border/40">
            <div className="text-[10px] font-bold text-slate-400 dark:text-gray-400 uppercase tracking-wider px-3 my-1">Ayarlar</div>
            <a
              href="#/ayarlar"
              onClick={(e) => { e.preventDefault(); navigateTo('settings'); }}
              className={`w-full flex items-center space-x-3 px-3 py-2 rounded-xl text-xs font-bold transition ${
                activeTab === 'settings' ? 'bg-amber-500/10 text-amber-800 dark:text-gold-400 border border-amber-500/30 shadow-sm' : 'text-slate-700 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-brand-card'
              }`}
            >
              <span className="text-base">⚙️</span>
              <span>Sistem Ayarları</span>
            </a>
            <div className="pl-6 space-y-1">
              <a
                href="#/ayarlar/gorunum"
                onClick={(e) => { e.preventDefault(); navigateTo('settings-appearance'); }}
                className={`w-full flex items-center space-x-2 px-2 py-1.5 rounded-lg text-[11px] font-medium transition ${
                  activeTab === 'settings-appearance' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800'
                }`}
              >
                <span>🎨</span><span>Görünüm & Tema</span>
              </a>
              <a
                href="#/ayarlar/onbellek"
                onClick={(e) => { e.preventDefault(); navigateTo('settings-performance'); }}
                className={`w-full flex items-center space-x-2 px-2 py-1.5 rounded-lg text-[11px] font-medium transition ${
                  activeTab === 'settings-performance' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800'
                }`}
              >
                <span>⚡</span><span>Önbellekleme</span>
              </a>
              <a
                href="#/ayarlar/rol-izinleri"
                onClick={(e) => { e.preventDefault(); navigateTo('settings-rbac'); }}
                className={`w-full flex items-center space-x-2 px-2 py-1.5 rounded-lg text-[11px] font-medium transition ${
                  activeTab === 'settings-rbac' ? 'text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10' : 'text-slate-500 dark:text-gray-400 hover:text-slate-800'
                }`}
              >
                <span>🛡️</span><span>Rol & İzin Yönetimi</span>
              </a>
            </div>
          </div>
        )}
      </nav>
    </aside>
  );
}
