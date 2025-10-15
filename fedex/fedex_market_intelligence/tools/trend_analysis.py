"""Time series analysis tool for shipment trends."""

from google.cloud import bigquery
from typing import Optional
import json

from fedex_market_intelligence.config import config

PROJECT_ID = config.project_id
DATASET_ID = config.dataset_id


def query_shipment_trends(
    product_category: str,
    location: Optional[str] = None,
    time_period: str = "last_12_months",
    metric: str = "volume",
    limit: int = 100
) -> str:
    """
    Analyze shipment trends over time for specific products and locations.
    
    Args:
        product_category: Product category to analyze (e.g., 'pet_supplies', 'consumer_electronics')
        location: Geographic filter - can be zip code, city, state, metro area, or region
        time_period: Time range - 'last_6_months', 'last_12_months', 'last_24_months', 'last_36_months', 'ytd', 'q3_2025'
        metric: What to measure - 'volume', 'growth_rate', 'value', 'market_share'
        limit: Maximum number of results to return
    
    Returns:
        JSON string with trend analysis results
    """
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Parse time period
    where_clauses = [f"ad.product_category = '{product_category}'"]
    
    if time_period == "last_6_months":
        where_clauses.append("DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 6")
    elif time_period == "last_12_months":
        where_clauses.append("DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 12")
    elif time_period == "last_24_months":
        where_clauses.append("DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 24")
    elif time_period == "last_36_months":
        where_clauses.append("DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 36")
    elif time_period == "ytd":
        where_clauses.append("EXTRACT(YEAR FROM PARSE_DATE('%Y-%m', ad.year_month)) = 2025")
    elif time_period.startswith("q") and "2025" in time_period:
        # Handle Q3 2025, Q1 2025, etc.
        quarter = time_period[1]
        where_clauses.append(f"EXTRACT(YEAR FROM PARSE_DATE('%Y-%m', ad.year_month)) = 2025")
        where_clauses.append(f"EXTRACT(QUARTER FROM PARSE_DATE('%Y-%m', ad.year_month)) = {quarter}")
    
    # Parse location filter
    if location:
        location_lower = location.lower()
        # Try to determine location type
        if len(location) == 5 and location.isdigit():
            # Zip code
            where_clauses.append(f"ad.zip_code = '{location}'")
        elif len(location) == 2 and location.isupper():
            # State abbreviation
            where_clauses.append(f"UPPER(gm.state) = '{location.upper()}'")
        else:
            # City, metro area, or region - use flexible matching
            where_clauses.append(f"""(
                LOWER(gm.city) LIKE '%{location_lower}%' OR
                LOWER(gm.metro_area) LIKE '%{location_lower}%' OR
                LOWER(gm.region) LIKE '%{location_lower}%' OR
                LOWER(gm.state) LIKE '%{location_lower}%'
            )""")
    
    # Build query based on metric
    if metric == "growth_rate":
        order_by = "growth_rate_yoy DESC"
        select_fields = """
            ad.zip_code,
            gm.city,
            gm.state,
            gm.metro_area,
            gm.lat,
            gm.lng,
            ad.year_month,
            ad.total_shipments,
            ad.growth_rate_yoy,
            ad.growth_rate_mom,
            ch.category_name
        """
    elif metric == "value":
        order_by = "total_value DESC"
        select_fields = """
            ad.zip_code,
            gm.city,
            gm.state,
            gm.metro_area,
            gm.lat,
            gm.lng,
            ad.year_month,
            ad.total_shipments,
            ad.total_value,
            ad.growth_rate_yoy,
            ch.category_name
        """
    else:  # volume
        order_by = "total_shipments DESC"
        select_fields = """
            ad.zip_code,
            gm.city,
            gm.state,
            gm.metro_area,
            gm.lat,
            gm.lng,
            ad.year_month,
            ad.total_shipments,
            ad.total_value,
            ad.growth_rate_yoy,
            ch.category_name
        """
    
    query = f"""
        SELECT {select_fields}
        FROM `{PROJECT_ID}.{DATASET_ID}.aggregated_demand` ad
        LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.geographic_metadata` gm
            ON ad.zip_code = gm.zip_code
        LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.category_hierarchy` ch
            ON ad.product_category = ch.category_id
        WHERE {' AND '.join(where_clauses)}
        ORDER BY {order_by}
        LIMIT {limit}
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list of dicts
        data = []
        for row in results:
            data.append(dict(row))
        
        # Calculate summary statistics
        if data:
            total_shipments = sum(row.get('total_shipments', 0) for row in data)
            avg_growth = sum(row.get('growth_rate_yoy', 0) for row in data) / len(data) if data else 0
            
            summary = {
                "query_parameters": {
                    "product_category": product_category,
                    "location": location or "All locations",
                    "time_period": time_period,
                    "metric": metric
                },
                "summary_statistics": {
                    "total_records": len(data),
                    "total_shipments": int(total_shipments),
                    "average_growth_rate_yoy": round(avg_growth, 2)
                },
                "data": data[:limit]
            }
        else:
            summary = {
                "query_parameters": {
                    "product_category": product_category,
                    "location": location or "All locations",
                    "time_period": time_period,
                    "metric": metric
                },
                "summary_statistics": {
                    "total_records": 0,
                    "message": "No data found for the specified criteria"
                },
                "data": []
            }
        
        return json.dumps(summary, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query
        }, indent=2)

