
import os
import asyncio
import litellm
from crewai import Agent, Task, Crew, LLM

original_completion = litellm.completion
def modified_completion(*args, **kwargs):
    if "messages" in kwargs:
        for message in kwargs["messages"]:
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)
    return original_completion(*args, **kwargs)
litellm.completion = modified_completion

original_acompletion = litellm.acompletion
async def modified_acompletion(*args, **kwargs):
    if "messages" in kwargs:
        for message in kwargs["messages"]:
            if isinstance(message, dict):
                message.pop("cache_breakpoint", None)
    return await original_acompletion(*args, **kwargs)
litellm.acompletion = modified_acompletion


os.environ["CREWAI_DISABLE_PROMPT_CACHING"] = "true"
groq_key = "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"

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=groq_key,
    temperature=0.2 # Lowered temperature slightly for stricter instruction adherence
)

# ── SCOUT AGENT ──
scout = Agent(
    role="Financial Literacy Coach",
    goal="Educate members on harvest-cycle planning and detect financial stress signals",
    backstory="""You are a supportive financial coach for Ujima SACCO members in Kenya. 
    You understand matooke and maize harvest cycles (March/April and Sept/Oct). 
    You never recommend specific loans. You send maximum 3 SMS per day per member. 
    If a member mentions loan sharks or school fees stress, you output a clear escalation alert.
    DO NOT attempt to call any external tools or delegate work.""",
    verbose=True,
    allow_delegation=False, # DISABLED TO PREVENT TOOL CRASH
    llm=llm 
)

# ── GUARDIAN AGENT ──
guardian = Agent(
    role="Loan Triage Officer",
    goal="Screen Tier-1 loan applications and escalate complex cases to the Hunter Agent",
    backstory="""You are a fair loan screening officer for Ujima SACCO. 
    You approve loans up to KES 15,000 with fewer than 2 risk flags. 
    You NEVER approve or deny based on gender or occupation stereotypes. 
    You consider seasonal income variance from harvest cycles before making decisions. 
    Your sole task here is to write down the risk assessment packet. 
    DO NOT attempt to call tools, call functions, or execute manual delegations.""",
    verbose=True,
    allow_delegation=False, # DISABLED TO PREVENT TOOL CRASH
    llm=llm 
)

# ── HUNTER AGENT ──
hunter = Agent(
    role="Human-in-Loop Coordinator",
    goal="Prepare detailed briefing packets for human loan officers",
    backstory="""You coordinate between AI screening and human loan officers at Ujima SACCO. 
    You NEVER approve or deny loans yourself. You only prepare clear, empathetic briefing packets 
    for human officers. You match applications to officers with relevant expertise. 
    You always frame applicants with dignity — never using words like 'risky' or 'unreliable'.
    DO NOT attempt to call tools or delegate.""",
    verbose=True,
    allow_delegation=False, # RECONSTRUCTED
    llm=llm 
)

# ── TASKS ──
scout_task = Task(
    description="""A member named Grace, 42, maize farmer in Kakamega has sent this SMS: 
    'No money for school fees. Harvest not until October. Please help.'
    
    1. Identify her financial stress signal
    2. Note her next harvest date (October)
    3. Check if this needs to be escalated to the Guardian Agent
    4. Draft a supportive SMS response in simple English (max 3 sentences)""",
    agent=scout,
    expected_output="Financial stress analysis and SMS draft, with escalation recommendation"
)

guardian_task = Task(
    description="""Grace has submitted a loan application:
    - Name: Grace Akinyi, 42, maize farmer, Kakamega
    - Requested amount: KES 28,000
    - Purpose: School fees for 3 children (ages 6, 9, 14)
    - Income: KES 12,000/month average, spikes to KES 35,000 during October harvest
    - Transaction history: Regular savings deposits, no missed payments
    - Risk flags: Loan exceeds KES 15,000
    
    Using only text, execute these steps:
    1. Assess the application against harvest-cycle income
    2. Identify all risk flags
    3. Since amount exceeds KES 15,000, prepare the final textual assessment to pass forward.""",
    agent=guardian,
    expected_output="Risk assessment with harvest-cycle analysis and text-based handoff packet data"
)

hunter_task = Task(
    description="""Prepare a briefing packet for a human loan officer reviewing Grace's application.
    The previous context provided to you contains:
    - Applicant: Grace Akinyi, 42, maize farmer, Kakamega
    - Request: KES 28,000 for school fees
    - Income peaks in October/November harvest season
    - 3 children (ages 6, 9, 14)
    - No risk flags beyond loan amount
    - Recommended officer: Sarah (specialist in maize farmers)
    
    1. Write a dignified, empathetic briefing packet for Officer Sarah
    2. Suggest a harvest-aligned repayment schedule
    3. Note any cross-sell opportunities (e.g., drought insurance)
    4. Confirm human review is required before any decision""",
    agent=hunter,
    expected_output="Complete officer briefing packet with repayment schedule and dignity-centered framing"
)

# ── CREW ──
ujima_crew = Crew(
    agents=[scout, guardian, hunter],
    tasks=[scout_task, guardian_task, hunter_task],
    verbose=True
)

# ── RUN ──
print("=" * 60)
print("UJIMA SACCO — AGENT PRIDE PROTOTYPE")
print("Scout → Guardian → Hunter Handoff Simulation")
print("=" * 60)

try:
    result = ujima_crew.kickoff()
    print("\n" + "=" * 60)
    print("FINAL OUTPUT:")
    print("=" * 60)
    print(result)
except Exception as e:
    print(f"\n❌ Execution Failed: {e}")
