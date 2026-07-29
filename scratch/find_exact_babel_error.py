import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

scripts = re.findall(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
js_code = scripts[0]
lines = js_code.split('\n')

# Let's inspect line 6080 to line 6120 of index.html
print("Lines 6080 to 6115 in index.html:")
for idx in range(6080, min(6120, len(lines))):
    print(f"{idx}: {lines[idx-1]}")
