import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        await page.goto("http://localhost:8000")
        
        print("Checking Sub-Header Bar...")
        sub_header = page.locator("text=Hızlı Rol Değiştir")
        if await sub_header.count() > 0:
            print("Found 'Hızlı Rol Değiştir' text.")
        else:
            print("Could NOT find 'Hızlı Rol Değiştir' text.")
            
        badge = page.locator("text=Canlı Sistem")
        if await badge.count() > 0:
            print("Found 'Canlı Sistem' badge.")
        else:
            print("Could NOT find 'Canlı Sistem' badge.")

        # 2. Click badge and check modal
        if await badge.count() > 0:
            await badge.first.click()
            await page.wait_for_timeout(1000)
            modal = page.locator("text=Sistem Sürüm Geçmişi")
            if await modal.count() > 0:
                print("Modal 'Sistem Sürüm Geçmişi' opened smoothly.")
                
                v_text = await page.locator("body").inner_text()
                if "v0.0.1" in v_text and "v1.3.0" in v_text:
                    print("Found v0.0.1 to v1.3.0 versions.")
                else:
                    print("Could not find version text.")
                    
                close_btn = page.locator("button", has_text="Anlaşıldı")
                if await close_btn.count() == 0:
                    close_btn = page.locator("button:has-text('✕')")
                    
                if await close_btn.count() > 0:
                    await close_btn.first.click()
                    await page.wait_for_timeout(500)
                    if not await modal.is_visible():
                        print("Modal closed smoothly.")
                    else:
                        print("Modal did NOT close.")
                else:
                    print("Could not find close button for modal.")
            else:
                print("Modal did not open.")
                
        # 3. Check Vertical/Horizontal menus
        # You can add logic for menus here if needed
        
        await browser.close()

asyncio.run(main())
