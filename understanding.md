# Understanding This Project — In Plain English

This document explains what this project is, what it does, and why each piece
exists. It's written for someone non-technical, or for an engineer new to the
codebase who wants the "big picture" before reading the code.

---

## What is this project?

It's a **personal robot for LinkedIn**. The owner of the system is a person
looking for a job, who wants to grow their network, find good roles, get
referrals into companies, and stay visible on the platform — but doesn't want
to spend two hours a day clicking through LinkedIn manually.

So this project is a small staff of AI-powered "assistants" that do those
chores in the background. They run on a schedule, they're careful not to look
like a bot, and they ask the owner (through Slack) before doing anything
risky.

Think of it as: **"an autonomous LinkedIn intern that texts you on Slack."**

---

## Who is it for? Why does it exist?

LinkedIn rewards consistency, but consistency is exhausting. The reality:

- To get noticed, you have to **like and comment** on the right people's
  posts every few days, so you stay top-of-mind.
- To get referrals, you have to **find the right people** at a target
  company and reach out without sounding spammy.
- To find jobs, you have to **scroll LinkedIn jobs three times a day** so
  you catch good roles before they get 1,000 applicants.
- To get back to people, you have to **track conversations** across DMs,
  connection acceptances, and email.

If you do all this manually for two months while job hunting, you burn out.
If you write a bot to do it carelessly, LinkedIn flags your account and
bans you.

This project tries to do the middle thing: **act like a thoughtful human, on
schedule, with brakes.** Specifically:

- It only does a few actions per day (not hundreds).
- It pauses itself the moment LinkedIn shows any sign of suspicion.
- It runs every important decision past you in Slack.
- It has a "dry run" mode where it tells you what it would have done,
  without actually doing it.

---

## How does it work? The 10,000-foot view

There are basically five moving parts:

```
   ┌─ THE BRAIN (Inngest scheduler) ──┐
   │  Runs each assistant on a clock  │
   └──────────────┬───────────────────┘
                  │
   ┌──────────────▼─────────────────┐
   │  FIVE ASSISTANTS               │
   │  Each one watches LinkedIn for │
   │  a different opportunity       │
   └──────────────┬─────────────────┘
                  │
                  │  They don't touch LinkedIn directly.
                  │  They write "I want to do X" tickets to:
                  │
   ┌──────────────▼─────────────────┐
   │  THE QUEUE                     │
   │  Single line of pending actions│
   │  Sorted by priority            │
   └──────────────┬─────────────────┘
                  │
                  │  A worker picks one ticket every few minutes,
                  │  checks budget + safety, then:
                  │
   ┌──────────────▼─────────────────┐
   │  THE HANDS                     │
   │  A real Chrome browser that    │
   │  logs into LinkedIn (looking   │
   │  human) and clicks things      │
   └──────────────┬─────────────────┘
                  │
   ┌──────────────▼─────────────────┐
   │  THE CONTROL PANEL             │
   │  Slack — sends you updates,    │
   │  asks for approval, lets you   │
   │  pause everything              │
   └────────────────────────────────┘
```

Everything written to LinkedIn flows through that single queue, by design,
so the safety brakes can apply to every action regardless of which assistant
initiated it.

---

## The Five Assistants (called "agents")

Each is a separate Python file under `agents/`. Each runs on its own clock
and does one job.

### 1. The Connection Agent — *"Grow my network."*

**When it runs:** Twice a day, 9 AM and 6 PM.

**What it does:**
- Searches LinkedIn for people whose job titles match what the owner cares
  about (e.g., "backend engineer," "software engineer").
- For each person it finds, an AI reads their LinkedIn headline and
  decides: **on a scale of 0 to 100, how relevant is this person to me?**
- If the relevance score is high enough (default 60+), the AI writes a
  short, polite connection note tailored to that specific person ("Hey, saw
  your work on payments infra, would love to connect, I'm in backend
  engineering too — no pitch attached.")
- The connection request gets dropped into the queue. The queue worker
  will send it later, with a random gap, so it looks human.

**Why it exists:** Growing a network of relevant people is the
unglamorous foundation of getting referrals and job leads. If the system
can quietly add 5-10 well-targeted connections a day, the owner ends up
with hundreds of useful contacts over a couple of months.

### 2. The Acceptance Poller — *"Did anyone accept my requests?"*

**When it runs:** Every 6 hours.

**What it does:**
- Looks at the database for connection requests it sent that are still
  marked "pending."
- For each one, opens that person's profile, looks for the "1st" badge
  (LinkedIn shows this on direct connections), and updates the database to
  "accepted" if so.
- When a connection is newly accepted, it sends out a notification
  internally — other agents (especially the Referral Agent) listen for this
  and decide whether to follow up.

**Why it exists:** Acceptances are the trigger for the entire next phase
(referral asks, follow-up engagement). Without polling, the system has no
idea when a person becomes reachable.

### 3. The Content Agent — *"Keep me visible."*

This is actually two sub-agents in one file:

**Sub-agent A — Repost Suggestions** runs twice a day. It searches LinkedIn
for posts tagged with keywords the owner cares about (e.g., "hiring,"
"software engineer"), asks an AI to score each one for "would this make my
feed look more interesting if I reshared it?", and:

- If a post scores really high (90+), the system reshares it automatically.
- If it scores well but not amazing (60-89), the system sends the top
  candidates to Slack with **[Repost Now]** and **[Skip]** buttons so the
  owner can decide.

**Sub-agent B — Engagement Loop** runs three times a day. It's supposed to:

- Keep a list of "important people I want to stay visible to"
  (recruiters, hiring managers, recent connections).
- Once a day, like the most recent post from each of them.
- Once every three days, leave a thoughtful AI-written comment.

**Important caveat:** The engagement loop is currently dead — see issue
`B1` in `issue.md`. Nothing in the project populates the list of "important
people," so the agent runs but does nothing.

**Why it exists:** Algorithms (LinkedIn's and human ones) reward people
they see often. Quietly liking 5-10 of the right people's posts every day
is how you stay top-of-mind without having to actively scroll the feed.

### 4. The Job Hunter Agent — *"Find me good roles."*

**When it runs:** Three times a day, 8 AM, 1 PM, 7 PM.

**What it does:**
- Searches LinkedIn Jobs for the owner's preferred role keywords (e.g.,
  "backend engineer," "python developer") in their preferred locations
  (e.g., "India," "Remote").
- For every job it finds, sends the title, company, and description to an
  AI which returns: a relevance score, whether the role wants you to "drop
  a comment to apply," what comment to leave if so, and whether this is a
  company the owner would want a referral at.
- High-relevance jobs (70+) get posted to a Slack channel with quick
  action buttons: **[Mark Applied]**, **[Connect to Poster]**, **[Trigger
  Referral]**, **[Dismiss]**.
- Really high-relevance jobs at companies the AI flagged for referral
  automatically kick off the Referral Agent for that company.
- Jobs that explicitly ask for a comment (e.g., "Comment 'interested' to
  apply!") get a queued auto-comment.

**Why it exists:** Good jobs disappear under hundreds of applications
within a day. The owner wants to know within hours, not days. The AI
filtering means the Slack channel only contains genuinely relevant roles
instead of thousands of irrelevant ones.

### 5. The Referral Agent — *"Get me a referral at company X."*

**When it runs:** Triggered manually (the owner types `/referral Stripe` in
Slack) or automatically (the Job Hunter found a great role at a company).

**What it does:**

This is the most complex agent. It runs in two big phases.

**Phase 1: Find the right people.**
- The agent searches for employees of the target company in three priority
  tiers:
  1. **HR / Recruiters** — most likely to actually refer.
  2. **Engineering managers** — second most likely.
  3. **Individual contributors** (regular engineers) — third most likely.
- For each tier, it runs LinkedIn people-searches with specific role
  keywords ("Recruiter at Stripe," "Engineering Manager at Stripe," etc.).
- Up to ~30 people get added to the campaign.
- A polite connection note is written for each of them by the AI. So is a
  follow-up DM that politely asks for a referral — the DM is precomputed
  and stored so Slack can show the owner the exact wording later.
- The connection requests go into the action queue, prioritized by tier
  (HR goes out first).

**Phase 2: When they accept, send the referral ask.**
- Every 4 hours, the **Referral Acceptance Poller** checks who has
  accepted.
- If they accepted within 2 days of the request: the system automatically
  sends the precomputed DM. (Quick enough that the connection still feels
  fresh and the auto-ask seems natural.)
- If they accepted later than 2 days: the system asks the owner in Slack
  whether to send the DM. **[Send DM]** or **[Skip]** — the owner decides.
- If the owner doesn't respond to Slack within 3 days, the system auto-skips
  to keep things tidy.

**Why it exists:** Referrals are the single highest-leverage thing for
landing interviews. But the worst thing you can do is connect with someone
and immediately ask for a referral — it feels gross. This agent enforces
the delay and the polite framing, and it scales the work to 20-30
candidates per company instead of just 1-2.

---

## What runs LinkedIn under the hood

The agents never click LinkedIn themselves. They write "tickets" (called
**actions**) into a shared queue. A separate worker pulls one ticket every
few minutes and does the actual clicking. Why?

**Reason 1: One bottleneck, one safety brake.**
If five agents each click LinkedIn at random times, LinkedIn sees lots of
rapid activity from one account. By funneling everything through one queue
that runs at human pace (one action every ~5 minutes), LinkedIn sees a
slow, steady drip.

**Reason 2: Budget enforcement.**
The queue keeps a per-day counter for each action type:

| Type | Max per day |
|---|---|
| Connection requests | 25 |
| Profile views | 80 |
| Likes | 60 |
| Comments | 10 |
| Reposts | 3 |
| Searches | 30 |
| Easy Apply applications | 10 |
| Direct messages | 15 |

When the budget for that day is hit, the queue defers actions to tomorrow
instead of doing them anyway. The numbers are lowered in **week 1** of a
new account (only 3-5 connections/day) and gradually raised through week 4
— this is called "warm-up" and is meant to make a fresh account look like a
real person ramping up activity.

**Reason 3: Circuit breaker.**
If the system sees a CAPTCHA, a login wall, or "we noticed unusual
activity," a flag in the database flips to **RED**. The queue refuses to do
anything until the owner manually fixes it (`/resume` in Slack). This is
the single most important safety feature — it's the difference between
"we made one mistake" and "the account got banned."

---

## The browser

To actually click LinkedIn, the system runs a real Chrome browser using
Playwright. A few tricks make this hard to detect:

- The browser uses the **same** user-agent, screen size, and timezone every
  single time. LinkedIn fingerprints these and a sudden change looks bot-like.
- A "stealth" library patches the browser so `navigator.webdriver` doesn't
  scream "I am automation."
- Logins are done once, manually, by the owner — the cookies get saved to
  `state.json` and reused. No re-logging in every hour.
- Mouse moves take a curved path with random delays, typing has random gaps
  between keystrokes, and there are 2-8 second pauses before and after every
  action.
- When the browser can't find a button (LinkedIn redesigns frequently),
  there's a **vision fallback** — it takes a screenshot, sends it to an AI
  model that can see images, and asks "where exactly is the Connect button?"
  Then clicks the pixel the AI points to.

---

## Talking to the user — Slack

The owner doesn't have to look at a dashboard. Everything happens in Slack.

| Channel | What appears there |
|---|---|
| `#system-alerts` | Errors, circuit-breaker trips, anything broken |
| `#job-alerts` | New jobs the AI thinks are relevant |
| `#repost-suggestions` | Posts that might be worth resharing |
| `#referral-campaigns` | New referral campaigns + approval asks |
| `#feed-job-alerts` | Job-style posts spotted in the home feed |
| `#auto-apply` | Easy-Apply submissions + manual application links |

Slash commands the owner can type anywhere:

| Command | Effect |
|---|---|
| `/status` | Show current health + remaining daily budget |
| `/pause` | Stop everything (trips the circuit breaker to red) |
| `/resume` | Resume everything (clears the breaker) |
| `/dryrun on/off` | Toggle the "log only, don't actually click" mode |
| `/referral Stripe` | Start a referral campaign for Stripe |

Buttons on Slack messages can:

- Mark a job as applied → recorded in the database.
- Trigger a referral campaign for a company.
- Connect with a job-poster directly.
- Approve / skip a precomputed referral DM.
- Repost a suggested post.
- Dismiss a feed-job that's irrelevant.

---

## Where the data lives

A MongoDB database holds everything. The collections:

| Collection | What it stores |
|---|---|
| `action_queue` | Pending and historical actions (the tickets) |
| `daily_budgets` | Today's used vs. limit for each action type |
| `system_health` | Current circuit-breaker state (green/yellow/red) |
| `connections` | Every person we've ever connected with or tried to |
| `engage_list` | (Designed but currently empty) people to stay visible to |
| `jobs` | Jobs found by the Job Hunter agent |
| `recent_jobs` | Jobs from the auto-apply scraper (last 24h) |
| `feed_job_posts` | Job-style posts spotted in the home feed |
| `referral_campaigns` | All active and historical referral campaigns |
| `easy_apply_logs` | Audit trail of every Easy-Apply attempt |
| `reputation_scores` | (Designed but unused) per-person engagement stats |

---

## The AI layer

A single LLM (large language model) — currently Groq's Llama 3.3 70B — is
called for every smart decision:

- **Scoring** a profile, post, or job for relevance.
- **Writing** a personalized connection note in <280 characters.
- **Writing** a polite referral DM in <600 characters.
- **Writing** a genuine 1-2 sentence engagement comment.
- **Classifying** whether a random feed post is actually a job offer.
- **Answering** Easy-Apply form questions using the owner's profile data.

There's also OpenAI's GPT-4o reserved for the **vision fallback** — when the
Playwright code can't find a button by selectors, GPT-4o looks at the
screenshot and tells the system the pixel coordinates to click.

Every LLM call has temperature set explicitly, max_tokens capped, and
returns are constrained to JSON when the structure matters.

---

## Easy Apply — fully automated job applications

For jobs where the company supports LinkedIn's "Easy Apply" flow (a
multi-step form inside LinkedIn), the system can submit applications
automatically:

1. The Auto-Apply Agent scrapes jobs posted in the last 24 hours and
   scores them.
2. If a job scores 75+ AND is Easy-Apply-eligible, it gets queued for
   auto-submission.
3. A browser instance opens the application modal and walks through it step
   by step. On each step:
   - Contact info gets filled from the owner's profile.
   - The resume PDF gets uploaded.
   - Free-text questions get answered by the LLM (using the owner's profile
     as context).
   - Multiple-choice / yes-no / dropdown questions also get answered by the
     LLM, but only if the LLM picks an exact match in the allowed options.
4. If the LLM can't confidently answer a required question, the system
   bails out and sends a Slack alert saying "this one needs you to finish
   it manually."
5. On success, a "Applied via Easy Apply" message goes to Slack.

For jobs that have an external ATS (the "Apply on company website" button),
the system instead just sends a Slack alert with the link and lets the owner
finish it themselves.

---

## What's the "dry run" thing for?

Every action has a `dry_run` flag. When dry-run mode is on:

- The agents run all their logic (search, score, decide).
- Actions get written to the queue with `dry_run=True`.
- The queue worker reads them, but instead of opening a browser and
  clicking, it prints "[DRY RUN] Would execute: connect ->
  https://linkedin.com/in/foo" and moves on.
- Slack notifications still go out, so the owner can see whether the AI is
  making sensible picks.

It's a way to test the entire system **without** risking the LinkedIn
account. The intended workflow is: run in dry-run mode for 3-5 days, review
the picks, calibrate the thresholds, and only then flip to live mode.

---

## How agents wake up — Inngest

All the scheduling is handled by **Inngest**, which is essentially a
managed cron + event bus. The agents are defined as Inngest "functions"
with a trigger like `cron="0 9,18 * * *"` (every day at 9 AM and 6 PM).
Inngest's hosted service calls a webhook on the running FastAPI server
when it's time to run.

Events also fire across agents:

- When the Acceptance Poller sees a new acceptance → emits
  `connection/accepted`.
- When the Job Hunter sees a great role → emits `referral/campaign.start`.

So the system isn't a single monolithic loop — it's a network of small
functions that wake up on schedule or in response to each other.

---

## What's missing or broken right now

Read `issue.md` for the full audit, but the highlights:

1. **The content engagement loop is dead.** Nothing populates the
   `engage_list` collection, so the agent has no people to engage with.
2. **The Slack signature check is bypassed when the secret is unset.**
   Anyone on the network could trigger commands. Fail-closed needed.
3. **Several Slack buttons have no server handler** — clicking "Dismiss"
   or "Open ATS" does nothing.
4. **Some scrapers use stale LinkedIn selectors** — they sometimes return
   empty results because LinkedIn redesigned the page.
5. **Inngest retries can double-charge LLMs and queue actions twice** —
   per-item work needs to be wrapped in `step.run`.
6. **LinkedIn checkpoints are detected but silently ignored** — should
   trip the circuit breaker instead.

These are all fixable; nothing in the design is fundamentally broken.

---

## The bigger picture — why build this at all?

Job hunting in 2026 has gotten extreme. Every relevant role has hundreds
of applicants within hours of posting. Recruiters get inundated. Cold
applications convert at ~1%. The reliable ways to break through are:

1. A warm referral.
2. A genuine relationship with someone who already works there.
3. Being top-of-mind when a role opens.

All three require sustained, polite, low-volume social effort. This project
is one person's bet that you can automate the **mechanics** (searching,
remembering, polite outreach, tracking who said what when) without losing
the **substance** (genuine messages, no spam, respecting people's time and
LinkedIn's rules).

The point isn't to "game" LinkedIn — it's to give a job seeker a quiet,
disciplined assistant that does the boring work so they can focus on the
actual conversations.
