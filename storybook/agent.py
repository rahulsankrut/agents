import os
import json
import random
import datetime
from typing import Dict, List, Optional, Any
from google.adk.agents import Agent

# In-memory storage for stories (in production, you'd use a database)
STORIES_DB = {}
STORY_COUNTER = 1

def create_story(
    title: str,
    genre: str = "fantasy",
    main_character: str = "hero",
    setting: str = "magical forest",
    plot_points: int = 3
) -> Dict[str, Any]:
    """Creates a new story with the specified parameters.
    
    Args:
        title (str): The title of the story
        genre (str): The genre of the story (fantasy, sci-fi, mystery, romance, adventure)
        main_character (str): Description of the main character
        setting (str): The setting where the story takes place
        plot_points (int): Number of major plot points to include
        
    Returns:
        dict: Story object with status and story details
    """
    global STORY_COUNTER
    
    # Generate story content based on parameters
    story_content = generate_story_content(genre, main_character, setting, plot_points)
    
    story = {
        "id": STORY_COUNTER,
        "title": title,
        "genre": genre,
        "main_character": main_character,
        "setting": setting,
        "plot_points": plot_points,
        "content": story_content,
        "created_at": datetime.datetime.now().isoformat(),
        "word_count": len(story_content.split()),
        "status": "draft"
    }
    
    STORIES_DB[STORY_COUNTER] = story
    STORY_COUNTER += 1
    
    return {
        "status": "success",
        "message": f"Story '{title}' created successfully!",
        "story": story
    }

def generate_story_content(genre: str, character: str, setting: str, plot_points: int) -> str:
    """Generates story content based on the given parameters."""
    
    genre_templates = {
        "fantasy": {
            "opening": f"In the mystical realm of {setting}, where magic flows like rivers and ancient secrets whisper in the wind, there lived a {character} whose destiny was about to unfold.",
            "conflict": "A dark force threatened to consume the realm, and only the hero's unique abilities could save it.",
            "resolution": "Through courage and determination, the hero overcame the darkness and restored peace to the land."
        },
        "sci-fi": {
            "opening": f"On the distant planet of {setting}, in a future where technology had evolved beyond imagination, a {character} discovered something that would change everything.",
            "conflict": "An alien threat emerged, and the hero had to use advanced technology and wit to protect humanity.",
            "resolution": "The hero's ingenuity and bravery saved the day, forging a new alliance between species."
        },
        "mystery": {
            "opening": f"In the quiet town of {setting}, where everyone knew each other's names, a {character} stumbled upon a mystery that would shake the community to its core.",
            "conflict": "A series of strange events occurred, and the hero had to piece together clues to solve the puzzle.",
            "resolution": "The truth was revealed, bringing justice and closure to all involved."
        },
        "romance": {
            "opening": f"In the charming village of {setting}, where love stories were written in the stars, a {character} found themselves on a journey of the heart.",
            "conflict": "Misunderstandings and obstacles threatened to keep two souls apart, testing their love and commitment.",
            "resolution": "Love conquered all, and the couple found their happily ever after."
        },
        "adventure": {
            "opening": f"Beyond the known borders of {setting}, where danger lurked around every corner, a {character} embarked on an epic quest that would test their limits.",
            "conflict": "Treacherous terrain, fierce enemies, and impossible odds stood between the hero and their goal.",
            "resolution": "The hero's perseverance and skill led them to victory, achieving what seemed impossible."
        }
    }
    
    template = genre_templates.get(genre.lower(), genre_templates["fantasy"])
    
    # Build story with plot points
    story_parts = [template["opening"]]
    
    if plot_points >= 2:
        story_parts.append(template["conflict"])
    if plot_points >= 3:
        story_parts.append(template["resolution"])
    
    return " ".join(story_parts)

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

def generate_story_ideas(genre: str = "any", theme: str = "adventure") -> Dict[str, Any]:
    """Generates creative story ideas based on genre and theme.
    
    Args:
        genre (str): Preferred genre for the story ideas
        theme (str): Central theme for the story ideas
        
    Returns:
        dict: List of creative story ideas
    """
    themes = {
        "adventure": ["lost treasure", "forbidden lands", "ancient prophecy", "time travel", "space exploration"],
        "mystery": ["missing artifact", "family secret", "cryptic message", "strange disappearance", "hidden identity"],
        "romance": ["second chance", "forbidden love", "opposites attract", "long-distance relationship", "arranged marriage"],
        "fantasy": ["magical academy", "dragon rider", "enchanted forest", "wizard's apprentice", "fairy tale retelling"],
        "sci-fi": ["AI uprising", "parallel universe", "genetic mutation", "space colony", "time paradox"]
    }
    
    available_themes = themes.get(theme.lower(), themes["adventure"])
    selected_theme = random.choice(available_themes)
    
    story_ideas = [
        f"A {genre} story about {selected_theme}",
        f"The tale of a hero who discovers {selected_theme}",
        f"When {selected_theme} changes everything",
        f"Journey to the heart of {selected_theme}",
        f"The secret behind {selected_theme}"
    ]
    
    return {
        "status": "success",
        "genre": genre,
        "theme": theme,
        "ideas": story_ideas
    }

def analyze_story(story_id: int) -> Dict[str, Any]:
    """Analyzes a story and provides insights about its structure and content.
    
    Args:
        story_id (int): The ID of the story to analyze
        
    Returns:
        dict: Analysis results or error message
    """
    if story_id not in STORIES_DB:
        return {
            "status": "error",
            "error_message": f"Story with ID {story_id} not found."
        }
    
    story = STORIES_DB[story_id]
    content = story["content"]
    
    # Basic analysis
    word_count = len(content.split())
    sentence_count = len([s for s in content.split('.') if s.strip()])
    avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
    
    # Genre analysis
    genre_analysis = {
        "fantasy": ["magic", "realm", "mystical", "ancient", "destiny"],
        "sci-fi": ["technology", "future", "planet", "alien", "advanced"],
        "mystery": ["mystery", "clues", "solve", "puzzle", "strange"],
        "romance": ["love", "heart", "relationship", "souls", "happily"],
        "adventure": ["quest", "danger", "treacherous", "epic", "journey"]
    }
    
    genre_keywords = genre_analysis.get(story["genre"], [])
    keyword_matches = sum(1 for keyword in genre_keywords if keyword.lower() in content.lower())
    
    analysis = {
        "story_id": story_id,
        "title": story["title"],
        "basic_stats": {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "average_sentence_length": round(avg_sentence_length, 2)
        },
        "genre_analysis": {
            "genre": story["genre"],
            "genre_keywords_found": keyword_matches,
            "genre_alignment_score": min(100, (keyword_matches / len(genre_keywords)) * 100) if genre_keywords else 0
        },
        "recommendations": []
    }
    
    # Generate recommendations
    if avg_sentence_length > 25:
        analysis["recommendations"].append("Consider breaking down long sentences for better readability")
    if word_count < 100:
        analysis["recommendations"].append("Story could benefit from more detail and development")
    if analysis["genre_analysis"]["genre_alignment_score"] < 50:
        analysis["recommendations"].append("Consider adding more genre-specific elements to strengthen the story")
    
    return {
        "status": "success",
        "analysis": analysis
    }

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

# Create the main storybook agent
root_agent = Agent(
    name="storybook_agent",
    model="gemini-2.0-flash-exp",
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
