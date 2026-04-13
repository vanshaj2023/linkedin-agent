from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class ReferralMessages(BaseModel):
    connection_note: str = Field(description="A highly personalized, extremely brief (<200 char) connection note. State polite interest in their engineering culture or recent work. Do NOT ask for a referral yet. Just aiming to connect.")
    follow_up_message: str = Field(description="The follow up message to send a day after they accept. Be humble, mention you are exploring roles at their company, and politely ask if they'd be open to a brief chat or if they'd be comfortable pointing you in the right direction. (<500 char)")

llm = ChatOpenAI(temperature=0.5, model="gpt-4o")

async def generate_referral_sequence(target_name: str, headline: str, company: str, matched_role: str, client_profile: str) -> dict:
    """Generates the dual-message drip setup for a referral target."""
    evaluator_llm = llm.with_structured_output(ReferralMessages)
    
    prompt = f"""
    You are an expert technical recruiter coaching an engineer on networking.
    Your client profile: {client_profile}
    
    The target engineer you want a referral from:
    Name: {target_name}
    Headline: {headline}
    Company: {company}
    Role: {matched_role}
    
    Task:
    Draft a tight two-step drip sequence to eventually secure a referral from this person.
    1. A connection note (Day 1). It MUST be engaging, non-salesy, and purely about them or the tech at {company}.
    2. A follow-up message (Day 2 after acceptance). Explain you are looking at roles at {company} and ask politely if they'd be open to chatting or referring you if they feel comfortable.
    
    Do not use placeholders like [Your Name]. Just write the message bodies directly.
    """
    
    response: ReferralMessages = await evaluator_llm.ainvoke(prompt)
    return response.model_dump()
