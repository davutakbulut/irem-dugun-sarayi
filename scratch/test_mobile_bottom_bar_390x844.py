import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def run_test():
    print("=== CANLI SİSTEM MOBİL (390x844px) ALT BAR VE DETAYLAR ÇEKMECESİ TESTİ ===", flush=True)

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)
    
    # 1. Physical Mobile Viewport 390x844px via CDP Emulation
    driver.execute_cdp_cmd('Emulation.setDeviceMetricsOverride', {
        'width': 390,
        'height': 844,
        'deviceScaleFactor': 3,
        'mobile': True
    })

    # 2. Load page
    driver.get('http://localhost:8000/#/rezervasyon-olustur')
    time.sleep(3)

    v_width = driver.execute_script("return window.innerWidth;")
    v_height = driver.execute_script("return window.innerHeight;")
    print(f"\n1. Viewport Ölçüleri: {v_width}x{v_height}px (Hedef: 390x844px)", flush=True)

    os.makedirs("scratch", exist_ok=True)

    # 3. Sayfa Kaydırılmadan Önceki Alt Bar Kontrolü
    bar_check_script = """
      const matchingDivs = Array.from(document.querySelectorAll('div')).filter(el => {
        return el.innerText && el.innerText.includes('Detaylar') && el.innerText.includes('Net Bakiye');
      });
      if (matchingDivs.length === 0) return { found: false };

      const innerDiv = matchingDivs[matchingDivs.length - 1];
      const fixedBarContainer = innerDiv.closest('.fixed') || innerDiv;
      const rect = fixedBarContainer.getBoundingClientRect();
      const style = window.getComputedStyle(fixedBarContainer);

      return {
        found: true,
        text: fixedBarContainer.innerText.replace(/\\s+/g, ' ').trim(),
        position: style.position,
        bottom: style.bottom,
        left: style.left,
        right: style.right,
        zIndex: style.zIndex,
        rect: {
          top: Math.round(rect.top),
          bottom: Math.round(rect.bottom),
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          height: Math.round(rect.height),
          width: Math.round(rect.width)
        },
        windowHeight: window.innerHeight,
        windowScrollY: window.scrollY
      };
    """

    initial_bar = driver.execute_script(bar_check_script)
    print("\n2. Sayfa Kaydırılmadan Önceki Alt Bar Durumu:", flush=True)
    print(f"   - Alt Bar Ekranda Bulundu Mu?: {'✅ EVET' if initial_bar and initial_bar.get('found') else '❌ HAYIR'}", flush=True)
    if initial_bar and initial_bar.get('found'):
      print(f"   - İçerik Metni: '{initial_bar['text']}'", flush=True)
      print(f"   - CSS Position: '{initial_bar['position']}' (Beklenen: 'fixed')", flush=True)
      print(f"   - CSS Bottom: '{initial_bar['bottom']}' (Beklenen: '0px')", flush=True)
      print(f"   - z-Index Katmanı: {initial_bar['zIndex']}", flush=True)
      print(f"   - Fiziksel Ekran En Altına Sabitlik: Bar Alt Sınırı ({initial_bar['rect']['bottom']}px) == Ekran Yüksekliği ({initial_bar['windowHeight']}px)", flush=True)

    driver.save_screenshot("scratch/mobile_390x844_initial.png")

    # 4. Sayfayı 1200px Aşağı Kaydır
    driver.execute_script("window.scrollTo(0, 1200);")
    time.sleep(1)

    scrolled_bar = driver.execute_script(bar_check_script)
    print("\n3. Sayfa 1200px Aşağı Kaydırıldıktan Sonraki Alt Bar Durumu:", flush=True)
    print(f"   - Sayfa Scroll Miktarı (scrollY): {scrolled_bar.get('windowScrollY') if scrolled_bar else 0}px", flush=True)
    print(f"   - Alt Bar Hâlâ Ekranda Görünüyor Mu?: {'✅ EVET' if scrolled_bar and scrolled_bar.get('found') else '❌ HAYIR'}", flush=True)
    if scrolled_bar and scrolled_bar.get('found'):
      print(f"   - CSS Position: '{scrolled_bar['position']}' ({'✅ FIXED' if scrolled_bar['position'] == 'fixed' else '❌ FARKLI'})", flush=True)
      print(f"   - CSS Bottom: '{scrolled_bar['bottom']}' ({'✅ 0px' if scrolled_bar['bottom'] == '0px' else '❌ FARKLI'})", flush=True)
      is_fixed_bottom = abs(scrolled_bar['rect']['bottom'] - scrolled_bar['windowHeight']) <= 3
      print(f"   - Fiziksel Telefon Ekranının En Altında Sabit Kaldı Mı?: {'✅ EVET (fixed bottom-0)' if is_fixed_bottom else '❌ SABİT DEĞİL'}", flush=True)

    driver.save_screenshot("scratch/mobile_390x844_scrolled.png")

    # 5. [ ▲ Detaylar ] / Net Bakiye Butonuna Tıklanılması (React Synthetic MouseEvent dispatch)
    print("\n4. '[ ▲ Detaylar ]' / Net Bakiye Butonuna Tıklama Testi:", flush=True)
    click_script = """
      const clickEl = document.querySelector('div[title="Detaylı Canlı Hesaplamayı Aç"]') || Array.from(document.querySelectorAll('span')).find(e => e.innerText && e.innerText.includes('▲ Detaylar'))?.closest('.cursor-pointer');
      if (!clickEl) return { clicked: false };
      
      const evt = new MouseEvent('click', { bubbles: true, cancelable: true, view: window });
      clickEl.dispatchEvent(evt);
      return { clicked: true, text: clickEl.innerText.replace(/\\s+/g, ' ').trim() };
    """
    click_res = driver.execute_script(click_script)
    print(f"   - Detaylar Butonuna Tıklandı Mı?: {'✅ EVET' if click_res and click_res.get('clicked') else '❌ HAYIR'}", flush=True)
    time.sleep(1.5)

    # 6. Döküm Çekmecesinin (Slide-Up Sheet) Aşağıdan Yukarıya Bağımsız Açıldığını Doğrulama
    drawer_script = """
      const drawerHeader = Array.from(document.querySelectorAll('h3')).find(el => {
        return el.innerText && el.innerText.includes('Canlı Hesaplama & Sözleşme Detayı');
      });
      if (!drawerHeader) return { open: false };

      const drawerOverlay = drawerHeader.closest('.fixed');
      if (!drawerOverlay) return { open: false };

      const sheet = drawerHeader.closest('.bg-white, .dark\\\\:bg-slate-900') || drawerHeader.parentElement;
      const sheetRect = sheet ? sheet.getBoundingClientRect() : null;
      const style = window.getComputedStyle(drawerOverlay);

      return {
        open: true,
        headerText: drawerHeader.innerText.trim(),
        overlayPosition: style.position,
        overlayZIndex: style.zIndex,
        sheetRect: sheetRect ? {
          top: Math.round(sheetRect.top),
          bottom: Math.round(sheetRect.bottom),
          height: Math.round(sheetRect.height),
          width: Math.round(sheetRect.width)
        } : null,
        windowHeight: window.innerHeight
      };
    """

    drawer_info = driver.execute_script(drawer_script)
    print("\n5. Açılan Döküm Çekmecesi (Slide-Up Sheet) Doğrulaması:", flush=True)
    print(f"   - Döküm Çekmecesi Açıldı Mı?: {'✅ EVET' if drawer_info and drawer_info.get('open') else '❌ HAYIR'}", flush=True)
    if drawer_info and drawer_info.get('open'):
      print(f"   - Çekmece Başlığı: '{drawer_info['headerText']}'", flush=True)
      print(f"   - Katman (Overlay) CSS Position: '{drawer_info['overlayPosition']}' (z-index: {drawer_info['overlayZIndex']})", flush=True)
      if drawer_info['sheetRect']:
        is_sheet_bottom = abs(drawer_info['sheetRect']['bottom'] - drawer_info['windowHeight']) <= 10
        print(f"   - Çekmece Yüksekliği: {drawer_info['sheetRect']['height']}px", flush=True)
        print(f"   - Çekmece Ekranın En Altına Hizanıp Aşağıdan Yukarıya Bağımsız Açıldı Mı?: {'✅ EVET (Aşağıdan Yukarı Bağımsız Açılan Sheet)' if is_sheet_bottom else '⚠️ Farklı'}", flush=True)

    driver.save_screenshot("scratch/mobile_390x844_drawer_open.png")

    # 7. Çekmeceyi Kapatma (✕) Testi
    print("\n6. Çekmece Kapatma (✕) Testi:", flush=True)
    close_script = """
      const closeBtn = document.querySelector('div.fixed.inset-0 button') || Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === '✕' && b.className.includes('rounded-full'));
      if (!closeBtn) return { closed: false };
      const evt = new MouseEvent('click', { bubbles: true, cancelable: true, view: window });
      closeBtn.dispatchEvent(evt);
      return { closed: true };
    """
    close_res = driver.execute_script(close_script)
    time.sleep(1)
    drawer_after_close = driver.execute_script(drawer_script)
    print(f"   - Kapatma Butonuna (✕) Tıklandı Mı?: {'✅ EVET' if close_res and close_res.get('closed') else '❌ HAYIR'}", flush=True)
    print(f"   - Çekmece Başarıyla Kapandı Mı?: {'✅ EVET (Kullanıcı Ekranından Kayboldu)' if not (drawer_after_close and drawer_after_close.get('open')) else '❌ HÂLÂ AÇIK'}", flush=True)

    driver.save_screenshot("scratch/mobile_390x844_drawer_closed.png")

    driver.quit()

    is_bar_fixed = bool(
        initial_bar and initial_bar.get('found') and
        initial_bar.get('position') == 'fixed' and
        initial_bar.get('bottom') == '0px' and
        scrolled_bar and scrolled_bar.get('found') and
        scrolled_bar.get('position') == 'fixed' and
        scrolled_bar.get('bottom') == '0px' and
        abs(scrolled_bar['rect']['bottom'] - scrolled_bar['windowHeight']) <= 3
    )

    is_drawer_ok = bool(
        drawer_info and drawer_info.get('open') and
        not (drawer_after_close and drawer_after_close.get('open'))
    )

    overall_passed = is_bar_fixed and is_drawer_ok

    summary = {
        "viewport": f"{v_width}x{v_height}px",
        "url": "http://localhost:8000/#/rezervasyon-olustur",
        "scrolled_scrollY_px": scrolled_bar.get('windowScrollY') if scrolled_bar else 0,
        "bottom_bar_fixed_bottom_0": is_bar_fixed,
        "drawer_slide_up_functional": is_drawer_ok,
        "overall_status": "PASSED" if overall_passed else "FAILED"
    }

    print("\n=======================================================", flush=True)
    print(f"TEST GENEL SONUCU: {'🎉 BAŞARILI (PASSED)' if overall_passed else '❌ BAŞARISIZ (FAILED)'}", flush=True)
    print(json.dumps(summary, indent=2, ensure_ascii=False), flush=True)
    print("=======================================================\n", flush=True)
    return summary

if __name__ == "__main__":
    run_test()
