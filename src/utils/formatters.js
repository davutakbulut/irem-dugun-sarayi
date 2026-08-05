/**
 * İREM DÜĞÜN SARAYI & ORGANİZASYON PLATFORMU
 * Formatting & Calculation Utilities
 */

export const formatCurrency = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '0 ₺';
  return Number(val).toLocaleString('tr-TR') + ' ₺';
};

export const formatDate = (dateStr) => {
  if (!dateStr) return '';
  try {
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const year = parts[0];
      const monthIdx = parseInt(parts[1], 10) - 1;
      const day = parseInt(parts[2], 10);
      const months = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
      return `${day} ${months[monthIdx]} ${year}`;
    }
  } catch (e) {}
  return dateStr;
};

export const formatPhoneNumber = (val) => {
  if (!val) return '';
  const digits = val.replace(/\D/g, '');
  if (digits.length === 0) return '';
  
  let formatted = '0 ';
  let d = digits.startsWith('0') ? digits.slice(1) : digits;

  if (d.length > 0) formatted += '(' + d.slice(0, 3);
  if (d.length >= 3) formatted += ') ' + d.slice(3, 6);
  if (d.length >= 6) formatted += ' ' + d.slice(6, 8);
  if (d.length >= 8) formatted += ' ' + d.slice(8, 10);
  
  return formatted;
};

export const isValidPhoneNumber = (phoneStr) => {
  if (!phoneStr) return false;
  const digits = phoneStr.replace(/\D/g, '');
  return digits.length === 11 && digits.startsWith('05');
};

export const calculateReservationTotals = ({
  venuePrice = 0,
  guestCount = 0,
  selectedServices = [],
  allServices = [],
  campaignCode = '',
  campaigns = [],
  isInvoiced = false,
  hasDeposit = false,
  depositPaid = 0,
  paymentStatus = 'Bekliyor'
}) => {
  const vPrice = Number(venuePrice) || 0;
  
  let servicesTotal = 0;
  const serviceBreakdown = [];

  (selectedServices || []).forEach(item => {
    const sObj = allServices.find(x => x.id === item.serviceId);
    if (sObj) {
      const uPrice = item.customUnitPrice !== undefined ? Number(item.customUnitPrice) : Number(sObj.price);
      const qty = item.quantity !== undefined ? Number(item.quantity) : (sObj.pricingType === 'per_person' ? Number(guestCount) : 1);
      const lineTotal = uPrice * qty;
      servicesTotal += lineTotal;

      serviceBreakdown.push({
        id: sObj.id,
        name: sObj.name,
        unitPrice: uPrice,
        quantity: qty,
        pricingType: sObj.pricingType,
        total: lineTotal,
        isPaid: item.isPaid || false
      });
    }
  });

  const subtotal = vPrice + servicesTotal;

  let discount = 0;
  if (campaignCode) {
    const cmp = campaigns.find(c => c.code === campaignCode && c.active);
    if (cmp) {
      if (cmp.discountType === 'fixed') {
        discount = Number(cmp.discountValue);
      } else if (cmp.discountType === 'percent') {
        discount = (subtotal * Number(cmp.discountValue)) / 100;
      }
    }
  }

  const afterDiscount = Math.max(0, subtotal - discount);
  const vat = isInvoiced ? afterDiscount * 0.20 : 0;
  const grandTotal = afterDiscount + vat;

  let dep = 0;
  if (paymentStatus === 'Ödendi' || paymentStatus === 'Tamamlandı') {
    dep = grandTotal;
  } else if (hasDeposit || paymentStatus === 'Kapora Alındı') {
    dep = Number(depositPaid) || 0;
  }

  const remaining = Math.max(0, grandTotal - dep);
  const isFullyPaid = remaining === 0 || paymentStatus === 'Ödendi' || paymentStatus === 'Tamamlandı';

  return {
    venuePrice: vPrice,
    servicesTotal,
    serviceBreakdown,
    subtotal,
    discount,
    afterDiscount,
    vat,
    grandTotal,
    dep,
    remaining,
    isFullyPaid
  };
};

export const TAB_TO_SLUG = {
  'public-home': '',
  'public-halls': 'salonlar',
  'public-virtual-tour': '360-tur',
  'public-organizations': 'organizasyonlar',
  'public-videos': 'videolar',
  'public-blog': 'blog',
  'public-about': 'hakkimizda',
  'public-contact': 'iletisim',
  'public-customer-login': 'musteri-giris',
  'public-customer-register': 'musteri-kayit',
  'dashboard': 'anasayfa',
  'create-reservation': 'yeni-rezervasyon',
  'venues': 'dugun-salonlari',
  'services': 'ek-hizmetler',
  'reservations': 'rezervasyonlar',
  'calendar': 'takvim',
  'campaigns': 'kampanyalar',
  'finance': 'finans',
  'customers': 'musteri-rehberi',
  'users': 'kullanici-yonetimi',
  'roles': 'roller',
  'reports': 'raporlar-ai',
  'media': 'medya-yukle',
  'profile': 'profil',
  'mind-map': 'zihin-haritasi',
  'system-guide': 'sistem-kilavuzu',
  'settings': 'ayarlar',
  'settings-appearance': 'ayarlar/gorunum',
  'settings-performance': 'ayarlar/onbellek',
  'settings-rbac': 'ayarlar/rol-izinleri',
  'settings-indexing': 'ayarlar/seo-indeksleme',
  'settings-errors': 'ayarlar/hata-simulasyonu',
  'simulasyon-404': 'simulasyon-404',
  'simulasyon-301': 'simulasyon-301',
  'simulasyon-403': 'simulasyon-403',
  'simulasyon-500': 'simulasyon-500'
};

export const SLUG_TO_TAB = {
  '': 'public-home',
  'salonlar': 'public-halls',
  'salonlarimiz': 'public-halls',
  '360-tur': 'public-virtual-tour',
  'sanal-tur': 'public-virtual-tour',
  'organizasyonlar': 'public-organizations',
  'videolar': 'public-videos',
  'blog': 'public-blog',
  'hakkimizda': 'public-about',
  'kurumsal': 'public-about',
  'iletisim': 'public-contact',
  'musteri-giris': 'public-customer-login',
  'musteri-kayit': 'public-customer-register',
  'yonetim': 'dashboard',
  'yonetim/anasayfa': 'dashboard',
  'dashboard': 'dashboard',
  'anasayfa': 'dashboard',
  'medya': 'media',
  'm': 'media',
  'yeni-rezervasyon': 'create-reservation',
  'rezervasyon-olustur': 'create-reservation',
  'dugun-salonlari': 'venues',
  'ek-hizmetler': 'services',
  'rezervasyonlar': 'reservations',
  'takvim': 'calendar',
  'campaigns': 'campaigns',
  'kampanyalar': 'campaigns',
  'finans': 'finance',
  'musteri-rehberi': 'customers',
  'kullanici-yonetimi': 'users',
  'roller': 'roles',
  'raporlar-ai': 'reports',
  'reports': 'reports',
  'medya-yukle': 'media',
  'profil': 'profile',
  'zihin-haritasi': 'mind-map',
  'zihinharitasi': 'mind-map',
  'mind-map': 'mind-map',
  'mindmap': 'mind-map',
  'sistem-kilavuzu': 'system-guide',
  'kilavuz': 'system-guide',
  'system-guide': 'system-guide',
  'ayarlar': 'settings',
  'ayarlar/gorunum': 'settings-appearance',
  'ayarlar/onbellek': 'settings-performance',
  'ayarlar/rol-izinleri': 'settings-rbac',
  'ayarlar/seo-indeksleme': 'settings-indexing',
  'seo-indeksleme': 'settings-indexing',
  'arama-motoru-ayarlari': 'settings-indexing'
};

export const generateWhatsAppLink = (phone, customerName = '', date = '', remaining = '') => {
  const cleanPhone = phone ? phone.replace(/[^0-9]/g, '') : '';
  const text = `Merhabalar Sayın ${customerName}, İrem Düğün Sarayı & Organizasyon Şirketi ${date ? date + ' tarihli ' : ''}rezervasyonunuz hakkında bilgilendirmedir. Kalan Bakiyeniz: ${remaining ? formatCurrency(remaining) : 'Detaylar için iletişime geçiniz.'}`;
  return `https://wa.me/${cleanPhone}?text=${encodeURIComponent(text)}`;
};

export const generateDraftRefKey = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < 12; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
};

export const parseHashRoute = () => {
  if (typeof window === 'undefined') return { tab: 'public-home', slug: '' };
  const pathname = window.location.pathname || '/';
  const rawHash = (window.location.hash || '').replace('#/', '').replace('#', '');
  const [routePart, queryPart] = rawHash.split('?');
  const searchStr = window.location.search || (queryPart ? '?' + queryPart : '');
  const params = new URLSearchParams(searchStr);

  const cleanRoute = (routePart || '').replace(/^\/+/, '').replace(/\/+$/, '').toLowerCase();
  const refKey = params.get('ref') || null;
  const editId = params.get('editId') || params.get('edit') || null;

  // If path is admin route (/yonetim, /giris, /login)
  if (pathname.startsWith('/yonetim') || pathname === '/giris' || pathname === '/login') {
    let sub = cleanRoute;
    if (!sub) {
      sub = pathname.replace(/^\/yonetim\/?/, '').replace(/\/$/, '');
    }
    const targetTab = SLUG_TO_TAB[sub] || 'dashboard';
    return { tab: targetTab, slug: sub || 'dashboard', refKey, editId, params };
  }

  // PUBLIC SITE ROUTING
  let targetTab = 'public-home';
  let slug = cleanRoute;

  if (cleanRoute === 'salonlar' || cleanRoute === 'salonlarimiz' || cleanRoute === 'public-halls') {
    targetTab = 'public-halls';
    slug = 'salonlar';
  } else if (cleanRoute === '360-tur' || cleanRoute === 'sanal-tur' || cleanRoute === 'public-virtual-tour') {
    targetTab = 'public-virtual-tour';
    slug = '360-tur';
  } else if (cleanRoute === 'organizasyonlar' || cleanRoute === 'public-organizations') {
    targetTab = 'public-organizations';
    slug = 'organizasyonlar';
  } else if (cleanRoute === 'videolar' || cleanRoute === 'public-videos') {
    targetTab = 'public-videos';
    slug = 'videolar';
  } else if (cleanRoute === 'blog' || cleanRoute === 'public-blog') {
    targetTab = 'public-blog';
    slug = 'blog';
  } else if (cleanRoute === 'hakkimizda' || cleanRoute === 'kurumsal' || cleanRoute === 'public-about') {
    targetTab = 'public-about';
    slug = 'hakkimizda';
  } else if (cleanRoute === 'iletisim' || cleanRoute === 'public-contact') {
    targetTab = 'public-contact';
    slug = 'iletisim';
  } else if (cleanRoute === 'musteri-giris' || cleanRoute === 'public-customer-login') {
    targetTab = 'public-customer-login';
    slug = 'musteri-giris';
  } else if (cleanRoute === 'musteri-kayit' || cleanRoute === 'public-customer-register') {
    targetTab = 'public-customer-register';
    slug = 'musteri-kayit';
  } else if (cleanRoute === '' || cleanRoute === 'public-home' || cleanRoute === 'home') {
    targetTab = 'public-home';
    slug = '';
  } else {
    // Check if pathname has a specific public route
    if (pathname === '/salonlar') targetTab = 'public-halls';
    else if (pathname === '/360-tur') targetTab = 'public-virtual-tour';
    else if (pathname === '/organizasyonlar') targetTab = 'public-organizations';
    else if (pathname === '/videolar') targetTab = 'public-videos';
    else if (pathname === '/blog') targetTab = 'public-blog';
    else if (pathname === '/hakkimizda') targetTab = 'public-about';
    else targetTab = 'public-home';
  }
  return { tab: targetTab, slug, refKey, editId, params };
};

export const getHashTab = () => {
  return parseHashRoute().tab;
};

export async function fetchWithRetry(url, options = {}, retries = 3, backoff = 500) {
  try {
    const res = await fetch(url, options);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res;
  } catch (err) {
    if (retries <= 0) throw err;
    await new Promise(r => setTimeout(r, backoff));
    return fetchWithRetry(url, options, retries - 1, backoff * 2);
  }
}


