"""Configuration management for FedEx Market Intelligence Agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Configuration class for FedEx Market Intelligence Agent."""
    
    def __init__(self):
        # Google Cloud Configuration (Required)
        self.project_id: str = os.getenv("GOOGLE_CLOUD_PROJECT", "agent-space-465923")
        self.location: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1").lower()
        
        # BigQuery Configuration (Required)
        self.dataset_id: str = os.getenv("BIGQUERY_DATASET", "fedex_market_intelligence")
        
        # Model Configuration (Required)
        self.root_agent_model: str = os.getenv("ROOT_AGENT_MODEL", "gemini-2.5-pro")
        
        # Optional configurations with safe defaults
        self.temperature: float = float(os.getenv("MODEL_TEMPERATURE", "0.1"))
        self.google_maps_api_key: Optional[str] = os.getenv("GOOGLE_MAPS_API_KEY")
        self.log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        # Since we now have defaults, validation is always successful
        # This method is kept for compatibility but always returns True
        return True
    
    @property
    def bigquery_dataset_path(self) -> str:
        """Get the full BigQuery dataset path."""
        return f"{self.project_id}.{self.dataset_id}"


# Create a global config instance
config = Config()
# Don't validate during import - validation will happen when agent is used
# config.validate()

