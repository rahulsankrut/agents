"""Configuration settings for the timecard management agent."""

import os
import logging
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from env file if it exists
env_path = Path(__file__).parent.parent / "env"
if env_path.exists():
    load_dotenv(env_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AgentSettings(BaseSettings):
    """Agent configuration settings."""
    
    # Agent identity
    name: str = "Spark_v2"
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
        env_file = "env"
        extra = "ignore"  # Allow extra fields from .env


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.agent_settings = AgentSettings()
        
        # Google Cloud Configuration
        self.project_id: Optional[str] = os.getenv(
            "GOOGLE_CLOUD_PROJECT"
        ) or os.getenv("GCP_PROJECT_ID") or self.agent_settings.google_cloud_project
        self.location: Optional[str] = os.getenv(
            "GOOGLE_CLOUD_LOCATION", "us-central1"
        ).lower() or self.agent_settings.google_cloud_location
        self.use_vertex_ai: bool = (
            os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
        ) or (self.agent_settings.google_genai_use_vertexai == "1")
        
        # Model Configuration
        self.agent_model: str = os.getenv(
            "AGENT_MODEL", "gemini-2.5-pro"
        ) or self.agent_settings.model
        self.agent_name: str = os.getenv(
            "AGENT_NAME", "Spark_v2"
        ) or self.agent_settings.name
        
        # Validate required environment variables
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
        
        if not self.agent_settings.database_id:
            raise ValueError("DATABASE_ID environment variable is required")
            
        if not self.use_vertex_ai:
            raise ValueError("GOOGLE_GENAI_USE_VERTEXAI must be set to '1' for Vertex AI")
    
    @property
    def project_location(self) -> str:
        """Get the project location in the format required by Vertex AI."""
        return f"{self.project_id}.{self.location}"
    
    @property
    def model_config(self) -> dict:
        """Get the model configuration for Vertex AI."""
        return {
            "model": self.agent_model,
            "vertexai": True,
            "project": self.project_id,
            "location": self.location
        }
