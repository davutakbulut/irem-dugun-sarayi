import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

script_match = re.search(r'<script type="text/babel">(.*?)</script>', content, re.DOTALL)
if not script_match:
    print("No babel script found!")
    exit(1)

code = script_match.group(1)

# Remove single line comments and strings
def clean_code(text):
    # Remove strings
    lines = text.split('\n')
    cleaned_lines = []
    for line in lines:
        # Strip string contents roughly or parse carefully
        new_line = []
        in_s = None
        i = 0
        while i < len(line):
            ch = line[i]
            if in_s:
                if ch == in_s and (i == 0 or line[i-1] != '\\'):
                    in_s = None
                i += 1
                continue
            if ch in ('"', "'", '`'):
                in_s = ch
                i += 1
                continue
            if ch == '/' and i + 1 < len(line) and line[i+1] == '/':
                break
            new_line.append(ch)
            i += 1
        cleaned_lines.append("".join(new_line))
    return "\n".join(cleaned_lines)

cleaned = clean_code(code)

stack = []
for line_idx, line in enumerate(cleaned.split('\n'), 1):
    for col_idx, char in enumerate(line, 1):
        if char in '({[':
            stack.append((char, line_idx, col_idx))
        elif char in ')}]' :
            if not stack:
                print(f"ERROR: Extra closing '{char}' at line {line_idx}:{col_idx}")
            else:
                top_char, top_line, top_col = stack.pop()
                expected = {'(': ')', '{': '}', '[': ']'}[top_char]
                if char != expected:
                    print(f"ERROR: Mismatched '{char}' at line {line_idx}:{col_idx}, expected '{expected}' for '{top_char}' opened at line {top_line}:{top_col}")

if stack:
    print(f"ERROR: {len(stack)} unclosed tokens remaining at end of script:")
    for top_char, top_line, top_col in stack[-10:]:
        print(f"  Unclosed '{top_char}' opened at line {top_line}:{top_col}")
else:
    print("✅ ABSOLUTELY PERFECT! No unclosed braces, parens or brackets in Babel script!")
