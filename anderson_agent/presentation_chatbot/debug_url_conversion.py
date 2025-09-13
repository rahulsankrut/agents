#!/usr/bin/env python3
"""
Test script to debug the exact issue with logos and EQI
"""

import sys
import os
import requests
import json

# Add the presentation_chatbot to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'presentation_chatbot'))

from presentation_chatbot.tools.tools_enhanced import (
    create_weekly_presentation,
    convert_to_gs_url
)

def test_url_conversion():
    """Test URL conversion"""
    
    print("🧪 Testing URL Conversion")
    print("=" * 50)
    
    test_urls = [
        "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
        "https://storage.googleapis.com/anderson_images/customer_logos/walmart-logo.png",
        "gs://anderson_images/customer_logos/walmart-logo.png"
    ]
    
    for url in test_urls:
        converted = convert_to_gs_url(url)
        print(f"Original: {url}")
        print(f"Converted: {converted}")
        print()

def test_walmart_presentation():
    """Test Walmart presentation specifically"""
    
    print("🧪 Testing Walmart Presentation")
    print("=" * 50)
    
    try:
        result = create_weekly_presentation(customer_name="Walmart")
        print("✅ Walmart presentation test completed")
        print(f"Result: {result}")
        return True
        
    except Exception as e:
        print(f"❌ Walmart presentation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main debug function"""
    
    print("🔍 Debug: Logo and EQI Issues - URL Conversion Test")
    print("=" * 70)
    
    # Test URL conversion
    test_url_conversion()
    
    # Test Walmart presentation
    test_walmart_presentation()

if __name__ == "__main__":
    main()
