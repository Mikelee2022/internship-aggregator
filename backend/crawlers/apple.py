import logging
import time
import random
from playwright.sync_api import sync_playwright
from datetime import datetime

def crawl_apple(source_config):
    """
    Crawls Apple Jobs using Playwright with stealth techniques.
    """
    logging.info(f"[{datetime.now()}] Starting Apple crawl...")
    internships = []
    
    base_url = "https://jobs.apple.com"
    search_url = source_config.get('url', "https://jobs.apple.com/en-us/search?search=Intern&sort=relevance&location=united-states-USA")
    
    try:
        with sync_playwright() as p:
            # Launch WebKit (Safari engine)
            browser = p.webkit.launch(
                headless=True,
                args=[
                    "--disable-blink-features=AutomationControlled",
                ]
            )
            
            # Create context with realistic User Agent and viewport
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
                viewport={"width": 1440, "height": 900},
                device_scale_factor=2,
                locale="en-US",
                timezone_id="America/Los_Angeles"
            )
            
            # Stealth: Hide webdriver property
            context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            page = context.new_page()
            
            current_page = 1
            max_pages = 3 
            
            while current_page <= max_pages:
                page_url = f"{search_url}&page={current_page}"
                logging.info(f"Navigating to {page_url}...")
                
                try:
                    page.goto(page_url, timeout=60000, wait_until="domcontentloaded")
                except Exception as e:
                    logging.warning(f"Navigation warning: {e}")

                # Human-like interaction (Random movements & scrolling)
                logging.info("Simulating human behavior...")
                for _ in range(random.randint(2, 4)):
                    page.mouse.move(random.randint(100, 1000), random.randint(100, 800))
                    page.mouse.wheel(0, random.randint(200, 500))
                    time.sleep(random.uniform(1.0, 3.0))
                


                # Wait for results
                try:
                    logging.info("Waiting for job list to load...")
                    # Adjusted selector based on debug HTML: Apple uses an accordion list, not a table
                    page.wait_for_selector("#search-job-list", timeout=20000)
                    
                    # Optional: Wait a bit more for stable rendering
                    time.sleep(2)
                    
                    # Count results
                    jobs = page.query_selector_all("#search-job-list > li")
                    count = len(jobs)
                    logging.info(f"Found {count} job rows")
                    
                    # Initialize internships list for this page, or append to global
                    # The provided snippet implies a single list for all pages, so we'll append.
                    # If the intent was to reset per page, this would need adjustment.
                    # Assuming the outer `internships = []` is the main one.
                    
                    for job in jobs:
                        try:
                            # Title & ID are usually in the first part of the accordion
                            # Title link: <a class="link-inline ...">Title</a>
                            title_el = job.query_selector("a.link-inline")
                            if not title_el:
                                continue
                                
                            title = title_el.inner_text().strip()
                            relative_url = title_el.get_attribute("href")
                            url = f"https://jobs.apple.com{relative_url}" if relative_url else ""
                            
                            # Team (e.g. "Software and Services")
                            # <span class="team-name ...">Team</span>
                            team_el = job.query_selector(".team-name")
                            team = team_el.inner_text().strip() if team_el else "Apple"
                            
                            # Location
                            # <div class="job-title-location">...<span>LocationName</span></div>
                            # There might be multiple spans, usually the last one or checking ID
                            loc_el = job.query_selector(".job-title-location")
                            location = "United States"
                            if loc_el:
                                # The location text is often in a span following the "Location" label
                                # Clean up text: "Location\nCupertino" -> "Cupertino"
                                loc_text = loc_el.inner_text()
                                location = loc_text.replace("Location", "").strip()

                            # Date
                            # <span class="job-posted-date">Jan 01, 2026</span>
                            date_el = job.query_selector(".job-posted-date")
                            posted_date_str = date_el.inner_text().strip() if date_el else ""
                            
                            # Parse Date
                            posted_date = datetime.utcnow()
                            if posted_date_str:
                                try:
                                    # Format: "Dec 03, 2025"
                                    posted_date = datetime.strptime(posted_date_str, "%b %d, %Y")
                                except Exception:
                                    pass # Keep default

                            internships.append({
                                "company": "Apple",
                                "role": title,
                                "location": location,
                                "industry": "Tech",
                                "ai_label": 1 if any(x in title.lower() or x in team.lower() for x in ["ai", "intelligence", "machine learning", "data"]) else 0,
                                "url": url,
                                "posted_date": posted_date,
                                "source": "apple_official"
                            })
                            
                        except Exception as e:
                            logging.error(f"Error parsing job row: {e}")
                            continue
                            
                    # The provided snippet has a return here, which would exit after the first page.
                    # To continue pagination, this return should be moved or adjusted.
                    # For now, I'll assume the intent is to process all pages and then return.
                    # The original code had pagination logic, so let's keep that.
                    
                    # Next page logic check (re-using original logic, if applicable)
                    next_btn = page.locator("a.pagination__next").first
                    if next_btn.count() > 0 and "disabled" in next_btn.get_attribute("class"):
                        break # Exit while loop if next button is disabled
                        
                    current_page += 1

                except Exception as e:
                    logging.warning(f"Timeout or error waiting for jobs: {e}")
                    # Debug: Dump page content if we fail again
                    try:
                        with open("apple_debug_final.html", "w") as f:
                            f.write(page.content())
                        page.screenshot(path="apple_timeout_final.png")
                        logging.info("Dumped debug files to apple_debug_final.html and apple_timeout_final.png")
                    except:
                        pass
                    break # Break from while loop on error
                
    except Exception as e:
        logging.error(f"Apple crawler crash: {e}")
    finally:
        try:
            if 'browser' in locals() and browser.is_connected():
                browser.close()
        except:
            pass
    
    logging.info(f"Total Apple internships found: {len(internships)}")
    return internships
