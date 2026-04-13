import asyncio
from datetime import datetime, timedelta

from database import db, Connection
from system_health import CircuitBreaker, BudgetManager
from action_queue import ActionQueue
from slack_bot import send_referral_alert
from referral_scraper import scrape_company_employees
from referral_scorer import generate_referral_sequence

class ReferralAgent:
    def __init__(self, client_profile: str, is_dry_run: bool = False):
        self.client_profile = client_profile
        self.is_dry_run = is_dry_run

    async def initialize_campaign(self, target_company: str, target_roles: list):
        """SUB-TASK A: Launch a new campaign for a targeted company."""
        print(f"Launching Referral Campaign for '{target_company}'...")
        
        health = await CircuitBreaker.status()
        if health != "green":
            print("Circuit breaker active, aborting.")
            return
            
        if not await BudgetManager.check_budget("connection_requests"):
            print("No connection request budget today. Aborting.")
            return

        employees = await scrape_company_employees(target_company, target_roles, max_results=3, headless=True)
        
        campaign_logs = []
        for emp in employees:
            existing = await db.connections.find_one({"linkedin_url": emp["linkedin_url"]})
            if existing: # Avoid hitting people we already know or contacted
                continue
                
            messages = await generate_referral_sequence(
                target_name=emp["name"],
                headline=emp["headline"],
                company=target_company,
                matched_role=emp["matched_role"],
                client_profile=self.client_profile
            )
            
            campaign_logs.append({
                **emp,
                **messages
            })
            
            # Save to db
            conn_doc = Connection(
                linkedin_url=emp["linkedin_url"],
                name=emp["name"],
                headline=emp["headline"],
                company=target_company,
                status="request_sent",
                source_agent="referral",
                personalization_note=messages["connection_note"],
                drip_followup_message=messages["follow_up_message"],
                drip_day2_sent=False
            )
            
            if not self.is_dry_run:
                await db.connections.update_one(
                    {"linkedin_url": emp["linkedin_url"]}, 
                    {"$setOnInsert": conn_doc.model_dump(by_alias=True)},
                    upsert=True
                )
                
            # Queue the connect action
            await ActionQueue.push(
                agent="referral",
                action_type="connect",
                payload={"target_profile_url": emp["linkedin_url"], "message": messages["connection_note"]},
                priority=2, # high priority
                is_dry_run=self.is_dry_run
            )
            
        # Send slack summary of campaign
        if campaign_logs:
            await send_referral_alert(target_company, campaign_logs)

    async def process_drips(self):
        """SUB-TASK B: Send follow-ups to people who have accepted our Day 1 connection."""
        print("Processing Referral Follow-ups (Day 2)...")
        
        # Find connections that are accepted, from the referral agent, but haven't got the followup
        cursor = db.connections.find({
            "status": "accepted",
            "source_agent": "referral",
            "drip_day2_sent": False,
            "drip_followup_message": {"$exists": True, "$ne": None}
        })
        
        async for conn in cursor:
            # Enforce that we wait ~24 hours after they accepted
            accepted_at = conn.get("connected_at")
            if not accepted_at or datetime.utcnow() - accepted_at < timedelta(hours=20):
                continue
                
            if not await BudgetManager.check_budget("messages"):
                continue

            print(f"Queueing Day 2 Follow up message for {conn['name']}")
            
            message = conn["drip_followup_message"]
            
            await ActionQueue.push(
                agent="referral",
                action_type="message",
                payload={"target_profile_url": conn["linkedin_url"], "message": message},
                priority=2,
                is_dry_run=self.is_dry_run
            )
            
            if not self.is_dry_run:
                await db.connections.update_one(
                    {"_id": conn["_id"]},
                    {"$set": {"drip_day2_sent": True}}
                )

async def main():
    agent = ReferralAgent(
        client_profile="Senior Python Engineer looking to join a high-growth remote startup.",
        is_dry_run=True
    )
    # Example usage (usually triggered by Job Hunter or slack slash commands)
    await agent.initialize_campaign("Anthropic", ["Software Engineer", "Machine Learning Engineer"])
    
    # Run the drip processor (usually via a cron schedule)
    await agent.process_drips()

if __name__ == "__main__":
    asyncio.run(main())
