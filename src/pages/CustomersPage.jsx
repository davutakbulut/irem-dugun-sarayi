import React, { useState, useEffect, useRef } from 'react';
import { createPortal } from 'react-dom';
import { ThemeIcon } from '../components/ThemeIcon.jsx';

export function CustomersComponent({ customers, onAddClick, onEditClick, onDeleteClick }) {
      const [viewMode, setViewMode] = useState('grid'); // 'grid' | 'table'
      const [searchTerm, setSearchTerm] = useState('');
      const [taxTypeFilter, setTaxTypeFilter] = useState('ALL'); // 'ALL' | 'individual' | 'corporate'

      const filteredCustomers = useMemo(() => {
        return customers.filter(c => {
          const matchesTaxType = taxTypeFilter === 'ALL' || c.taxType === taxTypeFilter;
          const matchesSearch = !searchTerm || (
            c.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.phone?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
            c.tcNo?.includes(searchTerm) ||
            c.vknNo?.includes(searchTerm)
          );
          return matchesTaxType && matchesSearch;
        });
      }, [customers, taxTypeFilter, searchTerm]);

      return (
        <div className="space-y-6">
          {/* HEADER & PRIMARY ACTION */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200 dark:border-brand-border/40">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500 shrink-0">
                <ThemeIcon icon="user" fallbackEmoji="👥" className="w-6 h-6" />
              </div>
              <div>
                <h2 className="text-2xl font-heading font-extrabold text-slate-900 dark:text-gray-100 gold-gradient-text">
                  Müşteri Rehberi
                </h2>
                <p className="text-xs text-slate-500 dark:text-gray-400">
                  Toplam {filteredCustomers.length} kayıtlı müşteri rehberde listeleniyor
                </p>
              </div>
            </div>

            <button onClick={onAddClick} className="gold-button font-bold px-4 py-2.5 rounded-xl text-xs shadow flex items-center justify-center space-x-1.5 self-start sm:self-auto">
              <ThemeIcon icon="user" fallbackEmoji="👤" className="w-4 h-4 shrink-0" />
              <span>Yeni Müşteri Ekle</span>
            </button>
          </div>

          {/* FILTER TOOLBAR & VIEW MODE SWITCHER */}
          <div className="glass-panel p-4 rounded-2xl border border-slate-200 dark:border-brand-border/40 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 shadow-sm">
            
            {/* SEARCH INPUT */}
            <div className="flex-1 relative min-w-[200px]">
              <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-4 h-4" />
              </span>
              <input
                type="text"
                placeholder="Müşteri adı, telefon, e-posta veya TC/VKN no ara..."
                value={searchTerm}
                onChange={e => setSearchTerm(e.target.value)}
                className="w-full pl-9 pr-4 py-2 rounded-xl bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border text-xs text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500 transition"
              />
              {searchTerm && (
                <button onClick={() => setSearchTerm('')} className="absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-slate-600 dark:hover:text-gray-200 text-xs">
                  ✕
                </button>
              )}
            </div>

            {/* TAX TYPE FILTER */}
            <div className="flex items-center space-x-2">
              <span className="text-xs font-bold text-slate-500 dark:text-gray-400 shrink-0">Müşteri Türü:</span>
              <select
                value={taxTypeFilter}
                onChange={e => setTaxTypeFilter(e.target.value)}
                className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl px-3 py-2 text-xs font-bold text-slate-800 dark:text-gray-200 focus:outline-none focus:border-amber-500"
              >
                <option value="ALL">Tümü (Bireysel & Kurumsal)</option>
                <option value="individual">Bireysel Müşteriler</option>
                <option value="corporate">Kurumsal Müşteriler</option>
              </select>
            </div>

            {/* VIEW MODE TOGGLE BUTTONS */}
            <div className="flex items-center p-1 bg-slate-100 dark:bg-brand-dark rounded-xl border border-slate-200 dark:border-brand-border shrink-0 self-end md:self-auto">
              <button
                onClick={() => setViewMode('grid')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                  viewMode === 'grid'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-gray-100'
                }`}
                title="Kart Izgara Görünümü"
              >
                <ThemeIcon icon="grid" fallbackEmoji="🎴" className="w-4 h-4 shrink-0" />
                <span>Kart Görünümü</span>
              </button>
              <button
                onClick={() => setViewMode('table')}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold transition ${
                  viewMode === 'table'
                    ? 'bg-amber-500 text-slate-950 shadow-sm'
                    : 'text-slate-600 dark:text-gray-400 hover:text-slate-900 dark:hover:text-gray-100'
                }`}
                title="Detaylı Tablo Görünümü"
              >
                <ThemeIcon icon="list" fallbackEmoji="📋" className="w-4 h-4 shrink-0" />
                <span>Tablo Görünümü</span>
              </button>
            </div>

          </div>

          {/* CONTENT: GRID MODE vs TABLE MODE */}
          {filteredCustomers.length === 0 ? (
            <div className="glass-panel p-12 text-center rounded-3xl border border-dashed border-slate-300 dark:border-brand-border space-y-3">
              <ThemeIcon icon="search" fallbackEmoji="🔍" className="w-10 h-10 mx-auto text-slate-400 opacity-60" />
              <div className="font-bold text-slate-700 dark:text-gray-300 text-sm">Aramanızla Eşleşen Müşteri Bulunamadı</div>
              <p className="text-xs text-slate-500 dark:text-gray-400">Filtre kriterlerinizi temizleyerek tekrar arayabilirsiniz.</p>
              <button onClick={() => { setSearchTerm(''); setTaxTypeFilter('ALL'); }} className="px-4 py-2 rounded-xl bg-amber-500/10 text-amber-600 font-bold text-xs border border-amber-500/30">
                Filtreleri Temizle
              </button>
            </div>
          ) : viewMode === 'grid' ? (
            /* --- KART IZGARA GÖRÜNÜMÜ --- */
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {filteredCustomers.map(c => (
                <div key={c.id} className="glass-panel p-5 rounded-2xl flex items-start space-x-4 shadow-sm border border-slate-200 dark:border-brand-border/40 hover:border-amber-500/50 transition">
                  <img src={c.avatar} alt={`${c.name} Avatarı`} className="w-14 h-14 rounded-2xl object-cover border border-amber-500/40 shrink-0" />
                  <div className="flex-1 space-y-2">
                    <div className="flex justify-between items-start">
                      <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">{c.name}</h3>
                      <div className="flex space-x-1.5 items-center">
                        <button onClick={() => onEditClick(c)} className="text-[11px] text-amber-700 dark:text-gold-400 font-bold bg-amber-500/10 px-2.5 py-1 rounded-lg border border-amber-500/30 flex items-center space-x-1 hover:bg-amber-500/20 transition">
                          <span>Düzenle</span>
                          <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                        </button>
                        <button onClick={() => onDeleteClick(c.id)} className="px-2.5 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-xs uppercase border border-red-500/30 inline-flex items-center space-x-1.5 transition shadow-2xs">
                          <span>SİL</span>
                          <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                        </button>
                      </div>
                    </div>
                    <div className="text-xs text-slate-500 dark:text-gray-400">{c.phone} | {c.email}</div>
                    <div className="text-[11px] text-slate-600 dark:text-gray-400">
                      <span className="font-bold text-amber-600 dark:text-gold-400 inline-flex items-center space-x-1">
                        {c.taxType === 'corporate' ? (
                          <>
                            <ThemeIcon icon="briefcase" fallbackEmoji="🏢" className="w-3.5 h-3.5 shrink-0" />
                            <span>Kurumsal</span>
                          </>
                        ) : (
                          <>
                            <ThemeIcon icon="user" fallbackEmoji="👤" className="w-3.5 h-3.5 shrink-0" />
                            <span>Bireysel</span>
                          </>
                        )}
                      </span>
                      <span> - </span>
                      <span>{c.taxType === 'corporate' ? `VKN: ${c.vknNo || c.tcNo || '-'}` : `TC: ${c.tcNo || '-'}`} ({c.taxOffice || 'Sapanca VD'})</span>
                    </div>
                    <div className="pt-1">
                      <WhatsAppButton phone={c.phone} customerName={c.name} />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            /* --- TABLO GÖRÜNÜMÜ --- */
            <div className="glass-panel rounded-3xl border border-slate-200 dark:border-brand-border/40 overflow-hidden shadow-sm">
              <div className="overflow-x-auto custom-scrollbar">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-200 dark:border-brand-border/60 bg-slate-50/80 dark:bg-brand-dark/80 text-[11px] font-extrabold text-slate-500 dark:text-gray-400 uppercase tracking-wider">
                      <th className="py-3.5 px-4">Müşteri</th>
                      <th className="py-3.5 px-4">İletişim Bilgileri</th>
                      <th className="py-3.5 px-4">Müşteri Türü & Kimlik / Vergi No</th>
                      <th className="py-3.5 px-4">Vergi Dairesi & Adres</th>
                      <th className="py-3.5 px-4 text-right">Aksiyonlar</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 dark:divide-brand-border/30 text-xs font-semibold text-slate-700 dark:text-gray-200">
                    {filteredCustomers.map(c => (
                      <tr key={c.id} className="hover:bg-amber-500/5 transition">
                        <td className="py-3 px-4">
                          <div className="flex items-center space-x-3">
                            <img src={c.avatar} alt={c.name} className="w-9 h-9 rounded-xl object-cover border border-amber-500/30 shrink-0" />
                            <div>
                              <div className="font-bold text-slate-900 dark:text-gray-100">{c.name}</div>
                              <div className="text-[10px] text-slate-400">ID: #{c.id}</div>
                            </div>
                          </div>
                        </td>
                        <td className="py-3 px-4">
                          <div className="font-mono text-slate-800 dark:text-gray-200 font-bold">{c.phone}</div>
                          <div className="text-[11px] text-slate-500 dark:text-gray-400">{c.email}</div>
                        </td>
                        <td className="py-3 px-4">
                          <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full inline-flex items-center space-x-1 ${
                            c.taxType === 'corporate'
                              ? 'bg-blue-500/10 text-blue-600 dark:text-blue-400 border border-blue-500/20'
                              : 'bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20'
                          }`}>
                            {c.taxType === 'corporate' ? (
                              <>
                                <ThemeIcon icon="briefcase" fallbackEmoji="🏢" className="w-3 h-3 shrink-0" />
                                <span>Kurumsal</span>
                              </>
                            ) : (
                              <>
                                <ThemeIcon icon="user" fallbackEmoji="👤" className="w-3 h-3 shrink-0" />
                                <span>Bireysel</span>
                              </>
                            )}
                          </span>
                          <div className="text-[11px] font-mono text-slate-600 dark:text-gray-300 mt-1">
                            {c.taxType === 'corporate' ? `VKN: ${c.vknNo || '-'}` : `TC: ${c.tcNo || '-'}`}
                          </div>
                        </td>
                        <td className="py-3 px-4 text-slate-500 dark:text-gray-400">
                          <div>{c.taxOffice || 'Sapanca VD'}</div>
                          <div className="text-[10px] truncate max-w-xs">{c.address || 'Sakarya / Sapanca'}</div>
                        </td>
                        <td className="py-3 px-4 text-right">
                          <div className="flex items-center justify-end space-x-1.5">
                            <WhatsAppButton phone={c.phone} customerName={c.name} />
                            <button
                              onClick={() => onEditClick(c)}
                              className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-800 dark:text-gold-400 font-bold text-[11px] border border-amber-500/30 hover:bg-amber-500/20 transition flex items-center space-x-1"
                              title="Müşteri Bilgilerini Düzenle"
                            >
                              <ThemeIcon icon="edit" fallbackEmoji="✏️" className="w-3 h-3 shrink-0" />
                            </button>
                            <button
                              onClick={() => onDeleteClick(c.id)}
                              className="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-600 text-red-600 dark:text-red-400 hover:text-white font-extrabold text-[11px] border border-red-500/30 transition flex items-center justify-center"
                              title="Müşteriyi Sil"
                            >
                              <ThemeIcon icon="trash" fallbackEmoji="🗑️" className="w-3.5 h-3.5 shrink-0" />
                            </button>
                          </div>
                  </td>
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

// --- MIND MAP COMPONENT & INTERACTIVE SYSTEM TOPOLOGY ---

// COMPREHENSIVE MIND MAP NODE DATA WITH STATE DEPENDENCIES & CONNECTED NODES
const MIND_MAP_DATA = [
  {
    id: 'core-arch',
    title: 'Core Mimari & Altyapı',
    icon: 'sparkles',
    fallbackEmoji: '🏗️',
    category: 'Architecture',
    color: 'from-amber-500 to-amber-600',
    borderColor: 'border-amber-500',
    bgColor: 'bg-amber-500/10',
    summary: 'Çift mimarili senkronizasyon, otomatik taslak kaydı ve Toast notification altyapısı.',
    whatItDoes: 'İrem Düğün Sarayı dijital yönetim platformunun temel teknik ve mimari omurgasını oluşturur.',
    connectedNodes: ['page-dashboard', 'theme-iconography', 'page-create-reservation', 'page-rbac-settings'],
    readsState: ['activeRole', 'currentTheme', 'draftReservations', 'systemLogs'],
    mutatesState: ['draftReservations', 'systemLogs', 'alertModal'],
    whichFeatures: [
      'Dual-Architecture Sync (Monolitik index.html + Modüler React src/ yapısı)',
      'Otomatik Taslak Kaydı Engine (draftReservations & refKey ile kaldığı yerden devam etme)',
      'Global Standalone Toast Notification System (Sağ üst kayar bildirim popupı)',
      'Error Page Guard (Hata simülasyonlarında header & sidebar gizleme kuralı)',
      'LocalStorage Caching & Persistence Engine'
    ],
    whyWeBuiltIt: 'Platformun hem hızlı prototipleme için tek dosyadan çalışabilmesini hem de kurumsal ölçeklenebilirlik için modüler ES2022 Standartlarında kalmasını sağlamak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: Yapılan her UI ve mantık güncellemesi hem index.html hem de src/ bileşenlerinde %100 birebir senkronize edilmelidir.',
      'Kural 2: Hatalı veya eksik veri durumunda asla uygulama çökmemeli, null-safe optional chaining kullanılmalıdır.',
      'Kural 3: Formlar doldurulurken her adımda arka planda draftReservations güncellenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı sisteme girer, LocalStorage önbelleği ve varsayılan durumlar yüklenir.',
      '2. Adım: Herhangi bir işlem yapıldığında (ör. form doldurma) taslak motoru canlı tetiklenir.',
      '3. Adım: Başarılı işlemlerde global Toast popupı kullanıcıya anında geri bildirim verir.'
    ],
    relatedRoute: 'dashboard'
  },
  {
    id: 'theme-iconography',
    title: 'Tema Mimarisi & İkonografi',
    icon: 'sparkles',
    fallbackEmoji: '🎨',
    category: 'UI/UX System',
    color: 'from-blue-500 to-indigo-600',
    borderColor: 'border-blue-500',
    bgColor: 'bg-blue-500/10',
    summary: '5 Kurumsal Tema ve Emojisiz İkon Kuralları (ThemeIcon & NordicSvgMap).',
    whatItDoes: 'Tüm uygulamanın renk paletlerini, tipografisini, buton keskinliklerini ve minimalist ikon setlerini yönetir.',
    connectedNodes: ['core-arch', 'page-dashboard', 'page-create-reservation', 'page-finance'],
    readsState: ['currentTheme'],
    mutatesState: ['currentTheme'],
    whichFeatures: [
      '5 Kurumsal Tema: Nordic Light, Elite Luxury, Obsidian Gold, Sapphire Clean, Emerald Royal',
      'Nordic Light Temasında SIFIR EMOJİ KURALI (Tüm emojiler SVG vektör ikonlara dönüşür)',
      'ThemeIcon Bileşeni & NordicSvgMap Vektör Haritası (52+ Özel SVG İkon)',
      'Responsive Sticky Navigation (sticky top-0 h-[calc(100vh-105px)] kaydırma mimarisi)'
    ],
    whyWeBuiltIt: 'Kullanıcılara modern, lüks ve göz yormayan kurumsal bir deneyim sunmak; Nordic temasında emojiler yerine premium minimalist SVG ikonlar hissettirmek için tasarladık.',
    rulesAndCore: [
      'Kural 1: Nordic Light teması seçiliyken sayfada ham emoji görünmesi YASAKTIR. Tüm ikonlar <ThemeIcon /> ile sarmalanmalıdır.',
      'Kural 2: Tema değiştiğinde HTML data-ui-theme niteliği anında güncellenmeli ve CSS CSS-variables ile renkleri yenilemelidir.',
      'Kural 3: Sidebar ve Header menüleri ekran boyutu ne olursa olsun kırpılmamalı, kendi içinde kaymalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı Ayarlar > Görünüm sekmesinden veya header tema butonundan tema seçer.',
      '2. Adım: Uygulama data-ui-theme etiketini değiştirir ve ThemeIcon bileşenleri SVG haritasını günceller.',
      '3. Adım: Nordic temasında tüm ham emojiler minimalist siyah/gri vektör ikonlara dönüşür.'
    ],
    relatedRoute: 'settings-appearance'
  },
  {
    id: 'page-dashboard',
    title: 'Dashboard (Genel Bakış)',
    icon: 'chart',
    fallbackEmoji: '📊',
    category: 'Pages',
    color: 'from-emerald-500 to-teal-600',
    borderColor: 'border-emerald-500',
    bgColor: 'bg-emerald-500/10',
    summary: 'Canlı KPI kartları, yaklaşan düğünler, hızlı işlem barı ve sistem durumu.',
    whatItDoes: 'İşletmenin tüm anlık durumunu, cirosunu, yaklaşan organizasyonlarını tek bakışta özetler.',
    connectedNodes: ['page-create-reservation', 'page-reservations', 'page-finance', 'page-reports-ai'],
    readsState: ['reservations', 'venues', 'services', 'customers', 'campaigns'],
    mutatesState: [],
    whichFeatures: [
      'Canlı KPI Kartları: Bu Ayki Toplam Ciro, Onaylı Düğün Sayısı, Bekleyen Taslaklar, Doluluk Oranı',
      'Yaklaşan Organizasyonlar Listesi & Hızlı Detay Önizleme',
      'Hızlı Kısayol Butonları: Yeni Rezervasyon, Kasa Ekleme, Fatura Kes',
      'AI Öneri Kartı: Doluluk analizi ve tek tıkla aksiyon önerisi'
    ],
    whyWeBuiltIt: 'Salon yöneticisinin ve resepsiyon görevlisinin güne başlarken tüm kritik verileri tek ekranda görmesini sağlamak için inşa ettik.',
    rulesAndCore: [
      'Kural 1: Ciro ve doluluk sayıları statik olmamalı, reservations dizisinden canlı hesaplanmalıdır.',
      'Kural 2: Yaklaşan etkinliklerde müşteri adı, tarih ve seans bilgisi eksiksiz görünmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Kullanıcı sisteme girince varsayılan olarak Dashboard açılır.',
      '2. Adım: KPI kartları anlık rezervasyon durumlarını hesaplar.',
      '3. Adım: Hızlı butonlar üzerinden doğrudan rezervasyon veya finans sayfasına geçilir.'
    ],
    relatedRoute: 'dashboard'
  },
  {
    id: 'page-create-reservation',
    title: 'Rezervasyon Oluşturma (Wizard)',
    icon: 'calendar',
    fallbackEmoji: '📝',
    category: 'Pages',
    color: 'from-purple-500 to-pink-600',
    borderColor: 'border-purple-500',
    bgColor: 'bg-purple-500/10',
    summary: '6 adımlı canlı sözleşme ve rezervasyon sihirbazı, otomatik taslak kaydı.',
    whatItDoes: 'Yeni düğün/etkinlik sözleşmesi oluşturur, müşteri bilgilerini, ek hizmetleri, kaporayı ve özel istekleri kaydeder.',
    connectedNodes: ['page-reservations', 'page-calendar', 'page-finance', 'page-customers', 'page-campaigns'],
    readsState: ['venues', 'services', 'customers', 'campaigns', 'draftReservations'],
    mutatesState: ['reservations', 'customers', 'draftReservations'],
    whichFeatures: [
      '6 Adımlı Süreç: Müşteri Seçimi -> Salon/Tarih -> Ek Hizmetler -> Kampanya/İskonto -> Finans/Kapora -> Akış Planı',
      'Anlık Fatura & Sözleşme Hesaplama Motoru (KDV, Kapora, Kalan Bakiye)',
      'Otomatik Taslak Kaydı (RefKey bazlı taslak saklama)',
      'Dinamik Kampanya İndirimi Hesaplayıcı (campaigns dizisinde indirim kodunu tarama)'
    ],
    whyWeBuiltIt: 'Karmaşık düğün organizasyonu sözleşmelerini hatasız, hızlı ve 6 adımda adımlar arası taslak kaydı kaybedilmeden tamamlayabilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Giriş yapılan kampanya kodu canlı doğrulanmalı ve toplam tutardan düşmelidir.',
      'Kural 2: Müşteri adı veya salon seçilmediğinde sözleşme tamamlanamaz.',
      'Kural 3: Başarılı kayıtta müşteri rehberine ve rezervasyon listesine eşzamanlı eklenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Müşteri bilgileri girilir veya var olan rehberden seçilir.',
      '2. Adım: Salon, düğün tarihi ve seans (Gündüz/Gece) seçilir.',
      '3. Adım: Menü, Orkestra, Fotoğraf gibi ek hizmetler eklenir ve kampanya indirim kodu uygulanır.',
      '4. Adım: Alınan kapora yazılır, sözleşme onaylanır ve rezervasyon oluşturulur.'
    ],
    relatedRoute: 'create-reservation'
  },
  {
    id: 'page-reservations',
    title: 'Rezervasyon Listesi & Sözleşmeler',
    icon: 'user',
    fallbackEmoji: '📋',
    category: 'Pages',
    color: 'from-cyan-500 to-blue-600',
    borderColor: 'border-cyan-500',
    bgColor: 'bg-cyan-500/10',
    summary: 'Tüm onaylı ve taslak sözleşmelerin listelenmesi, filtreleme ve yazdırılabilir fatura.',
    whatItDoes: 'Geçmiş ve gelecek tüm düğün kayıtlarını arama, durum bazlı filtreleme ve resmi sözleşme çıktısı alma imkanı sunar.',
    connectedNodes: ['page-create-reservation', 'page-calendar', 'page-finance', 'page-reports-ai'],
    readsState: ['reservations', 'venues', 'customers', 'services'],
    mutatesState: ['reservations'],
    whichFeatures: [
      'Arama & Filtreleme (Sözleşme No, Müşteri Adı, Salon, Tarih Aralığı)',
      'Fatura & Resmi Sözleşme Yazdırma Modalı (A4 Formatlı Print View)',
      'Sözleşme Düzenleme & İptal Etme / Silme (RedAlert Güvenlik Onayı)',
      'Tarih / Seans Değiştirme (Reschedule Engine)'
    ],
    whyWeBuiltIt: 'Salon resepsiyonunun sözleşmeleri tek tıkla arayıp bulması ve müşteriye anında yazdırılabilir çıktı sunması için tasarladık.',
    rulesAndCore: [
      'Kural 1: İptal edilen rezervasyonlar silinmeden önce onay modalı çıkarılmalıdır.',
      'Kural 2: Yazdır butonuna basıldığında A4 formatında temiz fatura şablonu üretilmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Rezervasyonlar listesinden ilgili sözleşme bulunur.',
      '2. Adım: "Yazdır" butonuna basılarak resmi PDF/A4 sözleşme çıktısı alınır.',
      '3. Adım: Gerekirse "Tarih Değiştir" veya "Düzenle" ile kayıt güncellenir.'
    ],
    relatedRoute: 'reservations'
  },
  {
    id: 'page-calendar',
    title: 'Dinamik Takvim Yönetimi',
    icon: 'calendar',
    fallbackEmoji: '📅',
    category: 'Pages',
    color: 'from-amber-500 to-orange-600',
    borderColor: 'border-amber-500',
    bgColor: 'bg-amber-500/10',
    summary: 'Aylık/Haftalık görsel düğün takvimi, sürükle-bırak tarih değiştirme.',
    whatItDoes: 'Düğün salonlarının hangi gün ve hangi saat diliminde (Gündüz/Gece) dolu olduğunu takvim üzerinde gösterir.',
    connectedNodes: ['page-create-reservation', 'page-reservations', 'page-venues'],
    readsState: ['reservations', 'venues'],
    mutatesState: ['reservations'],
    whichFeatures: [
      'Dinamik Ay Navigasyonu (Önceki Ay / Bugün / Sonraki Ay)',
      'Salon Bazlı Renkli Etiketleme (Altın Salon, Balo Salonu, vb.)',
      'Boş Gün Tıklaması ile Hızlı Rezervasyon Başlatma',
      'Düğün Günü Detay Popupı (Müşteri, Misafir Sayısı, Kalan Bakiye)'
    ],
    whyWeBuiltIt: 'Müşteriler telefonla tarih sorduğunda hangi salonun ne zaman boş olduğunu saniyeler içinde görebilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Çift rezervasyon (çakışma) durumunda takvim günü kırmızı uyarı vermelidir.',
      'Kural 2: Takvim dinamik ay gün sayısı ve ilk gün indisini doğru hesaplamalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Takvimden aranılan ay ve yıla geçilir.',
      '2. Adım: İlgili güne tıklanarak kayıtlı düğün detayları incelenir.',
      '3. Adım: Boş bir güne tıklanarak doğrudan rezervasyon sihirbazı başlatılır.'
    ],
    relatedRoute: 'calendar'
  },
  {
    id: 'page-finance',
    title: 'Finans & Kasa Yönetimi',
    icon: 'finance',
    fallbackEmoji: '💰',
    category: 'Pages',
    color: 'from-emerald-600 to-green-700',
    borderColor: 'border-emerald-600',
    bgColor: 'bg-emerald-600/10',
    summary: 'Gelir/Gider tablosu, net kar hesabı, harcama kaydı ekleme modalı.',
    whatItDoes: 'Düğün kaporalarını, kalan tahsilatları ve orkestra/ikram/personel giderlerini tek kasada yönetir.',
    connectedNodes: ['page-reservations', 'page-reports-ai', 'page-dashboard'],
    readsState: ['reservations', 'financialStats'],
    mutatesState: ['financialStats'],
    whichFeatures: [
      'KPI Kartları: Toplam Ciro, Toplam Gider, Net Kar (Ciro - Gider), Tahsil Edilen Kapora',
      'Birleşik Gelir & Gider İşlem Tablosu (Tarih, Açıklama, Kategori, Tür, Tutar, Durum)',
      'Canlı Arama & Filtreleme (Tümü / Gelirler (+) / Giderler (-))',
      '+ Gider Kaydı Ekle Modalı (Harcama başlığı, Kategori, Tutar, Tarih, Ödeme Durumu)'
    ],
    whyWeBuiltIt: 'Düğün salonunun anlık nakit akışını, kaporaları ve organizasyon maliyetlerini şeffaf şekilde takip etmek için kurduk.',
    rulesAndCore: [
      'Kural 1: Net Kar = Toplam Ciro - Toplam Gider formülüyle canlı hesaplanmalıdır.',
      'Kural 2: Yeni gider eklendiğinde finansal göstergeler anında güncellenmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Finans sayfasına girilir, anlık ciro ve gider görülür.',
      '2. Adım: "+ Gider Kaydı Ekle" butonuna basılarak orkestra veya ikram harcaması yazılır.',
      '3. Adım: Net kar göstergesi otomatik güncellenir.'
    ],
    relatedRoute: 'finans'
  },
  {
    id: 'page-reports-ai',
    title: 'Raporlar & AI Analytics',
    icon: 'chart',
    fallbackEmoji: '📈',
    category: 'Pages',
    color: 'from-violet-500 to-purple-700',
    borderColor: 'border-violet-500',
    bgColor: 'bg-violet-500/10',
    summary: 'SVG grafikleri, dinamik doluluk oranları ve Tek Tıkla Kampanya Dönüştürme.',
    whatItDoes: 'Rezervasyon verilerini analiz eder, SVG Gelir ve Salon grafikleri üretir, AI tavsiyeleri sunar.',
    connectedNodes: ['page-finance', 'page-campaigns', 'page-dashboard'],
    readsState: ['reservations', 'venues', 'services'],
    mutatesState: ['campaigns', 'venues'],
    whichFeatures: [
      'Dinamik Doluluk Oranı Hesabı (occupancyRate)',
      'Donut SVG Gelir Dağılımı Grafiği Kartı',
      'Bar SVG Salon Tercih Oranları Grafiği Kartı',
      'AI Öneri Kartları ("Tek Tıkla Kampanyaya Dönüştür" ve "Fiyat Güncelle & Uygula")'
    ],
    whyWeBuiltIt: 'Yapay zekanın boş günleri tespit edip salon sahibine stratejik kampanya ve fiyat önerileri sunması için tasarladık.',
    rulesAndCore: [
      'Kural 1: "Tek Tıkla Kampanyaya Dönüştür" butonuna tıklandığında kampanya anında eklenmeli ve Kampanyalar sayfasına yönlendirilmelidir.',
      'Kural 2: Grafikler CSS/SVG ile responsive olarak çizilmelidir.'
    ],
    stepByStepFlow: [
      '1. Adım: Raporlar sayfasına girilir, grafikler ve doluluk incelenir.',
      '2. Adım: AI öneri kartındaki "Kampanyaya Dönüştür" butonuna basılır.',
      '3. Adım: Otomatik olarak Kampanyalar sayfasına yeni indirim kodu tanımlanır.'
    ],
    relatedRoute: 'raporlar-ai'
  },
  {
    id: 'page-campaigns',
    title: 'Kampanyalar & AI İndirimler',
    icon: 'sparkles',
    fallbackEmoji: '🏷️',
    category: 'Pages',
    color: 'from-rose-500 to-pink-600',
    borderColor: 'border-rose-500',
    bgColor: 'bg-rose-500/10',
    summary: 'İndirim kodları, erken rezervasyon kampanyaları ve AI önerili promosyonlar.',
    whatItDoes: 'Rezervasyon sırasında uygulanabilecek indirim kodlarını ve şartlarını yönetir.',
    connectedNodes: ['page-reports-ai', 'page-create-reservation'],
    readsState: ['campaigns'],
    mutatesState: ['campaigns'],
    whichFeatures: [
      'Aktif & Pasif Kampanya Listesi (İndirim Oranı, Son Geçerlilik Tarihi)',
      'Yeni Kampanya Tanımlama Modalı',
      'AI Otomatik Üretilmiş Kampanya Rozeti'
    ],
    whyWeBuiltIt: 'Düğün sezonu dışı aylarda ve hafta içi günlerde doluluk oranını artıracak esnek kampanyalar oluşturabilmek için tasarladık.',
    rulesAndCore: [
      'Kural 1: Süresi geçen veya pasif olan kampanyalar rezervasyon sihirbazında uygulanamaz.'
    ],
    stepByStepFlow: [
      '1. Adım: Kampanyalar sayfasından indirim kodu ve geçerlilik tarihi oluşturulur.',
      '2. Adım: Rezervasyon oluştururken müşteriye bu kod uygulanır.'
    ],
    relatedRoute: 'kampanyalar'
  },
  {
    id: 'page-venues',
    title: 'Düğün Salonları Yönetimi',
    icon: 'venue',
    fallbackEmoji: '🏰',
    category: 'Pages',
    color: 'from-yellow-600 to-amber-700',
    borderColor: 'border-yellow-600',
    bgColor: 'bg-yellow-600/10',
    summary: 'Salon kapasiteleri, paket fiyatları, görseller ve detay modalı.',
    whatItDoes: 'İşletmeye ait tüm düğün ve balo salonlarının özelliklerini ve görsellerini sergiler.',
    connectedNodes: ['page-create-reservation', 'page-calendar', 'page-reports-ai'],
    readsState: ['venues'],
    mutatesState: ['venues'],
    whichFeatures: [
      'Salon Kartları (Kapasite, Paket Fiyatı, Alan m²)',
      'Salon Detay Modalı (selectedVenueDetail ile zengin açıklama & galeri)',
      'Yeni Salon Ekleme / Fiyat Düzenleme Modalı'
    ],
    whyWeBuiltIt: 'Müşterilere salonların teknik kapasitesini ve görsellerini prestijli şekilde sunabilmek için geliştirdik.',
    rulesAndCore: [
      'Kural 1: Salon fiyatları değiştiğinde yeni rezervasyonlarda güncel fiyat baz alınmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Salonlar sayfasında ilgilenilen salona tıklanarak detay modalı açılır.',
      '2. Adım: Kapasite ve özellikler müşteriye gösterilir.'
    ],
    relatedRoute: 'dugun-salonlari'
  },
  {
    id: 'page-rbac-settings',
    title: 'Rol & İzin Matrisi (RBAC)',
    icon: 'shield',
    fallbackEmoji: '🔒',
    category: 'Security & Management',
    color: 'from-slate-700 to-slate-900',
    borderColor: 'border-slate-600',
    bgColor: 'bg-slate-500/10',
    summary: 'Rol bazlı erişim denetimi (Süper Admin, Moderatör, İyileştirme Uzmanı).',
    whatItDoes: 'Kullanıcıların hangi sayfaları görebileceğini ve hangi butonlara basabileceğini yetkilendirir.',
    connectedNodes: ['core-arch', 'page-users', 'page-profile'],
    readsState: ['roles', 'tabPermissions', 'activeRole'],
    mutatesState: ['roles', 'tabPermissions', 'activeRole'],
    whichFeatures: [
      'Rol Değiştirme Simülasyonu (Header & Profil üzerinden anlık rol değiştirme)',
      'Sayfa Erişim Hakları Matrisi',
      'Kullanıcı Şifre Yönetimi (UserModalComponent password input alanı)'
    ],
    whyWeBuiltIt: 'Resepsiyon personelinin yetkisiz finansal silme veya sistem ayarlarını değiştirmesini engellemek için kurduk.',
    rulesAndCore: [
      'Kural 1: Yetkisiz bir sayfaya girmeye çalışan kullanıcıya 403 Erişim Engellendi ekranı gösterilmelidir.',
      'Kural 2: Kullanıcı ekleme modalında giriş şifresi alanı zorunlu olmalıdır.'
    ],
    stepByStepFlow: [
      '1. Adım: Ayarlar > Rol & İzinler sekmesine gidilir.',
      '2. Adım: Moderatör rolünün Finans silme izni düzenlenir.',
      '3. Adım: Değişiklikler anında rol matrisine yansır.'
    ],
    relatedRoute: 'ayarlar/rol-izinleri'
  }
];

// STATE DATA DEPENDENCY MATRIX FOR VISUALIZATION
const DATA_FLOW_MATRIX = [
  {
    stateName: 'reservations',
    label: 'Rezervasyonlar & Sözleşmeler',
    storage: 'LocalStorage (irem_cache_reservations)',
    readers: ['Dashboard', 'Rezervasyon Sihirbazı', 'Rezervasyon Listesi', 'Takvim', 'Finans', 'Raporlar AI', 'Medya Galerisi'],
    mutators: ['Rezervasyon Sihirbazı (Ekle)', 'Rezervasyon Listesi (Düzenle/Sil/Ertele)', 'Takvim (Tarih Değiştir)'],
    description: 'Sistemdeki tüm düğün organizasyonu kayıtlarını, ödeme ve tarih verilerini tutan ana state.'
  },
  {
    stateName: 'venues',
    label: 'Düğün Salonları Listesi',
    storage: 'INITIAL_VENUES + LocalStorage',
    readers: ['Dashboard', 'Rezervasyon Sihirbazı', 'Takvim', 'Salonlar Sayfası', 'Raporlar AI'],
    mutators: ['Salonlar Sayfası (Ekle/Düzenle)', 'Raporlar AI (Fiyat Güncelle)'],
    description: 'Salon isimlerini, kapasitelerini, görsellerini ve varsayılan paket fiyatlarını saklar.'
  },
  {
    stateName: 'services',
    label: 'Ek Hizmetler Kataloğu',
    storage: 'INITIAL_SERVICES + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Ek Hizmetler Sayfası', 'Raporlar AI'],
    mutators: ['Ek Hizmetler Sayfası (Ekle/Düzenle)'],
    description: 'Orkestra, Fotoğrafçı, İkram Menüleri gibi organizasyon opsiyonlarını barındırır.'
  },
  {
    stateName: 'customers',
    label: 'Müşteri Rehberi',
    storage: 'INITIAL_CUSTOMERS + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Müşteri Rehberi Sayfası', 'Rezervasyon Listesi'],
    mutators: ['Müşteri Rehberi Sayfası (Ekle/Düzenle)', 'Rezervasyon Sihirbazı (Yeni Müşteri Kaydı)'],
    description: 'Müşteri ad-soyad, telefon, e-posta ve sözleşme geçmişi kayıtları.'
  },
  {
    stateName: 'campaigns',
    label: 'Kampanyalar & AI Promosyonlar',
    storage: 'INITIAL_CAMPAIGNS + LocalStorage',
    readers: ['Rezervasyon Sihirbazı', 'Kampanyalar Sayfası'],
    mutators: ['Kampanyalar Sayfası (Ekle/Düzenle)', 'Raporlar AI (Tek Tıkla Kampanyaya Dönüştür)'],
    description: 'Rezervasyon sihirbazında uygulanan indirim kodları ve tutarları.'
  },
  {
    stateName: 'financialStats',
    label: 'Kasa & Gider Hareketleri',
    storage: 'LocalStorage (irem_cache_financialStats)',
    readers: ['Finans & Kasa Sayfası', 'Dashboard'],
    mutators: ['Finans Sayfası (+ Gider Kaydı Ekle)'],
    description: 'Gider kalemlerini (Orkestra ödemesi, garson ikramları vb.) ve ciro analizini yönetir.'
  },
  {
    stateName: 'activeRole / tabPermissions',
    label: 'RBAC Yetki & Rol Tanımları',
    storage: 'LocalStorage (irem_cache_roles)',
    readers: ['Tüm Sayfalar (PageErrorBoundary / Header / Sidebar)'],
    mutators: ['Settings (Rol & İzin Matrisi)', 'Header Rol Simülatörü'],
    description: 'Kullanıcının erişebileceği modülleri ve buton aksiyon yetkilerini kısıtlar.'
  }
];

// END-TO-END USER WORKFLOWS
const E2E_WORKFLOWS = [
  {
    id: 'flow-1',
    title: '📝 1. Yeni Müşteri Sözleşmesi & Rezervasyon Kaydı Akışı',
    color: 'border-purple-500 bg-purple-500/10',
    steps: [
      { num: '01', title: 'Müşteri Seçimi / Ekleme', desc: 'Müşteri rehberinden arama yapılır veya yeni müşteri adı & telefonu girilir.' },
      { num: '02', title: 'Salon & Tarih Belirleme', desc: 'Takvim çakışma kontrolü yapılır, Altın Salon veya Balo Salonu gündüz/gece seansı seçilir.' },
      { num: '03', title: 'Hizmet & Kampanya Ekleme', desc: 'Fotoğraf, Orkestra paketi eklenir. Kampanya kodu (ör. IREM2026) girilerek indirim düşülür.' },
      { num: '04', title: 'Kapora Alımı & Sözleşme', desc: 'Alınan kapora tutarı yazılır. Sistem otomatik A4 formatında resmi sözleşme çıktısı üretir.' },
      { num: '05', title: 'Canlı Yansıma', desc: 'Kayıt anında Takvim, Finans Kasası, Dashboard KPI ve Müşteri Rehberine senkronize olur.' }
    ]
  },
  {
    id: 'flow-2',
    title: '🤖 2. AI Rapor Analizi -> Akıllı Kampanya Dönüştürme Akışı',
    color: 'border-violet-500 bg-violet-500/10',
    steps: [
      { num: '01', title: 'Veri Analizi', desc: 'Raporlar & AI Analytics sayfası rezervasyon verilerinden doluluk oranını (occupancyRate) hesaplar.' },
      { num: '02', title: 'AI Fırsat Tespiti', desc: 'Yapay zeka boş kalan günleri (ör. Hafta içi Salı akşamları) tespit edip indirim önerisi kartı üretir.' },
      { num: '03', title: 'Tek Tıkla Dönüştürme', desc: 'Kullanıcı AI Öneri kartındaki "Tek Tıkla Kampanyaya Dönüştür" butonuna tıklar.' },
      { num: '04', title: 'Kampanya Aktivasyonu', desc: 'Sistem Kampanyalar sayfasına yeni %15 indirim kodu tanımlar ve rezervasyon sihirbazında aktif eder.' }
    ]
  },
  {
    id: 'flow-3',
    title: '💰 3. Finans Kasa Hareketleri & Gider Kaydı Akışı',
    color: 'border-emerald-500 bg-emerald-500/10',
    steps: [
      { num: '01', title: 'Kapora Girişi', desc: 'Rezervasyon yapıldığında alınan kapora otomatik olarak Kasa Gelirleri (+) hanesine yazılır.' },
      { num: '02', title: 'Gider Kaydı Oluşturma', desc: 'Finans sayfasından "+ Gider Kaydı Ekle" butonuna basılarak ikram/garson harcaması girilir.' },
      { num: '03', title: 'Net Kar Hesaplama', desc: 'Sistem Net Kar = Toplam Ciro - Toplam Gider formülünü anlık çalıştırıp KPI kartını günceller.' }
    ]
  },
  {
    id: 'flow-4',
    title: '🛡️ 4. Rol Yetki Değişimi & RBAC Güvenlik Bloklama Akışı',
    color: 'border-slate-500 bg-slate-500/10',
    steps: [
      { num: '01', title: 'Yetki Düzenleme', desc: 'Süper Admin Ayarlar > Rol & İzin Matrisinden Moderatör rolünün Finans silme yetkisini kaldırır.' },
      { num: '02', title: 'Canlı Rol Simülasyonu', desc: 'Header menüsünden "Moderatör" rolü seçilerek sistem bu kimlikle test edilir.' },
      { num: '03', title: '403 Erişim Engeli', desc: 'Moderatör Finans silme butonuna bastığında veya yetkisiz adrese gittiğinde 403 Erişim Engellendi ekranı basılır.' }
    ]
  }
];
