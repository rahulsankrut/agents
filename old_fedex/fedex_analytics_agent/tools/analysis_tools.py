"""
Analysis tools for FedEx Site Selection Agent.
All BigQuery analysis and visualization functions.
"""

from typing import Optional
import os
from .bigquery_tool import BigQueryAnalysisTool
from .visualization_tool import VisualizationTool

# Initialize tools
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "agent-space-465923")
DATASET_ID = os.getenv("BIGQUERY_DATASET", "fedex")

bq_tool = BigQueryAnalysisTool(PROJECT_ID, DATASET_ID)
viz_tool = VisualizationTool()


def query_shipment_volume(state: Optional[str] = None, city: Optional[str] = None, limit: int = 20) -> str:
    """Query shipment volume by location."""
    df = bq_tool.query_shipment_volume_by_location(state, city, limit)
    if df.empty:
        return "No data found."
    
    viz = viz_tool.create_demand_heatmap(df, 'shipment_count', "Shipment Volume")
    return f"**Results:**\n\n{viz_tool.format_dataframe_for_display(df)}\n\n![Chart](data:image/png;base64,{viz})"


def analyze_category_demand(category: str, state: Optional[str] = None, limit: int = 10) -> str:
    """Analyze demand for specific product category (pet, electronics, health, sports, etc)."""
    df = bq_tool.analyze_category_demand_by_location(category, state, limit)
    if df.empty:
        return f"No data found for '{category}'."
    
    viz = viz_tool.create_demand_heatmap(df, 'shipment_count', f"{category.title()} Demand")
    return f"**{category.title()} Demand:**\n\n{viz_tool.format_dataframe_for_display(df)}\n\n![Chart](data:image/png;base64,{viz})"


def calculate_growth_trends(location_type: str = "city", category: Optional[str] = None, min_months: int = 6) -> str:
    """Calculate growth trends. location_type: 'city', 'state', or 'zip'."""
    df = bq_tool.calculate_growth_trends(location_type, category, min_months)
    if df.empty:
        return "Insufficient data."
    
    viz = viz_tool.create_growth_trend_chart(df, 10, "Growth Trends")
    return f"**Growth Analysis:**\n\n{viz_tool.format_dataframe_for_display(df)}\n\n![Chart](data:image/png;base64,{viz})"


def compare_locations(
    location1_city: Optional[str] = None, location1_state: Optional[str] = None,
    location2_city: Optional[str] = None, location2_state: Optional[str] = None,
    category: Optional[str] = None
) -> str:
    """Compare two locations."""
    loc1 = {k.replace('location1_', ''): v for k, v in {'city': location1_city, 'state': location1_state}.items() if v}
    loc2 = {k.replace('location2_', ''): v for k, v in {'city': location2_city, 'state': location2_state}.items() if v}
    
    df = bq_tool.compare_locations(loc1, loc2, category)
    if df.empty:
        return "No data found."
    
    viz = viz_tool.create_location_comparison_chart(df, 'total_shipments', "Comparison")
    return f"**Comparison:**\n\n{viz_tool.format_dataframe_for_display(df)}\n\n![Chart](data:image/png;base64,{viz})"


def identify_demand_gaps(category: str, state: str, city: Optional[str] = None, min_demand: int = 10) -> str:
    """Find high-demand underserved areas - perfect for new store locations."""
    region = {'state': state, 'city': city} if city else {'state': state}
    df = bq_tool.identify_demand_gaps(category, region, min_demand)
    if df.empty:
        return f"No significant demand for '{category}'."
    
    viz = viz_tool.create_demand_gap_visualization(df, f"High Demand: {category.title()}")
    return f"**Site Selection Opportunities:**\n\n{viz_tool.format_dataframe_for_display(df)}\n\n![Chart](data:image/png;base64,{viz})"


def get_available_categories() -> str:
    """List all available product categories."""
    categories = bq_tool.get_available_categories()
    result = "**Available Categories:**\n" + "\n".join([f"- {cat}" for cat in categories[:30]])
    if len(categories) > 30:
        result += f"\n\n...and {len(categories) - 30} more"
    return result

