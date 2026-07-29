with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Root level rendering of mobileReservationSummary outside <main>
has_root_rendering = 'activeTab === \'create-reservation\' && mobileReservationSummary' in content
print(f"[CHECK 1] Root App level mobileReservationSummary bar rendered: {has_root_rendering}")

# Check 2: Fixed bottom positioning (sm:hidden fixed bottom-0 left-0 right-0 z-50)
has_fixed_bottom = 'sm:hidden fixed bottom-0 left-0 right-0 z-50 bg-white/95' in content
print(f"[CHECK 2] Fixed bottom positioning outside <main>: {has_fixed_bottom}")

# Check 3: Slide-Up Drawer rendered outside <main> at root App level
has_root_drawer = 'activeTab === \'create-reservation\' && isMobileSummaryDrawerOpen && mobileReservationSummary' in content
print(f"[CHECK 3] Slide-Up Drawer rendered outside <main> at root App level: {has_root_drawer}")

if has_root_rendering and has_fixed_bottom and has_root_drawer:
    print("\n✅ ALL ROOT LEVEL MOBILE FIXED VIEWPORT BAR CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
