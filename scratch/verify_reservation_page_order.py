with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

sections = [
    "1. Düğün Salonu Seçin:",
    "2. Ek Hizmetler:",
    "3. Ödeme, Kapora & İndirim Kodu Bilgileri",
    "4. Müşteri İletişim Bilgileri:",
    "5. Fatura Bilgileri",
    "6. Organizasyon & Etkinlik Akış Planlaması",
    "7. Operasyonel Ek Notlar & Özel İstekler:"
]

indices = []
for sec in sections:
    idx = content.find(sec)
    print(f"[{sec}] -> Found at index: {idx}")
    indices.append(idx)

# Verify strictly increasing order
is_ordered = all(indices[i] < indices[i+1] for i in range(len(indices)-1)) and all(x != -1 for x in indices)
print(f"\n[ORDER VERIFICATION] Strictly increasing order (7 sections): {is_ordered}")

# Verify calendar grid is inside Section 1 (before Section 2)
sec1_idx = indices[0]
sec2_idx = indices[1]
cal_idx = content.find("🗓️ Canlı Takvim & Çakışma Önizlemesi", sec1_idx)
is_cal_in_sec1 = sec1_idx < cal_idx < sec2_idx
print(f"[CALENDAR RESTORATION] Calendar grid is inside Section 1: {is_cal_in_sec1} (index: {cal_idx})")

# Verify standardized heading classes
has_standard_h2 = content.count("font-heading font-bold text-base sm:text-lg text-slate-800 dark:text-gray-100") >= 7
print(f"[TYPOGRAPHY HIERARCHY] Standard H2 classes applied across sections: {has_standard_h2}")

if is_ordered and is_cal_in_sec1 and has_standard_h2:
    print("\n✅ ALL RESERVATION PAGE & TYPOGRAPHY CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
