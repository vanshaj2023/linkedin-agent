import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import config


def send_referral_email(to_email: str, to_name: str, company: str, role: str) -> bool:
    """
    Sends a referral request email via Gmail SMTP.
    Returns True on success, False on failure.
    When DRY_RUN=True, logs the email instead of sending it.
    """
    if config.DRY_RUN:
        print(
            f"[DRY RUN] Would send referral email:\n"
            f"  To: {to_name} <{to_email}>\n"
            f"  Subject: Quick ask — {role} role at {company}"
        )
        return True

    if not config.GMAIL_USER or not config.GMAIL_APP_PASSWORD:
        print("GMAIL_USER or GMAIL_APP_PASSWORD not configured. Skipping email.")
        return False

    subject = f"Quick ask — {role} role at {company}"
    html_body = f"""
<p>Hi {to_name},</p>

<p>Hope you're doing well! I've been following your work and really admire what the team
at {company} is building.</p>

<p>I noticed there's an open <strong>{role}</strong> position, and it looks like a great fit
for my background in {config.YOUR_DOMAIN}. I'd love to know if you'd be open to referring me
or just sharing any thoughts about the team culture.</p>

<p>No pressure at all — just thought I'd reach out since we connected recently.</p>

<p>Thanks so much,<br>
{config.YOUR_NAME}<br>
{config.YOUR_EMAIL}</p>
"""
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = config.GMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config.GMAIL_USER, config.GMAIL_APP_PASSWORD)
            server.sendmail(config.GMAIL_USER, to_email, msg.as_string())

        print(f"Referral email sent to {to_name} <{to_email}>")
        return True
    except Exception as e:
        print(f"Failed to send referral email to {to_name}: {e}")
        return False
