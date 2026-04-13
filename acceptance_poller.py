import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
import browser_manager
from database import db

async def scrape_connections(headless=True):
    """
    Navigates to the My Network -> Connections page and scrapes the URLs of recent connections.
    """
    results = []
    
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=headless)
        page = await context.new_page()
        await browser_manager.setup_page_stealth(page)
        
        # Sort by recently added
        url = "https://www.linkedin.com/mynetwork/invite-connect/connections/"
        print(f"Navigating to connections page: {url}")
        
        await browser_manager.safe_sleep()
        await page.goto(url)
        await page.wait_for_timeout(5000)
        
        # Scroll down to load recent ones (we don't need to load the entire history, just the top ~100)
        for _ in range(4):
            await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            await page.wait_for_timeout(1000)
            
        # The list items for connections
        containers = await page.locator("li.mn-connection-card").all()
        print(f"Found {len(containers)} connections on page.")
        
        for container in containers:
            try:
                link_locator = container.locator("a.mn-connection-card__link").first
                profile_url = await link_locator.get_attribute("href")
                if profile_url:
                    profile_url = profile_url.split("?")[0] # clean params
                    # ensure absolute URL if relative
                    if profile_url.startswith("/in/"):
                        profile_url = "https://www.linkedin.com" + profile_url
                    results.append(profile_url)
            except Exception as e:
                print(f"Error scraping a connection: {e}")
                
        await context.browser.close()
        
    return results

async def poll_acceptances(is_dry_run=False):
    print("Starting Acceptance Poller...")
    
    # 1. Get all pending connections from DB
    cursor = db.connections.find({"status": "request_sent"})
    pending_urls = []
    async for doc in cursor:
        pending_urls.append(doc["linkedin_url"])
        
    if not pending_urls:
        print("No pending requests in database. Exiting poller.")
        return
        
    print(f"Tracking {len(pending_urls)} pending requests.")
    
    # 2. Scrape recent connections
    recent_connection_urls = await scrape_connections(headless=True)
    
    # Simple normalization for matching (ignore trailing slashes)
    recent_connection_urls_norm = [u.rstrip('/') for u in recent_connection_urls]
    
    accepted_count = 0
    # 3. Cross-reference
    for pending_url in pending_urls:
        norm_pending_url = pending_url.rstrip('/')
        if norm_pending_url in recent_connection_urls_norm:
            print(f"Detected accepted request from: {pending_url}")
            accepted_count += 1
            if not is_dry_run:
                await db.connections.update_one(
                    {"linkedin_url": pending_url},
                    {"$set": {
                        "status": "accepted",
                        "connected_at": datetime.utcnow()
                    }}
                )
                
    print(f"Poller finished. Found {accepted_count} newly accepted connections.")

if __name__ == "__main__":
    asyncio.run(poll_acceptances(is_dry_run=True))
