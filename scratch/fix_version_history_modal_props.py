import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix VersionHistoryModalComponent invocation in App component
old_invocation = """          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent
            isOpen={isVersionModalOpen}
            onClose={() => setIsVersionModalOpen(false)}
          />"""

new_invocation = """          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent
            isOpen={isVersionModalOpen}
            onClose={() => setIsVersionModalOpen(false)}
            systemVersion={systemVersionState || systemSettings?.systemVersion || 'v1.4.59'}
            versionHistory={versionHistoryState && versionHistoryState.length > 0 ? versionHistoryState : systemSettings?.versionHistory}
          />"""

if old_invocation in html:
    html = html.replace(old_invocation, new_invocation)
    print("Updated VersionHistoryModalComponent invocation props in App component successfully!")
else:
    print("Could not find old_invocation in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html VersionHistoryModalComponent props fix successfully!")
