"""Holland Knight Legal Multi-Agent System"""

from google.adk.agents import Agent

from holland_knight import prompt
from holland_knight.sub_agents.legal_qa.agent import legal_qa_agent
from holland_knight.sub_agents.document_generation.agent import document_generation_agent


root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="Holland Knight Legal Multi-Agent System - coordinates legal Q&A and document generation",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        legal_qa_agent,
        document_generation_agent,
    ],
)
