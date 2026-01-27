from playwright.sync_api import sync_playwright
import time
from datetime import datetime

def crawl_meta(source_config):
    """
    Crawls Meta Careers using Playwright.
    """
    print(f"[{datetime.now()}] Starting Meta crawl...")
    internships = []
    
    base_url = "https://www.metacareers.com"
    search_url = source_config.get('url', "https://www.metacareers.com/jobsearch?roles[0]=Internship")
    
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
            
            # Pagination loop
            current_page = 1
            max_pages = 5 # Safety limit to prevent infinite loops during dev
            
            while current_page <= max_pages:
                page_url = f"{search_url}&page={current_page}"
                print(f"Navigating to {page_url}...")
                page.goto(page_url, timeout=60000)
                
                try:
                    page.wait_for_load_state("networkidle", timeout=20000)
                    # Wait for at least one h3 or job link
                    page.wait_for_selector('h3', timeout=10000)
                except Exception as e:
                    print(f"Timeout waiting for content on page {current_page}: {e}")
                    break

                # Get all anchors that look like job links
                # Usually href starts with /profile/job_details/ or /jobs/
                # The subagent said /profile/job_details/[ID]
                
                # Check if we have results
                # Meta usually says "0 Jobs Found" or something if empty
                # We can check the text content or just look for cards
                
                cards = page.locator("a[href*='/jobs/'], a[href*='/profile/job_details/']").all()
                # Filter out navigation links if any, usually job cards have an h3 inside
                
                job_cards = []
                for card in cards:
                     if card.locator("h3").count() > 0:
                         job_cards.append(card)
                
                print(f"Found {len(job_cards)} job cards on page {current_page}.")
                
                if len(job_cards) == 0:
                    print("No more jobs found.")
                    break
                
                for card in job_cards:
                    try:
                        title_el = card.locator("h3").first
                        title = title_el.inner_text().strip()
                        
                        relative_url = card.get_attribute("href")
                        job_url = base_url + relative_url if relative_url.startswith("/") else relative_url
                        
                        # Metadata (Location, etc.) is often in a div/span structure below title
                        # Let's try to grab all text and parse heuristically
                        all_text = card.inner_text().split('\n')
                        # Expected: Title, Location, Team...
                        # If title is index 0, location might be index 1
                        
                        location = "Remote / See Details"
                        # Try to find location-like text or just take the second line
                        if len(all_text) > 1 and all_text[0] == title:
                             location = all_text[1]
                        
                        # Fix for potential "New" badges etc
                        
                        internships.append({
                            "company": "Meta",
                            "role": title,
                            "location": location,
                            "industry": "Technology",
                            "ai_label": "AI" in title or "Learning" in title or "Research" in title,
                            "url": job_url,
                            "posted_date": datetime.now(),
                            "source": "Meta Careers"
                        })
                        
                    except Exception as inner_e:
                        print(f"Error parsing card: {inner_e}")
                        continue
                
                # Check for "Next" button/pagination state?
                # For now just increment page and rely on empty results to stop
                current_page += 1
                time.sleep(2) # Polite delay
                
            browser.close()
            
    except Exception as e:
        print(f"Playwright error: {e}")
    
    return internships
