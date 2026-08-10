import os
import json

venue_v1_only = [
  {
    "id": "v1",
    "name": "Kraliyet Balo Salonu",
    "category": "Kapalı Salon",
    "capacity": 750,
    "price": 100000,
    "costPrice": 35000,
    "deposit": 15000,
    "occupancyRate": 85,
    "description": "Yüksek tavanlı, kristal avizeli, iklimlendirme sistemli ve lüks sahne düzenine sahip ana balo salonumuz.",
    "image": "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80",
    "images": [
      "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80"
    ],
    "eventTypes": ["Düğün", "Nişan", "Kurumsal Kokteyl", "Mezuniyet"],
    "availableServices": ["s1", "s-tavuk-menu", "s2", "s3"]
  }
]

services_4_only = [
  { "id": "s1", "order": 1, "sortOrder": 1, "name": "Gurme Yemek Servisi (Et Menü)", "category": "Catering", "price": 750, "costPrice": 290, "pricingType": "per_person", "description": "Et Kavurma, Et Döner, Patates Püresi, Izgara Sebze, Tatlı, İçecek", "image": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80" },
  { "id": "s-tavuk-menu", "order": 2, "sortOrder": 2, "name": "Gurme Yemek Servisi (Tavuk Menü)", "category": "Genel Hizmetler", "price": 600, "costPrice": 200, "pricingType": "per_person", "description": "Tavuk Sote, Pilav, Patates püresi, Izgara Sebze, Tatlı, İçecek", "image": "https://images.unsplash.com/photo-1555244162-803834f70033?auto=format&fit=crop&w=600&q=80" },
  { "id": "s3", "order": 3, "sortOrder": 3, "name": "Canlı Müzik Orkestrası & DJ", "category": "Eğlence", "price": 25000, "costPrice": 15000, "pricingType": "fixed", "description": "6 kişilik orkestra ve DJ.", "image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&w=600&q=80" },
  { "id": "s2", "order": 4, "sortOrder": 4, "name": "Fotoğraf & 4K Video Paketi", "category": "Medya", "price": 18000, "costPrice": 10000, "pricingType": "fixed", "description": "Dış çekim, 4K sinematik albüm.", "image": "https://images.unsplash.com/photo-1537633552985-df8429e8048b?auto=format&fit=crop&w=600&q=80" }
]

print("1. Writing 1 venue (Kraliyet Balo Salonu) to scratch/db_venues.json ...")
with open('scratch/db_venues.json', 'w', encoding='utf-8') as f:
    json.dump(venue_v1_only, f, indent=2, ensure_ascii=False)

print("2. Writing 4 services to scratch/db_services.json ...")
with open('scratch/db_services.json', 'w', encoding='utf-8') as f:
    json.dump(services_4_only, f, indent=2, ensure_ascii=False)

print("3. Updating scratch/db_system_settings.json ...")
if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['venues'] = venue_v1_only
    sys_data['services'] = services_4_only
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)
        f.truncate()

print("SYNCED USER DESIRED VENUES (1) AND SERVICES (4) TO DB SUCCESSFULLY!")
