import json
import random

venues = [
    {"id": "v1", "name": "Bosphorus Gold Balo Salonu"},
    {"id": "v2", "name": "VIP Kır Bahçesi & Park"},
    {"id": "v3", "name": "Teras Salon Silver Rose"},
    {"id": "v4", "name": "Yakut Panorama Salon"},
    {"id": "v5", "name": "Zümrüt VIP Balo Salonu"}
]

customer_first_names = [
    "Ahmet", "Mehmet", "Can", "Burak", "Emre", "Murat", "Oğuz", "Serkan", "Tolga", "Bora",
    "Gökhan", "Eren", "Kaan", "Uğur", "Onur", "Volkan", "Deniz", "Cem", "Alper", "Tarkan",
    "Erhan", "Selim", "Kerem", "Batuhan", "Metin", "Tayfun", "Sinan", "Levent", "Zafer", "Mert"
]

bride_names = [
    "Ayşe", "Fatma", "Zeynep", "Elif", "Merve", "Selin", "Sibel", "Derya", "Gözde", "Ceren",
    "Deniz", "Gamze", "Ece", "Melis", "Damla", "Aslı", "Gizem", "İrem", "Büşra", "Hande",
    "Dilek", "Tuğba", "Pınar", "Özge", "Sinem", "Didem", "Yasemin", "Beren", "Eda", "Defne"
]

last_names = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Arslan", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Eroğlu", "Yalçın", "Korkmaz", "Kan", "Güneş", "Gül", "Tekin", "Bulut", "Keser", "Gündüz"
]

campaigns = [
    {"code": "YAZ_FIRSATI_10", "name": "%10 Yaz Fırsatı İndirimi", "discount_pct": 10},
    {"code": "ERKEN_REZ_15", "name": "%15 Erken Rezervasyon Kampanyası", "discount_pct": 15},
    {"code": "HAFTAICI_SURPRIZ_20", "name": "%20 Hafta İçi Sürpriz İndirimi", "discount_pct": 20},
    {"code": "VIP_DUGUN_SPECIAL", "name": "15.000 TL VIP Düğün Kampanyası", "discount_pct": 0, "fixed_discount": 15000},
    {"code": "KINA_PAKET_SPECIAL", "name": "%12 Kına Paket İndirimi", "discount_pct": 12},
    {"code": "EK_HIZMET_PAKET", "name": "Ek Hizmet Paket İndirimi", "discount_pct": 5, "service_discount": 8000}
]

august_reservations = []
res_counter = 1

# Loop through all 31 days of August 2026
for day in range(1, 32):
    date_str = f"2026-08-{day:02d}"
    
    # Aug 1 2026 is Saturday!
    # Aug 1,2,7,8,9,14,15,16,21,22,23,28,29,30 -> double sessions on weekends & busy days
    weekday = (day - 1 + 5) % 7
    is_weekend = weekday in [5, 6] or day in [7, 14, 21, 28]  # Friday, Saturday, Sunday
    
    sessions = []
    if is_weekend:
        sessions = [("12:00-16:00", "Gündüz Düğünü / Sünnet"), ("19:00-23:00", "Gece Yemekli Düğün Balo")]
    else:
        sessions = [("19:00-23:00", "Yemekli Düğün & Nişan")]
        
    for session_idx, (time_slot, event_type) in enumerate(sessions):
        res_id = f"RES-2026-AUG-{day:02d}{'A' if len(sessions)>1 and session_idx==0 else ('B' if len(sessions)>1 else '')}"
        media_key = f"MEDIA-AUG26-{day:02d}{'A' if len(sessions)>1 and session_idx==0 else ('B' if len(sessions)>1 else '')}"
        
        groom = random.choice(customer_first_names)
        bride = random.choice(bride_names)
        surname = random.choice(last_names)
        customer_name = f"{groom} & {bride} {surname}"
        
        venue = random.choice(venues)
        guest_count = random.randrange(250, 950, 50)
        
        # Varied non-standard base venue price
        base_venue_price = random.randrange(45000, 125000, 2500)
        
        # Varied food service price per person
        unit_food_price = random.choice([320, 360, 390, 420, 480, 550, 620])
        
        selected_services = [
            {"serviceId": "s1", "serviceName": "Özel Menü İkramı", "quantity": guest_count, "unitPrice": unit_food_price, "isPaid": True}
        ]
        
        # Optional extra services
        if random.random() > 0.3:
            selected_services.append({"serviceId": "s2", "serviceName": "Canlı Orkestra & DJ Performatör", "quantity": 1, "unitPrice": random.randrange(18000, 32000, 1000), "isPaid": True})
        if random.random() > 0.4:
            selected_services.append({"serviceId": "s3", "serviceName": "4K Drone & Jimmy Jib Video Çekimi", "quantity": 1, "unitPrice": random.randrange(14000, 26000, 1000), "isPaid": True})
        if random.random() > 0.5:
            selected_services.append({"serviceId": "s4", "serviceName": "Sis & Lazer Işık Şovu", "quantity": 1, "unitPrice": random.randrange(9000, 16000, 500), "isPaid": False})
        if random.random() > 0.6:
            selected_services.append({"serviceId": "s5", "serviceName": "VIP Gelin Arabası & Şoför Hizmeti", "quantity": 1, "unitPrice": random.randrange(10000, 22000, 1000), "isPaid": False})
            
        services_sum = sum(s["quantity"] * s["unitPrice"] for s in selected_services)
        subtotal = base_venue_price + services_sum
        
        # Apply campaign or custom discount (%10, %15, %20, %25)
        campaign = random.choice(campaigns)
        discount_amount = 0
        
        if campaign["discount_pct"] > 0:
            discount_amount = int(subtotal * (campaign["discount_pct"] / 100.0))
        elif campaign.get("fixed_discount", 0) > 0:
            discount_amount = campaign["fixed_discount"]
        elif campaign.get("service_discount", 0) > 0:
            discount_amount = campaign["service_discount"]
            
        # Extra manual discount in some cases
        if random.random() > 0.5:
            extra_manual_pct = random.choice([10, 15, 20])
            discount_amount = int(subtotal * (extra_manual_pct / 100.0))
            campaign_code = f"DISCOUNT_%{extra_manual_pct}"
        else:
            campaign_code = campaign["code"]
            
        taxable_amount = max(0, subtotal - discount_amount)
        vat_amount = int(taxable_amount * 0.20)  # %20 KDV
        total_amount = taxable_amount + vat_amount
        
        # Payment Status
        status_rand = random.random()
        if status_rand > 0.65:
            payment_status = "Ödendi"
            deposit_paid = total_amount
            remaining_balance = 0
        elif status_rand > 0.15:
            payment_status = "Kapora Alındı"
            deposit_paid = int(total_amount * random.choice([0.25, 0.30, 0.40, 0.50]))
            remaining_balance = total_amount - deposit_paid
        else:
            payment_status = "Beklemede"
            deposit_paid = 0
            remaining_balance = total_amount
            
        res_obj = {
            "id": res_id,
            "mediaKey": media_key,
            "mediaRetentionDays": 30,
            "mediaFiles": [],
            "venueId": venue["id"],
            "venueName": venue["name"],
            "customerId": f"cust_aug_{res_counter:03d}",
            "customerName": customer_name,
            "customerEmail": f"{groom.lower()}.{surname.lower()}@example.com",
            "customerPhone": f"+90 53{random.randint(1,9)} {random.randint(100,999)} {random.randint(1000,9999)}",
            "secondaryPhone": f"+90 54{random.randint(1,9)} {random.randint(100,999)} {random.randint(1000,9999)}",
            "date": date_str,
            "timeSlot": time_slot,
            "guestCount": guest_count,
            "selectedServices": selected_services,
            "venuePrice": base_venue_price,
            "subtotal": subtotal,
            "campaignCode": campaign_code,
            "discountAmount": discount_amount,
            "vatAmount": vat_amount,
            "totalAmount": total_amount,
            "depositPaid": deposit_paid,
            "remainingBalance": remaining_balance,
            "paymentStatus": payment_status,
            "isInvoiced": payment_status in ["Ödendi", "Kapora Alındı"],
            "invoiceType": "individual" if random.random() > 0.2 else "corporate",
            "taxOffice": "Sapanca VD",
            "tcNo": str(random.randint(10000000000, 99999999999)),
            "invoiceAddress": f"Atatürk Mah. No:{random.randint(1,100)} Sapanca / Sakarya",
            "notes": f"Özel Talep: {campaign_code} uygulandı. Salon süslemesi ve ikramlar planlandı.",
            "flowPlan": [
                {"time": time_slot.split("-")[0], "title": "Misafir Karşılama & Karşılama İkramı"},
                {"time": "19:45" if "19:00" in time_slot else "13:45", "title": "Gelin Damat Görkemli Giriş & İlk Dans"},
                {"time": "20:30" if "19:00" in time_slot else "14:30", "title": "Sıcak Yemek Servisi"},
                {"time": "21:30" if "19:00" in time_slot else "15:15", "title": "Düğün Pastası Kesimi & Şov"},
                {"time": "22:00" if "19:00" in time_slot else "15:45", "title": "Takı Töreni & Eğlence"}
            ],
            "mediaGallery": []
        }
        
        august_reservations.append(res_obj)
        res_counter += 1

print(f"Generated {len(august_reservations)} reservations for August 2026.")

with open("scratch/august_2026_reservations.json", "w", encoding="utf-8") as f:
    json.dump(august_reservations, f, ensure_ascii=False, indent=2)

print("Saved scratch/august_2026_reservations.json successfully.")
