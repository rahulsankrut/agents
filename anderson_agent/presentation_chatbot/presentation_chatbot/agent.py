"""Agent module for the presentation chatbot."""

import logging
import warnings
from google.adk import Agent
from .config import config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .tools.tools_enhanced import (
    generate_presentation,
    get_presentation_templates,
    list_presentations,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

# Validate configuration
config.validate()

# configure logging
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=config.agent_model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=config.agent_name,
    tools=[
        generate_presentation,
        get_presentation_templates,
        list_presentations,
    ],
)
