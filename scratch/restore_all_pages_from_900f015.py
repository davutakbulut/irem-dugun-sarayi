import subprocess
import re

html_900f015 = subprocess.check_output(['git', 'show', '900f015:index.html']).decode('utf-8')
lines = html_900f015.split('\n')

print(f"Total lines in 900f015:index.html: {len(lines)}")

# Find function positions
fn_pattern = re.compile(r'^\s*function\s+([A-Za-z0-9_]+)\s*\(')

func_positions = []
for idx, line in enumerate(lines):
    m = fn_pattern.match(line)
    if m:
        func_positions.append((m.group(1), idx + 1))

for idx, (name, start_line) in enumerate(func_positions):
    next_start = func_positions[idx + 1][1] if idx + 1 < len(func_positions) else len(lines)
    print(f"Function {name:30s}: lines {start_line:4d} to {next_start - 1:4d} (total {next_start - start_line:4d} lines)")
