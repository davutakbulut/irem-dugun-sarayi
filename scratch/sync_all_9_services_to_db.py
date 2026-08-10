import os
import json

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

print("1. Updating scratch/db_services.json with 9 services ...")
with open('scratch/db_services.json', 'w', encoding='utf-8') as f:
    json.dump(services_9, f, indent=2, ensure_ascii=False)

print("2. Updating scratch/db_system_settings.json with 9 services ...")
if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['services'] = services_9
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)

print("ALL 9 SERVICES SAVED TO DB SUCCESSFULLY!")
