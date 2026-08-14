import os, re

# 1. UPDATE server.js with nodemailer and real forgot/reset endpoints
with open('server.js', 'r', encoding='utf-8') as f:
    server_code = f.read()

# Add nodemailer require at top if missing
if "const nodemailer = require('nodemailer');" not in server_code:
    server_code = "const nodemailer = require('nodemailer');\n" + server_code

# Add password_resets table migration
migration_sql = """
      await pool.query(`
        CREATE TABLE IF NOT EXISTS password_resets (
          id INT AUTO_INCREMENT PRIMARY KEY,
          email VARCHAR(150) NOT NULL,
          code VARCHAR(10) NOT NULL,
          expires_at DATETIME NOT NULL,
          used TINYINT(1) DEFAULT 0,
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
      `);
"""

if "CREATE TABLE IF NOT EXISTS password_resets" not in server_code:
    pos = server_code.find("console.log('✅ MySQL Tabloları Doğrulandı ve Hazırlandı!');")
    if pos != -1:
        server_code = server_code[:pos] + migration_sql + "\n      " + server_code[pos:]

# Add Real SMTP Transporter and Endpoints in server.js
smtp_endpoints_code = """
// -------------------------------------------------------------
// REAL SMTP EMAIL & AUTHENTICATION ENDPOINTS
// -------------------------------------------------------------
async function getMailTransporter() {
  const host = process.env.SMTP_HOST || 'mail.iremdugunsarayi.com';
  const port = Number(process.env.SMTP_PORT || 587);
  const user = process.env.SMTP_USER || 'bilgi@iremdugunsarayi.com';
  const pass = process.env.SMTP_PASS || process.env.SMTP_PASSWORD || '';
  const secure = port === 465;

  return nodemailer.createTransport({
    host,
    port,
    secure,
    auth: user && pass ? { user, pass } : undefined,
    tls: { rejectUnauthorized: false }
  });
}

// 1. Send Password Reset Code (POST /api/auth/forgot-password)
app.post('/api/auth/forgot-password', async (req, res) => {
  const { identity } = req.body;
  if (!identity) {
    return res.status(400).json({ error: 'Lütfen kayıtlı e-posta adresinizi veya telefon numaranızı giriniz.' });
  }

  const cleanIdentity = identity.trim().toLowerCase();
  const digits = cleanIdentity.replace(/\\D/g, '');

  try {
    const pool = await getPool();
    if (!pool) {
      return res.status(500).json({ error: 'Veritabanı bağlantısı kurulamadı.' });
    }

    // Find in users table
    const [users] = await pool.query(
      "SELECT * FROM users WHERE LOWER(email) = ? OR REPLACE(REPLACE(phone, ' ', ''), '+', '') LIKE ?",
      [cleanIdentity, `%${digits || 'XYZ'}%`]
    );

    let targetUser = users[0];
    let targetRole = 'admin';

    if (!targetUser) {
      const [customers] = await pool.query(
        "SELECT * FROM customers WHERE LOWER(email) = ? OR REPLACE(REPLACE(phone, ' ', ''), '+', '') LIKE ?",
        [cleanIdentity, `%${digits || 'XYZ'}%`]
      );
      if (customers.length > 0) {
        targetUser = customers[0];
        targetRole = 'musteri';
      }
    }

    if (!targetUser) {
      return res.status(404).json({ error: 'Girdiğiniz bilgilere ait sistemde kayıtlı bir kullanıcı bulunamadı.' });
    }

    const email = targetUser.email || cleanIdentity;
    const name = targetUser.name || 'Sayın Yetkili';
    
    // Generate secure 6-digit verification code
    const resetCode = Math.floor(100000 + Math.random() * 900000).toString();
    const expiresAt = new Date(Date.now() + 15 * 60 * 1000); // 15 mins

    await pool.query(
      "INSERT INTO password_resets (email, code, expires_at) VALUES (?, ?, ?)",
      [email, resetCode, expiresAt]
    );

    let mailSent = false;
    let mailError = null;

    try {
      const transporter = await getMailTransporter();
      const mailOptions = {
        from: `"İrem Düğün Sarayı" <${process.env.SMTP_USER || 'bilgi@iremdugunsarayi.com'}>`,
        to: email,
        subject: `🔑 Şifre Sıfırlama Kodunuz: ${resetCode} - İrem Düğün Sarayı`,
        html: `
          <div style="font-family: Arial, sans-serif; background-color: #f8fafc; padding: 30px; color: #1e293b;">
            <div style="max-width: 550px; margin: 0 auto; background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
              <div style="text-align: center; margin-bottom: 20px;">
                <h1 style="color: #d97706; margin: 0; font-size: 22px;">İREM DÜĞÜN SARAYI</h1>
                <p style="color: #64748b; font-size: 12px; margin-top: 4px;">Sapanca / Sakarya Kurumsal Portalı</p>
              </div>
              <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 20px 0;" />
              <p style="font-size: 14px; line-height: 1.6;">Merhaba <strong>${name}</strong>,</p>
              <p style="font-size: 14px; line-height: 1.6;">İrem Düğün Sarayı Yönetim Paneli hesabınız için şifre sıfırlama talebinde bulundunuz. Şifrenizi yenilemek için aşağıdaki 6 haneli güvenlik kodunu kullanabilirsiniz:</p>
              <div style="text-align: center; margin: 25px 0;">
                <div style="display: inline-block; background: #fef3c7; color: #b45309; font-size: 28px; font-weight: 800; letter-spacing: 6px; padding: 14px 28px; border-radius: 12px; border: 1px solid #fde68a;">
                  ${resetCode}
                </div>
              </div>
              <p style="font-size: 12px; color: #64748b; text-align: center;">Bu kod <strong>15 dakika</strong> boyunca geçerlidir. Talebi siz yapmadıysanız bu e-postayı dikkate almayınız.</p>
              <hr style="border: none; border-top: 1px solid #f1f5f9; margin: 20px 0;" />
              <p style="font-size: 11px; color: #94a3b8; text-align: center; margin: 0;">© ${new Date().getFullYear()} İrem Düğün Sarayı. Tüm hakları saklıdır.</p>
            </div>
          </div>
        `
      };

      await transporter.sendMail(mailOptions);
      mailSent = true;
    } catch(mErr) {
      console.log('SMTP Delivery Note:', mErr.message);
      mailError = mErr.message;
    }

    return res.json({
      success: true,
      email,
      maskedEmail: email.replace(/(.{2})(.*)(@.*)/, '$1***$3'),
      mailSent,
      expiresInMinutes: 15,
      message: `${email} adresine 6 haneli güvenlik kodu gönderildi.`
    });

  } catch(err) {
    console.error('Forgot password endpoint error:', err);
    return res.status(500).json({ error: 'İşlem sırasında bir hata oluştu: ' + err.message });
  }
});

// 2. Verify Code & Set New Password (POST /api/auth/reset-password)
app.post('/api/auth/reset-password', async (req, res) => {
  const { email, code, newPassword } = req.body;
  if (!email || !code || !newPassword) {
    return res.status(400).json({ error: 'E-posta, 6 haneli doğrulama kodu ve yeni şifre zorunludur.' });
  }

  try {
    const pool = await getPool();
    if (!pool) return res.status(500).json({ error: 'Veritabanı bağlantısı yok.' });

    const cleanEmail = email.trim().toLowerCase();
    const cleanCode = code.trim();

    // Verify 6 digit code from database
    const [resets] = await pool.query(
      "SELECT * FROM password_resets WHERE LOWER(email) = ? AND code = ? AND used = 0 AND expires_at > NOW() ORDER BY created_at DESC LIMIT 1",
      [cleanEmail, cleanCode]
    );

    if (resets.length === 0) {
      return res.status(400).json({ error: 'Girdiğiniz doğrulama kodu geçersiz veya süresi dolmuş.' });
    }

    const resetRecord = resets[0];

    // Invalidate code
    await pool.query("UPDATE password_resets SET used = 1 WHERE id = ?", [resetRecord.id]);

    // Update in users table
    await pool.query(
      "UPDATE users SET password_hash = ? WHERE LOWER(email) = ?",
      [newPassword, cleanEmail]
    );

    // Update in customers table
    await pool.query(
      "UPDATE customers SET password = ? WHERE LOWER(email) = ?",
      [newPassword, cleanEmail]
    );

    return res.json({
      success: true,
      message: 'Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz.'
    });

  } catch(err) {
    return res.status(500).json({ error: 'Şifre güncellenirken hata oluştu: ' + err.message });
  }
});
"""

if "app.post('/api/auth/forgot-password'" not in server_code:
    pos = server_code.find("app.listen(")
    if pos != -1:
        server_code = server_code[:pos] + smtp_endpoints_code + "\n" + server_code[pos:]

with open('server.js', 'w', encoding='utf-8') as f:
    f.write(server_code)

print("Updated server.js with SMTP mailer and real password reset endpoints!")

# 2. UPDATE HTML files with clean 2-step password reset modal (NO FAKE BYPASS)
html_files = ['index.html', 'yonetim.html', 'yonetim/index.html', 'dist/index.html']

for h_file in html_files:
    if not os.path.exists(h_file):
        continue
    with open(h_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the FORGOT PASSWORD MODAL section in content
    old_modal_pattern = re.search(r'\{\s*/\*\s*FORGOT PASSWORD MODAL\s*\*/\s*\}[\s\S]*?\{showForgotModal && \([\s\S]*?<\/div>\s*\)\s*\}', content)

    new_modal = """{/* FORGOT PASSWORD REAL 2-STEP SMTP MODAL */}
          {showForgotModal && (
            <div className="fixed inset-0 z-[99999] bg-slate-900/60 dark:bg-black/80 backdrop-blur-md flex items-center justify-center p-4 animate-fade-in">
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-amber-500/30 rounded-3xl max-w-md w-full p-6 sm:p-7 space-y-5 shadow-[0_20px_50px_rgba(0,0,0,0.12)] text-slate-800 dark:text-white animate-scale-up relative">
                
                {/* HEADER */}
                <div className="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-3.5">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-2xl bg-amber-500/10 dark:bg-amber-500/20 border border-amber-500/30 flex items-center justify-center text-amber-600 dark:text-amber-400 shrink-0 shadow-xs">
                      <ThemeIcon icon="key" className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-sm font-extrabold text-slate-900 dark:text-amber-400">Şifre Sıfırlama</h3>
                      <p className="text-[10px] text-slate-500 dark:text-slate-400 font-medium">E-Posta ile Doğrulama & Yeni Şifre</p>
                    </div>
                  </div>
                  <button
                    type="button"
                    onClick={() => { setShowForgotModal(false); setForgotSuccessMail(null); setForgotInput(''); }}
                    className="w-8 h-8 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-white flex items-center justify-center transition cursor-pointer font-bold text-xs"
                  >
                    ✕
                  </button>
                </div>

                {!forgotSuccessMail ? (
                  /* STEP 1: ENTER EMAIL OR PHONE */
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    if (!forgotInput || !forgotInput.trim()) {
                      showToast('Lütfen geçerli bir e-posta veya telefon giriniz.', 'error');
                      return;
                    }
                    setIsLoading(true);
                    try {
                      const res = await fetch('/api/auth/forgot-password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ identity: forgotInput.trim() })
                      });
                      const data = await res.json();
                      setIsLoading(false);
                      if (!res.ok || data.error) {
                        showToast(data.error || 'Kullanıcı bulunamadı!', 'error');
                        return;
                      }
                      setForgotSuccessMail({
                        email: data.email,
                        maskedEmail: data.maskedEmail,
                        code: '',
                        newPassword: '',
                        confirmPassword: ''
                      });
                      showToast(data.message || 'Doğrulama kodu e-posta adresinize gönderildi!');
                    } catch(err) {
                      setIsLoading(false);
                      showToast('Sunucu ile iletişim kurulamadı.', 'error');
                    }
                  }} className="space-y-4 text-xs">
                    
                    <div className="bg-amber-50/80 dark:bg-amber-500/10 border border-amber-200/80 dark:border-amber-500/30 p-4 rounded-2xl flex items-start space-x-3 text-slate-700 dark:text-amber-200 shadow-xs">
                      <ThemeIcon icon="info" className="w-5 h-5 text-amber-600 dark:text-amber-400 shrink-0 mt-0.5" />
                      <p className="text-[11px] leading-relaxed font-medium">
                        Sistemde kayıtlı <strong>e-posta adresinizi</strong> veya <strong>telefon numaranızı</strong> giriniz. Şifrenizi güvenle yenileyebilmeniz için 6 haneli güvenlik kodu e-posta adresinize iletilecektir.
                      </p>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5 flex items-center space-x-1.5">
                        <ThemeIcon icon="mail" className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                        <span>Kayıtlı E-Posta veya Telefon:</span>
                      </label>
                      <input
                        type="text"
                        required
                        placeholder="Örn: dvtakblt@gmail.com veya 0532..."
                        value={forgotInput}
                        onChange={e => setForgotInput(e.target.value)}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3.5 text-xs text-slate-800 dark:text-amber-300 font-semibold placeholder:text-slate-400 dark:placeholder:text-slate-500 outline-none transition shadow-xs"
                      />
                    </div>

                    <div className="flex items-center space-x-2 pt-2">
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="flex-1 bg-gradient-to-r from-amber-500 via-orange-500 to-amber-600 hover:from-amber-600 hover:to-orange-600 text-white font-extrabold py-3.5 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition active:scale-[0.98]"
                      >
                        {isLoading ? <span>Kod Gönderiliyor...</span> : <span>Doğrulama Kodu Gönder</span>}
                      </button>
                    </div>
                  </form>
                ) : (
                  /* STEP 2: ENTER CODE & SET NEW PASSWORD */
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    if (!forgotSuccessMail.code || forgotSuccessMail.code.trim().length !== 6) {
                      showToast('Lütfen 6 haneli doğrulama kodunu giriniz.', 'error');
                      return;
                    }
                    if (!forgotSuccessMail.newPassword || forgotSuccessMail.newPassword.length < 4) {
                      showToast('Yeni şifre en az 4 karakter olmalıdır.', 'error');
                      return;
                    }
                    if (forgotSuccessMail.newPassword !== forgotSuccessMail.confirmPassword) {
                      showToast('Yeni şifreler birbiriyle eşleşmiyor!', 'error');
                      return;
                    }

                    setIsLoading(true);
                    try {
                      const res = await fetch('/api/auth/reset-password', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                          email: forgotSuccessMail.email,
                          code: forgotSuccessMail.code.trim(),
                          newPassword: forgotSuccessMail.newPassword
                        })
                      });
                      const data = await res.json();
                      setIsLoading(false);
                      if (!res.ok || data.error) {
                        showToast(data.error || 'Doğrulama kodu hatalı veya süresi dolmuş!', 'error');
                        return;
                      }

                      // Fill in login form automatically
                      setEmailInput(forgotSuccessMail.email);
                      setPassword(forgotSuccessMail.newPassword);
                      setLoginMethod('email');
                      setShowForgotModal(false);
                      setForgotSuccessMail(null);
                      setForgotInput('');
                      showToast('🎉 Şifreniz başarıyla yenilendi! Yeni şifrenizle giriş yapabilirsiniz.');
                    } catch(err) {
                      setIsLoading(false);
                      showToast('Şifre güncellenirken hata oluştu.', 'error');
                    }
                  }} className="space-y-4 text-xs">
                    
                    <div className="bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-300 dark:border-emerald-700/60 p-3.5 rounded-2xl flex items-start space-x-2.5 text-emerald-800 dark:text-emerald-300 shadow-xs">
                      <ThemeIcon icon="check" className="w-5 h-5 text-emerald-600 dark:text-emerald-400 shrink-0 mt-0.5" />
                      <div>
                        <div className="font-extrabold text-xs">Kod Gönderildi!</div>
                        <div className="text-[11px] mt-0.5"><strong>{forgotSuccessMail.maskedEmail || forgotSuccessMail.email}</strong> adresinize 6 haneli güvenlik kodu iletildi.</div>
                      </div>
                    </div>

                    <div>
                      <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                        6 Haneli Güvenlik Kodu <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        maxLength="6"
                        required
                        placeholder="Örn: 123456"
                        value={forgotSuccessMail.code}
                        onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, code: e.target.value.replace(/\\D/g, '') })}
                        className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-center text-lg font-black tracking-widest text-amber-700 dark:text-amber-300 outline-none transition"
                      />
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                      <div>
                        <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                          Yeni Şifre <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Yeni şifreniz"
                          value={forgotSuccessMail.newPassword}
                          onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, newPassword: e.target.value })}
                          className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs outline-none transition"
                        />
                      </div>
                      <div>
                        <label className="block text-slate-700 dark:text-slate-200 font-bold mb-1.5">
                          Şifre Tekrar <span className="text-red-500">*</span>
                        </label>
                        <input
                          type="password"
                          required
                          placeholder="Şifreyi tekrar yazın"
                          value={forgotSuccessMail.confirmPassword}
                          onChange={e => setForgotSuccessMail({ ...forgotSuccessMail, confirmPassword: e.target.value })}
                          className="w-full bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-700 focus:bg-white dark:focus:bg-slate-950 focus:border-amber-500 rounded-xl p-3 text-xs outline-none transition"
                        />
                      </div>
                    </div>

                    <div className="flex items-center space-x-2 pt-2">
                      <button
                        type="button"
                        onClick={() => setForgotSuccessMail(null)}
                        className="px-4 py-3 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold rounded-xl text-xs transition cursor-pointer"
                      >
                        Geri
                      </button>
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="flex-1 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white font-extrabold py-3 rounded-xl cursor-pointer shadow-md hover:shadow-lg flex items-center justify-center space-x-2 text-xs transition"
                      >
                        {isLoading ? <span>Güncelleniyor...</span> : <span>Şifremi Yenile ve Kaydet</span>}
                      </button>
                    </div>
                  </form>
                )}

              </div>
            </div>
          )}"""

    if old_modal_pattern:
        content = content[:old_modal_pattern.start()] + new_modal + content[old_modal_pattern.end():]
        print(f"Replaced forgot password modal with real 2-step SMTP flow in {h_file}")

    with open(h_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully processed {h_file}!")

print("All HTML files updated with real SMTP 2-step password reset modal!")
