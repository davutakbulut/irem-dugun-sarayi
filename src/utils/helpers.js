// Helper utilities for İrem Düğün Sarayı & Organizasyon Şirketi

export function formatCurrency(amount) {
  if (amount === undefined || amount === null) return '₺0';
  return new Intl.NumberFormat('tr-TR', {
    style: 'currency',
    currency: 'TRY',
    maximumFractionDigits: 0
  }).format(amount);
}

export function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('tr-TR', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  }).format(date);
}

export function checkBookingCollision(reservations, venueId, date, timeSlot, excludeId = null) {
  return reservations.find(r => {
    if (excludeId && r.id === excludeId) return false;
    return r.venueId === venueId && r.date === date && r.timeSlot === timeSlot;
  });
}

export function generateWhatsAppLink(phone, text = "Merhabalar Ben İrem Düğün Sarayı'ndan sizlere ulaşıyorum. Rezervasyonunuz hakkında.") {
  const cleanPhone = phone ? phone.replace(/[^0-9]/g, '') : '';
  const encodedText = encodeURIComponent(text);
  return `https://wa.me/${cleanPhone}?text=${encodedText}`;
}

export function generateWelcomeEmailHTML(name, email, password) {
  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
    .card { max-width: 600px; margin: 0 auto; background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 32px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .logo { font-size: 24px; font-weight: bold; color: #d97706; text-transform: uppercase; letter-spacing: 1.5px; text-align: center; margin-bottom: 24px; }
    .credentials { background: #0f172a; padding: 16px; border-radius: 8px; border-left: 4px solid #f59e0b; margin: 20px 0; }
    .footer { font-size: 12px; color: #94a3b8; text-align: center; margin-top: 32px; border-top: 1px solid #334155; padding-top: 16px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">✨ İrem Düğün Sarayı ✨</div>
    <h2 style="color: #f8fafc;">Erişiminiz Açıldı!</h2>
    <p>Merhaba <strong>${name}</strong>,</p>
    <p>İrem Düğün Sarayı’nı tercih ettiğiniz için bizi çok mutlu ettiniz. Aşağıdaki bilgilerle bundan sonra tüm süreçleri anlık ve sorunsuz takip edebileceksiniz!</p>
    
    <div class="credentials">
      <p style="margin: 4px 0;"><strong>Kullanıcı Adı (E-posta):</strong> ${email}</p>
      <p style="margin: 4px 0;"><strong>Geçici Şifreniz:</strong> <code style="background: #334155; padding: 2px 6px; border-radius: 4px; color: #f59e0b;">${password}</code></p>
    </div>

    <p style="font-weight: 600; color: #fbbf24;">Bu sistemle neler yapabilirsiniz?</p>
    <ul style="color: #cbd5e1; line-height: 1.6;">
      <li>📸 Tüm davetlilerinizin etkinlikte çekildiği fotoğrafları yüklemesi için özel alan oluşturabilirsiniz!</li>
      <li>🎬 Sana iletilecek olan tüm sinematik video & albüm içeriklerini buradan takip edebilirsin!</li>
      <li>📋 Davet detaylarını, saatlik akış planını ve ödeme bilgini dilediğin an görüntüleyebilirsin!</li>
    </ul>

    <div class="footer">
      <strong style="color: #f59e0b;">İREM DÜĞÜN SARAYI & ORGANİZASYON</strong><br>
      Sakarya, Sapanca Gölü Kenarı | 📞 +90 555 555 55 55 | 🌐 @iremdugunsarayi
    </div>
  </div>
</body>
</html>
  `;
}

export function generateReservationEmailHTML(reservation, venueName, serviceDetails = []) {
  const serviceRowsHTML = serviceDetails.map(s => `
    <tr>
      <td style="padding: 10px; border-bottom: 1px solid #334155;">${s.name}</td>
      <td style="padding: 10px; border-bottom: 1px solid #334155; text-align: center;">${s.quantity}</td>
      <td style="padding: 10px; border-bottom: 1px solid #334155; text-align: right;">${formatCurrency(s.total)}</td>
    </tr>
  `).join('');

  return `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #0f172a; color: #f8fafc; margin: 0; padding: 20px; }
    .card { max-width: 650px; margin: 0 auto; background: #1e293b; border-radius: 16px; border: 1px solid #334155; padding: 32px; }
    .logo { font-size: 24px; font-weight: bold; color: #d97706; text-align: center; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-top: 16px; }
    th { background: #0f172a; color: #f59e0b; padding: 12px; text-align: left; }
    .total-box { background: #0f172a; padding: 16px; border-radius: 10px; margin-top: 24px; border: 1px solid #d97706; }
    .footer { font-size: 12px; color: #94a3b8; text-align: center; margin-top: 32px; border-top: 1px solid #334155; padding-top: 16px; }
  </style>
</head>
<body>
  <div class="card">
    <div class="logo">👑 İrem Düğün Sarayı</div>
    <h2 style="color: #f8fafc; text-align: center;">Rezervasyonunuz Başarıyla Oluşturuldu!</h2>
    <p>Merhaba <strong>${reservation.customerName}</strong>,</p>
    <p>İrem Düğün Sarayı’nı tercih ettiğiniz için teşekkür ederiz. Rezervasyon dökümünüz aşağıdadır:</p>

    <div style="background: #0f172a; padding: 16px; border-radius: 8px; margin: 16px 0;">
      <p style="margin: 4px 0;">📌 <strong>Rezervasyon Kodu:</strong> ${reservation.id}</p>
      <p style="margin: 4px 0;">🏛️ <strong>Düğün Salonu:</strong> ${venueName}</p>
      <p style="margin: 4px 0;">📅 <strong>Etkinlik Tarihi:</strong> ${formatDate(reservation.date)} (${reservation.timeSlot})</p>
      <p style="margin: 4px 0;">👥 <strong>Davetli Sayısı:</strong> ${reservation.guestCount} Kişi</p>
    </div>

    <h3 style="color: #f59e0b; margin-top: 24px;">Alınan Hizmetler ve Fiyat Dökümü</h3>
    <table>
      <thead>
        <tr>
          <th>Hizmet / Kalem</th>
          <th style="text-align: center;">Adet/Kişi</th>
          <th style="text-align: right;">Tutar</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td style="padding: 10px; border-bottom: 1px solid #334155;">Salon Kiralama Bedeli (${venueName})</td>
          <td style="padding: 10px; border-bottom: 1px solid #334155; text-align: center;">1 Gün</td>
          <td style="padding: 10px; border-bottom: 1px solid #334155; text-align: right;">${formatCurrency(reservation.venuePrice)}</td>
        </tr>
        ${serviceRowsHTML}
      </tbody>
    </table>

    <div class="total-box">
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
        <span>Alt Toplam:</span>
        <strong>${formatCurrency(reservation.subtotal)}</strong>
      </div>
      ${reservation.discountAmount > 0 ? `
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px; color: #10b981;">
        <span>Kampanya İndirimi (${reservation.campaignCode}):</span>
        <strong>-${formatCurrency(reservation.discountAmount)}</strong>
      </div>` : ''}
      <div style="display: flex; justify-content: space-between; margin-bottom: 6px; color: #94a3b8;">
        <span>KDV (%20 Dahil):</span>
        <strong>${formatCurrency(reservation.vatAmount)}</strong>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 18px; font-weight: bold; color: #f59e0b; border-top: 1px solid #334155; padding-top: 8px;">
        <span>Genel Toplam Tutar:</span>
        <span>${formatCurrency(reservation.totalAmount)}</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 14px; color: #34d399; margin-top: 8px;">
        <span>Alınan Kapora:</span>
        <span>${formatCurrency(reservation.depositPaid)}</span>
      </div>
      <div style="display: flex; justify-content: space-between; font-size: 14px; color: #f87171; margin-top: 4px;">
        <span>Kalan Ödenecek Bakiye:</span>
        <span>${formatCurrency(reservation.remainingBalance)}</span>
      </div>
    </div>

    <p style="text-align: center; margin-top: 24px; font-style: italic; color: #cbd5e1;">"Hayallerinizdeki etkinliği unutulmaz kılmak bizim işimiz!"</p>

    <div class="footer">
      <strong style="color: #f59e0b;">İREM DÜĞÜN SARAYI & ORGANİZASYON</strong><br>
      Sakarya, Sapanca Gölü Kenarı | 📞 +90 555 555 55 55 | 🌐 @iremdugunsarayi
    </div>
  </div>
</body>
</html>
  `;
}
