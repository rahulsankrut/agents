import os
import json
import random
import datetime
from typing import Dict, List, Optional, Any
from google.adk.agents import Agent
from google.generativeai import GenerativeModel
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_model = GenerativeModel("gemini-2.5-pro")

# In-memory storage for stories (in production, you'd use a database)
STORIES_DB = {}
STORY_COUNTER = 1

def create_story_with_ai(
    title: str,
    genre: str = "fantasy",
    main_character: str = "hero",
    setting: str = "magical forest",
    plot_points: int = 3,
    tone: str = "adventurous",
    target_length: str = "medium"
) -> Dict[str, Any]:
    """Creates a new story using Gemini AI for creative generation.
    
    Args:
        title (str): The title of the story
        genre (str): The genre of the story (fantasy, sci-fi, mystery, romance, adventure)
        main_character (str): Description of the main character
        setting (str): The setting where the story takes place
        plot_points (int): Number of major plot points to include
        tone (str): The tone of the story (adventurous, dark, humorous, romantic, etc.)
        target_length (str): Target length (short, medium, long)
        
    Returns:
        dict: Story object with status and AI-generated story details
    """
    global STORY_COUNTER
    
    try:
        # Create a detailed prompt for Gemini
        prompt = f"""
        Create a creative and engaging {genre} story with the following specifications:
        
        Title: {title}
        Genre: {genre}
        Main Character: {main_character}
        Setting: {setting}
        Plot Points: {plot_points} major plot points
        Tone: {tone}
        Target Length: {target_length}
        
        Requirements:
        - Write a complete, engaging story that fits the specified genre
        - Include vivid descriptions and engaging dialogue
        - Ensure the story has a clear beginning, middle, and end
        - Make the main character compelling and relatable
        - Use the setting effectively to enhance the story
        - Maintain consistent tone throughout
        - Include {plot_points} distinct plot points that drive the narrative forward
        
        Please write the story in a natural, flowing narrative style. Make it creative and original, not a generic template.
        """
        
        # Generate story using Gemini
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            story_content = response.text.strip()
            
            # Create story object
            story = {
                "id": STORY_COUNTER,
                "title": title,
                "genre": genre,
                "main_character": main_character,
                "setting": setting,
                "plot_points": plot_points,
                "tone": tone,
                "target_length": target_length,
                "content": story_content,
                "created_at": datetime.datetime.now().isoformat(),
                "word_count": len(story_content.split()),
                "status": "draft",
                "ai_generated": True,
                "generation_prompt": prompt
            }
            
            STORIES_DB[STORY_COUNTER] = story
            STORY_COUNTER += 1
            
            return {
                "status": "success",
                "message": f"AI-generated story '{title}' created successfully!",
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
            "error_message": f"Error generating story with AI: {str(e)}"
        }

def create_story(
    title: str,
    genre: str = "fantasy",
    main_character: str = "hero",
    setting: str = "magical forest",
    plot_points: int = 3,
    tone: str = "adventurous",
    target_length: str = "medium"
) -> Dict[str, Any]:
    """Creates a new story with the specified parameters.
    
    This function now uses Gemini AI for creative story generation.
    
    Args:
        title (str): The title of the story
        genre (str): The genre of the story (fantasy, sci-fi, mystery, romance, adventure)
        main_character (str): Description of the main character
        setting (str): The setting where the story takes place
        plot_points (int): Number of major plot points to include
        tone (str): The tone of the story (adventurous, dark, humorous, romantic, etc.)
        target_length (str): Target length (short, medium, long)
        
    Returns:
        dict: Story object with status and story details
    """
    return create_story_with_ai(
        title=title,
        genre=genre,
        main_character=main_character,
        setting=setting,
        plot_points=plot_points,
        tone=tone,
        target_length=target_length
    )

def enhance_story_with_ai(story_id: int, enhancement_type: str = "general") -> Dict[str, Any]:
    """Enhances an existing story using Gemini AI.
    
    Args:
        story_id (int): The ID of the story to enhance
        enhancement_type (str): Type of enhancement (general, dialogue, description, ending, etc.)
        
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
            "general": f"Enhance this {story['genre']} story to make it more engaging and creative. Improve the writing style, add more vivid descriptions, and make the plot more compelling:\n\n{story['content']}",
            "dialogue": f"Enhance the dialogue in this story to make it more natural, engaging, and character-specific:\n\n{story['content']}",
            "description": f"Enhance the descriptions in this story to make them more vivid, sensory, and immersive:\n\n{story['content']}",
            "ending": f"Rewrite the ending of this story to make it more satisfying and impactful:\n\n{story['content']}",
            "character": f"Enhance the character development in this story, making the main character more compelling and well-rounded:\n\n{story['content']}"
        }
        
        prompt = enhancement_prompts.get(enhancement_type, enhancement_prompts["general"])
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            enhanced_content = response.text.strip()
            
            # Update the story with enhanced content
            story["content"] = enhanced_content
            story["word_count"] = len(enhanced_content.split())
            story["updated_at"] = datetime.datetime.now().isoformat()
            story["enhancement_type"] = enhancement_type
            
            return {
                "status": "success",
                "message": f"Story enhanced successfully with {enhancement_type} improvements!",
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
            "error_message": f"Error enhancing story with AI: {str(e)}"
        }

def generate_story_ideas_with_ai(genre: str = "any", theme: str = "adventure", mood: str = "inspiring") -> Dict[str, Any]:
    """Generates creative story ideas using Gemini AI.
    
    Args:
        genre (str): Preferred genre for the story ideas
        theme (str): Central theme for the story ideas
        mood (str): The mood or feeling for the story ideas
        
    Returns:
        dict: List of creative story ideas generated by AI
    """
    try:
        prompt = f"""
        Generate 5 unique and creative story ideas for a {genre} story with the theme of {theme} and a {mood} mood.
        
        For each idea, provide:
        1. A compelling title
        2. A brief 2-3 sentence description
        3. The main conflict or challenge
        4. A unique twist or element
        
        Make each idea distinct and creative. Avoid generic or clichéd concepts.
        """
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            ideas_content = response.text.strip()
            
            # Parse the ideas (simple parsing - could be enhanced)
            ideas = [idea.strip() for idea in ideas_content.split('\n') if idea.strip()]
            
            return {
                "status": "success",
                "genre": genre,
                "theme": theme,
                "mood": mood,
                "ideas": ideas,
                "raw_ai_response": ideas_content
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to generate story ideas with Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error generating story ideas with AI: {str(e)}"
        }

def generate_story_ideas(genre: str = "any", theme: str = "adventure") -> Dict[str, Any]:
    """Generates creative story ideas based on genre and theme.
    
    This function now uses Gemini AI for creative idea generation.
    
    Args:
        genre (str): Preferred genre for the story ideas
        theme (str): Central theme for the story ideas
        
    Returns:
        dict: List of creative story ideas
    """
    return generate_story_ideas_with_ai(genre=genre, theme=theme, mood="inspiring")

def analyze_story_with_ai(story_id: int) -> Dict[str, Any]:
    """Analyzes a story using Gemini AI for deeper insights.
    
    Args:
        story_id (int): The ID of the story to analyze
        
    Returns:
        dict: AI-powered analysis results or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story = STORIES_DB[story_id]
    
    try:
        prompt = f"""
        Analyze this {story['genre']} story titled "{story['title']}" and provide a comprehensive analysis:
        
        Story Content:
        {story['content']}
        
        Please analyze:
        1. **Plot Structure**: Evaluate the story's plot development, pacing, and structure
        2. **Character Development**: Assess the main character's growth and relatability
        3. **Genre Alignment**: How well does this story fit its intended genre?
        4. **Writing Quality**: Evaluate the prose, dialogue, and descriptions
        5. **Engagement Factor**: How compelling and engaging is the narrative?
        6. **Areas for Improvement**: Specific suggestions to enhance the story
        7. **Strengths**: What works well in this story?
        
        Provide detailed, constructive feedback with specific examples from the text.
        """
        
        response = gemini_model.generate_content(prompt)
        
        if response and response.text:
            ai_analysis = response.text.strip()
            
            # Basic stats
            word_count = len(story["content"].split())
            sentence_count = len([s for s in story["content"].split('.') if s.strip()])
            avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
            
            analysis = {
                "story_id": story_id,
                "title": story["title"],
                "ai_analysis": ai_analysis,
                "basic_stats": {
                    "word_count": word_count,
                    "sentence_count": sentence_count,
                    "average_sentence_length": round(avg_sentence_length, 2)
                },
                "analysis_type": "ai_enhanced"
            }
            
            return {
                "status": "success",
                "analysis": analysis
            }
        else:
            return {
                "status": "error",
                "error_message": "Failed to analyze story with Gemini AI."
            }
            
    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error analyzing story with AI: {str(e)}"
        }

def analyze_story(story_id: int) -> Dict[str, Any]:
    """Analyzes a story and provides insights about its structure and content.
    
    This function now uses Gemini AI for enhanced analysis.
    
    Args:
        story_id (int): The ID of the story to analyze
        
    Returns:
        dict: Analysis results or error message
    """
    return analyze_story_with_ai(story_id)

def export_story(story_id: int, format: str = "json") -> Dict[str, Any]:
    """Exports a story in the specified format.
    
    Args:
        story_id (int): The ID of the story to export
        format (str): Export format (json, text, markdown)
        
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
        export_content = f"{story['title']}\n\n{story['content']}"
    elif format.lower() == "markdown":
        export_content = f"# {story['title']}\n\n**Genre:** {story['genre']}\n**Setting:** {story['setting']}\n\n{story['content']}"
    else:
        return {
            "status": "error",
            "error_message": f"Unsupported format: {format}. Supported formats: json, text, markdown"
        }
    
    return {
        "status": "success",
        "format": format,
        "content": export_content,
        "filename": f"{story['title'].replace(' ', '_')}_{story_id}.{format}"
    }

def list_stories(genre: Optional[str] = None, status: Optional[str] = None) -> Dict[str, Any]:
    """Lists all stories with optional filtering by genre or status.
    
    Args:
        genre (str, optional): Filter stories by genre
        status (str, optional): Filter stories by status (draft, published, archived)
        
    Returns:
        dict: List of stories matching the criteria
    """
    stories = list(STORIES_DB.values())
    
    if genre:
        stories = [s for s in stories if s["genre"].lower() == genre.lower()]
    
    if status:
        stories = [s for s in stories if s["status"].lower() == status.lower()]
    
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

def edit_story(
    story_id: int,
    title: Optional[str] = None,
    content: Optional[str] = None,
    genre: Optional[str] = None,
    status: Optional[str] = None
) -> Dict[str, Any]:
    """Edits an existing story with new information.
    
    Args:
        story_id (int): The ID of the story to edit
        title (str, optional): New title for the story
        content (str, optional): New content for the story
        genre (str, optional): New genre for the story
        status (str, optional): New status for the story
        
    Returns:
        dict: Updated story object or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story = STORIES_DB[story_id]
    
    if title:
        story["title"] = title
    if content:
        story["content"] = content
        story["word_count"] = len(content.split())
    if genre:
        story["genre"] = genre
    if status:
        story["status"] = status
    
    story["updated_at"] = datetime.datetime.now().isoformat()
    
    return {
        "status": "success",
        "message": f"Story '{story['title']}' updated successfully!",
        "story": story
    }

def delete_story(story_id: int) -> Dict[str, Any]:
    """Deletes a story from the database.
    
    Args:
        story_id (int): The ID of the story to delete
        
    Returns:
        dict: Success or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story_title = STORIES_DB[story_id]["title"]
    del STORIES_DB[story_id]
    
    return {
        "status": "success",
        "message": f"Story '{story_title}' deleted successfully!"
    }

# Create the main storybook agent
root_agent = Agent(
    name="storybook_agent",
    model="gemini-2.5-pro",
    description=(
        "A creative AI agent that helps users create, edit, manage, and analyze stories. "
        "I can generate story ideas, create complete stories, edit existing ones, "
        "provide analysis, and export stories in various formats."
    ),
    instruction=(
        "I am a creative storybook agent that helps users with all aspects of story creation and management. "
        "I can create new stories based on user preferences, edit existing stories, generate creative ideas, "
        "analyze story structure and content, and export stories in different formats. "
        "I'm here to inspire creativity and help bring stories to life!"
    ),
    tools=[
        create_story,
        list_stories,
        get_story,
        edit_story,
        delete_story,
        generate_story_ideas,
        analyze_story,
        export_story
    ]
)
