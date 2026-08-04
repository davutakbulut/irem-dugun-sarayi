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
  '': 'dashboard',
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

  let targetTab = 'public-home';
  let slug = routePart || '';

  // 1. PUBLIC ROUTES (Default for root / or explicit public paths)
  if (pathname === '/' || pathname === '' || pathname === '/index.html') {
    if (routePart.startsWith('yonetim')) {
      const sub = routePart.replace(/^yonetim\/?/, '');
      targetTab = SLUG_TO_TAB[sub] || 'dashboard';
      slug = sub || 'dashboard';
    } else if (routePart === 'giris' || routePart === 'login') {
      targetTab = 'login';
      slug = 'giris';
    } else if (routePart && SLUG_TO_TAB[routePart]) {
      targetTab = SLUG_TO_TAB[routePart];
      slug = routePart;
    } else {
      targetTab = 'public-home';
      slug = '';
    }
  } else if (pathname === '/salonlar' || pathname === '/salonlarimiz') {
    targetTab = 'public-halls';
    slug = 'salonlar';
  } else if (pathname === '/360-tur' || pathname === '/sanal-tur') {
    targetTab = 'public-virtual-tour';
    slug = '360-tur';
  } else if (pathname === '/organizasyonlar' || pathname === '/organizasyon-paketleri') {
    targetTab = 'public-organizations';
    slug = 'organizasyonlar';
  } else if (pathname === '/videolar' || pathname === '/video-galeri') {
    targetTab = 'public-videos';
    slug = 'videolar';
  } else if (pathname === '/blog' || pathname === '/dugun-rehberi') {
    targetTab = 'public-blog';
    slug = 'blog';
  } else if (pathname === '/hakkimizda' || pathname === '/kurumsal') {
    targetTab = 'public-about';
    slug = 'hakkimizda';
  } else if (pathname === '/iletisim' || pathname === '/bize-ulasin') {
    targetTab = 'public-contact';
    slug = 'iletisim';
  } else if (pathname === '/musteri-giris' || pathname === '/vip-giris') {
    targetTab = 'public-customer-login';
    slug = 'musteri-giris';
  } else if (pathname === '/musteri-kayit' || pathname === '/cift-basvuru') {
    targetTab = 'public-customer-register';
    slug = 'musteri-kayit';
  } else if (pathname === '/giris' || pathname === '/login') {
    targetTab = 'login';
    slug = 'giris';
  } else if (pathname.startsWith('/medya') || pathname.startsWith('/m/')) {
    targetTab = 'media';
    slug = 'media';
  } else if (pathname.startsWith('/yonetim')) {
    let sub = pathname.replace(/^\/yonetim\/?/, '').replace(/\/$/, '');
    if (!sub && routePart) sub = routePart;
    targetTab = SLUG_TO_TAB[sub] || 'dashboard';
    slug = sub || 'dashboard';
  } else {
    targetTab = 'simulasyon-404';
    slug = '404';
  }

  const refKey = params.get('ref') || null;
  const editId = params.get('editId') || params.get('edit') || null;
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


