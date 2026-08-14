import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

fin_match = re.search(r'function FinanceComponent[\s\S]*?^    }', content, re.MULTILINE)
if fin_match:
    fin_code = fin_match.group(0)
    # Find non-ascii characters or emoji-like patterns
    emojis = set(re.findall(r'[\U00010000-\U0010ffff]|[\u2600-\u27ff]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u200d\ufe0f]', fin_code))
    print("Found emojis:", emojis)
    
    # Print lines containing emojis
    for idx, line in enumerate(fin_code.split('\n'), 1):
        for em in emojis:
            if em in line:
                print(f"Line {idx}: {line}")
                break
