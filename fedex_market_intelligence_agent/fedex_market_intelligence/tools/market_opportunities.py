"""Market opportunity identification tool - find gaps and underserved areas."""

from google.cloud import bigquery
from typing import Optional
import json

from fedex_market_intelligence.config import config

PROJECT_ID = config.project_id
DATASET_ID = config.dataset_id


def find_market_opportunities(
    product_category: str,
    market: str,
    gap_type: str = "low_competition",
    min_demand_threshold: int = 50,
    top_n: int = 10
) -> str:
    """
    Find market opportunities by identifying gaps, underserved areas, and high-potential locations.
    
    This tool analyzes FedEx shipping data to find ZIP codes with untapped business potential.
    Use this when the user asks about:
    - Where to open a new location
    - Finding areas with low competition
    - Identifying underserved markets
    - Discovering high-growth opportunities
    - Spotting gaps in market coverage
    
    Args:
        product_category: Product category (e.g., 'pet_supplies', 'consumer_electronics', 'coffee_products')
        market: Geographic market name (e.g., 'Phoenix', 'Chicago', 'Northeast')
                Note: Use city/metro/region names; "suburbs" keyword will be auto-handled
        gap_type: Type of opportunity to find:
            - 'low_competition': Areas with demand but low major brand presence
            - 'high_growth': Fast-growing markets (>20% YoY growth)
            - 'underserved': High demand areas with few suppliers
            - 'emerging': Growing markets with strong momentum (>15% growth)
        min_demand_threshold: Minimum monthly shipments required (default: 50)
                              Lower this (e.g., 10-20) for niche categories or smaller markets
        top_n: Number of top opportunities to return (default: 10)
    
    Returns:
        JSON string with detailed market opportunity analysis including:
        - ZIP codes with opportunity scores
        - Demand metrics and growth rates
        - Competition levels
        - Actionable insights
    
    Example:
        find_market_opportunities('pet_supplies', 'Phoenix', 'low_competition')
        Returns ZIP codes in Phoenix with high pet supply demand but low competition
    """
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Parse market location - handle "suburbs" and state names
    market_lower = market.lower()
    
    # Remove "suburbs", "suburban", "metro" keywords and use base location
    base_market = market_lower.replace(' suburbs', '').replace(' suburban', '').replace(' metro', '').strip()
    
    # Map common state names
    state_mapping = {
        'california': 'CA', 'texas': 'TX', 'florida': 'FL', 'new york': 'NY',
        'illinois': 'IL', 'pennsylvania': 'PA', 'ohio': 'OH', 'georgia': 'GA',
        'north carolina': 'NC', 'michigan': 'MI', 'arizona': 'AZ', 'tennessee': 'TN',
        'massachusetts': 'MA', 'washington': 'WA', 'colorado': 'CO', 'oregon': 'OR'
    }
    
    state_abbr = state_mapping.get(base_market, base_market.upper()[:2])
    
    location_filter = f"""(
        LOWER(gm.city) LIKE '%{base_market}%' OR
        LOWER(gm.metro_area) LIKE '%{base_market}%' OR
        LOWER(gm.region) LIKE '%{base_market}%' OR
        LOWER(gm.state) LIKE '%{base_market}%' OR
        UPPER(gm.state) = '{state_abbr}'
    )"""
    
    # Build query based on gap type
    if gap_type == "low_competition":
        # Areas with demand but low major brand presence
        additional_filters = "AND market_concentration < 50"
        order_by = "market_concentration ASC, total_shipments DESC"
        description = "Areas with high demand but low major brand presence"
        
    elif gap_type == "high_growth":
        # Fast growing markets
        additional_filters = "AND avg_growth_rate > 20"
        order_by = "avg_growth_rate DESC"
        description = "Fast-growing markets with momentum"
        
    elif gap_type == "underserved":
        # High demand but few unique shippers
        additional_filters = "AND avg_unique_shippers < 10"
        order_by = "total_shipments DESC"
        description = "High demand areas with few suppliers"
        
    else:  # emerging
        # Growing markets with increasing demand
        additional_filters = "AND avg_growth_rate > 15 AND total_shipments > 50"
        order_by = "avg_growth_rate DESC"
        description = "Emerging markets with strong growth signals"
    
    query = f"""
        WITH opportunity_data AS (
            SELECT 
                ad.zip_code,
                gm.city,
                gm.state,
                gm.metro_area,
                gm.lat,
                gm.lng,
                ch.category_name,
                SUM(ad.total_shipments) as total_shipments,
                AVG(ad.total_value) as avg_monthly_value,
                AVG(ad.growth_rate_yoy) as avg_growth_rate,
                AVG(ad.unique_shippers) as avg_unique_shippers,
                AVG(COALESCE(ms.market_concentration_index, 50)) as market_concentration,
                AVG(COALESCE(ms.major_brand_volume, 0)) as avg_major_brand_volume,
                AVG(COALESCE(ms.small_business_volume, 0)) as avg_small_business_volume
            FROM `{PROJECT_ID}.{DATASET_ID}.aggregated_demand` ad
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.geographic_metadata` gm
                ON ad.zip_code = gm.zip_code
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.market_share` ms
                ON ad.zip_code = ms.zip_code 
                AND ad.year_month = ms.year_month
                AND ad.product_category = ms.product_category
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.category_hierarchy` ch
                ON ad.product_category = ch.category_id
            WHERE ad.product_category = '{product_category}'
            AND {location_filter}
            AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 12
            GROUP BY ad.zip_code, gm.city, gm.state, gm.metro_area, gm.lat, gm.lng, ch.category_name
            HAVING SUM(ad.total_shipments) >= {min_demand_threshold}
        )
        SELECT *
        FROM opportunity_data
        WHERE 1=1 {additional_filters}
        ORDER BY {order_by}
        LIMIT {top_n}
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list of dicts
        opportunities = []
        row_count = 0
        for row in results:
            row_count += 1
            row_dict = dict(row)
            
            # Round numeric values
            for key in ['avg_monthly_value', 'avg_growth_rate', 'market_concentration', 
                       'avg_major_brand_volume', 'avg_small_business_volume', 'avg_unique_shippers']:
                if key in row_dict and row_dict[key] is not None:
                    row_dict[key] = round(row_dict[key], 2)
            
            # Add opportunity score (simple weighted calculation)
            score = 0
            if gap_type == "low_competition":
                score = (100 - row_dict.get('market_concentration', 50)) + (row_dict.get('total_shipments', 0) / 10)
            elif gap_type == "high_growth":
                score = row_dict.get('avg_growth_rate', 0)
            elif gap_type == "underserved":
                score = row_dict.get('total_shipments', 0) / (row_dict.get('avg_unique_shippers', 1) or 1)
            else:  # emerging
                score = row_dict.get('avg_growth_rate', 0) * 1.5
            
            row_dict['opportunity_score'] = round(score, 2)
            opportunities.append(row_dict)
        
        # Generate insights
        insights = []
        if opportunities:
            top = opportunities[0]
            if gap_type == "low_competition":
                insights.append(f"Top opportunity in {top.get('city', 'unknown')}: {top.get('total_shipments', 0)} monthly shipments with only {top.get('market_concentration', 0):.0f}% major brand dominance")
            elif gap_type == "high_growth":
                insights.append(f"Fastest growth in {top.get('city', 'unknown')}: {top.get('avg_growth_rate', 0):.1f}% YoY growth")
            elif gap_type == "underserved":
                insights.append(f"Most underserved: {top.get('city', 'unknown')} with {top.get('total_shipments', 0)} monthly shipments but only {top.get('avg_unique_shippers', 0):.0f} suppliers")
        elif row_count == 0 and min_demand_threshold > 20:
            # Suggest trying with lower threshold
            insights.append(f"No opportunities found with current threshold ({min_demand_threshold} shipments/month). Try lowering the min_demand_threshold parameter.")
        
        response = {
            "query_parameters": {
                "product_category": product_category,
                "market": market,
                "gap_type": gap_type,
                "description": description,
                "min_demand_threshold": min_demand_threshold
            },
            "summary": {
                "opportunities_found": len(opportunities),
                "analysis_type": description
            },
            "insights": insights,
            "opportunities": opportunities
        }
        
        return json.dumps(response, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query
        }, indent=2)

