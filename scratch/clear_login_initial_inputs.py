import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_initial_states = """      const [emailInput, setEmailInput] = useState('mustafa@iremdugunsarayi.com');
      const [phoneInput, setPhoneInput] = useState('0532 123 4567');
      const [password, setPassword] = useState('Msytf2026');"""

new_initial_states = """      const [emailInput, setEmailInput] = useState('');
      const [phoneInput, setPhoneInput] = useState('');
      const [password, setPassword] = useState('');"""

if old_initial_states in content:
    content = content.replace(old_initial_states, new_initial_states)
    print("1. Successfully updated initial login inputs state to empty strings ''!")
else:
    print("WARNING: Could not find old_initial_states in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
