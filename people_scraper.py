import asyncio
from playwright.async_api import async_playwright
import browser_manager

async def scrape_people_search(keyword="Software Engineer", max_results=10, headless=True):
    """
    Search for people on LinkedIn based on a keyword and scrape their basic profile links and metadata.
    Does not visit their profiles (that is done later by the Action Queue).
    """
    results = []
    
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=headless)
        page = await context.new_page()
        await browser_manager.setup_page_stealth(page)
        
        url = f"https://www.linkedin.com/search/results/people/?keywords={keyword}&origin=CLUSTER_EXPANSION"
        print(f"Navigating to people search: {url}")
        
        await browser_manager.safe_sleep()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        
        # Click randomly to ensure focus
        try:
            await page.locator("body").click(position={"x": 50, "y": 50})
        except Exception:
            pass
            
        # LinkedIn people search results are in `li.reusable-search__result-container`
        for i in range(3):
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight / 3)')
            await page.wait_for_timeout(1000)
            
        containers = await page.locator("li.reusable-search__result-container").all()
        print(f"Found {len(containers)} result containers.")
        
        for container in containers:
            if len(results) >= max_results:
                break
                
            try:
                # Extract URL and Name
                link_locator = container.locator("span.entity-result__title-text a.app-aware-link").first
                profile_url = await link_locator.get_attribute("href")
                if profile_url:
                    profile_url = profile_url.split("?")[0] # remove tracking params
                
                 # The 'aria-hidden=true' span usually contains just the name without the "View profile" screen reader text
                name_locator = link_locator.locator("span[aria-hidden='true']").first
                name = await name_locator.inner_text() if await name_locator.count() > 0 else "Unknown Name"
                
                # Extract Headline
                headline_locator = container.locator("div.entity-result__primary-subtitle").first
                headline = await headline_locator.inner_text() if await headline_locator.count() > 0 else ""
                
                # Extract Location / Company approximations
                location_locator = container.locator("div.entity-result__secondary-subtitle").first
                location = await location_locator.inner_text() if await location_locator.count() > 0 else ""
                
                if profile_url and "linkedin.com/in/" in profile_url:
                    results.append({
                        "name": name.strip(),
                        "linkedin_url": profile_url,
                        "headline": headline.strip(),
                        "location": location.strip()
                    })
            except Exception as e:
                print(f"Error scraping a people search result: {e}")
                
        await context.browser.close()
        
    return results

async def search_people(keywords: str, max_results: int = 30) -> list:
    """
    Alias used by agents. Searches LinkedIn people by keywords.
    Returns list of dicts: {name, headline, company, linkedin_url, mutual_connections}
    """
    raw = await scrape_people_search(keyword=keywords, max_results=max_results, headless=True)
    # Normalise field names + add company (extracted from location/headline field)
    normalised = []
    for r in raw:
        # location field often contains "Company · Location" or just company
        loc = r.get("location", "")
        company = loc.split("·")[0].strip() if "·" in loc else loc
        normalised.append({
            "name": r["name"],
            "headline": r.get("headline", ""),
            "company": company,
            "linkedin_url": r["linkedin_url"],
            "mutual_connections": 0,  # not extracted in base scraper
        })
    return normalised


async def search_company_employees(company: str, max_results: int = 50) -> list:
    """
    Searches LinkedIn for people currently at a specific company.
    """
    return await search_people(keywords=company, max_results=max_results)


if __name__ == "__main__":
    results = asyncio.run(scrape_people_search("Software Engineer", 3, headless=False))
    import json
    print(json.dumps(results, indent=2))
