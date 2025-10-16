# FedEx Market Intelligence Agent - Quick Setup Guide

## Prerequisites Checklist

- [ ] Python 3.11 or higher installed
- [ ] Google Cloud account with project `agent-space-465923`
- [ ] gcloud CLI installed
- [ ] BigQuery API enabled in your project

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd /Users/rahulkasanagottu/Desktop/agents/fedex
pip install -r requirements.txt
```

**Expected output**: All packages install successfully

### 2. Authenticate with Google Cloud

```bash
# Set default project
gcloud config set project agent-space-465923

# Authenticate
gcloud auth application-default login
```

**Expected output**: Browser opens for authentication, then success message

### 3. Verify BigQuery Access

```bash
# Test BigQuery connection
bq ls
```

**Expected output**: List of datasets (or empty if none exist yet)

### 4. Generate Synthetic Data

```bash
cd data
python generate_synthetic_data.py
```

**Expected output**:
```
==========================================
FedEx Market Intelligence - Synthetic Data Generator
==========================================

1. Generating geographic metadata...
   Created 5000+ zip code records
2. Generating shipment transaction data...
   Generated 1,000,000 records...
...
Data generation complete!
```

**Time**: ~5-10 minutes depending on your machine

### 5. Upload Data to BigQuery

```bash
python upload_to_bigquery.py
```

**Expected output**:
```
==========================================
FedEx Market Intelligence - BigQuery Upload
==========================================

Creating dataset...
Dataset agent-space-465923.fedex_market_intelligence already exists

Uploading tables...
Uploading shipment_data...
  ✓ Loaded 1,000,000 rows
...
✓ All data uploaded successfully!
```

**Time**: ~5-10 minutes for data upload

### 6. Verify Data in BigQuery

```bash
# Query to verify data
bq query --use_legacy_sql=false \
  'SELECT COUNT(*) as total_shipments FROM `agent-space-465923.fedex_market_intelligence.shipment_data`'
```

**Expected output**: Shows ~1,000,000 rows

### 7. Test the Agent

```bash
cd ..
python demo.py
```

**Expected output**:
```
Hello! I'm your FedEx Market Intelligence Agent...

Interactive Mode - Type 'quit' or 'exit' to stop
==========================================

You: 
```

Try a test query:
```
Show me the top 3 zip codes in Austin for pet supplies
```

## Troubleshooting

### Error: "No module named 'google.adk'"

**Solution**:
```bash
pip install --upgrade google-adk
```

### Error: "Permission denied" on BigQuery

**Solution**:
```bash
gcloud auth application-default login
# Make sure you're logged in with an account that has BigQuery access
```

### Error: "Dataset not found"

**Solution**:
Run the upload script again:
```bash
cd data
python upload_to_bigquery.py
```

### Error: "No data found for query"

**Possible causes**:
1. Data not generated yet → Run `generate_synthetic_data.py`
2. Data not uploaded → Run `upload_to_bigquery.py`
3. Wrong product category name → Use underscore format: `pet_supplies` not `Pet Supplies`

### Census API Errors

The Census API is public and doesn't require authentication. If you get errors:
- Check ZIP code format (must be 5 digits)
- Some rural ZIP codes may not have data
- Rate limiting: The tool automatically limits to 10 ZIP codes per request

## Verification Checklist

After setup, verify everything works:

- [ ] Python imports work: `python -c "from fedex_market_intelligence.agent import root_agent; print('OK')"`
- [ ] BigQuery connection works: `bq ls agent-space-465923:fedex_market_intelligence`
- [ ] Data exists: `bq query --use_legacy_sql=false 'SELECT COUNT(*) FROM \`agent-space-465923.fedex_market_intelligence.shipment_data\`'`
- [ ] Agent responds: `python demo.py "What categories do you have data for?"`

## Quick Test Queries

Once setup is complete, try these queries:

1. **Simple query**:
   ```
   What product categories do you have data for?
   ```

2. **Geographic query**:
   ```
   Show me top 5 cities for consumer electronics shipments
   ```

3. **Trend query**:
   ```
   What's the growth rate for pet supplies in Phoenix?
   ```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Try the sample queries in the demo
- Explore the tools and data structure
- Customize product categories or metro areas for your use case

## Support

If you encounter issues not covered here:
1. Check the main README.md
2. Verify all prerequisites are installed
3. Check GCP Console for BigQuery dataset and tables
4. Review error messages carefully

---

**Setup Time**: ~20-30 minutes total
**Data Size**: ~1GB in BigQuery

