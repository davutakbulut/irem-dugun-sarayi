with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Label changed to "Kalan Toplam:"
has_kalan_toplam = 'Kalan Toplam:' in content
print(f"[CHECK 1] Label 'Kalan Toplam:' present: {has_kalan_toplam}")

# Check 2: Enlarged price typography (text-sm sm:text-base font-black font-mono tracking-tight)
has_enlarged_price = 'text-sm sm:text-base font-black font-mono tracking-tight' in content
print(f"[CHECK 2] Enlarged price font present: {has_enlarged_price}")

# Check 3: Compact button with icon on left (px-3 py-2.5 rounded-xl text-xs)
has_compact_button = 'px-3 py-2.5 rounded-xl text-xs shadow-md' in content
print(f"[CHECK 3] Compact button with icon present: {has_compact_button}")

if has_kalan_toplam and has_enlarged_price and has_compact_button:
    print("\n✅ ALL MOBILE BAR DESIGN CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
