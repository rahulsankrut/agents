"""
FedEx Site Selection Agent - Helps identify optimal business locations.
"""

from google.adk.agents import Agent
from .prompt import SITE_SELECTION_AGENT_PROMPT
from .tools.analysis_tools import (
    query_shipment_volume,
    analyze_category_demand,
    calculate_growth_trends,
    compare_locations,
    identify_demand_gaps,
    get_available_categories,
)

# Create the agent
root_agent = Agent(
    name="fedex_site_selection_agent",
    model="gemini-2.5-pro",
    instruction=SITE_SELECTION_AGENT_PROMPT,
    tools=[
        query_shipment_volume,
        analyze_category_demand,
        calculate_growth_trends,
        compare_locations,
        identify_demand_gaps,
        get_available_categories,
    ],
)
