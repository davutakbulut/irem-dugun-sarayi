import re

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

emoji_pattern = re.compile(r'[\U0001F000-\U0001FFFF\U00002600-\U000027BF\U00002300-\U000023FF]')

emoji_counts = {}
found_lines = []

for line_no, line in enumerate(lines, 1):
    matches = emoji_pattern.findall(line)
    if matches:
        for m in matches:
            emoji_counts[m] = emoji_counts.get(m, 0) + 1
        found_lines.append((line_no, line.strip()))

print(f"Total lines with emojis: {len(found_lines)}")
print("Emoji Frequency Map:")
for emoji, count in sorted(emoji_counts.items(), key=lambda x: x[1], reverse=False):
    print(f"  '{emoji}': {count} times")

print("\nSample lines (first 20):")
for lno, text in found_lines[:20]:
    print(f"Line {lno}: {text[:100]}")
