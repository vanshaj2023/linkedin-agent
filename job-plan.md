 ▐▛███▛█   Claude Code v2.1.285
▝▜██████▀  Opus 5.5 · Claude Team
 ▝▝   ▝▝   ~\Desktop\VS Code\linkedin

  Get to finished work sooner with Opus 5.5. Switch anytime with /model.

❯ /model                                                                        
  ⎿  Set model to Opus 5.5 and saved as your default for new sessions

❯  read the complete project properly and tell me is it able to do like go on   
  linkedin and on the jobs listing and search for all the opening that posted   
    within an hour and then give me the list of all the jobs their apply link   
  and their matching score with my resume tell me is it able to do that???      
                                                                                
  264.6k in | 6.8k out | 5.2k thinking                                          
  ● Bash(& "c:\Users\kumar\Desktop\VS Code\linkedin\venv\Scripts\python.exe" -c 
  "import pypdf; print('pypdf installed')" 2>$null ; & "c:\Use...) (ctrl+o to   
  expand)                                                                       
                                                                                
    Right now: NO, it cannot do that completely as currently written.           
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
    While about 70%–80% of the scraping infrastructure is in place, there are   
  major missing pieces and limitations preventing it from doing exactly what    
  you                                                                           
    described.                                                                  
                                                                                
                                                                                
    ──────                                                                      
                                                                                
                                                                                
    ### Detailed Breakdown of Your 4 Requirements                               
                                                                                
                                                                                
                                                                                
                                                                                
                                                                                
     What you asked for                      │ Can the project do it right now? 
  │ Technical reality in the code                                               
                                                                                
  ─────────────────────────────────────────┼──────────────────────────────────┼ 
  ───────────────────────────────────────────────────────────────────────────── 
     1. Go to LinkedIn jobs listing          │               YES                
  │ Implemented using Playwright and saved browser cookies in jobs_recent.py    
                                             │                                  
  │ and jobs.py.                                                                
     2. Search openings posted within 1 hour │                NO                
  │ In jobs_recent.py:44, the filter is hardcoded to past 24 hours              
                                             │                                  
  │ (&f_TPR=r86400). LinkedIn's parameter for the past 1 hour is &f_TPR=r3600.  
                                             │                                  
  │ In jobs.                                                                    
  ──── (497 lines hidden) ───────────────────────────────────────────────────── 
  actly 60 minutes                                                              
  * 61-minute-old job                                                           
  * duplicate job                                                               
  * duplicate across search queries                                             
  * missing timestamp                                                           
  * missing application link                                                    
  * Easy Apply                                                                  
  * external ATS                                                                
  * empty description                                                           
  * LLM failure                                                                 
                                                                                
  ## 18. Exact File-by-File Implementation Roadmap                              
                                                                                
  This is the most important section.                                           
                                                                                
  Do NOT make the changes.                                                      
                                                                                
  Instead tell me exactly what should eventually be changed.                    
                                                                                
  For example:                                                                  
                                                                                
  ### Phase 1 — Resume Pipeline                                                 
                                                                                
  * File X → change Y                                                           
  * File Z → add functionality A                                                
                                                                                
  ### Phase 2 — LinkedIn Scanner                                                
                                                                                
  * File X → change Y                                                           
                                                                                
  ### Phase 3 — Matching Engine                                                 
                                                                                
  ...                                                                           
                                                                                
  For every planned change explain:                                             
                                                                                
  * what should change                                                          
  * why                                                                         
  * how it connects to existing code                                            
  * dependencies                                                                
  * possible risks                                                              
                                                                                
  ## 19. Dependency Changes                                                     
                                                                                
  List packages that would eventually need to be:                               
                                                                                
  * added                                                                       
  * removed                                                                     
  * reused                                                                      
                                                                                
  Do not install anything now.                                                  
                                                                                
  ## 20. Final Data Flow                                                        
                                                                                
  Show the complete proposed flow from:                                         
                                                                                
  ```text                                                                       
  Scheduled scan                                                                
  → LinkedIn                                                                    
  → job discovery                                                               
  → timestamp filtering                                                         
  → job extraction                                                              
  → deduplication                                                               
  → resume matching                                                             
  → scoring                                                                     
  → database                                                                    
  → Slack/output                                                                
  ```                                                                           
                                                                                
  ## 21. Risks and Limitations                                                  
                                                                                
  Be completely honest about limitations, especially:                           
                                                                                
  * LinkedIn scraping                                                           
  * completeness of job discovery                                               
  * timestamp accuracy                                                          
  * external application URLs                                                   
  * anti-bot systems                                                            
  * LLM scoring consistency                                                     
  * rate limits                                                                 
                                                                                
  ## 22. Definition of Done                                                     
                                                                                
  Create a checklist describing what must eventually be verified for the        
  feature to be considered complete.                                            
                                                                                
  ---                                                                           
                                                                                
  # IMPORTANT RULES                                                             
                                                                                
  1. **DO NOT IMPLEMENT ANYTHING.**                                             
  2. Do not modify files.                                                       
  3. Do not create files.                                                       
  4. Do not write patches.                                                      
  5. Do not install dependencies.                                               
  6. Do not refactor anything.                                                  
  7. Do not give generic advice disconnected from the repository.               
  8. Inspect the actual code before making recommendations.                     
  9. Reuse existing architecture where appropriate.                             
  10. Identify existing bugs that would affect this feature.                    
  11. Clearly distinguish:                                                      
                                                                                
  * what currently exists                                                       
  * what is broken                                                              
  * what is missing                                                             
  * what you recommend                                                          
                                                                                
  12. If something cannot be verified from the repository, explicitly say so.   
  13. Perform a second review of the repository before finalizing the plan to   
  ensure no relevant component was missed.                                      
                                                                                
  ### Final instruction                                                         
                                                                                
  I am going to use your response as the **technical blueprint for a future     
  implementation**.                                                             
                                                                                
  Therefore, prioritize:                                                        
                                                                                
  **accuracy → understanding the existing codebase → architecture →             
  implementation roadmap → edge cases**                                         
                                                                                
  over writing code.                                                            
                                                                                
  Again:                                                                        
                                                                                
  > **ONLY ANALYZE THE PROJECT AND CREATE THE PLAN. DO NOT IMPLEMENT            
  ANYTHING.**                                                                   

● Starting with a full read of the repo. No changes will be made.

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && git ls-files && echo
      "---UNTRACKED/IGNORED TOP---" && ls -la && echo "---" && cat .gitignore
      2>/dev/null)
  ⎿  .claude/settings.local.json
     .claude/spec/plan.md
     .env.example
     … +140 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in config.py
      main.py inngest_client.py run.py run_scraper.py login.py github_trigger.py
      requirements.txt p…)
  ⎿  =================== config.py
          1     import os
          2     from dotenv import load_dotenv
     … +687 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in
      scrapers/__init__.py scrapers/jobs.py scrapers/jobs_recent.py; do echo
      "=================== $f"; cat -n…)
  ⎿  =================== scrapers/__init__.py
     =================== scrapers/jobs.py
          1     import asyncio
     … +318 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in
      browser/__init__.py browser/manager.py browser/interactions.py; do echo
      "=================== $f"; cat -…)
  ⎿  =================== browser/__init__.py
     =================== browser/manager.py
          1     import os
     … +644 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in llm/__init__.py
      llm/service.py db/__init__.py; do echo "=================== $f"; cat -n
      "$f"; done)
  ⎿  =================== llm/__init__.py
     =================== llm/service.py
          1     import asyncio
     … +358 lines (ctrl+o to expand)

  Read 2 files (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in
      agents/__init__.py agents/job_hunter.py agents/auto_apply.py; do echo
      "=================== $f"; cat -n…)
  ⎿  =================== agents/__init__.py
     =================== agents/job_hunter.py
          1     import datetime
     … +199 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in core/__init__.py
      core/action_queue.py core/budget.py core/circuit_breaker.py
      core/warmup.py; do echo "=…)
  ⎿  =================== core/__init__.py
     =================== core/action_queue.py
          1     import asyncio
     … +386 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in
      slack/__init__.py slack/bot.py test_recent_jobs.py test_feed_scout.py
      test_connect_manual.py; do echo "…)
  ⎿  =================== slack/__init__.py
     =================== slack/bot.py
          1     import datetime
     … +423 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && ls venv/Lib/site-packages
      | grep -i -E "inngest|groq|playwright|motor|pymongo|pypdf|pdfplumber|fitz
      |pymupdf|open…)
  ⎿  fastapi
     fastapi-0.115.14.dist-info
     groq
     … +24 lines (ctrl+o to expand)

● Still auditing the codebase after reviewing config, scrapers, browser, LLM,
  DB, agents, core, and Slack. Next I'll check how the Inngest SDK handles the
  lambda in step.run, then finish reviewing the remaining agents, Easy Apply,
  docs, and .env.

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && sed -n 150,260p
      venv/Lib/site-packages/inngest/_internal/step_lib/step_async.py; echo "---
      base"; grep -n "iscor…)
  ⎿      ) -> tuple[types.T, ...]:
             """
             @deprecated Use `ctx.group.parallel()` instead. This method wi
     … +124 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && for f in
      browser/easy_apply.py agents/feed_scout.py; do echo "===================
      $f"; cat -n "$f"; done)
  ⎿  =================== browser/easy_apply.py
          1     import os
          2     import datetime
     … +402 lines (ctrl+o to expand)

  Searched for 1 pattern (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && wc -l agents/*.py
      scrapers/*.py browser/*.py mailer/*.py _*.py debug_*.py && echo "---" &&
      head -60 scrapers/fee…)
  ⎿       0 agents/__init__.py
        109 agents/auto_apply.py
        170 agents/connection.py
     … +135 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && sed -n 398,450p
      scrapers/feed.py && echo ... && sed -n 508,600p scrapers/feed.py && echo
      "=== crons" && grep -n…)
  ⎿  async def _scrape_hiring_posts_impl(keyword: str, max_posts: int, head
     less: bool) -> list:
         async with async_playwright() as p:
     … +167 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && cat README.md && echo
      "=========== understanding.md" && cat understanding.md | head -250)
  ⎿  # LinkedIn AI Agent

     An automated agent powered by **Playwright** and **LangChain** to auto
     … +307 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && grep -n "class
      Concurrency" -A 25
      venv/Lib/site-packages/inngest/_internal/server_lib/*.py
      venv/Lib/site-package…)
  ⎿  venv/Lib/site-packages/inngest/_internal/server_lib/registration.py:60
     :class Concurrency(_BaseConfig):
     venv/Lib/site-packages/inngest/_internal/server_lib/registration.py-61
     … +39 lines (ctrl+o to expand)

● Concurrency keys are supported, so a shared browser lock is possible. Next:
  checking .env with secrets masked, the previous-session transcript, and the
  planning docs.
● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && awk -F= '/^[[:space:]]*#/
      || NF<2 {next} { k=$1; v=substr($0, index($0,"=")+1); if (k ~
      /KEY|TOKEN|SECRET|PASSWO…)
  ⎿  Error: awk from 'C:\Users\kumar\Desktop\VS Code\linkedin\.env' was blocked 
     by a deny rule.

● .env reads are blocked by your permission rules, so I'll leave it alone and
  mark its values as unverified in the plan. Moving on to the earlier session
  transcript and the planning docs.

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && f="2026-06-25-025214-tell
      -me-how-i-run-this-to-get-the-job-post-availa.txt"; wc -l "$f"; grep -n -i
      "f_TPR\|resu…)
  ⎿  1101 2026-06-25-025214-tell-me-how-i-run-this-to-get-the-job-post-avai
     la.txt
     32:  LLM-scores them, sends Slack alerts for high-scoring ones, trigge
     … +41 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && head -c 3500
      .claude/spec/plan.md; echo; echo "=====plan.md grep"; grep -n -i
      "job\|resume\|score" plan.md | hea…)
  ⎿  # LinkedIn Automation — Job Hunting + Referral Plan

     ## Current State (What Already Exists)
     … +208 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && f="2026-06-25-025214-tell
      -me-how-i-run-this-to-get-the-job-post-availa.txt"; sed -n 1,20p "$f";
      echo ....; sed -…)
  ⎿  ╭─── Claude Code v2.1.170 ────────────────────────────────────────────
     ─────────╮
     │                                                    │ Tips for gettin
     … +140 lines (ctrl+o to expand)

● I found a significant bug: both job scrapers read the URL from the first card
  on the page instead of the one actually clicked. Now checking the uncommitted
  diffs on the job files and whether the resume PDF has a text layer.

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && git diff
      --ignore-all-space -- scrapers/jobs_recent.py scrapers/jobs.py
      test_recent_jobs.py agents/auto_apply.py…)
  ⎿  diff --git a/agents/auto_apply.py b/agents/auto_apply.py
     index 95356b7..0e70683 100644
     --- a/agents/auto_apply.py
     … +151 lines (ctrl+o to expand)

● Main modules read. Doing the second-pass review now: remaining agents, the
  diagnostic result files, and anything else touching jobs, the session, or the
  browser that I haven't covered yet.

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && grep -n -i
      "job\|recent\|resume\|score_job\|playwright_thread\|async_playwright"
      agents/referral.py agents/conne…)
  ⎿  agents/referral.py:57:    job_post_url = ctx.event.data.get("job_post_
     url", "")
     agents/referral.py:102:        "job_post_url": job_post_url,
     … +44 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && grep -n "def page(self)"
      venv/Lib/site-packages/playwright/async_api/_generated.py | head -5; grep
      -n "chromium"…)
  ⎿  3003:    def page(self) -> "Page":
     3080:    def page(self) -> "Page":
     6709:    def page(self) -> typing.Optional["Page"]:
     … +8 lines (ctrl+o to expand)

● Bash(cd "/c/Users/kumar/Desktop/VS Code/linkedin" && awk 'NR>=13000'
      venv/Lib/site-packages/playwright/async_api/_generated.py | grep -n
      "^class Locator" | head -2;…)
  ⎿  1633:class Locator(AsyncBase):
     5209:class LocatorAssertions(AsyncBase):
     Locator.page present: True

● I have everything I need. One correction to the earlier answer you pasted: the
  scrapers are in worse shape than it said, because job URLs and dedup are
  broken (details below). Writing up the plan now.

  ---

  1. Current Project Summary

  What it is: a single-user LinkedIn automation service. The audit covers the
  working tree, which has 30 uncommitted modified files. HEAD differs in places:
  for example, the await score_job_post fixes exist only in the working tree.

  Runtime shape:
  - main.py is a FastAPI app. It serves 11 Inngest functions at /api/inngest
    plus /slack/commands, /slack/actions and /health. You run it with python 
    main.py (uvicorn, reload=True) or run.py (Proactor loop, no reload), with
    the Inngest dev server or Inngest Cloud in front. cloudflared.exe in the
    repo suggests it gets tunneled publicly.
  - Scheduling: Inngest cron functions in agents/*.py and core/action_queue.py.
    All crons are UTC, because none uses a TZ= prefix.
  - Browser: each scraper call launches a fresh Chromium through Playwright 1.44
    + playwright-stealth. It loads cookies from state.json, which login.py
    creates through a manual headed login. Everything runs inside
    run_in_playwright_thread (a dedicated Proactor loop thread) to get around
    uvicorn's Selector loop on Windows.
  - LLM: Groq llama-3.3-70b-versatile (hardcoded) through the sync SDK, wrapped
    in asyncio.to_thread. Calls use temperature 0.3, max_tokens 1024 and JSON
    mode.
  - DB: MongoDB through Motor, database linkedin_automation. The Pydantic models
    in db/__init__.py mostly aren't used on insert; agents write raw dicts.
  - Safety layer: every LinkedIn write action (connect, like, comment, DM,
    repost, easy_apply) goes through ActionQueue, which runs one action every 5
    minutes. It enforces daily budgets with warm-up limits and a CircuitBreaker
    (green/yellow/red, stored in Mongo). Scrapers bypass all of this: reads
    aren't budgeted, and nothing trips the breaker on a block page.
  - Output: Slack Block Kit messages to hardcoded channels. With no token
    configured, they print to the console instead.
  - Alternate path: .github/workflows/scrape.yml + run_scraper.py +
    github_trigger.py run scrapers on GitHub Actions using a base64 state.json
    secret. Its jobs task uses scrapers/jobs.py, which has no time filter.

  Job-related functions today:
  - auto-apply-run (every 2h): runs scrapers/jobs_recent.py with a 24h filter.
    It scores each job with a generic LLM prompt, then queues Easy Apply (score
    ≥75), sends a Slack manual-apply alert (65-74), or stores the job as
    low_score.
  - job-hunter-run (3x/day UTC): runs scrapers/jobs.py with no time filter and
    the same generic score. It sends a Slack alert at ≥70, can auto-comment, and
    can auto-trigger a referral campaign at ≥80.
  - feed-scout-run: finds hiring posts in the home feed. This is unrelated to
    the Jobs tab.

  Not verified in this audit:
  - .env contents. Reading it is blocked by your permission rules, so any value
    overrides there are unknown.
  - Live LinkedIn DOM, selectors and URL parameters. I didn't hit LinkedIn.
  - Whether state.json (last modified Jun 7) is still a valid session.

  ---

  2. Current Capability vs Desired Capability

  Requirement: Open LinkedIn Jobs search
  Current Status: Complete (Needs verification)
  What Exists: jobs_recent._scrape_combo builds
  /jobs/search/?keywords&location&f_TPR&sortBy=DD
  What's Missing: Live selector validation
  ────────────────────────────────────────
  Requirement: Persisted auth
  Current Status: Complete
  What Exists: login.py saves state.json; get_authenticated_context loads it
  What's Missing: Path is relative (STATE_FILE="state.json"), so it breaks if
  the
  CWD differs
  ────────────────────────────────────────
  Requirement: Session expiry handling
  Current Status: Missing (in job scrapers)
  What Exists: validate_session() exists, used only by scrapers/feed.py and
  login.py
  What's Missing: Job scrapers never check. An expired session returns []
  silently, with no breaker trip or alert. A missing state.json means it runs
  logged out without telling you
  ────────────────────────────────────────
  Requirement: CAPTCHA/checkpoint detection
  Current Status: Missing (jobs)
  What Exists: Text markers in feed.py:577-583, iframe checks in
  debug_feed_full.py:78
  What's Missing: Nothing in job scrapers
  ────────────────────────────────────────
  Requirement: 1-hour filter
  Current Status: Missing
  What Exists: f_TPR=r86400 hardcoded at jobs_recent.py:44
  What's Missing: r3600 / configurable window. jobs.py has no filter at all
  ────────────────────────────────────────
  Requirement: Sort by most recent
  Current Status: Complete
  What Exists: sortBy=DD
  What's Missing:
  ────────────────────────────────────────
  Requirement: Timestamp validation
  Current Status: Missing
  What Exists: Raw posted_ago_text string (jobs_recent.py:110-114)
  What's Missing: Parsing, a computed posted_at, window enforcement, repost
  detection
  ────────────────────────────────────────
  Requirement: Pagination
  Current Status: Missing
  What Exists: Only the first results page
  What's Missing: &start=25,50… loop
  ────────────────────────────────────────
  Requirement: Infinite scroll / lazy list
  Current Status: Broken
  What Exists: window.scrollBy x3 (jobs_recent.py:70-72) doesn't scroll the list

  pane. jobs.py:35-48 does it correctly
  What's Missing: Port the list-pane scroll
  ────────────────────────────────────────
  Requirement: Multiple queries
  Current Status: Partial
  What Exists: keyword × location loop; agents slice [:3]/[:2]
  What's Missing: Filters (remote, experience, job type), OR-queries,
  config-driven searches
  ────────────────────────────────────────
  Requirement: Title / company
  Current Status: Complete (Needs verification)
  What Exists: Read from the details pane
  What's Missing:
  ────────────────────────────────────────
  Requirement: Location
  Current Status: Missing
  What Exists:
  What's Missing: Card/top-card location
  ────────────────────────────────────────
  Requirement: Job ID
  Current Status: Missing
  What Exists:
  What's Missing: data-occludable-job-id / currentJobId / /jobs/view/{id}
  ────────────────────────────────────────
  Requirement: LinkedIn job URL
  Current Status: Broken
  What Exists: jobs_recent.py:98 and jobs.py:73 use a page-scoped
  page.locator("a.job-card-list__title, …").first
  What's Missing: It always returns the first card's URL, so every job in a
  search gets the same URL
  ────────────────────────────────────────
  Requirement: Description
  Current Status: Partial
  What Exists: #job-details inner text truncated to 3000 chars, then to 800 
  chars
  in the LLM prompt
  What's Missing: Full text; a stale-pane guard
  ────────────────────────────────────────
  Requirement: Skills / experience / employment / workplace type
  Current Status: Missing
  What Exists:
  What's Missing: Structured extraction
  ────────────────────────────────────────
  Requirement: Easy Apply status
  Current Status: Partial (Needs verification)
  What Exists: _detect_apply_type checks the details pane button
  What's Missing: Stale-pane race (fixed 1.5s wait)
  ────────────────────────────────────────
  Requirement: External apply URL
  Current Status: Partial, likely Broken
  What Exists: Reads href from button.jobs-apply-button. Buttons have no href,
  so
  it's almost always None
  What's Missing: Popup capture or Voyager JSON
  ────────────────────────────────────────
  Requirement: Dedup
  Current Status: Broken
  What Exists: Keyed on the wrong URL (seen_urls, db.recent_jobs unique
  linkedin_post_url)
  What's Missing: Job-ID key. Today ~1 job per search survives
  ────────────────────────────────────────
  Requirement: Resume stored
  Current Status: Partial
  What Exists: Vanshaj_resume_.pdf at repo root (untracked, not gitignored).
  Config default ./resume.pdf doesn't exist
  What's Missing: Correct path. Can't verify whether .env overrides it
  ────────────────────────────────────────
  Requirement: Resume parsed
  Current Status: Missing
  What Exists: No PDF library installed (no pypdf/pdfplumber/pymupdf in venv).
  The PDF is pdfTeX output, so it should have a text layer
  What's Missing: Extraction + structured profile
  ────────────────────────────────────────
  Requirement: Resume used outside Easy Apply
  Current Status: Missing
  What Exists: Only easy_apply._handle_resume uploads the file
  What's Missing:
  ────────────────────────────────────────
  Requirement: Resume-specific score
  Current Status: Missing
  What Exists: score_job_post (llm/service.py:57-66): "You are helping a
  software
  engineer…" with no candidate data
  What's Missing: The entire matching engine
  ────────────────────────────────────────
  Requirement: Matching / missing skills, gaps
  Current Status: Missing
  What Exists:
  What's Missing:
  ────────────────────────────────────────
  Requirement: Short explanation
  Current Status: Partial
  What Exists: Generic LLM reasoning
  What's Missing: Explanation grounded in a score breakdown
  ────────────────────────────────────────
  Requirement: Deterministic score
  Current Status: Missing
  What Exists: temperature 0.3, no seed, free-form judgment. A parse error
  becomes score 0 (silent false negative)
  What's Missing:
  ────────────────────────────────────────
  Requirement: Storage
  Current Status: Partial
  What Exists: recent_jobs (raw dicts, 500-char description)
  What's Missing: Schema for the new fields, upserts, indexes
  ────────────────────────────────────────
  Requirement: Slack output
  Current Status: Partial
  What Exists: send_manual_apply_alert (#auto-apply). The "Open ATS" button has
  no url and no handler, so it does nothing
  What's Missing: New alert format with link buttons
  ────────────────────────────────────────
  Requirement: Scheduler
  Current Status: Partial
  What Exists: 0 */2 * * * UTC
  What's Missing: Sub-hourly cadence, overlap strategy, a browser concurrency
  lock
  ────────────────────────────────────────
  Requirement: Standalone CLI output
  Current Status: Broken
  What Exists: test_recent_jobs.py:23 calls async score_job_post without await,
  so 'coroutine' object has no attribute 'get'
  What's Missing: A working runner
  ────────────────────────────────────────
  Requirement: Automated tests
  Current Status: Missing
  What Exists: tests/ is empty; pytest/pytest-asyncio aren't in requirements
  What's Missing: Everything

  ---

  3. Existing Architecture

  python main.py  (uvicorn, reload=True)          Inngest Dev Server / Cloud
  FastAPI app ── /api/inngest  <───────────────── cron triggers (UTC)
     │          /slack/commands, /slack/actions
     │          /health
     │
     ├─ auto-apply-run   "0 */2 * * *"   retries=1
     │    step check-cb ── CircuitBreaker.status() ── Mongo system_health
     │    step scrape-recent-jobs
     │       └─ scrapers.jobs_recent.scrape_recent_jobs(KEYWORDS[:3],
  LOCATIONS[:2], 20)
     │            └─ run_in_playwright_thread ── new Chromium + state.json (no
  session check)
     │                 for kw × loc:
     │                   goto /jobs/search?...&f_TPR=r86400&sortBy=DD
     │                   window.scrollBy ×3
     │                   for card in "div.job-card-container,
  li.scaffold-layout__list-item":
     │                       click → sleep 1.5s → read details pane
     │                       url = page-level FIRST card link   ← BUG
     │                 dedupe by url → ~1 job per combo
     │    (non-step loop) per job:
     │       skip if db.recent_jobs has url
     │       llm.score_job_post (generic prompt, desc[:800], Groq)
     │       <65 → recent_jobs{status: low_score}
     │       EasyApply ∧ ≥75 → ActionQueue.push(easy_apply) →
  recent_jobs{queued_apply}
     │       else → slack.send_manual_apply_alert (#auto-apply) →
  recent_jobs{slack_manual}
     │
     ├─ queue-processor  "*/5 * * * *"  concurrency=1 (this fn only)
     │    process_one_action → budget check → _dispatch_action
     │       easy_apply → browser.easy_apply.run_easy_apply (uploads
  APPLICANT_RESUME_PATH)
     │
     ├─ job-hunter-run   "0 8,13,19 * * *"
     │    step search-<kw>-<loc> ×4 → scrapers.jobs.search_jobs (no time filter,
  same URL bug)
     │    per job: dedupe db.jobs → score_job_post → ≥70 Slack #job-alerts
     │             should_comment → ActionQueue(comment); ≥80 → event
  referral/campaign.start
     │
     └─ feed-scout-run, connection-*, content-*, referral-*, budget-reset (other
  Chromium users)

  Slack /slack/actions: mark_applied → db.jobs + db.recent_jobs (keyed by
  linkedin_post_url)

  There is no shared browser lock. feed-scout (every 30 min), auto-apply,
  job-hunter, the queue processor and the pollers can each launch Chromium on
  the same state.json at the same time.

  ---

  4. Files Relevant to This Feature

  File: scrapers/jobs_recent.py
  Current Responsibility: Recent-jobs scraper (24h)
  Role in New Feature: Core discovery engine
  Planned Change: Rewrite: card-scoped IDs, pagination, list scroll,
  configurable
  window/filters, session/block detection, stale-pane guard, passive JSON
  capture, known_ids skip
  ────────────────────────────────────────
  File: scrapers/jobs.py
  Current Responsibility: Unfiltered job search for job_hunter
  Role in New Feature: None (redundant)
  Planned Change: Retire with job_hunter, or apply the same URL fix if kept
  ────────────────────────────────────────
  File: scrapers/feed.py
  Current Responsibility: Feed scraping
  Role in New Feature: Pattern source
  Planned Change: Reuse its validate_session + interstitial check and its
  page.on("response") capture pattern
  ────────────────────────────────────────
  File: browser/manager.py
  Current Responsibility: Browser launch, stealth, validate_session
  Role in New Feature: Session + block detection
  Planned Change: Add detect_block_state(page); STATE_FILE from env; optional
  storage-state refresh
  ────────────────────────────────────────
  File: llm/service.py
  Current Responsibility: All Groq prompts
  Role in New Feature: Profile + JD requirement extraction
  Planned Change: Add 2 extraction functions; explicit retries/timeout;
  temperature 0; keep score_job_post only for legacy
  ────────────────────────────────────────
  File: config.py
  Current Responsibility: Env config
  Role in New Feature: All new knobs
  Planned Change: Add scanner/matching config; unify resume path; GROQ_MODEL
  from
  env
  ────────────────────────────────────────
  File: db/__init__.py
  Current Responsibility: Motor client, models, indexes
  Role in New Feature: Persistence
  Planned Change: New models + collections + indexes; load_dotenv ordering
  ────────────────────────────────────────
  File: agents/auto_apply.py
  Current Responsibility: 2h scrape + generic score + apply/alert
  Role in New Feature: Downstream consumer
  Planned Change: Remove its scraping; read scored jobs from the new collection
  ────────────────────────────────────────
  File: agents/job_hunter.py
  Current Responsibility: 3x/day generic job alerts
  Role in New Feature: Redundant
  Planned Change: Remove from ALL_FUNCTIONS (or fix)
  ────────────────────────────────────────
  File: agents/feed_scout.py
  Current Responsibility: Feed job signals
  Role in New Feature: Pattern source
  Planned Change: Shows the Inngest step layout
  ────────────────────────────────────────
  File: (new) agents/job_scanner.py
  Current Responsibility:
  Role in New Feature: Scheduled orchestrator
  Planned Change: New Inngest cron function
  ────────────────────────────────────────
  File: core/circuit_breaker.py
  Current Responsibility: Global health
  Role in New Feature: Block handling
  Planned Change: Scanner trips red/yellow on checkpoint/expiry (no code change
  needed)
  ────────────────────────────────────────
  File: core/action_queue.py
  Current Responsibility: Write-action queue + budgets
  Role in New Feature: Easy Apply hand-off
  Planned Change: Add the shared concurrency key to queue-processor
  ────────────────────────────────────────
  File: core/budget.py, core/warmup.py
  Current Responsibility: Daily budgets
  Role in New Feature: Read-load budgeting (optional)
  Planned Change: Optional job_scan_pages budget
  ────────────────────────────────────────
  File: slack/bot.py
  Current Responsibility: Slack messages
  Role in New Feature: Output
  Planned Change: New fresh-job alert + digest; channel from config; link
  buttons
  ────────────────────────────────────────
  File: main.py
  Current Responsibility: FastAPI + Slack endpoints
  Role in New Feature: Registration + handlers
  Planned Change: Register scanner; verify /slack/actions signature; dismiss_job

  handler; mark_applied by job_id; optional GET /jobs/recent
  ────────────────────────────────────────
  File: inngest_client.py
  Current Responsibility: Client
  Role in New Feature: Unchanged
  Planned Change:
  ────────────────────────────────────────
  File: browser/easy_apply.py
  Current Responsibility: Easy Apply flow
  Role in New Feature: Resume upload
  Planned Change: Uses the unified resume path; fail loudly when it's missing
  ────────────────────────────────────────
  File: login.py
  Current Responsibility: Manual login
  Role in New Feature: Session recovery
  Planned Change: Referenced by the expiry alert text
  ────────────────────────────────────────
  File: test_recent_jobs.py
  Current Responsibility: Manual smoke script
  Role in New Feature: Superseded
  Planned Change: Replace with a scan_jobs.py CLI (or add the missing await)
  ────────────────────────────────────────
  File: run_scraper.py, .github/workflows/scrape.yml, github_trigger.py
  Current Responsibility: Remote scrape path
  Role in New Feature: Not recommended for the scanner
  Planned Change: Leave alone. Datacenter IPs + your cookies are high risk
  ────────────────────────────────────────
  File: requirements.txt
  Current Responsibility: Deps
  Role in New Feature:
  Planned Change: Add pypdf, test deps
  ────────────────────────────────────────
  File: pytest.ini
  Current Responsibility: asyncio_mode=auto, testpaths=tests
  Role in New Feature: Test runner
  Planned Change: Needs pytest-asyncio installed
  ────────────────────────────────────────
  File: .gitignore
  Current Responsibility: Ignores
  Role in New Feature: Security
  Planned Change: Add resume, transcripts, output/, .claude/, CLAUDE.md
  ────────────────────────────────────────
  File: .env.example
  Current Responsibility: Env template
  Role in New Feature: Docs for new vars
  Planned Change: Add the new keys; fix APPLICANT_RESUME_PATH
  ────────────────────────────────────────
  File: agents/referral.py
  Current Responsibility: Referral campaigns
  Role in New Feature: Downstream of the "Trigger Referral" button
  Planned Change: No change
  ────────────────────────────────────────
  File: Vanshaj_resume_.pdf
  Current Responsibility: Resume
  Role in New Feature: Candidate source
  Planned Change: Move to an ignored path
  ────────────────────────────────────────
  File: README.md, understanding.md, plan.md, .claude/spec/plan.md
  Current Responsibility: Docs
  Role in New Feature:
  Planned Change: README is stale (mentions LangChain and files that don't
  exist)
  ────────────────────────────────────────
  File: .env
  Current Responsibility:
  Role in New Feature:
  Planned Change: Not inspected (permission deny)

  ---

  5. Proposed Final Architecture

  The principle: one discovery pipeline, many consumers. The new scanner becomes
  the only thing that scrapes the Jobs tab. Auto-apply and Slack read from its
  stored results. job_hunter and auto_apply's scraping go away, which also cuts
  LinkedIn traffic.

  Inngest cron  job-scanner-run   ("TZ=Asia/Kolkata */20 8-23 * * *")
    concurrency: limit=1, key="linkedin-browser", scope=env  (shared by ALL
  browser functions)
          │
    step check-cb ─────────────── CircuitBreaker.status() → red: skip
    step load-profile ─────────── matching.resume.load_candidate_profile()
          │                         PDF sha256 → Mongo candidate_profiles cache
  → (miss) pypdf → LLM extract → validate
    step plan-window ──────────── job_scan_runs.last_success → window_seconds
  (adaptive, 3600..86400)
    step load-known-ids ───────── job_listings.job_id where last_seen_at >
  now-48h
    step scan-<search_key> ×N ─── scrapers.jobs_recent.scan_search(search,
  window, known_ids)  [playwright thread]
          │   goto search url (f_TPR=r<window>, sortBy=DD, filters, start=0)
          │   detect_block_state → blocked? return {status: blocked}
          │   collect card stubs (job_id, title, company, location, age text,
  promoted, easy-apply badge) for all pages
          │   card-level title exclusion filter
          │   for NEW job_ids only: open details (click title link, wait until
  pane shows that job_id)
          │       extract details + passive Voyager JSON capture (listedAt,
  applyMethod, workplaceTypes...)
          │   returns JSON-safe dicts
    step upsert-listings ──────── bulk upsert by job_id ($setOnInsert
  first_seen_at, $addToSet matched_searches)
    step match-<job_id> ×M ────── llm.extract_job_requirements (cached by
  description_hash)
          │                         → matching.skills.normalize →
  matching.scoring.score(profile, requirements, job)
          │                         → job_listings.match
    step notify ───────────────── slack: per-job alert (score ≥ notify threshold
  & fresh), digest for the rest
    step hand-off ─────────────── easy apply ≥ auto threshold →
  ActionQueue.push(easy_apply)  (replaces auto_apply scraping)
    step record-run ───────────── job_scan_runs {counts, errors, window,
  duration}

  Consumers: Slack buttons (/slack/actions), queue-processor (Easy Apply),
  scan_jobs.py CLI, optional GET /jobs/recent

  ---

  6. LinkedIn Job Discovery Plan

  Search definition (config-driven): take the cartesian product of
  JOB_SEARCH_QUERIES × JOB_SEARCH_LOCATIONS, with shared filters. Cut the query
  count with LinkedIn's boolean keyword syntax, which is officially supported
  for job search: ("software engineer" OR "backend developer" OR "full stack 
  developer"). One OR-query × 2 locations means 2 searches per scan instead of
  6.

  URL builder (pure function in scrapers/job_parsing.py). All of these
  parameters are unofficial, so verify each on your account:

  ┌──────────────┬──────────────────────────────────────────────────────────┐
  │     Need     │                          Param                           │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Time window  │ f_TPR=r3600 (the UI only offers 24h/week/month, but the  │
  │              │ URL accepts arbitrary seconds)                           │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Newest first │ sortBy=DD                                                │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Location     │ location=India + geoId=102713980 (geoId is               │
  │              │ deterministic; free text gets resolved by LinkedIn)      │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │              │ f_WT=2 (1 on-site, 3 hybrid). Don't use location=Remote  │
  │ Remote       │ as current config does; it isn't a geo. Use              │
  │              │ geoId=92000000 (Worldwide) + f_WT=2 for global remote    │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Internship / │ f_E=1,2 (1 intern, 2 entry, 3 associate, 4 mid-senior)   │
  │  entry       │                                                          │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Job type     │ f_JT=F,I (F full-time, I internship, C contract)         │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Easy Apply   │ f_AL=true (optional)                                     │
  │ only         │                                                          │
  ├──────────────┼──────────────────────────────────────────────────────────┤
  │ Pagination   │ start=0,25,50… (25 per page)                             │
  └──────────────┴──────────────────────────────────────────────────────────┘

  1-hour filtering, two layers:
  1. Server-side: f_TPR=r<window>. This narrows results but can't be trusted
     alone: promoted cards ignore it, and its exact semantics are undocumented.
  2. Client-side: compute posted_at and enforce age ≤ JOB_POSTED_WITHIN_MINUTES.

  Timestamp sources, best first:
  1. Voyager/GraphQL JSON captured passively with page.on("response") while the
     details pane loads. This is the same technique feed.py already uses for
     URNs, and it adds no extra requests. Historically the payload has carried
     listedAt (epoch ms, exact), originalListedAt (detects reposts),
     applyMethod.companyApplyUrl, formattedLocation and workplaceTypes. Needs 
     verification: log the responses on your account first.
  2. Relative text ("34 minutes ago", "Reposted 20 minutes ago", "1 hour ago").
     Parse it into an [age_min, age_max) range, e.g. "34 minutes ago" →
     [34, 35). LinkedIn's granularity is coarse: "1 hour ago" covers 60-119 
     minutes, so 60 and 61 minutes can't be told apart from text. The context
     locale is pinned to en-US in manager.py, so the English regexes are safe.
  3. Filter-only: the job appeared under f_TPR but has no timestamp. Store
     posted_at_source="search_filter_only" and treat it as in-window but
     low-confidence.

  Pagination: loop start until a page returns <25 cards, the "No matching jobs"
  element shows up, or JOB_MAX_PAGES_PER_SEARCH (default 3) is hit. Use URL
  navigation, not the pagination buttons; it's deterministic.

  Lazy list: LinkedIn virtualizes the left list. Placeholder
  li[data-occludable-job-id] elements usually exist for all 25 cards even before
  their content renders (needs verification). That means job IDs can be 
  collected without scrolling, and scrolling the list container (port
  jobs.py:35-48) is only needed for title/company text.

  Card selection fix: use one selector, li[data-occludable-job-id]. Today
  "div.job-card-container, li.scaffold-layout__list-item" matches each job
  twice, because the li contains the div. Read the job ID and title from inside 
  the card, never with a page-level .first.

  Detail fetch fix:
  - Click the card's title anchor, not the li center, which can land on the
    company link and navigate away.
  - Then wait until the pane shows that job: currentJobId in page.url equals the
    card ID, or the top-card link contains /jobs/view/{id}. The fixed 1.5s wait
    causes stale-pane mismatches between title and description.
  - Only fetch details for job IDs not in known_ids. In steady state, most cards
    are already known, which cuts clicks by roughly 70-90%.

  Overlapping searches / duplicates: keep one in-scan seen_ids set shared across
  all searches, so a job is detail-fetched once even if three searches return
  it. Record every search that matched it through $addToSet matched_searches.

  External apply URL:
  - Primary: from the captured JSON (companyApplyUrl).
  - Fallback, opt-in (RESOLVE_EXTERNAL_APPLY_URL=true) and only for jobs that 
    already scored ≥ the notify threshold: click Apply, catch the
    context.expect_page() popup, record its URL, close it. Strip tracking params
    and unwrap LinkedIn redirect wrappers.
  - Otherwise fall back to the LinkedIn URL with apply_url_resolved=false.
    Clicking Apply has side effects: LinkedIn records the click and later asks
    "Did you apply?". That's why it's gated.

  Why "all jobs" isn't achievable:
  - LinkedIn search returns a ranked, personalized subset, capped at about 1000
    results (40 pages).
  - Promoted listings are injected, and some jobs only surface under specific
    geo or keyword combinations.
  - f_TPR is undocumented, reposts reset listedAt, and some postings (agency,
    confidential) are sparse or show up late in the index.
  - Realistically the goal is high recall within your defined searches, not
    completeness.

  ---

  7. Resume Processing Plan

  Resume PDF (RESUME_PATH, single source of truth)
     ↓  sha256(file bytes) → cache key
     ↓  cache hit in Mongo candidate_profiles? → return
  Text Extraction (pypdf; NFKC normalize to fix LaTeX ligatures "ﬁ"→"fi";
  de-hyphenate line breaks)
     ↓  guard: < 300 chars ⇒ likely image-only PDF ⇒ fail with clear alert (no
  OCR in scope)
  PII redaction (regex: email, phone, street address lines, profile URLs) before
  any LLM call
     ↓
  LLM structured extraction (temperature 0, JSON mode, Pydantic-validated, one
  call per resume version)
     ↓
  Deterministic post-processing:
     - skills → canonical names via matching/skills.py alias map
     - total experience computed in code from extracted date ranges (merge
  overlaps; internships weighted 0.5)
     ↓
  Overrides merge (optional gitignored JSON: target roles, locations, YOE, work
  authorization, exclusions)
     ↓
  Cached CandidateProfile {profile_hash, extraction_version, extracted_at}

  What to extract:
  - skills: canonical name, category (language/framework/db/cloud/tool/ml),
    evidence: listed_only | used_in_experience | used_in_project, and last-used
    year.
  - experience[]: title, company, start/end, is_internship, technologies.
  - projects[]: name, technologies.
  - education: degree, field, graduation year.
  - certifications, domains (e.g. AI/LLM, backend, fintech), target_roles (from
    overrides, else inferred), total_yoe (computed), seniority_estimate.
  - Logistics from overrides only: locations, remote preference, work
    authorization.

  What not to store: raw resume text and contact details. They're re-derivable
  from the file and they're PII.

  Why compute YOE in code: LLMs are unreliable at date arithmetic. Today
  APPLICANT_YOE defaults to 1 in config.py and 2 in .env.example; the override
  should win when it's set.

  ---

  8. Resume-to-Job Matching Plan

  Recommendation: hybrid. The LLM extracts facts; deterministic code produces 
  the score.

  Technique: LLM evaluation (score)
  Use it for: No
  Why: Not reproducible, prompt-injectable through the JD, can't be audited
  ────────────────────────────────────────
  Technique: LLM extraction
  Use it for: Yes, JD → requirements JSON, once per job (cached by description
  hash)
  Why: Only an LLM can reliably separate "required" from "nice to have" in free
  text
  ────────────────────────────────────────
  Technique: Keyword matching
  Use it for: Yes, as a fallback when the LLM fails, and for card-level title
  pre-filters
  Why: Cheap, deterministic
  ────────────────────────────────────────
  Technique: Skill matching via taxonomy
  Use it for: Yes, core
  Why: Canonical names + aliases (node/nodejs/node.js → Node.js, postgres → 
  PostgreSQL, k8s → Kubernetes) + related-skill partial credit
  ────────────────────────────────────────
  Technique: Embeddings / semantic similarity
  Use it for: Optional, later, ≤10% weight
  Why: YAGNI for one resume and a few hundred jobs a day. Adds a dependency
  (OpenAI embeddings or a local model) for marginal gain. Pinecone is
  unnecessary at this scale
  ────────────────────────────────────────
  Technique: Deterministic rules
  Use it for: Yes
  Why: Experience fit, seniority gates, logistics, hard-requirement caps

  JD extraction output (Pydantic JobRequirements):
  - required_skills[], preferred_skills[], min_years, max_years,
    education_required, seniority, employment_type, workplace_type.
  - hard_requirements[]: citizenship, clearance, required language, on-site-only
    city, degree mandatory.
  - domain_keywords[], responsibilities_summary.

  Prompt rules:
  - Required = phrases like "must", "required", "minimum", "you have",
    "requirements".
  - Preferred = "nice to have", "bonus", "preferred", "plus".
  - Optional = skills mentioned only in the company or stack description, not
    asked of the candidate. Those go in neither list.
  - Hard requirement = an eligibility condition, not a skill.
  - Pass the canonical skill vocabulary in the prompt and ask the model to map
    to it, with free-form entries in other_skills.
  - Wrap the JD in delimiters and tell the model it's untrusted data.

  The resume is never sent per job. JD extraction is candidate-independent and
  scoring is local. The resume goes to Groq once per resume version, which is a
  big privacy and token-cost win.

  Explanation: generate it from the breakdown with a template, e.g. "Strong
  backend match: 7/9 required skills (Python, FastAPI, MongoDB…). Missing
  Kubernetes, Go. Asks 3+ yrs, you have ~1.5." Optional LLM polish stays off by
  default.

  ---

  9. Match Score Design

  Scoring version v1. Weights are code constants with a version string, not env
  vars, so changes stay auditable.

  ┌────────────┬────────┬───────────────────────────────────────────────────┐
  │ Component  │ Points │                       Rule                        │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │            │        │ Σ credit / count(required). Credit: exact         │
  │ Required   │ 40     │ canonical match 1.0 (×0.8 if listed_only with no  │
  │ skills     │        │ usage evidence), related skill 0.5 (e.g. MySQL    │
  │            │        │ for PostgreSQL), else 0                           │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │ Preferred  │ 15     │ Same formula over preferred                       │
  │ skills     │        │                                                   │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │ Experience │ 15     │ cand ≥ min → 15; else 15 × max(0, 1 − (min −      │
  │  fit       │        │ cand)/3). No min stated → 12 (neutral)            │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │            │        │ Title role family                                 │
  │ Role       │ 10     │ (backend/full-stack/AI-ML/frontend/devops/data)   │
  │ alignment  │        │ vs profile target roles: same family 10, adjacent │
  │            │        │  5, else 0                                        │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │ Domain     │ 10     │ Jaccard of JD domain_keywords vs profile domains  │
  │ alignment  │        │ (+ optional embeddings later)                     │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │ Education  │ 5      │ Required degree met 5; unstated 5; not met 0      │
  ├────────────┼────────┼───────────────────────────────────────────────────┤
  │ Logistics  │ 5      │ Workplace type + location + employment type vs    │
  │            │        │ preferences                                       │
  └────────────┴────────┴───────────────────────────────────────────────────┘

  Renormalization: if a JD lists no preferred skills, its 15 points go to
  required skills proportionally. If it lists no skills at all, confidence=low.

  Hard gates (caps, applied after the sum):
  - Unmeetable eligibility requirement (citizenship/clearance/language): cap
    at 30.
  - min_years − cand ≥ 3: cap at 50.
  - Seniority title (senior/staff/principal/lead/manager/architect) while
    profile seniority is entry: cap at 50.

  Confidence:
  - high: description ≥1500 chars, ≥3 required skills extracted, timestamp
    source is JSON.
  - low: description <500 chars, keyword fallback used, or filter-only
    timestamp.
  - medium: otherwise.

  No data → no score. A missing description sets
  match.status="insufficient_data" with a null score, never 0. Current code
  turns a parse error into 0, which hides good jobs.

  Bands: 85+ strong, 70-84 good, 50-69 partial, <50 weak.

  Worked example: 8 required (6 exact + 1 related) → 6.5/8 × 40 = 32.5.
  Preferred 2/4 → 7.5. Experience: min 2, cand 1.5 → 12.5. Role 10, domain 6,
  education 5, logistics 5. Total 78.5 → 79.

  Reproducibility: the same cached extraction + the same profile hash + the same
  scoring version always gives the same score. Re-scoring after a resume change
  needs no LLM calls or LinkedIn hits, since requirements are cached per job.
  Calibrate by hand-labeling 30-50 jobs and adjusting weights under v2.

  ---

  10. Job Deduplication Plan

  - Primary key: the LinkedIn numeric job ID. Sources, in order: card
    data-occludable-job-id (or data-job-id) → currentJobId in the URL after the
    click → regex /jobs/view/(\d+) on any link.
  - Canonical URL: https://www.linkedin.com/jobs/view/{id}/, no query string.
  - In-scan: a shared seen_ids set across searches, checked before the detail
    fetch.
  - Cross-scan: the agent passes known_ids (seen in the last 48h) into the
    scraper, so it can skip detail fetches. Mongo has a unique index on job_id.
    Writes are update_one(..., upsert=True) with $setOnInsert: {first_seen_at, 
    …}, $set: {last_seen_at}, $inc: {seen_count: 1} and $addToSet: 
    {matched_searches}. Treat DuplicateKeyError from a race as a no-op.
  - Reposts: reposted listings usually keep the ID. For new-ID reposts, store a
    non-unique dedup_signature = sha1(norm(company)|norm(title)|norm(location)).
    On insert, if a doc with the same signature exists within 30 days, set
    possible_duplicate_of and suppress its notification.
  - Notifications: sent only when notification.status == "pending", so a job is
    never alerted twice, even if it's rescanned or rescored.

  ---

  11. Scheduling Plan

  Options evaluated:

  Strategy: Hourly, r3600
  Coverage: Gaps from any jitter, slow scan or failure
  LinkedIn load: Low
  Verdict: Reject
  ────────────────────────────────────────
  Strategy: Every 15 min, r3600
  Coverage: 45-min overlap, survives 3 consecutive failures, ≤15 min latency
  LinkedIn load: 96 scans/day
  Verdict: Good coverage, heavy footprint
  ────────────────────────────────────────
  Strategy: Every 20 min, waking hours, r3600 + adaptive widening
  Coverage: 40-min overlap, survives 2 failures; downtime is caught up
  automatically
  LinkedIn load: ~48 scans/day
  Verdict: Recommended default

  Adaptive window: window = clamp(now − last_successful_scan.started_at + 10 
  min, 3600, 86400).
  - After an outage or overnight, the first scan widens to cover the whole gap,
    with LinkedIn's 24h cap.
  - Jobs found in a widened window are stored and labeled
    freshness="missed_window" (age > 60 min), then go to a "posted while scanner
    was down" digest instead of per-job alerts.
  - So the 15-minute idea is directionally right, but a fixed overlapping window
    alone can't recover from downtime longer than the overlap. The adaptive
    window can.

  Other rules:
  - TZ: use the TZ=Asia/Kolkata cron prefix, which Inngest supports. Existing
    crons are UTC: feed-scout's 8-22 actually runs 13:30-04:00 IST. That's an
    existing bug worth fixing separately.
  - Jitter: a random 0-90s step.sleep at the start, to avoid an exact periodic
    signature.
  - Concurrency: one Inngest concurrency key ("linkedin-browser", scope env,
    limit 1) on every function that launches Chromium. Runs then queue instead
    of overlapping.
  - Load estimate (steady state): 2 searches × ~1.5 pages = 3 list loads per
    scan, plus detail clicks only for new IDs. That's ~150 list loads/day plus
    ~100-300 detail views/day. The existing searches budget (30/day) is never
    enforced on scrapers and is incompatible with this cadence. Either add a
    separate job_scan_pages budget (e.g. 250/day) or knowingly accept the
    footprint.

  ---

  12. Database Plan

  job_listings (new; I'd avoid reusing recent_jobs, since its existing docs are
  keyed by the buggy URL):

  job_id (unique), linkedin_url, title, company, company_url, location_text,
  workplace_type, employment_type, seniority_level, applicant_count_text,
  apply_type: easy_apply|external|unknown, is_easy_apply, external_apply_url,
  apply_url_resolved,
  description, description_hash, description_status: ok|missing|truncated,
  posted_at (Date|null), posted_at_source:
  voyager|relative_text|search_filter_only,
  posted_age_text, posted_age_min_minutes, posted_age_max_minutes, freshness:
  fresh|missed_window|stale,
  is_repost, original_posted_at, is_promoted, job_state,
  matched_searches[], dedup_signature, possible_duplicate_of,
  first_seen_at, last_seen_at, seen_count, first_scan_run_id, detail_attempts,
  requirements { ...JobRequirements, description_hash, model,
  extraction_version, extracted_at },
  match { status: scored|pending|insufficient_data|error, score, breakdown{},
  matching_skills[],
          missing_required[], missing_preferred[], gaps[], hard_gate_failures[],
  explanation,
          confidence, method: hybrid|keyword_fallback, profile_hash,
  scoring_version, scored_at, error },
  notification { status: pending|sent|skipped|failed, channel, slack_ts,
  attempts, notified_at },
  application { status: none|queued|applied|dismissed|failed, applied_at, source
  }

  Indexes: job_id unique; {first_seen_at:-1}; {"match.score":-1, 
  first_seen_at:-1}; {"notification.status":1, "match.score":-1};
  {posted_at:-1}; {dedup_signature:1, first_seen_at:-1}.

  candidate_profiles: _id = resume sha256, source_basename, profile{} (no
  contact PII), extraction_model, extraction_version, overrides_hash,
  extracted_at, is_active. Index {is_active:1}.

  job_scan_runs: started_at, finished_at, status: 
  success|partial|blocked|failed, window_seconds, searches[{key, pages, 
  cards_seen, new_ids, detail_ok, detail_failed}], new_jobs, scored, notified,
  block_reason, error. Indexes {started_at:-1} and {status:1, started_at:-1},
  with an optional TTL of 30 days.

  Also:
  - db/__init__.py reads MONGODB_URI at import without load_dotenv()
    (db/__init__.py:12). It works only because config happens to be imported
    first. Make db import config.
  - Datetimes must be ISO strings inside Inngest step outputs and converted to
    datetime only at write time. Inngest serializes step results to JSON.

  ---

  13. Output Plan

  Slack, per job (score ≥ MATCH_SCORE_NOTIFY_THRESHOLD and freshness=fresh), to
  SLACK_CHANNEL_FRESH_JOBS (default #fresh-jobs, or reuse #job-alerts):

  [header]  89/100 · Software Engineer Intern @ XYZ
  [section] 📍 Bengaluru (Hybrid) · Full-time · Easy Apply
            🕒 Posted 34 min ago (LinkedIn timestamp)      ← or "~1-2 h ago
  (approx.)" / "time unknown"
            ✓ React  ✓ Node.js  ✓ MongoDB  ✓ AWS
            ✗ Missing: Kubernetes
            ⚠ Gaps: asks 2+ yrs (you: ~1.5)
            Why: Strong full-stack match: 8/9 required skills; role family
  matches; remote-friendly.
  [context] confidence: high · scoring v1 · job 4012345678
  [actions] [Apply ↗ url] [LinkedIn ↗ url] [Mark Applied] [Dismiss] [Trigger
  Referral]

  - Link buttons use Block Kit's url field, so they open directly. Today's "Open
    ATS" button has a value but no URL and no handler, so it does nothing.
  - Mark Applied and Dismiss carry job_id. Update main.py:134-144 to write
    job_listings.application, and add a dismiss_job handler (the button exists
    in send_job_alert with no handler).
  - Digest: one message per scan for scores 50-69 and for missed_window jobs.
    Keep it under Slack's 50-block limit and the 3000-char section limit; chunk
    if needed.
  - Escaping: &, < and > in titles/companies must be escaped in mrkdwn.
  - Outbox pattern: notify from DB state (notification.status=pending). A failed
    Slack send is retried next scan instead of being lost (today send_* returns
    None and the job is still marked done).

  CLI (scan_jobs.py, replacing test_recent_jobs.py): python scan_jobs.py 
  --window 60 --headed --no-slack --json out.json prints a table: score, title,
  company, location, age, apply type, apply URL, LinkedIn URL, matching/missing
  skills. It reuses the same scraper and matching modules without Inngest. It's
  the fastest way to validate LinkedIn selectors.

  Optional: GET /jobs/recent?min_score=70&hours=1 returns JSON, for a future
  dashboard.

  ---

  14. Configuration Plan

  Var: JOB_SCAN_ENABLED
  Default: true
  Replaces:
  ────────────────────────────────────────
  Var: JOB_SCAN_CRON
  Default: TZ=Asia/Kolkata */20 8-23 * * *
  Replaces: hardcoded crons
  ────────────────────────────────────────
  Var: JOB_SEARCH_QUERIES
  Default: pipe-separated (queries may contain commas/quotes)
  Replaces: TARGET_JOB_KEYWORDS[:3] slicing
  ────────────────────────────────────────
  Var: JOB_SEARCH_LOCATIONS
  Default: India:102713980|Worldwide:92000000
  Replaces: TARGET_JOB_LOCATIONS (Remote as a location)
  ────────────────────────────────────────
  Var: JOB_WORKPLACE_TYPES
  Default: remote,hybrid,onsite
  Replaces:
  ────────────────────────────────────────
  Var: JOB_EXPERIENCE_LEVELS
  Default: 1,2,3
  Replaces:
  ────────────────────────────────────────
  Var: JOB_TYPES
  Default: F,I
  Replaces:
  ────────────────────────────────────────
  Var: JOB_EASY_APPLY_ONLY
  Default: false
  Replaces: easy_apply_only arg
  ────────────────────────────────────────
  Var: JOB_POSTED_WITHIN_MINUTES
  Default: 60
  Replaces: f_TPR=r86400
  ────────────────────────────────────────
  Var: JOB_SCAN_WINDOW_BUFFER_MINUTES
  Default: 10
  Replaces:
  ────────────────────────────────────────
  Var: JOB_MAX_PAGES_PER_SEARCH
  Default: 3
  Replaces:
  ────────────────────────────────────────
  Var: JOB_MAX_DETAIL_FETCHES_PER_SCAN
  Default: 40
  Replaces: max_per_combo=20
  ────────────────────────────────────────
  Var: JOB_EXCLUDE_TITLE_KEYWORDS
  Default: senior,staff,principal,lead,manager,director,architect
  Replaces:
  ────────────────────────────────────────
  Var: JOB_EXCLUDE_COMPANIES
  Default: empty
  Replaces:
  ────────────────────────────────────────
  Var: JOB_INCLUDE_REPOSTS
  Default: true (flagged in output)
  Replaces:
  ────────────────────────────────────────
  Var: MATCH_SCORE_NOTIFY_THRESHOLD
  Default: 70
  Replaces: JOB_SLACK_THRESHOLD / MANUAL_APPLY_MIN_SCORE=65
  ────────────────────────────────────────
  Var: MATCH_SCORE_DIGEST_THRESHOLD
  Default: 50
  Replaces:
  ────────────────────────────────────────
  Var: MATCH_SCORE_AUTO_APPLY_THRESHOLD
  Default: 80
  Replaces: EASY_APPLY_MIN_SCORE=75 constant
  ────────────────────────────────────────
  Var: RESUME_PATH
  Default: (required)
  Replaces: APPLICANT_RESUME_PATH default ./resume.pdf (keep as alias)
  ────────────────────────────────────────
  Var: CANDIDATE_PROFILE_OVERRIDES_PATH
  Default: optional, gitignored
  Replaces: APPLICANT_YOE, YOUR_DOMAIN
  ────────────────────────────────────────
  Var: GROQ_MODEL
  Default: llama-3.3-70b-versatile
  Replaces: hardcoded config.py:25
  ────────────────────────────────────────
  Var: MATCH_EXTRACTION_MODEL
  Default: same as GROQ_MODEL
  Replaces:
  ────────────────────────────────────────
  Var: RESOLVE_EXTERNAL_APPLY_URL
  Default: false
  Replaces:
  ────────────────────────────────────────
  Var: SLACK_CHANNEL_FRESH_JOBS (+ existing channels)
  Default: #fresh-jobs
  Replaces: hardcoded slack/bot.py:9-14
  ────────────────────────────────────────
  Var: LINKEDIN_STATE_PATH
  Default: absolute path outside repo
  Replaces: STATE_FILE="state.json"
  ────────────────────────────────────────
  Var: JOB_SCAN_DAILY_PAGE_BUDGET
  Default: 250
  Replaces:

  Keep scoring weights as versioned code constants. Making them configurable is
  over-engineering for one user.

  ---

  15. Error Handling Plan

  Failure: Session expired
  Detection: After each goto: URL contains /login, /authwall, /checkpoint or
  /uas/login; login inputs present; guest jobs layout; logged-in nav missing
  Response: Scraper returns {status:"blocked", reason:"session_expired"}. Agent
  trips breaker red (no auto-resume), sends one Slack alert ("run python 
  login.py"), records the run, raises NonRetriableError
  ────────────────────────────────────────
  Failure: CAPTCHA/checkpoint
  Detection: Reuse feed.py:577-583 text markers + captcha/challenge iframes
  Response: Same as above, reason checkpoint. Never try to solve it
  ────────────────────────────────────────
  Failure: Soft throttling (empty pages, 429, "try again later")
  Detection: HTTP status from response listener; repeated empty results with a
  present list container
  Response: Trip yellow with 3h auto-resume; skip remaining searches
  ────────────────────────────────────────
  Failure: Scraping failure per card
  Detection: try/except per card, counters
  Response: Continue. If >50% of cards in a search fail, treat it as DOM drift:
  save screenshot + HTML to output/debug/ (gitignored) and alert
  ────────────────────────────────────────
  Failure: Zero results
  Detection: Distinguish "No matching jobs found" element (legit) from list
  container missing (breakage)
  Response: Legit: record 0. Breakage: alert
  ────────────────────────────────────────
  Failure: Stale details pane
  Detection: Pane job ID ≠ clicked ID after timeout
  Response: Retry once, then skip the card (don't store mismatched data)
  ────────────────────────────────────────
  Failure: Missing description
  Detection: Empty #job-details / JSON
  Response: description_status=missing, match.status=insufficient_data, retry
  detail fetch next scan while in window (detail_attempts < 3)
  ────────────────────────────────────────
  Failure: Missing apply URL
  Detection: No JSON companyApplyUrl, no popup
  Response: Easy Apply: apply URL = LinkedIn URL. External: LinkedIn URL +
  apply_url_resolved=false
  ────────────────────────────────────────
  Failure: LinkedIn DOM changes
  Detection: Above signals
  Response: All selectors in one constant block; HTML fixture tests;
  scan_jobs.py
   --headed for quick diagnosis
  ────────────────────────────────────────
  Failure: PDF missing/unreadable
  Detection: File check at startup and in load-profile; text <300 chars
  Response: Alert once; discovery continues, jobs stored with
  match.status=pending; scoring resumes when fixed
  ────────────────────────────────────────
  Failure: LLM failure
  Detection: Groq exceptions; invalid JSON; Pydantic validation error
  Response: Set Groq(max_retries=3, timeout=30) explicitly (SDK has backoff for
  429/5xx). On persistent failure: match.status=pending, picked up next scan.
  If pending >2 scans: keyword fallback with confidence=low. Never default to 0
  ────────────────────────────────────────
  Failure: DB failure
  Detection: Motor exceptions
  Response: Check Mongo in check-cb before launching the browser (don't burn
  LinkedIn requests). Idempotent upserts make Inngest step retries safe
  ────────────────────────────────────────
  Failure: Slack failure
  Detection: SlackApiError / None ts
  Response: notification.status stays pending, attempts++, retried next scan;
  failed after 5. Use slack_sdk's built-in RateLimitErrorRetryHandler
  ────────────────────────────────────────
  Failure: Duplicates
  Detection: Unique index
  Response: Upsert; DuplicateKeyError swallowed with a log line, never in an
  empty catch
  ────────────────────────────────────────
  Failure: Overlapping runs
  Detection:
  Response: Shared Inngest concurrency key

  ---

  16. Security Plan

  Found in the repo, in priority order:

  1. /slack/actions has no signature verification at all (main.py:122-210).
     Anyone who can reach the tunnel URL can POST connect_poster (queues
     connection requests to arbitrary profiles with LLM notes), trigger_referral
     (starts full outreach campaigns), repost_now and approve_referral_dm. Fix:
     verify the signature and timestamp like /slack/commands does.
  2. _verify_slack_signature fails open when SLACK_SIGNING_SECRET is empty
     (main.py:67-68). Make it fail closed.
  3. Inngest dev mode behind a public tunnel: with INNGEST_IS_PRODUCTION=false,
     the serve endpoint doesn't verify request signatures, so functions
     (scraping, auto-apply) can be invoked by anyone who finds the URL. Only
     tunnel in production mode with a signing key.
  4. Untracked PII not in .gitignore: Vanshaj_resume_.pdf and the
     2026-06-25-…txt transcript (contains an email address). Your /push skill
     stages all changes, so one push commits both. Add *.pdf (or a private/ dir)
     and *.txt transcripts to .gitignore.
  5. output/ is tracked: LinkedIn screenshots and feed_results.json contain
     other people's names and posts. Ignore it and git rm --cached it. History
     stays unless rewritten.
  6. .claude/ is tracked (settings.local.json, spec/plan.md), against your
     global rule. Add .claude/ and CLAUDE.md to .gitignore and untrack them.
  7. state.json is gitignored (good) but sits in plaintext in the repo root.
     li_at equals full account access. Move it outside the repo through
     LINKEDIN_STATE_PATH and never log cookie values. The GitHub Actions secret
     path puts your cookies on datacenter IPs; avoid it.
  8. Resume sent to Groq: the new design redacts contact PII and sends the
     resume once per version. Job scoring never includes resume content.
  9. Prompt injection through JDs: job descriptions are untrusted. Using the LLM
     only for extraction and scoring deterministically limits the damage (it
     could still inject fake skills). Delimit the JD in prompts and validate
     output against the schema.
  10. Logs: no secrets are logged today. Keep resume text, prompts containing
      profile data, and PROXY_URL (may embed credentials) out of prints.
  11. MongoDB: URI only in .env, a least-privilege user, an Atlas IP allowlist.
      Store the profile without contact fields.
  12. .env: gitignored, but its contents couldn't be audited (permission deny).
      Verify yourself that no real values ever went into .env.example (the
      current file has blank values).

  ---

  17. Testing Plan

  (Plan only. Per your rules I won't write tests until you say so. Integration 
  tests should use a real local Mongo test DB, linkedin_automation_test; I'll 
  ask before mocking anything DB-related.)

  Unit (pytest + pytest-asyncio; pure functions, no network):

  Area: Relative-time parser
  Cases: "59 minutes ago" → in; "1 hour ago" → [60,120), in with boundary=true;
  JSON listedAt 60:00 → in, 61:00 → out; "Just now", "30 seconds ago";
  "Reposted 20 minutes ago" → repost flag; "2 days ago" → out; missing →
  search_filter_only; garbage → None
  ────────────────────────────────────────
  Area: Window filter
  Cases: 59 / exactly 60 / 61 min with JSON timestamp; adaptive window clamp
  (3600..86400)
  ────────────────────────────────────────
  Area: Job ID / URL
  Cases: /jobs/view/123/?trk=…, currentJobId=123, data-occludable-job-id,
  relative hrefs, no ID → skip
  ────────────────────────────────────────
  Area: Search URL builder
  Cases: Encoding of quotes/OR/commas, geoId, f_WT/f_E/f_JT combos, start
  ────────────────────────────────────────
  Area: Dedup
  Cases: Same ID twice in one scan; same ID across two searches
  (matched_searches
  merged); repost signature collision
  ────────────────────────────────────────
  Area: Skills
  Cases: Alias normalization, related-skill partial credit, case/punctuation
  ────────────────────────────────────────
  Area: Scoring
  Cases: Golden tests (the worked example = 79), renormalization with no
  preferred skills, each hard-gate cap, insufficient_data on empty description,
   keyword fallback marks low confidence
  ────────────────────────────────────────
  Area: Profile
  Cases: YOE computation with overlapping roles and internships; overrides
  precedence; redaction regexes
  ────────────────────────────────────────
  Area: LLM output validation
  Cases: Valid JSON, missing keys, wrong types, extra keys, non-JSON text
  ────────────────────────────────────────
  Area: Slack blocks
  Cases: Escaping, 50-block / 3000-char limits, link buttons present, Easy Apply

  vs external apply URL choice
  ────────────────────────────────────────
  Area: Config
  Cases: Pipe parsing, empty-string env tolerance

  Integration:
  - Scraper against saved HTML fixtures of a LinkedIn search page and a details
    pane, served through page.route/set_content (offline, zero LinkedIn
    traffic). Covers stale pane, a promoted card, a closed job, Easy Apply vs
    external, empty description, the guest/login page (session-expired path) and
    the checkpoint page.
  - Real Mongo: upsert idempotency, unique index race (two concurrent upserts),
    outbox retry after a simulated Slack failure.
  - LLM: recorded-response fixtures by default, plus one opt-in live Groq smoke
    test (ask first, since it costs tokens). Simulated 429 → pending → retry.
  - PDF: your real resume (text layer present), an image-only PDF (fails
    cleanly), a missing file.

  End-to-end (manual, gated): python scan_jobs.py --headed --window 60 
  --no-slack on the live account with DRY_RUN=true. Then one Inngest-triggered
  run in the dev server posting to a test Slack channel. Check against
  LinkedIn's UI by hand: 10 sampled jobs have the correct URL, title, age and
  apply type.

  ---

  18. Exact File-by-File Implementation Roadmap

  Phase 0: Blockers and safety (small; do first)

  - .gitignore: add *.pdf (or private/), 2026-*.txt, output/, .claude/,
    CLAUDE.md, the candidate overrides file.
    - Why: PII leak risk through /push. Risk: git rm --cached output .claude is
      needed to untrack them; get your confirmation before running it.
  - main.py: apply timestamp + signature checks to /slack/actions; make
    _verify_slack_signature fail closed.
    - Why: unauthenticated outbound LinkedIn actions. Risk: without the secret
      set, Slack buttons stop working until it's configured.
  - config.py: add RESUME_PATH (fall back to APPLICANT_RESUME_PATH) and validate
    that the file exists at startup in main.lifespan (warn, don't crash). Point
    APPLICANT_PROFILE["resume_path"] at it.
    - Why: Easy Apply currently returns needs_human when the path is wrong.
      Connects: browser/easy_apply.py:180.
  - All Chromium-launching Inngest functions
    (agents/{auto_apply,job_hunter,feed_scout,connection,content,referral}.py,
    core/action_queue.py): add concurrency=[inngest.Concurrency(limit=1, 
    key='"linkedin-browser"', scope="env")].
    - Why: concurrent sessions on one cookie jar are a strong bot signal. Risk:
      runs queue up; the queue processor every 5 min can delay scans. Accept
      that, or exempt dry-run.
  - test_recent_jobs.py, test_feed_scout.py: add the missing await (or delete
    them once Phase 5 lands).

  Phase 1: LinkedIn scanner (highest uncertainty, so it goes early)

  - New scrapers/job_parsing.py (pure, no Playwright): build_search_url(...),
    extract_job_id(...), canonical_job_url(id), parse_posted_age(text) -> (min, 
    max, is_repost), compute_freshness(...), normalize_text helpers.
    - Why: unit-testable core logic. Deps: none.
  - scrapers/jobs_recent.py (rewrite internals, keep the module):
    - scan_recent_jobs(searches, window_seconds, known_ids, max_pages, 
      max_details, headless) -> dict running through the existing
      run_in_playwright_thread.
    - Per search: navigate with start=, detect_block_state, collect card stubs
      from li[data-occludable-job-id] (card-scoped), list-pane scroll ported
      from jobs.py:35-48, card-level title exclusion.
    - For new IDs: click the card's title anchor, wait for pane ID match,
      extract top-card fields (title, company, location, workplace/employment
      chips, posted text, applicants) and the full description (no truncation;
      cap ~15k chars).
    - Register a page.on("response") listener to capture job-posting JSON
      (listedAt, applyMethod…), modeled on feed.py:526-546.
    - Fix _detect_apply_type (Easy Apply badge/button; external URL from JSON;
      optional popup capture behind a flag).
    - Return JSON-safe dicts plus {status, block_reason, stats}.
    - Keep the scrape_recent_jobs(...) signature as a thin compat wrapper until
      auto_apply is migrated.
    - Why: fixes the URL/dedup bug, the 24h window, pagination and missing
      fields. Connects: used by agents/job_scanner.py and scan_jobs.py. Risk:
      every selector and the JSON shape need live verification. Build
      scan_jobs.py --headed --debug-dump alongside so you can iterate.
  - browser/manager.py:
    - detect_block_state(page) -> str | None merging validate_session, the
      feed.py text markers, captcha iframes and the guest-layout check.
    - STATE_FILE from LINKEDIN_STATE_PATH.
    - Fail loudly if the state file is missing (today it silently runs logged
      out).
    - Optional save_storage_state(context) after a validated successful scan, to
      keep rotating cookies fresh.
    - Risk: refreshing state while another process reads it. Fine once the
      concurrency key is in place.
  - scrapers/jobs.py: either delete it when job_hunter is retired, or change
    line 73 to card-scoped extraction. I recommend retiring it.

  Phase 2: Resume pipeline

  - requirements.txt: add pypdf>=4.
  - New matching/__init__.py, matching/resume.py:
    load_candidate_profile(force=False):
    - Hash the file, check Mongo candidate_profiles, extract with pypdf,
      normalize (NFKC, de-hyphenate), guard on length, redact PII.
    - Call llm.extract_candidate_profile, compute YOE in code, merge overrides,
      canonicalize skills, upsert the cache.
    - Connects: the scanner's load-profile step and the CLI. Risk: multi-column
      LaTeX layouts can interleave text. Inspect the extracted text once; switch
      to pdfplumber if it's garbled.
  - llm/service.py:
    - extract_candidate_profile(redacted_text) -> dict (temperature 0,
      max_tokens ~1500, JSON mode).
    - Change _groq = Groq(api_key=..., max_retries=3, timeout=30.0).
    - Let _chat_sync accept model, temperature and max_tokens arguments
      (existing callers keep their current values).
    - Why: your rule requires explicit temperature/max_tokens; extraction
      wants 0.
  - db/__init__.py: Pydantic CandidateProfile, CandidateSkill, ExperienceEntry.
    Import config first, before reading MONGODB_URI.
  - config.py: CANDIDATE_PROFILE_OVERRIDES_PATH, GROQ_MODEL from env.

  Phase 3: Matching engine

  - New matching/skills.py: canonical taxonomy (~150-250 skills relevant to your
    stack), alias map, related-skill map with partial credit, role-family
    classifier from titles. Risk: the taxonomy needs curating; unknown skills
    fall back to exact normalized-string matching.
  - llm/service.py: extract_job_requirements(title, company, description) -> 
    dict (temperature 0, ~1200 max_tokens, JSON mode, canonical vocabulary in
    the prompt, JD delimited as untrusted). Leave score_job_post untouched for
    now; delete it in Phase 4 if job_hunter is retired.
  - New matching/scoring.py: SCORING_VERSION="v1"; score_job(profile, 
    requirements, job) -> MatchResult (components, renormalization, gates,
    confidence, matching/missing lists, gaps, template explanation);
    keyword_fallback_requirements(description). Pure and deterministic.
  - db/__init__.py: JobRequirements, MatchResult models, also used to validate
    LLM output.

  Phase 4: Orchestration and persistence

  - db/__init__.py: JobListing, JobScanRun models; setup_indexes() adds the
    Section 12 indexes. Risk: index builds on existing collections are trivial
    at this size.
  - New agents/job_scanner.py: job_scanner_run with the cron from config and the
    shared concurrency key, retries=1. Steps as in Section 5:
    - One scan-<search_key> step per search, so a failure in search 2 doesn't
      redo search 1. Memoized.
    - One match-<job_id> step per new job (Inngest allows up to 1000 steps per
      run, far beyond this).
    - Then notify, hand-off and record-run.
    - On a blocked result: CircuitBreaker.trip(...), alert, raise 
      inngest.NonRetriableError.
    - Also rescore match.status=pending jobs from previous scans.
    - Connects: CircuitBreaker, ActionQueue, slack.bot, matching.*,
      scrapers.jobs_recent. Risk: step outputs must stay JSON-serializable (no
      datetime/ObjectId).
  - main.py: import and add job_scanner_run to ALL_FUNCTIONS; remove
    job_hunter_run; keep auto_apply_run only after the refactor below.
  - agents/auto_apply.py: delete the scraping step; select from job_listings
    where is_easy_apply, match.score ≥ MATCH_SCORE_AUTO_APPLY_THRESHOLD,
    application.status="none"; push easy_apply with job_id; set
    application.status="queued". Alternatively fold this into the scanner's
    hand-off step and delete the function. I'd fold it: fewer moving parts.
    - Connects: core/action_queue._dispatch_action (update db.recent_jobs writes
      at lines 205-219 to job_listings).
    - Risk: auto-apply with DRY_RUN=false now depends on the new score. Keep it
      disabled until calibration.
  - agents/job_hunter.py: retire (generic score, no time filter, URL bug,
    auto-referral on generic scores). The "Trigger Referral" button keeps
    referral manual.

  Phase 5: Output

  - slack/bot.py: CHANNEL_FRESH_JOBS from config; send_fresh_job_alert(job) -> 
    str | None (Section 13 layout, link buttons, mrkdwn escaping);
    send_job_digest(jobs, title); send_alert reused for block/expiry alerts
    (deduplicated: one alert per block event).
  - main.py: mark_applied and dismiss_job keyed by job_id against job_listings
    (keep the legacy URL branch for old messages); optional GET /jobs/recent.
  - New scan_jobs.py (root, like login.py): argparse flags --window, --headed,
    --no-db, --no-slack, --json, --debug-dump; calls the scraper + matching
    directly; prints a table. Replaces test_recent_jobs.py.
  - .env.example: document all Section 14 vars; fix the resume path.

  Phase 6: Hardening

  - job_scan_runs anomaly alerts (0 cards across all searches on 2 consecutive
    scans while the list container is missing → DOM drift alert).
  - Debug snapshots on extraction failure to gitignored output/debug/.
  - Optional job_scan_pages budget in core/budget.py + core/warmup.py.
  - Fix existing crons to use the TZ= prefix (separate change).

  Phase 7: Tests (only after your go-ahead)

  As in Section 17.

  ---

  19. Dependency Changes

  Add:
  - pypdf>=4: resume text extraction (BSD, pure Python, enough for pdfTeX
    output).
  - pytest, pytest-asyncio: pytest.ini already assumes them; dev-only.
  - Optional later: rapidfuzz (fuzzy skill aliasing, only if the alias map
    proves insufficient); pdfplumber (only if pypdf garbles your layout).

  Reuse: groq (set retries/timeout explicitly), motor/pymongo, pydantic (LLM
  output validation), playwright, playwright-stealth, slack_sdk (+
  RateLimitErrorRetryHandler), inngest (concurrency key, TZ= crons,
  NonRetriableError), python-dotenv, certifi.

  Don't add: LangChain/LangGraph (README claims them, but they're not used; not
  needed here), Pinecone or sentence-transformers (YAGNI at this scale; torch is
  heavy), tenacity (Groq SDK retries suffice).

  Remove: nothing required. httpx is used by github_trigger.py but isn't
  declared (it's pulled in transitively); declare it if you keep that path.

  Flag: Playwright 1.44 ships Chromium 125.0.6422.26 while CONSISTENT_USER_AGENT
  claims Chrome/148 (browser/manager.py:58-62). Client Hints /
  navigator.userAgentData will likely report 125, which is a fingerprint
  inconsistency (needs verification). Fix it separately: upgrade Playwright, or
  launch channel="chrome" without overriding the UA. Changing the fingerprint
  likely requires a fresh login.py.

  ---

  20. Final Data Flow

  [Inngest cron, IST, every 20 min, shared browser lock]
    → check circuit breaker + Mongo reachable                      (abort before
  browser if not)
    → load candidate profile (sha256 cache → pypdf → redact → LLM extract once →
  canonicalize)
    → plan window = clamp(now − last_success + 10m, 1h, 24h)
    → load known job_ids (48h)
    → for each search (OR-query × geo × filters):
          LinkedIn /jobs/search?…&f_TPR=r<window>&sortBy=DD&start=0..N
          → block/session check (expired/checkpoint ⇒ trip breaker, alert, stop)
          → card stubs via li[data-occludable-job-id] (card-scoped
  id/title/company/age)
          → title exclusions → skip known ids → shared in-scan seen set
          → detail fetch (click title, wait pane==id) + passive JSON capture
    → timestamp resolution (JSON listedAt > relative text range > filter-only) →
  freshness label
    → upsert job_listings by job_id (first_seen/last_seen/matched_searches,
  repost signature)
    → per new/pending job:
          extract requirements (LLM, temp 0, cached by description_hash;
  fallback keywords)
          → normalize skills → deterministic score v1 + gates + confidence +
  explanation
          → job_listings.match
    → notify (outbox): fresh ∧ score ≥ 70 → per-job Slack; 50-69 + missed_window
  → digest
    → hand-off: Easy Apply ∧ score ≥ 80 ∧ not applied → ActionQueue(easy_apply)
  (budgets, DRY_RUN apply)
    → record job_scan_runs (counts, errors, window, duration)
  [Slack buttons] → /slack/actions (signed) → job_listings.application /
  referral event
  [CLI] scan_jobs.py → same scraper + matching → table/JSON

  ---

  21. Risks and Limitations

  - LinkedIn ToS: the User Agreement prohibits scraping and automation. Account
    restriction is a real, unmitigable risk; frequency is the biggest lever you
    control. A 20-min cadence is much more aggressive than anything the project
    does today.
  - Completeness: discovery is bounded by your searches, LinkedIn's
    ranking/personalization, the ~1000-result cap and promoted injection. "All
    jobs posted in the last hour" isn't achievable; "most jobs matching my
    searches" is.
  - Timestamp accuracy: relative text can't distinguish 60 from 119 minutes.
    Only listedAt from JSON gives exact ages, and its availability is
    unverified. Reposts reset listing time.
  - f_TPR=r3600: undocumented; LinkedIn could ignore or change it at any time.
    The client-side filter is the backstop.
  - External apply URLs: often only obtainable by clicking Apply (side effects)
    or from undocumented JSON. Some are tracking redirects, some expire, closed
    jobs have none.
  - Anti-bot: headless detection, the UA/engine mismatch, concurrent sessions
    across agents (until the lock exists), datacenter IPs if run on GitHub
    Actions, periodic timing. A checkpoint can block all agents, since they
    share one session.
  - Session lifetime: state.json is from Jun 7 and may already be invalid.
    Expiry needs a manual login.py, so it can't be automated without storing
    credentials (don't).
  - LLM consistency: extraction can vary between runs. Caching per description
    hash freezes it, but the first extraction can still be wrong (e.g. a
    preferred skill classified as required). Llama 3.3 70B on Groq may be
    deprecated; verify availability. Groq rate limits (requests/min and
    tokens/day, depending on your plan) cap how many new jobs per day get
    scored; pending-retry absorbs bursts.
  - DOM churn: LinkedIn has been rolling out redesigned job search experiences.
    All selectors in this plan need live verification, and they will break
    again.
  - Rate limits: Slack ~1 msg/s per channel (digest mitigates); Groq as above;
    LinkedIn unknown and adaptive.
  - Adjacent existing bug: browser/interactions.py functions
    (like/comment/connect/DM/repost) and get_browser_page are not wrapped in
    run_in_playwright_thread. Under python main.py (uvicorn reload=True forces a
    Selector loop on Windows), the queue processor's non-Easy-Apply actions can
    still hit NotImplementedError. Easy Apply is wrapped. Out of scope here,
    but it affects anything the scanner hands to the queue except Easy Apply.

  ---

  22. Definition of Done

  - [ ] /slack/actions rejects unsigned requests; signature check fails closed
    without a secret.
  - [ ] Resume, transcripts, output/, .claude/, CLAUDE.md gitignored and
    untracked.
  - [ ] All browser-launching Inngest functions share one concurrency key; no
    two Chromium sessions overlap (checked in the Inngest UI).
  - [ ] Live verification: 10 sampled jobs from one scan have the correct, 
    distinct LinkedIn URLs, titles, companies, locations, apply types and ages,
    matching LinkedIn's UI.
  - [ ] Pagination goes beyond page 1 when results exceed 25; list-pane scroll
    renders all cards.
  - [ ] f_TPR window is configurable and the client-side age filter enforces
    JOB_POSTED_WITHIN_MINUTES; posted_at_source recorded for every job.
  - [ ] Expired session and checkpoint each produce exactly one Slack alert, a
    red breaker, and no retries (tested by deleting/corrupting a copy of the
    state file).
  - [ ] Resume parses into a cached profile; changing the PDF triggers
    re-extraction; unchanged PDF makes zero LLM calls.
  - [ ] No resume text or contact PII appears in LLM job-scoring prompts, logs
    or Mongo.
  - [ ] Re-scoring the same job with the same profile and scoring version gives
    the identical score and breakdown.
  - [ ] Every scored job has score, breakdown, matching skills, missing
    required/preferred, gaps, explanation, confidence; missing descriptions
    yield insufficient_data, never 0.
  - [ ] LLM outage → jobs stay pending and are scored on a later scan.
  - [ ] Same job across 2 searches and 3 scans → one document, one notification,
    matched_searches has both.
  - [ ] Slack per-job alert matches the agreed format; Apply/LinkedIn buttons
    open URLs; Mark Applied/Dismiss update the job; a failed Slack send is
    retried.
  - [ ] python scan_jobs.py --headed --no-slack prints the table end to end.
  - [ ] Adaptive window catches up after a simulated 3-hour downtime, with those
    jobs labeled missed_window.
  - [ ] job_hunter retired; auto-apply consumes scanner results; LinkedIn page
    loads per day measured and within the chosen budget.
  - [ ] New env vars documented in .env.example; README updated.
  - [ ] Unit + integration suites (Section 17) green, after you approve writing
    them.

  ---

  Two things I couldn't verify: your .env values (permission rule blocked the
  read) and anything on live LinkedIn. Every selector, URL parameter and JSON
  field above is marked needs verification for that reason. If you want, I can
  save this plan as a shareable page.

✻ Baked for 12m 31s · done 7:02 PM

※ recap: I audited the repo and wrote a no-code plan for a 1-hour LinkedIn job scanner that scores jobs against your resume. Next, you choose whether I start with Phase 0: Slack signature checks, gitignore fixes and the shared browser lock. (disable recaps in /config)