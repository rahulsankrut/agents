#!/usr/bin/env python3
"""
Demo script for the Inspirational Stories Agent
This script demonstrates how the agent researches famous personalities and creates inspirational children's stories.
"""

import os
from dotenv import load_dotenv
from agent import root_agent

def main():
    """Main demo function showcasing the inspirational stories agent capabilities."""
    
    # Load environment variables
    load_dotenv()
    
    print("🌟 Welcome to the Inspirational Stories Agent Demo! 🌟")
    print("=" * 60)
    
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable not set!")
        print("Please set your Google API key and try again.")
        return
    
    print("✅ API key loaded successfully!")
    print("\n📚 Let's create inspirational stories for children! 🧒✨\n")
    
    try:
        # Demo 1: Suggest inspirational people
        print("🎯 Demo 1: Discovering Inspirational People")
        print("-" * 40)
        suggestions_result = root_agent.tools[2](
            category="scientists",
            age_group="children",
            interests=["curiosity", "perseverance", "discovery"]
        )
        if suggestions_result["status"] == "success":
            print("✨ Suggested inspirational scientists for children:")
            for i, suggestion in enumerate(suggestions_result["suggestions"][:5], 1):  # Show first 5
                print(f"  {i}. {suggestion}")
        print()
        
        # Demo 2: Research a famous person
        print("🔍 Demo 2: Researching a Famous Personality")
        print("-" * 40)
        research_result = root_agent.tools[0](
            person_name="Marie Curie",
            research_depth="comprehensive",
            focus_areas=["early life", "achievements", "challenges overcome", "legacy"]
        )
        if research_result["status"] == "success":
            research = research_result["research"]
            print(f"📖 Research completed for: {research['person_name']}")
            print(f"📊 Research depth: {research['research_depth']}")
            print(f"📝 Word count: {research['word_count']}")
            print(f"📋 Focus areas: {', '.join(research['focus_areas'])}")
            print(f"📄 Content preview: {research['content'][:200]}...")
        print()
        
        # Demo 3: Create an inspirational story
        print("📚 Demo 3: Creating an Inspirational Children's Story")
        print("-" * 40)
        story_result = root_agent.tools[1](
            person_name="Marie Curie",
            story_theme="overcoming challenges",
            target_age="8-12",
            story_length="medium",
            include_lessons=True
        )
        if story_result["status"] == "success":
            story = story_result["story"]
            print(f"📖 Story created: {story['person_name']} - {story['story_theme']}")
            print(f"🎯 Target age: {story['target_age']}")
            print(f"📏 Length: {story['story_length']}")
            print(f"💡 Life lessons: {'Yes' if story['include_lessons'] else 'No'}")
            print(f"📝 Content preview: {story['content'][:300]}...")
        print()
        
        # Demo 4: Create another story with different theme
        print("🚀 Demo 4: Creating Another Story with Different Theme")
        print("-" * 40)
        story2_result = root_agent.tools[1](
            person_name="Albert Einstein",
            story_theme="achieving dreams",
            target_age="10-14",
            story_length="long",
            include_lessons=True
        )
        if story2_result["status"] == "success":
            story2 = story2_result["story"]
            print(f"📖 Story created: {story2['person_name']} - {story2['story_theme']}")
            print(f"🎯 Target age: {story2['target_age']}")
            print(f"📏 Length: {story2['story_length']}")
            print(f"📝 Content preview: {story2['content'][:300]}...")
        print()
        
        # Demo 5: List all stories
        print("📋 Demo 5: Listing All Created Stories")
        print("-" * 40)
        list_result = root_agent.tools[4]()
        if list_result["status"] == "success":
            print(f"📚 Total stories: {list_result['count']}")
            for story in list_result["stories"]:
                print(f"  • {story['id']}: {story['person_name']} - {story['story_theme']} ({story['target_age']})")
        print()
        
        # Demo 6: Enhance a story for younger children
        print("👶 Demo 6: Enhancing Story for Younger Children")
        print("-" * 40)
        if list_result["status"] == "success" and list_result["stories"]:
            first_story_id = list_result["stories"][0]["id"]
            enhance_result = root_agent.tools[3](
                story_id=first_story_id,
                enhancement_type="age_appropriate",
                target_age="5-8"
            )
            if enhance_result["status"] == "success":
                print(f"✅ Story enhanced successfully!")
                print(f"🎯 New target age: {enhance_result['story']['target_age']}")
                print(f"🔧 Enhancement type: {enhance_result['story']['enhancement_type']}")
                print(f"📝 Enhanced content preview: {enhance_result['enhanced_content'][:300]}...")
        print()
        
        # Demo 7: List research conducted
        print("🔬 Demo 7: Listing Research Conducted")
        print("-" * 40)
        research_list_result = root_agent.tools[6]()
        if research_list_result["status"] == "success":
            print(f"🔍 Total research projects: {research_list_result['count']}")
            for research in research_list_result["research"]:
                print(f"  • {research['id']}: {research['person_name']} ({research['research_depth']})")
        print()
        
        # Demo 8: Export story in different formats
        print("📤 Demo 8: Exporting Stories")
        print("-" * 40)
        if list_result["status"] == "success" and list_result["stories"]:
            first_story_id = list_result["stories"][0]["id"]
            
            # Export as markdown
            export_result = root_agent.tools[7](story_id=first_story_id, format="markdown")
            if export_result["status"] == "success":
                print(f"📝 Markdown export: {export_result['filename']}")
                print("Content preview:")
                print(export_result["content"][:200] + "..." if len(export_result["content"]) > 200 else export_result["content"])
        print()
        
        print("🎉 Demo completed successfully!")
        print("\n💡 You can now use the inspirational stories agent to:")
        print("   • Research any famous personality")
        print("   • Create engaging stories for children of different ages")
        print("   • Discover inspirational people in various fields")
        print("   • Enhance stories to be more age-appropriate")
        print("   • Export stories in different formats")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    main()
