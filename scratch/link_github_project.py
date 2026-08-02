import json

json_path = "scratch/system_roadmap_100_items.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

data["github_project_url"] = "https://github.com/users/davutakbulut/projects/1/views/1"
data["github_project_number"] = 1

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# Update GITHUB_PROJECTS_BOARD.md
md_path = "scratch/GITHUB_PROJECTS_BOARD.md"
with open(md_path, "r", encoding="utf-8") as f:
    content = f.read()

header_update = """# 📊 İrem Düğün Sarayı — Resmi GitHub Projects Live Kanban Board

🔗 **Resmi GitHub Proje Panosu:** [https://github.com/users/davutakbulut/projects/1/views/1](https://github.com/users/davutakbulut/projects/1/views/1)

Bu döküman ve canlı pano, otonom yapay zeka geliştirme hattı (`task-2254`) tarafından anlık olarak senkronize edilir.

---
"""

# Replace header
lines = content.splitlines()
body_lines = []
skip = True
for line in lines:
    if line.startswith("---"):
        skip = False
        continue
    if not skip:
        body_lines.append(line)

new_md = header_update + "\n".join(body_lines)
with open(md_path, "w", encoding="utf-8") as f:
    f.write(new_md)

print("Successfully linked Official GitHub Project Board URL to roadmap & markdown board!")
