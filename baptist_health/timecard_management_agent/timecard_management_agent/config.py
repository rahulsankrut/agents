"""Configuration settings for the timecard management agent."""

import os
from typing import Optional
from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    """Agent configuration settings."""
    
    # Agent identity
    name: str = "Spark"
    model: str = "gemini-2.5-pro"
    
    # Firestore configuration
    project_id: str = "agent-space-465923"
    database_id: str = "timecard-demo-database"
    
    # Manager information
    manager_name: str = "Jenica"
    
    # Google Cloud settings (from .env file)
    google_cloud_project: Optional[str] = None
    google_cloud_location: Optional[str] = None
    google_genai_use_vertexai: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Allow extra fields from .env


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.agent_settings = AgentSettings()
        
        # Validate required environment variables
        if not self.agent_settings.project_id:
            raise ValueError("PROJECT_ID environment variable is required")
        
        if not self.agent_settings.database_id:
            raise ValueError("DATABASE_ID environment variable is required")
