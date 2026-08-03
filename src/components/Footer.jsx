import React from 'react';
import { ThemeIcon } from './ThemeIcon';

export function GlobalFooterComponent({ onNavigate, activeRole, campaigns = [], showToast, onOpenVersionModal, systemVersion = 'v1.5.30' }) {
  const activeCampaign = campaigns.length > 0 ? campaigns[0] : { title: 'Erken Rezervasyon Fırsatı', code: 'IREM2026', discount: '%20 İndirim' };
  const currentYear = new Date().getFullYear();

  return (
    <footer className="w-full m-0 mt-0 border-t border-slate-200 dark:border-brand-border/60 glass-panel rounded-none px-4 sm:px-8 py-8 space-y-8 animate-fade-in relative overflow-hidden">
      {/* BACKGROUND DECORATIVE GLOW */}
      <div className="absolute -top-24 -right-24 w-72 h-72 bg-amber-500/10 dark:bg-amber-500/5 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute -bottom-24 -left-24 w-72 h-72 bg-blue-500/10 dark:bg-blue-500/5 rounded-full blur-3xl pointer-events-none"></div>

      {/* MAIN 4-COLUMN FOOTER GRID */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 relative z-10">

        {/* COLUMN 1: CORPORATE INTRO & BRAND */}
        <div className="space-y-4">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white shadow-md shrink-0">
              <ThemeIcon icon="crown" fallbackEmoji="👑" className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-heading font-extrabold text-base text-slate-900 dark:text-gray-100 gold-gradient-text">
                İrem Düğün Sarayı
              </h3>
              <p className="text-[10px] font-mono text-slate-500 dark:text-gray-400 uppercase tracking-widest">
                Balo & Etkinlik Tesisleri
              </p>
            </div>
          </div>

          <p className="text-xs text-slate-600 dark:text-gray-300 leading-relaxed">
            15 yılı aşkın tecrübemiz ve 4 farklı konsept balo salonumuzla hayatınızın en özel ve unutulmaz anlarını kusursuz bir şölene dönüştürüyoruz.
          </p>

          <button
            type="button"
            onClick={onOpenVersionModal}
            className="inline-flex items-center space-x-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-600 dark:text-emerald-400 text-[11px] font-bold hover:bg-emerald-500/20 transition cursor-pointer"
            title="Sistem Sürüm Geçmişi ve Güncelleme Günlüğünü Göster"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span>Canlı Sistem ({systemVersion}) (Sürüm Notları 📋)</span>
          </button>
        </div>

        {/* COLUMN 2: QUICK NAVIGATION & IMPORTANT LINKS */}
        <div className="space-y-3">
          <h4 className="font-heading font-extrabold text-xs text-slate-900 dark:text-gray-100 uppercase tracking-wider flex items-center space-x-2 border-b pb-2 border-slate-200 dark:border-brand-border/40">
            <ThemeIcon icon="star" fallbackEmoji="⭐" className="w-4 h-4 text-amber-500 shrink-0" />
            <span>Önemli Bağlantılar</span>
          </h4>

          <ul className="space-y-2 text-xs font-semibold text-slate-600 dark:text-gray-300">
            <li>
              <button onClick={() => onNavigate && onNavigate('dashboard')} className="hover:text-amber-600 dark:hover:text-gold-400 transition flex items-center space-x-2">
                <span>›</span>
                <span>Anasayfa & Genel Bakış</span>
              </button>
            </li>
            <li>
              <button onClick={() => onNavigate && onNavigate('venues')} className="hover:text-amber-600 dark:hover:text-gold-400 transition flex items-center space-x-2">
                <span>›</span>
                <span>Balo Salonlarımız & Kapasiteler</span>
              </button>
            </li>
            <li>
              <button onClick={() => onNavigate && onNavigate('calendar')} className="hover:text-amber-600 dark:hover:text-gold-400 transition flex items-center space-x-2">
                <span>›</span>
                <span>Etkinlik Takvimi & Doluluk</span>
              </button>
            </li>
            <li>
              <button onClick={() => onNavigate && onNavigate('campaigns')} className="hover:text-amber-600 dark:hover:text-gold-400 transition flex items-center space-x-2">
                <span>›</span>
                <span>Sezon Kampanyaları & AI Önerileri</span>
              </button>
            </li>
            <li>
              <button onClick={() => onNavigate && onNavigate('customers')} className="hover:text-amber-600 dark:hover:text-gold-400 transition flex items-center space-x-2">
                <span>›</span>
                <span>Müşteri Portalı & Rehber</span>
              </button>
            </li>
          </ul>
        </div>

        {/* COLUMN 3: DYNAMIC PROMOTION & CAMPAIGN BANNER */}
        <div className="space-y-3">
          <h4 className="font-heading font-extrabold text-xs text-slate-900 dark:text-gray-100 uppercase tracking-wider flex items-center space-x-2 border-b pb-2 border-slate-200 dark:border-brand-border/40">
            <ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-4 h-4 text-amber-500 shrink-0" />
            <span>Aktif Sezon Kampanyası</span>
          </h4>

          <div className="p-4 rounded-2xl bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-transparent border border-amber-500/30 space-y-2.5 shadow-sm">
            <div className="flex justify-between items-center">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest px-2 py-0.5 rounded-full bg-amber-500 text-slate-950">
                Özel Fırsat
              </span>
              <span className="text-xs font-black text-amber-600 dark:text-gold-400 font-mono">
                {activeCampaign.code || 'IREM2026'}
              </span>
            </div>

            <div className="font-bold text-xs text-slate-900 dark:text-gray-100">
              {activeCampaign.title || '2026 Erken Rezervasyon İndirimi'}
            </div>

            <p className="text-[11px] text-slate-600 dark:text-gray-400">
              Rezervasyon formunda kampanya kodunu girerek %20 indirimden anında faydalanın.
            </p>

            <button
              onClick={() => onNavigate && onNavigate('create-reservation')}
              className="w-full text-center py-2 px-3 rounded-xl gold-button font-bold text-xs shadow hover:scale-[1.02] transition"
            >
              Hemen Rezervasyon Oluştur →
            </button>
          </div>
        </div>

        {/* COLUMN 4: DIRECT CONTACT & EMERGENCY SUPPORT */}
        <div className="space-y-3">
          <h4 className="font-heading font-extrabold text-xs text-slate-900 dark:text-gray-100 uppercase tracking-wider flex items-center space-x-2 border-b pb-2 border-slate-200 dark:border-brand-border/40">
            <ThemeIcon icon="phone" fallbackEmoji="📞" className="w-4 h-4 text-amber-500 shrink-0" />
            <span>İletişim & Canlı Destek</span>
          </h4>

          <ul className="space-y-2.5 text-xs text-slate-600 dark:text-gray-300">
            <li className="flex items-start space-x-2">
              <span className="text-amber-500 shrink-0">📍</span>
              <span>Sapanca Balo Tesisleri, Sakarya / Türkiye</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="text-amber-500 shrink-0">📞</span>
              <span className="font-mono font-bold text-slate-800 dark:text-gray-200">0850 555 0 777</span>
            </li>
            <li className="flex items-center space-x-2">
              <span className="text-amber-500 shrink-0">✉️</span>
              <span className="font-mono">iletisim@iremdugunsarayi.com</span>
            </li>
          </ul>

          <a
            href="https://wa.me/905320000000"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full flex items-center justify-center space-x-2 py-2 px-3 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition hover:scale-[1.02]"
          >
            <span>💬 WhatsApp Canlı Destek Line</span>
          </a>
        </div>

      </div>

      {/* SUB-FOOTER COPYRIGHT BAR */}
      <div className="pt-6 border-t border-slate-200 dark:border-brand-border/40 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs text-slate-500 dark:text-gray-400 relative z-10">
        <div>
          © {currentYear} <strong>İrem Düğün Sarayı & Balo Tesisleri</strong>. Tüm Hakları Saklıdır.
        </div>

        <div className="flex items-center space-x-4 font-semibold text-[11px]">
          <button onClick={() => onNavigate && onNavigate('settings-appearance')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Görünüm Ayarları</button>
          <span>•</span>
          <button onClick={onOpenVersionModal} className="hover:text-amber-600 dark:hover:text-gold-400 transition font-bold text-amber-600 dark:text-gold-400">📋 Sistem Sürüm Geçmişi (v1.3.0)</button>
          <span>•</span>
          <button onClick={() => showToast && showToast('🛡️ Gizlilik ve Güvenlik Sözleşmesi Onaylıdır')} className="hover:text-amber-600 dark:hover:text-gold-400 transition">Gizlilik Politikası</button>
        </div>
      </div>
    </footer>
  );
}
