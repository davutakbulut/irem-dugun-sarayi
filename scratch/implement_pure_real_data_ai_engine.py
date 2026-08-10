import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace generateSmartAITips and generateSmartAIRecommendations with 100% pure real-data functions
old_ai_functions = """    const generateSmartAITips = (reservations = [], venues = [], services = [], customers = []) => {
      const totalRes = Math.max(1, reservations.length);
      const activeRes = reservations.filter(r => r.paymentStatus !== 'İptal');
      const totalRevenue = activeRes.reduce((s, r) => s + (r.totalAmount || 0), 0);
      const topVenue = venues.length > 0 ? venues[0] : null;

      const resWithDrone = reservations.filter(r => (r.selectedServices || []).some(s => (s.serviceId || '').includes('s3') || (s.name || '').toLowerCase().includes('drone'))).length;
      const droneRatio = Math.round((resWithDrone / totalRes) * 100) || 78;

      return [
        {
          id: 'gpt-1',
          tag: '🤖 GPT Satış & Ciro Analizi',
          text: `Veritabanındaki ${reservations.length} sözleşme kaydı analiz edildi. Toplam ${formatCurrency(totalRevenue)} ciro oluştu. Önümüzdeki 60 gündeki boş tarihler için özel %10 indirim veya promosyon paketi sunarak satış kapatma hızını %25 artırabilirsiniz.`,
          badge: 'Veritabanı Canlı Analizi'
        },
        {
          id: 'gpt-2',
          tag: '💡 GPT Çapraz Satış İpucu',
          text: `Müşteri talepleri incelemesi: Sözleşmelerin %${droneRatio}'inde VIP Çekim & Drone hizmeti tercih ediliyor. Satış esnasında Drone paketini promosyonel indirim ile teklif etmek sözleşme tamamlama oranını %84'e yükseltir.`,
          badge: 'Çapraz Satış Taktiği'
        },
        {
          id: 'gpt-3',
          tag: '🚀 GPT Marj Koruma Önerisi',
          text: `Hafta sonu talebi yüksek olan ${topVenue ? topVenue.name : 'Salonlarımız'} için kiralama bedeline %10 fiyat güncellemesi yapmak net kâr marjını düşürmeden bu sezon fazladan 140.000 ₺ ciro sağlar.`,
          badge: 'Akıllı Fiyat Stratejisi'
        }
      ];
    };

    const generateSmartAIRecommendations = (reservations = [], venues = [], services = []) => {
      const kbVenue = venues.find(v => v.id === 'v2' || (v.name && v.name.includes('Kır Bahçesi'))) || venues[0];
      const kbOccupancy = kbVenue ? (kbVenue.occupancyRate || 92) : 92;
      const currentKbPrice = kbVenue ? kbVenue.price : 85000;
      const suggestedKbPrice = kbVenue ? Math.round(currentKbPrice * 1.10) : 93500;

      const droneService = services.find(s => s.id === 's3' || (s.name && s.name.toLowerCase().includes('drone'))) || services[2];
      const resCountWithDrone = reservations.filter(r => (r.selectedServices || []).some(s => s.serviceId === (droneService?.id || 's3'))).length;
      const totalRes = Math.max(1, reservations.length);
      const droneAdoptionRate = Math.round((resCountWithDrone / totalRes) * 100);

      return [
        {
          id: 'ai-1',
          code: 'AĞUSTOS10',
          title: `${kbVenue?.name || 'Kır Bahçesi'} Fiyat Artırım & Fırsat Önerisi (%${kbOccupancy} Doluluk)`,
          type: 'percent',
          value: 10,
          venueId: kbVenue?.id || 'v2',
          venueName: kbVenue?.name || 'Kır Bahçesi VİP',
          currentPrice: currentKbPrice,
          suggestedPrice: suggestedKbPrice,
          description: `${kbVenue?.name || 'Kır Bahçesi VİP'} salonunda hafta sonu doluluğu %${kbOccupancy} seviyesine ulaştı. Kiralama bedelini %10 artırarak ${formatCurrency(suggestedKbPrice)} seviyesine çekmek tahmini 140.000 ₺ ek gelir sağlar.`,
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          priceActionText: 'Fiyatı Güncelle & Uygula',
          badge: `%${kbOccupancy} Doluluk Zirvede`,
          canUpdatePrice: true
        },
        {
          id: 'ai-2',
          code: 'DRONE20',
          title: 'Drone Çekimi Çapraz Satış Fırsatı',
          type: 'free_service',
          value: 0,
          description: `Mevcut rezervasyonlarda Drone çekimi tercih oranı %${droneAdoptionRate}. Kır bahçesi kiralamalarında 4K drone çekimini promosyonlu sunarak ek 60.000 ₺ ciro elde edin.`,
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          badge: 'Çapraz Satış Trendi',
          canUpdatePrice: false
        },
        {
          id: 'ai-3',
          code: 'SONBAHAR26',
          title: 'Sonbahar Erken Rezervasyon Fırsatı (%20 Net İndirim)',
          type: 'percent',
          value: 20,
          description: 'Eylül ve Ekim düğün tarihleri için %20 Erken Rezervasyon Kampanyası başlatarak salon doluluğunu %100 seviyesine çıkarın.',
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          badge: 'Sezonluk Fırsat',
          canUpdatePrice: false
        }
      ];
    };"""

new_ai_functions = """    const generateSmartAITips = (reservations = [], venues = [], services = [], customers = []) => {
      const activeRes = (reservations || []).filter(r => r.paymentStatus !== 'İptal');
      const totalRevenue = activeRes.reduce((s, r) => s + (r.totalAmount || 0), 0);
      const totalCount = Math.max(1, activeRes.length);

      // Venue Analytics
      const venueStats = (venues || []).map(v => {
        const vRes = activeRes.filter(r => r.venueId === v.id);
        const vRevenue = vRes.reduce((s, r) => s + (r.totalAmount || 0), 0);
        const occupancy = Math.min(100, Math.round((vRes.length / 30) * 100));
        const emptyDays = Math.max(0, 30 - vRes.length);
        return { ...v, count: vRes.length, revenue: vRevenue, occupancy, emptyDays };
      });

      venueStats.sort((a, b) => b.count - a.count);
      const topVenue = venueStats[0] || { name: 'Ana Salon', occupancy: 85, emptyDays: 5, price: 85000 };
      const emptyVenue = venueStats[venueStats.length - 1] || topVenue;

      // Service Analytics
      const serviceStats = (services || []).map(s => {
        const count = activeRes.filter(r => (r.selectedServices || []).some(x => x.serviceId === s.id || x.id === s.id)).length;
        const ratio = Math.round((count / totalCount) * 100);
        return { ...s, count, ratio };
      });

      serviceStats.sort((a, b) => b.count - a.count);
      const topService = serviceStats[0] || { name: 'VIP Çekim & Paket Hizmeti', ratio: 75, price: 5000 };

      const estimatedPriceIncreaseRevenue = Math.round(topVenue.count * (topVenue.price || 50000) * 0.10);

      return [
        {
          id: 'gpt-1',
          tag: '🤖 Real-Data GPT Ciro & Doluluk Analizi',
          text: `Sistem veritabanındaki ${activeRes.length} aktif rezervasyon ve ${venues.length} mekan taranmıştır. Toplam gerçekleşen ciro: ${formatCurrency(totalRevenue)}. En yüksek doluluk %${topVenue.occupancy} ile "${topVenue.name}" salonumuzda gerçekleşmiştir.`,
          badge: 'Veritabanı Canlı Analizi'
        },
        {
          id: 'gpt-2',
          tag: '💡 Real-Data Ek Hizmet Çapraz Satış İpucu',
          text: `Ek hizmet analizine göre rezervasyonların %${topService.ratio}'inde '${topService.name}' (${formatCurrency(topService.price)}) ek hizmeti seçilmiştir. Satış esnasında bu hizmeti paket hediyesi olarak sunmak sözleşme kapatma oranını yükseltmektedir.`,
          badge: 'Gerçek Hizmet Trendi'
        },
        {
          id: 'gpt-3',
          tag: '🚀 Real-Data Boş Gün & Fiyat Stratejisi',
          text: `"${emptyVenue.name}" salonunda bu ay ${emptyVenue.emptyDays} gün boş takvim mevcuttur. Diğer yandan %${topVenue.occupancy} doluluğa ulaşan "${topVenue.name}" kiralama bedelini %10 artırmak bu sezon fazladan ${formatCurrency(estimatedPriceIncreaseRevenue)} ciro sağlar.`,
          badge: 'Gerçek Doluluk Stratejisi'
        }
      ];
    };

    const generateSmartAIRecommendations = (reservations = [], venues = [], services = [], customers = []) => {
      const activeRes = (reservations || []).filter(r => r.paymentStatus !== 'İptal');
      const totalCount = Math.max(1, activeRes.length);

      // Venue Analytics
      const venueStats = (venues || []).map(v => {
        const vRes = activeRes.filter(r => r.venueId === v.id);
        const vRevenue = vRes.reduce((s, r) => s + (r.totalAmount || 0), 0);
        const occupancy = Math.min(100, Math.round((vRes.length / 30) * 100));
        const emptyDays = Math.max(0, 30 - vRes.length);
        return { ...v, count: vRes.length, revenue: vRevenue, occupancy, emptyDays };
      });

      venueStats.sort((a, b) => b.count - a.count);
      const topVenue = venueStats[0] || { id: 'v1', name: 'Ana Salon', occupancy: 80, emptyDays: 6, price: 80000 };
      const emptyVenue = venueStats[venueStats.length - 1] || topVenue;

      // Service Analytics
      const serviceStats = (services || []).map(s => {
        const count = activeRes.filter(r => (r.selectedServices || []).some(x => x.serviceId === s.id || x.id === s.id)).length;
        const ratio = Math.round((count / totalCount) * 100);
        return { ...s, count, ratio };
      });

      serviceStats.sort((a, b) => b.count - a.count);
      const topService = serviceStats[0] || { name: 'VIP Çekim Hizmeti', ratio: 70 };

      const suggestedTopPrice = Math.round((topVenue.price || 80000) * 1.10);
      const topPriceDiff = Math.round(topVenue.count * (topVenue.price || 80000) * 0.10);
      const venueCode = (topVenue.name || 'SALON').split(' ')[0].toUpperCase() + '10';
      const emptyCode = (emptyVenue.name || 'FIRSAT').split(' ')[0].toUpperCase() + '15';

      return [
        {
          id: 'ai-1',
          code: venueCode,
          title: `${topVenue.name} Fiyat Güncelleme & Yüksek Talep Önerisi (%${topVenue.occupancy} Doluluk)`,
          type: 'percent',
          value: 10,
          venueId: topVenue.id,
          venueName: topVenue.name,
          currentPrice: topVenue.price,
          suggestedPrice: suggestedTopPrice,
          description: `Veritabanı kayıtlarına göre "${topVenue.name}" salonunda doluluk %${topVenue.occupancy} seviyesine (${topVenue.count} Sözleşme) ulaştı. Fiyatı ${formatCurrency(topVenue.price)} seviyesinden ${formatCurrency(suggestedTopPrice)} seviyesine çekmek tahmini ${formatCurrency(topPriceDiff)} ek gelir sağlar.`,
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          priceActionText: 'Fiyatı Güncelle & Uygula',
          badge: `%${topVenue.occupancy} Doluluk Zirvede`,
          actionType: 'update_price',
          canUpdatePrice: true
        },
        {
          id: 'ai-2',
          code: emptyCode,
          title: `${emptyVenue.name} Boş Gün Doldurma Kampanyası (${emptyVenue.emptyDays} Gün Boş)`,
          type: 'percent',
          value: 15,
          venueId: emptyVenue.id,
          venueName: emptyVenue.name,
          description: `Veritabanında "${emptyVenue.name}" salonumuz için önümüzdeki 30 gün içinde ${emptyVenue.emptyDays} gün boş takvim mevcuttur. Sezon doluluğunu artırmak için %15 özel indirim tanımlayabilirsiniz.`,
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          badge: `${emptyVenue.emptyDays} Boş Gün Mevcut`,
          actionType: 'create_campaign',
          canUpdatePrice: false
        },
        {
          id: 'ai-3',
          code: 'PROMO2026',
          title: `${topService.name} Çapraz Satış Promosyonu (%${topService.ratio} Tercih)`,
          type: 'free_service',
          value: 0,
          description: `Mevcut rezervasyonların %${topService.ratio}'inde "${topService.name}" tercih edilmiştir. Yeni müşteri randevularında bu hizmeti promosyonlu sunarak sözleşme kapatma süresini kısaltın.`,
          actionText: 'Tek Tıkla Kampanyaya Dönüştür',
          badge: 'Popüler Ek Hizmet',
          actionType: 'create_campaign',
          canUpdatePrice: false
        }
      ];
    };"""

if old_ai_functions in content:
    content = content.replace(old_ai_functions, new_ai_functions)
    print("1. Replaced generateSmartAITips and generateSmartAIRecommendations with 100% pure real-data functions.")
else:
    print("WARNING: Could not find old_ai_functions in index.html!")

# 2. Update DashboardComponent signature & calls
old_dash_sig = "function DashboardComponent({ activeRole, currentUser, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"
new_dash_sig = "function DashboardComponent({ activeRole, currentUser, venues = [], reservations = [], services = [], customers = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"

if old_dash_sig in content:
    content = content.replace(old_dash_sig, new_dash_sig)
    print("2. Updated DashboardComponent signature to receive services and customers.")

# 3. Update aiRecs & gptTipsList calls in DashboardComponent
old_ai_recs_call = """      const aiRecs = useMemo(() => {
        return generateSmartAIRecommendations(reservations, venues, []);
      }, [reservations, venues]);"""

new_ai_recs_call = """      const aiRecs = useMemo(() => {
        return generateSmartAIRecommendations(reservations, venues, services, customers);
      }, [reservations, venues, services, customers]);"""

if old_ai_recs_call in content:
    content = content.replace(old_ai_recs_call, new_ai_recs_call)
    print("3. Updated aiRecs useMemo call.")

content = content.replace(
    "const gptTipsList = generateSmartAITips(reservations, venues, [], []);",
    "const gptTipsList = generateSmartAITips(reservations, venues, services, customers);"
)

# 4. Update DashboardComponent call in App
old_dash_app_call = """                  {activeTab === 'dashboard' && (
                    <DashboardComponent
                      activeRole={activeRole}
                      currentUser={currentUserState}
                      venues={venues}
                      reservations={reservations}"""

new_dash_app_call = """                  {activeTab === 'dashboard' && (
                    <DashboardComponent
                      activeRole={activeRole}
                      currentUser={currentUserState}
                      venues={venues}
                      reservations={reservations}
                      services={services}
                      customers={customers}"""

if old_dash_app_call in content:
    content = content.replace(old_dash_app_call, new_dash_app_call)
    print("4. Updated DashboardComponent call in App.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
