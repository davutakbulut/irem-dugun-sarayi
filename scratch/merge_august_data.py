import json
import re

# 1. Load generated August reservations
with open('scratch/august_2026_reservations.json', 'r', encoding='utf-8') as f:
    august_res = json.load(f)

print(f"Loaded {len(august_res)} August 2026 reservations.")

# 2. Update scratch/db_system_settings.json
db_file = 'scratch/db_system_settings.json'
with open(db_file, 'r', encoding='utf-8') as f:
    db = json.load(f)

existing_res = db.get('reservations', [])
# Keep non-August reservations or replace August reservations
filtered_existing = [r for r in existing_res if not (isinstance(r, dict) and r.get('date', '').startswith('2026-08'))]
merged_db_res = august_res + filtered_existing

db['reservations'] = merged_db_res
with open(db_file, 'w', encoding='utf-8') as f:
    json.dump(db, f, ensure_ascii=False, indent=2)

print("Updated scratch/db_system_settings.json successfully.")

# 3. Update index.html INITIAL_RESERVATIONS
with open('index.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace INITIAL_RESERVATIONS = [ ... ];
august_json_str = json.dumps(august_res, ensure_ascii=False, indent=2)
new_initial = f"const INITIAL_RESERVATIONS = {august_json_str};"

html_content = re.sub(r'const INITIAL_RESERVATIONS = \[[\s\S]*?\n    \];', new_initial, html_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Updated index.html INITIAL_RESERVATIONS successfully.")
