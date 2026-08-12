import os, re

files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for f_path in files:
    if not os.path.exists(f_path):
        continue
    with open(f_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove SystemGuidePageComponent component definition
    sg_comp_start = "function SystemGuidePageComponent({"
    if sg_comp_start in content:
        c_start = content.find(sg_comp_start)
        # Find next top-level function definition
        c_end = content.find("function ", c_start + len(sg_comp_start))
        if c_start != -1 and c_end != -1:
            content = content[:c_start] + content[c_end:]
            print(f"Successfully removed SystemGuidePageComponent from {f_path}!")

    # 2. Remove system-guide from route mappings
    content = content.replace("      'system-guide': 'sistem-kilavuzu',\n", "")
    content = content.replace("      'sistem-kilavuzu': 'system-guide',\n", "")
    content = content.replace("      'kilavuz': 'system-guide',\n", "")
    content = content.replace("      'system-guide': '/yonetim/sistem-kilavuzu',\n", "")
    content = content.replace("      'system-guide': ['admin', 'satisci', 'sosyal_medyaci', 'musteri'],\n", "")

    # 3. Remove system-guide menu items from sidebar & navigation lists
    item_pattern_1 = r"\{\s*id:\s*'system-guide',[^}]*\},?\n?"
    content = re.sub(item_pattern_1, "", content)

    # 4. Remove activeTab === 'system-guide' JSX rendering block
    tab_block_start = "{activeTab === 'system-guide' && ("
    if tab_block_start in content:
        tb_start = content.find(tab_block_start)
        tb_end = content.find(")}", tb_start)
        if tb_start != -1 and tb_end != -1:
            content = content[:tb_start] + content[tb_end + 2:]
            print(f"Successfully removed system-guide tab render block from {f_path}!")

    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Completely removed system-guide from {f_path}!")

print("System Guide page destruction completed!")
