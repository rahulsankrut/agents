#!/usr/bin/env python3
"""
Test script for FedEx Site Selection Agent.
Run simple queries to verify the agent works.
"""

import asyncio
import os
from dotenv import load_dotenv
from fedex_analytics_agent.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Load environment
load_dotenv()

# Set required env vars
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")
os.environ.setdefault("GCP_PROJECT_ID", "agent-space-465923")


async def test_agent(query: str):
    """Run a test query."""
    print(f"\n{'='*80}")
    print(f"Query: {query}")
    print('='*80)
    
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    
    content = UserContent(parts=[Part(text=query)])
    print("\nResponse: ", end="", flush=True)
    
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text, end="", flush=True)
    
    print("\n")


async def main():
    """Run test queries."""
    print("\n🚚 FedEx Site Selection Agent - Test Suite")
    print("="*80)
    
    test_queries = [
        "Show me the top 5 cities by shipment volume",
        "What are the top zip codes in California?",
        "Analyze pet supply demand in Arizona",
        "Compare Los Angeles and Chicago shipment volumes",
    ]
    
    print("\nRunning test queries...\n")
    
    for query in test_queries:
        await test_agent(query)
        await asyncio.sleep(1)  # Brief pause between queries
    
    print("="*80)
    print("✅ All tests complete!")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())

