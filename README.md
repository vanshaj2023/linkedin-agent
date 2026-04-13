# LinkedIn AI Agent

An automated agent powered by **Playwright** and **LangChain** to autonomously search for hiring posts, extract relevant profile details (authors, founders, senior engineers), and perform intelligent connections, reactions, and comments using an LLM.

## Project Structure

* `login.py`: An interactive script that opens a browser for manual login and saves the authenticated cookies to `state.json`.
* `browser_manager.py`: A utility that re-uses the `state.json` file to launch headless/headed browsers for automated tasks, bypassing login walls.
* `state.json` (auto-generated): Contains local cookies for LinkedIn authentication.

## Setup Instructions

1. **Install Requirements:**
   ```bash
   pip install playwright langchain langchain-openai langgraph pytest
   playwright install
   ```

2. **Login Setup:**
   Run the initial login script to generate your session state:
   ```bash
   python login.py
   ```
   *Follow the terminal instructions, log in through the visible browser, and press Enter in the terminal to save your state.*

*(Further instructions mapping to Phase 2 and 3 will be deposited here as we build them out).*

## Progress
### Phase 1: Foundation (Completed)
- MongoDB integration implemented using `database.py` with full Pydantic schemas.
- Playwright Stealth wrapper mapped inside `browser_manager.py`.
- Core Global Action Queue (`action_queue.py`) built to centralize & rate limit requests.
- System Health, Circuit Breaker, and Budget Managers built inside `system_health.py` and `warmup.py`.
- Slack integration commands `/status` and `/pause` mocked in `slack_bot.py`.
- Dry run parameters structured securely into schemas.

### Phase 2: Connection Agent (Completed)
- LinkedIn people search scraper (`people_scraper.py`) to bypass layout limitations.
- Robust LLM integration (`llm_scorer.py`) utilizing LangChain and `gpt-4o` for relevance scoring and A/B template personalization notes.
- Agent Orchestration (`agent_connection.py`) parsing scrapes, verifying deductibles against `db.connections`, executing relevance checks, and pushing rate-limited connect actions into MongoDB queue.
- Acceptance Poller (`acceptance_poller.py`) scraping new connections and recording acceptances back into state.

### Phase 3: Content Agent (Completed)
- Organic feed extraction scraper (`content_scraper.py`), supporting dynamic user sub-page target extractions.
- LLM interaction evaluation module (`content_scorer.py`) utilizing LangChain's structured output wrappers to evaluate posts on a 0-100 rubric, assessing high-quality viral properties or producing deep conversational comments based on post contexts.
- Digest dispatching functionality in `slack_bot.py` to organize morning notifications of potential reposts straight to Slack workspace channels for review.
- High-level orchestration wrapper (`agent_content.py`) mapping auto-reactions against the `engage_list`, scheduling likes and LLM-generated comments automatically without bypassing budget constraints.

### Phase 4: Job Hunter Agent (Completed)
- Job extraction mechanism (`job_scraper.py`), configured to extract detailed job components directly from the dynamic search pane layout.
- AI relevance layer (`job_scorer.py`) leveraging LLMs to cross-match candidate profile keywords, scoring job fit objectively between 0-100 logic thresholds. 
- Integrated `#job-alerts` Slack pipeline within `slack_bot.py` triggering instantaneous interactive job posts for roles scoring over a specific threshold.
- Action-queue bridging in `agent_job_hunter.py` queuing an organic "I've applied / sent my resume!" comment action directly below the poster's post if manually requested in the actual job descriptions.

### Phase 5: Referral Agent (Completed)
- Direct employee extraction wrapper (`referral_scraper.py`) to bypass 1st-degree constraints and locate exact ICs (Individual Contributors) within targeted prospect companies.
- Context-aware LLM mapping model (`referral_scorer.py`) strictly structured via LangChain to draft authentic two-step Drip configurations: a no-ask non-sales connection request, and a humble ask-for-chat follow up depending on logic flow.
- The `agent_referral.py` execution orchestrator. This manages initializing wide net campaigns across Slack monitoring (`#referral-campaigns`) and schedules the Day-2 follow ups dynamically measuring 20+ hour delays precisely after your previous connections convert/accept through the global `acceptance_poller.py`. Drip interactions are pipelined directly to the central Action Queue buffer avoiding limit thresholds.

#   L i n k e d i n - M a r k e t i n g   