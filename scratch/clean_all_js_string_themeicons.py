import re
import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Strip <ThemeIcon ... /> from inside quotes (e.g. showToast("...", showToast('...'), placeholder="...", title="...", emoji: '...', etc.)
# Match <ThemeIcon ... /> inside quotes
pattern = r'<\s*ThemeIcon[^>]*/>\s*'

lines = content.split('\n')
new_lines = []

for line in lines:
    # If the line contains a string literal with <ThemeIcon
    if '<ThemeIcon' in line:
        # Check if <ThemeIcon is inside quotes (double quotes, single quotes, or backticks)
        # 1. showToast or alert or confirm or title="..." or placeholder="..." or emoji: '...'
        if ('showToast(' in line or 'alert(' in line or 'confirm(' in line or 
            'placeholder="' in line or "placeholder='" in line or
            'title="' in line or "title='" in line or
            'placeholderIcon="' in line or "placeholderIcon='" in line or
            'emoji:' in line or 'desc:' in line or 'label:' in line or
            'const breadcrumbIcons =' in line or 'const activeTabIconMap =' in line):
            
            # Remove <ThemeIcon ... /> tags from inside this line if it's a string argument
            cleaned_line = re.sub(r'<\s*ThemeIcon[^>]*/>\s*', '', line)
            new_lines.append(cleaned_line)
            continue

    new_lines.append(line)

new_content = '\n'.join(new_lines)

# Additional cleanup for any remaining <ThemeIcon> inside double or single quotes
def remove_themeicon_in_quotes(text):
    # Match double quoted string containing <ThemeIcon
    def replace_dq(match):
        val = match.group(1)
        val_clean = re.sub(r'<\s*ThemeIcon[^>]*/>\s*', '', val)
        return f'"{val_clean}"'

    # Match single quoted string containing <ThemeIcon
    def replace_sq(match):
        val = match.group(1)
        val_clean = re.sub(r'<\s*ThemeIcon[^>]*/>\s*', '', val)
        return f"'{val_clean}'"

    text = re.sub(r'"([^"\n]*<\s*ThemeIcon[^"\n]*/>[^"\n]*)"', replace_dq, text)
    text = re.sub(r"'([^'\n]*<\s*ThemeIcon[^'\n]*/>[^'\n]*)'", replace_sq, text)
    return text

final_content = remove_themeicon_in_quotes(new_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(final_content)

print("Successfully cleaned up all ThemeIcon tags inside JS string literals across index.html!")
