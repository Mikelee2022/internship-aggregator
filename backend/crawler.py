import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import Internship

# Target URL for Summer 2026 Internships
URL = "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/README.md" 

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

def fetch_data():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def parse_and_save(content):
    if not content:
        return

    # Use BeautifulSoup to parse HTML content within the markdown
    soup = BeautifulSoup(content, 'html.parser')
    
    # Find the table - assuming it's the first table or finding one with appropriate headers
    # The README seems to use a single main table for listings
    table = soup.find('table')
    if not table:
        print("No table found in content.")
        return

    rows = table.find_all('tr')
    
    with Session(engine) as session:
        count = 0
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
                # Handle details tag if present
                if location_col.find('details'):
                    # Just take the first location or "Multiple Locations"
                    # For simplicty, let's take the summary part usually saying "X locations" or just text
                    location = location_col.get_text(" ", strip=True)
                    # Clean up "X locations" prefix if we want, but keeping it simple for MVP
                else:
                    location = location_col.get_text(strip=True)
                
                # Extract URL
                # Look for the first <a> tag in the Application column
                link_tag = app_col.find('a')
                if link_tag and link_tag.get('href'):
                    url = link_tag.get('href')
                else:
                    # Fallback to company link? Or skip?
                    # Let's try to find any link in the Company column if App is empty
                    company_link = company_col.find('a')
                    url = company_link.get('href') if company_link else "https://github.com/SimplifyJobs/Summer2026-Internships"

                # Extract Date (Age)
                # content is usually "1d", "20h", "Feb 23"
                try:
                    if len(cols) >= 5:
                        age_text = cols[4].get_text(strip=True)
                        from datetime import timedelta
                        if 'h' in age_text:
                            hours = int(re.sub(r'[^0-9]', '', age_text))
                            posted_date = datetime.utcnow() - timedelta(hours=hours)
                        elif 'd' in age_text:
                            days = int(re.sub(r'[^0-9]', '', age_text))
                            posted_date = datetime.utcnow() - timedelta(days=days)
                        else:
                            # Fallback or try to parse 'Mon Day' if format changes
                            posted_date = datetime.utcnow()
                    else:
                        posted_date = datetime.utcnow()
                except Exception:
                   posted_date = datetime.utcnow()

                # Check for existing
                existing = session.exec(select(Internship).where(Internship.url == url)).first()
                if existing:
                    continue

                # Calculate Score
                # In a real app, we would fetch the full JD text from the URL. 
                # Here we use the available metadata (Role + Company + Requirements/Notes if we had them)
                # and some simulated random variance for the MVP demo if text is sparse.
                # Adding some mock descriptions to simulating finding keywords for demonstration.
                
                # Mock JD text based on company/role for demonstration
                mock_text_context = f"{role} at {company_name}. "
                if "Research" in role:
                    mock_text_context += " PhD preferred. "
                if "Defense" in company_name or "CACI" in company_name:
                    mock_text_context += " Security Clearance required. US Citizen only. "
                elif "Global" in company_name or "Meta" in company_name or "Google" in company_name:
                    mock_text_context += " Visa sponsorship available for eligible candidates. w/ CPT/OPT. "
                
                score = calculate_international_score(mock_text_context)

                # Heuristic for logo: clean company name + .com or try to extract from URL if possible
                # Simple version: logo.clearbit.com/{company_name}.com (very naive but visual)
                # Better: Leave empty for scraped ones or use a placeholder if we want consistent look.
                # Let's try a safe bet: if existing logic works, great. 
                # For scraped data, let's just use the company name to guess a domain 
                safe_company_domain = re.sub(r'[^a-zA-Z]', '', company_name).lower() + ".com"
                logo_url_guess = f"https://www.google.com/s2/favicons?domain={safe_company_domain}&sz=64"

                internship = Internship(
                    company=company_name,
                    role=role,
                    location=location,
                    url=url,
                    industry="Technology", # Default
                    ai_label="AI" in role.upper() or "LEARNING" in role.upper(),
                    posted_date=posted_date,
                    requirements="Python, React, SQL", # Placeholder
                    salary="$30 - $60 / hr", # Placeholder
                    deadline=None, # Placeholder
                    international_score=score,
                    logo_url=logo_url_guess
                )
                session.add(internship)
                count += 1
            except Exception as e:
                # print(f"Skipping row due to error: {e}")
                continue
        
        session.commit()
        print(f"Scraped and saved {count} new internships.")

def seed_premium_sources(session: Session):
    print("Batch crawling (simulated) premium sources...")
    
    # Configuration for Premium Sources
    companies = [
        {"name": "NASA", "domain": "nasa.gov", "url_base": "https://intern.nasa.gov/job/", "locations": ["Houston, TX", "Greenbelt, MD", "Pasadena, CA", "Huntsville, AL"], "roles": ["Aerospace Engineering Intern", "Software Engineering Intern", "Data Science Intern", "Research Associate Intern"], "score_context": "US Citizen Only. Security Clearance."},
        {"name": "Google", "domain": "google.com", "url_base": "https://careers.google.com/jobs/results/", "locations": ["Mountain View, CA", "New York, NY", "Seattle, WA", "Remote"], "roles": ["Software Engineering Intern, BS/MS", "STEP Intern", "Product Management Intern", "UX Design Intern"], "score_context": "Visa sponsorship. Global."},
        {"name": "Apple", "domain": "apple.com", "url_base": "https://jobs.apple.com/en-us/details/", "locations": ["Cupertino, CA", "Austin, TX", "Seattle, WA"], "roles": ["Software Engineer Intern", "Hardware Engineering Intern", "Machine Learning Intern", "Silicon Engineering Intern"], "score_context": "Visa sponsorship. Global."},
        {"name": "Goldman Sachs", "domain": "goldmansachs.com", "url_base": "https://www.goldmansachs.com/careers/", "locations": ["New York, NY", "Salt Lake City, UT", "Dallas, TX"], "roles": ["Summer Analyst - Engineering", "Summer Analyst - Global Markets", "Summer Analyst - Wealth Management"], "score_context": "Visa sponsorship possible. Finance."},
        {"name": "Microsoft", "domain": "microsoft.com", "url_base": "https://careers.microsoft.com/us/en/job/", "locations": ["Redmond, WA", "Atlanta, GA", "Cambridge, MA"], "roles": ["Software Engineering Intern", "Product Manager Intern", "Data Science Intern", "Explore Intern"], "score_context": "Visa sponsorship. Global."},
        {"name": "JPMorgan Chase", "domain": "jpmorgan.com", "url_base": "https://careers.jpmorgan.com/us/en/students/programs/", "locations": ["New York, NY", "Plano, TX", "Wilmington, DE"], "roles": ["Software Engineer Program - Summer Intern", "AI & Machine Learning Summer Associate", "Corporate Analyst Development Program"], "score_context": "Visa sponsorship possible. Finance."},
        {"name": "Morgan Stanley", "domain": "morganstanley.com", "url_base": "https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/xf-4a47688755b4/candidate/so/pm/1/pl/1/opp/", "locations": ["New York, NY", "Baltimore, MD"], "roles": ["Technology Summer Analyst", "Quantitative Finance Intern", "Investment Banking Summer Analyst"], "score_context": "Visa sponsorship possible. Finance."},
        {"name": "Meta", "domain": "meta.com", "url_base": "https://www.metacareers.com/v2/jobs/", "locations": ["Menlo Park, CA", "New York, NY", "Seattle, WA"], "roles": ["Software Engineer Intern", "Rotational Product Manager (RPM) Intern", "Research Scientist Intern", "Data Engineering Intern"], "score_context": "Visa sponsorship. Global."},
        {"name": "BlackRock", "domain": "blackrock.com", "url_base": "https://careers.blackrock.com/job/", "locations": ["New York, NY", "San Francisco, CA"], "roles": ["Summer Analyst - Engineering", "Summer Analyst - Investments", "Summer Analyst - Analytics & Risk"], "score_context": "Visa sponsorship possible. Finance."},
    ]

    count = 0
    import random
    
    for company_conf in companies:
        # Generate 3-5 listings per company to simulate a full crawl
        num_listings = random.randint(3, 5)
        
        for _ in range(num_listings):
            role = random.choice(company_conf["roles"])
            location = random.choice(company_conf["locations"])
            # Generate a pseudo-unique URL
            job_id = random.randint(100000, 999999)
            url = f"{company_conf['url_base']}{job_id}"
            
            existing = session.exec(select(Internship).where(Internship.url == url)).first()
            if existing:
                continue

            internship = Internship(
                company=company_conf["name"],
                role=role,
                location=location,
                url=url,
                industry="Technology" if company_conf["name"] not in ["Goldman Sachs", "JPMorgan Chase", "Morgan Stanley", "BlackRock"] else "Finance",
                ai_label=True if "AI" in role or "Machine Learning" in role or "Data" in role else False,
                posted_date=datetime.utcnow(),
                requirements="Currently enrolled in Bachelor's or Master's degree. 3.0+ GPA preferred.",
                salary="$40 - $70 / hr" if "Finance" not in company_conf["name"] else "$50 - $90 / hr",
                international_score=calculate_international_score(company_conf["score_context"]),
                logo_url=f"https://www.google.com/s2/favicons?domain={company_conf['domain']}&sz=128"
            )
            session.add(internship)
            count += 1
            
    session.commit()
    print(f"Batch crawled (simulated) {count} premium listings from official sources.")

def run_crawler():
    create_db_and_tables()
    
    with Session(engine) as session:
        seed_premium_sources(session)
        
    content = fetch_data()
    if content:
        parse_and_save(content)

if __name__ == "__main__":
    run_crawler()
