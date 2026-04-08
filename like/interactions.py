import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright
import browser_manager
async def react_to_post(post_url: str):
    """
    Navigates to a specific post URL and clicks the 'Like' button.
    """
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=False)
        page = await context.new_page()
        
        print(f"\nNavigating to post to React: {post_url}")
        await page.goto(post_url)
        
        # Give the post time to load
        await page.wait_for_timeout(3000)
        
        try:
            # LinkedIn now uses aria-label="Reaction button state: no reaction" for unliked posts
            # and aria-label="Reaction button state: Like" for already-liked posts.
            like_button_locator = page.locator("button[aria-label='Reaction button state: no reaction']").first

            if await like_button_locator.count() > 0:
                print("Found Like button. Clicking it...")
                await like_button_locator.click()
                print("Success: Reacted to post.")
            else:
                already_liked = await page.locator("button[aria-label='Reaction button state: Like']").count()
                if already_liked > 0:
                    print("Post is already liked.")
                else:
                    print("Could not find the Like button.")
        except Exception as e:
            print(f"Failed to react: {e}")
            
        await page.wait_for_timeout(2000)
        await context.browser.close()

async def comment_on_post(post_url: str, comment_text: str):
    """
    Navigates to a specific post URL, types a comment, and posts it.
    """
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=False)
        page = await context.new_page()
        
        print(f"\nNavigating to post to Comment: {post_url}")
        await page.goto(post_url)
        
        await page.wait_for_timeout(3000)
        
        try:
            # Find the comment box. It uses a specific editor class or aria-label 'Add a comment...'
            comment_box = page.locator("div[role='textbox'][aria-label*='comment'], div.ql-editor").first
            
            if await comment_box.count() > 0:
                print("Found comment box. Typing comment...")
                await comment_box.click()
                
                # Type human-like
                await page.keyboard.type(comment_text, delay=50)
                await page.wait_for_timeout(1000)
                
                # Click the submit/Post button
                import re
                
                # The actual submit button is a primary button (blue) that says "Comment" or "Post".
                # The main comment action toggle on the post is a ghost/secondary button, so we filter by primary.
                submit_button = page.locator("button.artdeco-button--primary:has-text('Comment'), button.artdeco-button--primary:has-text('Post')").first
                
                # Check if it was found
                if await submit_button.count() > 0:
                    # HUMAN IN THE LOOP WAIT
                    input(f"\n[HITL] Ready to post comment: '{comment_text}'. Press Enter to post, or Ctrl+C to cancel.")
                    await submit_button.click()
                    print("Success: Comment posted.")
                else:
                    print("Could not find the Post button in the UI.")
                    with open("debug_comment.html", "w", encoding="utf-8") as f:
                        f.write(await page.content())
                    print("DEBUG: Saved raw HTML to debug_comment.html")
            else:
                print("Could not find the comment entry box.")
        except Exception as e:
            print(f"Failed to comment: {e}")
            
        await page.wait_for_timeout(2000)
        await context.browser.close()

async def send_connection_request(profile_url: str, note_text: str = None):
    """
    Navigates to a LinkedIn profile and sends a connection request with an optional note.
    """
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=False)
        page = await context.new_page()
        
        print(f"\nNavigating to profile to Connect: {profile_url}")
        await page.goto(profile_url)
        
        await page.wait_for_timeout(3000)
        
        try:
            import re
            main_container = page.locator("main").first
            
            # Use Playwright's strict accessible naming to beat the obfuscated DOM.
            # Look for either a button explicitly named "Connect" or with the aria-label "Invite <name> to connect".
            connect_btn = main_container.get_by_role("button", name=re.compile(r"^(Connect|Invite .* to connect)$", re.IGNORECASE)).first
            
            try:
                # Wait up to 8 seconds for the Connect button to dynamically render
                await connect_btn.wait_for(state="visible", timeout=8000)
            except Exception:
                pass # It's okay if it times out, it might be in the 'More' menu or not available
                
            if await connect_btn.count() == 0:
                print("Connect button not instantly visible. Checking 'More' menu in profile...")
                # The "More actions" button in the profile header
                more_btn = main_container.get_by_role("button", name=re.compile(r"More", re.IGNORECASE)).first
                if await more_btn.count() > 0:
                    await more_btn.click()
                    await page.wait_for_timeout(1000)
                    # The dropdown menu is usually attached to the body or main, not necessarily inside top_section
                    # Look for the exact menu item that says Connect
                    connect_btn = page.locator("div[role='dialog'], div[role='menu']").get_by_role("menuitem", name=re.compile(r"Connect", re.IGNORECASE)).first
                    if await connect_btn.count() == 0:
                        # Fallback for weird dropdowns
                        connect_btn = page.locator("div[role='dialog'], div[role='menu']").locator("div, span").filter(has_text=re.compile(r"^Connect$")).first

            if await connect_btn.count() > 0:
                print("Found Connect button. Clicking...")
                await connect_btn.click()
                await page.wait_for_timeout(2000)
                
                # Now a modal usually pops up asking to add a note or send.
                if note_text:
                    add_note_btn = page.locator("button[aria-label='Add a note']").first
                    if await add_note_btn.count() > 0:
                        await add_note_btn.click()
                        await page.wait_for_timeout(500)
                        
                        textarea = page.locator("textarea[name='message']").first
                        await textarea.fill(note_text)
                        await page.wait_for_timeout(1000)
                
                # Check if we can find any send button
                send_btn = page.locator("button[aria-label='Send without a note'], button[aria-label='Send now'], button[aria-label='Send'], button:has-text('Send')").last
                
                # Try to save HTML for debugging
                with open("debug_connect.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())
                print("DEBUG: Saved raw HTML to debug_connect.html")
                
                # HUMAN IN THE LOOP WAIT
                input(f"\n[HITL] Ready to send connection request to {profile_url}. Press Enter to send, or Ctrl+C to cancel.")
                
                await send_btn.click()
                print("Success: Connection request sent.")
            else:
                print("Could not find a way to connect to this user.")
        except Exception as e:
            print(f"Failed to connect: {e}")
            try:
                with open("debug_connect_error.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())
                print("DEBUG: Saved raw HTML to debug_connect_error.html")
            except:
                pass
            
        await page.wait_for_timeout(2000)
        await context.browser.close()

async def view_user_activity(profile_url: str):
    """
    Navigates to a LinkedIn profile, scrolls to the Activity section,
    and clicks 'Show all' to view the user's posts/activity.
    """
    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=False)
        page = await context.new_page()
        
        print(f"\nNavigating to profile: {profile_url}")
        await page.goto(profile_url)
        
        # Give the profile page some initial time to load
        await page.wait_for_timeout(3000)
        
        try:
            print("Scrolling to find the Activity section...")
            import re
            
            # Scroll down slowly to let sections render dynamically
            for i in range(6):
                await page.evaluate("window.scrollBy(0, 500)")
                await page.wait_for_timeout(1000)
                
            # Usually, LinkedIn uses an h2 tag for the "Activity" section header.
            # We look for something containing the text "Activity"
            activity_heading = page.locator("h2, span").filter(has_text=re.compile(r"^Activity$", re.IGNORECASE)).first
            
            if await activity_heading.count() > 0:
                print("Found Activity section!")
                await activity_heading.scroll_into_view_if_needed()
                await page.wait_for_timeout(1000)
                
                # In modern LinkedIn, the "Show all ->" button is an anchor with an href containing 'recent-activity'.
                # Specifically, it includes text like "Show all [X] posts" or just "Show all"
                show_all_btn = page.locator("a[href*='recent-activity']").filter(has_text=re.compile(r"Show all", re.IGNORECASE)).first
                
                # Fallback if the href structure changed but text is similar
                if await show_all_btn.count() == 0:
                    show_all_btn = page.locator("a:has-text('Show all'), button:has-text('Show all')").first
                    
                if await show_all_btn.count() > 0:
                    print("Found 'Show all' button. Clicking it...")
                    await show_all_btn.click()
                    print("Success: Navigated to user's full activity page.")
                    
                    # Giving it a second to load the new feed so the user can verify
                    await page.wait_for_timeout(4000)
                    
                    print("\n--- Starting Auto-React Mode ---")
                    liked_count = 0
                    last_height = 0
                    stale_steps = 0  # consecutive steps with no new content

                    for step in range(50):
                        print(f"Scroll Step {step+1}...")

                        # Like all currently-loaded unliked posts first
                        unliked = page.locator("button[aria-label='Reaction button state: no reaction']")
                        already_liked_count = await page.locator("button[aria-label='Reaction button state: Like']").count()
                        count = await unliked.count()
                        print(f"  -> Unliked: {count} | Already liked: {already_liked_count}")

                        for _ in range(count):
                            try:
                                btn = unliked.first
                                if await btn.count() == 0:
                                    break
                                await btn.evaluate("""node => {
                                    node.scrollIntoView({behavior: 'instant', block: 'center'});
                                    node.click();
                                }""")
                                liked_count += 1
                                print(f"     Liked post #{liked_count}!")
                                await page.wait_for_timeout(1500)
                            except Exception as e:
                                print(f"     [error] {e}")

                        # Slow scroll — small steps with long pauses so LinkedIn's
                        # infinite scroll has time to detect the position and fetch more posts
                        for _ in range(6):
                            await page.evaluate("window.scrollBy(0, 400)")
                            await page.wait_for_timeout(1200)

                        # Extra wait after scroll for LinkedIn to render newly fetched posts
                        await page.wait_for_timeout(2500)

                        # End-of-feed detection: only stop after 3 consecutive steps
                        # with no height change AND no new unliked posts found
                        new_height = await page.evaluate("document.body.scrollHeight")
                        new_unliked = await page.locator("button[aria-label='Reaction button state: no reaction']").count()
                        if new_height == last_height and new_unliked == 0:
                            stale_steps += 1
                            print(f"  -> No new content ({stale_steps}/3 stale steps).")
                            if stale_steps >= 3:
                                print("  -> Reached end of feed, stopping.")
                                break
                        else:
                            stale_steps = 0
                        last_height = new_height
                        
                    print(f"\n--- Finished! Successfully liked {liked_count} new posts. ---")
                else:
                    print("Could not find the 'Show all' button in the Activity section.")
            else:
                print("Could not find the Activity heading. The user might not have recent activity visible, or we need to scroll further.")
                with open("debug_activity.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())
                print("DEBUG: Saved raw HTML to debug_activity.html")
                
        except Exception as e:
            print(f"Failed to view activity: {e}")
            
        await page.wait_for_timeout(2000)
        await context.browser.close()

if __name__ == "__main__":
    import sys
    # For testing: pass a post URL and test reaction
    # python interactions.py react "https://www.linkedin.com/feed/update/urn:li:activity:XXX"
    if len(sys.argv) > 2:
        action = sys.argv[1]
        url = sys.argv[2]
        
        if action == "react":
            asyncio.run(react_to_post(url))
        elif action == "comment" and len(sys.argv) > 3:
            asyncio.run(comment_on_post(url, sys.argv[3]))
        elif action == "connect":
            asyncio.run(send_connection_request(url, sys.argv[3] if len(sys.argv) > 3 else None))
        elif action == "activity":
            asyncio.run(view_user_activity(url))
