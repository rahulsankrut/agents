"""BigQuery analysis tool for shipment and demand data."""

from google.cloud import bigquery
from typing import Dict
import pandas as pd


class BigQueryAnalysisTool:
    """Query and analyze FedEx shipment data from BigQuery."""
    
    def __init__(self, project_id: str, dataset_id: str = "fedex"):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.client = bigquery.Client(project=project_id)
    
    def _build_table_ref(self, table: str) -> str:
        return f"`{self.project_id}.{self.dataset_id}.{table}`"
    
    def query_shipment_volume_by_location(self, state: str = None, city: str = None, limit: int = 20) -> pd.DataFrame:
        """Query shipment volume by location."""
        where = []
        if state:
            where.append(f"customer_state = '{state.upper()}'")
        if city:
            where.append(f"LOWER(customer_city) = '{city.lower()}'")
        
        where_sql = f"WHERE {' AND '.join(where)}" if where else ""
        
        query = f"""
        SELECT 
            customer_zip_code_prefix as zip_code,
            customer_city as city,
            customer_state as state,
            COUNT(DISTINCT o.order_id) as shipment_count,
            COUNT(DISTINCT o.customer_id) as unique_recipients,
            ROUND(AVG(oi.price), 2) as avg_shipment_value,
            ROUND(SUM(oi.price), 2) as total_value
        FROM {self._build_table_ref('olist_orders_dataset')} o
        JOIN {self._build_table_ref('olist_customers_dataset')} c ON o.customer_id = c.customer_id
        JOIN {self._build_table_ref('olist_order_items_dataset')} oi ON o.order_id = oi.order_id
        {where_sql}
        GROUP BY zip_code, city, state
        ORDER BY shipment_count DESC
        LIMIT {limit}
        """
        return self.client.query(query).to_dataframe()
    
    def analyze_category_demand_by_location(self, category: str, state: str = None, limit: int = 10) -> pd.DataFrame:
        """Analyze demand for specific product category by location."""
        where = [f"LOWER(p.product_category_name) LIKE '%{category.lower()}%'"]
        if state:
            where.append(f"c.customer_state = '{state.upper()}'")
        
        query = f"""
        SELECT 
            c.customer_zip_code_prefix as zip_code,
            c.customer_city as city,
            c.customer_state as state,
            p.product_category_name as category,
            COUNT(DISTINCT o.order_id) as shipment_count,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            ROUND(SUM(oi.price), 2) as total_revenue,
            ROUND(AVG(oi.price), 2) as avg_order_value
        FROM {self._build_table_ref('olist_orders_dataset')} o
        JOIN {self._build_table_ref('olist_customers_dataset')} c ON o.customer_id = c.customer_id
        JOIN {self._build_table_ref('olist_order_items_dataset')} oi ON o.order_id = oi.order_id
        JOIN {self._build_table_ref('olist_products_dataset')} p ON oi.product_id = p.product_id
        WHERE {' AND '.join(where)}
        GROUP BY zip_code, city, state, category
        ORDER BY shipment_count DESC
        LIMIT {limit}
        """
        return self.client.query(query).to_dataframe()
    
    def calculate_growth_trends(self, location_type: str = "city", category: str = None, min_months: int = 6) -> pd.DataFrame:
        """Calculate shipment growth trends over time."""
        location_map = {"city": "c.customer_city", "state": "c.customer_state", "zip": "c.customer_zip_code_prefix"}
        location_field = location_map.get(location_type, "c.customer_city")
        
        category_join = category_where = ""
        if category:
            category_join = f"""
            JOIN {self._build_table_ref('olist_order_items_dataset')} oi ON o.order_id = oi.order_id
            JOIN {self._build_table_ref('olist_products_dataset')} p ON oi.product_id = p.product_id
            """
            category_where = f"AND LOWER(p.product_category_name) LIKE '%{category.lower()}%'"
        
        query = f"""
        WITH monthly_data AS (
            SELECT 
                {location_field} as location,
                c.customer_state as state,
                FORMAT_TIMESTAMP('%Y-%m', o.order_purchase_timestamp) as month,
                COUNT(DISTINCT o.order_id) as shipment_count
            FROM {self._build_table_ref('olist_orders_dataset')} o
            JOIN {self._build_table_ref('olist_customers_dataset')} c ON o.customer_id = c.customer_id
            {category_join}
            WHERE o.order_status = 'delivered' {category_where}
            GROUP BY location, state, month
        ),
        metrics AS (
            SELECT
                location, state,
                COUNT(DISTINCT month) as months_active,
                MIN(month) as first_month,
                MAX(month) as last_month,
                AVG(shipment_count) as avg_monthly
            FROM monthly_data
            GROUP BY location, state
            HAVING months_active >= {min_months}
        )
        SELECT
            md.location, md.state, m.months_active, ROUND(m.avg_monthly, 2) as avg_monthly_shipments,
            ROUND(AVG(CASE WHEN PARSE_DATE('%Y-%m', md.month) <= DATE_ADD(PARSE_DATE('%Y-%m', m.first_month), INTERVAL 3 MONTH) 
                THEN md.shipment_count END), 2) as early_avg,
            ROUND(AVG(CASE WHEN PARSE_DATE('%Y-%m', md.month) >= DATE_SUB(PARSE_DATE('%Y-%m', m.last_month), INTERVAL 3 MONTH) 
                THEN md.shipment_count END), 2) as recent_avg,
            ROUND(((AVG(CASE WHEN PARSE_DATE('%Y-%m', md.month) >= DATE_SUB(PARSE_DATE('%Y-%m', m.last_month), INTERVAL 3 MONTH) 
                THEN md.shipment_count END) - AVG(CASE WHEN PARSE_DATE('%Y-%m', md.month) <= DATE_ADD(PARSE_DATE('%Y-%m', m.first_month), INTERVAL 3 MONTH) 
                THEN md.shipment_count END)) / NULLIF(AVG(CASE WHEN PARSE_DATE('%Y-%m', md.month) <= DATE_ADD(PARSE_DATE('%Y-%m', m.first_month), INTERVAL 3 MONTH) 
                THEN md.shipment_count END), 0)) * 100, 2) as growth_rate_pct
        FROM monthly_data md
        JOIN metrics m ON md.location = m.location AND md.state = m.state
        GROUP BY md.location, md.state, m.months_active, m.avg_monthly
        HAVING early_avg > 0
        ORDER BY growth_rate_pct DESC
        LIMIT 20
        """
        return self.client.query(query).to_dataframe()
    
    def compare_locations(self, location1: Dict, location2: Dict, category: str = None) -> pd.DataFrame:
        """Compare shipment metrics between two locations."""
        conditions = []
        for loc in [location1, location2]:
            cond = []
            if "city" in loc:
                cond.append(f"LOWER(c.customer_city) = '{loc['city'].lower()}'")
            if "state" in loc:
                cond.append(f"c.customer_state = '{loc['state'].upper()}'")
            if cond:
                conditions.append(f"({' AND '.join(cond)})")
        
        category_join = category_where = ""
        if category:
            category_join = f"JOIN {self._build_table_ref('olist_products_dataset')} p ON oi.product_id = p.product_id"
            category_where = f"AND LOWER(p.product_category_name) LIKE '%{category.lower()}%'"
        
        query = f"""
        SELECT 
            c.customer_city as city,
            c.customer_state as state,
            COUNT(DISTINCT o.order_id) as total_shipments,
            COUNT(DISTINCT o.customer_id) as unique_recipients,
            ROUND(AVG(oi.price), 2) as avg_shipment_value,
            ROUND(SUM(oi.price), 2) as total_revenue
        FROM {self._build_table_ref('olist_orders_dataset')} o
        JOIN {self._build_table_ref('olist_customers_dataset')} c ON o.customer_id = c.customer_id
        JOIN {self._build_table_ref('olist_order_items_dataset')} oi ON o.order_id = oi.order_id
        {category_join}
        WHERE ({' OR '.join(conditions)}) AND o.order_status = 'delivered' {category_where}
        GROUP BY city, state
        ORDER BY total_shipments DESC
        """
        return self.client.query(query).to_dataframe()
    
    def identify_demand_gaps(self, category: str, region: Dict, min_demand_threshold: int = 10) -> pd.DataFrame:
        """Identify high-demand areas for new store locations."""
        region_cond = []
        if "city" in region and region["city"]:
            region_cond.append(f"LOWER(c.customer_city) LIKE '%{region['city'].lower()}%'")
        if "state" in region:
            region_cond.append(f"c.customer_state = '{region['state'].upper()}'")
        
        where = " AND ".join(region_cond) if region_cond else "1=1"
        
        query = f"""
        SELECT 
            c.customer_zip_code_prefix as zip_code,
            c.customer_city as city,
            c.customer_state as state,
            COUNT(DISTINCT o.order_id) as shipment_count,
            COUNT(DISTINCT o.customer_id) as unique_customers,
            ROUND(SUM(oi.price), 2) as total_spent,
            ROUND(AVG(oi.price), 2) as avg_order_value,
            ROUND(COUNT(DISTINCT o.order_id) * AVG(oi.price), 2) as demand_score
        FROM {self._build_table_ref('olist_orders_dataset')} o
        JOIN {self._build_table_ref('olist_customers_dataset')} c ON o.customer_id = c.customer_id
        JOIN {self._build_table_ref('olist_order_items_dataset')} oi ON o.order_id = oi.order_id
        JOIN {self._build_table_ref('olist_products_dataset')} p ON oi.product_id = p.product_id
        WHERE {where} AND LOWER(p.product_category_name) LIKE '%{category.lower()}%' AND o.order_status = 'delivered'
        GROUP BY zip_code, city, state
        HAVING shipment_count >= {min_demand_threshold}
        ORDER BY demand_score DESC
        LIMIT 20
        """
        return self.client.query(query).to_dataframe()
    
    def get_available_categories(self) -> list:
        """Get list of all product categories."""
        query = f"""
        SELECT DISTINCT product_category_name as category
        FROM {self._build_table_ref('olist_products_dataset')}
        WHERE product_category_name IS NOT NULL
        ORDER BY category
        """
        df = self.client.query(query).to_dataframe()
        return df['category'].tolist()
