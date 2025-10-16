#!/usr/bin/env python3
"""
Demo script for FedEx Site Selection Agent.
Interactive CLI for testing site selection queries.
"""

import asyncio
import os
from dotenv import load_dotenv
from fedex_analytics_agent.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Load environment variables
load_dotenv()


def print_banner():
    """Print welcome banner."""
    print("=" * 80)
    print("🚚 FedEx Site Selection Intelligence Agent")
    print("=" * 80)
    print("\nHelp businesses find optimal locations using shipment data analysis\n")
    print("📝 Example Queries:")
    print('  • "Show me cities with highest growth in pet supply shipments"')
    print('  • "Compare electronics demand between Austin, TX and Nashville, TN"')
    print('  • "Find high-demand areas for pet supplies in Arizona"')
    print('  • "What are the top zip codes in California?"')
    print("\n" + "=" * 80 + "\n")


async def main():
    """Run interactive demo."""
    print_banner()
    
    print("🔄 Initializing agent...")
    
    # Create runner
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="demo_user"
    )
    
    print("✅ Agent ready! Type 'help' for examples, 'quit' to exit.\n")
    
    # Interactive loop
    while True:
        try:
            user_input = input("💬 You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Thank you for using FedEx Site Selection Agent!")
                break
            
            if user_input.lower() in ['help', 'examples', '?']:
                print("\n📝 Example Queries:")
                print('  • "Show me top 10 cities by shipment volume in Texas"')
                print('  • "Analyze pet supply demand in Arizona"')
                print('  • "What are the fastest growing markets for electronics?"')
                print('  • "Compare Los Angeles and Chicago shipment volumes"')
                print('  • "Find underserved areas for health products in California"')
                print('  • "What product categories are available?"\n')
                continue
            
            # Send to agent
            content = UserContent(parts=[Part(text=user_input)])
            print("\n🤖 Agent: ", end="", flush=True)
            
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content.parts and event.content.parts[0].text:
                    print(event.content.parts[0].text, end="", flush=True)
            
            print("\n")  # New line after response
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Type 'quit' to exit.")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again or type 'help' for examples.\n")


if __name__ == "__main__":
    # Ensure required env vars are set
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
    os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "us-central1")
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "1")
    os.environ.setdefault("GCP_PROJECT_ID", "agent-space-465923")
    
    asyncio.run(main())
