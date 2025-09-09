"""Agent module for the timecard management agent."""

import logging
import warnings
from google.adk import Agent
from .config import Config
from .prompts import GLOBAL_INSTRUCTION, INSTRUCTION
from .tools import (
    set_manager_context,
    get_summary,
    get_exceptions,
    approve_standard_timecards,
    get_employee_schedule,
    get_historical_comparison,
    draft_reminder_message,
)

warnings.filterwarnings("ignore", category=UserWarning, module=".*pydantic.*")

configs = Config()

# Configure logging
logger = logging.getLogger(__name__)


root_agent = Agent(
    model=configs.agent_model,
    global_instruction=GLOBAL_INSTRUCTION,
    instruction=INSTRUCTION,
    name=configs.agent_name,
    tools=[
        set_manager_context,
        get_summary,
        get_exceptions,
        approve_standard_timecards,
        get_employee_schedule,
        get_historical_comparison,
        draft_reminder_message,
    ],
)
