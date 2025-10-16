#!/usr/bin/env python3
"""Quick single-query test for FedEx agent."""

import asyncio
import os
from dotenv import load_dotenv
from fedex_analytics_agent.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

load_dotenv()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")
os.environ.setdefault("GCP_PROJECT_ID", "agent-space-465923")


async def main():
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="user"
    )
    
    # Change this query to test different things
    query = "Show me the top 5 cities by shipment volume"
    
    print(f"\n💬 Query: {query}\n")
    print("🤖 Agent: ", end="", flush=True)
    
    content = UserContent(parts=[Part(text=query)])
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text, end="", flush=True)
    
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())

