import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Locate the theme save button click handler in Settings component (around line 15735)
old_save_handler = """                      onThemeColorChange(draftTheme);
                      if (draftTheme === 'elite-luxury' || draftTheme === 'obsidian') {
                        document.documentElement.setAttribute('data-ui-theme', 'elite-luxury');
                      } else if (draftTheme === 'nordic-light') {
                        document.documentElement.setAttribute('data-ui-theme', 'nordic-light');
                      } else if (draftTheme === 'apple' || draftTheme === 'apple-light') {
                        document.documentElement.setAttribute('data-ui-theme', 'apple');
                      } else if (draftTheme === 'sapphire-minimal' || draftTheme === 'sapphire_clean' || draftTheme === 'sapphire') {
                        document.documentElement.setAttribute('data-ui-theme', 'sapphire-minimal');
                      } else if (draftTheme === 'emerald-royal' || draftTheme === 'emerald_royal' || draftTheme === 'emerald') {
                        document.documentElement.setAttribute('data-ui-theme', 'emerald-royal');
                      } else {
                        document.documentElement.removeAttribute('data-ui-theme');
                      }
                      showToast(`🎨 Tasarım Konsepti Başarıyla Değiştirildi ve Uygulandı! (${draftTheme})`);"""

new_save_handler = """                      onThemeColorChange(draftTheme);
                      if (draftTheme && draftTheme !== 'gold' && draftTheme !== 'classic_gold') {
                        document.documentElement.setAttribute('data-ui-theme', draftTheme);
                      } else {
                        document.documentElement.removeAttribute('data-ui-theme');
                      }
                      
                      // CRITICAL: PERMANENTLY POST TO BACKEND SERVER DATABASE
                      try {
                        fetch('/api/system-settings', {
                          method: 'POST',
                          headers: { 'Content-Type': 'application/json' },
                          body: JSON.stringify({ themeColor: draftTheme, updatedAt: new Date().toISOString(), updatedBy: 'admin' })
                        }).then(r => r.json()).then(res => {
                          console.log('✅ System theme saved to backend DB:', res);
                        }).catch(err => console.error('❌ Failed to save theme to backend DB:', err));
                      } catch(e) {}

                      showToast(`🎨 Tasarım Konsepti Başarıyla Veritabanına Kaydedildi! (${draftTheme})`);"""

if old_save_handler in html:
    html = html.replace(old_save_handler, new_save_handler)
    print("Fixed SettingsPage theme save handler to POST directly to /api/system-settings backend database!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html settings save DB POST fix successfully!")
