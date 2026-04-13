# LinkedIn Automation System — Implementation Plan

## System Overview

A multi-agent LinkedIn automation platform with four core agents (Connection, Job Hunter, Content, Referral) orchestrated through Inngest, backed by MongoDB for state management, and integrated with Slack for notifications and your existing mailer for outreach.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    INNGEST SCHEDULER                     │
│         (cron triggers + event-driven steps)             │
└──────┬──────────┬──────────┬──────────┬─────────────────┘
       │          │          │          │
   Connection  Job Hunter  Content   Referral
    Agent        Agent      Agent     Agent
       │          │          │          │
       └──────────┴──────────┴──────────┘
                      │
              ┌───────▼────────┐
              │  CENTRAL ACTION │
              │     QUEUE       │
              │  (rate-limited) │
              └───────┬────────┘
                      │
              ┌───────▼────────┐
              │   PLAYWRIGHT    │
              │  (stealth mode) │
              │  + proxy layer  │
              └───────┬────────┘
                      │
                  LinkedIn
                      │
       ┌──────────────┼──────────────┐
       │              │              │
    MongoDB        Slack API     Your Mailer
   (all state)   (notifications) (referral emails)
```

---

## Critical Infrastructure (Build This First)

Before touching any agent logic, these foundational layers must be in place. Every agent depends on them.

### 1. Central Action Queue

This is the single most important piece. All four agents push actions here; nothing touches LinkedIn directly.

**Why it matters:** LinkedIn detects bots by cross-action velocity. If your Connection agent sends 5 requests while your Content agent likes 10 posts simultaneously, that's a red flag even with per-action delays.

**MongoDB Collection: `action_queue`**
```js
{
  _id: ObjectId,
  agent: "connection" | "job_hunter" | "content" | "referral",
  action_type: "connect" | "like" | "comment" | "view_profile" | "search" | "repost",
  payload: {
    target_profile_url: String,
    message: String,        // for connection notes or comments
    post_url: String,       // for likes/reposts/comments
  },
  priority: 1-5,            // 1 = highest (referral engagement), 5 = lowest (feed reactions)
  status: "queued" | "processing" | "done" | "failed" | "deferred",
  created_at: Date,
  executed_at: Date,
  retry_count: Number,
  error: String,
  dry_run: Boolean
}
```

**Queue Processor (Inngest cron — every 3–5 minutes):**
- Check circuit breaker health flag → if tripped, exit immediately
- Check daily budget counters → if any limit hit, defer remaining actions
- Pull next action by priority (oldest first within same priority)
- Execute via Playwright with random delay (2–8 sec before, 1–4 sec after)
- Log result, update status
- Add random "idle browse" actions between real actions (scroll feed, view a random profile) to mimic human behavior

**Daily Budget Counters — Collection: `daily_budgets`**
```js
{
  date: "2026-04-14",
  connection_requests: { used: 12, limit: 25 },
  profile_views: { used: 45, limit: 80 },
  likes: { used: 30, limit: 60 },
  comments: { used: 3, limit: 10 },
  reposts: { used: 1, limit: 3 },
  searches: { used: 8, limit: 30 }
}
```

Reset counters at midnight via an Inngest cron. Start with conservative limits and only increase after 2+ weeks of stable operation.

### 2. Session & Proxy Management

**Session Persistence:**
- Store cookies in MongoDB (or a local encrypted file) after each successful session
- On each Playwright launch, load cookies first → check if session is alive → only login if expired
- Never log in more than once per day; treat a forced re-login as a soft warning signal

**Proxy Rotation:**
- Use residential proxies (BrightData, Oxylabs, or IPRoyal)
- Stick to ONE proxy IP per session (don't rotate mid-session — LinkedIn fingerprints this)
- Rotate proxy only on new session or after a cool-down period
- Keep a pool of 5-10 IPs minimum; track which IP was used when

**Playwright Stealth Setup:**
```bash
# Required packages
npm install playwright-extra puppeteer-extra-plugin-stealth
```
- Use `playwright-extra` with stealth plugin
- Randomize viewport size slightly (1280–1440 width, 720–900 height)
- Randomize user-agent from a curated realistic list (update monthly)
- Add mouse movement jitter — don't click-teleport, simulate cursor paths
- Randomize typing speed for messages (80–160ms per character)

### 3. Circuit Breaker

**MongoDB Collection: `system_health`**
```js
{
  _id: "circuit_breaker",
  status: "green" | "yellow" | "red",
  triggered_at: Date,
  reason: String,
  auto_resume_at: Date       // null if manual intervention needed
}
```

**Triggers:**
- CAPTCHA detected → status = "red", halt everything, Slack alert
- Login failure → status = "red", halt, Slack alert
- 3+ action failures in a row → status = "yellow", reduce rate by 50%
- "Unusual activity" page → status = "red", halt for 24h minimum
- Any HTTP 429 → status = "yellow", back off for 1 hour

**Every agent and the queue processor check this BEFORE any action.** No exceptions.

### 4. Warm-Up Protocol

For new accounts or accounts that haven't been automated before:

| Week | Daily Connections | Daily Likes | Profile Views | Comments |
|------|:-:|:-:|:-:|:-:|
| 1 | 3–5 | 5–10 | 10–15 | 1–2 |
| 2 | 8–12 | 15–25 | 25–40 | 3–5 |
| 3 | 15–20 | 30–45 | 50–70 | 5–8 |
| 4+ | 20–25 | 40–60 | 70–80 | 8–10 |

Store current warm-up week in MongoDB. The budget system reads from this to set dynamic limits.

---

## Agent 1: Connection Agent

**Trigger:** Inngest cron — twice daily (morning + evening, randomized ±30 min)

**Flow:**
1. Check circuit breaker → exit if not green
2. Run LinkedIn people search for your target keywords/domain
3. For each result:
   - Check MongoDB `connections` collection → skip if already contacted
   - Check daily budget → stop if connection limit reached
   - Score relevance (headline match, mutual connections, activity level)
   - If score > threshold → generate personalized note via LLM
   - Push to central action queue: `{ action_type: "view_profile" }` then `{ action_type: "connect", message: note }`
   - Save to `connections` collection with status "request_sent"

**MongoDB Collection: `connections`**
```js
{
  linkedin_url: String,
  name: String,
  headline: String,
  company: String,
  status: "identified" | "request_sent" | "accepted" | "declined" | "message_sent",
  source_agent: "connection" | "referral",
  relevance_score: Number,
  personalization_note: String,
  connected_at: Date,
  first_contacted_at: Date,
  last_action_at: Date,
  tags: [String]              // e.g., ["target_company", "hiring_manager"]
}
```

**Personalization (LLM Prompt Pattern):**
```
Given this person's headline: "{headline}"
And their latest post topic: "{post_summary}"
Write a 280-character connection note that:
- References something specific about their work
- Mentions a shared interest in {your_domain}
- Sounds casual and human, not salesy
- Does NOT ask for anything in the first message
```

Keep 5-8 note templates and rotate. A/B test acceptance rates per template (store which template was used in the connection record).

### Connection Acceptance Poller

**Trigger:** Inngest cron — every 6 hours

**Flow:**
1. Scrape your LinkedIn connections list (or "My Network" page)
2. Cross-reference against `connections` where status = "request_sent"
3. For newly accepted connections → update status to "accepted"
4. Emit Inngest event `connection.accepted` with the connection data
5. Other agents (especially Referral) listen for this event to trigger next steps

---

## Agent 2: Job Hunter Agent

**Trigger:** Inngest cron — 3x daily (morning, midday, evening)

**Flow:**
1. Check circuit breaker
2. Search LinkedIn jobs for your target roles, locations, keywords
3. For each job post:
   - Check MongoDB `jobs` collection → skip if already processed
   - Extract: company, role, poster, post text, date, application link
   - Send to AI decision layer for scoring and action routing

**AI Decision Layer (LLM call per job post):**
```
Analyze this job post and respond with JSON:
{
  "relevance_score": 0-100,
  "should_comment_email": boolean,
  "comment_text": "string or null",
  "reasoning": "why this score",
  "company_for_referral": "string or null"
}

Job Post:
Title: {title}
Company: {company}
Description: {description}
Poster's note: {poster_text}
```

**Routing Logic:**
- `relevance_score >= 70` → push to Slack with full details
- `should_comment_email == true` → queue a comment action with your email/note
- `company_for_referral != null` AND score >= 80 → optionally auto-trigger Referral Agent for that company
- `relevance_score < 40` → log and skip silently

**MongoDB Collection: `jobs`**
```js
{
  linkedin_post_url: String,
  job_title: String,
  company: String,
  poster_name: String,
  relevance_score: Number,
  action_taken: "none" | "commented" | "slack_notified" | "referral_triggered",
  comment_text: String,
  slack_message_ts: String,    // for threading follow-ups
  discovered_at: Date,
  applied: Boolean,
  applied_at: Date
}
```

**Slack Notification Format:**
```
🎯 *New Relevant Job* (Score: 85/100)
*Role:* Senior Backend Engineer
*Company:* Stripe
*Posted by:* Jane Doe (Engineering Manager)
*Why it matched:* Node.js + distributed systems + your experience level
*Link:* [View Post](url)
*Actions:* [Mark Applied] [Trigger Referral] [Dismiss]
```

Use Slack interactive buttons so you can trigger the Referral Agent or mark jobs as applied directly from Slack.

---

## Agent 3: Content Agent

### Sub-task A: Repost Suggestions

**Trigger:** Inngest cron — twice daily

**Flow:**
1. Scan LinkedIn feed (scroll + extract posts matching your domain keywords)
2. For each post, score on:
   - Author relevance (are they in your network? industry leader?)
   - Content quality (length, engagement count, topic match)
   - Engagement velocity (how fast is it gaining likes/comments?)
   - Recency (prefer posts < 6 hours old for maximum repost value)
3. Posts scoring above threshold → send to Slack as a digest

**Slack Digest Format:**
```
📢 *Repost Suggestions — Morning Digest*

1. [Score: 92] @SarahK — "Why microservices aren't always the answer..."
   Engagement: 234 likes, 45 comments in 3hrs
   [Repost Now] [Skip]

2. [Score: 78] @DevOpsDaily — "The hidden cost of Kubernetes..."
   Engagement: 89 likes, 12 comments in 5hrs
   [Repost Now] [Skip]
```

**Auto-repost mode:** If score >= your auto_repost_threshold (configurable, default 90), repost immediately and notify you after the fact. Otherwise, wait for your Slack approval.

### Sub-task B: Auto-Reactions

**Trigger:** Inngest cron — 3x daily, spread across the day

**Flow:**
1. Pull your "engage list" from MongoDB — people you want to stay visible to
2. For each person, check when you last engaged with their content
3. If > 24 hours since last engagement AND they have a new post → queue a like
4. If > 72 hours AND they have a new post with a good hook → queue a thoughtful comment (LLM-generated)

**MongoDB Collection: `engage_list`**
```js
{
  linkedin_url: String,
  name: String,
  reason: "referral_target" | "hiring_manager" | "industry_peer" | "recruiter",
  last_post_url: String,
  last_engaged_at: Date,
  engagement_count: Number,    // total likes/comments you've given
  auto_comment: Boolean,       // allow auto-comments or just likes
  added_by_agent: String       // which agent added them
}
```

**Important:** The Referral Agent automatically adds people to this engage list. This creates the engagement loop — you connect with someone, then the Content Agent keeps liking their posts so you stay visible before the referral ask.

---

## Agent 4: Referral Agent

**Trigger:** Manual (via Slack command or API call) OR automatic (from Job Hunter when a high-score job is found)

**Input:** Company name + optional target team/role filter

**Flow — Phase 1: Discovery**
1. Search LinkedIn for people at `{company}` filtered by relevant roles
2. Collect 30–50 profiles (paginate search results)
3. Score each by: role relevance, connection degree, activity level, seniority
4. Sort by score, take top 30–50
5. Store all in `referral_campaigns` collection

**Flow — Phase 2: Outreach (spread over 5–7 days)**

Day 1–2: Send connection requests to batch 1 (10–15 people)
- Personalized note mentioning shared domain interest (NOT asking for referral yet)
- Add each person to the Content Agent's engage list

Day 3–4: Send connection requests to batch 2
- Like 1–2 posts from batch 1 people (even if not yet accepted)
- Continue engaging with any batch 1 who accepted

Day 5–7: Send connection requests to batch 3
- Continue liking posts from batches 1 & 2
- For accepted connections from batch 1: enqueue in your mailer for referral email

**MongoDB Collection: `referral_campaigns`**
```js
{
  campaign_id: String,
  company: String,
  target_role: String,         // the job you want a referral for
  job_post_url: String,
  status: "active" | "paused" | "completed",
  created_at: Date,
  targets: [{
    linkedin_url: String,
    name: String,
    role: String,
    score: Number,
    batch: 1 | 2 | 3,
    connection_status: "pending" | "sent" | "accepted" | "declined",
    posts_liked: Number,
    referral_email_sent: Boolean,
    referral_email_sent_at: Date,
    response_received: Boolean,
    notes: String
  }]
}
```

**Event-Driven Transitions:**
- When `connection.accepted` event fires (from Acceptance Poller) AND the person is in an active referral campaign → wait 48–72 hours → enqueue referral email in your mailer
- The delay is crucial — you don't want to connect and immediately ask for a referral

**Referral Email Timing:**
```
Connection accepted
    → Day 0: Like 1-2 of their posts
    → Day 1-2: Comment on one post (genuine, not salesy)
    → Day 3: Send referral email via your mailer
```

This spacing makes the referral request feel natural, not transactional.

---

## Slack Integration Hub

Your Slack workspace becomes the control center for the entire system.

**Channels:**
| Channel | Purpose |
|---|---|
| `#job-alerts` | Job Hunter sends relevant posts here |
| `#repost-suggestions` | Content Agent sends repost candidates |
| `#referral-campaigns` | Status updates on referral campaign progress |
| `#system-health` | Circuit breaker alerts, budget warnings, errors |

**Slack Commands (via Slack bot or slash commands):**
- `/referral Stripe` → trigger Referral Agent for Stripe
- `/status` → show current daily budget usage, circuit breaker status
- `/pause` → pause all agents immediately
- `/resume` → resume agents
- `/dry-run on|off` → toggle dry-run mode

---

## Dry-Run Mode

**Purpose:** Test the entire pipeline without touching LinkedIn.

When `dry_run: true` in system config:
- All agents run their full logic (search, score, decide)
- Actions are logged to MongoDB with `dry_run: true` flag
- Playwright launches but skips the actual click/submit step
- Slack notifications are sent with a `[DRY RUN]` prefix

Run in dry-run mode for at least 3-5 days before going live. Review:
- Are the right people being targeted?
- Are LLM-generated messages natural?
- Are job relevance scores calibrated?
- Are rate limits being respected?

---

## Reputation & Learning System

**MongoDB Collection: `reputation_scores`**
```js
{
  linkedin_url: String,
  acceptance_rate: Number,           // did they accept connection?
  response_rate: Number,             // did they respond to messages?
  referral_conversion: Boolean,      // did they give a referral?
  engagement_reciprocity: Number,    // do they engage back with your content?
  outreach_template_used: String,    // which template worked
  company: String,
  role_type: String,
  updated_at: Date
}
```

**Feedback Loop:**
- After 2-4 weeks of data, analyze which templates get higher acceptance rates
- Analyze which company sizes / role types respond better
- Feed aggregate stats back into the LLM prompt so it learns your patterns:
  ```
  Historical context: Connection notes mentioning specific projects
  have a 34% acceptance rate vs 18% for generic domain mentions.
  Adjust your tone accordingly.
  ```

---

## Implementation Order

Build in this exact sequence. Each phase depends on the previous one.

### Phase 1: Foundation (Week 1–2)
- [ ] Set up MongoDB collections (all schemas above)
- [ ] Build Playwright stealth wrapper (session persistence, proxy rotation, random delays)
- [ ] Build central action queue + queue processor
- [ ] Build circuit breaker system
- [ ] Build daily budget counter system
- [ ] Set up Slack bot with channels and basic commands (`/status`, `/pause`)
- [ ] Implement dry-run mode toggle
- [ ] Deploy warm-up configuration

### Phase 2: Connection Agent (Week 3)
- [ ] LinkedIn people search scraper
- [ ] Deduplication logic against `connections` collection
- [ ] LLM-powered personalization for connection notes
- [ ] A/B template rotation system
- [ ] Connection acceptance poller
- [ ] Integration with central action queue
- [ ] Test in dry-run mode for 3+ days

### Phase 3: Content Agent (Week 4)
- [ ] Feed scanner with keyword matching
- [ ] Post scoring algorithm
- [ ] Repost suggestion → Slack digest pipeline
- [ ] Auto-reaction system with engage list
- [ ] Slack interactive buttons for approve/skip
- [ ] Test in dry-run mode for 3+ days

### Phase 4: Job Hunter Agent (Week 5)
- [ ] LinkedIn job search scraper
- [ ] AI decision layer (relevance scoring, comment detection)
- [ ] Slack notification with interactive buttons
- [ ] Auto-comment queue for email-request posts
- [ ] Slack → Referral Agent trigger integration
- [ ] Test in dry-run mode for 3+ days

### Phase 5: Referral Agent (Week 6–7)
- [ ] Company employee search + collection
- [ ] Batch splitting logic (3 batches over 5–7 days)
- [ ] Auto-add to Content Agent's engage list
- [ ] Event listener for `connection.accepted`
- [ ] Delayed referral email trigger (connect with your existing mailer)
- [ ] Campaign tracking dashboard in Slack
- [ ] Test with ONE real company in dry-run mode first

### Phase 6: Hardening & Learning (Week 8+)
- [ ] Reputation tracking system
- [ ] Template A/B test analysis
- [ ] Gradually increase warm-up limits
- [ ] Monitor circuit breaker triggers and tune sensitivity
- [ ] Build weekly analytics digest (Slack or a simple dashboard)
- [ ] Fine-tune LLM prompts based on real conversion data

---

## Risk Mitigation Checklist

- [ ] **Secondary account for dev/testing** — never test automation on your primary LinkedIn
- [ ] **Residential proxies active** — datacenter IPs get flagged instantly
- [ ] **playwright-extra stealth plugin** — bare Playwright is detectable
- [ ] **Action volumes are human-like** — no more than 1 action per 2-3 minutes on average
- [ ] **Session reuse** — not logging in fresh every run
- [ ] **No parallel browser sessions** — one session at a time, always
- [ ] **Circuit breaker tested** — simulate a CAPTCHA and verify all agents halt
- [ ] **Dry-run validated** — full pipeline tested without real actions for 3+ days
- [ ] **Daily budget never exceeded** — even if queue is full, actions defer to next day
- [ ] **Random off-hours** — don't run automation at 3 AM; schedule during realistic working hours (8 AM–10 PM with gaps)

---

## Tech Stack Summary

| Component | Tool |
|---|---|
| Browser automation | Playwright + playwright-extra + stealth plugin |
| Scheduling & orchestration | Inngest (cron + event-driven) |
| State management | MongoDB |
| AI/LLM layer | LangChain + Groq (or Claude API for complex decisions) |
| Notifications & control | Slack (webhooks + interactive messages + slash commands) |
| Proxy management | BrightData / Oxylabs / IPRoyal (residential) |
| Email outreach | Your existing mailer system |
| Semantic matching (optional) | Pinecone for job relevance / profile matching |

---

## Key Numbers to Track

| Metric | Target | Track In |
|---|---|---|
| Connection acceptance rate | > 30% | MongoDB + weekly Slack digest |
| Referral response rate | > 10% | MongoDB `referral_campaigns` |
| Job relevance accuracy | > 80% of Slack-sent jobs are actually relevant | Manual review weekly |
| Circuit breaker triggers | 0 per week (after tuning) | `system_health` collection |
| Daily budget utilization | 70–90% (not maxing out, not wasting capacity) | `daily_budgets` collection |
| Template A/B winner | Statistically significant after 50+ sends | `connections` + `reputation_scores` |