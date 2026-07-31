import sys

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Upgrade getUrlKey inside MediaComponent to parse both #/medya/:key and ?key=:key
old_get_url_key = """  // Extract URL search param key (e.g. #/medya-yukle?key=MEDIA-8X92M1KP or #/medya-yukle?resId=RES-2026-001)
  const getUrlKey = () => {
    if (typeof window === 'undefined') return '';
    const hash = window.location.hash || '';
    const match = hash.match(/[?&](key|resId)=([A-Za-z0-9_-]+)/);
    return match ? match[2] : '';
  };"""

new_get_url_key = """  // Extract URL key from both path route (#/medya/MEDIA-8X92M1KP) and query param (?key=MEDIA-8X92M1KP)
  const getUrlKey = () => {
    if (typeof window === 'undefined') return '';
    const hash = window.location.hash || '';
    const pathMatch = hash.match(/^#\/(?:medya|m)\/([A-Za-z0-9_-]+)/);
    if (pathMatch) return pathMatch[1];
    const queryMatch = hash.match(/[?&](key|resId)=([A-Za-z0-9_-]+)/);
    return queryMatch ? queryMatch[2] : '';
  };"""

if old_get_url_key in html:
    html = html.replace(old_get_url_key, new_get_url_key)
    print("Upgraded getUrlKey to support path-style #/medya/:key routes!")

# 2. Upgrade isPublicGuestMode inside MediaComponent
old_media_guest_mode = """  // STRICT GUEST MODE: Active ONLY on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, []);"""

new_media_guest_mode = """  // STRICT GUEST MODE: Active on standalone guest links (#/medya/:key or ?mode=guest)
  const isPublicGuestMode = useMemo(() => {
    if (typeof window === 'undefined') return false;
    const hash = window.location.hash || '';
    return /^#\/(?:medya|m)\//.test(hash) || hash.includes('mode=guest');
  }, [selectedResKey]);"""

if old_media_guest_mode in html:
    html = html.replace(old_media_guest_mode, new_media_guest_mode)
    print("Updated isPublicGuestMode dependency!")

# 3. Clean up old promo card block if still present in MediaComponent return
old_promo_block_dup = """      {/* GUEST PROMOTION FOOTER BANNER (Visible ONLY in Public Guest Mode) */}
      {isPublicGuestMode && (
        <div className="glass-panel p-6 rounded-3xl border-2 border-amber-500/40 bg-gradient-to-br from-amber-500/10 via-slate-900 to-slate-950 text-white text-center space-y-4 shadow-xl mt-8">
          <div className="max-w-md mx-auto space-y-2">
            <h4 className="font-heading font-black text-lg text-amber-400">
              Kendi Düğün veya Nişanınız İçin Denemek İster Mısınız?
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed font-medium">
              Siz de kendi etkinliğinizde davetlilerinizin çektiği tüm fotoğraf ve videoları anında tek tıkla toplamak ister misiniz? İrem Düğün Sarayı Dijital Anı Albümü ile anılarınızı ölümsüzleştirin.
            </p>
          </div>

          <button
            type="button"
            onClick={() => {
              if (typeof window !== 'undefined') {
                window.location.href = 'tel:+905321112233';
              }
            }}
            className="px-6 py-3 gold-button text-slate-950 font-black text-xs rounded-xl shadow-lg hover:scale-105 transition inline-flex items-center space-x-2 cursor-pointer"
          >
            <ThemeIcon icon="phone" fallbackEmoji="" className="w-4 h-4 shrink-0" />
            <span>📞 Bilgi Al & İletişime Geç (+90 532 111 2233)</span>
          </button>
        </div>
      )}"""

if old_promo_block_dup in html:
    html = html.replace(old_promo_block_dup, "")
    print("Cleaned up old promo card block from MediaComponent!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html URL key parsing & guest view rendering successfully!")
