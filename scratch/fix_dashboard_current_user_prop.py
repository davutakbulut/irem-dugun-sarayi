import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_sig = "function DashboardComponent({ activeRole, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"
new_sig = "function DashboardComponent({ activeRole, currentUser, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"

if old_sig in content:
    content = content.replace(old_sig, new_sig)
    print("1. Added currentUser to DashboardComponent function signature.")
else:
    print("WARNING: Could not find old_sig in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
