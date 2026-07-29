import asyncio
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to create reservation page
        await page.goto("http://localhost:8000/#/rezervasyon-olustur")
        await page.wait_for_timeout(1000)
        
        # Click "Rezervasyonu Oluştur" without filling customer info
        submit_button = page.locator("button:has-text('Rezervasyonu Oluştur')").first
        await submit_button.click()
        await page.wait_for_timeout(500)
        
        # Check if 3-second floating popup is visible
        popup = page.locator("text=⚠️ LÜTFEN ZORUNLU ALANLARI DOLDURUNUZ")
        popup_visible_at_start = await popup.is_visible()
        print(f"[TEST 1] Floating popup visible right after submit: {popup_visible_at_start}")
        
        # Check inline required field error message under Customer Name
        inline_error = page.locator("text=⚠️ Doldurulması zorunludur.")
        inline_visible = await inline_error.count() > 0
        print(f"[TEST 2] Inline 'Bu alanın doldurulması zorunludur' warnings visible: {inline_visible} (count: {await inline_error.count()})")
        
        # Check red input glow border styling
        name_input = page.locator("#new-cust-name-input")
        name_class = await name_input.get_attribute("class")
        print(f"[TEST 3] Name input red error class active: {'border-red-500' in name_class}")
        
        # Wait 3.5 seconds to verify popup auto-dismisses
        await page.wait_for_timeout(3500)
        popup_visible_after_delay = await popup.is_visible()
        print(f"[TEST 4] Floating popup auto-dismissed after 3 seconds: {not popup_visible_after_delay}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_test())
