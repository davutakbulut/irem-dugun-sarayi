import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
code = script_match.group(1)
lines = code.split('\n')

for i in range(1750, 1780):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
