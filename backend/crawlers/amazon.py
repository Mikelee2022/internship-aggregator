import logging
import time
import random
from playwright.sync_api import sync_playwright
from datetime import datetime

def crawl_amazon(source_config):
    """
    Crawls Amazon Jobs using Playwright for 2026 internship listings.
    """
    logging.info(f"[{datetime.now()}] Starting Amazon crawl...")
    internships = []
    
    search_url = source_config.get('url', "https://www.amazon.jobs/en/search?base_query=internship+2026&loc_query=United+States")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1440, "height": 900},
                locale="en-US",
                timezone_id="America/Los_Angeles"
            )
            
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()
            
            logging.info(f"Navigating to {search_url}...")
            page.goto(search_url, timeout=60000, wait_until="domcontentloaded")
            
            # Wait for page to load
            time.sleep(4)
            
            # Scroll to trigger lazy loading
            for _ in range(3):
                page.mouse.wheel(0, random.randint(500, 1000))
                time.sleep(random.uniform(1.5, 2.5))
            
            try:
                # Wait for job cards
                page.wait_for_selector(".job-tile", timeout=15000)
                
                # Extract job listings
                jobs = page.query_selector_all(".job-tile")
                logging.info(f"Found {len(jobs)} Amazon job listings")
                
                for job in jobs[:30]:  # Limit to 30 results
                    try:
                        # Title
                        title_el = job.query_selector("h3, .job-title")
                        if not title_el:
                            continue
                        title = title_el.inner_text().strip()
                        
                        # URL
                        link_el = job.query_selector("a")
                        url = link_el.get_attribute("href") if link_el else ""
                        if url and not url.startswith("http"):
                            url = f"https://www.amazon.jobs{url}"
                        
                        # Location
                        location_el = job.query_selector(".location-and-id, .job-location")
                        location = "United States"
                        if location_el:
                            loc_text = location_el.inner_text().strip()
                            # Extract location (usually format: "City, State, Country")
                            location = loc_text.split("|")[0].strip() if "|" in loc_text else loc_text
                        
                        # Check if it's an internship
                        if "intern" not in title.lower():
                            continue
                        
                        # AI label detection
                        ai_keywords = ["ai", "machine learning", "ml", "artificial intelligence", "data science", "applied scientist"]
                        ai_label = 1 if any(kw in title.lower() for kw in ai_keywords) else 0
                        
                        internships.append({
                            "company": "Amazon",
                            "role": title,
                            "location": location,
                            "industry": "Technology",
                            "ai_label": ai_label,
                            "url": url,
                            "posted_date": datetime.utcnow(),
                            "logo_url": "https://upload.wikimedia.org/wikipedia/commons/a/a9/Amazon_logo.svg",
                            "international_score": 6  # Amazon sponsors visas but competitive
                        })
                        
                    except Exception as e:
                        logging.error(f"Error parsing Amazon job: {e}")
                        continue
                        
            except Exception as e:
                logging.warning(f"Error loading Amazon jobs: {e}")
                
            browser.close()
            
    except Exception as e:
        logging.error(f"Amazon crawler crash: {e}")
    
    logging.info(f"Total Amazon internships found: {len(internships)}")
    return internships
