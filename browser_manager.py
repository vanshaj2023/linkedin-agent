import os
import json
import random
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from playwright_stealth import stealth_async

STATE_FILE = "state.json"

# Reasonable user agents for stealth
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

def get_random_viewport():
    return {
        "width": random.randint(1280, 1440),
        "height": random.randint(720, 900)
    }

async def get_authenticated_context(p, headless: bool = True) -> BrowserContext:
    """
    Launches a browser with stealth plugins, randomized user-agent, and viewport.
    """
    # E.g., read proxy from environment if proxy rotation needed per session
    proxy_url = os.getenv("PROXY_URL", None)
    
    launch_options = {
        "headless": headless,
        "args": ["--disable-blink-features=AutomationControlled"]
    }
    
    if proxy_url:
        launch_options["proxy"] = {"server": proxy_url}

    browser = await p.chromium.launch(**launch_options)
    
    user_agent = random.choice(USER_AGENTS)
    viewport = get_random_viewport()
    
    context_options = {
        "user_agent": user_agent,
        "viewport": viewport,
        "locale": "en-US",
        "timezone_id": "America/New_York",
    }
    
    if os.path.exists(STATE_FILE):
        print(f"Loading cached session from {STATE_FILE}...")
        context_options["storage_state"] = STATE_FILE
        
    context = await browser.new_context(**context_options)
    
    # Check if we didn't have state
    if not os.path.exists(STATE_FILE):
        print("No cached session found. You may need to run login.py first.")
        
    return context

async def setup_page_stealth(page: Page):
    """
    Applies stealth scripts and prepares page for human-like interaction.
    """
    await stealth_async(page)
    return page

async def human_type(page: Page, selector: str, text: str):
    """
    Types text with randomized delay between 80-160ms.
    """
    for char in text:
        await page.type(selector, char, delay=random.randint(80, 160))

async def human_click(page: Page, selector: str):
    """
    Hovers first to simulate mouse movement, randomizes click offset, then clicks.
    """
    element = page.locator(selector).first
    box = await element.bounding_box()
    if box:
        # Hover at a random offset within the element
        x = box["x"] + random.uniform(5, box["width"] - 5)
        y = box["y"] + random.uniform(5, box["height"] - 5)
        await page.mouse.move(x, y, steps=10)
        await asyncio.sleep(random.uniform(0.1, 0.4))
        await page.mouse.move(x, y, steps=2)
    
    await element.click(delay=random.randint(50, 150))

async def safe_sleep():
    """
    Random delay to use before/after critical actions (2-8s as per plan.md).
    """
    await asyncio.sleep(random.uniform(2.0, 8.0))

# Tester
async def test_manager():
    async with async_playwright() as p:
        context = await get_authenticated_context(p, headless=False)
        page = await context.new_page()
        await setup_page_stealth(page)
        
        print("Navigating to LinkedIn feed...")
        await safe_sleep()
        await page.goto("https://www.linkedin.com/feed/")
        
        if "login" in page.url or "checkpoint" in page.url:
            print("WARNING: We are not logged in or hit a checkpoint! Run login.py again.")
        else:
            print("Successfully loaded the feed using stealth + cached credentials!")
            
        await page.close()
        await context.browser.close()

if __name__ == "__main__":
    asyncio.run(test_manager())
