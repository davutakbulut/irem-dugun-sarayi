import os
import json

venues_5 = [
  {
    "id": "v1",
    "name": "Kraliyet Balo Salonu (Bosphorus Gold)",
    "category": "Kapalı Balo Salonu",
    "capacity": 1000,
    "price": 85000,
    "costPrice": 45000,
    "deposit": 20000,
    "occupancyRate": 85,
    "description": "Kristal avizeler, yüksek tavan, altın varaklı dekorasyon ve dev sahneli lüks kapalı balo salonu.",
    "image": "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80",
      "https://images.unsplash.com/photo-1544078751-58fee2d8a03b?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Düğün", "Gala", "Kurumsal Etkinlik", "Sünnet Düğünü"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
  },
  {
    "id": "v2",
    "name": "VIP Kır Bahçesi & Park",
    "category": "Açık Hava & Kır Bahçesi",
    "capacity": 1500,
    "price": 95000,
    "costPrice": 50000,
    "deposit": 25000,
    "occupancyRate": 92,
    "description": "Sapanca göl manzaralı, doğal çim zeminli, asırlık ağaçlar altında 1500 kişilik kır düğünü konsepti.",
    "image": "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1465495976277-4387d4b0b4c6?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Düğün", "Nişan", "Kına", "Kokteyl"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
  },
  {
    "id": "v3",
    "name": "Teras Salon Silver Rose",
    "category": "Teras Salon",
    "capacity": 600,
    "price": 65000,
    "costPrice": 35000,
    "deposit": 15000,
    "occupancyRate": 78,
    "description": "Göl ve şehir manzaralı geniş teras alanı, modern gümüş ve pembe tonlarında lüks dekorasyon.",
    "image": "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1527529482837-4698179dc6ce?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Nişan", "Kına", "Sünnet Düğünü", "Kokteyl"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
  },
  {
    "id": "v4",
    "name": "Yakut Panorama Salon",
    "category": "Panoramik Balo Salonu",
    "capacity": 800,
    "price": 75000,
    "costPrice": 40000,
    "deposit": 18000,
    "occupancyRate": 80,
    "description": "360 derece cam panoramik mimari, göl manzarası ve yakut konseptli lüks aydınlatma tasarımı.",
    "image": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Düğün", "Gala", "Kurumsal Etkinlik"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
  },
  {
    "id": "v5",
    "name": "Pırlanta Davet & Balo",
    "category": "Butik Balo Salonu",
    "capacity": 450,
    "price": 55000,
    "costPrice": 30000,
    "deposit": 12000,
    "occupancyRate": 70,
    "description": "Butik nişan, kına ve samimi davetler için tasarlanmış şık pırlanta konseptli balo salonu.",
    "image": "https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1520854221256-17451cc331bf?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Nişan", "Kına", "Sünnet Düğünü", "Butik Davet"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
  }
]

services_9 = [
  { "id": "s1", "order": 1, "sortOrder": 1, "name": "Gurme Yemek Servisi (Et Menü)", "category": "Catering", "price": 750, "costPrice": 290, "pricingType": "per_person", "description": "Ordövr, Dana Biftek, düğün pastası.", "image": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80" },
  { "id": "s-tavuk-menu", "order": 2, "sortOrder": 2, "name": "Gurme Yemek Servisi (Tavuk Menü)", "category": "Genel Hizmetler", "price": 600, "costPrice": 200, "pricingType": "per_person", "description": "Tavuk Sote, Pilav, Patates püresi, Izgara Sebze", "image": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80" },
  { "id": "s3", "order": 3, "sortOrder": 3, "name": "Canlı Müzik Orkestrası & DJ", "category": "Eğlence", "price": 25000, "costPrice": 15000, "pricingType": "fixed", "description": "6 kişilik orkestra ve DJ.", "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80" },
  { "id": "s4", "order": 4, "sortOrder": 4, "name": "Masa & Sahne Süsleme", "category": "Dekorasyon", "price": 15000, "costPrice": 8000, "pricingType": "fixed", "description": "Canlı çiçekler ve şamdanlar.", "image": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=600&q=80" },
  { "id": "s5", "order": 5, "sortOrder": 5, "name": "Volkan, Konfeti & Işık Şovu", "category": "Efekt", "price": 8000, "costPrice": 4000, "pricingType": "fixed", "description": "Soğuk volkan ve konfeti.", "image": "https://images.unsplash.com/photo-1492684223066-81342ee5ff30?auto=format&fit=crop&w=600&q=80" },
  { "id": "s6", "order": 6, "sortOrder": 6, "name": "VİP Karşılama Kokteyli & İkram Barı", "category": "Catering", "price": 150, "costPrice": 90, "pricingType": "per_person", "description": "Karşılama şampanyası, kanapeler ve taze meyve barları.", "image": "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?auto=format&fit=crop&w=600&q=80" },
  { "id": "s7", "order": 7, "sortOrder": 7, "name": "Profesyonel Garson & Servis Ekibi", "category": "Servis", "price": 12000, "costPrice": 7000, "pricingType": "per_person", "description": "10 kişilik eğitimli üniformalı servis ekibi.", "image": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=600&q=80" },
  { "id": "s8", "order": 8, "sortOrder": 8, "name": "Çocuk Oyun Alanı & Palyaço", "category": "Eğlence", "price": 6000, "costPrice": 3500, "pricingType": "fixed", "description": "Çocuk animatörü, yüz boyama ve eğlenceli oyun alanı.", "image": "https://images.unsplash.com/photo-1502086223501-7ea6ecd79368?auto=format&fit=crop&w=600&q=80" },
  { "id": "s2", "order": 9, "sortOrder": 9, "name": "Fotoğraf & 4K Video Paketi", "category": "Medya", "price": 18000, "costPrice": 10000, "pricingType": "fixed", "description": "Dış çekim, 4K sinematik albüm.", "image": "https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80" }
]

print("1. Writing 5 venues to scratch/db_venues.json ...")
with open('scratch/db_venues.json', 'w', encoding='utf-8') as f:
    json.dump(venues_5, f, indent=2, ensure_ascii=False)

print("2. Writing 9 services to scratch/db_services.json ...")
with open('scratch/db_services.json', 'w', encoding='utf-8') as f:
    json.dump(services_9, f, indent=2, ensure_ascii=False)

print("3. Rebuilding db_system_settings.json with full entities ...")
if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['venues'] = venues_5
    sys_data['services'] = services_9
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)

print("COMPLETED FULL VENUES (5) AND SERVICES (9) SYNC!")
