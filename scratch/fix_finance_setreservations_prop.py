import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_func_sig = "function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation }) {"
new_func_sig = "function FinanceComponent({ financialStats, reservations = [], setReservations = () => {}, venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation = () => {}, showToast = () => {} }) {"

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_func_sig in content:
        content = content.replace(old_func_sig, new_func_sig)
        print(f"Updated FinanceComponent signature in {h_file}")
    else:
        print(f"old_func_sig not found in {h_file}")

    # Also make sure setReservations is safely checked or falls back
    content = content.replace(
        "if (setReservations) {",
        "if (typeof setReservations === 'function') {"
    )

    content = content.replace(
        "if (showToast) {",
        "if (typeof showToast === 'function') {"
    )

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("setReservations prop fixed in all files!")
