# İrem Düğün Sarayı & Organizasyon Platformu - Design System & UI/UX Memory

## 📐 Tasarım Sistemi Mimarisi & Felsefesi (Design System Architecture)

İrem Düğün Sarayı platformu, dinamik tema motoru, mikro-interaksiyonlar, GPU hızlandırmalı frosted-glass çeperleri ve role dayalı arayüz kişiselleştirmesi sunan kurumsal bir UI/UX mimarisine sahiptir. Platform 6 temel kurumsal tema ve "Nordic Clarity & Scandinavian Minimal" özel temasını destekler.

---

## 🎨 Tema Tanımları & Renk/Geometri Paletleri (Theme Specs)

### 1. ❄️ Nordic Clarity & Scandinavian Minimal (`nordic-clarity`)
- **SIFIR EMOJİ DIRECTIVE**: Arayüzde, başlıklarda, aksiyon butonlarında ve menülerde **HİÇBİR EMOJİ KULLANILMAZ**. Sadece 1.75px stroke-width geometrik İskandinav SVG ikonları (`NordicSvgMap`) render edilir.
- **Font Hiyerarşisi**: Primary: `Inter`, Heading: `Plus Jakarta Sans`. Yüksek okunabilirlik, `tracking-widest uppercase` alt başlıklar.
- **Renk Paleti**:
  - Gece Mavisi (`#0F172A`)
  - Kutup Beyazı (`#F8FAFC`)
  - Buz Grisi (`#E2E8F0`)
  - İskandinav Gümüşü (`#94A3B8`)
- **Geometri**: `rounded-md` / `rounded-lg` (4px-8px minimalist kavisli köşeler).
- **Çeper Efekti**: `border: 1px solid #E2E8F0`, hafif buz mavisi gölge.

### 2. 👑 Classic Gold - Saray Altını (`gold` / `classic-gold`)
- **İkon / Emoji Seti**: 👑 🏰 ✏️ 👁️ 🗑️
- **Renk Paleti**: Sıcak Altın (`#D4AF37` / `#D97706`) & Siyah (`#0B0F19`).
- **Geometri**: `rounded-2xl` (16px yumuşak lüks kavisler).
- **Çeper Efekti**: Sıcak altın gradyan border ve ışıltılı gölgeler.

### 3. 🖤 Obsidian Gold - Derin Siyah & Altın (`obsidian-gold`)
- **İkon / Emoji Seti**: 🖤 🏛️ 🖊️ 🌟 💣
- **Renk Paleti**: Obsidyen Siyahı (`#090A0F` / `#18181B`) & Şampanya Altını (`#F59E0B`).
- **Geometri**: `rounded-none` (0px dik keskin köşeler).
- **Çeper Efekti**: Obsidyen siyahı ve 1px altın metalik çeper border (`border: 1px solid rgba(217, 119, 6, 0.8)`).

### 4. 🔷 Sapphire Clean - Saf Safir (`sapphire-clean`)
- **İkon / Emoji Seti**: 🔷 🏢 📝 🔍 ❌
- **Renk Paleti**: Safir Mavi (`#1E40AF` / `#1D4EDB`) & Kristal Beyaz (`#FFFFFF`).
- **Geometri**: `rounded-md` (4px neo-minimalist kavis).
- **Çeper Efekti**: Temiz safir mavisi çeper (`border: 1px solid rgba(37, 99, 235, 0.45)`).

### 5. 🩶 Platinum Silver - Platin Gümüş (`platinum-silver`)
- **İkon / Emoji Seti**: 🥈 🏛️ ⚙️ 🔍 🗑️
- **Renk Paleti**: Platin Gümüş (`#E2E8F0` / `#CBD5E1`) & Füme (`#334155` / `#475569`).
- **Geometri**: `rounded-sm` (2px micro-keskin köşeler).
- **Çeper Efekti**: Parlak metalik platin & gümüş yansıma çeperi (`border: 1px solid rgba(203, 213, 225, 0.8)`).

### 6. 🌿 Emerald Royal - Zümrüt Balo (`emerald-royal`)
- **İkon / Emoji Seti**: 🌿 🏡 ✍️ 👁️ 🍂
- **Renk Paleti**: Zümrüt Yeşili (`#065F46` / `#047857`) & Altın Vurgu (`#F59E0B`).
- **Geometri**: `rounded-none` (0px keskin zümrüt çeperler).
- **Çeper Efekti**: Orman yeşili ve zümrüt altını metalik çeper.

### 7. ⚡ Titanium Tech - Titanyum Gelecek (`titanium-tech`)
- **İkon / Emoji Seti**: ⚡ 🏬 🛠️ 📡 🚫
- **Renk Paleti**: Titanyum Grisi (`#1E293B` / `#6D28D9`) & Neon Mavi (`#38BDF8` / `#A78BFA`).
- **Geometri**: `rounded-md` (4px teknolojik kavisler).
- **Çeper Efekti**: Titanyum fırçalanmış metal ve neon siber mor çeper.

---

## 🛠️ İkon & Emoji Sarmalama Kuralları (Icon & Emoji Directive)

1. **Nordic Clarity Temasında**:
   - Tüm emoji ifadeleri gizlenir veya yerine 1.75px kontur kalınlığında `NordicSvgMap` bileşenleri render edilir.
   - Sivil mimari & minimal tasarım dili esastır.

2. **Diğer Temalarda**:
   - Temaya özel ikon/emoji seti kullanılır.
   - Aksiyon butonları (Düzenle, Gör, Sil, Ekle) temaya uygun ikon karakteri ile desteklenir.

---

## 🏛️ CSS & Geometri Katman Yapısı (CSS Layers)

```css
/* Nordic Clarity */
html[data-theme="nordic-clarity"], [data-theme="nordic-clarity"] {
  --color-gold: #0f172a;
  --color-gold-hover: #1e293b;
  --glass-bg: #ffffff;
  --glass-border: #e2e8f0;
}

/* Obsidian Gold */
html[data-theme="obsidian-gold"], [data-theme="obsidian-gold"] {
  --color-gold: #d97706;
  --glass-border: rgba(217, 119, 6, 0.8);
}
```

---

## 🚀 Ayarlar > Görünüm Sekmesi Entegrasyonu

`SettingsPage.jsx` içerisindeki Görünüm & Tema sekmesinde kullanıcı tüm temaları görsel olarak inceleyebilir, köşe keskinlik parametrelerini görebilir ve tek tıkla uygulamada anlık olarak değiştirebilir.
