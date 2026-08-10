import os

# 1. Update serve_fast_3g.py to add 'expenses': 'db_expenses.json'
server_file = 'scratch/serve_fast_3g.py'
with open(server_file, 'r', encoding='utf-8') as f:
    s_content = f.read()

old_entities = """                    'services': 'db_services.json',
                    'draftReservations': 'db_draft_reservations.json'"""

new_entities = """                    'services': 'db_services.json',
                    'draftReservations': 'db_draft_reservations.json',
                    'expenses': 'db_expenses.json'"""

s_content = s_content.replace(old_entities, new_entities)

with open(server_file, 'w', encoding='utf-8') as f:
    f.write(s_content)

print("1. Updated serve_fast_3g.py with 'expenses': 'db_expenses.json' sync.")

# 2. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    h_content = f.read()

# Add expenses state to App component
old_app_states = "      const [draftReservations, setDraftReservations] = useState([]);"
new_app_states = """      const [draftReservations, setDraftReservations] = useState([]);
      const [expenses, setExpenses] = useState([]);"""

if old_app_states in h_content:
    h_content = h_content.replace(old_app_states, new_app_states)
    print("2. Added expenses state to App component.")

# Add expenses useEffect POST handler in App component
old_effects_end = """      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('users', users);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(users)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users })
          }).catch(() => {});
        }
      }, [users]);"""

new_effects_end = """      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('users', users);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(users)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ users })
          }).catch(() => {});
        }
      }, [users]);
      useEffect(() => {
        if (!isInitialLoadDoneRef.current) return;
        CacheService.set('expenses', expenses);
        const fetchFn = window.fetchWithRetry || fetch;
        if (fetchFn && Array.isArray(expenses)) {
          fetchFn('/api/system-settings', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expenses })
          }).catch(() => {});
        }
      }, [expenses]);"""

if old_effects_end in h_content:
    h_content = h_content.replace(old_effects_end, new_effects_end)
    print("3. Added expenses useEffect POST handler to App component.")

# Add expenses loader in fetchSystemSettings
old_fetch_drafts = """                  if (data.draftReservations !== undefined && Array.isArray(data.draftReservations)) {
                    setDraftReservations(prev => {
                      if (JSON.stringify(prev) !== JSON.stringify(data.draftReservations)) {
                        return data.draftReservations;
                      }
                      return prev;
                    });
                  }"""

new_fetch_drafts = """                  if (data.draftReservations !== undefined && Array.isArray(data.draftReservations)) {
                    setDraftReservations(prev => {
                      if (JSON.stringify(prev) !== JSON.stringify(data.draftReservations)) {
                        return data.draftReservations;
                      }
                      return prev;
                    });
                  }
                  if (data.expenses !== undefined && Array.isArray(data.expenses)) {
                    setExpenses(data.expenses);
                  }"""

if old_fetch_drafts in h_content:
    h_content = h_content.replace(old_fetch_drafts, new_fetch_drafts)
    print("4. Added expenses loader to fetchSystemSettings.")

# Update FinanceComponent signature & remove hardcoded demo expenses array
old_finance_comp = """    function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], onUpdateReservation }) {
      const [expenses, setExpenses] = useState([
        { id: 'exp-1', title: 'Orkestra & Ses Sistemi Ödemesi', category: 'Personel & Sanatçı', type: 'gider', amount: 18000, date: '2026-08-01', status: 'Ödendi' },
        { id: 'exp-2', title: 'Salon Garson ve Mutfak Yevmiyeleri', category: 'Personel & Sanatçı', type: 'gider', amount: 24500, date: '2026-08-05', status: 'Ödendi' },
        { id: 'exp-3', title: 'Peyzaj & Çiçek Süsleme Malzemeleri', category: 'Dekorasyon & Çiçek', type: 'gider', amount: 14200, date: '2026-08-10', status: 'Ödendi' },
        { id: 'exp-4', title: 'Elektrik & Jeneratör Yakıt Faturası', category: 'Faturalar & Enerji', type: 'gider', amount: 16800, date: '2026-08-12', status: 'Bekliyor' },
        { id: 'exp-5', title: 'Pasta & Catering Malzeme Alımı', category: 'Yiyecek & İçecek', type: 'gider', amount: 32000, date: '2026-08-15', status: 'Ödendi' }
      ]);"""

new_finance_comp = """    function FinanceComponent({ financialStats, reservations = [], venues = [], services = [], expenses = [], setExpenses = () => {}, onUpdateReservation }) {"""

if old_finance_comp in h_content:
    h_content = h_content.replace(old_finance_comp, new_finance_comp)
    print("5. Refactored FinanceComponent to pull expenses from DB props and removed demo hardcoded array.")

# Update FinanceComponent render call in App component to pass expenses and setExpenses
old_finance_call = """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      venues={venues}
                      services={services}
                      onUpdateReservation={handleSaveReservation}
                    />
                  )}"""

new_finance_call = """                  {activeTab === 'finance' && (
                    <FinanceComponent
                      financialStats={financialStats}
                      reservations={reservations}
                      venues={venues}
                      services={services}
                      expenses={expenses}
                      setExpenses={setExpenses}
                      onUpdateReservation={handleSaveReservation}
                    />
                  )}"""

if old_finance_call in h_content:
    h_content = h_content.replace(old_finance_call, new_finance_call)
    print("6. Passed expenses & setExpenses props to FinanceComponent in App component.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(h_content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(h_content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(h_content)

print("Synced index.html to yonetim.html and dist/index.html!")
