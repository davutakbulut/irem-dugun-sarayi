import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add state to App component
old_state = """      const [isVersionModalOpen, setIsVersionModalOpen] = useState(false);"""
new_state = """      const [isVersionModalOpen, setIsVersionModalOpen] = useState(false);
      const [isEmailTemplateModalOpen, setIsEmailTemplateModalOpen] = useState(false);"""

if old_state in content:
    content = content.replace(old_state, new_state)
    print("1. Added isEmailTemplateModalOpen state to App component.")

# 2. Add EmailTemplateModalComponent rendering before VersionHistoryModalComponent
old_modal = """          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent"""

new_modal = """          {/* EMAIL TEMPLATES CENTER MODAL */}
          {isEmailTemplateModalOpen && (
            <EmailTemplateModalComponent
              onClose={() => setIsEmailTemplateModalOpen(false)}
              customers={customers}
              reservations={reservations}
              venues={venues}
              showToast={showToast}
            />
          )}

          {/* SYSTEM VERSION HISTORY MODAL */}
          <VersionHistoryModalComponent"""

if old_modal in content:
    content = content.replace(old_modal, new_modal)
    print("2. Added EmailTemplateModalComponent modal rendering to App component.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
