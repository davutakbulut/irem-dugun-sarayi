import os

with open('scratch/serve_fast_3g.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace time.strftime with datetime.datetime.now().strftime
content = content.replace('time.strftime("%Y-%m-%d %H:%M:%S")', 'datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")')

# Ensure datetime is imported
if 'import datetime' not in content:
    content = 'import datetime\n' + content

with open('scratch/serve_fast_3g.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("1. Replaced time.strftime with datetime.datetime.now().strftime in serve_fast_3g.py!")
