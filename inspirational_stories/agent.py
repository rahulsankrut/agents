import os
import json
import datetime
from typing import Dict, List, Optional, Any
from google.adk.agents import Agent
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = GenerativeModel("gemini-2.5-pro")

# In-memory storage for stories and research (in production, you'd use a database)
STORIES_DB = {}
RESEARCH_DB = {}
STORY_COUNTER = 1
RESEARCH_COUNTER = 1

def research_famous_person(
    person_name: str,
    research_depth: str = "comprehensive",
    focus_areas: List[str] = None
) -> Dict[str, Any]:
    """Researches a famous personality using Gemini AI to gather information.
    
    Args:
        person_name (str): Name of the famous person to research
        research_depth (str): Level of research detail (basic, comprehensive, detailed)
        focus_areas (List[str]): Specific areas to focus on (e.g., ["early life", "achievements", "challenges"])
        
    Returns:
        dict: Research results with comprehensive information about the person
    """
    global RESEARCH_COUNTER
    
    try:
        # Set default focus areas if none provided
        if not focus_areas:
            focus_areas = ["early life", "major achievements", "challenges overcome", "personal qualities", "legacy"]
        
        # Create a comprehensive research prompt
        prompt = f"""
        Conduct a {research_depth} research on {person_name}, a famous personality. 
        Focus on the following areas and provide detailed, accurate information:
        
        Focus Areas:
        {', '.join(focus_areas)}
        
        Please provide:
        1. **Basic Information**: Full name, birth/death dates, nationality, profession
        2. **Early Life**: Childhood, family background, early influences
        3. **Major Achievements**: Key accomplishments, discoveries, contributions
        4. **Challenges Overcome**: Obstacles faced and how they were overcome
        5. **Personal Qualities**: Character traits, values, personality
        6. **Legacy**: Impact on society, lasting influence, lessons for future generations
        7. **Interesting Facts**: Lesser-known details, anecdotes, unique aspects
        8. **Inspirational Elements**: What makes this person inspiring, especially for children
        
        Make the information engaging and suitable for creating an inspirational children's story.
        Focus on positive aspects, resilience, determination, and values that children can learn from.
        """
        
        # Generate research using Gemini
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            research_content = response.text.strip()
            
            # Create research object
            research = {
                "id": RESEARCH_COUNTER,
                "person_name": person_name,
                "research_depth": research_depth,
                "focus_areas": focus_areas,
                "content": research_content,
                "created_at": datetime.datetime.now().isoformat(),
                "word_count": len(research_content.split()),
                "status": "completed"
            }
            
            RESEARCH_DB[RESEARCH_COUNTER] = research
            RESEARCH_COUNTER += 1
            
            return {
                "status": "success",
                "message": f"Research completed for {person_name}!",
                "research": research
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to generate research content from Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error conducting research: {str(e)}"
        }

def create_inspirational_story(
    person_name: str,
    story_theme: str = "overcoming challenges",
    target_age: str = "8-12",
    story_length: str = "medium",
    include_lessons: bool = True,
    research_id: Optional[int] = None
) -> Dict[str, Any]:
    """Creates an inspirational children's story about a famous personality using Gemini AI.
    
    Args:
        person_name (str): Name of the famous person
        story_theme (str): Central theme of the story (overcoming challenges, achieving dreams, helping others, etc.)
        target_age (str): Target age group for the story
        story_length (str): Desired story length (short, medium, long)
        include_lessons: bool: Whether to include life lessons and morals
        research_id (int, optional): ID of existing research to use
        
    Returns:
        dict: Story object with AI-generated inspirational content
    """
    global STORY_COUNTER
    
    try:
        # Get research data (either existing or conduct new research)
        research_data = None
        if research_id and research_id in RESEARCH_DB:
            research_data = RESEARCH_DB[research_id]["content"]
        else:
            # Conduct basic research if none provided
            research_result = research_famous_person(person_name, "basic")
            if research_result["status"] == "success":
                research_data = research_result["research"]["content"]
            else:
                return {
                    "status": "error",
                    "error_message": f"Could not research {person_name}: {research_result['error_message']}"
                }
        
        # Create a detailed story generation prompt
        prompt = f"""
        Create an inspirational children's story about {person_name} based on the following research:
        
        Research Information:
        {research_data}
        
        Story Requirements:
        - Theme: {story_theme}
        - Target Age: {target_age} years old
        - Length: {story_length}
        - Include Life Lessons: {include_lessons}
        
        Story Guidelines:
        1. **Make it engaging for children**: Use simple language, vivid descriptions, and relatable scenarios
        2. **Focus on inspiration**: Highlight determination, courage, kindness, and positive values
        3. **Include challenges**: Show how obstacles were overcome with resilience and creativity
        4. **Add dialogue**: Include conversations that bring the story to life
        5. **Create emotional connection**: Help children relate to the person's journey
        6. **Include lessons**: {f"Embed {story_theme} lessons naturally in the story" if include_lessons else "Focus on the narrative without explicit lessons"}
        7. **Make it memorable**: Use imagery, metaphors, and storytelling techniques suitable for children
        
        Write a complete, engaging story that will inspire children to dream big and persevere.
        The story should be educational, entertaining, and motivational.
        """
        
        # Generate story using Gemini
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            story_content = response.text.strip()
            
            # Create story object
            story = {
                "id": STORY_COUNTER,
                "person_name": person_name,
                "story_theme": story_theme,
                "target_age": target_age,
                "story_length": story_length,
                "include_lessons": include_lessons,
                "research_id": research_id,
                "content": story_content,
                "created_at": datetime.datetime.now().isoformat(),
                "word_count": len(story_content.split()),
                "status": "draft",
                "ai_generated": True,
                "story_type": "inspirational_biography"
            }
            
            STORIES_DB[STORY_COUNTER] = story
            STORY_COUNTER += 1
            
            return {
                "status": "success",
                "message": f"Inspirational story about {person_name} created successfully!",
                "story": story
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to generate story content from Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error creating inspirational story: {str(e)}"
        }

def suggest_inspirational_people(
    category: str = "general",
    age_group: str = "children",
    interests: List[str] = None
) -> Dict[str, Any]:
    """Suggests inspirational people for children's stories using Gemini AI.
    
    Args:
        category (str): Category of people (scientists, artists, leaders, athletes, etc.)
        age_group (str): Target age group (toddlers, children, teens)
        interests (List[str]): Specific interests or themes
        
    Returns:
        dict: List of suggested inspirational people with brief descriptions
    """
    try:
        if not interests:
            interests = ["courage", "creativity", "perseverance", "kindness"]
        
        prompt = f"""
        Suggest 10 inspirational people who would be great subjects for {age_group} stories in the {category} category.
        
        Focus on people who demonstrate these values: {', '.join(interests)}
        
        For each person, provide:
        1. **Name**: Full name
        2. **Profession/Field**: What they're known for
        3. **Key Achievement**: Their most inspiring accomplishment
        4. **Why They're Inspiring**: What makes them a good role model for children
        5. **Age-Appropriate**: Why this person is suitable for {age_group}
        
        Include a mix of:
        - Historical figures and contemporary people
        - Different backgrounds and cultures
        - Various fields (science, arts, sports, leadership, etc.)
        - Both well-known and lesser-known inspirational figures
        
        Make sure all suggestions are appropriate for children and have positive, educational value.
        """
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            suggestions_content = response.text.strip()
            
            # Parse the suggestions (simple parsing - could be enhanced)
            suggestions = [suggestion.strip() for suggestion in suggestions_content.split('\n') if suggestion.strip()]
            
            return {
                "status": "success",
                "category": category,
                "age_group": age_group,
                "interests": interests,
                "suggestions": suggestions,
                "raw_ai_response": suggestions_content
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to generate suggestions with Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating suggestions: {str(e)}"
        }

def enhance_story_for_children(
    story_id: int,
    enhancement_type: str = "age_appropriate",
    target_age: str = "8-12"
) -> Dict[str, Any]:
    """Enhances a story to make it more suitable for children using Gemini AI.
    
    Args:
        story_id (int): The ID of the story to enhance
        enhancement_type (str): Type of enhancement (age_appropriate, more_engaging, educational, etc.)
        target_age (str): Target age group for the enhancement
        
    Returns:
        dict: Enhanced story content or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story = STORIES_DB[story_id]
    
    try:
        enhancement_prompts = {
            "age_appropriate": f"Rewrite this story to make it more suitable for {target_age} year old children. Adjust language complexity, add more engaging elements, and ensure it's age-appropriate:\n\n{story['content']}",
            "more_engaging": f"Make this children's story more engaging by adding vivid descriptions, dialogue, and interactive elements that will capture a {target_age} year old's attention:\n\n{story['content']}",
            "educational": f"Enhance this story to include more educational elements, facts, and learning opportunities while maintaining the engaging narrative for {target_age} year olds:\n\n{story['content']}",
            "emotional_connection": f"Strengthen the emotional connection in this story to help {target_age} year old children relate to the character's journey and feelings:\n\n{story['content']}"
        }
        
        prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["age_appropriate"])
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            enhanced_content = response.text.strip()
            
            # Update the story with enhanced content
            story["content"] = enhanced_content
            story["word_count"] = len(enhanced_content.split())
            story["updated_at"] = datetime.datetime.now().isoformat()
            story["enhancement_type"] = enhancement_type
            story["target_age"] = target_age
            
            return {
                "status": "success",
                "message": f"Story enhanced successfully for {target_age} year olds!",
                "enhanced_content": enhanced_content,
                "story": story
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to enhance story with Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error enhancing story: {str(e)}"
        }

def list_stories(person_name: Optional[str] = None, theme: Optional[str] = None) -> Dict[str, Any]:
    """Lists all inspirational stories with optional filtering.
    
    Args:
        person_name (str, optional): Filter stories by famous person
        theme (str, optional): Filter stories by theme
        
    Returns:
        dict: List of stories matching the criteria
    """
    stories = list(STORIES_DB.values())
    
    if person_name:
        stories = [s for s in stories if s["person_name"].lower() == person_name.lower()]
    
    if theme:
        stories = [s for s in stories if s["story_theme"].lower() == theme.lower()]
    
    return {
        "status": "success",
        "count": len(stories),
        "stories": stories
    }

def get_story(story_id: int) -> Dict[str, Any]:
    """Retrieves a specific story by ID.
    
    Args:
        story_id (int): The ID of the story to retrieve
        
    Returns:
        dict: Story object or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    return {
        "status": "success",
        "story": STORIES_DB[story_id]
    }

def list_research(person_name: Optional[str] = None) -> Dict[str, Any]:
    """Lists all research conducted with optional filtering.
    
    Args:
        person_name (str, optional): Filter research by famous person
        
    Returns:
        dict: List of research matching the criteria
    """
    research_list = list(RESEARCH_DB.values())
    
    if person_name:
        research_list = [r for r in research_list if r["person_name"].lower() == person_name.lower()]
    
    return {
        "status": "success",
        "count": len(research_list),
        "research": research_list
    }

def export_story(story_id: int, format: str = "text") -> Dict[str, Any]:
    """Exports a story in the specified format.
    
    Args:
        story_id (int): The ID of the story to export
        format (str): Export format (text, markdown, json)
        
    Returns:
        dict: Exported story content or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story = STORIES_DB[story_id]
    
    if format.lower() == "json":
        export_content = json.dumps(story, indent=2)
    elif format.lower() == "text":
        export_content = f"# {story['person_name']} - {story['story_theme']}\n\n{story['content']}"
    elif format.lower() == "markdown":
        export_content = f"# {story['person_name']} - {story['story_theme']}\n\n**Target Age:** {story['target_age']}\n**Theme:** {story['story_theme']}\n**Length:** {story['story_length']}\n\n{story['content']}"
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported format: {format}. Supported formats: json, text, markdown"
        }
    
    return {
        "status": "success",
        "format": format,
        "content": export_content,
        "filename": f"{story['person_name'].replace(' ', '_')}_{story['story_theme'].replace(' ', '_')}_{story_id}.{format}"
    }

# Create the main inspirational stories agent
root_agent = Agent(
    name="inspirational_stories_agent",
    model="gemini-2.5-pro",
    description=(
        "An AI agent that creates inspirational children's stories about famous personalities. "
        "I can research famous people, generate engaging stories for children, and enhance "
        "stories to be age-appropriate and educational."
    ),
    instruction=(
        "I am an inspirational stories agent that helps create engaging, educational stories "
        "for children about famous personalities. I can research people, generate creative "
        "stories, suggest inspirational figures, and enhance stories for different age groups. "
        "My goal is to inspire children through real-life stories of courage, determination, "
        "and achievement."
    ),
    tools=[
        research_famous_person,
        create_inspirational_story,
        suggest_inspirational_people,
        enhance_story_for_children,
        list_stories,
        get_story,
        list_research,
        export_story
    ]
)
