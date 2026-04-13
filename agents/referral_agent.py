import datetime
import uuid
import inngest
from inngest_client import inngest_client
from database import db
from action_queue import ActionQueue
from system_health import CircuitBreaker
from people_scraper import search_company_employees
from llm_service import score_connection_profile, generate_connection_note
from mailer import send_referral_email
from slack_bot import send_referral_alert, send_alert
from config import config


@inngest_client.create_function(
    fn_id="referral-campaign-start",
    trigger=inngest.TriggerEvent(event="referral/campaign.start"),
    retries=1,
)
async def referral_campaign_start(ctx: inngest.Context, step: inngest.Step) -> dict:
    """
    Triggered by job_hunter_agent or the /referral Slack slash command.

    Phase 1 (Day 1-2): Discover company employees, score them, save campaign,
                        queue connection requests for batch 1 (15 people).
    Phase 2 (Day 3-4): After Inngest sleep, queue batch 2.
    Phase 3 (Day 5-7): After another sleep, queue batch 3.

    Each batch also adds targets to the Content Agent's engage_list so they
    get liked/commented automatically to warm them up before the referral ask.
    """
    company = ctx.event.data.get("company", "")
    target_role = ctx.event.data.get("target_role", "Software Engineer")
    job_post_url = ctx.event.data.get("job_post_url", "")
    campaign_id = str(uuid.uuid4())[:8]

    health = await step.run("check-cb", CircuitBreaker.status)
    if health == "red":
        return {"status": "skipped", "reason": "circuit_breaker_red"}

    # Phase 1: Discover + score employees
    raw_profiles = await step.run(
        "discover-employees",
        search_company_employees,
        company,
        50,
    )

    scored = []
    for p in raw_profiles:
        score = score_connection_profile(
            p["headline"], p["company"], p.get("mutual_connections", 0)
        )
        scored.append({**p, "score": score})
    scored.sort(key=lambda x: x["score"], reverse=True)
    top_targets = scored[:45]

    # Save campaign document to MongoDB
    campaign_doc = {
        "campaign_id": campaign_id,
        "company": company,
        "target_role": target_role,
        "job_post_url": job_post_url,
        "status": "active",
        "created_at": datetime.datetime.utcnow(),
        "targets": [
            {
                **t,
                "batch": (i // 15) + 1,
                "connection_status": "pending",
                "posts_liked": 0,
                "referral_email_sent": False,
                "referral_email_sent_at": None,
                "response_received": False,
                "notes": None,
            }
            for i, t in enumerate(top_targets)
        ],
    }
    await db.referral_campaigns.insert_one(campaign_doc)

    # Build Slack preview for batch 1
    batch1 = top_targets[:15]
    slack_candidates = [
        {
            **t,
            "headline": t.get("headline", ""),
            "connection_note": generate_connection_note(t["headline"], t.get("company", ""), "A"),
            "follow_up_message": (
                f"Following up on our connection — I'm interested in the {target_role} "
                f"role at {company} and would love your perspective."
            ),
        }
        for t in batch1
    ]
    await send_referral_alert(company, slack_candidates)

    # Batch 1 outreach (Day 1-2)
    await step.run(
        "queue-batch-1",
        _queue_batch_outreach,
        batch1,
        1,
        campaign_id,
        company,
    )

    # Sleep 2 days, then batch 2
    await step.sleep("wait-before-batch-2", datetime.timedelta(days=2))
    batch2 = top_targets[15:30]
    await step.run(
        "queue-batch-2",
        _queue_batch_outreach,
        batch2,
        2,
        campaign_id,
        company,
    )

    # Sleep 2 more days, then batch 3
    await step.sleep("wait-before-batch-3", datetime.timedelta(days=2))
    batch3 = top_targets[30:45]
    await step.run(
        "queue-batch-3",
        _queue_batch_outreach,
        batch3,
        3,
        campaign_id,
        company,
    )

    return {
        "status": "done",
        "campaign_id": campaign_id,
        "total_targets": len(top_targets),
        "dry_run": config.DRY_RUN,
    }


async def _queue_batch_outreach(
    targets: list, batch_num: int, campaign_id: str, company: str
) -> dict:
    """
    Queues view_profile + connect actions for one batch of targets and adds
    each target to the Content Agent's engage_list for ongoing warming.
    """
    queued = 0
    for t in targets:
        note = generate_connection_note(t["headline"], t.get("company", ""), "A")

        await ActionQueue.push(
            "referral", "view_profile",
            {"target_profile_url": t["linkedin_url"]},
            priority=1,
            is_dry_run=config.DRY_RUN,
        )
        await ActionQueue.push(
            "referral", "connect",
            {"target_profile_url": t["linkedin_url"], "message": note},
            priority=1,
            is_dry_run=config.DRY_RUN,
        )

        # Add to engage_list so Content Agent keeps warming them
        await db.engage_list.update_one(
            {"linkedin_url": t["linkedin_url"]},
            {
                "$setOnInsert": {
                    "linkedin_url": t["linkedin_url"],
                    "name": t["name"],
                    "reason": "referral_target",
                    "last_post_url": None,
                    "last_engaged_at": None,
                    "engagement_count": 0,
                    "auto_comment": True,
                    "added_by_agent": f"referral:{campaign_id}",
                }
            },
            upsert=True,
        )

        # Update campaign target status to "sent"
        await db.referral_campaigns.update_one(
            {"campaign_id": campaign_id, "targets.linkedin_url": t["linkedin_url"]},
            {"$set": {"targets.$.connection_status": "sent"}},
        )
        queued += 1

    return {"batch": batch_num, "queued": queued}


@inngest_client.create_function(
    fn_id="referral-on-connection-accepted",
    trigger=inngest.TriggerEvent(event="connection/accepted"),
    retries=1,
)
async def referral_on_connection_accepted(ctx: inngest.Context, step: inngest.Step) -> dict:
    """
    Fires whenever a connection request is accepted (emitted by the acceptance poller).
    If the person is in an active referral campaign:
      Day 0 — Content Agent already likes their posts (via engage_list)
      Day 1-2 — Content Agent comments (via engage_list + auto_comment)
      Day 3 — Send referral email via Gmail SMTP
    """
    linkedin_url = ctx.event.data.get("linkedin_url", "")
    name = ctx.event.data.get("name", "")

    # Check if this person is in an active referral campaign
    campaign = await db.referral_campaigns.find_one(
        {"status": "active", "targets.linkedin_url": linkedin_url}
    )
    if not campaign:
        return {"status": "not_in_campaign"}

    target_role = campaign.get("target_role", "Software Engineer")
    company = campaign.get("company", "")

    # Wait 3 days before the referral ask (content agent warms them in the meantime)
    await step.sleep("wait-3-days-before-email", datetime.timedelta(days=3))

    # Send referral email (LinkedIn doesn't expose emails — placeholder to_email)
    # In practice: you'd need to find their email via other means or use LinkedIn InMail
    email_sent = await step.run(
        "send-referral-email",
        send_referral_email,
        "",  # to_email — fill from your own contacts list or LinkedIn InMail
        name,
        company,
        target_role,
    )

    if email_sent:
        await db.referral_campaigns.update_one(
            {"_id": campaign["_id"], "targets.linkedin_url": linkedin_url},
            {
                "$set": {
                    "targets.$.connection_status": "accepted",
                    "targets.$.referral_email_sent": True,
                    "targets.$.referral_email_sent_at": datetime.datetime.utcnow(),
                }
            },
        )
        await send_alert(
            f"Referral email queued for {name} at {company} ({target_role}). DRY_RUN={config.DRY_RUN}"
        )

    return {"status": "done", "email_sent": email_sent, "name": name, "company": company}
