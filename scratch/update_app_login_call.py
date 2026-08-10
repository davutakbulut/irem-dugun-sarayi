import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_call = """          <LoginComponent
            users={users}
            showToast={showToast}
            onLoginSuccess={(userObj) => {
              let returnUrl = null;
              let returnTab = null;
              try {
                returnUrl = sessionStorage.getItem('login_return_url');
                returnTab = sessionStorage.getItem('login_return_tab');
                sessionStorage.removeItem('login_return_url');
                sessionStorage.removeItem('login_return_tab');
              } catch(e){}

              let targetTab = returnTab || 'dashboard';
              if (targetTab === 'login') targetTab = 'dashboard';
              
              let targetPath = returnUrl || (TAB_TO_PATH[targetTab] || '/yonetim');
              if (targetPath === '/giris' || targetPath === '/login') {
                targetPath = '/yonetim';
                targetTab = 'dashboard';
              }

              setSessionUser(userObj);
              CacheService.set('session_user', userObj);
              setCurrentUserState(userObj);
              CacheService.set('current_user', userObj);
              setActiveRole(userObj.role || 'admin');
              setActiveTabState(targetTab);
              if (typeof window !== 'undefined' && window.history && window.history.pushState) {
                window.history.pushState({}, '', targetPath);
              }
              const tabLabel = TAB_LABELS[targetTab] || 'Yönetim Paneli';
              showToast(`Hoş geldiniz ${userObj.name}! ${targetTab !== 'dashboard' ? `"${tabLabel}" sayfasına aktarılıyorsunuz...` : 'Yönetim paneline aktarılıyorsunuz...'}`);
            }}
            showToast={showToast}
          />"""

new_call = """          <LoginComponent
            users={users}
            customers={customers}
            showToast={showToast}
            onLoginSuccess={(userObj) => {
              let returnUrl = null;
              let returnTab = null;
              try {
                returnUrl = sessionStorage.getItem('login_return_url');
                returnTab = sessionStorage.getItem('login_return_tab');
                sessionStorage.removeItem('login_return_url');
                sessionStorage.removeItem('login_return_tab');
              } catch(e){}

              const isCustomerRole = userObj.role === 'musteri';
              let targetTab = returnTab || (isCustomerRole ? 'musteri-portali' : 'dashboard');
              if (targetTab === 'login') targetTab = isCustomerRole ? 'musteri-portali' : 'dashboard';
              
              let targetPath = returnUrl || (TAB_TO_PATH[targetTab] || (isCustomerRole ? '/yonetim/musteri-portali' : '/yonetim'));
              if (targetPath === '/giris' || targetPath === '/login') {
                targetPath = isCustomerRole ? '/yonetim/musteri-portali' : '/yonetim';
                targetTab = isCustomerRole ? 'musteri-portali' : 'dashboard';
              }

              setSessionUser(userObj);
              CacheService.set('session_user', userObj);
              setCurrentUserState(userObj);
              CacheService.set('current_user', userObj);
              setActiveRole(userObj.role || 'admin');
              setActiveTabState(targetTab);
              if (typeof window !== 'undefined' && window.history && window.history.pushState) {
                window.history.pushState({}, '', targetPath);
              }
              const tabLabel = TAB_LABELS[targetTab] || (isCustomerRole ? 'Müşteri Portalı' : 'Yönetim Paneli');
              showToast(`Hoş geldiniz ${userObj.name}! (${isCustomerRole ? 'Müşteri Portalı\'na aktarılıyorsunuz...' : 'Yönetim paneline aktarılıyorsunuz...'})`);
            }}
          />"""

if old_call in content:
    content = content.replace(old_call, new_call)
    print("1. Successfully updated App component LoginComponent call with customers prop and customer portal routing!")
else:
    print("WARNING: Could not find old_call in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
