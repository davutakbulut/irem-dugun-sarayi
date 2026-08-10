import os
import json

print("1. Cleaning leaked draft records from db_reservations.json and db_system_settings.json ...")

with open('scratch/db_reservations.json', 'r', encoding='utf-8') as f:
    reservations = json.load(f)

# Keep only confirmed reservations (filter out RES-DRAFT-...)
cleaned_reservations = [
    r for r in reservations
    if not (
        (r.get('id') and r.get('id').startswith('RES-DRAFT-')) or
        r.get('status') == 'DRAFT' or
        r.get('isDraft') is True or
        r.get('customerName') == 'İsimsiz Müşteri'
    )
]

print(f"   Original count in db_reservations.json: {len(reservations)}")
print(f"   Cleaned count in db_reservations.json: {len(cleaned_reservations)}")

with open('scratch/db_reservations.json', 'w', encoding='utf-8') as f:
    json.dump(cleaned_reservations, f, indent=2, ensure_ascii=False)

if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['reservations'] = cleaned_reservations
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)
    print("   Updated scratch/db_system_settings.json with cleaned reservations list!")

print("\n2. Fixing CreateReservationPage autoSave logic in index.html ...")

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Target the autoSave snippet that incorrectly pushed drafts into setReservations
old_auto_save_leak = """          if (!isEditMode && setDraftReservations) {
            setDraftReservations(prev => {
              const existingIdx = (prev || []).findIndex(d => d.refKey === activeRefKey);
              if (existingIdx >= 0) {
                const copy = [...prev];
                const existing = copy[existingIdx];
                const combinedLogs = [
                  ...(existing.accessLogs || []),
                  {
                    userId: currentUser?.id || 'u-admin',
                    userName: currentUser?.name || 'Davut Akbulut',
                    action: 'AUTO_SAVE',
                    timestamp: new Date().toISOString()
                  }
                ].slice(-25);

                copy[existingIdx] = {
                  ...draftResRecord,
                  createdAt: existing.createdAt || draftResRecord.createdAt,
                  createdBy: existing.createdBy || draftResRecord.createdBy,
                  accessLogs: combinedLogs
                };
                return copy;
              }
              return [draftResRecord, ...(prev || [])];
            });
          }

          if (setReservations) {
            setReservations(prev => {
              const copy = [...(prev || [])];
              const targetId = editingResFromUrl ? editingResFromUrl.id : (draftResRecord.id || activeRefKey);
              const idx = copy.findIndex(r => r.id === targetId || (activeRefKey && r.refKey === activeRefKey));
              if (idx >= 0) {
                copy[idx] = { ...copy[idx], ...draftResRecord, id: copy[idx].id || targetId };
              } else if (!isEditMode) {
                copy.unshift(draftResRecord);
              }
              return copy;
            });
          }"""

new_auto_save_fixed = """          if (isEditMode && setReservations && editingResFromUrl) {
            // In edit mode of an existing confirmed reservation, update it directly
            setReservations(prev => {
              const copy = [...(prev || [])];
              const idx = copy.findIndex(r => r.id === editingResFromUrl.id);
              if (idx >= 0) {
                copy[idx] = { ...copy[idx], ...draftResRecord, id: editingResFromUrl.id };
              }
              return copy;
            });
          } else if (!isEditMode && setDraftReservations) {
            // In new form creation mode, AUTO_SAVE strictly writes ONLY to draftReservations
            setDraftReservations(prev => {
              const existingIdx = (prev || []).findIndex(d => d.refKey === activeRefKey);
              if (existingIdx >= 0) {
                const copy = [...prev];
                const existing = copy[existingIdx];
                const combinedLogs = [
                  ...(existing.accessLogs || []),
                  {
                    userId: currentUser?.id || 'u-admin',
                    userName: currentUser?.name || 'Davut Akbulut',
                    action: 'AUTO_SAVE',
                    timestamp: new Date().toISOString()
                  }
                ].slice(-25);

                copy[existingIdx] = {
                  ...draftResRecord,
                  createdAt: existing.createdAt || draftResRecord.createdAt,
                  createdBy: existing.createdBy || draftResRecord.createdBy,
                  accessLogs: combinedLogs
                };
                return copy;
              }
              return [draftResRecord, ...(prev || [])];
            });
          }"""

if old_auto_save_leak in content:
    content = content.replace(old_auto_save_leak, new_auto_save_fixed)
    print("   Successfully replaced autoSave logic in index.html!")
else:
    print("   WARNING: Could not find exact old_auto_save_leak snippet in index.html!")

# Save index.html
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Sync to yonetim.html and dist/index.html
with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
