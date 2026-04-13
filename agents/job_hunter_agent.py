import datetime
import inngest
from inngest_client import inngest_client
from database import db
from action_queue import ActionQueue
from system_health import CircuitBreaker
from job_scraper import search_jobs
from llm_service import score_job_post
from slack_bot import send_job_alert, send_alert
from config import config


@inngest_client.create_function(
    fn_id="job-hunter-run",
    trigger=inngest.TriggerCron(cron="0 8,13,19 * * *"),  # 3x daily
    retries=2,
)
async def job_hunter_run(ctx: inngest.Context, step: inngest.Step) -> dict:
    """
    3x daily: search LinkedIn jobs → LLM score each → Slack notify high matches
    → auto-comment on posts that ask for email → trigger Referral Agent for
    companies where score >= 80.
    """
    health = await step.run("check-cb", CircuitBreaker.status)
    if health == "red":
        return {"status": "skipped", "reason": "circuit_breaker_red"}

    all_jobs = []
    for keyword in config.TARGET_JOB_KEYWORDS[:2]:
        for location in config.TARGET_JOB_LOCATIONS[:2]:
            jobs = await step.run(
                f"search-jobs-{keyword.replace(' ', '_')}-{location.replace(' ', '_')}",
                search_jobs,
                keyword,
                location,
                10,
            )
            all_jobs.extend(jobs)

    notified = 0
    for job in all_jobs:
        # Skip already processed
        existing = await db.jobs.find_one({"linkedin_post_url": job["linkedin_post_url"]})
        if existing:
            continue

        # LLM scoring
        score_data = score_job_post(
            title=job["job_title"],
            company=job["company"],
            description=job.get("description", ""),
            poster_text=job.get("poster_text", ""),
        )
        relevance_score = score_data.get("relevance_score", 0)
        action_taken = "none"
        slack_ts = None

        # Slack notify for high-relevance jobs
        if relevance_score >= config.JOB_SLACK_NOTIFY_THRESHOLD:
            slack_ts = await send_job_alert({**job, **score_data})
            action_taken = "slack_notified"
            notified += 1

        # Auto-comment if poster asked for email/DM
        if score_data.get("should_comment_email") and score_data.get("comment_text"):
            await ActionQueue.push(
                "job_hunter", "comment",
                {"post_url": job["linkedin_post_url"], "message": score_data["comment_text"]},
                priority=2,
                is_dry_run=config.DRY_RUN,
            )
            action_taken = "commented"

        # Auto-trigger Referral Agent for very high matches
        if score_data.get("company_for_referral") and relevance_score >= 80:
            await inngest_client.send(
                inngest.Event(
                    name="referral/campaign.start",
                    data={
                        "company": score_data["company_for_referral"],
                        "job_post_url": job["linkedin_post_url"],
                        "target_role": job["job_title"],
                        "source": "job_hunter",
                    },
                )
            )
            action_taken = "referral_triggered"

        # Persist to jobs collection
        await db.jobs.insert_one(
            {
                "linkedin_post_url": job["linkedin_post_url"],
                "job_title": job["job_title"],
                "company": job["company"],
                "poster_name": job.get("poster_name", ""),
                "relevance_score": relevance_score,
                "action_taken": action_taken,
                "comment_text": score_data.get("comment_text"),
                "slack_message_ts": slack_ts,
                "reasoning": score_data.get("reasoning", ""),
                "discovered_at": datetime.datetime.utcnow(),
                "applied": False,
                "applied_at": None,
            }
        )

    return {"status": "done", "notified": notified, "total_found": len(all_jobs)}
