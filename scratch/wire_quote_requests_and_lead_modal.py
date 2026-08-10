import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update TAB_TO_PATH, TAB_TO_SLUG, TAB_LABELS
if "'customers': '/yonetim/musteriler'," in content:
    content = content.replace(
        "'customers': '/yonetim/musteriler',",
        "'customers': '/yonetim/musteriler',\n    'quote-requests': '/yonetim/teklif-talepleri',"
    )

if "'customers': 'musteriler'," in content:
    content = content.replace(
        "'customers': 'musteriler',",
        "'customers': 'musteriler',\n    'quote-requests': 'teklif-talepleri',"
    )

if "'customers': 'Müşteri Rehberi (CRM)'," in content:
    content = content.replace(
        "'customers': 'Müşteri Rehberi (CRM)',",
        "'customers': 'Müşteri Rehberi (CRM)',\n    'quote-requests': 'Fiyat Teklif Talepleri (Leads)',"
    )

if "'customers': ['admin', 'manager', 'sales', 'reception']," in content:
    content = content.replace(
        "'customers': ['admin', 'manager', 'sales', 'reception'],",
        "'customers': ['admin', 'manager', 'sales', 'reception'],\n    'quote-requests': ['admin', 'manager', 'sales', 'reception'],"
    )

# 2. Add quoteRequests state and effect in App()
old_app_states = "      const [customers, setCustomers] = useState([]);"
new_app_states = """      const [customers, setCustomers] = useState([]);
      const [quoteRequests, setQuoteRequests] = useState(() => CacheService.get('quote_requests', INITIAL_QUOTE_REQUESTS));

      const handleSaveQuoteRequest = (newQuote) => {
        setQuoteRequests(prev => {
          const updated = [newQuote, ...(prev || [])];
          CacheService.set('quote_requests', updated);
          if (window.fetchWithRetry) {
            window.fetchWithRetry('/api/public-settings', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ quoteRequests: updated })
            }).catch(() => {});
          }
          return updated;
        });
      };"""

if old_app_states in content:
    content = content.replace(old_app_states, new_app_states)
    print("Added quoteRequests state and handleSaveQuoteRequest handler!")

# 3. Add sidebar navigation item for quote-requests
old_sidebar_cust = "{ id: 'customers', label: 'Müşteri Rehberi (CRM)', icon: 'user', fallbackEmoji: '' },"
new_sidebar_cust = """{ id: 'customers', label: 'Müşteri Rehberi (CRM)', icon: 'user', fallbackEmoji: '' },
                        { id: 'quote-requests', label: 'Teklif Talepleri (Leads)', icon: 'document', fallbackEmoji: '', badge: 'CANLI' },"""

if old_sidebar_cust in content:
    content = content.replace(old_sidebar_cust, new_sidebar_cust)
    print("Added Teklif Talepleri (Leads) item to sidebar navigation!")

# 4. Add quote-requests page renderer in App()
old_page_render = "{activeTab === 'customers' && ("
new_page_render = """{activeTab === 'quote-requests' && (
                    <QuoteRequestsPageComponent
                      quoteRequests={quoteRequests}
                      setQuoteRequests={setQuoteRequests}
                      showToast={showToast}
                      navigateTo={navigateTo}
                      setRedAlertModalData={setRedAlertModalData}
                    />
                  )}

                  {activeTab === 'customers' && ("""

if old_page_render in content:
    content = content.replace(old_page_render, new_page_render)
    print("Added QuoteRequestsPageComponent to page render switch!")

# 5. Pass onSaveQuoteRequest to LeadModal calls
old_lead_modal_render = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} />"
new_lead_modal_render = "<LeadModal isOpen={isLeadModalOpen} onClose={() => setIsLeadModalOpen(false)} onSaveQuoteRequest={handleSaveQuoteRequest} showToast={showToast} />"

if old_lead_modal_render in content:
    content = content.replace(old_lead_modal_render, new_lead_modal_render)
    print("Passed handleSaveQuoteRequest and showToast to LeadModal!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
