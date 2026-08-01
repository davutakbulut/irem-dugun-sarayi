import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_block = """                  {activeTab === 'mind-map' && (
                    <MindMapPageComponent navigateTo={navigateTo} />
                  )}"""

new_block = """                  {activeTab === 'mind-map' && (
                    <MindMapPageComponent navigateTo={navigateTo} />
                  )}

                  {activeTab === 'system-guide' && (
                    <SystemGuidePageComponent navigateTo={navigateTo} activeRole={activeRole} themeColor={themeColor} menuLayout={menuLayout} />
                  )}"""

if old_block in html:
    html = html.replace(old_block, new_block)
    print("Added SystemGuidePageComponent render block to App component successfully!")
else:
    print("Could not find old_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html SystemGuidePageComponent rendering fix successfully!")
