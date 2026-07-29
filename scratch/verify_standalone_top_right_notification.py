with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Top-Right Floating Notification Popup positioning
has_top_right_pos = 'fixed top-5 right-4 sm:right-6 left-4 sm:left-auto z-[99999]' in content
print(f"[CHECK 1] Standalone Top-Right Notification positioning present: {has_top_right_pos}")

# Check 2: Red accent border & glassmorphism styling
has_red_accent = 'border-l-8 border-l-red-600' in content and 'border-2 border-red-500/70' in content
print(f"[CHECK 2] Crimson red accent border present: {has_red_accent}")

# Check 3: Action button and close X button present
has_buttons = 'Anladım, Düzelt ✓' in content and 'aria-label="Kapat"' in content
print(f"[CHECK 3] Action button and close X button present: {has_buttons}")

if has_top_right_pos and has_red_accent and has_buttons:
    print("\n✅ ALL STANDALONE TOP-RIGHT NOTIFICATION CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
