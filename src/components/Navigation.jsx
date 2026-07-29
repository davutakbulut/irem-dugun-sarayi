import React from 'react';
import { ThemeIcon } from './ThemeIcon';

export function SidebarComponent({ activeTab, onTabChange, activeRole, onRoleChange }) {
  const menuItems = [
    { id: 'dashboard', label: 'Genel Bakış', icon: 'chart', fallbackEmoji: '📊' },
    { id: 'create-reservation', label: 'Rezervasyon Oluştur', icon: 'sparkles', fallbackEmoji: '✨', badge: 'YENİ' },
    { id: 'reservations', label: 'Rezervasyonlar & Takvim', icon: 'calendar', fallbackEmoji: '📅' },
    { id: 'venues', label: 'Düğün Salonları', icon: 'venue', fallbackEmoji: '🏰' },
    { id: 'services', label: 'Ek Hizmetler', icon: 'gift', fallbackEmoji: '🎁' },
    { id: 'customers', label: 'Müşteriler & Üyeler', icon: 'user', fallbackEmoji: '👥' },
    { id: 'campaigns', label: 'Kampanyalar & AI', icon: 'campaign', fallbackEmoji: '🏷️' },
    { id: 'reports', label: 'Raporlar & Analizler', icon: 'chart', fallbackEmoji: '📈' },
    { id: 'users', label: 'Yetkili Personel (RBAC)', icon: 'shield', fallbackEmoji: '🛡️', roleNeeded: 'SuperAdmin' },
    { id: 'settings', label: 'Ayarlar & Görünüm', icon: 'settings', fallbackEmoji: '⚙️' }
  ];

  return (
    <aside className="w-64 bg-white dark:bg-brand-card border-r border-slate-200 dark:border-brand-border flex flex-col justify-between shrink-0 shadow-sm transition-all duration-300">
      <div>
        {/* LOGO & BRANDING */}
        <div className="p-5 border-b border-slate-200 dark:border-brand-border flex items-center space-x-3">
          <div className="w-10 h-10 rounded-2xl gold-button flex items-center justify-center font-extrabold text-xl shadow-md shrink-0">
            <ThemeIcon icon="crown" fallbackEmoji="🏰" className="w-6 h-6 shrink-0" />
          </div>
          <div>
            <h1 className="font-heading font-extrabold text-base gold-gradient-text leading-tight tracking-tight">
              İREM DÜĞÜN SARAYI
            </h1>
            <p className="text-[10px] text-slate-500 dark:text-gray-400 font-bold uppercase tracking-wider">
              Rezervasyon & Yönetim
            </p>
          </div>
        </div>

        {/* NAVIGATION LINKS */}
        <nav className="p-3 space-y-1.5">
          {menuItems.map(item => {
            if (item.roleNeeded && activeRole !== item.roleNeeded && activeRole !== 'SuperAdmin') {
              return null;
            }

            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-bold text-xs transition-all duration-200 ${
                  isActive
                    ? 'gold-button shadow-md transform translate-x-1'
                    : 'text-slate-700 dark:text-gray-300 hover:bg-slate-100 dark:hover:bg-brand-dark'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <ThemeIcon icon={item.icon} fallbackEmoji={item.fallbackEmoji} className="w-4 h-4 shrink-0" />
                  <span>{item.label}</span>
                </div>
                {item.badge && (
                  <span className="text-[9px] bg-red-500 text-white font-extrabold px-2 py-0.5 rounded-full shadow">
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </nav>
      </div>

      {/* FOOTER & ROLE SWITCHER */}
      <div className="p-4 border-t border-slate-200 dark:border-brand-border space-y-3 bg-slate-50/50 dark:bg-brand-dark/50">
        <div className="flex items-center justify-between">
          <div className="text-[10px] font-bold text-slate-500 dark:text-gray-400">Aktif Rol (RBAC):</div>
          <select
            value={activeRole}
            onChange={(e) => onRoleChange(e.target.value)}
            className="text-[10px] font-bold bg-white dark:bg-brand-card border border-slate-200 dark:border-brand-border rounded-lg px-2 py-1 text-slate-800 dark:text-gray-200"
          >
            <option value="SuperAdmin">SuperAdmin (Tam Yetki)</option>
            <option value="Manager">Müdür (Manager)</option>
            <option value="Staff">Personel (Staff)</option>
          </select>
        </div>

        <div className="text-[10px] text-center text-slate-400 dark:text-gray-500 font-bold">
          İrem Düğün Sarayı v2.0 • Vite React
        </div>
      </div>
    </aside>
  );
}

export function HeaderComponent({ activeTab, onTabChange, activeRole, currentUser }) {
  return (
    <header className="h-16 bg-white/80 dark:bg-brand-card/80 backdrop-blur-md border-b border-slate-200 dark:border-brand-border px-6 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      <div className="flex items-center space-x-3">
        <h2 className="font-heading font-extrabold text-sm sm:text-base text-slate-800 dark:text-gray-100 flex items-center space-x-2">
          {activeTab === 'dashboard' && <><ThemeIcon icon="chart" fallbackEmoji="📊" className="w-5 h-5 text-amber-500 shrink-0" /><span>Genel Bakış & Performans Özeti</span></>}
          {activeTab === 'create-reservation' && <><ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-5 h-5 text-amber-500 shrink-0" /><span>Yeni Rezervasyon & Sözleşme Kartı</span></>}
          {activeTab === 'reservations' && <><ThemeIcon icon="calendar" fallbackEmoji="📅" className="w-5 h-5 text-amber-500 shrink-0" /><span>Rezervasyon Yönetimi & Canlı Takvim</span></>}
          {activeTab === 'venues' && <><ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-5 h-5 text-amber-500 shrink-0" /><span>Düğün Salonları & Kapasite Bilgileri</span></>}
          {activeTab === 'services' && <><ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-5 h-5 text-amber-500 shrink-0" /><span>Ek Hizmetler & Birim Fiyatlar</span></>}
          {activeTab === 'customers' && <><ThemeIcon icon="user" fallbackEmoji="👥" className="w-5 h-5 text-amber-500 shrink-0" /><span>Müşteri Rehberi & Otomatik Üyelikler</span></>}
          {activeTab === 'campaigns' && <><ThemeIcon icon="campaign" fallbackEmoji="🏷️" className="w-5 h-5 text-amber-500 shrink-0" /><span>Kampanyalar & AI Öneri Motoru</span></>}
          {activeTab === 'reports' && <><ThemeIcon icon="chart" fallbackEmoji="📈" className="w-5 h-5 text-amber-500 shrink-0" /><span>Raporlar & Finansal Analizler</span></>}
          {activeTab === 'users' && <><ThemeIcon icon="shield" fallbackEmoji="🛡️" className="w-5 h-5 text-amber-500 shrink-0" /><span>Yetkili Personel Listesi (RBAC)</span></>}
          {activeTab === 'settings' && <><ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-5 h-5 text-amber-500 shrink-0" /><span>Sistem Ayarları & Kurumsal Temalar</span></>}
        </h2>
      </div>

      <div className="flex items-center space-x-4">
        {activeTab !== 'create-reservation' && (
          <button
            onClick={() => onTabChange('create-reservation')}
            className="gold-button font-bold text-xs px-3.5 py-2 rounded-xl shadow flex items-center space-x-1.5 hover:scale-105 transition"
          >
            <ThemeIcon icon="plus" fallbackEmoji="➕" className="w-3.5 h-3.5 shrink-0" />
            <span>Yeni Rezervasyon Oluştur</span>
          </button>
        )}

        <div className="flex items-center space-x-2.5 border-l border-slate-200 dark:border-brand-border pl-4">
          <img
            src={currentUser?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'}
            alt="User"
            className="w-9 h-9 rounded-full object-cover border-2 border-amber-500/50 shadow-sm"
          />
          <div className="hidden sm:block text-left">
            <div className="text-xs font-bold text-slate-800 dark:text-gray-100 leading-tight">
              {currentUser?.name || 'Davut Akbulut'}
            </div>
            <div className="text-[10px] text-amber-600 dark:text-gold-400 font-bold">
              {activeRole}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
