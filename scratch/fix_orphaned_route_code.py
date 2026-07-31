with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_snippet = """      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return !!guestMediaKeyMatch || hash.includes('mode=guest');
      }, [activeTab, guestMediaKeyMatch]);
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return hash.includes('key=') || hash.includes('mode=guest');
      }, [activeTab]);"""

good_snippet = """      const isPublicGuestRoute = useMemo(() => {
        if (typeof window === 'undefined') return false;
        const hash = window.location.hash || '';
        return !!guestMediaKeyMatch || hash.includes('mode=guest') || hash.includes('key=');
      }, [activeTab, guestMediaKeyMatch]);"""

if bad_snippet in html:
    html = html.replace(bad_snippet, good_snippet)
    print("Cleaned up orphaned route code snippet successfully!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
