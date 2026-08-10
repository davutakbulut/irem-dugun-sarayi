import os
import glob
import re

PHONE_FORMAT_FORMATTED = "+90 547 144 00 54"
PHONE_FORMAT_DIGITS = "905471440054"
PHONE_FORMAT_COMPACT = "+905471440054"

def replace_phone_numbers(text):
    # 1. Tel & Whatsapp Href links
    text = re.sub(r'href=["\']tel:\+?90[0-9\s\-]+["\']', f'href="tel:{PHONE_FORMAT_COMPACT}"', text)
    text = re.sub(r'href=["\']https://wa\.me/90[0-9]+["\']', f'href="https://wa.me/{PHONE_FORMAT_DIGITS}"', text)
    
    # 2. Specific phone number patterns
    patterns = [
        r'\+90\s*\(?264\)?\s*582\s*00\s*0[0-9]',
        r'\+90\s*547\s*144\s*00\s*44',
        r'\+905471440044',
        r'905471440044',
        r'\+90\s*547\s*291\s*7891',
        r'\+90\s*532\s*123\s*4567',
        r'0532\s*000\s*00\s*00',
        r'905320000000',
        r'\+90\s*\(264\)\s*582\s*00\s*00'
    ]

    for p in patterns:
        text = re.sub(p, PHONE_FORMAT_FORMATTED, text)

    return text

# Files to process
files_to_process = [
    'index.html',
    'yonetim.html',
    'dist/index.html',
    'scratch/serve_fast_3g.py'
]

# Add all db_*.json files
json_files = glob.glob('scratch/db_*.json')
files_to_process.extend(json_files)

processed_count = 0
for file_path in files_to_process:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = replace_phone_numbers(content)
        
        # Specific JSON fixes
        if file_path.endswith('.json'):
            new_content = re.sub(r'"phone":\s*"[^"]*"', f'"phone": "{PHONE_FORMAT_FORMATTED}"', new_content)
            new_content = re.sub(r'"whatsapp":\s*"[^"]*"', f'"whatsapp": "{PHONE_FORMAT_DIGITS}"', new_content)

        if content != new_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Updated phone numbers in: {file_path}")
            processed_count += 1
        else:
            print(f"ℹ️ No changes needed in: {file_path}")

print(f"\nCompleted phone number standardization across {processed_count} files!")
