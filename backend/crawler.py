import requests
import re
import json
import os
import random
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Internship

# Configure Logging
log_file_path = os.path.join(os.path.dirname(__file__), 'crawler.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler()
    ]
)

# Helper function to load config
def load_data_sources():
    config_path = os.path.join(os.path.dirname(__file__), 'data_sources.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading data sources config: {e}")
        return []

def calculate_international_score(text: str) -> int:
    score = 5 # Neutral start
    text_upper = text.upper()
    
    # Positive signals
    positives = ["VISA SPONSORSHIP", "CPT", "OPT", "INTERNATIONAL", "GLOBAL", "RELOCATION", "SPONSOR"]
    for p in positives:
        if p in text_upper:
            score += 2
            
    # Negative signals (Stronger penality)
    negatives = ["US CITIZEN", "U.S. CITIZEN", "SECURITY CLEARANCE", "NO SPONSORSHIP", "CITIZENSHIP REQUIRED", "US PERSON"]
    for n in negatives:
        if n in text_upper:
            score -= 10
            
    return max(1, min(10, score))

def process_github_readme(source_config, session):
    """
    Detailed crawler for the GitHub README source.
    """
    url = source_config.get('url')
    logging.info(f"Fetching data from GitHub source: {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.text
    except Exception as e:
        logging.error(f"Error fetching GitHub data: {e}")
        return

    # Use BeautifulSoup to parse HTML content within the markdown
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the table - assuming it's the first table
    table = soup.find('table')
    if not table:
        logging.warning("No table found in content.")
        return

    rows = table.find_all('tr')
    count = 0
    errors = 0
    
    for row in rows:
        cols = row.find_all('td')
        if not cols or len(cols) < 3: # Header row or invalid
            continue
        
        try:
            # 0: Company, 1: Role, 2: Location, 3: Application, 4: Age
            company_col = cols[0]
            role_col = cols[1]
            location_col = cols[2]
            app_col = cols[3]
            
            # Extract Company Name
            company_text = company_col.get_text(strip=True)
            # Remove emojis if any (heuristic)
            company_name = re.sub(r'[^\w\s&.-]', '', company_text).strip()
            
            # Extract Role
            role = role_col.get_text(strip=True)
            
            # Extract Location
            if location_col.find('details'):
                 location = location_col.get_text(" ", strip=True)
            else:
                location = location_col.get_text(strip=True)
            
            # Extract URL
            link_tag = app_col.find('a')
            if link_tag and link_tag.get('href'):
                url = link_tag.get('href')
            else:
                company_link = company_col.find('a')
                url = company_link.get('href') if company_link else source_config.get('url')

            # Extract Date (Age)
            try:
                if len(cols) >= 5:
                    age_text = cols[4].get_text(strip=True)
                    if 'h' in age_text:
                        hours = int(re.sub(r'[^0-9]', '', age_text))
                        posted_date = datetime.utcnow() - timedelta(hours=hours)
                    elif 'd' in age_text:
                        days = int(re.sub(r'[^0-9]', '', age_text))
                        posted_date = datetime.utcnow() - timedelta(days=days)
                    else:
                        posted_date = datetime.utcnow()
                else:
                    posted_date = datetime.utcnow()
            except Exception:
               posted_date = datetime.utcnow()

            # Check for existing
            existing = session.exec(select(Internship).where(Internship.url == url)).first()
            if existing:
                continue

            # Mock JD text / Score calculation
            mock_text_context = f"{role} at {company_name}. "
            if "Research" in role:
                mock_text_context += " PhD preferred. "
            if "Defense" in company_name or "CACI" in company_name:
                mock_text_context += " Security Clearance required. US Citizen only. "
            elif "Global" in company_name or "Meta" in company_name or "Google" in company_name:
                mock_text_context += " Visa sponsorship available for eligible candidates. w/ CPT/OPT. "
            
            score = calculate_international_score(mock_text_context)

            # Logo guessing
            safe_company_domain = re.sub(r'[^a-zA-Z]', '', company_name).lower() + ".com"
            logo_url_guess = f"https://www.google.com/s2/favicons?domain={safe_company_domain}&sz=64"

            internship = Internship(
                company=company_name,
                role=role,
                location=location,
                url=url,
                industry="Technology",
                ai_label="AI" in role.upper() or "LEARNING" in role.upper(),
                posted_date=posted_date,
                requirements="Python, React, SQL", # Placeholder
                salary="$30 - $60 / hr", # Placeholder
                deadline=None,
                international_score=score,
                logo_url=logo_url_guess
            )
            session.add(internship)
            count += 1
        except Exception as e:
            errors += 1
            logging.error(f"Error parsing row: {e}")
            continue
            
    logging.info(f"Scraped and saved {count} new internships from GitHub. Errors encountered: {errors}")

def process_simulated_source(source_config, session):
    """
    Simulates scraping a premium company source based on config.
    """
    logging.info(f"Processing simulated source: {source_config['name']}")
    config = source_config.get('config', {})
    
    company_name = config.get("company_name", source_config['name'])
    domain = config.get("domain", "")
    base_url = source_config.get("url", "")
    locations = config.get("locations", ["Remote"])
    roles = config.get("roles", ["Intern"])
    score_context = config.get("score_context", "")

    # Generate 3-5 listings
    num_listings = random.randint(3, 5)
    count = 0
    
    for _ in range(num_listings):
        role = random.choice(roles)
        location = random.choice(locations)
        # Generate a pseudo-unique URL
        job_id = random.randint(100000, 999999)
        url = f"{base_url}{job_id}"
        
        existing = session.exec(select(Internship).where(Internship.url == url)).first()
        if existing:
            continue

        internship = Internship(
            company=company_name,
            role=role,
            location=location,
            url=url,
            industry="Technology" if company_name not in ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "BlackRock"] else "Finance",
            ai_label=True if "AI" in role or "Machine Learning" in role or "Data" in role else False,
            posted_date=datetime.utcnow(),
            requirements="Currently enrolled in Bachelor's or Master's degree. 3.0+ GPA preferred.",
            salary="$40 - $70 / hr" if "Finance" not in company_name else "$50 - $90 / hr",
            international_score=calculate_international_score(score_context),
            logo_url=f"https://www.google.com/s2/favicons?domain={domain}&sz=128"
        )
        session.add(internship)
        count += 1
        
    logging.info(f"Saved {count} listings for {company_name}.")


def run_crawler():
    logging.info("Starting crawler run...")
    create_db_and_tables()
    
    sources = load_data_sources()
    if not sources:
        logging.warning("No data sources configured.")
        return

    with Session(engine) as session:
        for source in sources:
            if not source.get("enabled", True):
                continue
                
            source_type = source.get("type")
            
            if source_type == "github_readme":
                process_github_readme(source, session)
            elif source_type == "simulated_company_listing":
                process_simulated_source(source, session)
            else:
                logging.warning(f"Unknown source type: {source_type} for {source['name']}")
        
        session.commit()
        logging.info("Crawler run complete.")

if __name__ == "__main__":
    run_crawler()
