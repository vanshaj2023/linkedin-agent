import asyncio
import random
from datetime import datetime
from database import db, ActionQueueItem

class ActionQueue:
    @staticmethod
    async def push(agent: str, action_type: str, payload: dict, priority: int = 5, is_dry_run: bool = False):
        """Push a new action onto the central queue."""
        item = ActionQueueItem(
            agent=agent,
            action_type=action_type,
            payload=payload,
            priority=priority,
            dry_run=is_dry_run
        )
        
        result = await db.action_queue.insert_one(item.model_dump(by_alias=True))
        print(f"[{agent}] Queued action '{action_type}' (ID: {result.inserted_id})")
        return result.inserted_id

    @staticmethod
    async def get_next_action():
        """Pulls the next highest priority queued action."""
        # Find oldest, highest priority queued action
        item = await db.action_queue.find_one_and_update(
            {"status": "queued"},
            {"$set": {"status": "processing"}},
            sort=[("priority", 1), ("created_at", 1)],
            return_document=True
        )
        return item

    @staticmethod
    async def mark_done(action_id):
        """Mark action as successfully completed."""
        await db.action_queue.update_one(
            {"_id": action_id},
            {"$set": {"status": "done", "executed_at": datetime.utcnow()}}
        )

    @staticmethod
    async def mark_failed(action_id, error_msg: str, max_retries: int = 3):
        """Mark action as failed, or increment retry count and push back to queued."""
        item = await db.action_queue.find_one({"_id": action_id})
        if item:
            if item.get("retry_count", 0) < max_retries:
                await db.action_queue.update_one(
                    {"_id": action_id},
                    {
                        "$inc": {"retry_count": 1},
                        "$set": {"status": "queued", "error": error_msg}
                    }
                )
            else:
                await db.action_queue.update_one(
                    {"_id": action_id},
                    {
                        "$set": {"status": "failed", "error": error_msg, "executed_at": datetime.utcnow()}
                    }
                )

from system_health import CircuitBreaker, BudgetManager

# Map action_type to budget keys
BUDGET_MAP = {
    "connect": "connection_requests",
    "like": "likes",
    "comment": "comments",
    "view_profile": "profile_views",
    "search": "searches",
    "repost": "reposts"
}

# Example queue loop for orchestrator to consume from
async def processor_loop():
    print("Action queue processor started.")
    while True:
        # 1. Check Circuit Breaker
        health = await CircuitBreaker.status()
        if health == "red":
            print("System halted! Circuit breaker is RED. Sleeping for 5 minutes...")
            await asyncio.sleep(300)
            continue
            
        # 2. Check budgets for the next action we MIGHT pick
        # Since get_next_action doesn't peek, we pull it and if budget is blown, we defer it
        action = await ActionQueue.get_next_action()
        if not action:
            # Nothing in queue, chill.
            await asyncio.sleep(10)
            continue
            
        action_type = action["action_type"]
        budget_key = BUDGET_MAP.get(action_type)
        
        if budget_key:
            has_budget = await BudgetManager.check_budget(budget_key)
            if not has_budget:
                print(f"Budget for '{budget_key}' exhausted today. Deferring action {action['_id']}")
                # Push back with deferred status so a cron can reset them tomorrow
                await db.action_queue.update_one(
                    {"_id": action["_id"]},
                    {"$set": {"status": "deferred"}}
                )
                await asyncio.sleep(2)
                continue
                
        print(f"Processing action {action['_id']} ({action_type}) from {action['agent']}")
        try:
            # Here it would interface with Playwright / browser_manager
            # For now, simulate success
            await asyncio.sleep(2)
            
            # Increment budget and mark done
            if budget_key:
                await BudgetManager.increment_budget(budget_key)
                
            await ActionQueue.mark_done(action["_id"])
            print(f"Action {action['_id']} complete.")
        except Exception as e:
            await ActionQueue.mark_failed(action["_id"], str(e))
            print(f"Action {action['_id']} failed. Reason: {e}")
            # Potentially trip yellow/red circuit breaker here if consecutive errors mount up.
            
        # Hard rate limiting to prevent getting locked by LinkedIn
        # Adjust based on yellow status
        delay = random.uniform(5, 15)
        if health == "yellow":
            print("Circuit breaker is YELLOW. Enforcing doubled backoff delay.")
            delay *= 2
            
        await asyncio.sleep(delay)
