import os

server_file = 'scratch/serve_fast_3g.py'

with open(server_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update GET /api/system-settings reader to auto-repair JSON error if extra data exists
old_get_reader = """                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            cfg_data = json.load(f)
                    except Exception: pass"""

new_get_reader = """                if os.path.exists(db_file):
                    try:
                        with open(db_file, 'r', encoding='utf-8') as f:
                            raw_txt = f.read().strip()
                        # Try parsing raw text, if extra data exists, take valid json portion
                        try:
                            cfg_data = json.loads(raw_txt)
                        except Exception as e_pos:
                            pos = getattr(e_pos, 'pos', None)
                            if pos and pos > 0:
                                cfg_data = json.loads(raw_txt[:pos].strip())
                    except Exception as ex:
                        print("Error reading db_system_settings.json in GET:", ex)"""

if old_get_reader in content:
    content = content.replace(old_get_reader, new_get_reader)
    print("1. Updated GET /api/system-settings reader with auto-repair truncation guard.")

# 2. Update POST /api/system-settings writer to call f.truncate() and ef.truncate()
old_post_writer = """                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2)

                # Dedicated files sync
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
                for k, filename in entity_files.items():
                    if k in data:
                        try:
                            with open(os.path.join(db_dir, filename), 'w', encoding='utf-8') as ef:
                                json.dump(data[k], ef, indent=2)
                        except Exception: pass"""

new_post_writer = """                with open(db_file, 'w', encoding='utf-8') as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
                    f.truncate()

                # Dedicated files sync
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
                for k, filename in entity_files.items():
                    if k in data:
                        try:
                            with open(os.path.join(db_dir, filename), 'w', encoding='utf-8') as ef:
                                json.dump(data[k], ef, indent=2, ensure_ascii=False)
                                ef.truncate()
                        except Exception: pass"""

if old_post_writer in content:
    content = content.replace(old_post_writer, new_post_writer)
    print("2. Added f.truncate() and ef.truncate() to POST /api/system-settings writer.")

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated scratch/serve_fast_3g.py successfully!")
