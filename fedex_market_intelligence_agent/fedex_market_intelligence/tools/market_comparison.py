"""Market comparison tool for side-by-side analysis."""

from google.cloud import bigquery
from typing import List, Optional
import json

from fedex_market_intelligence.config import config

PROJECT_ID = config.project_id
DATASET_ID = config.dataset_id


def compare_markets(
    product_category: str,
    markets: List[str],
    time_period: str = "last_12_months",
    metrics: Optional[List[str]] = None
) -> str:
    """
    Compare multiple markets side-by-side.
    
    Args:
        product_category: Product category to compare
        markets: List of markets to compare (cities, metros, states)
        time_period: Time period for comparison
        metrics: List of metrics to compare - defaults to ['volume', 'growth', 'value', 'competition']
    
    Returns:
        JSON string with market comparison results
    """
    
    if metrics is None:
        metrics = ['volume', 'growth', 'value', 'competition']
    
    if not markets or len(markets) < 2:
        return json.dumps({
            "error": "Please provide at least 2 markets to compare"
        }, indent=2)
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Parse time period
    time_filter = ""
    if time_period == "last_6_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 6"
    elif time_period == "last_12_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 12"
    elif time_period == "last_24_months":
        time_filter = "AND DATE_DIFF(DATE('2025-12-31'), PARSE_DATE('%Y-%m', ad.year_month), MONTH) <= 24"
    elif time_period.startswith("q") and "2025" in time_period:
        quarter = time_period[1]
        time_filter = f"AND EXTRACT(YEAR FROM PARSE_DATE('%Y-%m', ad.year_month)) = 2025 AND EXTRACT(QUARTER FROM PARSE_DATE('%Y-%m', ad.year_month)) = {quarter}"
    
    # Build location filters for each market
    market_filters = []
    for market in markets:
        market_lower = market.lower().replace(",", "").strip()
        market_filters.append(f"""(
            LOWER(gm.city) LIKE '%{market_lower}%' OR
            LOWER(gm.metro_area) LIKE '%{market_lower}%' OR
            LOWER(gm.state) LIKE '%{market_lower}%'
        )""")
    
    location_filter = " OR ".join(market_filters)
    
    query = f"""
        WITH market_data AS (
            SELECT 
                CASE
                    {' '.join([f"WHEN LOWER(gm.city) LIKE '%{market.lower().replace(',', '').strip()}%' THEN '{market}'" for market in markets])}
                    {' '.join([f"WHEN LOWER(gm.metro_area) LIKE '%{market.lower().replace(',', '').strip()}%' THEN '{market}'" for market in markets])}
                    {' '.join([f"WHEN LOWER(gm.state) LIKE '%{market.lower().replace(',', '').strip()}%' THEN '{market}'" for market in markets])}
                    ELSE 'Other'
                END as market_name,
                ad.*,
                gm.city,
                gm.state,
                gm.metro_area,
                gm.region,
                ms.market_concentration_index,
                ms.major_brand_volume,
                ms.small_business_volume
            FROM `{PROJECT_ID}.{DATASET_ID}.aggregated_demand` ad
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.geographic_metadata` gm
                ON ad.zip_code = gm.zip_code
            LEFT JOIN `{PROJECT_ID}.{DATASET_ID}.market_share` ms
                ON ad.zip_code = ms.zip_code 
                AND ad.year_month = ms.year_month
                AND ad.product_category = ms.product_category
            WHERE ad.product_category = '{product_category}'
            AND ({location_filter})
            {time_filter}
        )
        SELECT 
            market_name,
            COUNT(DISTINCT zip_code) as unique_zip_codes,
            SUM(total_shipments) as total_shipments,
            SUM(total_value) as total_value,
            AVG(growth_rate_yoy) as avg_growth_rate_yoy,
            AVG(growth_rate_mom) as avg_growth_rate_mom,
            AVG(unique_shippers) as avg_unique_shippers,
            AVG(market_concentration_index) as avg_market_concentration,
            SUM(major_brand_volume) as total_major_brand_volume,
            SUM(small_business_volume) as total_small_business_volume,
            COUNT(DISTINCT year_month) as months_with_data
        FROM market_data
        WHERE market_name != 'Other'
        GROUP BY market_name
        ORDER BY total_shipments DESC
    """
    
    try:
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to list of dicts
        comparison_data = []
        for row in results:
            row_dict = dict(row)
            
            # Round numeric values
            for key in ['total_value', 'avg_growth_rate_yoy', 'avg_growth_rate_mom', 
                       'avg_unique_shippers', 'avg_market_concentration']:
                if key in row_dict and row_dict[key] is not None:
                    row_dict[key] = round(row_dict[key], 2)
            
            # Calculate derived metrics
            total_volume = (row_dict.get('total_major_brand_volume', 0) or 0) + (row_dict.get('total_small_business_volume', 0) or 0)
            if total_volume > 0:
                row_dict['major_brand_share_pct'] = round((row_dict.get('total_major_brand_volume', 0) or 0) / total_volume * 100, 1)
                row_dict['small_business_share_pct'] = round((row_dict.get('total_small_business_volume', 0) or 0) / total_volume * 100, 1)
            
            comparison_data.append(row_dict)
        
        # Generate insights
        insights = []
        if len(comparison_data) >= 2:
            # Volume leader
            volume_leader = max(comparison_data, key=lambda x: x.get('total_shipments', 0))
            insights.append(f"{volume_leader['market_name']} leads in volume with {volume_leader['total_shipments']:,} shipments")
            
            # Growth leader
            growth_leader = max(comparison_data, key=lambda x: x.get('avg_growth_rate_yoy', 0))
            insights.append(f"{growth_leader['market_name']} shows fastest growth at {growth_leader['avg_growth_rate_yoy']:.1f}% YoY")
            
            # Competition analysis
            competition_data = [x for x in comparison_data if x.get('avg_market_concentration') is not None]
            if competition_data:
                least_competitive = min(competition_data, key=lambda x: x.get('avg_market_concentration', 100))
                insights.append(f"{least_competitive['market_name']} has lowest major brand dominance at {least_competitive['avg_market_concentration']:.0f}%")
        
        # Winner in each category
        winners = {}
        if comparison_data:
            winners = {
                "volume": max(comparison_data, key=lambda x: x.get('total_shipments', 0))['market_name'],
                "growth": max(comparison_data, key=lambda x: x.get('avg_growth_rate_yoy', 0))['market_name'],
                "value": max(comparison_data, key=lambda x: x.get('total_value', 0))['market_name'],
            }
            if any(x.get('avg_market_concentration') is not None for x in comparison_data):
                winners["opportunity"] = min([x for x in comparison_data if x.get('avg_market_concentration') is not None], 
                                            key=lambda x: x.get('avg_market_concentration', 100))['market_name']
        
        response = {
            "query_parameters": {
                "product_category": product_category,
                "markets_compared": markets,
                "time_period": time_period
            },
            "summary": {
                "markets_analyzed": len(comparison_data),
                "insights": insights,
                "winners_by_metric": winners
            },
            "comparison_data": comparison_data
        }
        
        return json.dumps(response, indent=2, default=str)
        
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "query": query
        }, indent=2)

