# Anderson Agent - Presentation Generation System

## 🎯 Overview
This system automatically generates PowerPoint presentations from Firestore project data using Google Cloud Functions.

## 📁 Current File Structure

### Core Files
- `firestore_operations.py` - Main database operations and CRUD functions
- `schema.py` - Data models for Customer, Project, and ImageData
- `one_click_presentation.py` - **MAIN SCRIPT** - One-click presentation generator
- `update_to_cloud_function_format.py` - Updates database with cloud function format
- `replace_real_data_simple.py` - Populates database with real project data

### Generated Presentations
- `slide_01_Colgate_Liquid_Fabric_Softener_Audit_598_Clubs.pptx`
- `slide_02_Square_Block_Display_Retrofit_Wave_1_99_Clubs.pptx`
- `slide_03_TNT_Parking_Lot_Take_Down_Survey_Utah_Stores_37_St.pptx`
- `slide_04_Haleon_TEST_Tums_Multi-Vendor_Corrugate_SideCap_Aw.pptx`
- `slide_05_Ghirardelli-Lindt_Chocolate_Summer_Grocery_Premium.pptx`
- `slide_06_Haleon_Advil_TABLET_2pk_Vial_Packouts_1981_Stores.pptx`
- `slide_07_Colgate_Total_Toothpaste_ENDCAP_Audit_598_Clubs.pptx`
- `slide_08_TNT_Parking_Lot_Take_Down_Survey_Utah_Clubs_3_Club.pptx`
- `slide_09_Haleon_Parodontax_NEW_Package_Rotation_1966_Stores.pptx`
- `slide_10_Haleon_Advil_Top_Ten_Validate_SCAN_VSCAN_1966_Stor.pptx`
- `slide_11_Colgate-Palmolive_Colgate_TOP_traited_Priority_Ite.pptx`
- `slide_12_UI_Distributors_Game_Signing_3623_Stores.pptx`

### Utility Files
- `add_your_data.py` - Example script for adding custom data
- `bulk_import.py` - Bulk data import example
- `direct_firestore.py` - Direct Firestore operations example
- `example_usage.py` - Usage examples
- `update_eqi_to_yes_no.py` - EQI field migration script

### Archive Directory
- `archive/` - Contains old test files, duplicates, and backup files

## 🚀 Quick Start

### Generate Individual Slides
```bash
python one_click_presentation.py
```

### Update Database with New Data
```bash
python update_to_cloud_function_format.py
```

### Add Custom Project Data
```bash
python add_your_data.py
```

## 📊 Database Structure

### Projects Collection
Each project contains:
- `project_id` - Unique identifier
- `customer_name` - Customer name (Walmart, Target, Sam's Club)
- `customer_logo_url` - GCS URL to customer logo
- `project_title` - Project title
- `project_overview` - Project description with bullet points
- `eqi` - Environmental Quality Index ("Yes" or "No")
- `images` - Array of image objects with URLs and descriptions
- `created_at` - Timestamp
- `updated_at` - Timestamp

## 🔧 Configuration

### Cloud Function
- **URL**: `https://us-central1-agent-space-465923.cloudfunctions.net/ppt-generator`
- **Endpoint**: `/generate`
- **Method**: POST

### Cloud Storage
- **Bucket**: `gs://agent-space-465923-presentations`
- **Project ID**: `agent-space-465923`

## 📋 Current Data
- **Total Projects**: 12
- **Walmart**: 4 projects
- **Target**: 4 projects  
- **Sam's Club**: 4 projects

## 🎨 Presentation Features
- Professional slide layouts
- Customer logos
- Project images with descriptions
- EQI indicators
- Bullet-point project overviews
- Consistent formatting

## 📝 Notes
- Individual slides preserve original formatting perfectly
- For combined presentations, manually copy slides in PowerPoint to maintain formatting
- All presentations are saved both locally and to Cloud Storage
- System is fully automated and ready for production use

## 🔄 Maintenance
- Run `one_click_presentation.py` to regenerate presentations when data changes
- Use `update_to_cloud_function_format.py` to update database structure
- Check `archive/` directory for old files before deleting
