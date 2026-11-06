"""
Google Maps Leads Scraper - Fixed v2 - extracts name/phone correctly
"""
from playwright.sync_api import sync_playwright
from .utils import log
from .verifier import clean_business
import time
import re

class GMapsScraper:
    def __init__(self, headless=True):
        self.headless = headless

    def scrape(self, search_query: str, max_results=50) -> list:
        leads = []
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=self.headless,
                args=['--disable-blink-features=AutomationControlled']
            )
            context = browser.new_context(
                viewport={'width': 1280, 'height': 900},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            log(f"Searching Google Maps: {search_query}")
            
            try:
                page.goto(f"https://www.google.com/maps/search/{search_query}/", timeout=60000)
                page.wait_for_timeout(4000)

                for cookie_sel in ['button:has-text("Accept all")', 'button:has-text("Accetta tutto")', '#L2AGLb']:
                    try:
                        if page.locator(cookie_sel).first.is_visible(timeout=2000):
                            page.locator(cookie_sel).first.click()
                            log(f"Clicked cookie: {cookie_sel}")
                            page.wait_for_timeout(2000)
                            break
                    except:
                        pass

                try:
                    page.wait_for_selector('div[role="feed"]', timeout=15000)
                except:
                    pass

                # Scroll
                feed_selector = 'div[role="feed"]'
                for i in range(25):
                    try:
                        page.evaluate(f"""() => {{ const f=document.querySelector('{feed_selector}'); if(f) f.scrollBy(0,2500); }}""")
                    except:
                        page.mouse.wheel(0, 3000)
                    page.wait_for_timeout(1500)
                    count = page.evaluate("""() => document.querySelectorAll('div[role="feed"] > div > div[jsaction]').length""")
                    log(f"Scroll {i+1}: ~{count} in DOM")
                    if count >= max_results + 10:  # +10 for header ads
                        break

                # Get cards - SKIP first 2 which are ads/search header
                cards = page.locator('div[role="feed"] > div > div[jsaction] > a.hfpxzc').all()
                if len(cards) < 5:
                    cards = page.locator('div[role="feed"] div.Nv2PK a.hfpxzc').all()
                
                log(f"Found {len(cards)} cards (using a.hfpxzc)")
                # Filter out non-business
                valid_cards = []
                for c in cards:
                    try:
                        href = c.get_attribute('href') or ""
                        if '/maps/place/' in href:
                            valid_cards.append(c)
                    except:
                        pass
                cards = valid_cards
                log(f"After filter place/: {len(cards)} valid")

                for idx, card in enumerate(cards[:max_results]):
                    try:
                        log(f"Processing {idx+1}/{min(len(cards), max_results)}")
                        card.click(timeout=5000)
                        page.wait_for_timeout(4000)

                        # Wait for details panel
                        try:
                            page.wait_for_selector('h1.DUwDvf', timeout=5000)
                        except:
                            page.wait_for_timeout(2000)

                        name = "N/A"
                        try:
                            h1 = page.locator('h1.DUwDvf').first
                            if h1.is_visible(timeout=2000):
                                name = h1.inner_text().strip()
                        except:
                            pass

                        # Skip if it's still search results page
                        if name == "Risultati" or name == "Results" or name == "N/A" or len(name) < 2:
                            log(f" -> Skip (name={name}) - not a business page")
                            continue

                        address = ""
                        phone = ""
                        website = ""
                        rating = "N/A"

                        # --- ADDRESS ---
                        for sel in [
                            'button[data-item-id="address"] div.Io6YTe',
                            'div[data-item-id="address"] span.Io6YTe',
                            'button[data-item-id="address"]',
                        ]:
                            try:
                                loc = page.locator(sel).first
                                if loc.is_visible(timeout=1000):
                                    txt = loc.inner_text(timeout=1000).strip()
                                    if txt and len(txt) > 5 and '' not in txt and '' not in txt:
                                        address = txt
                                        break
                                    # if contains icon, try parent
                                    if '' in txt:
                                        parent = page.locator('button[data-item-id="address"]').first
                                        address = parent.inner_text().replace('','').strip()
                                        break
                            except:
                                pass

                        # --- PHONE ---
                        for sel in [
                            'button[data-item-id*="phone"] div.Io6YTe',
                            'div[data-item-id*="phone"] span.Io6YTe',
                            'button[data-item-id^="phone"]',
                            'a[href^="tel:"]',
                        ]:
                            try:
                                loc = page.locator(sel).first
                                if loc.is_visible(timeout=1000):
                                    txt = loc.inner_text(timeout=1000).strip()
                                    href = loc.get_attribute('href') or ""
                                    if href.startswith('tel:'):
                                        phone = href.replace('tel:','')
                                        break
                                    # clean icon chars
                                    txt_clean = txt.replace('','').replace('','').strip()
                                    if txt_clean and any(c.isdigit() for c in txt_clean):
                                        phone = txt_clean
                                        break
                            except:
                                pass

                        # Fallback phone via regex from whole panel
                        if not phone:
                            try:
                                panel_text = page.locator('div[role="main"]').inner_text(timeout=2000)
                                # italian phone pattern +39 or 0xx
                                m = re.search(r'(\+?39\s?)?0?\d{2,4}[\s\-]?\d{5,8}', panel_text)
                                if m:
                                    phone = m.group(0)
                            except:
                                pass

                        # --- WEBSITE ---
                        for sel in [
                            'a[data-item-id="authority"]',
                            'a[data-value="Website"]',
                            'a[href^="http"]:has-text(".") >> nth=0'
                        ]:
                            try:
                                loc = page.locator(sel).first
                                if loc.is_visible(timeout=1000):
                                    href = loc.get_attribute('href') or loc.inner_text()
                                    if href and 'google.com' not in href and 'maps' not in href:
                                        website = href
                                        break
                            except:
                                pass

                        # --- RATING ---
                        try:
                            rating_loc = page.locator('div.F7nice span[aria-hidden="true"]').first
                            if rating_loc.is_visible(timeout=1000):
                                rating = rating_loc.inner_text(timeout=1000).strip()
                        except:
                            pass

                        lead = clean_business({
                            "Business Name": name,
                            "Address": address,
                            "Phone": phone,
                            "Website": website,
                            "Category": search_query.split(" in ")[0] if " in " in search_query else search_query,
                            "Rating": rating,
                            "Source": "Google Maps"
                        })
                        log(f" -> {lead['Business Name']} | Phone:{lead['Phone']} | Addr:{lead['Address'][:40]}")
                        leads.append(lead)

                    except Exception as e:
                        log(f"Skip card {idx}: {e}")
                        continue

            except Exception as e:
                log(f"Fatal: {e}")
                try:
                    page.screenshot(path="data/error.png")
                except:
                    pass
            finally:
                browser.close()
        
        log(f"Total leads: {len(leads)}")
        return leads
