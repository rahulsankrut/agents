"""
Simple test script for Anderson Firestore Database
Tests basic functionality without requiring actual Firestore connection.
"""

import sys
import os
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from schema import Project, Customer, ImageData, COLLECTIONS
from test_data import SAMPLE_CUSTOMERS, SAMPLE_PROJECTS


def test_schema_creation():
    """Test creating schema objects."""
    print("Testing schema creation...")
    
    # Test ImageData
    image = ImageData(
        image_url="gs://test-bucket/test-image.png",
        description="Test image description"
    )
    assert image.image_url == "gs://test-bucket/test-image.png"
    assert image.description == "Test image description"
    print("✓ ImageData creation successful")
    
    # Test Customer
    customer = Customer(
        customer_id="test-customer-123",
        customer_name="Test Customer",
        customer_logo_url="gs://test-bucket/test-logo.png"
    )
    assert customer.customer_name == "Test Customer"
    assert len(customer.projects) == 0
    print("✓ Customer creation successful")
    
    # Test Project
    project = Project(
        project_id="test-project-123",
        customer_name="Test Customer",
        customer_logo_url="gs://test-bucket/test-logo.png",
        project_title="Test Project",
        project_overview="This is a test project overview",
        images=[image]
    )
    assert project.project_title == "Test Project"
    assert len(project.images) == 1
    assert project.images[0].description == "Test image description"
    print("✓ Project creation successful")
    
    print("All schema tests passed!\n")


def test_sample_data():
    """Test sample data structure."""
    print("Testing sample data...")
    
    # Test sample customers
    assert len(SAMPLE_CUSTOMERS) == 5
    for customer in SAMPLE_CUSTOMERS:
        assert "customer_name" in customer
        assert "customer_logo_url" in customer
        assert customer["customer_logo_url"].startswith("gs://")
    print("✓ Sample customers data valid")
    
    # Test sample projects
    assert len(SAMPLE_PROJECTS) == 5
    for project in SAMPLE_PROJECTS:
        assert "customer_name" in project
        assert "project_title" in project
        assert "project_overview" in project
        assert "images" in project
        assert len(project["images"]) > 0
        
        for image in project["images"]:
            assert isinstance(image, ImageData)
            assert image.image_url.startswith("gs://")
            assert len(image.description) > 0
    print("✓ Sample projects data valid")
    
    print("All sample data tests passed!\n")


def test_collections_constants():
    """Test collection name constants."""
    print("Testing collection constants...")
    
    assert COLLECTIONS["CUSTOMERS"] == "customers"
    assert COLLECTIONS["PROJECTS"] == "projects"
    print("✓ Collection constants valid")
    
    print("All constants tests passed!\n")


def test_validation_constants():
    """Test validation constants."""
    print("Testing validation constants...")
    
    from schema import (
        MAX_CUSTOMER_NAME_LENGTH,
        MAX_PROJECT_TITLE_LENGTH,
        MAX_PROJECT_OVERVIEW_LENGTH,
        MAX_IMAGE_DESCRIPTION_LENGTH
    )
    
    assert MAX_CUSTOMER_NAME_LENGTH == 100
    assert MAX_PROJECT_TITLE_LENGTH == 500
    assert MAX_PROJECT_OVERVIEW_LENGTH == 5000
    assert MAX_IMAGE_DESCRIPTION_LENGTH == 1000
    print("✓ Validation constants valid")
    
    print("All validation tests passed!\n")


def main():
    """Run all tests."""
    print("=== Anderson Firestore Database Tests ===\n")
    
    try:
        test_schema_creation()
        test_sample_data()
        test_collections_constants()
        test_validation_constants()
        
        print("🎉 All tests passed successfully!")
        print("\nThe Anderson Firestore Database is ready to use!")
        print("Next steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Set up Google Cloud authentication")
        print("3. Set your project ID: export GOOGLE_CLOUD_PROJECT=your-project-id")
        print("4. Run example_usage.py to test with actual Firestore")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
