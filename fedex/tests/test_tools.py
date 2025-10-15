"""Test all tools in the FedEx Market Intelligence Agent."""

import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fedex_market_intelligence.tools import (
    query_shipment_trends,
    analyze_geographic_demand,
    find_market_opportunities,
    compare_markets,
    forecast_demand,
    get_demographics,
    generate_map_visualization,
)


class TestResults:
    """Track test results."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"✓ {test_name}")
    
    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")
    
    def print_summary(self):
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        
        if self.errors:
            print("\nFailed Tests:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        return self.failed == 0


def test_query_shipment_trends(results):
    """Test the query_shipment_trends tool."""
    test_name = "query_shipment_trends"
    
    try:
        # Test basic query
        response = query_shipment_trends(
            product_category="pet_supplies",
            location="Phoenix",
            time_period="last_12_months",
            metric="volume"
        )
        
        # Parse response
        data = json.loads(response)
        
        # Validate response structure
        assert "query_parameters" in data, "Missing query_parameters"
        assert "summary_statistics" in data, "Missing summary_statistics"
        assert "data" in data, "Missing data"
        
        # Validate data is not empty
        if data["summary_statistics"]["total_records"] == 0:
            results.add_fail(test_name, "No data returned")
        else:
            results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_analyze_geographic_demand(results):
    """Test the analyze_geographic_demand tool."""
    test_name = "analyze_geographic_demand"
    
    try:
        response = analyze_geographic_demand(
            product_category="consumer_electronics",
            geographic_scope="metro",
            time_period="last_12_months",
            top_n=5
        )
        
        data = json.loads(response)
        
        # Check if error or valid response
        if "error" in data:
            results.add_fail(test_name, f"Query error: {data['error'][:100]}")
        else:
            assert "query_parameters" in data, "Missing query_parameters"
            assert "summary" in data, "Missing summary"
            assert "top_locations" in data, "Missing top_locations"
            
            if data["summary"]["total_locations"] == 0:
                results.add_fail(test_name, "No locations returned")
            else:
                results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_find_market_opportunities(results):
    """Test the find_market_opportunities tool."""
    test_name = "find_market_opportunities"
    
    try:
        response = find_market_opportunities(
            product_category="pet_supplies",
            market="Phoenix",
            gap_type="low_competition",
            min_demand_threshold=50,
            top_n=5
        )
        
        data = json.loads(response)
        
        # Check if error or valid response
        if "error" in data:
            results.add_fail(test_name, f"Query error: {data['error'][:100]}")
        else:
            assert "query_parameters" in data, "Missing query_parameters"
            assert "summary" in data, "Missing summary"
            assert "opportunities" in data, "Missing opportunities"
            
            if data["summary"]["opportunities_found"] == 0:
                results.add_fail(test_name, "No opportunities found")
            else:
                results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_compare_markets(results):
    """Test the compare_markets tool."""
    test_name = "compare_markets"
    
    try:
        response = compare_markets(
            product_category="consumer_electronics",
            markets=["Austin", "Nashville"],
            time_period="last_12_months"
        )
        
        data = json.loads(response)
        
        assert "query_parameters" in data, "Missing query_parameters"
        assert "summary" in data, "Missing summary"
        assert "comparison_data" in data, "Missing comparison_data"
        
        if data["summary"]["markets_analyzed"] < 2:
            results.add_fail(test_name, "Less than 2 markets analyzed")
        else:
            results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_forecast_demand(results):
    """Test the forecast_demand tool."""
    test_name = "forecast_demand"
    
    try:
        response = forecast_demand(
            product_category="home_fitness",
            market="California",
            forecast_months=6
        )
        
        data = json.loads(response)
        
        # Check if error or valid response
        if "error" in data:
            # It's okay if there's no data, just check the error is reasonable
            if "No historical data" in data["error"]:
                results.add_pass(f"{test_name} (no data - expected)")
            else:
                results.add_fail(test_name, data["error"])
        else:
            assert "baseline_metrics" in data, "Missing baseline_metrics"
            assert "forecast" in data, "Missing forecast"
            assert len(data["forecast"]) == 6, "Wrong number of forecast months"
            results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_get_demographics(results):
    """Test the get_demographics tool."""
    test_name = "get_demographics"
    
    try:
        # Test with a known NYC zip code
        response = get_demographics(
            zip_codes=["10001", "10002"],
            metrics=["population", "income"]
        )
        
        data = json.loads(response)
        
        assert "query_parameters" in data, "Missing query_parameters"
        assert "summary" in data, "Missing summary"
        assert "demographics" in data, "Missing demographics"
        
        # Check if at least one succeeded
        successful = data["summary"]["successful_queries"]
        if successful > 0:
            results.add_pass(test_name)
        else:
            results.add_fail(test_name, "No successful demographic queries")
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def test_generate_map_visualization(results):
    """Test the generate_map_visualization tool."""
    test_name = "generate_map_visualization"
    
    try:
        locations = [
            {"lat": 33.4484, "lng": -112.0740, "label": "Phoenix", "value": 1000},
            {"lat": 33.5779, "lng": -112.1006, "label": "Scottsdale", "value": 800}
        ]
        
        response = generate_map_visualization(
            locations=locations,
            map_type="demand_heatmap",
            zoom_level=10
        )
        
        data = json.loads(response)
        
        assert "query_parameters" in data, "Missing query_parameters"
        assert "visualization" in data, "Missing visualization"
        assert "locations_plotted" in data, "Missing locations_plotted"
        
        results.add_pass(test_name)
            
    except Exception as e:
        results.add_fail(test_name, str(e))


def run_all_tests():
    """Run all tool tests."""
    print("=" * 60)
    print("FedEx Market Intelligence Agent - Tool Tests")
    print("=" * 60)
    print()
    
    results = TestResults()
    
    print("Testing Tools:")
    print("-" * 60)
    
    # Run all tests
    test_query_shipment_trends(results)
    test_analyze_geographic_demand(results)
    test_find_market_opportunities(results)
    test_compare_markets(results)
    test_forecast_demand(results)
    test_get_demographics(results)
    test_generate_map_visualization(results)
    
    # Print summary
    success = results.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

