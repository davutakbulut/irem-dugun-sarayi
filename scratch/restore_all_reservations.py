import json
import os

reservations_6 = [
    {
        "id": "RES-2026-AUG-06",
        "mediaKey": "MEDIA-AUG26-06",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v4",
        "venueName": "Yakut Panorama Salon",
        "customerId": "cust_aug_008",
        "customerName": "Mert & Ece Yılmaz",
        "customerEmail": "mert.yılmaz@example.com",
        "customerPhone": "+90 537 893 8619",
        "secondaryPhone": "+90 541 478 5197",
        "date": "2026-08-06",
        "timeSlot": "19:00-23:00",
        "guestCount": 700,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Özel Menü İkramı",
                "quantity": 700,
                "unitPrice": 360
            },
            {
                "serviceId": "s2",
                "serviceName": "Canlı Orkestra & DJ Performatör",
                "quantity": 1,
                "unitPrice": 22000
            },
            {
                "serviceId": "s3",
                "serviceName": "4K Drone & Jimmy Jib Video Çekimi",
                "quantity": 1,
                "unitPrice": 16000
            },
            {
                "serviceId": "s4",
                "serviceName": "Kristal Şamdan & Konsept Masa Tasarımı",
                "quantity": 1,
                "unitPrice": 14000
            },
            {
                "serviceId": "s5",
                "serviceName": "Soğuk Volkan & Konfeti Şovu",
                "quantity": 1,
                "unitPrice": 8500
            },
            {
                "serviceId": "s6",
                "serviceName": "Karşılama Kokteyli & İkram Barı",
                "quantity": 700,
                "unitPrice": 88
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 41600,
        "venuePrice": 65000,
        "totalAmount": 374400,
        "depositPaid": 150000,
        "paymentStatus": "Kapora Alındı",
        "notes": "Erken rezervasyon %10 indirim uygulandı.",
        "createdAt": "2026-08-01T12:00:00.000Z"
    },
    {
        "id": "RES-2026-AUG-05",
        "mediaKey": "MEDIA-AUG26-05",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v4",
        "venueName": "Yakut Panorama Salon",
        "customerId": "cust_aug_007",
        "customerName": "Mehmet & Derya Kaya",
        "customerEmail": "mehmet.kaya@example.com",
        "customerPhone": "+90 536 782 7508",
        "secondaryPhone": "+90 540 367 4086",
        "date": "2026-08-05",
        "timeSlot": "19:00-23:00",
        "guestCount": 650,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Özel Menü İkramı",
                "quantity": 650,
                "unitPrice": 350
            },
            {
                "serviceId": "s2",
                "serviceName": "Canlı Orkestra & DJ Performatör",
                "quantity": 1,
                "unitPrice": 20000
            },
            {
                "serviceId": "s3",
                "serviceName": "4K Drone & Jimmy Jib Video Çekimi",
                "quantity": 1,
                "unitPrice": 15000
            },
            {
                "serviceId": "s4",
                "serviceName": "Kristal Şamdan & Konsept Masa Tasarımı",
                "quantity": 1,
                "unitPrice": 13000
            },
            {
                "serviceId": "s5",
                "serviceName": "Soğuk Volkan & Konfeti Şovu",
                "quantity": 1,
                "unitPrice": 8000
            },
            {
                "serviceId": "s6",
                "serviceName": "Karşılama Kokteyli & İkram Barı",
                "quantity": 650,
                "unitPrice": 80
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 35580,
        "venuePrice": 65000,
        "totalAmount": 320220,
        "depositPaid": 120000,
        "paymentStatus": "Kapora Alındı",
        "notes": "Erken rezervasyon %10 indirim uygulandı.",
        "createdAt": "2026-08-01T11:00:00.000Z"
    },
    {
        "id": "RES-2026-AUG-07A",
        "mediaKey": "MEDIA-AUG26-07A",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v2",
        "venueName": "VIP Kır Bahçesi & Park",
        "customerId": "cust_aug_009",
        "customerName": "Sinan & Fatma Bulut",
        "customerEmail": "sinan.bulut@example.com",
        "customerPhone": "+90 538 904 9720",
        "secondaryPhone": "+90 542 589 6208",
        "date": "2026-08-07",
        "timeSlot": "19:00-23:00",
        "guestCount": 850,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Özel Menü İkramı",
                "quantity": 850,
                "unitPrice": 380
            },
            {
                "serviceId": "s2",
                "serviceName": "Canlı Orkestra & DJ Performatör",
                "quantity": 1,
                "unitPrice": 25000
            },
            {
                "serviceId": "s3",
                "serviceName": "4K Drone & Jimmy Jib Video Çekimi",
                "quantity": 1,
                "unitPrice": 18000
            },
            {
                "serviceId": "s4",
                "serviceName": "Kristal Şamdan & Konsept Masa Tasarımı",
                "quantity": 1,
                "unitPrice": 15000
            },
            {
                "serviceId": "s5",
                "serviceName": "Soğuk Volkan & Konfeti Şovu",
                "quantity": 1,
                "unitPrice": 9000
            },
            {
                "serviceId": "s6",
                "serviceName": "Karşılama Kokteyli & İkram Barı",
                "quantity": 850,
                "unitPrice": 95
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 54618,
        "venuePrice": 85000,
        "totalAmount": 491568,
        "depositPaid": 200000,
        "paymentStatus": "Kapora Alındı",
        "notes": "Kır bahçesi özel gala konsepti.",
        "createdAt": "2026-08-01T13:00:00.000Z"
    },
    {
        "id": "RES-2026-AUG-07B",
        "mediaKey": "MEDIA-AUG26-07B",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v3",
        "venueName": "Teras Salon Silver Rose",
        "customerId": "cust_aug_010",
        "customerName": "Mert & Yasemin Arslan",
        "customerEmail": "mert.arslan@example.com",
        "customerPhone": "+90 539 015 0831",
        "secondaryPhone": "+90 543 690 7319",
        "date": "2026-08-07",
        "timeSlot": "19:00-23:00",
        "guestCount": 800,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Özel Menü İkramı",
                "quantity": 800,
                "unitPrice": 370
            },
            {
                "serviceId": "s2",
                "serviceName": "Canlı Orkestra & DJ Performatör",
                "quantity": 1,
                "unitPrice": 24000
            },
            {
                "serviceId": "s3",
                "serviceName": "4K Drone & Jimmy Jib Video Çekimi",
                "quantity": 1,
                "unitPrice": 17000
            },
            {
                "serviceId": "s4",
                "serviceName": "Kristal Şamdan & Konsept Masa Tasarımı",
                "quantity": 1,
                "unitPrice": 14500
            },
            {
                "serviceId": "s5",
                "serviceName": "Soğuk Volkan & Konfeti Şovu",
                "quantity": 1,
                "unitPrice": 8800
            },
            {
                "serviceId": "s6",
                "serviceName": "Karşılama Kokteyli & İkram Barı",
                "quantity": 800,
                "unitPrice": 90
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 52080,
        "venuePrice": 75000,
        "totalAmount": 468720,
        "depositPaid": 180000,
        "paymentStatus": "Kapora Alındı",
        "notes": "Teras salon özel ışık konsepti.",
        "createdAt": "2026-08-01T14:00:00.000Z"
    },
    {
        "id": "RES-2026-AUG-04",
        "mediaKey": "MEDIA-AUG26-04",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v1",
        "venueName": "Bosphorus Gold Balo Salonu",
        "customerId": "cust_aug_006",
        "customerName": "Sinan & Yasemin Kurt",
        "customerEmail": "sinan.kurt@example.com",
        "customerPhone": "+90 535 671 6497",
        "secondaryPhone": "+90 539 256 3975",
        "date": "2026-08-04",
        "timeSlot": "19:00-23:00",
        "guestCount": 600,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Özel Menü İkramı",
                "quantity": 600,
                "unitPrice": 400
            },
            {
                "serviceId": "s2",
                "serviceName": "Canlı Orkestra & DJ Performatör",
                "quantity": 1,
                "unitPrice": 25000
            },
            {
                "serviceId": "s3",
                "serviceName": "4K Drone & Jimmy Jib Video Çekimi",
                "quantity": 1,
                "unitPrice": 18000
            },
            {
                "serviceId": "s4",
                "serviceName": "Kristal Şamdan & Konsept Masa Tasarımı",
                "quantity": 1,
                "unitPrice": 15000
            },
            {
                "serviceId": "s5",
                "serviceName": "Soğuk Volkan & Konfeti Şovu",
                "quantity": 1,
                "unitPrice": 9000
            },
            {
                "serviceId": "s6",
                "serviceName": "Karşılama Kokteyli & İkram Barı",
                "quantity": 600,
                "unitPrice": 100
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 44176,
        "venuePrice": 75000,
        "totalAmount": 397584,
        "depositPaid": 160000,
        "paymentStatus": "Kapora Alındı",
        "notes": "VİP düğün organizasyonu.",
        "createdAt": "2026-08-01T10:00:00.000Z"
    },
    {
        "id": "RES-2026-AUG-08",
        "mediaKey": "MEDIA-AUG26-08",
        "mediaRetentionDays": 30,
        "mediaFiles": [],
        "venueId": "v1",
        "venueName": "Kraliyet Balo Salonu",
        "customerId": "cust1",
        "customerName": "Ahmet Yılmaz & Ayşe Kaya",
        "customerEmail": "ahmet.yilmaz@example.com",
        "customerPhone": "+90 532 111 2233",
        "secondaryPhone": "+90 535 999 8877",
        "date": "2026-08-08",
        "timeSlot": "19:00-23:00",
        "guestCount": 500,
        "selectedServices": [
            {
                "serviceId": "s1",
                "serviceName": "Gurme Yemek Servisi (Et Menü)",
                "quantity": 500,
                "unitPrice": 750
            },
            {
                "serviceId": "s3",
                "serviceName": "Canlı Müzik Orkestrası & DJ",
                "quantity": 1,
                "unitPrice": 25000
            }
        ],
        "appliedCampaignCode": "IREM2026",
        "appliedDiscountAmount": 50000,
        "venuePrice": 100000,
        "totalAmount": 450000,
        "depositPaid": 200000,
        "paymentStatus": "Kapora Alındı",
        "notes": "Kraliyet balo salonu organizasyonu.",
        "createdAt": "2026-08-02T10:00:00.000Z"
    }
]

print("1. Restoring 6 confirmed reservations to db_reservations.json ...")
with open('scratch/db_reservations.json', 'w', encoding='utf-8') as f:
    json.dump(reservations_6, f, indent=2, ensure_ascii=False)

print("2. Restoring 6 confirmed reservations to db_system_settings.json ...")
if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['reservations'] = reservations_6
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)

print("RESTORED 6 CONFIRMED RESERVATIONS TO DATABASE SUCCESSFULLY!")
