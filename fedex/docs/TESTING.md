# FedEx Market Intelligence Agent - Tests

This directory contains comprehensive tests for the FedEx Market Intelligence Agent.

## Test Files

### 1. `test_config.py`
Tests configuration management:
- Validates all config values are set
- Checks environment variables
- Verifies BigQuery dataset path format

### 2. `test_tools.py`
Tests all 7 analysis tools:
- `query_shipment_trends` - Time series analysis
- `analyze_geographic_demand` - Geographic insights
- `find_market_opportunities` - Opportunity identification
- `compare_markets` - Market comparison
- `forecast_demand` - Demand forecasting
- `get_demographics` - Census API integration
- `generate_map_visualization` - Map generation

### 3. `test_agent.py`
Tests the main agent:
- Agent initialization
- Session creation
- Simple query handling
- Response validation

### 4. `run_all_tests.py`
Master test runner that executes all test suites in order.

## Running Tests

### Run All Tests
```bash
cd /Users/rahulkasanagottu/Desktop/agents/fedex
python tests/run_all_tests.py
```

### Run Individual Test Suites

**Configuration tests only:**
```bash
python tests/test_config.py
```

**Tool tests only:**
```bash
python tests/test_tools.py
```

**Agent tests only:**
```bash
python tests/test_agent.py
```

## Prerequisites

Before running tests, ensure:

1. **BigQuery data is loaded:**
   ```bash
   cd data
   python generate_synthetic_data.py
   python upload_to_bigquery.py
   ```

2. **Environment is configured:**
   - `.env` file exists with correct values
   - Google Cloud authentication is set up
   - Virtual environment is activated

3. **Dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

## Test Output

Tests will output:
- ✓ for passed tests
- ✗ for failed tests
- Detailed error messages for failures
- Summary statistics

### Example Output
```
====================================================================
                 FEDEX MARKET INTELLIGENCE AGENT
                     COMPREHENSIVE TEST SUITE
====================================================================

📋 PHASE 1: Configuration Tests
--------------------------------------------------------------------
✓ project_id: agent-space-465923
✓ location: us-central1
✓ dataset_id: fedex_market_intelligence
...

🔧 PHASE 2: Tool Tests
--------------------------------------------------------------------
✓ query_shipment_trends
✓ analyze_geographic_demand
✓ find_market_opportunities
...

🤖 PHASE 3: Agent Tests
--------------------------------------------------------------------
✓ Agent initialized successfully
✓ Session created successfully
✓ Agent responded successfully

====================================================================
                        FINAL SUMMARY
====================================================================
Configuration       : ✓ PASSED
Tools               : ✓ PASSED
Agent               : ✓ PASSED
====================================================================

🎉 ALL TESTS PASSED!

The FedEx Market Intelligence Agent is ready to use.
Run 'python demo.py' to start the interactive demo.
```

## Troubleshooting

### "No data returned" errors
- Ensure BigQuery tables have data
- Run data generation and upload scripts
- Check that queries return results

### "Connection failed" errors
- Verify Google Cloud authentication
- Check project ID matches in .env
- Ensure BigQuery API is enabled

### "Module not found" errors
- Install missing dependencies: `pip install -r requirements.txt`
- Check Python path is correct
- Activate virtual environment

### Census API errors
- Census API is public and free
- Check ZIP codes are valid 5-digit codes
- Some rural ZIP codes may not have data

## Adding New Tests

To add new tests:

1. Create test function in appropriate file
2. Follow naming convention: `test_<feature_name>`
3. Use assertions for validation
4. Add to test runner if needed
5. Document in this README

## Best Practices

- Run tests before committing changes
- Add tests for new features
- Keep tests independent and isolated
- Use meaningful test names
- Document test purposes

