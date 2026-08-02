import json

with open("scratch/db_system_settings.json", "r", encoding="utf-8") as f:
    db = json.load(f)

db["systemVersion"] = "v1.5.05"
release_note = {
    "version": "v1.5.05",
    "date": "02 Ağustos 2026",
    "title": "fix(calendar): Çapraz Salon Doluluk Önizleme & 5 Ağustos Görünürlük Düzeltmesi (Cross-Venue Mini Calendar Occupancy Engine)",
    "description": "Yeni rezervasyon oluşturma sihirbazındaki canlı takvim önizleme şeridi geliştirildi. 5 Ağustos rezervasyonunun 'Yakut Panorama Salon' için kayıtlı olmasından dolayı 'Kraliyet Balo Salonu' seçiliyken BOŞ görünmesi durumu düzeltildi. Takvim şeridine 'DİĞER DOLU' (Amber renkli) rozet ve detaylı tooltip bilgilendirmesi eklenerek salonlar arası doluluk farkındalığı %100 seviyesine çıkarıldı."
}

db["versionHistory"].insert(0, release_note)

with open("scratch/db_system_settings.json", "w", encoding="utf-8") as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Bumped system version to v1.5.05 in db_system_settings.json")
