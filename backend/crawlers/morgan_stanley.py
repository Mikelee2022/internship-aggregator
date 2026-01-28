import requests
import logging
from datetime import datetime

def crawl_morgan_stanley(source_config):
    """
    Crawls Morgan Stanley Careers using their internal API.
    """
    logging.info(f"[{datetime.now()}] Starting Morgan Stanley crawl...")
    internships = []
    
    # Base URL for the search API
    search_api_url = "https://www.morganstanley.com/web/career_services/webapp/service/careerservice/resultset.json"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    params = {
        "opportunity": "sg", # Students & Graduates
        "lang": "EN",
        "businessArea": "Technology"
    }
    
    try:
        logging.info("Fetching jobs from Morgan Stanley API...")
        response = requests.get(search_api_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        # Structure is data['resultSet'] (array)
        if 'resultSet' not in data:
            logging.error(f"Unexpected response structure from Morgan Stanley API: {list(data.keys())}")
            return []
            
        jobs = data['resultSet']
        logging.info(f"Found {len(jobs)} jobs in API response.")
        
        for job in jobs:
            title = job.get('jobTitle')
            job_url = job.get('url')
            
            # Combine city and country for location
            city = job.get('allCity', '')
            country = job.get('allCountries', '')
            location = f"{city}, {country}".strip(", ")
            
            if not location:
                location = "Global / See Details"
            
            if not job_url:
                job_id = job.get('jobNumber')
                job_url = f"https://morganstanley.tal.net/vx/candidate/apply/{job_id}" if job_id else source_config.get('url')
            
            internships.append({
                "company": "Morgan Stanley",
                "role": title,
                "location": location,
                "industry": "Finance",
                "ai_label": any(kw in title.upper() for kw in ['AI', 'LEARNING', 'DATA', 'INTELLIGENCE', 'ML', 'QUANT', 'DEVELOPER', 'ENGINEER', 'TECH']),
                "url": job_url,
                "posted_date": datetime.now(),
                "source": "morgan_stanley_official",
                "logo_url": "https://upload.wikimedia.org/wikipedia/commons/3/34/Morgan_Stanley_Logo_1.svg"
            })
            
    except Exception as e:
        logging.error(f"Error fetching Morgan Stanley jobs: {e}")
        
    logging.info(f"Morgan Stanley crawl complete. Found {len(internships)} jobs.")
    return internships
