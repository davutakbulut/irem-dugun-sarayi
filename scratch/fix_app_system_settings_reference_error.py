import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_invocation = """          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent
            isOpen={isVersionModalOpen}
            onClose={() => setIsVersionModalOpen(false)}
            systemVersion={systemVersion || systemSettings?.systemVersion || 'v1.4.60'}
            versionHistory={versionHistoryState && versionHistoryState.length > 0 ? versionHistoryState : systemSettings?.versionHistory}
          />"""

new_invocation = """          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent
            isOpen={isVersionModalOpen}
            onClose={() => setIsVersionModalOpen(false)}
            systemVersion={systemVersion || 'v1.4.62'}
            versionHistory={versionHistoryState}
          />"""

if old_invocation in html:
    html = html.replace(old_invocation, new_invocation)
    print("Fixed systemSettings ReferenceError in index.html successfully!")
else:
    print("Could not find old_invocation in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html systemSettings ReferenceError fix successfully!")
