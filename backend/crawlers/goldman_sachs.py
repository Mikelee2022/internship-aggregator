import logging
from playwright.sync_api import sync_playwright
from datetime import datetime
import time
import random

def crawl_goldman_sachs(source_config):
    """
    Crawl Goldman Sachs internship listings using Playwright.
    """
    url = source_config.get('url')
    if not url:
        return []

    internships = []
    
    try:
        with sync_playwright() as p:
            # Launch browser
            # Goldman Sachs might need standard headers/user-agent manipulation
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            logging.info(f"Navigating to {url}...")
            page.goto(url, timeout=60000)
            
            # Wait for content
            try:
                # Wait for the specific list item class we identified
                logging.info("Waiting for intern list...")
                page.wait_for_selector("li.gs-uitk-c-1svbtzk--content-list-item-root", timeout=30000)
            except Exception as e:
                logging.error(f"Timeout waiting for Goldman Sachs jobs: {e}")
                page.screenshot(path="gs_timeout.png")
                return []

            # Scroll to load listing (just in case of lazy load)
            for _ in range(3):
                page.mouse.wheel(0, 1000)
                time.sleep(2)
            
            # Extract items
            job_cards = page.query_selector_all("li.gs-uitk-c-1svbtzk--content-list-item-root")
            logging.info(f"Found {len(job_cards)} job cards.")

            for card in job_cards:
                try:
                    # Title and Link
                    # Selector: a.gs-uitk-c-jdfrbi--link-root--link-anchor--text-content-list-header-link
                    title_el = card.query_selector("a.gs-uitk-c-jdfrbi--link-root--link-anchor--text-content-list-header-link")
                    if not title_el:
                        continue
                        
                    title = title_el.inner_text().strip()
                    href = title_el.get_attribute("href")
                    # GS links might be relative or absolute, usually absolute or relative to domain
                    full_url = href if href.startswith("http") else f"https://www.goldmansachs.com{href}"
                    
                    # Location
                    # Selector: span.gs-uitk-c-sm0my--content-list-item-meta
                    loc_el = card.query_selector("span.gs-uitk-c-sm0my--content-list-item-meta")
                    location = loc_el.inner_text().strip() if loc_el else "Global"

                    # Basic AI Labeling
                    is_ai = any(kw in title.lower() for kw in ['ai', 'intelligence', 'machine learning', 'data', 'engineer'])

                    internships.append({
                        "company": "Goldman Sachs",
                        "role": title,
                        "location": location,
                        "industry": "Finance",
                        "ai_label": 1 if is_ai else 0,
                        "url": full_url,
                        "posted_date": datetime.utcnow(), # GS doesn't always show date on list view
                        "source": "goldman_sachs_official",
                        "logo_url": "https://upload.wikimedia.org/wikipedia/commons/6/61/Goldman_Sachs.svg"
                    })
                    
                except Exception as e:
                    logging.warning(f"Error parsing GS job card: {e}")
                    continue

    except Exception as e:
        logging.error(f"Goldman Sachs crawler failed: {e}")
        
    logging.info(f"Total Goldman Sachs internships found: {len(internships)}")
    return internships
