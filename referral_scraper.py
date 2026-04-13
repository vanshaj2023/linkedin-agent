import asyncio
from playwright.async_api import async_playwright
import browser_manager
from people_scraper import scrape_people_search # We can leverage the existing people scraper logic!

async def scrape_company_employees(company_name: str, target_roles: list, max_results: int = 3, headless: bool = True):
    """
    Search for employees at a specific company who hold specific target roles.
    Uses the existing people scraper query logic.
    """
    results = []
    
    for role in target_roles:
        query = f'"{role}" AND "{company_name}"'
        print(f"Scraping for: {query}")
        
        # We reuse the people_scraper logic since it already bypasses the network restrictions
        # by searching through the global search bar
        profiles = await scrape_people_search(keyword=query, max_results=max_results, headless=headless)
        
        for profile in profiles:
            if len(results) >= max_results:
                break
                
            # Basic validation to ensure the company name actually appears in their location/headline
            headline_lower = profile.get("headline", "").lower()
            location_lower = profile.get("location", "").lower()
            comp_lower = company_name.lower().replace("inc.", "").replace("llc", "").strip()
            
            if comp_lower in headline_lower or comp_lower in location_lower:
                results.append({
                    "name": profile["name"],
                    "linkedin_url": profile["linkedin_url"],
                    "headline": profile["headline"],
                    "company_target": company_name,
                    "matched_role": role
                })
        
        if len(results) >= max_results:
            break
            
    return results

if __name__ == "__main__":
    employees = asyncio.run(scrape_company_employees("Google", ["Software Engineer", "Engineering Manager"], 2, headless=False))
    print(employees)
