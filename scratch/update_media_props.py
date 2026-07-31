import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update MediaComponent invocation in App component to pass setReservations and activeRole
old_invocation = '<MediaComponent reservations={reservations} showToast={showToast} />'
new_invocation = '<MediaComponent reservations={reservations} setReservations={setReservations} activeRole={activeRole} showToast={showToast} />'

if old_invocation in html:
    html = html.replace(old_invocation, new_invocation)
    print("Updated MediaComponent props in App!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated MediaComponent invocation successfully!")
