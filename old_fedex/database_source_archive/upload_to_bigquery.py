"""
Script to upload CSV files from source-files folder to BigQuery tables.
Each CSV file will be uploaded to a separate table in the 'fedex' dataset.
"""

import os
from google.cloud import bigquery
from pathlib import Path

def upload_csv_to_bigquery(project_id, dataset_id="fedex", csv_directory="source-files"):
    """
    Upload all CSV files from the specified directory to BigQuery.
    
    Args:
        project_id (str): GCP project ID
        dataset_id (str): BigQuery dataset name (default: 'fedex')
        csv_directory (str): Directory containing CSV files (default: 'source-files')
    """
    # Initialize BigQuery client
    client = bigquery.Client(project=project_id)
    
    # Get the current directory
    current_dir = Path(__file__).parent
    csv_path = current_dir / csv_directory
    
    if not csv_path.exists():
        print(f"Error: Directory {csv_path} does not exist")
        return
    
    # Get all CSV files
    csv_files = list(csv_path.glob("*.csv"))
    
    if not csv_files:
        print(f"No CSV files found in {csv_path}")
        return
    
    print(f"Found {len(csv_files)} CSV files to upload\n")
    
    # Process each CSV file
    for csv_file in csv_files:
        # Create table name from filename (remove .csv extension)
        table_name = csv_file.stem
        
        # Full table ID
        table_id = f"{project_id}.{dataset_id}.{table_name}"
        
        print(f"Processing: {csv_file.name}")
        print(f"  → Creating table: {table_id}")
        
        # Configure the load job
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,  # Skip header row
            autodetect=True,  # Auto-detect schema
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite if exists
        )
        
        # Load the CSV file
        with open(csv_file, "rb") as source_file:
            try:
                load_job = client.load_table_from_file(
                    source_file,
                    table_id,
                    job_config=job_config
                )
                
                # Wait for the job to complete
                load_job.result()
                
                # Get table info
                table = client.get_table(table_id)
                print(f"  ✓ Successfully loaded {table.num_rows:,} rows")
                print(f"  ✓ Schema: {len(table.schema)} columns\n")
                
            except Exception as e:
                print(f"  ✗ Error loading {csv_file.name}: {str(e)}\n")
                continue
    
    print("=" * 60)
    print("Upload complete!")
    print(f"\nTo view your tables, visit:")
    print(f"https://console.cloud.google.com/bigquery?project={project_id}&d={dataset_id}")


if __name__ == "__main__":
    import sys
    
    # Get project ID from command line argument or environment variable
    if len(sys.argv) > 1:
        project_id = sys.argv[1]
    else:
        project_id = os.environ.get("GCP_PROJECT_ID")
    
    if not project_id:
        print("Error: Please provide GCP project ID")
        print("\nUsage:")
        print("  python upload_to_bigquery.py YOUR_PROJECT_ID")
        print("\nOr set environment variable:")
        print("  export GCP_PROJECT_ID=YOUR_PROJECT_ID")
        print("  python upload_to_bigquery.py")
        sys.exit(1)
    
    print("=" * 60)
    print("BigQuery CSV Uploader")
    print("=" * 60)
    print(f"Project ID: {project_id}")
    print(f"Dataset: fedex")
    print("=" * 60)
    print()
    
    upload_csv_to_bigquery(project_id)

