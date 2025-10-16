# 📚 Storybook Agent

A creative AI agent built with Google's Agent Development Kit (ADK) that helps users create, edit, manage, and analyze stories. This agent combines the power of large language models with specialized tools to provide a comprehensive storytelling experience.

## ✨ Features

### 🎭 Story Creation
- **Multi-genre support**: Fantasy, Science Fiction, Mystery, Romance, Adventure
- **Customizable parameters**: Title, genre, main character, setting, plot points
- **Intelligent content generation**: AI-powered story content based on your specifications
- **Template-based generation**: Genre-specific story structures and themes

### 📝 Story Management
- **CRUD operations**: Create, read, update, and delete stories
- **Metadata tracking**: Creation date, word count, status, and more
- **Filtering and search**: Find stories by genre, status, or other criteria
- **Version control**: Track changes and updates to your stories

### 🔍 Story Analysis
- **Structural analysis**: Word count, sentence count, average sentence length
- **Genre alignment**: Score how well your story fits its intended genre
- **Smart recommendations**: AI-powered suggestions for improvement
- **Content insights**: Detailed breakdown of story elements

### 💡 Creative Assistance
- **Story idea generation**: Get inspired with creative prompts
- **Theme exploration**: Discover new narrative directions
- **Character development**: Suggestions for character arcs and motivations
- **Plot structuring**: Help with story pacing and structure

### 📤 Export Options
- **Multiple formats**: JSON, plain text, and Markdown
- **File naming**: Automatic filename generation
- **Content preservation**: Maintain all story metadata and formatting

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Cloud account with API access
- Google API key for authentication

### Installation

1. **Clone or navigate to the storybook directory:**
   ```bash
   cd storybook
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the storybook directory:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   
   **Note**: The API key is automatically loaded from environment variables by the Google ADK.

4. **Run the demo:**
   ```bash
   python demo.py
   ```

## 🛠️ Available Tools

The storybook agent comes with 8 powerful tools:

### 1. `create_story`
Creates a new story with customizable parameters.
```python
create_story(
    title="My Amazing Story",
    genre="fantasy",
    main_character="brave warrior",
    setting="enchanted forest",
    plot_points=3
)
```

### 2. `list_stories`
Lists all stories with optional filtering.
```python
list_stories(genre="fantasy", status="draft")
```

### 3. `get_story`
Retrieves a specific story by ID.
```python
get_story(story_id=1)
```

### 4. `edit_story`
Edits an existing story with new information.
```python
edit_story(
    story_id=1,
    title="Updated Title",
    content="New story content...",
    status="published"
)
```

### 5. `delete_story`
Removes a story from the database.
```python
delete_story(story_id=1)
```

### 6. `generate_story_ideas`
Generates creative story ideas based on genre and theme.
```python
generate_story_ideas(genre="sci-fi", theme="adventure")
```

### 7. `analyze_story`
Provides detailed analysis of story structure and content.
```python
analyze_story(story_id=1)
```

### 8. `export_story`
Exports a story in various formats.
```python
export_story(story_id=1, format="markdown")
```

## 🎯 Use Cases

### For Writers
- **Overcoming writer's block**: Generate story ideas and prompts
- **Genre exploration**: Try different writing styles and themes
- **Story development**: Get help with plot structure and character development
- **Content analysis**: Understand your writing patterns and improve

### For Educators
- **Creative writing classes**: Demonstrate storytelling concepts
- **Student projects**: Help students develop narrative skills
- **Assignment creation**: Generate writing prompts and examples
- **Feedback generation**: Provide structured analysis of student work

### For Content Creators
- **Social media content**: Generate engaging story snippets
- **Blog posts**: Create narrative content for various topics
- **Marketing campaigns**: Develop brand storytelling elements
- **Entertainment**: Create interactive storytelling experiences

## 🔧 Customization

### Adding New Genres
To add a new genre, modify the `genre_templates` dictionary in the `generate_story_content` function:

```python
genre_templates = {
    "horror": {
        "opening": "In the dark depths of {setting}, where shadows dance and fear lurks...",
        "conflict": "A terrifying presence emerged, testing the limits of human courage...",
        "resolution": "Through sheer willpower, the hero confronted the darkness..."
    }
    # ... existing genres
}
```

### Extending Story Analysis
Add new analysis metrics by modifying the `analyze_story` function:

```python
# Add new analysis criteria
if "dialogue" in content.lower():
    dialogue_count = content.count('"')
    analysis["dialogue_analysis"] = {
        "dialogue_marks": dialogue_count,
        "dialogue_density": dialogue_count / word_count
    }
```

### Adding Export Formats
Support new export formats by extending the `export_story` function:

```python
elif format.lower() == "html":
    export_content = f"""
    <html>
        <head><title>{story['title']}</title></head>
        <body>
            <h1>{story['title']}</h1>
            <p><strong>Genre:</strong> {story['genre']}</p>
            <p>{story['content']}</p>
        </body>
    </html>
    """
```

## 🚀 Deployment

### Local Development
The agent runs locally with in-memory storage. Perfect for development and testing.

### Production Deployment
For production use, consider:
- **Database integration**: Replace in-memory storage with PostgreSQL, MongoDB, etc.
- **API endpoints**: Create REST/GraphQL APIs for web/mobile access
- **Authentication**: Add user management and access control
- **Scalability**: Deploy to cloud platforms like Google Cloud, AWS, or Azure

### Google Cloud Vertex AI
The agent is designed to work with Google Cloud Vertex AI Agent Engines. See the deployment script in the parent directory for deployment instructions.

## 🤝 Contributing

Contributions are welcome! Areas for improvement include:
- **Additional genres and themes**
- **Enhanced story analysis algorithms**
- **More export formats**
- **Integration with external services**
- **Performance optimizations**

## 📄 License

This project is part of the Google ADK samples and follows the same licensing terms.

## 🆘 Support

For issues and questions:
1. Check the Google ADK documentation
2. Review the demo script for usage examples
3. Examine the tool function docstrings for detailed parameter information

## 🔮 Future Enhancements

Planned features include:
- **Multi-language support**: Generate stories in different languages
- **Audio narration**: Convert stories to speech
- **Image generation**: Create illustrations for stories
- **Collaborative writing**: Multi-user story creation
- **Advanced analytics**: Sentiment analysis, readability scores
- **Integration APIs**: Connect with writing platforms and tools

---

**Happy storytelling! 📚✨**
