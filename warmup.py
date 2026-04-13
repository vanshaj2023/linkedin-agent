import datetime
from database import db, DailyBudgets, DailyBudgetLimit

WARMUP_SCHEDULE = {
    1: {"connections": 5, "likes": 10, "views": 15, "comments": 2},
    2: {"connections": 12, "likes": 25, "views": 40, "comments": 5},
    3: {"connections": 20, "likes": 45, "views": 70, "comments": 8},
    4: {"connections": 25, "likes": 60, "views": 80, "comments": 10},
}

async def apply_warmup_budget(week: int = 1):
    """
    Overwrites today's daily budget limit bounds based on the warmup week.
    This should be run daily at midnight by a cron job or just before processing starts.
    """
    if week > 4:
        week = 4
        
    config = WARMUP_SCHEDULE[week]
    today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    
    # Ensure Record exists
    record = await db.daily_budgets.find_one({"date": today_str})
    if not record:
        budget = DailyBudgets(
            date=today_str,
            connection_requests=DailyBudgetLimit(limit=config["connections"]),
            profile_views=DailyBudgetLimit(limit=config["views"]),
            likes=DailyBudgetLimit(limit=config["likes"]),
            comments=DailyBudgetLimit(limit=config["comments"]),
            reposts=DailyBudgetLimit(limit=3),
            searches=DailyBudgetLimit(limit=30)
        )
        await db.daily_budgets.insert_one(budget.model_dump(by_alias=True))
        print(f"Initialized Day {today_str} on Warmup Week {week}")
    else:
        # Update existing
        await db.daily_budgets.update_one(
            {"date": today_str},
            {"$set": {
                "connection_requests.limit": config["connections"],
                "profile_views.limit": config["views"],
                "likes.limit": config["likes"],
                "comments.limit": config["comments"],
            }}
        )
        print(f"Updated Day {today_str} with limits for Warmup Week {week}")
