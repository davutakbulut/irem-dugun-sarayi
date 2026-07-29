with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: Drawer portaled to document.body
has_drawer_portal = 'isMobileSummaryDrawerOpen && typeof ReactDOM !== \'undefined\' && ReactDOM.createPortal && ReactDOM.createPortal(' in content
print(f"[CHECK 1] Mobile Drawer portaled to document.body: {has_drawer_portal}")

# Check 2: Subtle background dimming (bg-slate-950/35 backdrop-blur-xs)
has_subtle_dim = 'bg-slate-950/35 backdrop-blur-xs' in content
print(f"[CHECK 2] Subtle background dimming (bg-slate-950/35): {has_subtle_dim}")

# Check 3: Independent z-[99999] positioning
has_high_z = 'z-[99999] bg-slate-950/35' in content
print(f"[CHECK 3] Independent z-[99999] positioning: {has_high_z}")

if has_drawer_portal and has_subtle_dim and has_high_z:
    print("\n✅ ALL SUBTLE PORTALED MOBILE DRAWER CHECKS PASSED 100%!")
else:
    print("\n❌ SOME CHECKS FAILED!")
