"""Geographic analysis tool for location-based insights."""

from google.cloud import bigquery
from typing import Optional, List
import json

from fedex_market_intelligence.config import config

PROJECT_ID = config.project_id
DATASET_ID = config.dataset_id


def analyze_geographic_demand(
    product_category: str,
    geographic_scope: str = "metro",
    demographic_filter: Optional[str] = None,
    time_period: str = "last_12_months",
    top_n: int = 10
) -> str:
    """
    Analyze demand patterns by geographic location.
    
    Args:
        product_category: Product category to analyze
        geographic_scope: Level of analysis - 'zip', 'city', 'metro', 'state', 'region'
        demographic_filter: Optional demographic filter (e.g., 'millennial_heavy', 'high_income')
        time_period: Time range to analyze
        top_n: Number of top locations to return
    
    Returns:
        JSON string with geographic analysis results
    """
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Parse time period
    time_filter = ""
    if time_period == "last_6_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 6"
    elif time_period == "last_12_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 12"
    elif time_period == "last_24_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 24"
    
    # Determine grouping field - always include coordinates for visualization
    if geographic_scope == "zip":
        group_field = "ad.zip_code, gm.city, gm.state, gm.metro_area, gm.lat, gm.lng"
        select_fields = "ad.zip_code as location, gm.city, gm.state, gm.metro_area, gm.lat, gm.lng"
    elif geographic_scope == "city":
        group_field = "gm.city, gm.state"
        select_fields = "CONCAT(gm.city, ', ', gm.state) as location, ANY_VALUE(gm.lat) as lat, ANY_VALUE(gm.lng) as lng"
    elif geographic_scope == "metro":
        group_field = "gm.metro_area, gm.region"
        select_fields = "gm.metro_area as location, gm.region, ANY_VALUE(gm.lat) as lat, ANY_VALUE(gm.lng) as lng"
    elif geographic_scope == "state":
        group_field = "gm.state, gm.region"
        select_fields = "gm.state as location, gm.region, ANY_VALUE(gm.lat) as lat, ANY_VALUE(gm.lng) as lng"
    elif geographic_scope == "region":
        group_field = "gm.region"
        select_fields = "gm.region as location, ANY_VALUE(gm.lat) as lat, ANY_VALUE(gm.lng) as lng"
    else:
        group_field = "gm.metro_area, gm.region"
        select_fields = "gm.metro_area as location, gm.region, ANY_VALUE(gm.lat) as lat, ANY_VALUE(gm.lng) as lng"
    
    query = f"""
        SELECT 
            {select_fields},
            ch.category_name,
            SUM(ad.total_shipments) as total_shipments,
            SUM(ad.total_value) as total_value,
            AVG(ad.growth_rate_yoy) as avg_growth_rate_yoy,
            AVG(ad.growth_rate_mom) as avg_growth_rate_mom,
            COUNT(DISTINCT ad.year_month) as months_with_data,
            COUNT(DISTINCT ad.zip_code) as unique_zip_codes
        FROM `{PROJECT_ID}.{DATASET_ID}.aggregated_demand` ad
        LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.geographic_metadata` gm
            ON ad.zip_code = gm.zip_code
        LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.category_hierarchy` ch
            ON ad.product_category = ch.category_id
        WHERE ad.product_category = '{product_category}'
        {time_filter}
        GROUP BY {group_field}, ch.category_name
        ORDER BY total_shipments DESC
        LIMIT {top_n}
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list of dicts
        data = []
        for row in results:
            row_dict = dict(row)
            # Round numeric values
            if 'avg_growth_rate_yoy' in row_dict:
                row_dict['avg_growth_rate_yoy'] = round(row_dict['avg_growth_rate_yoy'], 2)
            if 'avg_growth_rate_mom' in row_dict:
                row_dict['avg_growth_rate_mom'] = round(row_dict['avg_growth_rate_mom'], 2)
            if 'total_value' in row_dict:
                row_dict['total_value'] = round(row_dict['total_value'], 2)
            data.append(row_dict)
        
        # If demographic filter requested, add note
        demographic_note = None
        if demographic_filter:
            demographic_note = f"Note: Demographic filter '{demographic_filter}' would require Census API integration to be fully applied. Results show all areas for now."
        
        response = {
            "query_parameters": {
                "product_category": product_category,
                "geographic_scope": geographic_scope,
                "demographic_filter": demographic_filter,
                "time_period": time_period
            },
            "summary": {
                "total_locations": len(data),
                "total_shipments": sum(row.get('total_shipments', 0) for row in data),
                "avg_growth_rate": round(sum(row.get('avg_growth_rate_yoy', 0) for row in data) / len(data), 2) if data else 0
            },
            "top_locations": data,
            "demographic_note": demographic_note
        }
        
        return json.dumps(response, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query
        }, indent=2)

