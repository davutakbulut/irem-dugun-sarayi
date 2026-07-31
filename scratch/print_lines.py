import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
code = script_match.group(1)
lines = code.split('\n')

for i in range(2730, 2830):
    if i < len(lines):
        print(f"{i}: {lines[i]}")
