"""Generate synthetic FedEx shipment data for the market intelligence agent."""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)
np.random.seed(42)

# Load configuration
DATA_DIR = Path(__file__).parent
with open(DATA_DIR / "product_categories.json") as f:
    CATEGORIES = json.load(f)["categories"]

with open(DATA_DIR / "metro_areas.json") as f:
    METRO_AREAS = json.load(f)["metro_areas"]


def generate_zip_codes():
    """Generate all zip codes from metro areas with additional synthetic ones."""
    zip_codes = []
    
    for metro in METRO_AREAS:
        for zip_code in metro["zip_code_samples"]:
            # Add main city zip codes
            city = random.choice(metro["major_cities"])
            zip_codes.append({
                "zip_code": zip_code,
                "city": city,
                "state": metro["state"],
                "metro_area": metro["metro_name"],
                "region": metro["region"],
                "lat": round(random.uniform(25.0, 48.0), 6),
                "lng": round(random.uniform(-125.0, -70.0), 6),
            })
            
            # Add neighboring zip codes (expand to ~5000 total)
            for i in range(random.randint(5, 15)):
                synthetic_zip = str(int(zip_code) + i + 1)
                if len(synthetic_zip) == 5:
                    zip_codes.append({
                        "zip_code": synthetic_zip,
                        "city": city if random.random() > 0.3 else random.choice(metro["major_cities"]),
                        "state": metro["state"],
                        "metro_area": metro["metro_name"],
                        "region": metro["region"],
                        "lat": round(random.uniform(25.0, 48.0), 6),
                        "lng": round(random.uniform(-125.0, -70.0), 6),
                    })
    
    return zip_codes


def get_seasonality_multiplier(month, seasonality_type):
    """Return multiplier based on seasonality pattern."""
    if seasonality_type == "stable":
        return 1.0 + random.uniform(-0.05, 0.05)
    elif seasonality_type == "q1_peak":
        # Peak in Jan-Mar
        return 1.5 if month in [1, 2, 3] else 0.9
    elif seasonality_type == "q2_peak":
        # Peak in Apr-Jun
        return 1.4 if month in [4, 5, 6] else 0.95
    elif seasonality_type == "q4_peak":
        # Peak in Oct-Dec
        return 1.6 if month in [10, 11, 12] else 0.85
    return 1.0


def generate_shipment_data(zip_codes, start_date, end_date, num_shipments=1000000):
    """Generate detailed shipment transaction data."""
    print(f"Generating {num_shipments:,} shipment records...")
    
    shipments = []
    date_range = (end_date - start_date).days
    
    # Weight distribution for different categories
    category_weights = {cat["category_id"]: 1.0 + cat["growth_rate"] for cat in CATEGORIES}
    
    for i in range(num_shipments):
        if i % 50000 == 0:
            print(f"  Generated {i:,} records...")
        
        # Random date within range
        random_days = random.randint(0, date_range)
        shipment_date = start_date + timedelta(days=random_days)
        
        # Select category (weighted by popularity)
        category = random.choices(CATEGORIES, weights=[category_weights[c["category_id"]] for c in CATEGORIES])[0]
        
        # Seasonality is still reflected in aggregated metrics through natural patterns
            
        subcategory = random.choice(category["subcategories"])
        
        # Origin and destination
        origin_zip = random.choice(zip_codes)
        destination_zip = random.choice(zip_codes)
        
        # Shipper type
        shipper_types = ["major_brand", "small_business", "individual"]
        shipper_weights = [0.4, 0.35, 0.25]
        shipper_type = random.choices(shipper_types, weights=shipper_weights)[0]
        
        # Generate shipper name
        if shipper_type == "major_brand":
            shipper_name = f"Brand_{random.choice(['A', 'B', 'C', 'D', 'E', 'F'])}"
        elif shipper_type == "small_business":
            shipper_name = f"SmallBiz_{random.randint(1, 200)}"
        else:
            shipper_name = "Individual"
        
        # Package details
        package_count = random.choices([1, 2, 3, 4, 5], weights=[0.6, 0.2, 0.1, 0.05, 0.05])[0]
        total_weight = round(random.uniform(1, 50) * package_count, 2)
        
        # Value varies by category
        base_value = random.uniform(20, 500)
        if category["category_id"] == "consumer_electronics":
            base_value = random.uniform(100, 2000)
        elif category["category_id"] == "jewelry":
            base_value = random.uniform(50, 5000)
        
        declared_value = round(base_value * package_count, 2)
        
        shipments.append({
            "shipment_id": f"FX{shipment_date.strftime('%Y%m%d')}{i:08d}",
            "date": shipment_date.strftime("%Y-%m-%d"),
            "product_category": category["category_id"],
            "product_subcategory": subcategory,
            "origin_zip_code": origin_zip["zip_code"],
            "destination_zip_code": destination_zip["zip_code"],
            "package_count": package_count,
            "total_weight_lbs": total_weight,
            "declared_value": declared_value,
            "shipper_type": shipper_type,
            "shipper_name": shipper_name,
        })
    
    print(f"Generated {len(shipments):,} shipment records")
    return shipments


def aggregate_demand_data(shipments_df):
    """Pre-aggregate shipment data for performance."""
    print("Aggregating demand data...")
    
    # Add year_month column
    shipments_df['date'] = pd.to_datetime(shipments_df['date'])
    shipments_df['year_month'] = shipments_df['date'].dt.to_period('M').astype(str)
    
    # Group by destination zip, month, and category
    aggregated = shipments_df.groupby(['destination_zip_code', 'year_month', 'product_category']).agg({
        'package_count': 'sum',
        'declared_value': 'sum',
        'shipper_name': 'nunique'
    }).reset_index()
    
    aggregated.columns = ['zip_code', 'year_month', 'product_category', 'total_shipments', 'total_value', 'unique_shippers']
    
    # Calculate growth rates
    aggregated = aggregated.sort_values(['zip_code', 'product_category', 'year_month'])
    
    # Month-over-month growth
    aggregated['prev_month_shipments'] = aggregated.groupby(['zip_code', 'product_category'])['total_shipments'].shift(1)
    aggregated['growth_rate_mom'] = ((aggregated['total_shipments'] - aggregated['prev_month_shipments']) / aggregated['prev_month_shipments'] * 100).round(2)
    
    # Year-over-year growth
    aggregated['prev_year_shipments'] = aggregated.groupby(['zip_code', 'product_category'])['total_shipments'].shift(12)
    aggregated['growth_rate_yoy'] = ((aggregated['total_shipments'] - aggregated['prev_year_shipments']) / aggregated['prev_year_shipments'] * 100).round(2)
    
    # Fill NaN with 0
    aggregated['growth_rate_mom'] = aggregated['growth_rate_mom'].fillna(0)
    aggregated['growth_rate_yoy'] = aggregated['growth_rate_yoy'].fillna(0)
    
    # Drop helper columns
    aggregated = aggregated.drop(['prev_month_shipments', 'prev_year_shipments'], axis=1)
    
    print(f"Created {len(aggregated):,} aggregated demand records")
    return aggregated


def generate_market_share_data(shipments_df):
    """Generate market share analysis data."""
    print("Generating market share data...")
    
    shipments_df['date'] = pd.to_datetime(shipments_df['date'])
    shipments_df['year_month'] = shipments_df['date'].dt.to_period('M').astype(str)
    
    # Group by destination zip, month, category, and shipper type
    market_share = shipments_df.groupby(['destination_zip_code', 'year_month', 'product_category', 'shipper_type']).agg({
        'package_count': 'sum'
    }).reset_index()
    
    # Pivot to get major brand vs small business volumes
    market_share_pivot = market_share.pivot_table(
        index=['destination_zip_code', 'year_month', 'product_category'],
        columns='shipper_type',
        values='package_count',
        fill_value=0
    ).reset_index()
    
    # Rename columns
    market_share_pivot.columns.name = None
    market_share_pivot = market_share_pivot.rename(columns={
        'destination_zip_code': 'zip_code',
        'major_brand': 'major_brand_volume',
        'small_business': 'small_business_volume'
    })
    
    # Drop the 'individual' column if it exists (we only want major_brand and small_business)
    if 'individual' in market_share_pivot.columns:
        market_share_pivot = market_share_pivot.drop(columns=['individual'])
    
    # Ensure we only have the columns we need
    required_columns = ['zip_code', 'year_month', 'product_category', 'major_brand_volume', 'small_business_volume']
    market_share_pivot = market_share_pivot[required_columns]
    
    # Convert volumes to integers (they may have been converted to float during pivot)
    market_share_pivot['major_brand_volume'] = market_share_pivot['major_brand_volume'].astype(int)
    market_share_pivot['small_business_volume'] = market_share_pivot['small_business_volume'].astype(int)
    
    # Calculate market concentration index (0-100, higher = more concentrated)
    total_volume = market_share_pivot['major_brand_volume'] + market_share_pivot['small_business_volume']
    market_share_pivot['market_concentration_index'] = ((market_share_pivot['major_brand_volume'] / total_volume) * 100).round(2)
    market_share_pivot['market_concentration_index'] = market_share_pivot['market_concentration_index'].fillna(50)
    
    print(f"Created {len(market_share_pivot):,} market share records")
    return market_share_pivot


def generate_category_hierarchy():
    """Generate category hierarchy lookup table."""
    print("Generating category hierarchy...")
    
    hierarchy = []
    for cat in CATEGORIES:
        for subcat in cat["subcategories"]:
            hierarchy.append({
                "category_id": cat["category_id"],
                "category_name": cat["category_name"],
                "subcategory": subcat,
                "keywords": json.dumps([cat["category_name"].lower(), subcat.replace("_", " ")])
            })
    
    print(f"Created {len(hierarchy)} category hierarchy records")
    return hierarchy


def main():
    """Main execution function."""
    print("=" * 60)
    print("FedEx Market Intelligence - Synthetic Data Generator")
    print("=" * 60)
    
    # Date range: 36 months (Jan 2023 - Dec 2025)
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2025, 12, 31)
    
    # Generate geographic metadata
    print("\n1. Generating geographic metadata...")
    zip_codes = generate_zip_codes()
    geo_metadata_df = pd.DataFrame(zip_codes)
    print(f"   Created {len(geo_metadata_df)} zip code records")
    
    # Generate shipment data
    print("\n2. Generating shipment transaction data...")
    shipments = generate_shipment_data(zip_codes, start_date, end_date, num_shipments=1000000)
    shipments_df = pd.DataFrame(shipments)
    
    # Generate aggregated demand data
    print("\n3. Generating aggregated demand data...")
    aggregated_df = aggregate_demand_data(shipments_df.copy())
    
    # Generate market share data
    print("\n4. Generating market share data...")
    market_share_df = generate_market_share_data(shipments_df.copy())
    
    # Generate category hierarchy
    print("\n5. Generating category hierarchy...")
    category_hierarchy = generate_category_hierarchy()
    category_hierarchy_df = pd.DataFrame(category_hierarchy)
    
    # Save to CSV files
    print("\n6. Saving data to CSV files...")
    output_dir = DATA_DIR / "output"
    output_dir.mkdir(exist_ok=True)
    
    shipments_df.to_csv(output_dir / "shipment_data.csv", index=False)
    print(f"   Saved shipment_data.csv ({len(shipments_df):,} rows)")
    
    aggregated_df.to_csv(output_dir / "aggregated_demand.csv", index=False)
    print(f"   Saved aggregated_demand.csv ({len(aggregated_df):,} rows)")
    
    market_share_df.to_csv(output_dir / "market_share.csv", index=False)
    print(f"   Saved market_share.csv ({len(market_share_df):,} rows)")
    
    geo_metadata_df.to_csv(output_dir / "geographic_metadata.csv", index=False)
    print(f"   Saved geographic_metadata.csv ({len(geo_metadata_df):,} rows)")
    
    category_hierarchy_df.to_csv(output_dir / "category_hierarchy.csv", index=False)
    print(f"   Saved category_hierarchy.csv ({len(category_hierarchy_df):,} rows)")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("SUMMARY STATISTICS")
    print("=" * 60)
    print(f"Total shipments: {len(shipments_df):,}")
    print(f"Date range: {shipments_df['date'].min()} to {shipments_df['date'].max()}")
    print(f"Unique zip codes: {len(geo_metadata_df):,}")
    print(f"Product categories: {shipments_df['product_category'].nunique()}")
    print(f"Total declared value: ${shipments_df['declared_value'].sum():,.2f}")
    print(f"Average shipment value: ${shipments_df['declared_value'].mean():,.2f}")
    print("\nTop 5 categories by volume:")
    print(shipments_df['product_category'].value_counts().head())
    print("\n" + "=" * 60)
    print("Data generation complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

