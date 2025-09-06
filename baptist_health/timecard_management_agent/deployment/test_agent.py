"""Simple test agent for deployment verification."""

from google.adk import Agent

# Create a simple test agent
test_agent = Agent(
    model="gemini-2.0-flash-exp",
    instruction="You are a helpful assistant that can answer questions about timecard management.",
    name="Test_Timecard_Agent",
    tools=[],
)
