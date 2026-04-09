"""
scheduler.py
------------
Runs every day at RUN_HOUR (default 10 AM), picks the next PROFILES_PER_DAY
profiles from like/profile.json, likes their posts, then sleeps until the
next day. Cycles back to the start when the end of the list is reached.

Usage:
    python scheduler.py          # runs forever, daily at 10:00 AM
    python scheduler.py --now    # skip the wait and run the batch immediately
"""

import asyncio
import json
import os
import sys
from datetime import datetime, date, timedelta

# ── Config ────────────────────────────────────────────────────────────────────
RUN_HOUR        = 10   # 10 AM  (change to e.g. 22 for 10 PM)
RUN_MINUTE      = 0
PROFILES_PER_DAY = 20
WAIT_BETWEEN_PROFILES_SEC = 120   # 2 minutes
# ──────────────────────────────────────────────────────────────────────────────

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright
import browser_manager
from interactions import _like_activity_on_page

LIKE_DIR      = os.path.dirname(os.path.abspath(__file__))
PROFILE_JSON  = os.path.join(LIKE_DIR, "like", "profile.json")
PROGRESS_JSON = os.path.join(LIKE_DIR, "like", "progress.json")


# ── Persistence helpers ───────────────────────────────────────────────────────

def load_profiles():
    with open(PROFILE_JSON, "r") as f:
        return json.load(f)


def load_progress():
    if os.path.exists(PROGRESS_JSON):
        with open(PROGRESS_JSON, "r") as f:
            return json.load(f)
    return {"current_index": 0, "last_run_date": None}


def save_progress(data: dict):
    with open(PROGRESS_JSON, "w") as f:
        json.dump(data, f, indent=2)


# ── Timing helpers ────────────────────────────────────────────────────────────

def today_run_time() -> datetime:
    """Returns today's scheduled run datetime (RUN_HOUR:RUN_MINUTE)."""
    now = datetime.now()
    return now.replace(hour=RUN_HOUR, minute=RUN_MINUTE, second=0, microsecond=0)


def next_run_time() -> datetime:
    """Returns the next future scheduled run datetime."""
    target = today_run_time()
    if datetime.now() >= target:
        target += timedelta(days=1)
    return target


async def sleep_until(target_dt: datetime):
    """Sleep until target_dt, printing a countdown every minute."""
    while True:
        remaining = (target_dt - datetime.now()).total_seconds()
        if remaining <= 0:
            break
        if remaining > 60:
            print(f"  Sleeping... next run at {target_dt.strftime('%Y-%m-%d %H:%M:%S')} "
                  f"({remaining/3600:.1f}h remaining)", end="\r")
            await asyncio.sleep(60)
        else:
            await asyncio.sleep(remaining)
    print()  # newline after \r


# ── Core daily batch ──────────────────────────────────────────────────────────

async def run_daily_batch():
    profiles = load_profiles()
    if not profiles:
        print("No profiles found in profile.json. Nothing to do.")
        return

    total    = len(profiles)
    progress = load_progress()
    start    = progress["current_index"] % total   # wrap if list shrank

    # Build today's batch (wrap around end of list)
    batch = [profiles[(start + i) % total] for i in range(PROFILES_PER_DAY)]
    end_index = (start + PROFILES_PER_DAY) % total

    print(f"\n{'='*55}")
    print(f"  Daily batch  —  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total profiles : {total}")
    print(f"  Starting index : {start}  (profile #{start + 1})")
    print(f"  Batch size     : {len(batch)}")
    print(f"{'='*55}\n")

    async with async_playwright() as p:
        context = await browser_manager.get_authenticated_context(p, headless=False)
        page    = await context.new_page()

        for i, profile_url in enumerate(batch, start=1):
            print(f"\n[{i}/{len(batch)}] {profile_url}")
            await _like_activity_on_page(page, profile_url)

            if i < len(batch):
                print(f"\nWaiting {WAIT_BETWEEN_PROFILES_SEC // 60} min before next profile "
                      f"(browser stays open)...")
                for elapsed in range(0, WAIT_BETWEEN_PROFILES_SEC, 10):
                    remaining = WAIT_BETWEEN_PROFILES_SEC - elapsed
                    print(f"  {remaining}s remaining...   ", end="\r")
                    await asyncio.sleep(10)
                print(f"  Done waiting. Moving to next profile.         ")

        await context.browser.close()

    # Persist progress
    progress["current_index"] = end_index
    progress["last_run_date"] = date.today().isoformat()
    save_progress(progress)

    print(f"\nBatch done. Next batch starts at index {end_index} (profile #{end_index + 1}).")


# ── Scheduler loop ────────────────────────────────────────────────────────────

async def main(run_now: bool = False):
    print("LinkedIn Auto-Liker Scheduler")
    print(f"  Scheduled time : {RUN_HOUR:02d}:{RUN_MINUTE:02d} daily")
    print(f"  Profiles/day   : {PROFILES_PER_DAY}")
    print(f"  Profile list   : {PROFILE_JSON}")
    print(f"  Progress file  : {PROGRESS_JSON}\n")

    while True:
        progress = load_progress()
        today_str = date.today().isoformat()

        if run_now:
            run_now = False   # only skip the wait once
        elif progress["last_run_date"] == today_str:
            # Already ran today — wait until tomorrow
            target = next_run_time()
            print(f"Already ran today ({today_str}). "
                  f"Next run: {target.strftime('%Y-%m-%d %H:%M:%S')}")
            await sleep_until(target)
        else:
            # Haven't run today yet
            target = today_run_time()
            if datetime.now() < target:
                print(f"Waiting until today's run time: {target.strftime('%H:%M:%S')}")
                await sleep_until(target)
            # else: it's already past run time today and we haven't run — run now

        await run_daily_batch()


if __name__ == "__main__":
    run_now = "--now" in sys.argv
    asyncio.run(main(run_now=run_now))
