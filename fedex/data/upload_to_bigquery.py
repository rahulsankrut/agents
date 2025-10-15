"""Upload synthetic data to BigQuery for the FedEx Market Intelligence Agent."""

from google.cloud import bigquery
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Configuration from environment variables (no defaults - must be set)
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
DATASET_ID = os.getenv("BIGQUERY_DATASET")
DATA_DIR = Path(__file__).parent / "output"

if not PROJECT_ID or not DATASET_ID:
    print("ERROR: Required environment variables not set")
    print("  - GOOGLE_CLOUD_PROJECT")
    print("  - BIGQUERY_DATASET")
    print("\nPlease set them in your .env file")
    sys.exit(1)


def create_dataset(client):
    """Create the BigQuery dataset if it doesn't exist."""
    dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
    
    try:
        client.get_dataset(dataset_id)
        print(f"Dataset {dataset_id} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_id)
        dataset.location = "US"
        dataset = client.create_dataset(dataset, timeout=30)
        print(f"Created dataset {dataset_id}")


def create_table_schemas():
    """Define schemas for all tables."""
    schemas = {
        "shipment_data": [
            bigquery.SchemaField("shipment_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("product_category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("product_subcategory", "STRING"),
            bigquery.SchemaField("origin_zip_code", "STRING"),
            bigquery.SchemaField("destination_zip_code", "STRING"),
            bigquery.SchemaField("package_count", "INTEGER"),
            bigquery.SchemaField("total_weight_lbs", "FLOAT"),
            bigquery.SchemaField("declared_value", "FLOAT"),
            bigquery.SchemaField("shipper_type", "STRING"),
            bigquery.SchemaField("shipper_name", "STRING"),
        ],
        "aggregated_demand": [
            bigquery.SchemaField("zip_code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("year_month", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("product_category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("total_shipments", "INTEGER"),
            bigquery.SchemaField("total_value", "FLOAT"),
            bigquery.SchemaField("unique_shippers", "INTEGER"),
            bigquery.SchemaField("growth_rate_mom", "FLOAT"),
            bigquery.SchemaField("growth_rate_yoy", "FLOAT"),
        ],
        "market_share": [
            bigquery.SchemaField("zip_code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("year_month", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("product_category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("major_brand_volume", "INTEGER"),
            bigquery.SchemaField("small_business_volume", "INTEGER"),
            bigquery.SchemaField("market_concentration_index", "FLOAT"),
        ],
        "geographic_metadata": [
            bigquery.SchemaField("zip_code", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("city", "STRING"),
            bigquery.SchemaField("state", "STRING"),
            bigquery.SchemaField("metro_area", "STRING"),
            bigquery.SchemaField("region", "STRING"),
            bigquery.SchemaField("lat", "FLOAT"),
            bigquery.SchemaField("lng", "FLOAT"),
        ],
        "category_hierarchy": [
            bigquery.SchemaField("category_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("category_name", "STRING"),
            bigquery.SchemaField("subcategory", "STRING"),
            bigquery.SchemaField("keywords", "STRING"),
        ],
    }
    return schemas


def upload_table(client, table_name, csv_file, schema):
    """Upload a CSV file to BigQuery table."""
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    # Configure load job
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        skip_leading_rows=1,  # Skip header row
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite existing data
        max_bad_records=100,
    )
    
    # Check if file exists
    if not csv_file.exists():
        print(f"ERROR: File {csv_file} not found")
        return False
    
    print(f"\nUploading {table_name}...")
    print(f"  Source: {csv_file}")
    print(f"  Destination: {table_id}")
    
    try:
        with open(csv_file, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file, table_id, job_config=job_config
            )
        
        # Wait for the job to complete
        load_job.result()
        
        # Get table info
        table = client.get_table(table_id)
        print(f"  ✓ Loaded {table.num_rows:,} rows")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False


def create_views(client):
    """Create useful views for common queries."""
    dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
    
    views = {
        "demand_with_geography": f"""
            SELECT 
                ad.*,
                gm.city,
                gm.state,
                gm.metro_area,
                gm.region,
                gm.lat,
                gm.lng
            FROM `{dataset_ref}.aggregated_demand` ad
            LEFT JOIN `{dataset_ref}.geographic_metadata` gm
                ON ad.zip_code = gm.zip_code
        """,
        "market_intelligence_summary": f"""
            SELECT 
                ad.zip_code,
                ad.year_month,
                ad.product_category,
                ch.category_name,
                ad.total_shipments,
                ad.total_value,
                ad.growth_rate_yoy,
                ms.market_concentration_index,
                gm.city,
                gm.state,
                gm.metro_area,
                gm.region
            FROM `{dataset_ref}.aggregated_demand` ad
            LEFT JOIN `{dataset_ref}.market_share` ms
                ON ad.zip_code = ms.zip_code 
                AND ad.year_month = ms.year_month
                AND ad.product_category = ms.product_category
            LEFT JOIN `{dataset_ref}.geographic_metadata` gm
                ON ad.zip_code = gm.zip_code
            LEFT JOIN `{dataset_ref}.category_hierarchy` ch
                ON ad.product_category = ch.category_id
        """
    }
    
    print("\n" + "=" * 60)
    print("Creating views...")
    print("=" * 60)
    
    for view_name, query in views.items():
        view_id = f"{dataset_ref}.{view_name}"
        view = bigquery.Table(view_id)
        view.view_query = query
        
        try:
            client.delete_table(view_id, not_found_ok=True)
            view = client.create_table(view)
            print(f"✓ Created view: {view_name}")
        except Exception as e:
            print(f"✗ Error creating view {view_name}: {str(e)}")


def main():
    """Main execution function."""
    print("=" * 60)
    print("FedEx Market Intelligence - BigQuery Upload")
    print("=" * 60)
    
    # Check if data files exist
    if not DATA_DIR.exists():
        print(f"\nERROR: Data directory not found: {DATA_DIR}")
        print("Please run generate_synthetic_data.py first")
        sys.exit(1)
    
    # Initialize BigQuery client
    print(f"\nProject ID: {PROJECT_ID}")
    print(f"Dataset ID: {DATASET_ID}")
    
    try:
        client = bigquery.Client(project=PROJECT_ID)
        print("✓ Connected to BigQuery")
    except Exception as e:
        print(f"✗ Error connecting to BigQuery: {str(e)}")
        sys.exit(1)
    
    # Create dataset
    print("\n" + "=" * 60)
    print("Creating dataset...")
    print("=" * 60)
    create_dataset(client)
    
    # Get schemas
    schemas = create_table_schemas()
    
    # Upload tables
    print("\n" + "=" * 60)
    print("Uploading tables...")
    print("=" * 60)
    
    tables_to_upload = [
        ("geographic_metadata", "geographic_metadata.csv"),
        ("category_hierarchy", "category_hierarchy.csv"),
        ("shipment_data", "shipment_data.csv"),
        ("aggregated_demand", "aggregated_demand.csv"),
        ("market_share", "market_share.csv"),
    ]
    
    success_count = 0
    for table_name, csv_filename in tables_to_upload:
        csv_file = DATA_DIR / csv_filename
        schema = schemas[table_name]
        if upload_table(client, table_name, csv_file, schema):
            success_count += 1
    
    # Create views
    create_views(client)
    
    # Summary
    print("\n" + "=" * 60)
    print("UPLOAD SUMMARY")
    print("=" * 60)
    print(f"Successfully uploaded: {success_count}/{len(tables_to_upload)} tables")
    
    if success_count == len(tables_to_upload):
        print("\n✓ All data uploaded successfully!")
        print(f"\nYou can now query the data at:")
        print(f"  {PROJECT_ID}.{DATASET_ID}")
    else:
        print("\n⚠ Some tables failed to upload. Check errors above.")
    
    print("=" * 60)


if __name__ == "__main__":
    main()

