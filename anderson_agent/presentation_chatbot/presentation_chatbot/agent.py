"""Agent module for the presentation chatbot."""

import logging
import warnings
from google.adk.agents import Agent
from .config import config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .tools.tools_enhanced import (
    generate_presentation,
    generate_multi_slide_presentation,
    create_weekly_presentation,
    list_customers,
    get_presentation_templates,
    list_presentations,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

# Validate configuration
config.validate()

# configure logging
logger = logging.getLogger(__name__)


root_agent = Agent(
    name="presentation_chatbot",
    model="gemini-2.5-pro",
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    tools=[
        generate_presentation,
        generate_multi_slide_presentation,
        create_weekly_presentation,
        list_customers,
        get_presentation_templates,
        list_presentations,
    ],
)