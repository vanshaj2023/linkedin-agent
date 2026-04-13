import os
import random
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

# We use structured output for scoring
class ProfileEvaluation(BaseModel):
    relevance_score: int = Field(description="Score from 0 to 100 on how relevant this person is for networking")
    reasoning: str = Field(description="Why this score was given")
    personalized_note: str = Field(description="A connection note under 280 characters based on the template")
    template_used: str = Field(description="The ID of the template you were asked to use")

# Initialize LLM
llm = ChatOpenAI(temperature=0.7, model="gpt-4o") # Using gpt-4o for nuanced reasoning
evaluator_llm = llm.with_structured_output(ProfileEvaluation)

TEMPLATES = {
    "T1_DOMAIN": "Hi {name}, noticed your work in {domain} at {company}. I'm also exploring this space and would love to connect and follow your updates!",
    "T2_CASUAL": "Hey {name}! Came across your profile while looking at {domain} leaders. Really impressed by your background. Let's connect!",
    "T3_PEER": "Hi {name}, I'm building my network with other professionals in {domain} and your experience at {company} stood out. Would be great to connect.",
    "T4_LEARNER": "Hi {name}, as someone interested in {domain}, I regularly look for experienced folks like yourself to learn from. Would love to stay connected.",
    "T5_DIRECT": "Hey {name}, great to see your work at {company} in {domain}. I'm expanding my network here and would love to add you."
}

def rotate_template():
    """Selects a random template for A/B testing."""
    key = random.choice(list(TEMPLATES.keys()))
    return key, TEMPLATES[key]

async def score_and_generate_note(name: str, headline: str, company: str, target_domain: str) -> dict:
    """
    Evaluates a profile's relevance to the target_domain.
    If relevant, drafts a personalized connection note based on a rotated template.
    """
    template_id, template_text = rotate_template()
    
    prompt = f"""
    You are an expert networking assistant evaluating a LinkedIn profile for a user who works in or is interested in '{target_domain}'.
    
    Profile Details:
    - Name: {name}
    - Headline: {headline}
    - Company / Location: {company}
    
    Task 1: Score Relevance (0-100)
    How valuable is this connection for someone in the {target_domain} space? Consider if they are a peer, hiring manager, or industry leader.
    
    Task 2: Personalize Connection Note
    Use the following template structure, replacing placeholders and adapting it so it sounds completely natural, human, and conversational. Do not sound salesy. 
    It MUST be under 280 characters.
    
    Template Instruction (ID: {template_id}):
    {template_text}
    """
    
    # We use invoke because we wrapped the model in structure output
    response: ProfileEvaluation = await evaluator_llm.ainvoke(prompt)
    
    return {
        "score": response.relevance_score,
        "reasoning": response.reasoning,
        "note": response.personalized_note,
        "template_id": template_id
    }

# Tester
if __name__ == "__main__":
    import asyncio
    async def test():
        res = await score_and_generate_note(
            name="John Smith", 
            headline="Senior Backend Engineer | Specialized in distributed systems", 
            company="Stripe", 
            target_domain="Backend Engineering & Distributed Systems"
        )
        print("Score:", res["score"])
        print("Reason:", res["reasoning"])
        print("Note:", res["note"])
        print("Template:", res["template_id"])
        
    asyncio.run(test())
