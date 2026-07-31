import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update SettingsPage component to sync draftTheme state whenever themeColor prop changes
old_settings_state = "const [draftTheme, setDraftTheme] = useState(themeColor || 'gold');"

new_settings_state = """const [draftTheme, setDraftTheme] = useState(themeColor || 'gold');

      useEffect(() => {
        if (themeColor) {
          setDraftTheme(themeColor);
        }
      }, [themeColor]);"""

if old_settings_state in html and "setDraftTheme(themeColor);" not in html:
    html = html.replace(old_settings_state, new_settings_state)
    print("Fixed SettingsPage draftTheme state sync with themeColor prop!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html SettingsPage draftTheme sync fix successfully!")
