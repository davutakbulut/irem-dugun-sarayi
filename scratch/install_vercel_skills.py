import os
import shutil
import sys

print("==================================================")
print("🚀 INSTALLING VERCEL LABS SKILLS (vercel-labs/skills)")
print("==================================================")

target_workspace = '.skills'
os.makedirs(target_workspace, exist_ok=True)

skills_to_install = []

# 1. From vercel_skills/skills/find-skills
src_find = 'scratch/vercel_skills/skills/find-skills'
if os.path.exists(src_find):
    skills_to_install.append(('find-skills', src_find))

# 2. From vercel_agent_skills/skills/
src_agent_skills = 'scratch/vercel_agent_skills/skills'
if os.path.exists(src_agent_skills):
    for item in os.listdir(src_agent_skills):
        item_path = os.path.join(src_agent_skills, item)
        if os.path.isdir(item_path):
            skills_to_install.append((item, item_path))

installed_count = 0
installed_names = []

for name, path in skills_to_install:
    dest_ws = os.path.join(target_workspace, name)
    if os.path.exists(dest_ws):
        shutil.rmtree(dest_ws)
    shutil.copytree(path, dest_ws)
    installed_count += 1
    installed_names.append(name)
    print(f"✅ Installed Skill: '{name}' -> .skills/{name}/SKILL.md")

print(f"\n🎉 TOTAL VERCEL LABS SKILLS INSTALLED: {installed_count}")
print("==================================================")
