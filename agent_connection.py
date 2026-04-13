import asyncio
import datetime
from people_scraper import scrape_people_search
from llm_scorer import score_and_generate_note
from system_health import CircuitBreaker, BudgetManager
from database import db, Connection
from action_queue import ActionQueue

class ConnectionAgent:
    def __init__(self, target_keyword: str, target_domain: str, is_dry_run: bool = False):
        self.target_keyword = target_keyword
        self.target_domain = target_domain
        self.is_dry_run = is_dry_run
        
    async def run(self):
        print(f"Starting Connection Agent [Target: {self.target_keyword}]")
        
        # 1. Check Circuit Breaker
        health = await CircuitBreaker.status()
        if health != "green":
            print(f"Agent Aborting: Circuit breaker is {health}.")
            return
            
        # Check overall budget for connecting before scraping
        has_budget = await BudgetManager.check_budget("connection_requests")
        if not has_budget:
            print("Agent Aborting: Connection request budget reached for today.")
            return

        # 2. Scrape Profiles
        print("Searching for potential connections...")
        # Scrape headless natively
        profiles = await scrape_people_search(keyword=self.target_keyword, max_results=20, headless=True)
        print(f"Scraped {len(profiles)} raw profiles.")
        
        for profile in profiles:
            url = profile["linkedin_url"]
            name = profile["name"]
            
            if not url:
                continue
                
            # 3. Deduplication Check
            existing = await db.connections.find_one({"linkedin_url": url})
            if existing:
                print(f"Skipping {name} - already exists in system.")
                continue
                
            # 4. LLM Scoring
            print(f"Scoring {name}...")
            evaluation = await score_and_generate_note(
                name=name,
                headline=profile["headline"],
                company=profile["location"],
                target_domain=self.target_domain
            )
            
            score = evaluation["score"]
            if score < 70:
                print(f"Skipping {name} - relevance score too low ({score}/100)")
                continue
                
            print(f"Match found! {name} scored {score}/100.")
            
            # 5. Save to DB as 'identified' first
            db_conn = Connection(
                linkedin_url=url,
                name=name,
                headline=profile["headline"],
                company=profile["location"],
                status="request_sent", # It will be sent via queue
                source_agent="connection",
                relevance_score=score,
                personalization_note=evaluation["note"],
                tags=[self.target_keyword]
            )
            await db.connections.update_one(
                {"linkedin_url": url}, 
                {"$setOnInsert": db_conn.model_dump(by_alias=True)},
                upsert=True
            )
            
            # 6. Push to Action Queue
            # Push a view first
            await ActionQueue.push(
                agent="connection",
                action_type="view_profile",
                payload={"target_profile_url": url},
                priority=3,
                is_dry_run=self.is_dry_run
            )
            # Push the actual connect request slightly lower priority so the view happens first
            await ActionQueue.push(
                agent="connection",
                action_type="connect",
                payload={"target_profile_url": url, "message": evaluation["note"]},
                priority=4,
                is_dry_run=self.is_dry_run
            )

        print("Connection Agent run complete.")

if __name__ == "__main__":
    agent = ConnectionAgent(
        target_keyword="Python Developer",
        target_domain="Python Backend Engineering and Distributed Systems",
        is_dry_run=True  # Dry run by default for testing
    )
    asyncio.run(agent.run())
