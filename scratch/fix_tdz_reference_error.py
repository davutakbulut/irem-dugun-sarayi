import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix Temporal Dead Zone variable declaration order in MediaComponent
old_block = """  const urlKey = getUrlKey();
  
  // STRICT GUEST MODE: Active on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, [selectedResKey]);

  // Active selected reservation key (Preserved in URL Hash on click & refresh)
  const [selectedResKey, setSelectedResKey] = useState(() => {
    if (urlKey) return urlKey;
    return null;
  });"""

new_block = """  const urlKey = getUrlKey();
  
  // Active selected reservation key (Preserved in URL Hash on click & refresh)
  const [selectedResKey, setSelectedResKey] = useState(() => {
    if (urlKey) return urlKey;
    return null;
  });

  // STRICT GUEST MODE: Active on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, [selectedResKey]);"""

if old_block in html:
    html = html.replace(old_block, new_block)
    print("Fixed Temporal Dead Zone variable declaration order in MediaComponent!")
else:
    print("WARNING: Target block not matched cleanly. Checking alternative replacement.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html TDZ fix successfully!")
