import os
from dotenv import load_dotenv

load_dotenv()


def _env_int(name: str, default: int) -> int:
    """Read an int env var with empty-string tolerance (Docker / CI footgun)."""
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


class Config:
    # --- LLM ---
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_VISION_MODEL: str = os.getenv("OPENAI_VISION_MODEL", "gpt-4o")

    # --- Slack ---
    SLACK_BOT_TOKEN: str = os.getenv("SLACK_BOT_TOKEN", "")
    SLACK_SIGNING_SECRET: str = os.getenv("SLACK_SIGNING_SECRET", "")

    # --- Gmail SMTP ---
    GMAIL_USER: str = os.getenv("GMAIL_USER", "")
    GMAIL_APP_PASSWORD: str = os.getenv("GMAIL_APP_PASSWORD", "")

    # --- MongoDB ---
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

    # --- Inngest ---
    INNGEST_SIGNING_KEY: str = os.getenv("INNGEST_SIGNING_KEY", "")
    INNGEST_EVENT_KEY: str = os.getenv("INNGEST_EVENT_KEY", "")
    INNGEST_IS_PRODUCTION: bool = _env_bool("INNGEST_IS_PRODUCTION", False)

    # --- System flags ---
    DRY_RUN: bool = _env_bool("DRY_RUN", True)
    WARMUP_WEEK: int = _env_int("WARMUP_WEEK", 1)

    # --- Targeting ---
    TARGET_KEYWORDS: list = [
        k.strip() for k in os.getenv(
            "TARGET_KEYWORDS", "hiring,software engineer,backend developer"
        ).split(",")
    ]
    TARGET_JOB_KEYWORDS: list = [
        k.strip() for k in os.getenv(
            "TARGET_JOB_KEYWORDS", "software engineer,backend developer,full stack developer"
        ).split(",")
    ]
    TARGET_JOB_LOCATIONS: list = [
        k.strip() for k in os.getenv(
            "TARGET_JOB_LOCATIONS", "India,Remote"
        ).split(",")
    ]
    AUTO_REPOST_SCORE_THRESHOLD: int = _env_int("AUTO_REPOST_THRESHOLD", 90)
    CONNECTION_RELEVANCE_THRESHOLD: int = _env_int("CONNECTION_THRESHOLD", 60)
    JOB_SLACK_NOTIFY_THRESHOLD: int = _env_int("JOB_SLACK_THRESHOLD", 70)

    # --- Your profile ---
    YOUR_DOMAIN: str = os.getenv("YOUR_DOMAIN", "AI and backend engineering")
    YOUR_NAME: str = os.getenv("YOUR_NAME", "")
    YOUR_EMAIL: str = os.getenv("YOUR_EMAIL", "")

    # --- Applicant details for Easy Apply forms ---
    APPLICANT_PROFILE: dict = {
        "phone": os.getenv("APPLICANT_PHONE", ""),
        "years_experience": _env_int("APPLICANT_YOE", 1),
        "current_role": os.getenv("APPLICANT_ROLE", ""),
        "resume_path": os.getenv("APPLICANT_RESUME_PATH", "./resume.pdf"),
        "linkedin_url": os.getenv("APPLICANT_LINKEDIN_URL", ""),
        "github_url": os.getenv("APPLICANT_GITHUB_URL", ""),
        "salary_expectation": os.getenv("APPLICANT_SALARY", "Negotiable"),
        "willing_to_relocate": _env_bool("APPLICANT_RELOCATE", False),
        "requires_sponsorship": _env_bool("APPLICANT_SPONSORSHIP", False),
    }


config = Config()
