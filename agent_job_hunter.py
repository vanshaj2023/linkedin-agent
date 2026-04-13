import asyncio
from datetime import datetime

from database import db
from system_health import CircuitBreaker, BudgetManager
from action_queue import ActionQueue
from slack_bot import send_job_alert
from job_scraper import scrape_jobs
from job_scorer import score_job_relevance

class JobHunterAgent:
    def __init__(self, target_roles: list, target_locations: list, client_profile: str, is_dry_run: bool = False):
        self.target_roles = target_roles
        self.target_locations = target_locations
        self.client_profile = client_profile
        self.is_dry_run = is_dry_run
        
    async def run(self):
        print(f"Starting Job Hunter Agent...")
        
        health = await CircuitBreaker.status()
        if health != "green":
            print(f"Agent Aborting: Circuit breaker is {health}.")
            return
            
        for role in self.target_roles:
            for location in self.target_locations:
                print(f"\nSearching for '{role}' in '{location}'...")
                
                # Fetch recent jobs
                jobs = await scrape_jobs(keyword=role, location=location, max_jobs=5, headless=True)
                
                for job in jobs:
                    # Deduplication check against DB
                    existing = await db.jobs.find_one({"linkedin_post_url": job["linkedin_post_url"]})
                    if existing:
                        continue
                        
                    print(f"Evaluating: {job['job_title']} at {job['company']}...")
                    
                    # Score post
                    eval_data = await score_job_relevance(
                        job_title=job["job_title"],
                        company=job["company"],
                        description=job["description"],
                        target_profile=self.client_profile
                    )
                    
                    score = eval_data.get("relevance_score", 0)
                    
                    # Update DB immediately
                    job_doc = {
                        "job_title": job["job_title"],
                        "company": job["company"],
                        "linkedin_post_url": job["linkedin_post_url"],
                        "poster_name": job["poster_name"],
                        "relevance_score": score,
                        "eval_reasoning": eval_data.get("reasoning"),
                        "scraped_at": datetime.utcnow()
                    }
                    if not self.is_dry_run:
                        await db.jobs.insert_one(job_doc)
                        
                    if score < 40:
                        print(f"Score {score} - Skipping.")
                        continue
                        
                    print(f"High Match ({score}/100)! Processing triggers...")
                    
                    # Slack Alert condition
                    if score >= 70:
                        await send_job_alert({**job, "relevance_score": score, "reasoning": eval_data.get("reasoning")})
                    
                    # Auto-comment / Email Routing
                    if eval_data.get("should_comment_email") and await BudgetManager.check_budget("comments"):
                        print(f"Poster asked for a comment. Queuing action...")
                        await ActionQueue.push(
                            agent="jobs",
                            action_type="comment",
                            payload={
                                "post_url": job["linkedin_post_url"],
                                "message": eval_data.get("comment_text", "Interested!")
                            },
                            priority=1, # Very high priority so we apply fast
                            is_dry_run=self.is_dry_run
                        )

async def main():
    agent = JobHunterAgent(
        target_roles=["Senior Python Engineer", "Backend Developer"],
        target_locations=["United States Remote"],
        client_profile="Senior Python / Backend Developer with 5 years of experience scaling Microservices with FastAPI, MongoDB, and Kubernetes.",
        is_dry_run=True
    )
    await agent.run()

if __name__ == "__main__":
    asyncio.run(main())
