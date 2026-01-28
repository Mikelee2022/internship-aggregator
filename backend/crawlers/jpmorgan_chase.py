import logging
from playwright.sync_api import sync_playwright
from datetime import datetime
import time

def crawl_jpmorgan_chase(source_config):
    """
    Crawl JPMorgan Chase tech program listings using Playwright.
    """
    url = source_config.get('url')
    if not url:
        return []

    internships = []
    
    try:
        with sync_playwright() as p:
            # Launch browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            logging.info(f"Navigating to {url}...")
            page.goto(url, timeout=60000)
            
            # Wait for content to load
            try:
                page.wait_for_selector(".card", timeout=30000)
            except Exception as e:
                logging.error(f"Timeout waiting for JPMC cards: {e}")
                return []

            # Tabs to iterate through: School Programs, Internship, Full-Time
            # We'll click each tab and collect the visible cards.
            # Tab labels: "School Programs & Apprenticeships", "Early Insight (pre-internship)", "Internship", "Full-Time"
            tabs_to_collect = ["Internship", "School Programs & Apprenticeships"]
            
            for tab_label in tabs_to_collect:
                logging.info(f"Collecting JPMC programs from tab: {tab_label}")
                
                try:
                    # Find and click the tab
                    tab_buttons = page.locator("button[role='tab']").all()
                    target_tab = None
                    for btn in tab_buttons:
                        if tab_label in btn.inner_text():
                            target_tab = btn
                            break
                    
                    if target_tab:
                        target_tab.click()
                        time.sleep(2) # Polite delay for content switch
                        
                        # Extract cards for this tab
                        # Only collect visible cards (offsetParent !== null)
                        cards = page.evaluate("""
                            () => {
                                const cardElements = Array.from(document.querySelectorAll('.card'));
                                return cardElements
                                    .filter(card => card.offsetParent !== null)
                                    .map(card => ({
                                        title: card.querySelector('h2')?.innerText?.trim(),
                                        category: card.querySelector('p')?.innerText?.trim(),
                                        location: card.querySelector('div span p')?.innerText?.trim() || card.querySelector('span p')?.innerText?.trim(),
                                        url: card.href
                                    }));
                            }
                        """)
                        
                        for card_data in cards:
                            title = card_data.get('title')
                            if not title: continue
                            
                            category = card_data.get('category', 'Internship')
                            location = card_data.get('location', 'Global')
                            full_url = card_data.get('url')
                            
                            internships.append({
                                "company": "JPMorgan Chase",
                                "role": title,
                                "location": location,
                                "industry": "Finance",
                                "ai_label": any(kw in title.lower() for kw in ['ai', 'intelligence', 'machine learning', 'data', 'engineer', 'tech']),
                                "url": full_url,
                                "posted_date": datetime.utcnow(),
                                "source": "jpmorgan_chase_official",
                                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/af/J_P_Morgan_Chase_Logo_2008.svg"
                            })
                    else:
                        logging.warning(f"Tab not found: {tab_label}")
                        
                except Exception as tab_e:
                    logging.error(f"Error processing JPMC tab {tab_label}: {tab_e}")
                    continue

            browser.close()
            
    except Exception as e:
        logging.error(f"JPMorgan Chase crawler failed: {e}")
        
    logging.info(f"Total JPMorgan Chase programs found: {len(internships)}")
    return internships
