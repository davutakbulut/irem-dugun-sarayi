import os
import json

print("Initializing scratch/db_expenses.json ...")
with open('scratch/db_expenses.json', 'w', encoding='utf-8') as f:
    json.dump([], f, indent=2)

if os.path.exists('scratch/db_system_settings.json'):
    with open('scratch/db_system_settings.json', 'r', encoding='utf-8') as f:
        sys_data = json.load(f)
    sys_data['expenses'] = []
    with open('scratch/db_system_settings.json', 'w', encoding='utf-8') as f:
        json.dump(sys_data, f, indent=2, ensure_ascii=False)

print("INITIALIZED db_expenses.json SUCCESSFULLY!")
