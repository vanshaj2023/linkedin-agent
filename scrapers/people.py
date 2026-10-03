import asyncio
from playwright.async_api import async_playwright
from browser.manager import get_authenticated_context, setup_page_stealth, safe_sleep, run_in_playwright_thread


async def _scrape_people_search_impl(keyword: str, max_results: int, headless: bool) -> list:
    results = []
    async with async_playwright() as p:
        context = await get_authenticated_context(p, headless=headless)
        page = await context.new_page()
        await setup_page_stealth(page)

        from urllib.parse import quote_plus
        url = (
            f"https://www.linkedin.com/search/results/people/"
            f"?keywords={quote_plus(keyword)}&origin=CLUSTER_EXPANSION"
        )
        await safe_sleep()
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        await page.wait_for_timeout(4000)

        # Scroll to load results
        for _ in range(4):
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight / 3)")
            await page.wait_for_timeout(1000)

        # Stamp each result row with a stable id so we can return Locators
        # regardless of which layout LinkedIn rendered (2026 layout uses
        # <li componentkey="…">, legacy uses li.reusable-search__result-container,
        # and the React rebuild uses div[data-chameleon-result-urn]). We walk
        # every /in/ profile link, climb to its result-row ancestor, dedupe,
        # and stamp.
        count = await page.evaluate("""() => {
            document.querySelectorAll('[data-scraper-people-id]').forEach(
                el => el.removeAttribute('data-scraper-people-id'));
            const seen = new Set();
            const rows = [];
            const links = document.querySelectorAll(
                'main a[href*="/in/"], div[role="main"] a[href*="/in/"]'
            );
            for (const a of links) {
                let el = a;
                for (let i = 0; i < 8; i++) {
                    el = el.parentElement;
                    if (!el || el.tagName === 'BODY') break;
                    if (seen.has(el)) break;
                    const isRow =
                        el.matches('li.reusable-search__result-container') ||
                        el.hasAttribute('data-chameleon-result-urn') ||
                        (el.tagName === 'LI' && el.hasAttribute('componentkey')) ||
                        el.matches('div.entity-result') ||
                        el.matches('div.linked-area');
                    if (isRow) {
                        seen.add(el);
                        rows.push(el);
                        break;
                    }
                }
            }
            rows.forEach((el, i) => el.setAttribute('data-scraper-people-id', String(i)));
            return rows.length;
        }""")

        containers = [
            page.locator(f'[data-scraper-people-id="{i}"]') for i in range(count)
        ]

        for container in containers:
            if len(results) >= max_results:
                break
            try:
                # Profile link is the most stable anchor — pick the first
                # /in/ link inside this row.
                link = container.locator("a[href*='/in/']").first
                if await link.count() == 0:
                    continue
                profile_url = await link.get_attribute("href") or ""
                profile_url = profile_url.split("?")[0]
                if "linkedin.com/in/" not in profile_url:
                    # Convert /in/<handle> → absolute URL
                    if profile_url.startswith("/in/"):
                        profile_url = "https://www.linkedin.com" + profile_url
                    else:
                        continue

                # Name: prefer aria-hidden span (deduped), fall back to link text.
                name = ""
                aria_span = link.locator("span[aria-hidden='true']").first
                if await aria_span.count() > 0:
                    name = (await aria_span.inner_text()).strip()
                if not name:
                    name = (await link.inner_text()).strip().split("\n")[0].strip()
                if not name or name.lower() in ("view profile", "linkedin member"):
                    name = "Unknown"

                # Headline & location: pull all "subtitle" rows. New layout uses
                # `.t-14.t-black--light` or similar; legacy uses
                # `.entity-result__primary-subtitle` and `__secondary-subtitle`.
                headline = ""
                location = ""
                for sel in (
                    "div.entity-result__primary-subtitle",
                    "div[class*='primary-subtitle']",
                    ".t-14.t-black",
                ):
                    el = container.locator(sel).first
                    if await el.count() > 0:
                        headline = (await el.inner_text()).strip()
                        break
                for sel in (
                    "div.entity-result__secondary-subtitle",
                    "div[class*='secondary-subtitle']",
                    ".t-14.t-normal",
                ):
                    el = container.locator(sel).first
                    if await el.count() > 0:
                        location = (await el.inner_text()).strip()
                        break

                results.append({
                    "name": name,
                    "linkedin_url": profile_url,
                    "headline": headline,
                    "location": location,
                })
            except Exception as e:
                print(f"Error scraping people result: {e}")

        await context.browser.close()

    # Deduplicate by linkedin_url (the JS walk may stamp the same row twice
    # if it contains two /in/ links — e.g. name + avatar).
    seen_urls: set[str] = set()
    deduped: list[dict] = []
    for r in results:
        if r["linkedin_url"] in seen_urls:
            continue
        seen_urls.add(r["linkedin_url"])
        deduped.append(r)
    return deduped


async def scrape_people_search(keyword: str = "Software Engineer", max_results: int = 10, headless: bool = True) -> list:
    return await run_in_playwright_thread(
        lambda: _scrape_people_search_impl(keyword, max_results, headless)
    )


async def search_people(keywords: str, max_results: int = 30) -> list:
    """Agent-facing wrapper. Returns normalised dicts with company field."""
    raw = await scrape_people_search(keyword=keywords, max_results=max_results, headless=True)
    normalised = []
    for r in raw:
        loc = r.get("location", "")
        company = loc.split("\u00b7")[0].strip() if "\u00b7" in loc else loc
        normalised.append({
            "name": r["name"],
            "headline": r.get("headline", ""),
            "company": company,
            "linkedin_url": r["linkedin_url"],
            "mutual_connections": 0,
        })
    return normalised


async def search_company_employees(company: str, max_results: int = 50) -> list:
    """Search for people currently at a specific company."""
    return await search_people(keywords=company, max_results=max_results)


if __name__ == "__main__":
    import json
    results = asyncio.run(_scrape_people_search_impl("Software Engineer", 3, headless=False))
    print(json.dumps(results, indent=2))
