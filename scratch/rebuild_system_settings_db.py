import os
import json

db_dir = 'scratch'

entity_files = {
    'campaigns': 'db_campaigns.json',
    'users': 'db_users.json',
    'roles': 'db_roles.json',
    'customers': 'db_customers.json',
    'reservations': 'db_reservations.json',
    'venues': 'db_venues.json',
    'services': 'db_services.json',
    'draftReservations': 'db_draft_reservations.json'
}

system_settings = {
    "themeColor": "nordic-light",
    "menuLayout": "vertical",
    "systemVersion": "v1.5.31"
}

for key, filename in entity_files.items():
    filepath = os.path.join(db_dir, filename)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                val = json.load(f)
                system_settings[key] = val
                print(f"Loaded {key} ({len(val) if isinstance(val, list) else 'object'}) from {filename}")
        except Exception as e:
            print(f"Error loading {filename}:", e)

sys_file = os.path.join(db_dir, 'db_system_settings.json')
with open(sys_file, 'w', encoding='utf-8') as f:
    json.dump(system_settings, f, indent=2, ensure_ascii=False)
    f.truncate()

print("Rebuilt scratch/db_system_settings.json cleanly!")
