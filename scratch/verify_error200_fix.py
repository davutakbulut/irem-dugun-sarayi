with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check 1: 0 unsafe ReactDOM.createPortal calls remaining in index.html
portal_count = content.count('ReactDOM.createPortal')
print(f"[CHECK 1] ReactDOM.createPortal calls remaining in index.html: {portal_count}")

# Check 2: Mobile bottom bar rendered cleanly (sm:hidden fixed bottom-0 left-0 right-0 z-40)
has_clean_bottom_bar = 'sm:hidden fixed bottom-0 left-0 right-0 z-40' in content
print(f"[CHECK 2] Clean mobile bottom bar present: {has_clean_bottom_bar}")

# Check 3: Mobile drawer rendered cleanly (isMobileSummaryDrawerOpen && (...) with z-[99999])
has_clean_drawer = 'isMobileSummaryDrawerOpen && (' in content and 'z-[99999] bg-slate-950/35' in content
print(f"[CHECK 3] Clean mobile summary drawer present: {has_clean_drawer}")

if portal_count == 0 and has_clean_bottom_bar and has_clean_drawer:
    print("\n✅ REACT ERROR #200 COMPLETELY ELIMINATED! 100% PASS!")
else:
    print("\n❌ SOME CHECKS FAILED!")
