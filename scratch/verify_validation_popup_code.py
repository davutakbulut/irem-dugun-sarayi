with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: 3-second floating popup markup exists
popup_str = '⚠️ LÜTFEN ZORUNLU ALANLARI DOLDURUNUZ'
has_popup_markup = popup_str in content
print(f"[CHECK 1] Popup markup string present: {has_popup_markup}")

# Check 2: triggerValidationPopup auto-dismiss timer exists
has_timer = 'setTimeout' in content and 'setValidationPopup(false)' in content and '3000' in content
print(f"[CHECK 2] 3-second auto-dismiss timer logic present: {has_timer}")

# Check 3: alert(...) calls removed from customer submit validation
has_alert_in_submit = "alert('⚠️ LÜTFEN MÜŞTERİ BİLGİLERİNİ EKSİKSİZ DOLDURUNUZ" in content
print(f"[CHECK 3] Browser alert dialog removed: {not has_alert_in_submit}")

# Check 4: Inline warning text under required fields
has_inline_warning = '⚠️ Doldurulması zorunludur.' in content
print(f"[CHECK 4] Inline required field warning text present: {has_inline_warning}")

# Check 5: Red glowing ring border styling on error
has_red_glow = 'border-2 border-red-500 bg-red-500/10 ring-2 ring-red-500/30' in content
print(f"[CHECK 5] Red glowing ring border error styling present: {has_red_glow}")

if has_popup_markup and has_timer and not has_alert_in_submit and has_inline_warning and has_red_glow:
    print("\n✅ ALL 5 VALIDATION POPUP AND INLINE WARNING CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
