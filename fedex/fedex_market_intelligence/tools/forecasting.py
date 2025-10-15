"""Demand forecasting tool using SQL-based time series analysis."""

from google.cloud import bigquery
import json
from typing import Optional

from fedex_market_intelligence.config import config

PROJECT_ID = config.project_id
DATASET_ID = config.dataset_id


def forecast_demand(
    product_category: str,
    market: str,
    forecast_months: int = 6
) -> str:
    """
    Forecast future demand using historical trends and seasonality.
    
    Use this tool to predict future shipment volumes based on historical patterns.
    
    Args:
        product_category: Product category ID (e.g., 'home_fitness', 'pet_supplies', 'consumer_electronics')
                         Note: Use the category_id format with underscores, not the display name
        market: Geographic market (e.g., 'California', 'Phoenix Metro', 'Northeast')
        forecast_months: Number of months to forecast, between 3 and 12 (default: 6)
    
    Returns:
        JSON string with detailed demand forecast including:
        - Monthly predictions
        - Confidence intervals
        - Growth trends
        - Seasonality factors
    
    Example:
        forecast_demand('home_fitness', 'California', 6)
    """
    
    if forecast_months < 3 or forecast_months > 12:
        return json.dumps({
            "error": "Forecast months must be between 3 and 12"
        }, indent=2)
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Parse market location - handle common state names
    market_lower = market.lower()
    
    # Map common state names to abbreviations
    state_mapping = {
        'california': 'CA', 'texas': 'TX', 'florida': 'FL', 'new york': 'NY',
        'illinois': 'IL', 'pennsylvania': 'PA', 'ohio': 'OH', 'georgia': 'GA',
        'north carolina': 'NC', 'michigan': 'MI', 'arizona': 'AZ', 'tennessee': 'TN',
        'massachusetts': 'MA', 'washington': 'WA', 'colorado': 'CO', 'oregon': 'OR'
    }
    
    state_abbr = state_mapping.get(market_lower, market_lower.upper()[:2])
    
    location_filter = f"""(
        LOWER(gm.city) LIKE '%{market_lower}%' OR
        LOWER(gm.metro_area) LIKE '%{market_lower}%' OR
        LOWER(gm.region) LIKE '%{market_lower}%' OR
        LOWER(gm.state) LIKE '%{market_lower}%' OR
        UPPER(gm.state) = '{state_abbr}'
    )"""
    
    # Query to get historical data and calculate trends
    query = f"""
        WITH historical_data AS (
            SELECT 
                ad.year_month,
                EXTRACT(MONTH FROM PARSE_DATE('%Y-%m', ad.year_month)) as month_num,
                EXTRACT(YEAR FROM PARSE_DATE('%Y-%m', ad.year_month)) as year_num,
                SUM(ad.total_shipments) as total_shipments,
                SUM(ad.total_value) as total_value,
                AVG(ad.growth_rate_yoy) as avg_growth_rate,
                COUNT(DISTINCT ad.zip_code) as zip_count
            FROM `{PROJECT_ID}.{DATASET_ID}.aggregated_demand` ad
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.geographic_metadata` gm
                ON ad.zip_code = gm.zip_code
            WHERE ad.product_category = '{product_category}'
            AND {location_filter}
            GROUP BY ad.year_month
            ORDER BY ad.year_month
        ),
        recent_trends AS (
            SELECT 
                AVG(total_shipments) as avg_monthly_shipments,
                AVG(avg_growth_rate) as avg_growth_rate,
                STDDEV(total_shipments) as stddev_shipments
            FROM historical_data
            WHERE year_month >= FORMAT_DATE('%Y-%m', DATE_SUB(DATE('2025-12-31'), INTERVAL 12 MONTH))
        ),
        seasonality AS (
            SELECT 
                month_num,
                AVG(total_shipments) as avg_shipments_for_month,
                AVG(total_shipments) / (SELECT AVG(total_shipments) FROM historical_data) as seasonality_factor
            FROM historical_data
            GROUP BY month_num
        )
        SELECT 
            (SELECT avg_monthly_shipments FROM recent_trends) as baseline_shipments,
            (SELECT avg_growth_rate FROM recent_trends) as avg_growth_rate,
            (SELECT stddev_shipments FROM recent_trends) as stddev_shipments,
            month_num,
            seasonality_factor
        FROM seasonality
        ORDER BY month_num
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        # Extract baseline and seasonality
        baseline_shipments = 0
        avg_growth_rate = 0
        stddev_shipments = 0
        seasonality_factors = {}
        
        for row in results:
            baseline_shipments = row['baseline_shipments'] or 0
            avg_growth_rate = row['avg_growth_rate'] or 0
            stddev_shipments = row['stddev_shipments'] or 0
            seasonality_factors[row['month_num']] = row['seasonality_factor'] or 1.0
        
        if baseline_shipments == 0:
            # Provide helpful suggestions
            available_categories = [
                "pet_supplies", "consumer_electronics", "coffee_products", "skincare",
                "home_fitness", "winter_outerwear", "books", "toys", "home_decor",
                "kitchen_appliances", "baby_products", "vitamins_supplements", 
                "outdoor_gear", "beauty_cosmetics", "jewelry", "sporting_goods"
            ]
            
            return json.dumps({
                "error": f"No historical data found for '{product_category}' in {market}",
                "suggestion": "Try a different market or product category",
                "help": {
                    "note": "Make sure to use the category_id format (with underscores)",
                    "example_categories": available_categories[:10],
                    "example_markets": ["California", "Phoenix Metro", "Austin", "Chicago Metro", "Northeast", "Southwest"]
                }
            }, indent=2)
        
        # Generate forecast
        forecasts = []
        current_date = "2025-12-31"
        
        # Apply growth rate (as monthly rate)
        monthly_growth_rate = avg_growth_rate / 100 / 12  # Convert YoY to monthly
        
        for i in range(1, forecast_months + 1):
            # Calculate future month/year
            future_month = (12 + i) % 12  # Start from Jan 2026
            if future_month == 0:
                future_month = 12
            future_year = 2026 if i <= 12 else 2027
            
            # Get seasonality factor
            seasonality = seasonality_factors.get(future_month, 1.0)
            
            # Calculate forecast with growth and seasonality
            growth_factor = (1 + monthly_growth_rate) ** i
            forecast_value = baseline_shipments * growth_factor * seasonality
            
            # Calculate confidence interval (simple approach)
            confidence_lower = max(0, forecast_value - stddev_shipments)
            confidence_upper = forecast_value + stddev_shipments
            
            forecasts.append({
                "month": f"{future_year}-{future_month:02d}",
                "forecasted_shipments": int(round(forecast_value)),
                "confidence_interval_lower": int(round(confidence_lower)),
                "confidence_interval_upper": int(round(confidence_upper)),
                "seasonality_factor": round(seasonality, 2),
                "growth_factor": round(growth_factor, 2)
            })
        
        # Generate insights
        insights = []
        total_forecast = sum(f['forecasted_shipments'] for f in forecasts)
        avg_forecast = total_forecast / len(forecasts)
        
        peak_month = max(forecasts, key=lambda x: x['forecasted_shipments'])
        insights.append(f"Peak demand expected in {peak_month['month']} with {peak_month['forecasted_shipments']:,} shipments")
        
        if avg_growth_rate > 10:
            insights.append(f"Strong growth momentum: {avg_growth_rate:.1f}% YoY growth rate")
        elif avg_growth_rate < 0:
            insights.append(f"Declining trend: {avg_growth_rate:.1f}% YoY growth rate")
        else:
            insights.append(f"Stable market: {avg_growth_rate:.1f}% YoY growth rate")
        
        response = {
            "query_parameters": {
                "product_category": product_category,
                "market": market,
                "forecast_months": forecast_months
            },
            "baseline_metrics": {
                "current_avg_monthly_shipments": int(round(baseline_shipments)),
                "avg_growth_rate_yoy": round(avg_growth_rate, 2),
                "volatility_stddev": int(round(stddev_shipments))
            },
            "forecast": forecasts,
            "summary": {
                "total_forecasted_shipments": total_forecast,
                "avg_monthly_forecast": int(round(avg_forecast)),
                "insights": insights
            },
            "methodology": "Simple time series forecast using 12-month moving average, historical growth rates, and seasonal patterns"
        }
        
        return json.dumps(response, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query
        }, indent=2)

