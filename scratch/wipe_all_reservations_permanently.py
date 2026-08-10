import json
import os

print("1. Wiping scratch/db_reservations.json to [] ...")
with open('scratch/db_reservations.json', 'w', encoding='utf-8') as f:
    json.dump([], f, indent=2)

print("2. Wiping scratch/db_draft_reservations.json to [] ...")
with open('scratch/db_draft_reservations.json', 'w', encoding='utf-8') as f:
    json.dump([], f, indent=2)

print("3. Wiping reservations & draftReservations in scratch/db_system_settings.json to [] ...")
if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['reservations'] = []
    sys_data['draftReservations'] = []
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)
        f.truncate()

print("PERMANENTLY WIPED ALL RESERVATIONS AND DRAFTS FROM DATABASE!")
