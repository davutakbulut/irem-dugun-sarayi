import datetime

md_path = "scratch/GITHUB_PROJECTS_BOARD.md"
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

test_notice = f"\n\n<!-- 📲 LIVE GITHUB MOBILE NOTIFICATION TEST COMMIT: {now_str} -->\n"
if "LIVE GITHUB MOBILE NOTIFICATION TEST" not in content:
    content += test_notice
else:
    # Update timestamp
    import re
    content = re.sub(r'<!-- 📲 LIVE GITHUB MOBILE NOTIFICATION TEST COMMIT: .*? -->', f'<!-- 📲 LIVE GITHUB MOBILE NOTIFICATION TEST COMMIT: {now_str} -->', content)

with open(md_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated test notification timestamp: {now_str}")
