with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_sidebar_cond = "{!isErrorPage && menuLayout === 'vertical' && ("
good_sidebar_cond = "{!isErrorPage && !isPublicGuestRoute && menuLayout === 'vertical' && ("

if bad_sidebar_cond in html:
    html = html.replace(bad_sidebar_cond, good_sidebar_cond)
    print("Fixed missing !isPublicGuestRoute check on sidebar line 5520!")

# Also simplify isPublicGuestRoute definition to guarantee matching any medya/ or key= URL
old_guest_route_def = """      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return !!guestMediaKeyMatch || hash.includes('mode=guest') || hash.includes('key=');
      }, [activeTab, guestMediaKeyMatch]);"""

new_guest_route_def = """      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('medya/') || hash.includes('m/') || hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

if old_guest_route_def in html:
    html = html.replace(old_guest_route_def, new_guest_route_def)
    print("Simplified isPublicGuestRoute check to match all medya/ routes!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
