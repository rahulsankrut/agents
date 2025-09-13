#!/usr/bin/env python3
"""
Test script to verify logo URLs are accessible
"""

import requests

def test_logo_urls():
    """Test if logo URLs are accessible"""
    
    print("🧪 Testing Logo URL Accessibility")
    print("=" * 50)
    
    logo_urls = [
        "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
        "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png", 
        "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg"
    ]
    
    for url in logo_urls:
        try:
            print(f"Testing: {url}")
            response = requests.head(url, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                print(f"  ✅ Accessible")
            else:
                print(f"  ❌ Not accessible")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        print()

if __name__ == "__main__":
    test_logo_urls()
