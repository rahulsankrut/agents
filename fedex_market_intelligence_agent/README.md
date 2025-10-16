# FedEx Market Intelligence Agent

AI-powered market intelligence system that analyzes FedEx shipping data to identify business opportunities and optimal site selection locations. This agent helps businesses make data-driven decisions about where to open new stores, facilities, or services by analyzing real shipping patterns and demand trends.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Cloud account with BigQuery access
- gcloud CLI installed and authenticated
- Google Maps API key (optional, for map visualizations)

### 1. Installation

```bash
# Clone or download this folder
cd fedex_market_intelligence_agent

# Install dependencies
pip install -r requirements.txt

# Or using poetry (if you prefer)
poetry install
```

### 2. Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your settings
# Required: GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_STORAGE_BUCKET
# Optional: GOOGLE_MAPS_API_KEY (for map visualizations)
```

### 3. Generate and Upload Data

```bash
# Generate synthetic FedEx shipping data
cd data
python generate_synthetic_data.py

# Upload data to BigQuery
python upload_to_bigquery.py
```

### 4. Deploy to Google Cloud

```bash
# Deploy the agent to Vertex AI
python deployment/deploy_with_tracing.py --create \
  --project_id=your-project-id \
  --location=us-central1 \
  --bucket=your-storage-bucket
```

### 5. Test the Agent

```bash
# Run a quick test
python -c "
from fedex_market_intelligence.agent import root_agent
print('✅ Agent loaded successfully!')
print(f'Agent name: {root_agent.name}')
print(f'Available tools: {len(root_agent.tools)}')
"
```

## 📊 Features

### Core Capabilities

- **🔍 Market Intelligence**: Analyze shipping patterns and demand trends across 50+ product categories
- **📍 Site Selection**: Identify optimal locations for new ventures using data-driven insights
- **📈 Demand Forecasting**: Predict future market conditions (3-12 months ahead)
- **🎯 Opportunity Finding**: Discover underserved markets and low-competition zones
- **🗺️ Geographic Analysis**: Compare markets across regions, cities, and ZIP codes
- **📊 Competitive Intelligence**: Analyze market concentration and competition levels
- **🎨 Visual Mapping**: Generate interactive maps showing demand zones and opportunities

### Data Coverage

- **Time Range**: 36 months of historical data (2023-2025)
- **Geographic Coverage**: 5,000+ ZIP codes across major US metro areas
- **Product Categories**: 50+ categories including:
  - Pet Supplies, Consumer Electronics, Coffee Products
  - Skincare, Home Fitness, Winter Outerwear
  - Books, Toys, Home Decor, Kitchen Appliances
  - Baby Products, Vitamins, Outdoor Gear, and more
- **Market Intelligence**: Market share, competitive landscape, growth rates

## 🛠️ Available Tools

The agent includes 7 powerful analysis tools:

1. **`query_shipment_trends`** - Analyze time series trends, growth rates, seasonality
2. **`analyze_geographic_demand`** - Compare demand across locations (ZIP, city, metro, state, region)
3. **`find_market_opportunities`** - Identify gaps, underserved areas, low competition zones
4. **`compare_markets`** - Side-by-side comparison of multiple markets
5. **`forecast_demand`** - Predict future demand (3-12 months ahead)
6. **`get_demographics`** - Enrich analysis with Census data (population, income, age)
7. **`generate_map_visualization`** - Create visual maps of demand zones

## 💡 Example Use Cases

### 1. Site Selection for Retail

**Query**: "Where should I open a pet supply store in Phoenix?"

**Agent Response**: 
- Analyzes pet supply demand across Phoenix metro area
- Identifies top ZIP codes with high demand and growth
- Compares competition levels and market saturation
- Provides demographic data (income, population)
- Generates map visualization of opportunities

### 2. Market Expansion Analysis

**Query**: "What's the growth potential for home fitness equipment in Austin?"

**Agent Response**:
- Shows growth trends and seasonality patterns
- Compares Austin to other major cities
- Forecasts future demand (next 6-12 months)
- Identifies underserved areas within the metro

### 3. Competitive Intelligence

**Query**: "Which cities have the lowest competition for coffee products?"

**Agent Response**:
- Analyzes market concentration across metro areas
- Identifies cities with high demand but low competition
- Shows market share distribution
- Provides opportunity scores for each location

## 🏗️ Architecture

### Project Structure

```
fedex_market_intelligence_agent/
├── fedex_market_intelligence/          # Core agent package
│   ├── __init__.py
│   ├── agent.py                       # Main agent definition
│   ├── config.py                      # Configuration management
│   ├── prompt.py                      # System prompts
│   └── tools/                         # Analysis tools
│       ├── __init__.py
│       ├── trend_analysis.py          # Time series analysis
│       ├── geographic_analysis.py     # Location-based analysis
│       ├── market_opportunities.py    # Opportunity identification
│       ├── market_comparison.py       # Multi-market comparison
│       ├── forecasting.py             # Demand forecasting
│       ├── demographics.py            # Census data integration
│       └── visualization.py           # Map generation
├── data/                              # Data generation and upload
│   ├── generate_synthetic_data.py     # Generate synthetic FedEx data
│   ├── upload_to_bigquery.py          # Upload data to BigQuery
│   ├── metro_areas.json               # Metro area definitions
│   └── product_categories.json        # Product category definitions
├── deployment/
│   └── deploy_with_tracing.py         # Cloud deployment script
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Poetry configuration
├── .env.template                      # Environment template
└── README.md                          # This file
```

### Tech Stack

- **Google Agent Development Kit (ADK)** - Agent framework
- **Vertex AI** - Cloud AI platform
- **Gemini 2.5 Pro** - Large language model
- **BigQuery** - Data warehouse (requires dataset setup)
- **Google Maps API** - Map visualizations (optional)
- **Census API** - Demographic data (public, no auth required)

## 📋 Setup Guide

Follow the step-by-step instructions below to get started.

### Quick Setup Checklist

- [ ] Install Python 3.11+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Set up Google Cloud project
- [ ] Configure `.env` file
- [ ] Generate data: `cd data && python generate_synthetic_data.py`
- [ ] Upload data: `python upload_to_bigquery.py`
- [ ] Deploy agent: `python deployment/deploy_with_tracing.py --create`
- [ ] Test agent functionality

### Data Generation

This package includes **complete data generation capabilities**:

1. **Synthetic Data Generation**: Creates realistic FedEx shipping data with:
   - 1M+ shipment transactions across 36 months
   - 50+ product categories with realistic demand patterns
   - 5,000+ ZIP codes across major US metro areas
   - Market share and competitive landscape data
   - Geographic and demographic information

2. **BigQuery Upload**: Automatically creates dataset and uploads data:
   - Creates required BigQuery tables with proper schema
   - Uploads all generated data with proper formatting
   - Sets up indexes and partitions for optimal performance

3. **Configuration Files**: Includes metro areas and product categories:
   - `metro_areas.json` - 20+ major US metro areas with ZIP codes
   - `product_categories.json` - 50+ product categories with subcategories

## 🎯 Demo Queries

Try these sample queries with the agent:

```bash
# Basic market analysis
"What are the top 5 cities for consumer electronics shipments?"

# Site selection
"Where should I open a coffee shop in Nashville? Show me opportunities on a map."

# Trend analysis
"What's the growth rate for home fitness equipment in Chicago?"

# Competitive analysis
"Which ZIP codes in Austin have the lowest competition for pet supplies?"

# Forecasting
"Predict demand for winter outerwear in Denver for the next 6 months"
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_CLOUD_PROJECT` | Your GCP project ID | Yes | - |
| `GOOGLE_CLOUD_LOCATION` | GCP region | Yes | us-central1 |
| `GOOGLE_CLOUD_STORAGE_BUCKET` | GCS bucket for staging | Yes | - |
| `BIGQUERY_DATASET` | BigQuery dataset name | Yes | fedex_market_intelligence |
| `ROOT_AGENT_MODEL` | AI model to use | No | gemini-2.5-pro |
| `MODEL_TEMPERATURE` | Model creativity level | No | 0.1 |
| `GOOGLE_MAPS_API_KEY` | For map visualizations | No | - |
| `LOG_LEVEL` | Logging level | No | INFO |

### Product Categories

The agent supports 50+ product categories. Use the category_id format (lowercase with underscores):

- `pet_supplies` - Pet Supplies: dog food, cat toys, medications
- `consumer_electronics` - Consumer Electronics: smartphones, laptops, smart home
- `coffee_products` - Coffee Products: beans, pods, equipment
- `skincare` - Skincare: K-beauty, serums, natural products
- `home_fitness` - Home Fitness Equipment: dumbbells, treadmills, yoga mats
- `winter_outerwear` - Winter Outerwear: jackets, parkas, coats
- `books` - Books: fiction, non-fiction, textbooks
- `toys` - Toys & Games: action figures, board games
- `home_decor` - Home Decor: wall art, candles, pillows
- `kitchen_appliances` - Kitchen Appliances: blenders, air fryers
- `baby_products` - Baby Products: diapers, formula, strollers
- `vitamins_supplements` - Vitamins & Supplements: protein, multivitamins
- `outdoor_gear` - Outdoor Gear: camping equipment, hiking boots
- `beauty_cosmetics` - Beauty & Cosmetics: makeup, lipstick
- `jewelry` - Jewelry & Accessories: necklaces, watches
- `sporting_goods` - Sporting Goods: golf, tennis, basketball
- `craft_supplies` - Craft Supplies: yarn, fabric, paint
- `automotive_parts` - Automotive Parts: oil filters, brake pads
- `garden_supplies` - Garden Supplies: seeds, fertilizers, tools
- `office_supplies` - Office Supplies: paper, pens, notebooks

## 🚀 Deployment

### Local Development

```bash
# Run agent locally for testing
python -c "
from fedex_market_intelligence.agent import root_agent
print('Agent ready for local testing')
"
```

### Cloud Deployment

```bash
# Deploy to Vertex AI with tracing
python deployment/deploy_with_tracing.py --create \
  --project_id=your-project-id \
  --location=us-central1 \
  --bucket=your-storage-bucket

# List deployed agents
python deployment/deploy_with_tracing.py --list \
  --project_id=your-project-id \
  --location=us-central1

# Delete an agent
python deployment/deploy_with_tracing.py --delete \
  --project_id=your-project-id \
  --location=us-central1 \
  --resource_id=your-agent-resource-id
```

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup instructions
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Architecture and implementation details
- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - Demo scenarios and example queries
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview and features

## 🧪 Testing

```bash
# Test agent initialization
python -c "from fedex_market_intelligence.agent import root_agent; print('✅ OK')"

# Test configuration
python -c "from fedex_market_intelligence.config import config; print(f'Project: {config.project_id}')"

# Test tools import
python -c "from fedex_market_intelligence.tools import query_shipment_trends; print('✅ Tools OK')"

# Test data generation
cd data
python generate_synthetic_data.py --help

# Test BigQuery upload
python upload_to_bigquery.py --help
```

## 🔍 Troubleshooting

### Common Issues

1. **"No module named 'google.adk'"**
   ```bash
   pip install --upgrade google-adk
   ```

2. **"Permission denied" on BigQuery**
   ```bash
   gcloud auth application-default login
   ```

3. **"Dataset not found"**
   - Ensure your BigQuery dataset exists
   - Check the dataset name in your `.env` file
   - Verify you have access to the dataset

4. **"No data found for query"**
   - Check that your BigQuery tables are populated
   - Verify product category names (use underscore format)
   - Ensure ZIP codes exist in your data

### Getting Help

1. Check the documentation files in this folder
2. Verify your environment configuration
3. Test with simple queries first
4. Check Google Cloud Console for BigQuery dataset status

## 📄 License

This project is licensed under the Apache License 2.0. See the original project for full license details.

## 🤝 Contributing

This is a shared version of the FedEx Market Intelligence Agent. For the full project with data generation capabilities, please refer to the original repository.

---

**Setup Time**: ~15-20 minutes  
**Dependencies**: Google Cloud account, BigQuery dataset with shipping data  
**Use Case**: Market intelligence, site selection, demand forecasting, competitive analysis

## 🎯 Next Steps

1. **Set up your environment** using the setup guide
2. **Generate synthetic data** using the included scripts
3. **Upload data to BigQuery** automatically
4. **Deploy the agent** to Vertex AI
5. **Try the demo queries** to understand capabilities
6. **Customize for your use case** by modifying categories or adding new tools

## 📦 What's Included

This complete package includes:

- ✅ **Full Agent Code** - All 7 analysis tools and core logic
- ✅ **Data Generation** - Scripts to create realistic FedEx shipping data
- ✅ **BigQuery Upload** - Automated data upload and table creation
- ✅ **Configuration Files** - Metro areas and product categories
- ✅ **Deployment Scripts** - Cloud deployment with tracing
- ✅ **Complete Documentation** - Setup guides, technical docs, demo scripts
- ✅ **Environment Templates** - Ready-to-configure .env template

**Total Setup Time**: ~30 minutes including data generation  
**Data Size**: ~1GB of synthetic shipping data in BigQuery  
**Ready to Use**: Complete end-to-end market intelligence system

For questions or support, refer to the comprehensive documentation files included in this package.
