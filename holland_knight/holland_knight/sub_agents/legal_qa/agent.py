"""Legal Q&A Agent for Holland Knight"""

from google.adk.agents import Agent

from holland_knight.sub_agents.legal_qa import prompt
from holland_knight.tools import court_listener_search


legal_qa_agent = Agent(
    model="gemini-2.5-flash",
    name="legal_qa_agent",
    description="Specialized agent for answering legal questions and researching case law",
    instruction=prompt.LEGAL_QA_INSTR,
    tools=[court_listener_search],
)
