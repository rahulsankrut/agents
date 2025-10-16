#!/usr/bin/env python3
"""
Demo script for the presentation chatbot.
"""

import asyncio
import logging
from presentation_chatbot.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """Run the presentation chatbot demo."""
    print("🎯 Presentation Chatbot Demo")
    print("=" * 50)
    print("This chatbot will help you create a PowerPoint presentation!")
    print("I'll ask you a few questions to collect the necessary information.")
    print("=" * 50)
    
    # Create runner
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="demo_user"
    )
    
    # Start the conversation
    content = UserContent(parts=[Part(text="Hello! I'd like to create a PowerPoint presentation. Can you help me?")])
    
    print("\n🤖 Bot: ", end="")
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].text:
            print(event.content.parts[0].text, end="")
    print()  # New line after bot response
    
    # Interactive conversation loop
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("\n🤖 Bot: Thank you for using the presentation chatbot! Goodbye!")
                break
            
            if not user_input:
                continue
                
            # Get response from agent
            content = UserContent(parts=[Part(text=user_input)])
            print("🤖 Bot: ", end="")
            async for event in runner.run_async(
                user_id=session.user_id,
                session_id=session.id,
                new_message=content,
            ):
                if event.content.parts and event.content.parts[0].text:
                    print(event.content.parts[0].text, end="")
            print()  # New line after bot response
            
        except KeyboardInterrupt:
            print("\n\n🤖 Bot: Goodbye! Thanks for using the presentation chatbot!")
            break
        except Exception as e:
            logger.error(f"Error in conversation: {e}")
            print(f"\n🤖 Bot: Sorry, I encountered an error. Please try again.")


if __name__ == "__main__":
    asyncio.run(main())
