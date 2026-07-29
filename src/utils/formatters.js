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
