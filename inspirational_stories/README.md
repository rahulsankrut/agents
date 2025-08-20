# 🌟 Inspirational Stories Agent

An AI-powered agent that creates engaging, educational stories for children about famous personalities. This agent combines research capabilities with creative storytelling to inspire young minds through real-life stories of courage, determination, and achievement.

## ✨ Features

### 🔍 **Research Capabilities**
- **AI-powered research**: Uses Gemini 2.5 Pro to gather comprehensive information about famous people
- **Customizable depth**: Choose from basic, comprehensive, or detailed research levels
- **Focused areas**: Specify what aspects to research (early life, achievements, challenges, legacy)
- **Child-friendly content**: Research is tailored for creating age-appropriate stories

### 📚 **Story Creation**
- **Dynamic storytelling**: AI generates unique, creative stories based on research
- **Age-appropriate content**: Stories tailored for different age groups (toddlers to teens)
- **Theme customization**: Choose story themes (overcoming challenges, achieving dreams, helping others)
- **Length control**: Generate short, medium, or long stories
- **Life lessons**: Option to include educational morals and values

### 🎯 **Inspirational Discovery**
- **Person suggestions**: AI recommends inspirational people in various categories
- **Category filtering**: Explore scientists, artists, leaders, athletes, and more
- **Value-based selection**: Focus on people who demonstrate specific qualities
- **Age-appropriate recommendations**: Ensure suitability for target audience

### 🔧 **Story Enhancement**
- **Age adaptation**: Modify stories for different age groups
- **Engagement improvement**: Make stories more captivating and interactive
- **Educational enhancement**: Add learning opportunities and facts
- **Emotional connection**: Strengthen character relatability for children

### 📤 **Export & Management**
- **Multiple formats**: Export as text, markdown, or JSON
- **Story organization**: List, filter, and manage created stories
- **Research tracking**: Keep track of all research conducted
- **Metadata management**: Comprehensive story and research information

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Cloud account with API access
- Google API key for authentication

### Installation

1. **Navigate to the inspirational_stories directory:**
   ```bash
   cd inspirational_stories
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your environment variables:**
   Create a `.env` file in the inspirational_stories directory:
   ```bash
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

4. **Run the demo:**
   ```bash
   python demo.py
   ```

## 🛠️ Available Tools

The inspirational stories agent comes with 8 powerful tools:

### 1. `research_famous_person`
Conducts AI-powered research on any famous personality.
```python
research_famous_person(
    person_name="Marie Curie",
    research_depth="comprehensive",
    focus_areas=["early life", "achievements", "challenges overcome"]
)
```

### 2. `create_inspirational_story`
Creates an inspirational children's story about a famous person.
```python
create_inspirational_story(
    person_name="Albert Einstein",
    story_theme="achieving dreams",
    target_age="8-12",
    story_length="medium",
    include_lessons=True
)
```

### 3. `suggest_inspirational_people`
Recommends inspirational people for children's stories.
```python
suggest_inspirational_people(
    category="scientists",
    age_group="children",
    interests=["curiosity", "perseverance", "discovery"]
)
```

### 4. `enhance_story_for_children`
Enhances stories to be more suitable for children.
```python
enhance_story_for_children(
    story_id=1,
    enhancement_type="age_appropriate",
    target_age="5-8"
)
```

### 5. `list_stories`
Lists all created stories with optional filtering.
```python
list_stories(person_name="Marie Curie", theme="overcoming challenges")
```

### 6. `get_story`
Retrieves a specific story by ID.
```python
get_story(story_id=1)
```

### 7. `list_research`
Lists all research conducted with optional filtering.
```python
list_research(person_name="Albert Einstein")
```

### 8. `export_story`
Exports stories in various formats.
```python
export_story(story_id=1, format="markdown")
```

## 🎯 Use Cases

### For Parents & Educators
- **Bedtime stories**: Create engaging stories about real heroes
- **Classroom learning**: Teach history and values through storytelling
- **Character development**: Inspire positive qualities in children
- **Educational content**: Make learning fun and memorable

### For Content Creators
- **Children's books**: Generate story ideas and content
- **Educational materials**: Create age-appropriate learning resources
- **Social media content**: Share inspirational stories for families
- **Podcast scripts**: Develop engaging narratives for young audiences

### For Libraries & Schools
- **Reading programs**: Provide diverse, inspirational content
- **Cultural education**: Introduce children to global heroes
- **Value-based learning**: Teach important life lessons
- **Multicultural stories**: Celebrate diversity and inclusion

## 🔍 How It Works

### **1. Research Phase**
- User specifies a famous person to research
- Agent uses Gemini AI to gather comprehensive information
- Research focuses on child-friendly, inspirational aspects
- Information is stored for story creation

### **2. Story Generation**
- Agent combines research with story parameters
- Gemini AI creates unique, engaging narratives
- Stories are tailored for specific age groups
- Content includes appropriate themes and lessons

### **3. Enhancement & Customization**
- Stories can be enhanced for different age groups
- Content is adapted for engagement and education
- Multiple enhancement types available
- Continuous improvement through AI feedback

## 🌍 Example Personalities

### **Scientists & Inventors**
- Marie Curie (perseverance, discovery)
- Albert Einstein (creativity, imagination)
- Thomas Edison (persistence, innovation)
- Jane Goodall (compassion, curiosity)

### **Leaders & Activists**
- Mahatma Gandhi (peace, nonviolence)
- Rosa Parks (courage, justice)
- Nelson Mandela (forgiveness, leadership)
- Malala Yousafzai (education, bravery)

### **Artists & Creators**
- Frida Kahlo (self-expression, resilience)
- Vincent van Gogh (creativity, passion)
- Maya Angelou (words, wisdom)
- Walt Disney (imagination, dreams)

### **Athletes & Explorers**
- Jesse Owens (determination, breaking barriers)
- Amelia Earhart (adventure, courage)
- Jackie Robinson (perseverance, dignity)
- Edmund Hillary (adventure, teamwork)

## 🔧 Customization

### Adding New Categories
Extend the agent to include new categories of inspirational people:
```python
# Add new categories to suggest_inspirational_people
categories = ["environmentalists", "musicians", "writers", "philosophers"]
```

### Custom Research Areas
Define specific research focus areas for different types of stories:
```python
focus_areas = {
    "scientists": ["discoveries", "experiments", "scientific method"],
    "artists": ["creative process", "inspiration", "artistic vision"],
    "leaders": ["leadership style", "decision making", "vision"]
}
```

### Story Theme Expansion
Add new story themes and educational objectives:
```python
themes = {
    "environmental stewardship": "caring for the planet",
    "cultural appreciation": "celebrating diversity",
    "scientific curiosity": "asking questions and exploring"
}
```

## 🚀 Deployment

### Local Development
Perfect for personal use, education, and content creation.

### Production Use
Consider:
- **Database integration**: Replace in-memory storage
- **User management**: Add authentication and user accounts
- **Content moderation**: Ensure age-appropriate content
- **API endpoints**: Create web/mobile interfaces
- **Content distribution**: Share stories across platforms

## 🤝 Contributing

Areas for improvement:
- **Additional research sources**: Integrate with external APIs
- **Multilingual support**: Create stories in different languages
- **Audio generation**: Convert stories to speech
- **Illustration suggestions**: AI-powered visual content ideas
- **Interactive elements**: Add questions and activities to stories

## 📄 License

This project follows the same licensing terms as the Google ADK samples.

## 🆘 Support

For issues and questions:
1. Check the Google ADK documentation
2. Review the demo script for usage examples
3. Examine the tool function docstrings for detailed parameter information

## 🔮 Future Enhancements

Planned features:
- **Multimedia integration**: Images, audio, and interactive elements
- **Collaborative storytelling**: Multi-user story creation
- **Advanced analytics**: Story engagement and learning metrics
- **Curriculum integration**: Educational standards alignment
- **Parent/teacher tools**: Discussion guides and activities

---

**Inspiring the next generation, one story at a time! 🌟📚✨**
