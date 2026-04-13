from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from typing import Optional

class JobEvaluation(BaseModel):
    relevance_score: int = Field(description="Score 0-100 indicating how closely this job matches the user's background and goals.")
    reasoning: str = Field(description="Why this score was given, focusing on key skills mentioned.")
    should_comment_email: bool = Field(description="If the job poster explicitly asks people to comment or email their resume in the description.")
    comment_text: Optional[str] = Field(description="If we should comment, the text to comment. Usually expressing interest and saying 'Sent!'. Leave null if not needed.")
    company_for_referral: Optional[str] = Field(description="The exact name of the company if the score is > 80, otherwise null. We will use this to trigger the Referral Agent.")

llm = ChatOpenAI(temperature=0.3, model="gpt-4o")

async def score_job_relevance(job_title: str, company: str, description: str, target_profile: str) -> dict:
    """Evaluates a job description against the user's target profile for routing."""
    evaluator_llm = llm.with_structured_output(JobEvaluation)
    
    prompt = f"""
    You are an expert career strategist. Evaluate the following job posting against your client's profile.
    
    Client Profile: {target_profile}
    
    Job Title: {job_title}
    Company: {company}
    Description: {description[:3000]}
    
    Task:
    1. Provide a relevance_score (0-100). Be highly critical. Only score >80 if it perfectly matches the client's tier, seniority, and tech stack.
    2. Read carefully to see if the poster asks candidates to "comment below for a referral", "comment interested", or "email me your resume". If so, set should_comment_email to True.
    3. Generate a short polite comment if requested by the poster (e.g. "I'm very interested, just sent you an email!").
    4. Provide the company name if we should look for a referral later.
    """
    
    response: JobEvaluation = await evaluator_llm.ainvoke(prompt)
    return response.model_dump()
