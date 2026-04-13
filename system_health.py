import datetime
from database import db, SystemHealth, DailyBudgets

class CircuitBreaker:
    @staticmethod
    async def status():
        """Returns the current system health status."""
        health = await db.system_health.find_one({"_id": "circuit_breaker"})
        if not health:
            # Initialize if missing
            await db.system_health.insert_one(SystemHealth().model_dump(by_alias=True))
            return "green"
            
        # Check if we should auto-resume
        if health["status"] in ["yellow", "red"] and health.get("auto_resume_at"):
            if datetime.datetime.utcnow() >= health["auto_resume_at"]:
                await CircuitBreaker.reset()
                return "green"
                
        return health["status"]

    @staticmethod
    async def trip(level: str, reason: str, auto_resume_hours: int = None):
        """
        Trip the circuit breaker to 'yellow' or 'red'.
        Red stops the entire system.
        """
        updates = {
            "status": level,
            "triggered_at": datetime.datetime.utcnow(),
            "reason": reason
        }
        if auto_resume_hours:
            updates["auto_resume_at"] = datetime.datetime.utcnow() + datetime.timedelta(hours=auto_resume_hours)
        else:
            updates["auto_resume_at"] = None
            
        await db.system_health.update_one(
            {"_id": "circuit_breaker"},
            {"$set": updates},
            upsert=True
        )
        print(f"CRITICAL: Circuit breaker tripped to {level.upper()}! Reason: {reason}")

    @staticmethod
    async def reset():
        """Force reset the circuit breaker back to green."""
        await db.system_health.update_one(
            {"_id": "circuit_breaker"},
            {"$set": {"status": "green", "auto_resume_at": None, "reason": "Manually or Auto Reset"}}
        )
        print("System health reset to green.")

class BudgetManager:
    @staticmethod
    async def _get_today():
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        record = await db.daily_budgets.find_one({"date": today_str})
        if not record:
            # Initialize based on warm-up configuration (default values in schema for now)
            # In Phase 6, this would dynamically read from a warm-up schedule
            new_budget = DailyBudgets(date=today_str).model_dump(by_alias=True)
            await db.daily_budgets.insert_one(new_budget)
            return new_budget
        return record

    @staticmethod
    async def check_budget(action_key: str) -> bool:
        """
        Checks if we have budget left for a specific action today.
        action_key should be: 'connection_requests', 'profile_views', 'likes', 'comments', 'reposts', or 'searches'
        """
        today = await BudgetManager._get_today()
        budget = today.get(action_key, {})
        used = budget.get("used", 0)
        limit = budget.get("limit", 1)
        return used < limit

    @staticmethod
    async def increment_budget(action_key: str):
        """Increments the used count for an action by 1."""
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        await db.daily_budgets.update_one(
            {"date": today_str},
            {"$inc": {f"{action_key}.used": 1}},
            upsert=True
        )
