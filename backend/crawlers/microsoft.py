import requests
import logging
from datetime import datetime

def crawl_microsoft(source_config):
    """
    Crawls Microsoft Careers using their internal API.
    """
    logging.info(f"[{datetime.now()}] Starting Microsoft crawl...")
    internships = []
    
    # Base URL for the search API
    search_api_url = "https://apply.careers.microsoft.com/api/pcsx/search"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json"
    }
    
    # We'll fetch multiple pages until we hit the limit or no more results
    start = 0
    page_size = 20
    max_items = 200 # Safety limit
    
    while start < max_items:
        params = {
            "domain": "microsoft.com",
            "query": "internship",
            "location": "",
            "start": start,
            "sort_by": "relevance"
        }
        
        try:
            logging.info(f"Fetching jobs starting from {start}...")
            response = requests.get(search_api_url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            # The structure is: data['data']['positions']
            if 'data' not in data or 'positions' not in data['data']:
                logging.error(f"Unexpected response structure from Microsoft API: {list(data.keys())}")
                break
                
            positions = data['data']['positions']
            if not positions:
                logging.info("No more positions found.")
                break
            
            for pos in positions:
                job_id = pos.get('id')
                title = pos.get('name')
                locations = pos.get('locations', [])
                location_str = ", ".join(locations) if locations else "Global"
                
                # Construct the direct job URL
                # The browser subagent saw: https://apply.careers.microsoft.com/careers?query=internship&start=0&pid=[JOB_ID]
                # But a cleaner one is often /careers/job/[JOB_ID]
                job_url = f"https://apply.careers.microsoft.com/careers/job/{job_id}" if job_id else source_config.get('url')
                
                internships.append({
                    "company": "Microsoft",
                    "role": title,
                    "location": location_str,
                    "industry": "Technology",
                    "ai_label": "AI" in title.upper() or "LEARNING" in title.upper() or "DATA" in title.upper(),
                    "url": job_url,
                    "posted_date": datetime.now(),
                    "source": "microsoft_official",
                    "logo_url": "https://upload.wikimedia.org/wikipedia/commons/4/44/Microsoft_logo.svg"
                })
            
            # Increment start for next page
            start += page_size
            
            # If we got fewer positions than page_size, it's likely the last page
            if len(positions) < page_size:
                break
                
        except Exception as e:
            logging.error(f"Error fetching Microsoft jobs (start={start}): {e}")
            break
            
    logging.info(f"Microsoft crawl complete. Found {len(internships)} jobs.")
    return internships
