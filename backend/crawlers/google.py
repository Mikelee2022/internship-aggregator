import logging
import time
import random
from playwright.sync_api import sync_playwright
from datetime import datetime

def crawl_google(source_config):
    """
    Crawls Google Careers using Playwright for 2026 internship listings.
    """
    logging.info(f"[{datetime.now()}] Starting Google crawl...")
    internships = []
    
    search_url = source_config.get('url', "https://www.google.com/about/careers/applications/jobs/results/?q=internship%202026")
    
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
            
            # Wait for job listings to load
            time.sleep(3)
            
            # Scroll to load more results
            for _ in range(3):
                page.mouse.wheel(0, random.randint(500, 1000))
                time.sleep(random.uniform(1.5, 2.5))
            
            
            try:
                # Wait for job cards - use the actual class name from Google's page
                page.wait_for_selector("li.lLd3Je", timeout=15000)
                
                # Extract job listings
                jobs = page.query_selector_all("li.lLd3Je")
                logging.info(f"Found {len(jobs)} Google job listings")
                
                for job in jobs[:30]:  # Limit to 30 results
                    try:
                        # Title - in h3 with class QJPWVe
                        title_el = job.query_selector("h3.QJPWVe")
                        if not title_el:
                            continue
                        title = title_el.inner_text().strip()
                        
                        # Check if it's an internship
                        if "intern" not in title.lower():
                            continue
                        
                        # URL - in a tag with class WpHeLc
                        link_el = job.query_selector("a.WpHeLc")
                        url = link_el.get_attribute("href") if link_el else ""
                        if url and not url.startswith("http"):
                            url = f"https://www.google.com/about/careers/applications/{url}"
                        
                        # Location - in span with class r0wTof
                        location_els = job.query_selector_all("span.r0wTof")
                        if location_els and len(location_els) > 0:
                            location = location_els[0].inner_text().strip()
                        else:
                            location = "United States"
                        
                        # AI label detection
                        ai_keywords = ["ai", "machine learning", "ml", "artificial intelligence", "data science", "research"]
                        ai_label = 1 if any(kw in title.lower() for kw in ai_keywords) else 0
                        
                        internships.append({
                            "company": "Google",
                            "role": title,
                            "location": location,
                            "industry": "Technology",
                            "ai_label": ai_label,
                            "url": url,
                            "source": "google_official",
                            "posted_date": datetime.utcnow(),
                            "logo_url": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                            "international_score": 7  # Google is generally international-friendly
                        })
                        
                    except Exception as e:
                        logging.error(f"Error parsing Google job: {e}")
                        continue
                        
            except Exception as e:
                logging.warning(f"Error loading Google jobs: {e}")

                
            browser.close()
            
    except Exception as e:
        logging.error(f"Google crawler crash: {e}")
    
    logging.info(f"Total Google internships found: {len(internships)}")
    return internships
