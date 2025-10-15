# FedEx Market Intelligence Agent

An AI agent that analyzes FedEx shipping data to identify business opportunities and optimal site selection locations. Built with Google Agent Development Kit (ADK).

## Overview

This agent helps businesses make data-driven decisions by analyzing shipping patterns, demand trends, and market dynamics. FedEx's shipping data serves as a leading indicator of consumer demand, revealing insights that aren't visible through traditional market research.

### Key Capabilities

- **Site Selection**: Identify optimal locations for new stores, facilities, or services
- **Market Intelligence**: Understand demand patterns and growth trends
- **Competitive Analysis**: Find gaps and underserved markets
- **Growth Opportunities**: Spot emerging trends and high-growth areas
- **Demand Forecasting**: Predict future market conditions (3-12 months)
- **Geographic Analysis**: Compare markets across ZIP codes, cities, metros, states, and regions

## Data Sources

1. **Synthetic FedEx Shipping Data** (BigQuery):
   - 1M+ shipment records over 36 months (Jan 2023 - Dec 2025)
   - 50+ product categories with subcategories
   - 5,000+ ZIP codes across major US metro areas
   - Market share and competitive landscape data

2. **US Census API** (Real-time):
   - Population demographics
   - Median household income
   - Age distribution
   - Employment statistics

3. **Google Maps API** (Real-time):
   - Geographic visualization
   - Location mapping
   - Distance calculations

## Architecture

### Agent Components

- **Main Agent**: `fedex_market_intelligence_agent` (Gemini 2.0 Flash)
- **7 Specialized Tools**:
  1. `query_shipment_trends` - Time series analysis
  2. `analyze_geographic_demand` - Location-based insights
  3. `find_market_opportunities` - Gap analysis
  4. `compare_markets` - Side-by-side comparison
  5. `forecast_demand` - Demand forecasting
  6. `get_demographics` - Census data integration
  7. `generate_map_visualization` - Map generation

### Data Layer

BigQuery dataset: `agent-space-465923.fedex_market_intelligence`

**Tables**:
- `shipment_data` - Core transactional data (~1M rows)
- `aggregated_demand` - Pre-aggregated metrics for performance
- `market_share` - Competitive landscape data
- `geographic_metadata` - Location mapping
- `category_hierarchy` - Product taxonomy

## Setup Instructions

### Prerequisites

- Python 3.11+
- Google Cloud Project (agent-space-465923)
- Google Cloud credentials configured
- BigQuery API enabled
- (Optional) Google Maps API key for visualizations

### Installation

1. **Clone the repository**:
```bash
cd /Users/rahulkasanagottu/Desktop/agents/fedex
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
# OR using poetry
poetry install
```

3. **Authenticate with Google Cloud**:
```bash
gcloud auth application-default login
gcloud config set project agent-space-465923
```

### Data Generation and Upload

4. **Generate synthetic data**:
```bash
cd data
python generate_synthetic_data.py
```

This will create:
- ~1M shipment records
- 5,000+ ZIP codes
- 36 months of data
- Output files in `data/output/` directory

5. **Upload to BigQuery**:
```bash
python upload_to_bigquery.py
```

This will:
- Create the `fedex_market_intelligence` dataset
- Create all necessary tables
- Upload the generated data
- Create useful views for common queries

## Usage

### Interactive Demo

Run the agent in interactive mode:

```bash
python demo.py
```

Commands:
- Type your question naturally
- Type `samples` to see example queries
- Type `quit` or `exit` to stop

### Single Query Mode

Run a single query from command line:

```bash
python demo.py "Show me top 5 zip codes in Phoenix with highest pet supply growth"
```

### Sample Queries

1. **Growth Analysis**:
   ```
   Show me the top 5 zip codes in the Phoenix metro area with the highest growth 
   in pet supply shipments over the last 24 months.
   ```

2. **Market Comparison**:
   ```
   Compare the inbound shipment volume of consumer electronics between Austin, TX 
   and Nashville, TN for Q3 2025.
   ```

3. **Opportunity Identification**:
   ```
   Identify three neighborhoods in suburban Chicago that show high demand for 
   premium coffee products but have a low volume of shipments from major coffee brands.
   ```

4. **Trend Analysis**:
   ```
   What is the aggregate demand trend for 'winter outerwear' in the Northeast? 
   Show me the year-over-year growth.
   ```

5. **Forecasting**:
   ```
   Generate a 6-month demand forecast for 'home fitness equipment' shipments 
   in California and Florida.
   ```

6. **Demographic Analysis**:
   ```
   Which niche skincare product categories are seeing the fastest growth in 
   shipments to millennial-heavy zip codes?
   ```

## Product Categories

The agent has data on 20+ major categories:

- Pet Supplies
- Consumer Electronics
- Coffee Products
- Skincare Products
- Home Fitness Equipment
- Winter Outerwear
- Books
- Toys & Games
- Home Decor
- Kitchen Appliances
- Baby Products
- Vitamins & Supplements
- Outdoor Gear
- Beauty & Cosmetics
- Jewelry & Accessories
- Sporting Goods
- Craft Supplies
- Automotive Parts
- Garden Supplies
- Office Supplies

Each category has 5-10 subcategories for detailed analysis.

## Geographic Coverage

Data covers 15+ major metro areas:

**Southwest**: Phoenix, Austin, Dallas, Denver  
**West**: Los Angeles, San Francisco, Seattle, Portland  
**Northeast**: NYC, Boston, Philadelphia  
**Southeast**: Nashville, Atlanta, Miami  
**Midwest**: Chicago

Total: 5,000+ ZIP codes across all regions

## API Reference

### Tool Functions

#### query_shipment_trends
```python
query_shipment_trends(
    product_category: str,
    location: Optional[str] = None,
    time_period: str = "last_12_months",
    metric: str = "volume",
    limit: int = 100
) -> str
```

#### analyze_geographic_demand
```python
analyze_geographic_demand(
    product_category: str,
    geographic_scope: str = "metro",
    demographic_filter: Optional[str] = None,
    time_period: str = "last_12_months",
    top_n: int = 10
) -> str
```

#### find_market_opportunities
```python
find_market_opportunities(
    product_category: str,
    market: str,
    gap_type: str = "low_competition",
    min_demand_threshold: int = 100,
    top_n: int = 10
) -> str
```

#### compare_markets
```python
compare_markets(
    product_category: str,
    markets: List[str],
    time_period: str = "last_12_months",
    metrics: List[str] = None
) -> str
```

#### forecast_demand
```python
forecast_demand(
    product_category: str,
    market: str,
    forecast_months: int = 6
) -> str
```

#### get_demographics
```python
get_demographics(
    zip_codes: List[str],
    metrics: Optional[List[str]] = None
) -> str
```

#### generate_map_visualization
```python
generate_map_visualization(
    locations: List[Dict[str, any]],
    center_location: Optional[str] = None,
    map_type: str = "demand_heatmap",
    zoom_level: int = 10
) -> str
```

## Project Structure

```
fedex/
├── fedex_market_intelligence/
│   ├── __init__.py
│   ├── agent.py              # Main agent definition
│   ├── prompt.py             # System prompts
│   └── tools/
│       ├── __init__.py
│       ├── trend_analysis.py
│       ├── geographic_analysis.py
│       ├── market_opportunities.py
│       ├── market_comparison.py
│       ├── forecasting.py
│       ├── demographics.py
│       └── visualization.py
├── data/
│   ├── product_categories.json
│   ├── metro_areas.json
│   ├── generate_synthetic_data.py
│   ├── upload_to_bigquery.py
│   └── output/              # Generated CSV files
├── demo.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## How It Works

### Data Flow

1. **User Query** → Agent receives natural language question
2. **Tool Selection** → Agent selects appropriate analysis tools
3. **BigQuery Query** → Tools query the data warehouse
4. **Census API** (optional) → Enrich with demographic data
5. **Analysis** → Calculate insights, trends, and recommendations
6. **Response** → Return actionable insights to user

### Example Flow

Query: *"Where should I open a pet supply store in Phoenix?"*

1. Agent calls `analyze_geographic_demand(product_category="pet_supplies", geographic_scope="zip", market="Phoenix")`
2. Agent calls `find_market_opportunities(product_category="pet_supplies", market="Phoenix", gap_type="low_competition")`
3. Agent calls `get_demographics(zip_codes=["85254", "85260", "85262"])`
4. Agent synthesizes data and recommends: "ZIP 85254 (North Scottsdale) shows 1,240 monthly shipments with 187% YoY growth, median income $89k, and only 2 existing competitors..."

## Deployment

Deployment configuration coming soon. Will support:
- ADK Web deployment
- Cloud Run deployment
- API endpoint access

## Troubleshooting

### Common Issues

**BigQuery Authentication Error**:
```bash
gcloud auth application-default login
gcloud config set project agent-space-465923
```

**No Data Found**:
- Ensure data generation script has been run
- Verify BigQuery tables exist: Check in GCP Console
- Check product category name (use underscore format: `pet_supplies` not `Pet Supplies`)

**Census API Errors**:
- Census API is free and doesn't require a key
- ZIP codes must be 5 digits
- Some rural ZIP codes may not have data

**Import Errors**:
- Install all dependencies: `pip install -r requirements.txt`
- Ensure you're in the correct directory

## Performance Notes

- **BigQuery**: Queries typically complete in 1-3 seconds
- **Census API**: Rate limited to ~10 ZIP codes per request
- **Forecasting**: Simple SQL-based, very fast (<1 second)
- **Data Volume**: 1M+ rows, optimized with pre-aggregation

## Future Enhancements

- [ ] Real-time data integration
- [ ] ML-based demand forecasting (BigQuery ML)
- [ ] Interactive map visualizations
- [ ] Export to PDF reports
- [ ] Multi-category analysis
- [ ] Competitive intelligence dashboard
- [ ] Integration with real estate APIs
- [ ] Mobile app deployment

## License

MIT License

## Support

For questions or issues, please contact the development team.

---

**Built with Google Agent Development Kit (ADK)**

