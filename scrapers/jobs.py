import asyncio
from playwright.async_api import async_playwright
from browser.manager import get_authenticated_context, setup_page_stealth, safe_sleep, run_in_playwright_thread


async def _scrape_jobs_impl(keyword: str, location: str, max_jobs: int, headless: bool) -> list:
    results = []
    async with async_playwright() as p:
        context = await get_authenticated_context(p, headless=headless)
        page = await context.new_page()
        await setup_page_stealth(page)

        url = (
            f"https://www.linkedin.com/jobs/search/"
            f"?keywords={keyword}&location={location}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON"
        )
        await safe_sleep()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # The list container moved from `.jobs-search-results-list` (legacy) to
        # `.scaffold-layout__list-container` on the 2025/2026 layout. Wait for
        # either, whichever this account renders.
        try:
            await page.wait_for_selector(
                ".jobs-search-results-list, ul.scaffold-layout__list-container",
                state="visible", timeout=15000,
            )
        except Exception:
            pass
        await page.wait_for_timeout(3000)

        # Scroll the list pane to force lazy-loaded cards into the DOM. Direct
        # JS scroll on the container is more reliable than focus+PageDown,
        # which fails silently when the click target doesn't exist.
        list_pane = page.locator(
            "ul.scaffold-layout__list-container, .jobs-search-results-list"
        ).first
        for _ in range(4):
            try:
                if await list_pane.count() > 0:
                    await list_pane.evaluate(
                        "el => el.scrollBy(0, el.clientHeight)"
                    )
                else:
                    await page.evaluate("window.scrollBy(0, 800)")
            except Exception:
                await page.evaluate("window.scrollBy(0, 800)")
            await page.wait_for_timeout(1200)

        job_cards = await page.locator(
            "div.job-card-container, li.scaffold-layout__list-item"
        ).all()

        for card in job_cards:
            if len(results) >= max_jobs:
                break
            try:
                await card.click()
                await page.wait_for_timeout(1500)

                title_el = page.locator(
                    ".job-details-jobs-unified-top-card__job-title, "
                    ".t-24.t-bold, h1.t-24"
                ).first
                title = (await title_el.inner_text()).strip() if await title_el.count() > 0 else "Unknown Title"

                company_el = page.locator(
                    ".job-details-jobs-unified-top-card__company-name a, "
                    ".job-details-jobs-unified-top-card__primary-description a"
                ).first
                company = (await company_el.inner_text()).strip() if await company_el.count() > 0 else "Unknown"

                link_el = page.locator("a.job-card-list__title, a.job-card-container__link").first
                post_url = await link_el.get_attribute("href")
                if post_url:
                    post_url = post_url.split("?")[0]
                    if post_url.startswith("/jobs/"):
                        post_url = "https://www.linkedin.com" + post_url

                desc_el = page.locator("#job-details, .jobs-description__content").first
                description = (await desc_el.inner_text())[:3000] if await desc_el.count() > 0 else ""

                poster_el = page.locator(".hirer-card__hirer-information .app-aware-link").first
                poster = ""
                poster_url = None
                if await poster_el.count() > 0:
                    poster = (await poster_el.inner_text()).strip()
                    href = await poster_el.get_attribute("href")
                    if href:
                        poster_url = (
                            "https://www.linkedin.com" + href
                            if href.startswith("/in/")
                            else href.split("?")[0]
                        )
                else:
                    name_el = page.locator(".hirer-card__hirer-information span").first
                    if await name_el.count() > 0:
                        poster = (await name_el.inner_text()).strip()

                if post_url:
                    results.append({
                        "job_title": title,
                        "company": company,
                        "linkedin_post_url": post_url,
                        "description": description,
                        "poster_name": poster,
                        "poster_url": poster_url,
                        "poster_text": "",
                    })
            except Exception as e:
                print(f"Error scraping job: {e}")

        await context.browser.close()

    return results


async def scrape_jobs(keyword: str, location: str = "United States", max_jobs: int = 5, headless: bool = True) -> list:
    return await run_in_playwright_thread(
        lambda: _scrape_jobs_impl(keyword, location, max_jobs, headless)
    )


async def search_jobs(keywords: str, location: str = "", max_results: int = 20) -> list:
    """Agent-facing wrapper."""
    loc = location if location else "Remote"
    return await scrape_jobs(keyword=keywords, location=loc, max_jobs=max_results, headless=True)


if __name__ == "__main__":
    jobs = asyncio.run(_scrape_jobs_impl("Python Developer", "Remote", 2, headless=False))
    print(jobs)
