import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update DashboardComponent signature to receive currentUser
old_comp_def = "function DashboardComponent({ activeRole, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"
new_comp_def = "function DashboardComponent({ activeRole, currentUser, venues = [], reservations = [], financialStats, onNewResClick, onTabChange, onConvertToCampaign, onUpdateVenuePrice }) {"

if old_comp_def in content:
    print("Found DashboardComponent signature.")

# 2. Update DashboardComponent call in App component to pass currentUser={currentUserState}
old_call = """                  {activeTab === 'dashboard' && (
                    <DashboardComponent
                      activeRole={activeRole}
                      venues={venues}"""

new_call = """                  {activeTab === 'dashboard' && (
                    <DashboardComponent
                      activeRole={activeRole}
                      currentUser={currentUserState}
                      venues={venues}"""

if old_call in content:
    content = content.replace(old_call, new_call)
    print("1. Passed currentUser={currentUserState} to DashboardComponent in App.")
else:
    print("WARNING: Could not find old_call in index.html!")

# 3. Replace fixed welcome title and subtitle with personalized userName
old_header_block = """              <h2 className="text-2xl font-heading font-extrabold text-slate-800 dark:text-gray-100 mt-2 flex items-center space-x-2">
                <ThemeIcon icon="sparkles" fallbackEmoji="" className="w-5 h-5 text-amber-500 shrink-0" />
                <span>
                  {activeRole === 'admin' && 'Hoş Geldiniz, İrem Hanım (Admin)'}
                  {activeRole === 'satisci' && 'Satış Operasyon Paneli - İrem Düğün Sarayı'}
                  {activeRole === 'sosyal_medyaci' && 'Medya & Fotoğraf Yönetim Ekranı'}
                  {activeRole === 'musteri' && 'Değerli Müşterimiz, Hoş Geldiniz! '}
                </span>
              </h2>
              <p className="text-xs text-slate-500 dark:text-gray-400 mt-1">
                {activeRole === 'admin' && 'İrem Düğün Sarayı genel finansal ciro verileri, canlı analiz grafikleri ve yapay zeka önerileri.'}
                {activeRole === 'satisci' && 'Düğün salonu kiralama durumları, boş gün takvimi ve aktif rezervasyon satış süreçleri.'}
                {activeRole === 'sosyal_medyaci' && 'Salon galerisi görselleri, medya yükleme alanı ve içerik takvimi takibi.'}
                {activeRole === 'musteri' && 'Düğün organizasyonunuzun canlı detayları, salon bilgileri ve kalan ödeme bakiyeniz.'}
              </p>"""

new_header_block = """              {(() => {
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

if old_header_block in content:
    content = content.replace(old_header_block, new_header_block)
    print("2. Replaced static header banner with personalized welcome title & subtitle.")
else:
    print("WARNING: Could not find old_header_block in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
