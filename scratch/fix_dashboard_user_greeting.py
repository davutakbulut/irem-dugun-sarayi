import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Synchronize currentUserState with sessionUser in App component
old_session_effect = """      useEffect(() => {
        CacheService.set('session_user', sessionUser);
      }, [sessionUser]);"""

new_session_effect = """      useEffect(() => {
        CacheService.set('session_user', sessionUser);
        if (sessionUser && sessionUser.name) {
          setCurrentUserState(sessionUser);
          CacheService.set('current_user', sessionUser);
        }
      }, [sessionUser]);"""

if old_session_effect in content:
    content = content.replace(old_session_effect, new_session_effect, 1)
    print("1. Added sessionUser sync effect to update currentUserState automatically.")
else:
    print("WARNING: Could not find old_session_effect in index.html!")

# 2. Update DashboardComponent greeting logic to use dynamic logged-in user name
old_greeting_logic = """              {(() => {
                const userName = currentUser?.name || (activeRole === 'admin' ? 'Mustafa Bey' : (activeRole === 'satisci' ? 'Sümeyra Hanım' : 'Kullanıcı'));
                return (
                  <>
                    <h2 className="text-2xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2 flex items-center space-x-2">
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Hoş Geldiniz, {userName}! 👋</span>
                    </h2>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      {activeRole === 'admin' && `Sayın ${userName}, İrem Düğün Sarayı genel finansal ciro verileri, canlı analiz grafikleri ve yapay zeka önerileriniz aşağıdadır.`}
                      {activeRole === 'satisci' && `Sayın ${userName}, düğün salonu kiralama durumları, boş gün takvimi ve aktif rezervasyon satış süreçlerinizi buradan yönetebilirsiniz.`}
                      {activeRole === 'sosyal_medyaci' && `Sayın ${userName}, salon galerisi görselleri, medya yükleme alanı ve içerik takvimi takibinizi buradan gerçekleştirebilirsiniz.`}
                      {activeRole === 'musteri' && `Sayın ${userName}, düğün organizasyonunuzun canlı detayları, salon bilgileri ve kalan ödeme bakiyeniz aşağıdadır.`}
                    </p>
                  </>
                );
              })()}"""

new_greeting_logic = """              {(() => {
                const activeUser = currentUser || sessionUser;
                const userName = activeUser?.name || 'Sayın Yöneticimiz';
                return (
                  <>
                    <h2 className="text-2xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2 flex items-center space-x-2">
                      <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                      <span>Hoş Geldiniz, {userName}! 👋</span>
                    </h2>
                    <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                      {activeRole === 'admin' && `Sayın ${userName}, İrem Düğün Sarayı genel finansal ciro verileri, canlı analiz grafikleri ve yapay zeka önerileriniz aşağıdadır.`}
                      {activeRole === 'satisci' && `Sayın ${userName}, düğün salonu kiralama durumları, boş gün takvimi ve aktif rezervasyon satış süreçlerinizi buradan yönetebilirsiniz.`}
                      {activeRole === 'sosyal_medyaci' && `Sayın ${userName}, salon galerisi görselleri, medya yükleme alanı ve içerik takvimi takibinizi buradan gerçekleştirebilirsiniz.`}
                      {activeRole === 'musteri' && `Sayın ${userName}, düğün organizasyonunuzun canlı detayları, salon bilgileri ve kalan ödeme bakiyeniz aşağıdadır.`}
                    </p>
                  </>
                );
              })()}"""

if old_greeting_logic in content:
    content = content.replace(old_greeting_logic, new_greeting_logic, 1)
    print("2. Updated DashboardComponent greeting logic to use dynamic logged-in user name!")
else:
    print("WARNING: Could not find old_greeting_logic in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
