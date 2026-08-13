import os, re

# 1. UPDATE server.js: ADD FALLBACK HANDLER FOR /api/draft-reservations TO PREVENT ANY 404s
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

fallback_draft_handler = """// Safe fallback for any lingering draft reservation requests from cached clients
app.all(['/api/draft-reservations', '/api/draft-reservations/*', '/api/draft-reservations-delete/*'], (req, res) => {
  return res.json({ success: true, draftReservations: [] });
});
"""

if "/api/draft-reservations" not in server_code or "app.all(['/api/draft-reservations'" not in server_code:
    # Insert right before 404 catch-all
    not_found_pos = server_code.find("app.use((req, res) => {")
    if not_found_pos != -1:
        server_code = server_code[:not_found_pos] + fallback_draft_handler + "\n" + server_code[not_found_pos:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated server.js with fallback draft handler!")

# 2. UPDATE HTML FILES: CLEAN APP COMPONENT AND CreateReservationPageComponent
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # A. Fix Google Fonts link
    old_font_regex = r'<link href="https://fonts\.googleapis\.com/css2\?family=Outfit:[^"]+" rel="stylesheet">'
    new_font_tag = '<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">'
    content = re.sub(old_font_regex, new_font_tag, content)

    # B. Remove syncDrafts in App component
    sync_drafts_block = """      // Live Cross-Browser / Cross-User Draft Synchronization Effect
      useEffect(() => {
        const syncDrafts = () => {
          const fetchFn = window.fetchWithRetry || fetch;
          if (fetchFn) {
            fetchFn('/api/draft-reservations')
              .then(res => res.ok ? res.json() : null)
              .then(data => {
                if (Array.isArray(data)) {
                  setDraftReservations(data);
                }
              })
              .catch(() => {});
          }
        };

        window.addEventListener('focus', syncDrafts);
        const interval = setInterval(syncDrafts, 15000);
        return () => {
          window.removeEventListener('focus', syncDrafts);
          clearInterval(interval);
        };
      }, []);"""

    if sync_drafts_block in content:
        content = content.replace(sync_drafts_block, "")
        print(f"Removed syncDrafts from {h_file}")

    # Remove fetchFn('/api/draft-reservations') in fetchSystemSettings
    draft_fetch_pattern = """            // Fetch Draft Reservations from Database
            fetchFn('/api/draft-reservations')
              .then(res => res.json())
              .then(data => {
                if (Array.isArray(data)) {
                  setDraftReservations(data);
                }
              })
              .catch(() => {});"""
    if draft_fetch_pattern in content:
        content = content.replace(draft_fetch_pattern, "")
        print(f"Removed fetchFn draft in fetchSystemSettings from {h_file}")

    # Remove draftReservations sync useEffect in App
    draft_sync_effect = """      // Live Draft Reservations Sync with MySQL Backend & LocalStorage
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        const fetchFn = window.fetchWithRetry || fetch;
        CacheService.set('draft_reservations', draftReservations);
        const jsonStr = JSON.stringify(draftReservations || []);
        if (lastSyncedDraftsRef.current === jsonStr) return;
        lastSyncedDraftsRef.current = jsonStr;

        if (fetchFn && Array.isArray(draftReservations)) {
          fetchFn('/api/draft-reservations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {
            fetchFn('/api/public-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ draftReservations })
            }).catch(() => {});
          });
        }
      }, [draftReservations]);"""

    if draft_sync_effect in content:
        content = content.replace(draft_sync_effect, "")
        print(f"Removed draft_sync_effect from {h_file}")

    # C. In CreateReservationPageComponent, remove URL sync effect with ?ref=
    url_sync_effect = """      // Synchronize activeRefKey with URL hash and preserve existing draft refKeys & editId
      useEffect(() => {
        const syncRef = () => {
          const hashData = parseHashRoute();
          const searchParams = new URLSearchParams(window.location.search);
          const currentEditId = hashData.editId || searchParams.get('editId') || searchParams.get('edit');
          if (hashData.tab !== 'create-reservation') return;
          if (hashData.refKey && hashData.refKey !== activeRefKey) {
            setActiveRefKey(hashData.refKey);
          } else if (!hashData.refKey && activeRefKey && !currentEditId) {
            const cleanPath = window.location.pathname.endsWith('/yeni-rezervasyon') ? window.location.pathname : '/yonetim/yeni-rezervasyon';
            const newUrl = `${cleanPath}?ref=${activeRefKey}`;
            window.history.replaceState({ tab: 'create-reservation', refKey: activeRefKey }, '', newUrl);
          }
        };

        syncRef();
        window.addEventListener('hashchange', syncRef);
        window.addEventListener('popstate', syncRef);
        return () => {
          window.removeEventListener('hashchange', syncRef);
          window.removeEventListener('popstate', syncRef);
        };
      }, [activeRefKey]);"""

    if url_sync_effect in content:
        content = content.replace(url_sync_effect, "")
        print(f"Removed url_sync_effect from {h_file}")

    # Remove DRAFT AUTOMATION & AUTO-SAVE block in CreateReservationPageComponent
    old_draft_state_block = """      // DRAFT AUTOMATION & AUTO-SAVE (650ms DEBOUNCE, 12-CHAR REFKEY, USER AUDIT LOGS, CONFLICT MODAL)
      const initialRefKey = useMemo(() => {
        const hashData = parseHashRoute();
        return hashData.refKey || generateDraftRefKey();
      }, []);

      const [activeRefKey, setActiveRefKey] = useState(initialRefKey);
      const [lastSavedTime, setLastSavedTime] = useState(null);
      const [conflictModal, setConflictModal] = useState({ isOpen: false, draft: null });
      const autoSaveTimerRef = useRef(null);
      const isInitialMountRef = useRef(true);
      const hasLoadedDraftRef = useRef(null);"""

    new_draft_state_block = """      // STANDARD RESERVATION CREATION WORKSPACE
      const [activeRefKey, setActiveRefKey] = useState(null);"""

    if old_draft_state_block in content:
        content = content.replace(old_draft_state_block, new_draft_state_block)
        print(f"Replaced old_draft_state_block in {h_file}")

    # Remove the 650ms autoSave useEffect
    auto_save_use_effect_start = "      // REAL-TIME AUTO-SAVE DEBOUNCED ENGINE"
    if auto_save_use_effect_start in content:
        s_pos = content.find(auto_save_use_effect_start)
        e_pos = content.find("      // CUSTOMER DRAFT CONFLICT POPUP DETECTOR", s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            print(f"Removed autoSave useEffect from {h_file}")

    # Remove CUSTOMER DRAFT CONFLICT POPUP DETECTOR
    conflict_detector_start = "      // CUSTOMER DRAFT CONFLICT POPUP DETECTOR"
    if conflict_detector_start in content:
        s_pos = content.find(conflict_detector_start)
        e_pos = content.find("      const selectedVenue = venues.find", s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            print(f"Removed conflict detector from {h_file}")

    # Remove Load existing draft if present for activeRefKey
    load_draft_start = "      // Load existing draft if present for activeRefKey"
    if load_draft_start in content:
        s_pos = content.find(load_draft_start)
        e_pos = content.find("      // Load existing reservation for EDIT MODE", s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            print(f"Removed load existing draft from {h_file}")

    # Remove conflict modal JSX in CreateReservationPageComponent
    conflict_modal_jsx_start = "{/* CUSTOMER DRAFT CONFLICT POPUP WARNING MODAL */}"
    if conflict_modal_jsx_start in content:
        s_pos = content.find(conflict_modal_jsx_start)
        e_pos = content.find("{/* STANDALONE FLOATING TOP-RIGHT NOTIFICATION POPUP */}", s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            print(f"Removed conflict modal JSX from {h_file}")

    # Replace the Ref / Taslak Kaydedildi badges in CreateReservationPageComponent header
    old_badges_block = """                {/* DRAFT REF KEY BADGE WITH CLICK TO COPY */}
                <button
                  type="button"
                  onClick={() => {
                    if (activeRefKey && navigator.clipboard) {
                      navigator.clipboard.writeText(activeRefKey);
                      if (showToast) showToast('Sözleşme referans kodu kopyalandı! ', 'success');
                    }
                  }}
                  className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-mono font-bold inline-flex items-center space-x-1 shrink-0 cursor-pointer transition whitespace-nowrap snap-start"
                  title="Referans kodunu kopyalamak için tıklayın"
                >
                  <span><ThemeIcon icon="key" className="w-4 h-4 inline-block shrink-0" /> Ref:</span>
                  <span className="tracking-wider">{activeRefKey}</span>
                  <span className="text-[10px] text-amber-500"><ThemeIcon icon="document" className="w-4 h-4 inline-block shrink-0" /></span>
                </button>

                {lastSavedTime ? (
                  <span className="px-2.5 py-1 rounded-lg bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">
                    <span><ThemeIcon icon="check" className="w-4 h-4 inline-block shrink-0" /> Taslak Kaydedildi</span>
                    <span className="text-[10px] font-mono">({lastSavedTime})</span>
                  </span>
                ) : (
                  <span className="px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-brand-dark text-slate-500 text-xs font-semibold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">
                    <span><ThemeIcon icon="clock" className="w-4 h-4 inline-block shrink-0" /> Canlı Otomatik Kayıt</span>
                  </span>
                )}"""

    new_badges_block = """                <span className="px-2.5 py-1 rounded-lg bg-amber-500/10 text-amber-700 dark:text-gold-400 border border-amber-500/30 text-xs font-bold inline-flex items-center space-x-1 shrink-0 whitespace-nowrap snap-start">
                  <ThemeIcon icon="sparkles" className="w-3.5 h-3.5 inline-block shrink-0 text-amber-600 dark:text-gold-400" />
                  <span>{isEditMode ? `Düzenleme Modu (${editingResFromUrl?.id || ''})` : 'Standart Rezervasyon Kaydı'}</span>
                </span>"""

    if old_badges_block in content:
        content = content.replace(old_badges_block, new_badges_block)
        print(f"Replaced old_badges_block in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All draft cleanup operations completed successfully!")
