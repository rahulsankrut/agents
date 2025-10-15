# FedEx Market Intelligence Agent

AI-powered market intelligence system that analyzes FedEx shipping data to identify business opportunities and optimal site selection locations.

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Generate and upload data**:
   ```bash
   cd data
   python generate_synthetic_data.py
   python upload_to_bigquery.py
   ```

4. **Run the agent**:
   ```bash
   adk web
   ```

## Documentation

- **[Full Documentation](docs/README.md)** - Complete guide and features
- **[Setup Guide](docs/SETUP_GUIDE.md)** - Detailed setup instructions
- **[Demo Script](docs/DEMO_SCRIPT.md)** - Comprehensive demo scenarios and use cases
- **[Testing Guide](docs/TESTING.md)** - How to run tests
- **[Project Summary](docs/PROJECT_SUMMARY.md)** - Architecture and design

## Features

- 🔍 **Market Intelligence**: Analyze shipping patterns and demand trends
- 📍 **Site Selection**: Identify optimal locations for new ventures
- 📊 **Demand Forecasting**: Predict future market conditions
- 🎯 **Opportunity Finding**: Discover underserved markets and gaps
- 🗺️ **Geographic Analysis**: Compare markets across regions
- 📈 **Competitive Intelligence**: Analyze market concentration and competition

## Tech Stack

- **Google Agent Development Kit (ADK)**
- **BigQuery** - Data warehouse
- **Gemini 2.5 Pro** - AI model
- **US Census API** - Demographics
- **Google Maps API** - Visualization

## Project Structure

```
fedex/
├── fedex_market_intelligence/  # Main agent package
├── data/                        # Data generation scripts
├── tests/                       # Test suite
├── docs/                        # Documentation
└── requirements.txt             # Dependencies
```

## Support

For detailed information, see the [documentation](docs/).

---

Built with Google Agent Development Kit (ADK)

