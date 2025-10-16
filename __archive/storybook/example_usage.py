#!/usr/bin/env python3
"""
Example usage of the Storybook Agent
This script demonstrates how to use the storybook agent programmatically.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def example_basic_usage():
    """Example of basic storybook agent usage."""
    print("📚 Example: Basic Storybook Agent Usage")
    print("=" * 50)
    
    try:
        # Import the agent (this will work if you have the Google API key set)
        from agent import root_agent
        
        print("✅ Agent loaded successfully!")
        print(f"🤖 Agent name: {root_agent.name}")
        print(f"📝 Description: {root_agent.description}")
        print(f"🛠️ Available tools: {len(root_agent.tools)}")
        
        # List available tools
        for i, tool in enumerate(root_agent.tools):
            print(f"  {i+1}. {tool.__name__}: {tool.__doc__.split('.')[0] if tool.__doc__ else 'No description'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Could not load agent: {e}")
        print("💡 Make sure you have:")
        print("   • Set GOOGLE_API_KEY environment variable")
        print("   • Installed google-adk package")
        print("   • Valid Google API credentials")
        return False

def example_direct_tool_usage():
    """Example of using the agent's tools directly."""
    print("\n🔧 Example: Direct Tool Usage")
    print("=" * 50)
    
    try:
        # Import individual tools
        from agent import (
            create_story, 
            list_stories, 
            generate_story_ideas,
            analyze_story,
            export_story
        )
        
        print("✅ Tools imported successfully!")
        
        # Generate some story ideas
        print("\n💡 Generating story ideas...")
        ideas = generate_story_ideas(genre="fantasy", theme="adventure")
        if ideas["status"] == "success":
            print("✨ Generated ideas:")
            for i, idea in enumerate(ideas["ideas"], 1):
                print(f"  {i}. {idea}")
        
        # Create a story
        print("\n📖 Creating a story...")
        story = create_story(
            title="The Lost Crystal",
            genre="fantasy",
            main_character="young wizard",
            setting="crystal caves",
            plot_points=3
        )
        
        if story["status"] == "success":
            print(f"✅ Story created: {story['story']['title']}")
            print(f"📝 Content: {story['story']['content'][:100]}...")
            
            # Analyze the story
            print("\n🔍 Analyzing the story...")
            analysis = analyze_story(story["story"]["id"])
            if analysis["status"] == "success":
                stats = analysis["analysis"]["basic_stats"]
                print(f"📊 Analysis results:")
                print(f"   • Word count: {stats['word_count']}")
                print(f"   • Sentences: {stats['sentence_count']}")
                print(f"   • Avg sentence length: {stats['average_sentence_length']}")
            
            # Export the story
            print("\n📤 Exporting story...")
            export = export_story(story["story"]["id"], "markdown")
            if export["status"] == "success":
                print(f"✅ Exported as: {export['filename']}")
                print("📄 Content preview:")
                print(export["content"][:200] + "..." if len(export["content"]) > 200 else export["content"])
        
        return True
        
    except Exception as e:
        print(f"❌ Tool usage failed: {e}")
        return False

def example_story_management():
    """Example of story management operations."""
    print("\n📚 Example: Story Management")
    print("=" * 50)
    
    try:
        from agent import (
            create_story, 
            list_stories, 
            edit_story, 
            delete_story
        )
        
        # Create multiple stories
        print("📝 Creating multiple stories...")
        stories = [
            {
                "title": "Space Pirates",
                "genre": "sci-fi",
                "main_character": "space captain",
                "setting": "distant star system",
                "plot_points": 2
            },
            {
                "title": "Mystery Manor",
                "genre": "mystery",
                "main_character": "detective",
                "setting": "old mansion",
                "plot_points": 3
            }
        ]
        
        created_stories = []
        for story_data in stories:
            result = create_story(**story_data)
            if result["status"] == "success":
                created_stories.append(result["story"])
                print(f"✅ Created: {result['story']['title']}")
        
        # List all stories
        print(f"\n📋 Listing all stories...")
        all_stories = list_stories()
        if all_stories["status"] == "success":
            print(f"📚 Total stories: {all_stories['count']}")
            for story in all_stories["stories"]:
                print(f"  • {story['id']}: {story['title']} ({story['genre']}) - {story['status']}")
        
        # Edit a story
        if created_stories:
            print(f"\n✏️ Editing story: {created_stories[0]['title']}")
            edit_result = edit_story(
                story_id=created_stories[0]["id"],
                title="Space Pirates - Extended Edition",
                status="published"
            )
            if edit_result["status"] == "success":
                print(f"✅ Updated: {edit_result['message']}")
        
        # Filter stories by genre
        print(f"\n🔍 Filtering stories by genre...")
        fantasy_stories = list_stories(genre="fantasy")
        if fantasy_stories["status"] == "success":
            print(f"🎭 Fantasy stories: {fantasy_stories['count']}")
        
        sci_fi_stories = list_stories(genre="sci-fi")
        if sci_fi_stories["status"] == "success":
            print(f"🚀 Sci-fi stories: {sci_fi_stories['count']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Story management failed: {e}")
        return False

def main():
    """Run all examples."""
    print("🌟 Storybook Agent Examples")
    print("=" * 60)
    
    examples = [
        ("Basic Usage", example_basic_usage),
        ("Direct Tool Usage", example_direct_tool_usage),
        ("Story Management", example_story_management)
    ]
    
    for example_name, example_func in examples:
        print(f"\n🎯 Running {example_name} example...")
        success = example_func()
        if success:
            print(f"✅ {example_name} completed successfully!")
        else:
            print(f"❌ {example_name} failed!")
        print()
    
    print("=" * 60)
    print("🎉 Examples completed!")
    print("\n💡 Next steps:")
    print("   • Set your GOOGLE_API_KEY environment variable")
    print("   • Run the full demo: python demo.py")
    print("   • Test the agent: python test_agent.py")
    print("   • Explore the agent's capabilities with your own stories!")

if __name__ == "__main__":
    main()
