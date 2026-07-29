import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { formatCurrency, formatPhoneNumber, isValidPhoneNumber } from '../utils/formatters';

export function VenueDetailModalComponent({ venue, onClose, onSelectVenue }) {
  if (!venue) return null;

  useEffect(() => {
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, []);

  const interiorImages = [
    (venue.image ? venue.image.replace('w=800', 'w=450&q=65') : 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=450&q=65'),
    'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=450&q=65'
  ];

  const exteriorImages = [
    'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=450&q=65'
  ];

  const supportedEvents = [
    { title: 'Düğün Organizasyonu', desc: 'Yemekli & Yemeksiz Düğün Baloları' },
    { title: 'Kına Gecesi Konsepti', desc: 'Taht, Otantik Süslemeler & DJ' },
    { title: 'Nişan & Söz Töreni', desc: 'Butik ve Şık Kutlamalar' },
    { title: 'Kurumsal Gala & Lansman', desc: 'VIP Şirket Etkinlikleri' }
  ];

  const availableServices = [
    'Gurme Yemek Servisi (Et / Tavuk / Vejetaryen)',
    '4K Fotoğraf & Sinematik Video Çekimi',
    'Canlı Müzik Orkestrası & Profesyonel DJ',
    'Özel Çiçekli Masa ve Sahne Dekoru',
    'Gelin Odası İkramları & VIP Karşılama'
  ];

  const mapQueryUrl = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((venue.name || '') + ' ' + (venue.location || 'Sapanca Sakarya İrem Düğün Sarayı'))}`;

  const modalJSX = (
    <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[999999] bg-black/85 backdrop-blur-md flex items-center justify-center p-0 sm:p-6 overflow-hidden animate-fade-in">
      <div className="bg-white dark:bg-brand-card border-0 sm:border border-slate-200 dark:border-brand-border w-full h-full sm:h-auto sm:max-h-[90vh] sm:max-w-4xl rounded-none sm:rounded-3xl shadow-2xl overflow-hidden flex flex-col justify-between custom-scrollbar my-auto">
        
        {/* MODAL HEADER */}
        <div className="relative h-44 sm:h-72 overflow-hidden shrink-0 bg-slate-900">
          <img
            src={venue.image}
            alt={venue.name}
            loading="eager"
            decoding="async"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-slate-950 via-slate-950/50 to-transparent flex flex-col justify-end p-4 sm:p-6 text-white">
            <div className="flex justify-between items-end">
              <div>
                <a
                  href={mapQueryUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="gold-button text-[10px] sm:text-xs font-bold px-3 py-0.5 sm:py-1 rounded-full shadow inline-flex items-center space-x-1 hover:scale-105 transition"
                  title="Haritada Yol Tarifi Al ve Konumu Aç"
                >
                  <svg className="w-3.5 h-3.5 inline text-slate-900" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                  <span>📍 {venue.location || 'Sapanca Göl Kenarı, Sakarya'} (Haritalarda Göster ↗)</span>
                </a>
                <h2 className="text-xl sm:text-3xl font-heading font-extrabold text-white mt-1.5 drop-shadow">
                  {venue.name}
                </h2>
                <p className="text-[11px] sm:text-xs text-gray-200 mt-1 max-w-2xl line-clamp-2 sm:line-clamp-none">{venue.description}</p>
              </div>
              <button
                onClick={onClose}
                className="w-8 h-8 sm:w-10 sm:h-10 rounded-full bg-black/60 hover:bg-red-600 text-white font-bold text-base sm:text-lg flex items-center justify-center backdrop-blur-md transition border border-white/30 shrink-0"
                title="Kapat"
              >
                ✕
              </button>
            </div>
          </div>
        </div>

        {/* MODAL CONTENT BODY */}
        <div className="p-4 sm:p-6 space-y-4 sm:space-y-5 flex-1 overflow-y-auto custom-scrollbar text-xs">
          
          {/* LOCATION MAP BAR */}
          <div className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border flex justify-between items-center text-xs">
            <div className="space-y-0.5">
              <div className="font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-1">
                <svg className="w-4 h-4 text-amber-500 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path></svg>
                <span>Salon Konumu:</span>
              </div>
              <div className="text-slate-500 dark:text-gray-400 text-[11px]">{venue.location || 'Sapanca Göl Kenarı, Sakarya / Türkiye'}</div>
            </div>
            <a
              href={mapQueryUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-1.5 bg-slate-200 dark:bg-brand-card hover:bg-slate-300 text-slate-800 dark:text-gray-200 font-bold rounded-xl text-xs border border-slate-300 dark:border-brand-border flex items-center space-x-1 shrink-0 shadow-sm"
            >
              <span>Haritalarda Aç 🗺️</span>
            </a>
          </div>

          {/* KEY SPECS GRID */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
            <div className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-3 sm:p-3.5 rounded-2xl">
              <span className="text-slate-500 block text-[10px] sm:text-[11px] font-bold">Kapasite:</span>
              <span className="text-sm sm:text-base font-extrabold text-slate-800 dark:text-gray-100">{venue.capacity} Kişi</span>
            </div>

            <div className="bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border p-3 sm:p-3.5 rounded-2xl">
              <span className="text-slate-500 block text-[10px] sm:text-[11px] font-bold">Kiralama Liste Fiyatı:</span>
              <span className="text-sm sm:text-base font-extrabold text-slate-800 dark:text-gray-100">{formatCurrency(venue.price)}</span>
            </div>

            <div className="bg-emerald-500/10 border border-emerald-500/30 p-3 sm:p-3.5 rounded-2xl">
              <span className="text-slate-500 block text-[10px] sm:text-[11px] font-bold">Kapora Bedeli:</span>
              <span className="text-sm sm:text-base font-extrabold text-emerald-600 dark:text-emerald-400">{formatCurrency(venue.deposit || 15000)}</span>
            </div>

            <div className="bg-blue-500/10 border border-blue-500/30 p-3 sm:p-3.5 rounded-2xl">
              <span className="text-slate-500 block text-[10px] sm:text-[11px] font-bold">Sezonluk Doluluk Oranı:</span>
              <div className="flex items-center space-x-2 mt-1">
                <div className="flex-1 bg-slate-200 dark:bg-brand-dark h-2 rounded-full overflow-hidden">
                  <div className="bg-blue-600 h-full rounded-full" style={{ width: `${venue.occupancyRate || 85}%` }}></div>
                </div>
                <span className="font-extrabold text-blue-600 dark:text-blue-400">%{venue.occupancyRate || 85}</span>
              </div>
            </div>
          </div>

          {/* İÇ GÖRSELLERİ GALERİSİ */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
              <span>İç Mekan & Balo Salonu Görselleri:</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {interiorImages.map((img, i) => (
                <div key={i} className="w-full h-32 bg-slate-100 dark:bg-brand-dark rounded-2xl overflow-hidden border border-slate-200 dark:border-brand-border shadow-sm">
                  <img src={img} alt="İç Mekan" loading="lazy" decoding="async" className="w-full h-full object-cover hover:scale-[1.02] transition" />
                </div>
              ))}
            </div>
          </div>

          {/* DIŞ GÖRSELLERİ GALERİSİ */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path></svg>
              <span>Dış Mekan & Göl Manzarası Görselleri:</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              {exteriorImages.map((img, i) => (
                <div key={i} className="w-full h-32 bg-slate-100 dark:bg-brand-dark rounded-2xl overflow-hidden border border-slate-200 dark:border-brand-border shadow-sm">
                  <img src={img} alt="Dış Mekan" loading="lazy" decoding="async" className="w-full h-full object-cover hover:scale-[1.02] transition" />
                </div>
              ))}
            </div>
          </div>

          {/* YAPILABİLECEK ETKİNLİKLER */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
              <span>Yapılabilecek Etkinlik Türleri:</span>
            </h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {supportedEvents.map((ev, i) => (
                <div key={i} className="bg-slate-50 dark:bg-brand-dark p-3 rounded-2xl border border-slate-200 dark:border-brand-border text-center space-y-1">
                  <div className="font-bold text-slate-800 dark:text-gray-200 text-xs">{ev.title}</div>
                  <div className="text-[10px] text-slate-500">{ev.desc}</div>
                </div>
              ))}
            </div>
          </div>

          {/* SEÇİLEBİLECEK HİZMETLER */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span>Dahil Edilebilir Hizmet Paket İçerikleri:</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {availableServices.map((srv, i) => (
                <div key={i} className="flex items-center space-x-2 bg-slate-50 dark:bg-brand-dark p-2.5 rounded-xl border border-slate-200 dark:border-brand-border font-semibold text-slate-700 dark:text-gray-300">
                  <span className="text-emerald-500 font-bold">✓</span>
                  <span>{srv}</span>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* MODAL FOOTER */}
        <div className="p-3 sm:p-4 bg-slate-50 dark:bg-brand-dark border-t border-slate-200 dark:border-brand-border flex flex-col sm:flex-row justify-between items-center gap-2 shrink-0">
          <button onClick={onClose} className="w-full sm:w-auto px-5 py-2.5 bg-slate-200 dark:bg-brand-card text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold hover:bg-slate-300 text-center">
            Kapat
          </button>
          <button
            onClick={() => {
              onSelectVenue(venue);
              onClose();
            }}
            className="w-full sm:w-auto gold-button font-extrabold px-6 py-2.5 rounded-xl text-xs shadow-lg text-center"
          >
            Bu Salonu Seç ve Rezervasyona Ekle ✓
          </button>
        </div>

      </div>
    </div>
  );

  return ReactDOM.createPortal(modalJSX, document.body);
}

export function CustomerFormModal({ customer, onClose, onSave }) {
  const [name, setName] = useState(customer?.name || '');
  const [email, setEmail] = useState(customer?.email || '');
  const [phone, setPhone] = useState(customer?.phone || '');
  const [address, setAddress] = useState(customer?.address || '');
  const [tcNo, setTcNo] = useState(customer?.tcNo || '');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in" role="dialog" aria-modal="true">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{customer ? 'Müşteri Kartı Düzenle' : 'Yeni Müşteri Ekle'}</h3>
        
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Müşteri / Çift Adı Soyadı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">Telefon Numarası:</label>
            <input type="text" value={phone} onChange={e => setPhone(formatPhoneNumber(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">E-posta Adresi:</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" />
          </div>

          <div>
            <label className="font-bold block mb-1">TC Kimlik No:</label>
            <input type="text" value={tcNo} onChange={e => setTcNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" />
          </div>

          <div>
            <label className="font-bold block mb-1">Adres:</label>
            <textarea value={address} onChange={e => setAddress(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">İptal</button>
          <button
            onClick={() => {
              if (!name.trim()) return;
              onSave({ id: customer?.id || 'c-' + Date.now(), name, email, phone, address, tcNo });
            }}
            className="gold-button px-5 py-2 rounded-xl text-xs font-bold shadow"
          >
            Kaydet ✓
          </button>
        </div>
      </div>
    </div>
  );
}

export function VenueModalComponent({ venue, onClose, onSave }) {
  const [name, setName] = useState(venue?.name || '');
  const [category, setCategory] = useState(venue?.category || 'Kapalı Balo Salonu');
  const [capacity, setCapacity] = useState(venue?.capacity || 500);
  const [price, setPrice] = useState(venue?.price || 50000);
  const [deposit, setDeposit] = useState(venue?.deposit || 10000);
  const [description, setDescription] = useState(venue?.description || '');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{venue ? 'Salon Düzenle' : 'Yeni Salon Ekle'}</h3>
        
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Salon Adı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">Kategori:</label>
            <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
              <option value="Kapalı Balo Salonu">Kapalı Balo Salonu</option>
              <option value="Kır Bahçesi">Kır Bahçesi (Açık Hava)</option>
              <option value="Butik Salon">Butik Salon (Nişan & Kına)</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="font-bold block mb-1">Kapasite (Kişi):</label>
              <input type="number" value={capacity} onChange={e => setCapacity(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
            </div>
            <div>
              <label className="font-bold block mb-1">Kiralama Fiyatı (TL):</label>
              <input type="number" value={price} onChange={e => setPrice(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-amber-600" />
            </div>
          </div>

          <div>
            <label className="font-bold block mb-1">Açıklama:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">İptal</button>
          <button
            onClick={() => {
              if (!name.trim()) return;
              onSave({
                id: venue?.id || 'v-' + Date.now(),
                name,
                category,
                capacity,
                price,
                deposit,
                description,
                image: venue?.image || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'
              });
            }}
            className="gold-button px-5 py-2 rounded-xl text-xs font-bold shadow"
          >
            Kaydet ✓
          </button>
        </div>
      </div>
    </div>
  );
}

export function ServiceModalComponent({ service, onClose, onSave }) {
  const [name, setName] = useState(service?.name || '');
  const [category, setCategory] = useState(service?.category || 'Catering');
  const [price, setPrice] = useState(service?.price || 100);
  const [pricingType, setPricingType] = useState(service?.pricingType || 'per_person');
  const [description, setDescription] = useState(service?.description || '');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{service ? 'Hizmet Düzenle' : 'Yeni Hizmet Ekle'}</h3>
        
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Hizmet Adı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="font-bold block mb-1">Kategori:</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                <option value="Catering">Catering / İkram</option>
                <option value="Medya">Medya & Çekim</option>
                <option value="Müzik">Müzik & Orkestra</option>
                <option value="Efekt">Efekt & Dekorasyon</option>
                <option value="Ulaşım">VIP Ulaşım</option>
              </select>
            </div>
            <div>
              <label className="font-bold block mb-1">Fiyat Tipi:</label>
              <select value={pricingType} onChange={e => setPricingType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                <option value="per_person">Kişi Başı (₺/Kişi)</option>
                <option value="fixed">Sabit Paket (₺)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="font-bold block mb-1">Birim Fiyat (TL):</label>
            <input type="number" value={price} onChange={e => setPrice(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-amber-600" />
          </div>

          <div>
            <label className="font-bold block mb-1">Açıklama:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">İptal</button>
          <button
            onClick={() => {
              if (!name.trim()) return;
              onSave({
                id: service?.id || 's-' + Date.now(),
                name,
                category,
                price,
                pricingType,
                description
              });
            }}
            className="gold-button px-5 py-2 rounded-xl text-xs font-bold shadow"
          >
            Kaydet ✓
          </button>
        </div>
      </div>
    </div>
  );
}

export function CampaignModalComponent({ campaign, onClose, onSave }) {
  const [code, setCode] = useState(campaign?.code || '');
  const [title, setTitle] = useState(campaign?.title || '');
  const [discountType, setDiscountType] = useState(campaign?.discountType || 'fixed');
  const [discountValue, setDiscountValue] = useState(campaign?.discountValue || 5000);
  const [minGuest, setMinGuest] = useState(campaign?.minGuest || 300);
  const [validUntil, setValidUntil] = useState(campaign?.validUntil || '2026-12-31');
  const [description, setDescription] = useState(campaign?.description || '');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{campaign ? 'Kampanya Düzenle' : 'Yeni Kampanya Ekle'}</h3>
        
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Kampanya Kodu (Örn: YAZ2026):</label>
            <input type="text" value={code} onChange={e => setCode(e.target.value.toUpperCase())} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold font-mono" />
          </div>

          <div>
            <label className="font-bold block mb-1">Kampanya Başlığı:</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="font-bold block mb-1">İndirim Tipi:</label>
              <select value={discountType} onChange={e => setDiscountType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
                <option value="fixed">Sabit Tutar (TL)</option>
                <option value="percent">Yüzde Oranı (%)</option>
              </select>
            </div>
            <div>
              <label className="font-bold block mb-1">İndirim Miktarı:</label>
              <input type="number" value={discountValue} onChange={e => setDiscountValue(Number(e.target.value))} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold text-amber-600" />
            </div>
          </div>

          <div>
            <label className="font-bold block mb-1">Son Geçerlilik Tarihi:</label>
            <input type="date" value={validUntil} onChange={e => setValidUntil(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">Açıklama:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 h-16" />
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">İptal</button>
          <button
            onClick={() => {
              if (!code.trim() || !title.trim()) return;
              onSave({
                id: campaign?.id || 'cmp-' + Date.now(),
                code,
                title,
                discountType,
                discountValue,
                minGuest,
                validUntil,
                active: true,
                description
              });
            }}
            className="gold-button px-5 py-2 rounded-xl text-xs font-bold shadow"
          >
            Kaydet ✓
          </button>
        </div>
      </div>
    </div>
  );
}

export function UserModalComponent({ user, onClose, onSave }) {
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [role, setRole] = useState(user?.role || 'Staff');
  const [title, setTitle] = useState(user?.title || 'Etkinlik Sorumlusu');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{user ? 'Personel Düzenle' : 'Yeni Personel Ekle'}</h3>
        
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Adı Soyadı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">E-posta Adresi:</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold" />
          </div>

          <div>
            <label className="font-bold block mb-1">Yetki Rolü (RBAC):</label>
            <select value={role} onChange={e => setRole(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5 font-bold">
              <option value="SuperAdmin">👑 SuperAdmin (Tam Yetki)</option>
              <option value="Manager">💼 Manager (Müdür Yetkisi)</option>
              <option value="Staff">👤 Staff (Personel Yetkisi)</option>
            </select>
          </div>

          <div>
            <label className="font-bold block mb-1">Unvan / Görev:</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 rounded-xl p-2.5" />
          </div>
        </div>

        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-200 dark:bg-brand-dark text-slate-700 dark:text-gray-300 rounded-xl text-xs font-bold">İptal</button>
          <button
            onClick={() => {
              if (!name.trim() || !email.trim()) return;
              onSave({
                id: user?.id || 'u-' + Date.now(),
                name,
                email,
                role,
                title,
                avatar: user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
              });
            }}
            className="gold-button px-5 py-2 rounded-xl text-xs font-bold shadow"
          >
            Kaydet ✓
          </button>
        </div>
      </div>
    </div>
  );
}
