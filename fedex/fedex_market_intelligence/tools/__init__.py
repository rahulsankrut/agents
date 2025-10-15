"""Tools for FedEx Market Intelligence Agent."""

from .trend_analysis import query_shipment_trends
from .geographic_analysis import analyze_geographic_demand
from .market_opportunities import find_market_opportunities
from .market_comparison import compare_markets
from .forecasting import forecast_demand
from .demographics import get_demographics
from .visualization import generate_map_visualization

__all__ = [
    "query_shipment_trends",
    "analyze_geographic_demand",
    "find_market_opportunities",
    "compare_markets",
    "forecast_demand",
    "get_demographics",
    "generate_map_visualization",
]

