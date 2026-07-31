import React from 'react';
import { ROLE_NAMES, TAB_TO_SLUG } from '../constants';
import { ThemeIcon } from './ThemeIcon';

export default function MobileDrawer({ isOpen, onClose, activeTab, activeRole, tabPermissionsState, navigateTo }) {
  if (!isOpen) return null;

  const drawerItems = [
    { id: 'dashboard', label: 'Anasayfa / İstatistikler', icon: 'chart', fallbackEmoji: '📊' },
    { id: 'create-reservation', label: 'Yeni Rezervasyon', icon: 'plus', fallbackEmoji: '➕' },
    { id: 'venues', label: 'Düğün Salonlarım', icon: 'venue', fallbackEmoji: '🏰' },
    { id: 'services', label: 'Ek Hizmetler', icon: 'gift', fallbackEmoji: '🎁' },
    { id: 'reservations', label: 'Rezervasyonlarım', icon: 'calendar', fallbackEmoji: '📋' },
    { id: 'calendar', label: 'Takvim Görünümü', icon: 'calendar', fallbackEmoji: '📅' },
    { id: 'campaigns', label: 'Kampanyalar', icon: 'campaign', fallbackEmoji: '🏷️' },
    { id: 'finance', label: 'Finans & Fatura', icon: 'money', fallbackEmoji: '💰' },
    { id: 'customers', label: 'Müşteri Rehberi', icon: 'user', fallbackEmoji: '👥' },
    { id: 'users', label: 'Kullanıcı Yönetimi', icon: 'shield', fallbackEmoji: '🛡️' },
    { id: 'reports', label: 'Raporlar & AI Öneri', icon: 'chart', fallbackEmoji: '📈' },
    { id: 'media', label: 'Medya & Foto Yükle', icon: 'preview', fallbackEmoji: '📸' }
  ];

  return (
    <div
      className="fixed inset-0 z-[99999] bg-slate-900/80 backdrop-blur-md flex justify-start transition-opacity duration-300"
      onClick={onClose}
    >
      <div
        onClick={e => e.stopPropagation()}
        className="bg-white dark:bg-brand-card border-r-2 border-amber-500/50 w-[90vw] sm:w-[80vw] max-w-md h-full p-6 space-y-5 overflow-y-auto shadow-2xl flex flex-col justify-between animate-slide-in-left"
      >
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b border-slate-200 dark:border-brand-border/40 pb-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl gold-button flex items-center justify-center font-bold text-xl shadow">
                <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-6 h-6 shrink-0" />
              </div>
              <div>
                <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100">İrem Düğün Sarayı</h3>
                <p className="text-[10px] text-amber-600 dark:text-gold-400 font-bold">Tüm Gezinti Panelleri</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="w-10 h-10 rounded-full bg-slate-100 dark:bg-brand-dark hover:bg-red-500 hover:text-white font-bold flex items-center justify-center transition border"
            >
              ✕
            </button>
          </div>

          <div className="space-y-1 text-xs">
            {drawerItems
            .filter(item => (tabPermissionsState[item.id] || []).includes(activeRole))
            .map(item => (
              <button
                key={item.id}
                onClick={() => { navigateTo(item.id); onClose(); }}
                className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left ${
                  activeTab === item.id ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                }`}
              >
                <ThemeIcon icon={item.icon} fallbackEmoji={item.fallbackEmoji} className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </button>
            ))}

            {(tabPermissionsState['settings'] || []).includes(activeRole) && (
              <div className="pt-2 space-y-1.5 border-t border-slate-200 dark:border-brand-border/40">
                <div className="text-[10px] font-bold text-amber-600 dark:text-gold-400 uppercase tracking-wider px-1">Sistem Ayarları Sub-Menü:</div>
                <button
                  onClick={() => { navigateTo('settings-appearance'); onClose(); }}
                  className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left ${
                    activeTab === 'settings-appearance' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                  }`}
                >
                  <ThemeIcon icon="paint" fallbackEmoji="🎨" className="w-4 h-4 shrink-0" />
                  <span>Görünüm & Tema Ayarları</span>
                </button>
                <button
                  onClick={() => { navigateTo('settings-performance'); onClose(); }}
                  className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left ${
                    activeTab === 'settings-performance' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                  }`}
                >
                  <ThemeIcon icon="zap" fallbackEmoji="⚡" className="w-4 h-4 shrink-0" />
                  <span>Önbellek & Performans</span>
                </button>
                <button
                  onClick={() => { navigateTo('settings-rbac'); onClose(); }}
                  className={`w-full p-2.5 rounded-xl border flex items-center space-x-2.5 transition text-left ${
                    activeTab === 'settings-rbac' ? 'gold-button font-bold' : 'bg-slate-50 dark:bg-brand-dark text-slate-800 dark:text-gray-200 border-slate-200 dark:border-brand-border/40'
                  }`}
                >
                  <span className="text-base">🛡️</span>
                  <span>Rol & İzin Yönetimi</span>
                </button>
              </div>
            )}
          </div>
        </div>

        {/* DRAWER FOOTER */}
        <div className="pt-4 border-t border-slate-200 dark:border-brand-border/40 space-y-2">
          <div className="bg-amber-500/10 p-3 rounded-2xl border border-amber-500/30 flex items-center space-x-3">
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&w=150&q=80" alt="Avatar" className="w-10 h-10 rounded-full border-2 border-amber-500 object-cover" />
            <div className="text-xs">
              <div className="font-bold text-slate-800 dark:text-gray-100">İrem Yılmaz</div>
              <div className="text-[10px] text-amber-700 dark:text-gold-400 font-bold">{ROLE_NAMES[activeRole]}</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
