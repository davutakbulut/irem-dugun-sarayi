import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the draftReservations sync useEffect around line 8907
    draft_sync_chunk = """      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('draft_reservations', draftReservations);
        const jsonStr = JSON.stringify(draftReservations || []);
        if (jsonStr === lastSyncedDraftsRef.current) return;
        lastSyncedDraftsRef.current = jsonStr;
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(draftReservations)) {
          fetchFn('/api/draft-reservations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {});
          fetchFn('/api/public-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ draftReservations })
          }).catch(() => {});
        }
      }, [draftReservations]);"""

    if draft_sync_chunk in content:
        content = content.replace(draft_sync_chunk, "")
        print(f"Removed draft_sync_chunk from {h_file}")

    # Remove the if (setDraftReservations) block inside onSaveReservation
    save_draft_clean_start = "if (setDraftReservations) {"
    if save_draft_clean_start in content:
        s_pos = content.find(save_draft_clean_start)
        e_pos = content.find("showToast(isEdit ?", s_pos)
        if s_pos != -1 and e_pos != -1:
            content = content[:s_pos] + content[e_pos:]
            print(f"Removed save_draft_clean from {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Purged remaining draft code in {h_file}!")

print("All remaining draft code purged!")
