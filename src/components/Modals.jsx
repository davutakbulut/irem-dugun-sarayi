import React, { useEffect } from 'react';
import { formatCurrency, formatDate } from '../utils/helpers';

// ----------------------------------------------------
// 1. IN-APP RED ALERT & CONFIRMATION POPUP MODAL
// ----------------------------------------------------
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
        {/* Red Pulse Badge Icon */}
        <div className="w-16 h-16 rounded-2xl bg-red-500/10 text-red-600 dark:text-red-400 flex items-center justify-center text-3xl mx-auto border border-red-500/30 shadow-inner animate-pulse shrink-0">
          {icon}
        </div>

        {/* Title & Message */}
        <div className="space-y-2">
          <h3 className="font-heading font-extrabold text-lg sm:text-xl text-slate-800 dark:text-white">
            {title}
          </h3>
          <p className="text-xs sm:text-sm text-slate-600 dark:text-gray-300 leading-relaxed font-medium">
            {message}
          </p>
        </div>

        {/* Action Buttons */}
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

// ----------------------------------------------------
// 2. IN-APP INVOICE & CONTRACT NOTIFICATION MODAL
// ----------------------------------------------------
export function InvoiceNotificationModal({ res, onClose, onPrint }) {
  if (!res) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-lg w-full shadow-2xl space-y-6">
        <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800 pb-4">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">📄</span>
            <div>
              <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">Resmi Sözleşme & Fatura</h3>
              <p className="text-xs text-amber-600 dark:text-gold-400 font-bold">Sözleşme No: {res.id}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white text-lg font-bold">✕</button>
        </div>

        <div className="bg-slate-50 dark:bg-slate-800/60 p-4 rounded-2xl border border-slate-200/60 dark:border-slate-700/50 space-y-3 text-xs">
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-gray-400">Müşteri Adı:</span>
            <strong className="text-slate-800 dark:text-gray-100">{res.customerName}</strong>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-gray-400">Etkinlik Tarihi:</span>
            <strong className="text-slate-800 dark:text-gray-100">{formatDate(res.date)} ({res.timeSlot || 'Akşam Seansı'})</strong>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-gray-400">Toplam Tutarlar:</span>
            <strong className="text-slate-800 dark:text-gray-100">{formatCurrency(res.totalAmount)}</strong>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-500 dark:text-gray-400">Tahsil Edilen Kaparo:</span>
            <strong className="text-emerald-600 dark:text-emerald-400">{formatCurrency(res.depositPaid)}</strong>
          </div>
          <div className="flex justify-between pt-2 border-t border-slate-200 dark:border-slate-700">
            <span className="text-slate-500 dark:text-gray-400 font-bold">Kalan Bakiye:</span>
            <strong className="text-amber-700 dark:text-gold-400 text-sm font-extrabold">{formatCurrency(Math.max(0, res.totalAmount - res.depositPaid))}</strong>
          </div>
        </div>

        <div className="flex items-center space-x-3 pt-2">
          <button
            onClick={onClose}
            className="flex-1 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-gray-200 font-bold text-xs transition"
          >
            Kapat
          </button>
          <button
            onClick={() => {
              onPrint(res);
              onClose();
            }}
            className="flex-1 gold-button py-3 rounded-xl font-bold text-xs shadow flex items-center justify-center space-x-2"
          >
            <span>🖨️ Faturayı Yazdır</span>
          </button>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 3. VENUE MODAL COMPONENT (ADD / EDIT VENUE)
// ----------------------------------------------------
export function VenueModalComponent({ venue, onClose, onSave }) {
  const [formData, setFormData] = React.useState({
    id: venue?.id || '',
    name: venue?.name || '',
    capacity: venue?.capacity || 500,
    price: venue?.price || 50000,
    category: venue?.category || 'Balo Salonu',
    description: venue?.description || '',
    image: venue?.image || 'https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...formData, id: formData.id || 'v_' + Date.now() });
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
            {venue ? '✏️ Düğün Salonunu Düzenle' : '🏰 Yeni Düğün Salonu Ekle'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Salon Adı</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Örn: Kraliyet Gold Balo Salonu"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Kapasite (Kişi)</label>
              <input
                type="number"
                required
                value={formData.capacity}
                onChange={e => setFormData({ ...formData, capacity: Number(e.target.value) })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Başlangıç Fiyatı (₺)</label>
              <input
                type="number"
                required
                value={formData.price}
                onChange={e => setFormData({ ...formData, price: Number(e.target.value) })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Salon Kategorisi</label>
            <select
              value={formData.category}
              onChange={e => setFormData({ ...formData, category: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
            >
              <option value="Balo Salonu">Balo Salonu</option>
              <option value="Kır Bahçesi">Kır Bahçesi</option>
              <option value="VIP Teras">VIP Teras</option>
              <option value="Otel Salonu">Otel Salonu</option>
            </select>
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Açıklama</label>
            <textarea
              rows="3"
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Salon özellikleri ve atmosfer detayları..."
            />
          </div>

          <div className="flex space-x-3 pt-2">
            <button type="button" onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
            <button type="submit" className="w-1/2 gold-button py-3 rounded-xl font-bold">Kaydet ✓</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 4. SERVICE MODAL COMPONENT (ADD / EDIT SERVICE)
// ----------------------------------------------------
export function ServiceModalComponent({ service, onClose, onSave }) {
  const [formData, setFormData] = React.useState({
    id: service?.id || '',
    name: service?.name || '',
    price: service?.price || 5000,
    description: service?.description || '',
    image: service?.image || 'https://images.unsplash.com/photo-1511285560929-80b456fea0bc?auto=format&fit=crop&w=400&q=80'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...formData, id: formData.id || 's_' + Date.now() });
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
            {service ? '✏️ Ek Hizmeti Düzenle' : '✨ Yeni Ek Hizmet Ekle'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Hizmet Adı</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Örn: 4K Drone & Video Çekim Paketi"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Hizmet Fiyatı (₺)</label>
            <input
              type="number"
              required
              value={formData.price}
              onChange={e => setFormData({ ...formData, price: Number(e.target.value) })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Açıklama</label>
            <textarea
              rows="3"
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Hizmet kapsamı detayları..."
            />
          </div>

          <div className="flex space-x-3 pt-2">
            <button type="button" onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
            <button type="submit" className="w-1/2 gold-button py-3 rounded-xl font-bold">Kaydet ✓</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 5. CAMPAIGN MODAL COMPONENT (ADD / EDIT CAMPAIGN)
// ----------------------------------------------------
export function CampaignModalComponent({ campaign, onClose, onSave }) {
  const [formData, setFormData] = React.useState({
    id: campaign?.id || '',
    code: campaign?.code || '',
    title: campaign?.title || '',
    discountPercent: campaign?.discountPercent || 10,
    description: campaign?.description || '',
    active: campaign?.active ?? true
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...formData, id: formData.id || 'c_' + Date.now() });
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
            {campaign ? '✏️ Kampanyayı Düzenle' : '🎁 Yeni Kampanya Ekle'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Kampanya Başlığı</label>
            <input
              type="text"
              required
              value={formData.title}
              onChange={e => setFormData({ ...formData, title: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Örn: Erken Rezervasyon Fırsatı"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Kampanya Kodu</label>
              <input
                type="text"
                required
                value={formData.code}
                onChange={e => setFormData({ ...formData, code: e.target.value.toUpperCase() })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100 uppercase"
                placeholder="ERKEN2026"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">İndirim Oranı (%)</label>
              <input
                type="number"
                required
                min="1"
                max="100"
                value={formData.discountPercent}
                onChange={e => setFormData({ ...formData, discountPercent: Number(e.target.value) })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Açıklama</label>
            <textarea
              rows="3"
              value={formData.description}
              onChange={e => setFormData({ ...formData, description: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Kampanya şartları ve indirim detayları..."
            />
          </div>

          <div className="flex space-x-3 pt-2">
            <button type="button" onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
            <button type="submit" className="w-1/2 gold-button py-3 rounded-xl font-bold">Kaydet ✓</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 6. USER MODAL COMPONENT (ADD / EDIT USER)
// ----------------------------------------------------
export function UserModalComponent({ user, onClose, onSave }) {
  const [formData, setFormData] = React.useState({
    id: user?.id || '',
    name: user?.name || '',
    email: user?.email || '',
    role: user?.role || 'operator',
    phone: user?.phone || ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...formData, id: formData.id || 'u_' + Date.now() });
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
            {user ? '✏️ Kullanıcı Hesabını Düzenle' : '👤 Yeni Kullanıcı Ekle'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Ad Soyad</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Ahmet Yılmaz"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">E-Posta Adresi</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={e => setFormData({ ...formData, email: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="ahmet@iremdugunsarayi.com"
            />
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Erişim Rolü</label>
            <select
              value={formData.role}
              onChange={e => setFormData({ ...formData, role: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
            >
              <option value="admin">Yönetici (Admin)</option>
              <option value="manager">Salon Müdürü</option>
              <option value="operator">Rezervasyon Görevlisi</option>
              <option value="accountant">Muhasebe & Finans</option>
            </select>
          </div>

          <div className="flex space-x-3 pt-2">
            <button type="button" onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
            <button type="submit" className="w-1/2 gold-button py-3 rounded-xl font-bold">Kaydet ✓</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 7. CUSTOMER FORM MODAL COMPONENT (ADD / EDIT CUSTOMER)
// ----------------------------------------------------
export function CustomerFormModal({ customer, onClose, onSave }) {
  const [formData, setFormData] = React.useState({
    id: customer?.id || '',
    name: customer?.name || '',
    phone: customer?.phone || '',
    email: customer?.email || '',
    notes: customer?.notes || ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({ ...formData, id: formData.id || 'cust_' + Date.now() });
  };

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100">
            {customer ? '✏️ Müşteri Kartını Düzenle' : '👤 Yeni Müşteri Kaydet'}
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Müşteri Ad Soyad</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={e => setFormData({ ...formData, name: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Mehmet & Ayşe Kaya"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Telefon</label>
              <input
                type="text"
                required
                value={formData.phone}
                onChange={e => setFormData({ ...formData, phone: e.target.value })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
                placeholder="0532 111 2233"
              />
            </div>
            <div>
              <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">E-Posta</label>
              <input
                type="email"
                value={formData.email}
                onChange={e => setFormData({ ...formData, email: e.target.value })}
                className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
                placeholder="musteri@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block font-bold text-slate-700 dark:text-gray-300 mb-1">Özel Notlar</label>
            <textarea
              rows="3"
              value={formData.notes}
              onChange={e => setFormData({ ...formData, notes: e.target.value })}
              className="w-full p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-gray-100"
              placeholder="Müşterinin özel düğün istekleri, masa yerleşimi tercihleri..."
            />
          </div>

          <div className="flex space-x-3 pt-2">
            <button type="button" onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
            <button type="submit" className="w-1/2 gold-button py-3 rounded-xl font-bold">Kaydet ✓</button>
          </div>
        </form>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 8. RESERVATION DETAIL MODAL COMPONENT
// ----------------------------------------------------
export function ReservationDetailModal({ res, venues = [], services = [], onClose, onPrintInvoice, onUpdatePayment, onShowEmail }) {
  if (!res) return null;

  const venue = venues.find(v => v.id === res.venueId);

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-2xl w-full shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start border-b border-slate-200 dark:border-slate-800 pb-4">
          <div>
            <span className="text-xs font-bold text-amber-700 dark:text-gold-400 bg-amber-500/10 px-3 py-1 rounded-full">
              Sözleşme No: {res.id}
            </span>
            <h2 className="font-heading font-extrabold text-xl sm:text-2xl text-slate-800 dark:text-gray-100 mt-2">
              {res.customerName}
            </h2>
            <p className="text-xs text-slate-500 dark:text-gray-400">📅 Tarih: {formatDate(res.date)} | ⏰ {res.timeSlot || 'Akşam Seansı'}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold text-xl">✕</button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="bg-slate-50 dark:bg-slate-800/60 p-4 rounded-2xl border border-slate-200/60 dark:border-slate-700/50 space-y-2">
            <h4 className="font-bold text-slate-800 dark:text-gray-100 text-sm border-b pb-1">🏰 Düğün Salonu Bilgileri</h4>
            <div><strong className="text-slate-700 dark:text-gray-300">Salon:</strong> {venue?.name || 'Seçili Salon'}</div>
            <div><strong className="text-slate-700 dark:text-gray-300">Kapasite:</strong> {venue?.capacity || 500} Kişilik</div>
            <div><strong className="text-slate-700 dark:text-gray-300">Konum:</strong> {venue?.location || 'Sakarya Sapanca İrem Düğün Sarayı'}</div>
          </div>

          <div className="bg-slate-50 dark:bg-slate-800/60 p-4 rounded-2xl border border-slate-200/60 dark:border-slate-700/50 space-y-2">
            <h4 className="font-bold text-slate-800 dark:text-gray-100 text-sm border-b pb-1">💳 Finansal Durum</h4>
            <div><strong className="text-slate-700 dark:text-gray-300">Toplam Paket Tutarı:</strong> {formatCurrency(res.totalAmount)}</div>
            <div><strong className="text-slate-700 dark:text-gray-300">Ödenen Kaparo:</strong> <span className="text-emerald-600 dark:text-emerald-400 font-bold">{formatCurrency(res.depositPaid)}</span></div>
            <div><strong className="text-slate-700 dark:text-gray-300">Kalan Bakiye:</strong> <span className="text-amber-700 dark:text-gold-400 font-bold">{formatCurrency(Math.max(0, res.totalAmount - res.depositPaid))}</span></div>
          </div>
        </div>

        <div className="flex flex-wrap gap-3 pt-2">
          <button
            onClick={() => onShowEmail(res)}
            className="flex-1 py-3 px-4 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 font-bold text-xs border border-blue-500/30 flex items-center justify-center space-x-1"
          >
            <span>📧 E-Posta Gönder</span>
          </button>
          <button
            onClick={onPrintInvoice}
            className="flex-1 gold-button py-3 px-4 rounded-xl font-bold text-xs shadow flex items-center justify-center space-x-1"
          >
            <span>🖨️ Faturayı Yazdır</span>
          </button>
        </div>
      </div>
    </div>
  );
}

// ----------------------------------------------------
// 9. EMAIL NOTIFICATION MODAL COMPONENT
// ----------------------------------------------------
export function EmailNotificationModal({ emailData, onClose }) {
  if (!emailData) return null;

  return (
    <div className="fixed inset-0 z-[9999] flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-brand-border rounded-3xl p-6 sm:p-8 max-w-xl w-full shadow-2xl space-y-4">
        <div className="flex justify-between items-center border-b border-slate-200 dark:border-slate-800 pb-3">
          <h3 className="font-heading font-extrabold text-lg text-slate-800 dark:text-gray-100 flex items-center space-x-2">
            <span>✉️ Otomatik E-Posta & Bildirim Gönderimi</span>
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 dark:hover:text-white font-bold">✕</button>
        </div>

        <div className="space-y-3 text-xs">
          <div>
            <label className="block text-slate-500 dark:text-gray-400 font-bold">Alıcı E-Posta:</label>
            <input type="text" readOnly value={emailData.to} className="w-full p-2.5 rounded-xl border bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-gray-200" />
          </div>
          <div>
            <label className="block text-slate-500 dark:text-gray-400 font-bold">E-Posta Konusu:</label>
            <input type="text" readOnly value={emailData.subject} className="w-full p-2.5 rounded-xl border bg-slate-100 dark:bg-slate-800 text-slate-800 dark:text-gray-200 font-bold" />
          </div>
          <div>
            <label className="block text-slate-500 dark:text-gray-400 font-bold">Önizleme İçeriği:</label>
            <div className="p-4 rounded-xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-gray-300 space-y-2 max-h-40 overflow-y-auto">
              <p>Sayın <strong>{emailData.name}</strong>,</p>
              <p>İrem Düğün Sarayı & Organizasyon platformunda oluşturulan resmi rezervasyon belgeniz ekte bilgilerinize sunulmuştur.</p>
              <p className="text-[11px] text-slate-500">Bizi tercih ettiğiniz için teşekkür ederiz!</p>
            </div>
          </div>
        </div>

        <div className="flex space-x-3 pt-3">
          <button onClick={onClose} className="w-1/2 py-3 rounded-xl bg-slate-100 dark:bg-slate-800 font-bold text-slate-600 dark:text-gray-300">Vazgeç</button>
          <button
            onClick={() => {
              if (emailData.onSent) emailData.onSent();
              onClose();
            }}
            className="w-1/2 gold-button py-3 rounded-xl font-bold flex items-center justify-center space-x-1"
          >
            <span>🚀 Bildirimi Gönder</span>
          </button>
        </div>
      </div>
    </div>
  );
}
