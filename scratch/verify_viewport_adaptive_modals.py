with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: InAppAlertModal uses screen-state adaptive classes
has_adaptive_inapp = 'w-screen h-screen z-[99999] bg-slate-950/80 backdrop-blur-md flex items-end sm:items-center' in content
print(f"[CHECK 1] InAppAlertModal viewport adaptive positioning: {has_adaptive_inapp}")

# Check 2: RedAlertConfirmModal uses viewport screen-state classes
has_adaptive_confirm = 'items-end sm:items-center justify-center' in content
print(f"[CHECK 2] RedAlertConfirmModal viewport adaptive positioning: {has_adaptive_confirm}")

# Check 3: Toast notification responsive position (top-4 left-4 right-4 sm:top-20 sm:right-6)
has_adaptive_toast = 'top-4 left-4 right-4 sm:top-20 sm:left-auto sm:right-6' in content
print(f"[CHECK 3] Toast notification responsive positioning: {has_adaptive_toast}")

if has_adaptive_inapp and has_adaptive_confirm and has_adaptive_toast:
    print("\n✅ ALL VIEWPORT ADAPTIVE MODAL CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
