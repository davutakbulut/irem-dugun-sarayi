import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update App state initializers to start EMPTY [] for all entities
old_inits = """      const [venues, setVenues] = useState(INITIAL_VENUES);
      const [services, setServices] = useState(INITIAL_SERVICES);
      const [campaigns, setCampaigns] = useState(INITIAL_CAMPAIGNS);
      const [customers, setCustomers] = useState(INITIAL_CUSTOMERS);"""

new_inits = """      const [venues, setVenues] = useState([]);
      const [services, setServices] = useState([]);
      const [campaigns, setCampaigns] = useState([]);
      const [customers, setCustomers] = useState([]);"""

if old_inits in content:
    content = content.replace(old_inits, new_inits)
    print("1. Updated App state initializers to start empty [].")

# 2. Update fetchSystemSettings entity loaders to accept [] from DB without requiring length > 0
old_fetch_loaders = """                  if (data.campaigns && Array.isArray(data.campaigns) && data.campaigns.length > 0) {
                    setCampaigns(data.campaigns);
                  }
                  if (data.users && Array.isArray(data.users) && data.users.length > 0) {
                    setUsers(data.users);
                  }
                  if (data.roles && Array.isArray(data.roles) && data.roles.length > 0) {
                    setRolesState(data.roles);
                  }
                  if (data.tab_permissions && typeof data.tab_permissions === 'object') {
                    setTabPermissionsState(prev => ({ ...prev, ...data.tab_permissions }));
                  }
                  if (data.customers && Array.isArray(data.customers) && data.customers.length > 0) {
                    setCustomers(data.customers);
                  }
                  if (data.systemVersion) {
                    setSystemVersion(data.systemVersion);
                  }
                  if (data.versionHistory) {
                    setVersionHistoryState(data.versionHistory);
                  }
                  if (data.venues && Array.isArray(data.venues)) {
                    setVenues(data.venues);
                  }
                  if (data.services && Array.isArray(data.services)) {
                    setServices(data.services);
                  }"""

new_fetch_loaders = """                  if (data.campaigns !== undefined && Array.isArray(data.campaigns)) {
                    setCampaigns(data.campaigns);
                  }
                  if (data.users !== undefined && Array.isArray(data.users)) {
                    setUsers(data.users);
                  }
                  if (data.roles !== undefined && Array.isArray(data.roles)) {
                    setRolesState(data.roles);
                  }
                  if (data.tab_permissions && typeof data.tab_permissions === 'object') {
                    setTabPermissionsState(prev => ({ ...prev, ...data.tab_permissions }));
                  }
                  if (data.customers !== undefined && Array.isArray(data.customers)) {
                    setCustomers(data.customers);
                  }
                  if (data.systemVersion) {
                    setSystemVersion(data.systemVersion);
                  }
                  if (data.versionHistory) {
                    setVersionHistoryState(data.versionHistory);
                  }
                  if (data.venues !== undefined && Array.isArray(data.venues)) {
                    setVenues(data.venues);
                  }
                  if (data.services !== undefined && Array.isArray(data.services)) {
                    setServices(data.services);
                  }"""

if old_fetch_loaders in content:
    content = content.replace(old_fetch_loaders, new_fetch_loaders)
    print("2. Updated fetchSystemSettings entity loaders to accept empty [] from server DB.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
