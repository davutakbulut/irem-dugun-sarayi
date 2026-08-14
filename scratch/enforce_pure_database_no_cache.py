import os

# 1. UPDATE server.js: Add no-cache headers to all API responses
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

no_cache_middleware = """
// STRICT RULE: ZERO CACHE - ALL RESPONSES 100% FRESH FROM MYSQL
app.use('/api', (req, res, next) => {
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
  res.setHeader('Pragma', 'no-cache');
  res.setHeader('Expires', '0');
  res.setHeader('Surrogate-Control', 'no-store');
  next();
});
"""

if "STRICT RULE: ZERO CACHE" not in server_code:
    pos = server_code.find("app.use(express.json")
    if pos != -1:
        server_code = server_code[:pos] + no_cache_middleware + "\n" + server_code[pos:]
        with open('server.js', 'w', encoding='utf-8') as f:
            f.write(server_code)
        print("Added strict no-cache headers middleware in server.js!")

# 2. UPDATE all HTML files: Neutralize CacheService for database entities and initialize state directly from API
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Clear localStorage on load to kill any lingering stale caches
    clear_cache_on_boot = """    // STRICT RULE: PURE REALTIME MYSQL DATABASE - ZERO LOCAL CACHING
    try {
      if (typeof localStorage !== 'undefined') {
        const preserveKeys = ['session_user', 'current_user', 'auth_token'];
        Object.keys(localStorage).forEach(k => {
          if (!preserveKeys.includes(k) && !k.startsWith('auth')) {
            localStorage.removeItem(k);
          }
        });
      }
    } catch(e){}
"""
    if "STRICT RULE: PURE REALTIME MYSQL DATABASE" not in content:
        pos_head = content.find("<script>")
        if pos_head != -1:
            content = content[:pos_head + 8] + "\n" + clear_cache_on_boot + content[pos_head + 8:]
            print(f"Added cache purge on boot in {h_file}")

    # Neutralize CacheService.get / set for data collections
    old_cache_engine = """    const CacheService = {
      get: (key, fallback) => {
        if (!getCacheEnabled() || typeof localStorage === 'undefined') return fallback;
        try {
          const item = localStorage.getItem(CACHE_PREFIX + key);
          return item ? JSON.parse(item) : fallback;
        } catch (e) {
          console.warn('Cache read error:', e);
          return fallback;
        }
      },
      set: (key, value) => {
        if (!getCacheEnabled() || typeof localStorage === 'undefined') return;
        try {
          localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(value));
        } catch (e) {
          console.warn('Cache write error (storage full?):', e);
        }
      },"""

    new_cache_engine = """    // ZERO CACHE ENGINE - 100% DIRECT MYSQL DATABASE DRIVEN
    const CacheService = {
      get: (key, fallback) => {
        // Only allow auth session, reject database entity caching
        if (key === 'session_user' || key === 'current_user') {
          try {
            const item = localStorage.getItem(CACHE_PREFIX + key);
            return item ? JSON.parse(item) : fallback;
          } catch (e) { return fallback; }
        }
        return fallback; // Return initial fallback without reading stale localStorage
      },
      set: (key, value) => {
        if (key === 'session_user' || key === 'current_user') {
          try {
            localStorage.setItem(CACHE_PREFIX + key, JSON.stringify(value));
          } catch(e){}
        }
        // Do not cache venues, reservations, company settings etc in localStorage
      },"""

    if old_cache_engine in content:
        content = content.replace(old_cache_engine, new_cache_engine)
        print(f"Neutralized data caching in CacheService for {h_file}")

    # Ensure initial states in App start empty/null and load from MySQL
    old_venues_init = "const [venues, setVenues] = useState(() => CacheService.get('venues', INITIAL_VENUES) || INITIAL_VENUES);"
    new_venues_init = "const [venues, setVenues] = useState([]);"

    old_services_init = "const [services, setServices] = useState(() => CacheService.get('services', INITIAL_SERVICES) || INITIAL_SERVICES);"
    new_services_init = "const [services, setServices] = useState([]);"

    old_campaigns_init = "const [campaigns, setCampaigns] = useState(() => CacheService.get('campaigns', INITIAL_CAMPAIGNS) || INITIAL_CAMPAIGNS);"
    new_campaigns_init = "const [campaigns, setCampaigns] = useState([]);"

    old_customers_init = "const [customers, setCustomers] = useState(() => CacheService.get('customers', INITIAL_CUSTOMERS) || INITIAL_CUSTOMERS);"
    new_customers_init = "const [customers, setCustomers] = useState([]);"

    old_comp_init = "const [companySettings, setCompanySettings] = useState(() => CacheService.get('company_settings', DEFAULT_COMPANY_SETTINGS));"
    new_comp_init = "const [companySettings, setCompanySettings] = useState(DEFAULT_COMPANY_SETTINGS);"

    content = content.replace(old_venues_init, new_venues_init)
    content = content.replace(old_services_init, new_services_init)
    content = content.replace(old_campaigns_init, new_campaigns_init)
    content = content.replace(old_customers_init, new_customers_init)
    content = content.replace(old_comp_init, new_comp_init)

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("Database-only & Zero-Cache rule applied 100% across the entire system!")
