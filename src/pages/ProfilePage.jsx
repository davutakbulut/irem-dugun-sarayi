import React, { useState, useEffect, useRef } from 'react';
import { formatPhoneNumber } from '../utils/formatters.js';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function ProfileComponent({ currentUser, activeRole, onSaveProfile, showToast, onRoleChange }) {
      const [name, setName] = useState(currentUser?.name || 'Davut Akbulut');
      const [email, setEmail] = useState(currentUser?.email || 'davut@iremdugunsarayi.com');
      const [phone, setPhone] = useState(currentUser?.phone || '+90 532 123 4567');
      const [avatar, setAvatar] = useState(currentUser?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80');
      const [password, setPassword] = useState('');
      const [selectedRole, setSelectedRole] = useState(activeRole);

      const [notifyWhatsapp, setNotifyWhatsapp] = useState(true);
      const [notifyEmail, setNotifyEmail] = useState(true);
      const [notifySms, setNotifySms] = useState(false);

      const handleSave = (e) => {
        e.preventDefault();
        onSaveProfile({
          name,
          email,
          phone,
          avatar,
          role: selectedRole
        });
        if (selectedRole !== activeRole && onRoleChange) {
          onRoleChange(selectedRole);
        }
        showToast('👤 Profil ve Hesap Bilgileriniz Başarıyla Güncellendi!');
      };

      const isAdmin = activeRole === 'admin';

      return (
        <div className="max-w-4xl mx-auto space-y-6 animate-fade-in pb-12">
          {/* HEADER */}
          <div className="glass-panel p-6 rounded-3xl border border-amber-500/30 flex flex-col sm:flex-row justify-between items-center gap-4 shadow-sm">
            <div className="flex items-center space-x-4">
              <OptimizedImage src={avatar} alt={name} className="w-16 h-16 rounded-full border-2 border-amber-500/60 shadow" />
              <div>
                <span className="text-[10px] font-bold gold-button px-2.5 py-0.5 rounded-full shadow">
                  {ROLE_NAMES[activeRole]}
                </span>
                <h2 className="text-xl sm:text-2xl font-heading font-extrabold gold-gradient-text mt-1">
                  {name}
                </h2>
                <p className="text-xs text-slate-500 dark:text-gray-400">{email} | {phone}</p>
              </div>
            </div>
          </div>

          <form onSubmit={handleSave} className="glass-panel p-6 rounded-3xl space-y-6 shadow-sm border border-slate-200 dark:border-brand-border/40">
            <h3 className="font-heading font-extrabold text-base text-slate-800 dark:text-gray-100 border-b border-slate-200 dark:border-brand-border/40 pb-3 flex items-center space-x-2">
              <span>👤 Profil & Güvenlik Ayarlarını Düzenle</span>
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Ad Soyad / Unvan:</label>
                <input
                  type="text"
                  value={name}
                  onChange={e => setName(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">E-posta Adresi:</label>
                <input
                  type="email"
                  value={email}
                  onChange={e => setEmail(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                  required
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Telefon Numarası:</label>
                <input
                  type="text"
                  placeholder="0 (5XX) XXX XX XX"
                  value={phone}
                  onChange={e => setPhone(formatPhoneNumber(e.target.value))}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                />
              </div>

              <div className="sm:col-span-2">
                <ImageDropzoneUploader
                  label="Profil Fotoğrafı Yükle"
                  value={avatar}
                  onChange={setAvatar}
                  aspectGuide="400x400 px (1:1 Kare Profil Görseli)"
                  placeholderIcon="👤"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs pt-2 border-t border-slate-100 dark:border-brand-border/40">
              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">Yeni Parola / Güvenlik Şifresi:</label>
                <input
                  type="password"
                  placeholder="Değiştirmek istemiyorsanız boş bırakın..."
                  value={password}
                  onChange={e => setPassword(e.target.value)}
                  className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200"
                />
              </div>

              <div>
                <label className="font-bold text-slate-700 dark:text-gray-300 block mb-1">
                  Sistem Rolü & Yetkileri: {isAdmin ? '(Admin Yetkisi)' : '(Salt Okunur)'}
                </label>
                {isAdmin ? (
                  <select
                    value={selectedRole}
                    onChange={e => setSelectedRole(e.target.value)}
                    className="w-full bg-slate-100 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
                  >
                    <option value="admin">Admin (Tam Yetkili)</option>
                    <option value="satisci">Satış Müdürü (Rezervasyon & Müşteri)</option>
                    <option value="sosyal_medyaci">Sosyal Medya (Fotoğraf & Galeri)</option>
                    <option value="musteri">Müşteri (Özelleştirilmiş Görünüm)</option>
                  </select>
                ) : (
                  <div className="p-2.5 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border text-slate-500 dark:text-gray-400 font-bold">
                    {ROLE_NAMES[activeRole]} — Roller sadece Sistem Yöneticisi (Admin) tarafından değiştirilebilir.
                  </div>
                )}
              </div>
            </div>

            <div className="space-y-2 text-xs pt-2 border-t border-slate-100 dark:border-brand-border/40">
              <label className="font-bold text-slate-800 dark:text-gray-200 block mb-1">🔔 Otomatik Bildirim Tercihleri:</label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <label className="flex items-center space-x-2 cursor-pointer font-bold bg-emerald-500/10 text-emerald-800 dark:text-emerald-300 p-2 rounded-xl border border-emerald-500/20">
                  <input type="checkbox" checked={notifyWhatsapp} onChange={e => setNotifyWhatsapp(e.target.checked)} className="w-4 h-4 accent-[#25D366] rounded" />
                  <ThemeIcon icon="whatsapp" fallbackEmoji="💬" className="w-4 h-4 text-[#25D366] shrink-0" />
                  <span>WhatsApp Bildirimleri</span>
                </label>
                <label className="flex items-center space-x-2 cursor-pointer font-bold">
                  <input type="checkbox" checked={notifyEmail} onChange={e => setNotifyEmail(e.target.checked)} className="w-4 h-4 accent-amber-600 rounded" />
                  <span>E-posta Hatırlatmaları</span>
                </label>
                <label className="flex items-center space-x-2 cursor-pointer font-bold">
                  <input type="checkbox" checked={notifySms} onChange={e => setNotifySms(e.target.checked)} className="w-4 h-4 accent-amber-600 rounded" />
                  <span>SMS Bilgilendirme</span>
                </label>
              </div>
            </div>

            <div className="pt-2 flex justify-end">
              <button type="submit" className="gold-button font-bold px-6 py-3 rounded-2xl text-xs shadow-lg hover:scale-105 transition">
                Değişiklikleri Kaydet ✓
              </button>
            </div>
          </form>
        </div>
      );
    }

    // --- VERSION HISTORY & RELEASE LOG MODAL ---
