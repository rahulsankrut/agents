"""Configuration module for the presentation chatbot."""

import os
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from env file if it exists
env_path = Path(__file__).parent.parent / "env"
if env_path.exists():
    load_dotenv(env_path)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Config:
    def __init__(self):
        # Google Cloud Configuration
        self.project_id: Optional[str] = os.getenv(
            "GOOGLE_CLOUD_PROJECT"
        ) or os.getenv("GCP_PROJECT_ID")
        self.location: Optional[str] = os.getenv(
            "GOOGLE_CLOUD_LOCATION", "us-central1"
        ).lower()
        self.use_vertex_ai: bool = (
            os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "0") == "1"
        )

        # Model Configuration
        self.agent_model: str = os.getenv(
            "AGENT_MODEL", "gemini-2.5-pro"
        )
        self.agent_name: str = os.getenv(
            "AGENT_NAME", "presentation_chatbot"
        )

        # Cloud Function Configuration
        self.cloud_function_url: str = os.getenv(
            "CLOUD_FUNCTION_URL",
            "https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator"
        )

    def validate(self) -> bool:
        """Validate that all required configuration is present."""
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is required")
        if not self.use_vertex_ai:
            raise ValueError("GOOGLE_GENAI_USE_VERTEXAI must be set to '1' for Vertex AI")
        return True

    @property
    def project_location(self) -> str:
        """Get the project location in the format required by Vertex AI."""
        return f"{self.project_id}.{self.location}"


# Create a global config instance
config = Config()
