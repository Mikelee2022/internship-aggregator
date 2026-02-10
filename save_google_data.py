#!/usr/bin/env python3
"""
Script to run Google crawler and save results to database
"""
import sys
import os
import logging

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from crawlers.google import crawl_google
from database import get_session, create_db_and_tables
from models import Internship
from sqlmodel import select

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("Running Google crawler and saving to database...")
    print("=" * 60)
    
    # Create tables if they don't exist
    create_db_and_tables()
    
    source_config = {
        "id": "google_official",
        "name": "Google Careers",
        "url": "https://www.google.com/about/careers/applications/jobs/results/?q=internship%202026",
        "type": "google_official"
    }
    
    # Crawl Google
    internships = crawl_google(source_config)
    
    print(f"\nCrawled {len(internships)} Google internships")
    
    # Save to database
    saved_count = 0
    duplicate_count = 0
    
    with next(get_session()) as session:
        for internship_data in internships:
            # Check if already exists
            existing = session.exec(
                select(Internship).where(Internship.url == internship_data['url'])
            ).first()
            
            if existing:
                duplicate_count += 1
                continue
            
            # Create new internship
            internship = Internship(**internship_data)
            session.add(internship)
            saved_count += 1
        
        session.commit()
    
    print("=" * 60)
    print(f"\nResults:")
    print(f"  - New internships saved: {saved_count}")
    print(f"  - Duplicates skipped: {duplicate_count}")
    print(f"  - Total crawled: {len(internships)}")
