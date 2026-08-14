import os

html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

old_call = """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      venues={venues}
                      services={services}
                      onUpdateReservation={handleUpdateReservation}
                    />
                  )}"""

new_call = """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      venues={venues}
                      services={services}
                      expenses={expenses}
                      setExpenses={setExpenses}
                      onUpdateReservation={handleUpdateReservation}
                    />
                  )}"""

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    if old_call in content:
        content = content.replace(old_call, new_call)
        with open(h_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Passed expenses and setExpenses props to FinanceComponent in {h_file}")
    else:
        print(f"old_call not found in {h_file}")

print("All files updated successfully!")
