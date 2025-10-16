#!/usr/bin/env python3
"""
Demo script for the Storybook Agent
This script demonstrates the various capabilities of the storybook agent.
"""

import os
from dotenv import load_dotenv
from agent import root_agent

def main():
    """Main demo function showcasing the storybook agent capabilities."""
    
    # Load environment variables
    load_dotenv()
    
    print("🌟 Welcome to the Storybook Agent Demo! 🌟")
    print("=" * 50)
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key and try again.")
        return
    
    print("✅ API key loaded successfully!")
    print("\n🎭 Let's create some stories together!\n")
    
    try:
        # Demo 1: Generate story ideas
        print("📚 Demo 1: Generating Story Ideas")
        print("-" * 30)
        ideas_result = root_agent.tools[5](genre="fantasy", theme="adventure")
        if ideas_result["status"] == "success":
            print("✨ Generated story ideas:")
            for i, idea in enumerate(ideas_result["ideas"], 1):
                print(f"  {i}. {idea}")
        print()
        
        # Demo 2: Create a fantasy story
        print("📖 Demo 2: Creating a Fantasy Story")
        print("-" * 30)
        story_result = root_agent.tools[0](
            title="The Dragon's Heart",
            genre="fantasy",
            main_character="brave knight",
            setting="enchanted castle",
            plot_points=3
        )
        if story_result["status"] == "success":
            story = story_result["story"]
            print(f"📖 Story created: {story['title']}")
            print(f"🎭 Genre: {story['genre']}")
            print(f"👤 Character: {story['main_character']}")
            print(f"🏰 Setting: {story['setting']}")
            print(f"📝 Content: {story['content']}")
            print(f"📊 Word count: {story['word_count']}")
        print()
        
        # Demo 3: Create a sci-fi story
        print("🚀 Demo 3: Creating a Sci-Fi Story")
        print("-" * 30)
        scifi_result = root_agent.tools[0](
            title="Beyond the Stars",
            genre="sci-fi",
            main_character="space explorer",
            setting="distant galaxy",
            plot_points=2
        )
        if scifi_result["status"] == "success":
            scifi_story = scifi_result["story"]
            print(f"🚀 Story created: {scifi_story['title']}")
            print(f"🔬 Genre: {scifi_story['genre']}")
            print(f"👨‍🚀 Character: {scifi_story['main_character']}")
            print(f"🌌 Setting: {scifi_story['setting']}")
            print(f"📝 Content: {scifi_story['content']}")
        print()
        
        # Demo 4: List all stories
        print("📋 Demo 4: Listing All Stories")
        print("-" * 30)
        list_result = root_agent.tools[1]()
        if list_result["status"] == "success":
            print(f"📚 Total stories: {list_result['count']}")
            for story in list_result["stories"]:
                print(f"  • {story['id']}: {story['title']} ({story['genre']})")
        print()
        
        # Demo 5: Analyze the first story
        print("🔍 Demo 5: Analyzing Story Structure")
        print("-" * 30)
        if list_result["status"] == "success" and list_result["stories"]:
            first_story_id = list_result["stories"][0]["id"]
            analysis_result = root_agent.tools[6](story_id=first_story_id)
            if analysis_result["status"] == "success":
                analysis = analysis_result["analysis"]
                print(f"📊 Analysis for: {analysis['title']}")
                print(f"📝 Word count: {analysis['basic_stats']['word_count']}")
                print(f"🔤 Sentences: {analysis['basic_stats']['sentence_count']}")
                print(f"📏 Avg sentence length: {analysis['basic_stats']['average_sentence_length']}")
                print(f"🎭 Genre alignment: {analysis['genre_analysis']['genre_alignment_score']:.1f}%")
                if analysis["recommendations"]:
                    print("💡 Recommendations:")
                    for rec in analysis["recommendations"]:
                        print(f"  • {rec}")
        print()
        
        # Demo 6: Export story in different formats
        print("📤 Demo 6: Exporting Stories")
        print("-" * 30)
        if list_result["status"] == "success" and list_result["stories"]:
            first_story_id = list_result["stories"][0]["id"]
            
            # Export as text
            text_export = root_agent.tools[7](story_id=first_story_id, format="text")
            if text_export["status"] == "success":
                print(f"📄 Text export: {text_export['filename']}")
                print("Content preview:")
                print(text_export["content"][:100] + "..." if len(text_export["content"]) > 100 else text_export["content"])
                print()
            
            # Export as markdown
            md_export = root_agent.tools[7](story_id=first_story_id, format="markdown")
            if md_export["status"] == "success":
                print(f"📝 Markdown export: {md_export['filename']}")
                print("Content preview:")
                print(md_export["content"][:100] + "..." if len(md_export["content"]) > 100 else md_export["content"])
        print()
        
        # Demo 7: Edit a story
        print("✏️ Demo 7: Editing a Story")
        print("-" * 30)
        if list_result["status"] == "success" and list_result["stories"]:
            first_story_id = list_result["stories"][0]["id"]
            edit_result = root_agent.tools[3](
                story_id=first_story_id,
                title="The Dragon's Heart - Enhanced Edition",
                status="published"
            )
            if edit_result["status"] == "success":
                print(f"✅ Story updated: {edit_result['message']}")
                print(f"📝 New title: {edit_result['story']['title']}")
                print(f"📊 Status: {edit_result['story']['status']}")
        print()
        
        print("🎉 Demo completed successfully!")
        print("\n💡 You can now interact with the storybook agent using the ADK!")
        print("   Try asking it to create different types of stories or help with your writing.")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    main()
