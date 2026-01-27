from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def crawl_nasa(source_config):
    """
    Crawls NASA STEM Gateway using Playwright to handle LWC/Shadow DOM.
    """
    print(f"[{datetime.now()}] Starting NASA crawl...")
    internships = []
    
    try:
        with sync_playwright() as p:
            # Launch browser with anti-detection args
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
            page = context.new_page()
            
            url = source_config.get('url', "https://stemgateway.nasa.gov/public/s/explore-opportunities")
            print(f"Navigating to {url}...")
            page.goto(url, timeout=60000)
            
            # Wait for content
            print("Page loaded, waiting for dynamic content...")
            try:
                page.wait_for_load_state("networkidle", timeout=30000)
                
                # Check title
                print(f"Page title: {page.title()}")
                
                # Take debug screenshot
                page.screenshot(path="nasa_debug.png")
                
                # Try generic wait first
                page.wait_for_selector("c-ostem_opportunityresultscard", timeout=20000)
            except Exception as e:
                print(f"Timeout/Error waiting for content: {e}")
                # Save screenshot of what we saw
                page.screenshot(path="nasa_error.png")
                # Try to extract ANY h2 tags in case structure matches
                
            # Get all cards (or whatever handles h2)
            cards = page.locator("c-ostem_opportunityresultscard").all()
            if not cards:
                 # Backup: look for any card-like structure
                 print("No specific cards found, looking for generic articles...")
                 cards = page.locator("article").all()
            
            print(f"Found {len(cards)} opportunity cards.")
            
            for card in cards:
                try:
                    title_loc = card.locator("h2")
                    if title_loc.count() == 0:
                        # try looking for any text causing 'Student'
                        if "Student" in card.inner_text():
                             title = card.inner_text().split("\n")[0]
                        else:
                             continue
                    else:
                        title = title_loc.first.inner_text().strip()

                    
                    # Tags/Locations often in .slds-button_neutral
                    # We can join them to form "Location" or "Requirements"
                    tags = card.locator(".slds-button_neutral").all_inner_texts()
                    location = "NASA Center (See Details)"
                    # Try to find a tag that looks like a location (e.g. contains , or State)
                    # For now just join them
                    summary_tags = ", ".join([t for t in tags if "Internship" not in t])
                    
                    # Generate URL
                    # We try to click or find ID. 
                    # If strictly listing, we might just link to the main page or try to extract ID
                    # If we can't find specific URL, link to base
                    job_url = url
                    
                    # Try to find a 'view' button or anchor?
                    # Subagent said clicking title works.
                    # We can't easily get the URL without clicking unless it's an <a> tag.
                    # Let's check for an anchor with href
                    links = card.locator("a").all()
                    for link in links:
                        href = link.get_attribute("href")
                        if href and ("course-offering" in href or "opportunity" in href):
                            if href.startswith("/"):
                                job_url = "https://stemgateway.nasa.gov" + href
                            else:
                                job_url = href
                            break
                    
                    internships.append({
                        "company": "NASA",
                        "role": title,
                        "location": summary_tags if summary_tags else location,
                        "industry": "Aerospace / Government",
                        "ai_label": 0, # Default
                        "url": job_url,
                        "posted_date": datetime.now(), # Real-time
                        "source": "NASA STEM Gateway"
                    })
                    
                except Exception as inner_e:
                    print(f"Error parsing card: {inner_e}")
                    continue
            
            browser.close()
            
    except Exception as e:
        print(f"Playwright error: {e}")
        # Return what we have or empty
    
    return internships
