"""Test configuration management."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from fedex_market_intelligence.config import config


def test_config_values():
    """Test that all config values are set."""
    print("Testing Configuration Values...")
    
    tests_passed = []
    
    # Test project_id
    try:
        assert config.project_id is not None, "project_id not set"
        assert len(config.project_id) > 0, "project_id is empty"
        print(f"✓ project_id: {config.project_id}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ project_id: {e}")
        tests_passed.append(False)
    
    # Test location
    try:
        assert config.location is not None, "location not set"
        assert len(config.location) > 0, "location is empty"
        print(f"✓ location: {config.location}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ location: {e}")
        tests_passed.append(False)
    
    # Test dataset_id
    try:
        assert config.dataset_id is not None, "dataset_id not set"
        assert len(config.dataset_id) > 0, "dataset_id is empty"
        print(f"✓ dataset_id: {config.dataset_id}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ dataset_id: {e}")
        tests_passed.append(False)
    
    # Test root_agent_model
    try:
        assert config.root_agent_model is not None, "root_agent_model not set"
        assert len(config.root_agent_model) > 0, "root_agent_model is empty"
        print(f"✓ root_agent_model: {config.root_agent_model}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ root_agent_model: {e}")
        tests_passed.append(False)
    
    # Test temperature
    try:
        assert config.temperature is not None, "temperature not set"
        assert 0.0 <= config.temperature <= 1.0, "temperature out of range"
        print(f"✓ temperature: {config.temperature}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ temperature: {e}")
        tests_passed.append(False)
    
    # Test bigquery_dataset_path
    try:
        path = config.bigquery_dataset_path
        assert path is not None, "bigquery_dataset_path not set"
        assert "." in path, "bigquery_dataset_path invalid format"
        print(f"✓ bigquery_dataset_path: {path}")
        tests_passed.append(True)
    except AssertionError as e:
        print(f"✗ bigquery_dataset_path: {e}")
        tests_passed.append(False)
    
    return all(tests_passed)


def run_config_tests():
    """Run all configuration tests."""
    print("=" * 60)
    print("FedEx Market Intelligence Agent - Configuration Tests")
    print("=" * 60)
    print()
    
    success = test_config_values()
    
    print("\n" + "=" * 60)
    if success:
        print("✓ All configuration tests passed")
    else:
        print("✗ Some configuration tests failed")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = run_config_tests()
    sys.exit(exit_code)

