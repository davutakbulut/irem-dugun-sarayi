import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update App state initializers to use server-first defaults instead of CacheService localStorage fallbacks
old_state_init = """      const [venues, setVenues] = useState(() => CacheService.get('venues', INITIAL_VENUES));
      const [services, setServices] = useState(() => CacheService.get('services', INITIAL_SERVICES));
      const [campaigns, setCampaigns] = useState(() => CacheService.get('campaigns', INITIAL_CAMPAIGNS));
      const [customers, setCustomers] = useState(() => {
        const cached = CacheService.get('customers', INITIAL_CUSTOMERS);
        const cachedArray = Array.isArray(cached) ? cached : [];

        const customerMap = new Map();

        // 1. Initial customers
        INITIAL_CUSTOMERS.forEach(c => {
          customerMap.set(c.id, c);
        });

        // 2. Cached customers
        cachedArray.forEach(c => {
          customerMap.set(c.id, c);
        });

        // 3. Extract & Auto-create full Customer records from all 45+ reservations
        const activeResList = CacheService.get('reservations', INITIAL_RESERVATIONS) || INITIAL_RESERVATIONS;
        (activeResList || []).forEach(r => {
          const cId = r.customerId || `cust_${(r.id || '').toLowerCase()}`;
          if (r.customerName && !customerMap.has(cId)) {
            customerMap.set(cId, {
              id: cId,
              name: r.customerName,
              email: r.customerEmail || `${cId}@example.com`,
              phone: r.customerPhone || '+90 532 000 0000',
              secondaryPhone: r.secondaryPhone || '',
              address: r.invoiceAddress || 'Atatürk Mah. Sapanca / Sakarya',
              taxType: r.invoiceType || 'individual',
              tcNo: r.tcNo || '12345678901',
              taxOffice: r.taxOffice || 'Sapanca VD',
              vknNo: r.vknNo || '',
              followUp: false,
              followUpNote: `Ağustos 2026 Rezervasyonu (${r.venueName || 'Balo Salonu'})`,
              avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80'
            });
          }
        });

        return Array.from(customerMap.values());
      });"""

new_state_init = """      const [venues, setVenues] = useState(INITIAL_VENUES);
      const [services, setServices] = useState(INITIAL_SERVICES);
      const [campaigns, setCampaigns] = useState(INITIAL_CAMPAIGNS);
      const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);"""

if old_state_init in content:
    content = content.replace(old_state_init, new_state_init)
    print("1. Updated App state initializers to eliminate localStorage cache interference.")

# 2. Update draftReservations initializer to start empty [] and load from server DB
old_draft_init = "const [draftReservations, setDraftReservations] = useState(() => CacheService.get('draft_reservations', []));"
new_draft_init = "const [draftReservations, setDraftReservations] = useState([]);"

if old_draft_init in content:
    content = content.replace(old_draft_init, new_draft_init)
    print("2. Updated draftReservations state initializer to start empty [] and load from server DB.")

# 3. Update users state initializer to use INITIAL_USERS
old_users_init = """      const [users, setUsers] = useState(() => {
        const cachedUsers = CacheService.get('users', null);
        if (cachedUsers && Array.isArray(cachedUsers) && cachedUsers.length > 0) {
          return cachedUsers;
        }

        const userMap = new Map();

        // 1. Initial users (Mustafa Beyazyüz Admin + İrem Yılmaz + Canan + Murat)
        INITIAL_USERS.forEach(u => {
          const key = (u.email || u.id).toLowerCase();
          userMap.set(key, u);
        });

        return Array.from(userMap.values());
      });"""

new_users_init = "      const [users, setUsers] = useState(INITIAL_USERS);"

if old_users_init in content:
    content = content.replace(old_users_init, new_users_init)
    print("3. Updated users state initializer to use INITIAL_USERS directly.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
