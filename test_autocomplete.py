import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        errors = []
        page.on("pageerror", lambda err: errors.append(err.message))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        print("Navigating...")
        await page.goto("http://localhost:8000/#/rezervasyon-olustur")
        
        print("Waiting for page load...")
        await page.wait_for_timeout(2000)
        
        print("Typing 532 into phone input...")
        # Since this is a React app, it might be easiest to find input by placeholder or just find any input where label is 'Telefon' or similar
        input_locator = page.locator("input[type='tel']")
        if await input_locator.count() > 0:
            await input_locator.first.fill("532")
        else:
            # Let's try locating any input with name phone or placeholder phone
            try:
                await page.locator("input[name='phone']").fill("532")
            except:
                print("Could not find input by name='phone', trying placeholder")
                try:
                    await page.locator("input[placeholder*='5']").fill("532")
                except:
                    print("Could not find placeholder, trying label")
                    await page.locator("text=Telefon >> xpath=../..//input").first.fill("532")
        
        print("Waiting for autocomplete...")
        await page.wait_for_timeout(2000)
        
        autocomplete_box = page.locator("text=Kayıtlı Müşteri Eşleşti")
        if await autocomplete_box.count() > 0:
            print("Autocomplete box found!")
            # Get the parent element or the box itself to check z-index
            box_html = await autocomplete_box.first.evaluate("el => el.parentElement.outerHTML")
            z_index = await autocomplete_box.first.evaluate("el => window.getComputedStyle(el.parentElement).zIndex")
            print(f"Z-index of autocomplete box parent: {z_index}")
            
            print("Clicking autocomplete box...")
            await autocomplete_box.first.click()
            await page.wait_for_timeout(2000)
            
            # Check for toast success message
            toast = page.locator("text=Kayıtlı Müşteri Olarak Seçildi ve Aktarıldı")
            if await toast.count() > 0:
                print("Success toast found!")
            else:
                print("Success toast NOT found.")
                # Maybe check full DOM for toast
                body_text = await page.evaluate("document.body.innerText")
                print("Body contains 'Aktarıldı':", 'Aktarıldı' in body_text)
        else:
            print("Autocomplete box not found.")
            # Print page body text to see what is there
            body_text = await page.evaluate("document.body.innerText")
            print("Body text snippet:", body_text[:500])
            
        print("JS Errors encountered:")
        for e in errors:
            print(" -", e)
            
        await browser.close()

asyncio.run(run())
