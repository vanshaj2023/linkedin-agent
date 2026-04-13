import asyncio
from playwright.async_api import async_playwright
import browser_manager

async def scrape_jobs(keyword: str, location: str = "United States", max_jobs: int = 5, headless: bool = True):
    """
    Search for jobs on LinkedIn and scrape the titles, companies, and descriptions.
    """
    results = []
    
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=headless)
        page = await context.new_page()
        await browser_manager.setup_page_stealth(page)
        
        url = f"https://www.linkedin.com/jobs/search/?keywords={keyword}&location={location}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON"
        print(f"Navigating to job search: {url}")
        
        await browser_manager.safe_sleep()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        
        # Job cards are usually inside 'li.jobs-search-results__list-item' 
        # or '.job-card-container'
        
        # Scroll down left pane to load a few jobs
        try:
            await page.locator('.jobs-search-results-list').click()
            for _ in range(3):
                await page.keyboard.press('PageDown')
                await page.wait_for_timeout(1000)
        except Exception:
            pass

        job_cards = await page.locator("div.job-card-container").all()
        print(f"Found {len(job_cards)} job cards.")
        
        for card in job_cards:
            if len(results) >= max_jobs:
                break
                
            try:
                # Click the card to load it into the right pane
                await card.click()
                await page.wait_for_timeout(1500)
                
                # Wait for the right pane to load the title
                title_locator = page.locator(".job-details-jobs-unified-top-card__job-title, .t-24.t-bold").first
                title = await title_locator.inner_text() if await title_locator.count() > 0 else "Unknown Title"
                title = title.strip()
                
                # Company name
                company_locator = page.locator(".job-details-jobs-unified-top-card__company-name a, .job-details-jobs-unified-top-card__primary-description a").first
                company = await company_locator.inner_text() if await company_locator.count() > 0 else "Unknown Company"
                company = company.strip()
                
                # Post URL
                link_locator = page.locator("a.job-card-list__title, a.job-card-container__link").first
                post_url = await link_locator.get_attribute("href")
                if post_url:
                    post_url = post_url.split("?")[0]
                    if post_url.startswith("/jobs/"):
                        post_url = "https://www.linkedin.com" + post_url
                
                # Raw description
                desc_locator = page.locator("#job-details, .jobs-description__content")
                description = await desc_locator.inner_text() if await desc_locator.count() > 0 else ""
                
                # "Posted by" note (sometimes present if a recruiter posted it)
                poster_locator = page.locator(".hirer-card__hirer-information span")
                poster = await poster_locator.inner_text() if await poster_locator.count() > 0 else ""

                if post_url:
                    results.append({
                        "job_title": title,
                        "company": company,
                        "linkedin_post_url": post_url,
                        "description": description[:3000],  # Limit length for LLM context
                        "poster_name": poster.strip()
                    })
                    
            except Exception as e:
                print(f"Error scraping a job: {e}")
                
        await context.browser.close()
        
    return results

async def search_jobs(keywords: str, location: str = "", max_results: int = 20) -> list:
    """
    Alias used by agents. Wraps scrape_jobs with standard field names.
    Returns list of dicts: {job_title, company, linkedin_post_url, description, poster_name, poster_text}
    """
    loc = location if location else "Remote"
    raw = await scrape_jobs(keyword=keywords, location=loc, max_jobs=max_results, headless=True)
    # Add missing poster_text field (not extracted by base scraper)
    for job in raw:
        job.setdefault("poster_text", "")
    return raw


if __name__ == "__main__":
    jobs = asyncio.run(scrape_jobs("Python Developer", "Remote", 2, headless=False))
    print(jobs)
