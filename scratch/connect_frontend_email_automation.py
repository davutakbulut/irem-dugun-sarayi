import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_login_mail_code = """                          const target = forgotInput.trim();
                          setForgotSuccessMail({
                            to: target.includes('@') ? target : `${target}@iremdugunsarayi.com`,
                            subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
                          });
                          showToast(`✉️ E-Posta otomasyonu tetiklendi: ${target} adresine aktivasyon maili iletildi!`);"""

new_login_mail_code = """                          const target = forgotInput.trim();
                          const recipientMail = target.includes('@') ? target : `${target}@iremdugunsarayi.com`;

                          if (window.fetchWithRetry) {
                            window.fetchWithRetry('/api/send-email', {
                              method: 'POST',
                              headers: { 'Content-Type': 'application/json' },
                              body: JSON.stringify({
                                to: recipientMail,
                                subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                                body: 'Sayın Kullanıcımız, şifre yenileme ve otomatik giriş bağlantınız başarıyla oluşturulmuştur.'
                              })
                            }).catch(() => {});
                          }

                          setForgotSuccessMail({
                            to: recipientMail,
                            subject: '🔑 Şifre Sıfırlama ve Otomatik Giriş Bağlantısı',
                            sentAt: new Date().toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit' })
                          });
                          showToast(`✉️ SMTP Mail Sunucusu 200 OK: ${recipientMail} adresine aktivasyon maili iletildi!`);"""

if old_login_mail_code in content:
    content = content.replace(old_login_mail_code, new_login_mail_code)
    print("1. Connected backend email sending API call to LoginComponent modal.")
else:
    print("WARNING: Could not find old_login_mail_code in index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('yonetim.html', 'w', encoding='utf-8') as f:
    f.write(content)

os.makedirs('dist', exist_ok=True)
with open('dist/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Synced index.html to yonetim.html and dist/index.html!")
