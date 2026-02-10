#!/usr/bin/env python3
"""
Test script to run Google crawler independently for debugging
"""
import sys
import os
import logging

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from crawlers.google import crawl_google

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("Testing Google crawler...")
    print("=" * 60)
    
    source_config = {
        "id": "google_official",
        "name": "Google Careers",
        "url": "https://www.google.com/about/careers/applications/jobs/results/?q=internship%202026",
        "type": "google_official"
    }
    
    internships = crawl_google(source_config)
    
    print("=" * 60)
    print(f"\nResults: Found {len(internships)} internships")
    
    if internships:
        print("\nFirst 3 internships:")
        for i, internship in enumerate(internships[:3], 1):
            print(f"\n{i}. {internship['role']}")
            print(f"   Location: {internship['location']}")
            print(f"   URL: {internship['url']}")
            print(f"   AI Label: {internship['ai_label']}")
    else:
        print("\nNo internships found. Check the logs above for errors.")
