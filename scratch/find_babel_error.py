import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if not script_match:
    print("No babel script found")
    exit(1)

script_text = script_match.group(1)
lines = script_text.split('\n')
print(f"Total lines in babel script: {len(lines)}")

for idx, line in enumerate(lines[3555:3575], 3556):
    print(f"{idx}: {repr(line)}")
