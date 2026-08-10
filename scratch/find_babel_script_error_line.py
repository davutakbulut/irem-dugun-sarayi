with open("index.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

script_start_line = 0
for i, line in enumerate(lines):
    if '<script type="text/babel">' in line or '<script type="text/babel" id="app-script">' in line:
        script_start_line = i + 1
        print(f"Babel script tag starts at line {script_start_line}")
        break

target_idx = 6767 + script_start_line - 1
print(f"Target line in file: {target_idx}")

for lno in range(max(1, target_idx - 10), min(len(lines), target_idx + 10)):
    print(f"{lno}: {lines[lno-1]}", end="")
