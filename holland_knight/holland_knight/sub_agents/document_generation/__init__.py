"""Document Generation Agent for Holland Knight"""

from google.adk.agents import Agent

from holland_knight.sub_agents.document_generation import prompt


document_generation_agent = Agent(
    model="gemini-2.5-flash",
    name="document_generation_agent",
    description="Specialized agent for generating legal documents and contracts",
    instruction=prompt.DOCUMENT_GENERATION_INSTR,
)
