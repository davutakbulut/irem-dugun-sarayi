import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_state = """      const [showForgotModal, setShowForgotModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');"""

new_state = """      const [showForgotModal, setShowForgotModal] = useState(false);
      const [showHelpModal, setShowHelpModal] = useState(false);
      const [forgotSuccessMail, setForgotSuccessMail] = useState(null);
      const [forgotInput, setForgotInput] = useState('');"""

if old_state in content:
    content = content.replace(old_state, new_state)
    print("1. Added showHelpModal state declaration back to LoginComponent.")
else:
    print("WARNING: Could not find old_state in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
