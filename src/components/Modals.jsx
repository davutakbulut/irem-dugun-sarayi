import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import { formatDate, formatCurrency, formatPhoneNumber, isValidPhoneNumber } from '../utils/formatters';
import { ThemeIcon } from './ThemeIcon';
import { ImageDropzoneUploader } from './ImageDropzoneUploader';

export function VenueDetailModalComponent({ venue, services = [], onClose, onSelectVenue }) {
  if (!venue) return null;

  useEffect(() => {
    const originalOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    return () => {
      document.body.style.overflow = originalOverflow;
    };
  }, []);

  const interiorImages = venue.images && venue.images.length > 0 ? venue.images : [
    (venue.image ? venue.image.replace('w=800', 'w=450&q=65') : 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=450&q=65'),
    'https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=450&q=65'
  ];

  const exteriorImages = [
    'https://images.unsplash.com/photo-1464366400600-7168b8af9bc3?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1519225421980-715cb0215aed?auto=format&fit=crop&w=450&q=65',
    'https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=450&q=65'
  ];

  // DYNAMIC EVENT TYPES FROM VENUE RECORD
  const dynamicEventTypes = (venue.eventTypes && venue.eventTypes.length > 0)
    ? venue.eventTypes
    : ['Düğün', 'Nişan', 'Kurumsal Kokteyl'];

  // DYNAMIC AVAILABLE SERVICES MATCHING THIS VENUE'S UNIQUE SERVICE IDS
  const venueServiceIds = venue.availableServices || [];
  const dynamicVenueServices = venueServiceIds.length > 0
    ? (services || []).filter(s => venueServiceIds.includes(s.id))
    : (services || []).slice(0, 4);

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
                  <span><ThemeIcon icon="location" fallbackEmoji="📍" className="w-3.5 h-3.5 inline-block mr-1" /> {venue.location || 'Sapanca Göl Kenarı, Sakarya'} (Haritalarda Göster ↗)</span>
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

        {/* MODAL BODY */}
        <div className="p-4 sm:p-6 space-y-6 overflow-y-auto custom-scrollbar flex-1 max-h-[calc(90vh-180px)]">
          
          {/* TOP HIGHLIGHT BAR */}
          <div className="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-xs">
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-amber-800 dark:text-gold-400">🏛️ Salon Kategorisi:</span>
              <span className="px-2.5 py-0.5 rounded-full bg-amber-500 text-slate-900 font-extrabold">{venue.category || 'Balo Salonu'}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-slate-700 dark:text-gray-300">Özel İmkanlar:</span>
              <span className="font-semibold text-slate-600 dark:text-gray-300">{(venue.features || ['Kristal Avize', 'VIP Odası']).join(' • ')}</span>
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

          {/* DYNAMIC YAPILABİLECEK ETKİNLİK TÜRLERİ */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path></svg>
              <span>Mekanda Düzenlenebilen Etkinlik Türleri ({dynamicEventTypes.length}):</span>
            </h3>
            <div className="flex flex-wrap gap-2">
              {dynamicEventTypes.map((ev, i) => (
                <div key={i} className="bg-amber-500/10 border border-amber-500/30 px-3.5 py-2 rounded-xl text-amber-800 dark:text-gold-400 font-extrabold text-xs flex items-center space-x-1.5 shadow-sm">
                  <ThemeIcon icon="target" fallbackEmoji="🎯" className="w-3.5 h-3.5 inline-block text-amber-500 shrink-0" />
                  <span>{ev}</span>
                </div>
              ))}
            </div>
          </div>

          {/* DYNAMIC SEÇİLEBİLECEK HİZMETLER (MEKANA ÖZEL VE DOĞRU) */}
          <div className="space-y-2">
            <h3 className="font-bold text-xs sm:text-sm text-slate-800 dark:text-gray-100 flex items-center space-x-2">
              <svg className="w-4 h-4 text-slate-600 dark:text-gray-400 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
              <span>{venue.name} Mekanıyla Uyumlu Dahil Edilebilir Ek Hizmetler ({dynamicVenueServices.length}):</span>
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {dynamicVenueServices.length === 0 ? (
                <div className="p-3 bg-amber-500/10 rounded-xl border border-amber-500/30 text-xs font-bold text-amber-800 dark:text-gold-400 col-span-2">
                  Bu mekana özel ek tanımlı hizmet bulunmamaktadır.
                </div>
              ) : (
                dynamicVenueServices.map((srv, i) => (
                  <div key={srv.id || i} className="flex items-start space-x-2.5 bg-slate-50 dark:bg-brand-dark p-3 rounded-xl border border-slate-200 dark:border-brand-border">
                    <span className="text-emerald-500 font-extrabold text-sm shrink-0 mt-0.5">✓</span>
                    <div className="space-y-0.5">
                      <div className="font-bold text-xs text-slate-800 dark:text-gray-200">{srv.name}</div>
                      <div className="text-[10px] text-slate-500 dark:text-gray-400">{srv.description} | {formatCurrency(srv.price)} {srv.pricingType === 'per_person' ? '/Kişi' : srv.pricingType === 'per_unit' ? '/Adet' : '/Paket'}</div>
                    </div>
                  </div>
                ))
              )}
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
              if (onSelectVenue) onSelectVenue(venue);
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

  if (typeof ReactDOM !== 'undefined' && ReactDOM.createPortal && document.body) {
    return ReactDOM.createPortal(modalJSX, document.body);
  }
  return modalJSX;
}

export function CustomerFormModal({ customer, onClose, onSave }) {
  const [name, setName] = useState(customer?.name || '');
  const [email, setEmail] = useState(customer?.email || '');
  const [phone, setPhone] = useState(customer?.phone || '');
  const [address, setAddress] = useState(customer?.address || '');
  const [taxType, setTaxType] = useState(customer?.taxType || 'individual');
  const [tcNo, setTcNo] = useState(customer?.tcNo || '');
  const [taxOffice, setTaxOffice] = useState(customer?.taxOffice || '');

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in" role="dialog" aria-modal="true">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">{customer ? 'Müşteri Kartı Düzenle' : 'Yeni Müşteri Ekle'}</h3>
        <div className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Müşteri / Çift Adı Soyadı:</label>
            <input type="text" placeholder="Müşteri / Firma Adı" value={name} onChange={e => setName(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="font-bold block mb-1">Telefon Numarası:</label>
              <input
                type="text"
                placeholder="Telefon 0 (5XX) XXX XX XX"
                value={phone}
                onChange={e => setPhone(formatPhoneNumber(e.target.value))}
                className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold"
              />
            </div>
            <div>
              <label className="font-bold block mb-1">E-posta Adresi:</label>
              <input type="email" placeholder="E-posta" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
            </div>
          </div>
          <div>
            <label className="font-bold block mb-1">Müşteri Tipi:</label>
            <select value={taxType} onChange={e => setTaxType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold">
              <option value="individual">Bireysel Müşteri (TC No)</option>
              <option value="corporate">Kurumsal Müşteri (VKN)</option>
            </select>
          </div>
          <div className="grid grid-cols-2 gap-2">
            <div>
              <label className="font-bold block mb-1">{taxType === 'individual' ? 'TC Kimlik No:' : 'Vergi Kimlik No (VKN):'}</label>
              <input type="text" placeholder={taxType === 'individual' ? 'TC Kimlik No' : 'Vergi Kimlik No (VKN)'} value={tcNo} onChange={e => setTcNo(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
            </div>
            <div>
              <label className="font-bold block mb-1">Vergi Dairesi:</label>
              <input type="text" placeholder="Vergi Dairesi" value={taxOffice} onChange={e => setTaxOffice(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200" />
            </div>
          </div>
          <div>
            <label className="font-bold block mb-1">Adres Bilgisi:</label>
            <textarea placeholder="Adres Bilgisi" value={address} onChange={e => setAddress(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 h-16" />
          </div>
        </div>
        <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
          <button onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl text-xs font-bold">İptal</button>
          <button onClick={() => {
            if (!name.trim()) return;
            onSave({ id: customer?.id || 'c-' + Date.now(), name, email, phone, address, taxType, tcNo, taxOffice });
          }} className="gold-button font-bold px-5 py-2 rounded-xl text-xs">Müşteriyi Kaydet ✓</button>
        </div>
      </div>
    </div>
  );
}

export function VenueModalComponent({ venue, allServices = [], onClose, onSave }) {
  const [name, setName] = useState(venue?.name || '');
  const [category, setCategory] = useState(venue?.category || 'Kapalı Balo Salonu');
  const [capacity, setCapacity] = useState(venue?.capacity || 500);
  const [price, setPrice] = useState(venue?.price || 50000);
  const [deposit, setDeposit] = useState(venue?.deposit || 10000);
  const [description, setDescription] = useState(venue?.description || '');
  const [image, setImage] = useState(venue?.image || venue?.images?.[0] || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80');

  const [eventTypes, setEventTypes] = useState(
    venue?.eventTypes || ['Düğün', 'Nişan', 'Kına', 'Kurumsal Etkinlik', 'Gala', 'Sünnet Düğünü']
  );
  const [newEventInput, setNewEventInput] = useState('');

  const addEventType = () => {
    const trimmed = newEventInput.trim();
    if (trimmed && !eventTypes.includes(trimmed)) {
      setEventTypes([...eventTypes, trimmed]);
      setNewEventInput('');
    }
  };

  const removeEventType = (typeToRemove) => {
    setEventTypes(eventTypes.filter(t => t !== typeToRemove));
  };

  const defaultServicesList = allServices.length > 0 ? allServices : [
    { id: 's1', name: 'Gurme Yemek Servisi (Et Menü)' },
    { id: 's2', name: 'Fotoğraf & 4K Video Paketi' },
    { id: 's3', name: 'Canlı Müzik Orkestrası & DJ' },
    { id: 's4', name: 'Masa & Sahne Süsleme' },
    { id: 's5', name: 'Volkan, Konfeti & Işık Şovu' }
  ];

  const [selectedServices, setSelectedServices] = useState(
    venue?.availableServices || ['s1', 's2', 's3'] // Auto-assign standard default services for new venues!
  );

  const toggleService = (srvId) => {
    setSelectedServices(prev => 
      prev.includes(srvId) ? prev.filter(id => id !== srvId) : [...prev, srvId]
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      id: venue?.id || `v-${Date.now()}`,
      name,
      category,
      capacity: Number(capacity),
      price: Number(price),
      deposit: Number(deposit),
      description,
      image,
      images: [image],
      occupancyRate: venue?.occupancyRate || 75,
      eventTypes: eventTypes,
      availableServices: selectedServices
    });
  };

  return (
    <div className="fixed inset-0 z-[999999] bg-black/75 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-lg w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100 flex items-center space-x-2">
            <span>
              <ThemeIcon icon="venue" fallbackEmoji="🏰" className="w-5 h-5 inline-block mr-1.5 text-amber-500" />
              {venue ? 'Etkinlik Mekanını Düzenle' : 'Yeni Etkinlik Mekanı Ekle'}
            </span>
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold text-lg">✕</button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Etkinlik Mekanı Adı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required placeholder="Örn: Kraliyet Balo Salonu / Kır Bahçesi" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">Kategori / Konsept:</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold">
                <option value="Kapalı Balo Salonu">Kapalı Balo Salonu</option>
                <option value="Kır Bahçesi">Kır Bahçesi (Açık Hava)</option>
                <option value="Butik Salon">Butik Salon (Nişan & Kına)</option>
                <option value="Havuz Başı">Havuz Başı Etkinlik Alanı</option>
                <option value="Kurumsal Konferans">Kurumsal Konferans & Gala</option>
              </select>
            </div>
            <div>
              <label className="font-bold block mb-1">Maksimum Kapasite (Kişi):</label>
              <input type="number" value={capacity} onChange={e => setCapacity(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-slate-800 dark:text-gray-200 font-bold" />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">Kiralama Fiyatı (TL):</label>
              <input type="number" value={price} onChange={e => setPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-amber-700 font-bold" />
            </div>
            <div>
              <label className="font-bold block mb-1">Asgari Kaparo Bedeli (TL):</label>
              <input type="number" value={deposit} onChange={e => setDeposit(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-emerald-600 font-bold" />
            </div>
          </div>

          {/* SEÇİLEBİLİR EK HİZMETLER TANIMLAMA SEKTÖRÜ */}
          <div className="border-t border-b border-slate-200 dark:border-brand-border/60 py-3 space-y-2">
            <label className="font-extrabold block text-slate-800 dark:text-gray-100 flex items-center justify-between">
              <span>✨ Bu Mekanda Sunulabilecek Hizmetler:</span>
              <span className="text-[10px] text-amber-600 font-bold">({selectedServices.length} Seçili)</span>
            </label>
            <p className="text-[11px] text-slate-500 dark:text-gray-400">
              Bu etkinlik mekanına özel tanımlamak istediğiniz paket hizmetlerini işaretleyin:
            </p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-h-36 overflow-y-auto custom-scrollbar p-2.5 bg-slate-50 dark:bg-brand-dark/60 border border-slate-200 dark:border-brand-border rounded-xl">
              {defaultServicesList.map(srv => {
                const isChecked = selectedServices.includes(srv.id);
                return (
                  <label key={srv.id} className={`flex items-center space-x-2 p-2 rounded-xl cursor-pointer transition-all ${
                    isChecked 
                      ? 'bg-amber-500/10 border border-amber-500/30 text-amber-900 dark:text-amber-300 font-bold' 
                      : 'hover:bg-slate-200/50 dark:hover:bg-brand-card text-slate-700 dark:text-gray-300'
                  }`}>
                    <input
                      type="checkbox"
                      checked={isChecked}
                      onChange={() => toggleService(srv.id)}
                      className="accent-amber-500 rounded w-4 h-4 cursor-pointer"
                    />
                    <span className="text-xs truncate">{srv.name}</span>
                  </label>
                );
              })}
            </div>
          </div>

          {/* ETKİNLİK TÜRLERİ YÖNETİMİ */}
          <div className="space-y-1.5 pt-1">
            <label className="font-bold block text-slate-700 dark:text-gray-200 flex items-center justify-between">
              <span>🎯 Düzenlenebilen Etkinlik Türleri:</span>
              <span className="text-[10px] text-amber-600 font-bold">({eventTypes.length} Tür Tanımlı)</span>
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={newEventInput}
                onChange={e => setNewEventInput(e.target.value)}
                onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addEventType(); } }}
                placeholder="Örn: Sünnet, Bekarlığa Veda, Gala (Enter'a basın)"
                className="flex-1 bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2 text-slate-800 dark:text-gray-200 text-xs font-bold"
              />
              <button
                type="button"
                onClick={addEventType}
                className="gold-button font-bold px-3 py-2 rounded-xl text-xs"
              >
                + Tür Ekle
              </button>
            </div>
            <div className="flex flex-wrap gap-1.5 pt-1">
              {eventTypes.map(type => (
                <span key={type} className="inline-flex items-center space-x-1 text-[11px] bg-amber-500/10 dark:bg-amber-500/20 text-amber-800 dark:text-amber-300 font-bold px-2.5 py-1 rounded-lg border border-amber-500/30">
                  <span>{type}</span>
                  <button type="button" onClick={() => removeEventType(type)} className="hover:text-red-500 font-extrabold ml-1.5">✕</button>
                </span>
              ))}
            </div>
          </div>

          <ImageDropzoneUploader
            label="Mekan Kapak Görseli Yükle"
            value={image}
            onChange={setImage}
            aspectGuide="1200x800 px (16:9 Geniş)"
            placeholderIcon="🏰"
          />
          <div>
            <label className="font-bold block mb-1">Açıklama & Mekan Özellikleri:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 h-16 text-slate-800 dark:text-gray-200" placeholder="Mekan detayları, teknik altyapı ve imkanlar..." />
          </div>
          <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold">İptal</button>
            <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl">Mekanı Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" /></button>
          </div>
        </form>
      </div>
    </div>
  );
}

export function ServiceModalComponent({ service, onClose, onSave }) {
  const [name, setName] = useState(service?.name || '');
  const [category, setCategory] = useState(service?.category || 'Catering');
  const [pricingType, setPricingType] = useState(service?.pricingType || 'per_person');
  const [price, setPrice] = useState(service?.price || 250);
  const [description, setDescription] = useState(service?.description || '');
  const [image, setImage] = useState(service?.image || 'https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=400&q=80');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      id: service?.id || `s-${Date.now()}`,
      name,
      category,
      pricingType,
      price: Number(price),
      description,
      image
    });
  };

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">
            {service ? (
              <><ThemeIcon icon="sparkles" fallbackEmoji="✨" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Ek Hizmeti Düzenle</>
            ) : (
              <><ThemeIcon icon="plus" fallbackEmoji="➕" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Yeni Ek Hizmet Ekle</>
            )}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">✕</button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Hizmet Adı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">Kategori:</label>
              <select value={category} onChange={e => setCategory(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200">
                <option value="Catering">Catering / İkram</option>
                <option value="Medya">Medya & Çekim</option>
                <option value="Müzik">Müzik & Orkestra</option>
                <option value="Efekt">Efekt & Dekorasyon</option>
                <option value="Ulaşım">VIP Ulaşım</option>
              </select>
            </div>
            <div>
              <label className="font-bold block mb-1">Fiyatlandırma Tipi:</label>
              <select value={pricingType} onChange={e => setPricingType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200">
                <option value="per_person">Kişi Başı (₺/Kişi)</option>
                <option value="flat">Sabit Paket (₺/Paket)</option>
                <option value="fixed">Sabit Paket (₺)</option>
              </select>
            </div>
          </div>
          <div>
            <label className="font-bold block mb-1">Birim Fiyat (TL):</label>
            <input type="number" value={price} onChange={e => setPrice(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 text-amber-700 font-bold" />
          </div>
          <ImageDropzoneUploader
            label="Hizmet Kapak Görseli Yükle"
            value={image}
            onChange={setImage}
            aspectGuide="600x400 px (3:2)"
            placeholderIcon="✨"
          />
          <div>
            <label className="font-bold block mb-1">Açıklama:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 h-16 text-slate-800 dark:text-gray-200" />
          </div>
          <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold">İptal</button>
            <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl">Hizmeti Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" /></button>
          </div>
        </form>
      </div>
    </div>
  );
}

export function CampaignModalComponent({ campaign, onClose, onSave, campaigns = [] }) {
  const [code, setCode] = useState(campaign?.code || '');
  const [title, setTitle] = useState(campaign?.title || '');
  const [discountType, setDiscountType] = useState(campaign?.discountType || campaign?.type || 'percent');
  const [discountValue, setDiscountValue] = useState(campaign?.discountValue || campaign?.value || 15);
  const [minGuest, setMinGuest] = useState(campaign?.minGuest || 300);
  const [validUntil, setValidUntil] = useState(campaign?.validUntil || '2026-12-31');
  const [description, setDescription] = useState(campaign?.description || '');
  const [codeError, setCodeError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    const cleanCode = code.trim().toUpperCase();
    if (!cleanCode) {
      setCodeError('Kampanya indirim kodu boş olamaz!');
      return;
    }
    const isDuplicate = (campaigns || []).some(c => c.id !== campaign?.id && (c.code || '').trim().toUpperCase() === cleanCode);
    if (isDuplicate) {
      setCodeError(`" ${cleanCode} " kodlu bir kampanya zaten mevcut! Lütfen benzersiz bir kupon kodu yazınız.`);
      return;
    }
    setCodeError('');
    onSave({
      id: campaign?.id || `c-${Date.now()}`,
      code: cleanCode,
      title,
      discountType,
      discountValue: Math.max(0, Number(discountValue)),
      type: discountType,
      value: Math.max(0, Number(discountValue)),
      minGuest: Math.max(1, Number(minGuest)),
      validUntil,
      active: true,
      description
    });
  };

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">
            {campaign ? (
              <><ThemeIcon icon="gift" fallbackEmoji="🎁" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Kampanyayı Düzenle</>
            ) : (
              <><ThemeIcon icon="plus" fallbackEmoji="➕" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Yeni Özel Kampanya Ekle</>
            )}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">✕</button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">Kampanya Kodu:</label>
              <input type="text" placeholder="Örn: YAZ2026" value={code} onChange={e => setCode(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-mono font-bold uppercase text-amber-700 dark:text-gold-400" />
            </div>
            <div>
              <label className="font-bold block mb-1">İndirim Tipi:</label>
              <select value={discountType} onChange={e => setDiscountType(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200">
                <option value="percent">% Yüzde İndirimi</option>
                <option value="fixed">TL Sabit Tutar İndirimi</option>
                <option value="amount">TL Tutar İndirimi</option>
                <option value="free_service">Hediye Hizmet</option>
              </select>
            </div>
          </div>
          <div>
            <label className="font-bold block mb-1">Kampanya Başlığı:</label>
            <input type="text" value={title} onChange={e => setTitle(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">İndirim Miktarı ({discountType === 'percent' ? '%' : 'TL'}):</label>
              <input type="number" value={discountValue} onChange={e => setDiscountValue(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-emerald-600" />
            </div>
            <div>
              <label className="font-bold block mb-1">Son Geçerlilik Tarihi:</label>
              <input type="date" value={validUntil} onChange={e => setValidUntil(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
            </div>
          </div>
          <div>
            <label className="font-bold block mb-1">Detaylı Kampanya Açıklaması:</label>
            <textarea value={description} onChange={e => setDescription(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 h-16 text-slate-800 dark:text-gray-200" />
          </div>
          <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold">İptal</button>
            <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl">Kampanyayı Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" /></button>
          </div>
        </form>
      </div>
    </div>
  );
}

export function UserModalComponent({ user, onClose, onSave }) {
  const [name, setName] = useState(user?.name || '');
  const [email, setEmail] = useState(user?.email || '');
  const [password, setPassword] = useState(user?.password || '');
  const [role, setRole] = useState(user?.role || 'satisci');
  const [title, setTitle] = useState(user?.title || 'Etkinlik Sorumlusu');
  const [avatar, setAvatar] = useState(user?.avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      id: user?.id || `u-${Date.now()}`,
      name,
      email,
      password,
      role,
      title,
      avatar
    });
  };

  return (
    <div className="fixed inset-0 z-[99999] bg-black/80 backdrop-blur-md flex items-center justify-center p-3 sm:p-6 overflow-y-auto animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto custom-scrollbar my-auto">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <h3 className="text-lg font-bold text-slate-800 dark:text-gray-100">
            {user ? (
              <><ThemeIcon icon="settings" fallbackEmoji="⚙️" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Kullanıcıyı Düzenle</>
            ) : (
              <><ThemeIcon icon="plus" fallbackEmoji="➕" className="w-5 h-5 inline-block mr-1.5 text-amber-500" /> Yeni Kullanıcı Ekle</>
            )}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 text-xs">
          <div>
            <label className="font-bold block mb-1">Adı Soyadı:</label>
            <input type="text" value={name} onChange={e => setName(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
          </div>
          <div>
            <label className="font-bold block mb-1">E-posta Adresi:</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
          </div>
          <div>
            <label className="font-bold block mb-1">Giriş Şifresi:</label>
            <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="••••••••" className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
          </div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="font-bold block mb-1">Sistem Rolü (RBAC):</label>
              <select value={role} onChange={e => setRole(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200">
                <option value="admin">Admin (Tam Yetkili)</option>
                <option value="satisci">Satış Müdürü (Rezervasyon & Satış)</option>
                <option value="sosyal_medyaci">Sosyal Medya Sorumlusu (Foto/Medya)</option>
                <option value="musteri">Müşteri (Özel Takip Portalı)</option>
                <option value="SuperAdmin">SuperAdmin (Tam Yetki)</option>
                <option value="Manager">Manager (Müdür Yetkisi)</option>
                <option value="Staff">Staff (Personel Yetkisi)</option>
              </select>
            </div>
            <div>
              <label className="font-bold block mb-1">Unvan / Görev:</label>
              <input type="text" value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-slate-50 dark:bg-brand-dark border border-slate-200 dark:border-brand-border rounded-xl p-2.5 font-bold text-slate-800 dark:text-gray-200" />
            </div>
          </div>
          <ImageDropzoneUploader
            label="Kullanıcı Profil Fotoğrafı Yükle"
            value={avatar}
            onChange={setAvatar}
            aspectGuide="400x400 px (1:1 Kare)"
            placeholderIcon="👤"
          />
          <div className="flex justify-end space-x-2 pt-2 border-t border-slate-200 dark:border-brand-border">
            <button type="button" onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl font-bold">İptal</button>
            <button type="submit" className="gold-button font-bold px-5 py-2 rounded-xl">Kullanıcıyı Kaydet <ThemeIcon icon="check" fallbackEmoji="✓" className="w-3.5 h-3.5 inline-block ml-1" /></button>
          </div>
        </form>
      </div>
    </div>
  );
}

export function RedAlertConfirmModal({ isOpen, title, message, confirmText = 'Evet, Sil', cancelText = 'Vazgeç', onConfirm, onClose, icon = '🚨' }) {
  if (!isOpen) return null;

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') onClose();
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  return (
    <div className="fixed inset-0 top-0 left-0 w-screen h-screen z-[99999] bg-slate-950/80 backdrop-blur-md flex items-end sm:items-center justify-center p-0 sm:p-6 overflow-hidden animate-fade-in">
      <div className="w-full max-w-lg sm:max-w-md bg-white dark:bg-slate-900 border-t-2 sm:border-2 border-red-500/60 rounded-t-3xl sm:rounded-3xl p-6 sm:p-8 shadow-[0_25px_60px_-15px_rgba(239,68,68,0.4)] relative animate-slide-up sm:animate-scale-up text-center space-y-5 max-h-[85vh] overflow-y-auto">
        <div className="w-16 h-16 rounded-2xl bg-red-500/10 text-red-600 dark:text-red-400 flex items-center justify-center text-3xl mx-auto border border-red-500/30 shadow-inner animate-pulse shrink-0">
          {typeof icon === 'string' ? (
            <ThemeIcon icon="trash" fallbackEmoji={icon} className="w-8 h-8 shrink-0 text-red-600 dark:text-red-400" />
          ) : (
            icon
          )}
        </div>

        <div className="space-y-2">
          <h3 className="font-heading font-extrabold text-lg sm:text-xl text-slate-800 dark:text-white">
            {title}
          </h3>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-300 leading-relaxed font-medium">
            {message}
          </p>
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <button
            type="button"
            onClick={onClose}
            className="flex-1 py-3 px-4 rounded-2xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-gray-200 font-bold text-xs sm:text-sm transition"
          >
            {cancelText}
          </button>
          <button
            type="button"
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className="flex-1 py-3 px-4 rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-bold text-xs sm:text-sm shadow-lg shadow-red-500/30 hover:scale-[1.02] active:scale-[0.98] transition flex items-center justify-center space-x-1"
          >
            <span>{confirmText}</span>
          </button>
        </div>
      </div>
    </div>
  );
}

export function EmailNotificationModal({ emailData, onClose }) {
  if (!emailData) return null;

  return (
    <div className="fixed inset-0 z-[999999] bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-white dark:bg-brand-card border-2 border-amber-500/50 rounded-3xl max-w-xl w-full p-6 space-y-4 shadow-2xl max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-center border-b pb-3 border-slate-200 dark:border-brand-border">
          <div className="flex items-center space-x-2">
            <ThemeIcon icon="email" fallbackEmoji="✉️" className="w-5 h-5 shrink-0 text-amber-500" />
            <div>
              <h3 className="font-bold text-sm text-slate-800 dark:text-gray-100">Otomatik E-Posta Gönderim Simülatörü</h3>
              <p className="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold"><ThemeIcon icon="check" fallbackEmoji="✓" className="w-3 h-3 inline-block mr-1" /> Müşteri E-Posta Adresine Başarıyla İletildi</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        {/* EMAIL TEMPLATE PREVIEW */}
        <div className="bg-slate-50 dark:bg-brand-dark p-5 rounded-2xl border border-slate-200 dark:border-brand-border space-y-4 text-xs font-sans">
          <div className="space-y-1 border-b border-slate-200 dark:border-brand-border pb-3">
            <div><strong className="text-slate-500">Alıcı:</strong> <span className="font-bold text-slate-800 dark:text-gray-200">{emailData.to}</span></div>
            <div><strong className="text-slate-500">Konu:</strong> <span className="font-bold text-amber-700 dark:text-gold-400">{emailData.subject}</span></div>
          </div>

          <div className="space-y-3 leading-relaxed text-slate-700 dark:text-gray-300">
            <p>Merhaba <strong>{emailData.name}</strong>,</p>
            <p>İrem Düğün Sarayı'nı tercih ettiğiniz için bizi çok mutlu ettiniz. Aşağıdaki bilgilerle tüm süreçleri anlık ve sorunsuz takip edebilirsiniz:</p>

            {emailData.type === 'welcome' && (
              <div className="bg-white dark:bg-brand-card p-4 rounded-xl border border-amber-500/30 space-y-2">
                <div className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="key" fallbackEmoji="🔑" className="w-4 h-4 inline-block mr-1 shrink-0" /> Üyelik ve Giriş Bilgileriniz:</div>
                <div>• Kullanıcı Adı / E-Posta: <strong className="font-mono text-slate-900 dark:text-white">{emailData.email}</strong></div>
                <div>• Geçici Giriş Şifresi: <strong className="font-mono text-slate-900 dark:text-white">İrem2026!</strong></div>
              </div>
            )}

            {emailData.type === 'reservation' && emailData.res && (
              <div className="bg-white dark:bg-brand-card p-4 rounded-xl border border-amber-500/30 space-y-2">
                <div className="font-bold text-amber-700 dark:text-gold-400"><ThemeIcon icon="document" fallbackEmoji="📋" className="w-4 h-4 inline-block mr-1 shrink-0" /> Rezervasyon Fatura ve Ödeme Özeti ({emailData.res.id}):</div>
                <table className="w-full text-left text-[11px] border-collapse">
                  <tbody>
                    <tr className="border-b"><td className="py-1">Salon:</td><td className="font-bold">{emailData.res.customerName}</td></tr>
                    <tr className="border-b"><td className="py-1">Tarih & Saat:</td><td className="font-bold">{formatDate(emailData.res.date)} ({emailData.res.timeSlot})</td></tr>
                    <tr className="border-b"><td className="py-1">Toplam Tutarı:</td><td className="font-bold text-slate-900 dark:text-white">{formatCurrency(emailData.res.totalAmount)}</td></tr>
                    <tr className="border-b"><td className="py-1">Ödenen Kapora:</td><td className="font-bold text-emerald-600">{formatCurrency(emailData.res.depositPaid)}</td></tr>
                    <tr><td className="py-1">Kalan Bakiye:</td><td className="font-bold text-red-500">{formatCurrency(emailData.res.remainingBalance)}</td></tr>
                  </tbody>
                </table>
              </div>
            )}

            <div className="pt-2 border-t border-slate-200 dark:border-brand-border text-[11px] text-slate-500 text-center">
              Hayallerinizdeki etkinliği unutulmaz kılmak bizim işimiz!<br />
              <strong>İREM DÜĞÜN SARAYI</strong> | Sakarya, Sapanca | +90 555 555 55 55 | @iremdugunsarayi
            </div>
          </div>
        </div>

        <div className="flex justify-end">
          <button onClick={onClose} className="gold-button font-bold px-6 py-2.5 rounded-xl text-xs shadow">Tamam, Kapat</button>
        </div>
      </div>
    </div>
  );
}

export function DayDetailModalComponent({ dayData, venues = [], onResClick, onCreateNewForDay, onClose, navigateTo }) {
  if (!dayData) return null;
  const { dateStr, dayNumber, reservations = [], drafts = [] } = dayData;

  const dateObj = new Date(dateStr);
  const formattedDate = dateObj.toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', weekday: 'long' });

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-fade-in">
      <div className="bg-white dark:bg-brand-card border border-amber-500/40 rounded-3xl p-6 max-w-2xl w-full shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto custom-scrollbar">
        {/* MODAL HEADER */}
        <div className="flex justify-between items-start border-b border-slate-200 dark:border-brand-border pb-4">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center font-bold text-amber-700 dark:text-gold-400 text-lg">
              {dayNumber}
            </div>
            <div>
              <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
                {formattedDate} Detayı
              </h3>
              <p className="text-xs text-slate-500 dark:text-gray-400">
                Bu güne ait tüm rezervasyonlar, salon doluluk durumları ve yarım kalmış taslaklar
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold text-lg">✕</button>
        </div>

        {/* DRAFT RESERVATIONS SECTION IF ANY */}
        {drafts.length > 0 && (
          <div className="p-4 rounded-2xl bg-amber-500/10 border border-dashed border-amber-500/50 space-y-3">
            <div className="flex justify-between items-center">
              <h4 className="font-bold text-xs uppercase tracking-wider text-amber-700 dark:text-gold-400 flex items-center space-x-1.5">
                <span>⏳</span>
                <span>Yarım Kalmış Taslak Rezervasyonlar ({drafts.length})</span>
              </h4>
              <span className="text-[10px] font-bold text-amber-800 dark:text-gold-400 bg-amber-500/20 px-2 py-0.5 rounded">
                Tamamlanmayı Bekliyor
              </span>
            </div>

            <div className="space-y-2">
              {drafts.map(d => (
                <div key={d.refKey} className="bg-white dark:bg-brand-dark p-3 rounded-xl border border-amber-500/30 flex justify-between items-center">
                  <div>
                    <div className="font-bold text-xs text-slate-800 dark:text-gray-100 flex items-center space-x-2">
                      <span>{d.customerName || 'İsimsiz Taslak Müşteri'}</span>
                      <span className="text-[10px] text-slate-500 font-normal">({d.timeSlot || 'Seans Belirtilmedi'})</span>
                    </div>
                    <div className="text-[10px] text-slate-500 dark:text-gray-400">
                      Salon: <strong>{venues.find(v => v.id === d.venueId)?.name || 'Salon 1'}</strong> • Son Kayıt: {d.lastSaved || 'Bugün'}
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      onClose();
                      if (navigateTo) navigateTo('create-reservation', { ref: d.refKey });
                    }}
                    className="px-3 py-1.5 bg-amber-500 text-white rounded-xl text-xs font-bold shadow hover:bg-amber-600 transition flex items-center space-x-1"
                  >
                    <span>✍️</span>
                    <span>Taslağı Tamamla</span>
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* VENUES AVAILABILITY & CONFLICT MATRIX */}
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <h4 className="font-bold text-xs uppercase tracking-wider text-slate-700 dark:text-gray-300">
              🏛️ Salon Doluluk & Seans Çakışma Analizi
            </h4>
            <span className="text-[10px] font-bold text-slate-500 dark:text-gray-400 font-mono bg-slate-100 dark:bg-brand-dark px-2.5 py-1 rounded-lg">
              Toplam {reservations.length} Onaylı Rezervasyon
            </span>
          </div>

          <div className="grid grid-cols-1 gap-3">
            {venues.map(venue => {
              const venueRes = reservations.filter(r => r.venueId === venue.id);
              const isOccupied = venueRes.length > 0;

              return (
                <div
                  key={venue.id}
                  className={`p-4 rounded-2xl border transition ${
                    isOccupied
                      ? 'bg-amber-500/10 border-amber-500/40 text-slate-800 dark:text-gray-100'
                      : 'bg-emerald-500/5 border-emerald-500/30 text-slate-700 dark:text-gray-300'
                  }`}
                >
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-2">
                      <span className="font-bold text-sm">{venue.name}</span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                        isOccupied
                          ? 'bg-amber-500/20 text-amber-800 dark:text-gold-400 border border-amber-500/30'
                          : 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-400 border border-emerald-500/30'
                      }`}>
                        {isOccupied ? `⚠️ ${venueRes.length} Organizasyon Yapılacak` : '✅ TAMAMEN MÜSAİT'}
                      </span>
                    </div>
                    <span className="font-mono text-xs font-bold text-amber-700 dark:text-gold-400">
                      {formatCurrency(venue.price)}
                    </span>
                  </div>

                  {/* RESERVATIONS IN THIS VENUE */}
                  {isOccupied ? (
                    <div className="mt-3 space-y-2 pt-2 border-t border-amber-500/20">
                      {venueRes.map(r => (
                        <div
                          key={r.id}
                          onClick={() => { onClose(); onResClick(r); }}
                          className="bg-white dark:bg-brand-card p-3 rounded-xl border border-amber-500/30 flex justify-between items-center hover:scale-[1.01] transition cursor-pointer shadow-sm"
                        >
                          <div className="space-y-0.5">
                            <div className="flex items-center space-x-2">
                              <span className="font-mono text-[10px] font-bold text-amber-700 dark:text-gold-400">{r.id}</span>
                              <span className="font-bold text-xs text-slate-800 dark:text-gray-100">{r.customerName}</span>
                            </div>
                            <div className="text-[10px] text-slate-500 dark:text-gray-400 flex items-center space-x-2">
                              <span>⏰ Seans: <strong className="text-amber-800 dark:text-gold-300">{r.timeSlot}</strong></span>
                              <span>• 👥 {r.guestCount} Davetli</span>
                            </div>
                          </div>
                          <div className="flex items-center space-x-2">
                            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20">
                              {r.paymentStatus}
                            </span>
                            <span className="text-xs text-amber-700 dark:text-gold-400">Detay 🔍</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-[11px] text-emerald-600 dark:text-emerald-400 mt-1.5">
                      💡 Bu salon için {formattedDate} tarihinde henüz hiç rezervasyon yapılmamıştır. Gündüz veya Gece seansı hemen rezerve edilebilir!
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* MODAL FOOTER */}
        <div className="pt-3 border-t border-slate-200 dark:border-brand-border flex justify-between items-center">
          <button onClick={onClose} className="px-4 py-2 bg-slate-100 dark:bg-brand-dark text-slate-600 dark:text-gray-400 rounded-xl text-xs font-bold">
            Kapat
          </button>
          <button
            onClick={() => { onClose(); onCreateNewForDay(dateStr); }}
            className="gold-button font-bold text-xs py-2.5 px-6 rounded-xl shadow-lg flex items-center space-x-2"
          >
            <span>➕</span>
            <span>{formattedDate} İçin Yeni Rezervasyon Oluştur</span>
          </button>
        </div>

      </div>
    </div>
  );
}

