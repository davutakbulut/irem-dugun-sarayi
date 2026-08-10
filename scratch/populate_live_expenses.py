import json

expenses = [
  {
    "id": "exp-101",
    "resId": "RES-2026-3791",
    "resTitle": "Selin & Emre Çifti Düğün Organizasyonu",
    "title": "Garson & Komi Yevmiye Ödemesi (6 Personel)",
    "category": "Yevmiye & Personel",
    "amount": 7500,
    "date": "2026-08-08",
    "notes": "Etkinlik sonrası nakit elden ödendi",
    "createdAt": "2026-08-08T18:00:00.000Z"
  },
  {
    "id": "exp-102",
    "resId": "RES-2026-3791",
    "resTitle": "Selin & Emre Çifti Düğün Organizasyonu",
    "title": "Sahne Işık Sistemleri & Ekipman Kiralama Bedeli",
    "category": "Teknik & Ekipman",
    "amount": 12000,
    "date": "2026-08-08",
    "notes": "Fatura kesildi - Banka Havalesi",
    "createdAt": "2026-08-08T18:30:00.000Z"
  }
]

with open("scratch/db_expenses.json", "w", encoding="utf-8") as f:
    json.dump(expenses, f, ensure_ascii=False, indent=2)

print("Populated scratch/db_expenses.json with 2 live operational expense records!")
