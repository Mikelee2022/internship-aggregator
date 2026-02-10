#!/usr/bin/env python3
"""
Debug script to inspect Google Careers page structure
"""
import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from playwright.sync_api import sync_playwright
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def inspect_google_page():
    url = "https://www.google.com/about/careers/applications/jobs/results/?q=internship%202026"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run with visible browser
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            viewport={"width": 1440, "height": 900}
        )
        
        page = context.new_page()
        
        print(f"Navigating to {url}...")
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        
        # Wait for page to load
        time.sleep(5)
        
        # Scroll to trigger lazy loading
        for _ in range(3):
            page.mouse.wheel(0, 800)
            time.sleep(2)
        
        # Get page HTML
        html = page.content()
        
        # Save HTML for inspection
        with open('google_page_debug.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Saved page HTML to google_page_debug.html")
        
        # Try to find job listings with different selectors
        selectors_to_try = [
            "[role='listitem']",
            "li[role='listitem']",
            ".gc-card",
            "[data-job-id]",
            "article",
            ".job-card",
            "[class*='job']",
            "a[href*='/jobs/']",
            "div[class*='result']"
        ]
        
        print("\nTrying different selectors:")
        for selector in selectors_to_try:
            try:
                elements = page.query_selector_all(selector)
                print(f"  {selector}: Found {len(elements)} elements")
                if len(elements) > 0 and len(elements) < 100:
                    # Get first element's HTML
                    first_el = elements[0]
                    print(f"    First element tag: {first_el.evaluate('el => el.tagName')}")
                    print(f"    First element classes: {first_el.evaluate('el => el.className')}")
            except Exception as e:
                print(f"  {selector}: Error - {e}")
        
        # Keep browser open for manual inspection
        print("\nBrowser will stay open for 30 seconds for manual inspection...")
        time.sleep(30)
        
        browser.close()

if __name__ == "__main__":
    inspect_google_page()
