with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

sections = [
    "1. Düğün Salonu Seçin:",
    "2. Ek Hizmetler:",
    "3. Ödeme, Kapora & İndirim Kodu Bilgileri",
    "4. Müşteri İletişim Bilgileri:",
    "5. Fatura Bilgileri",
    "6. Organizasyon & Etkinlik Akış Planlaması",
    "7. Operasyonel Ek Notlar & Özel İstekler:",
    "8. Takvim Canlı Ön İzlemesi"
]

indices = []
for sec in sections:
    idx = content.find(sec)
    print(f"[{sec}] -> Found at index: {idx}")
    indices.append(idx)

# Verify strictly increasing order
is_ordered = all(indices[i] < indices[i+1] for i in range(len(indices)-1)) and all(x != -1 for x in indices)
print(f"\n[ORDER VERIFICATION] Strictly increasing order: {is_ordered}")

# Verify selectedServices default state is []
has_empty_services = "const [selectedServices, setSelectedServices] = useState([]);" in content
print(f"[SERVICES UNCHECKED VERIFICATION] selectedServices default state is []: {has_empty_services}")

if is_ordered and has_empty_services:
    print("\n✅ ALL RESERVATION PAGE ORDER CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
