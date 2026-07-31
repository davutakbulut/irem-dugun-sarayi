import sys

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '← Rezervasyon Listesine Dön' in line and i + 4 < len(lines):
        if lines[i+3].strip() == '</div>' and lines[i+4].strip() == '</div>':
            print(f"Removing duplicate closing div at line {i+4+1}")
            del lines[i+4]
            break

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Cleaned extra closing div in index.html successfully!")
