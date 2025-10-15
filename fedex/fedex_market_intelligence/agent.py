"""FedEx Market Intelligence Agent - Main Agent Entry Point"""

import logging
from datetime import date

from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import FunctionTool
from google.genai import types
import vertexai

# Import configuration
from fedex_market_intelligence.config import config

# Import tools
from fedex_market_intelligence.tools import (
    query_shipment_trends,
    analyze_geographic_demand,
    find_market_opportunities,
    compare_markets,
    forecast_demand,
    get_demographics,
    generate_map_visualization,
)

# Import prompts
from fedex_market_intelligence.prompt import SYSTEM_PROMPT

# Set up logging
logging.basicConfig(
    level=getattr(logging, config.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Vertex AI
vertexai.init(project=config.project_id, location=config.location)
logger.info(
    f"Initialized Vertex AI with project={config.project_id}, location={config.location}"
)


def load_config_in_context(callback_context: CallbackContext):
    """Load configuration settings into the callback context on first use."""
    if "config" not in callback_context.state:
        callback_context.state["config"] = {
            "project_id": config.project_id,
            "dataset_id": config.dataset_id,
            "bigquery_dataset_path": config.bigquery_dataset_path,
        }
        logger.debug("Loaded config into callback context")


# Create function tools (FunctionTool automatically uses function name and docstring)
query_shipment_trends_tool = FunctionTool(query_shipment_trends)
analyze_geographic_demand_tool = FunctionTool(analyze_geographic_demand)
find_market_opportunities_tool = FunctionTool(find_market_opportunities)
compare_markets_tool = FunctionTool(compare_markets)
forecast_demand_tool = FunctionTool(forecast_demand)
get_demographics_tool = FunctionTool(get_demographics)
generate_map_visualization_tool = FunctionTool(generate_map_visualization)


# Main agent for deployment
root_agent = LlmAgent(
    name="fedex_market_intelligence_agent",
    model=config.root_agent_model,
    instruction=SYSTEM_PROMPT,
    tools=[
        query_shipment_trends_tool,
        analyze_geographic_demand_tool,
        find_market_opportunities_tool,
        compare_markets_tool,
        forecast_demand_tool,
        get_demographics_tool,
        generate_map_visualization_tool,
    ],
    before_agent_callback=load_config_in_context,
    generate_content_config=types.GenerateContentConfig(
        temperature=config.temperature,
        top_p=0.95,
        top_k=40,
    ),
)

logger.info("FedEx Market Intelligence Agent initialized successfully")

