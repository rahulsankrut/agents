#!/usr/bin/env python3
"""
Simple test runner for presentation generator
Runs the presentation script with the specified test title.
"""

import subprocess
import sys
import os

def main():
    """Run the presentation generator with test title and logo"""
    
    # Test data as specified
    test_title = "Client: Project/Activity Store Count: 1234"
    test_logo = "test_resources/walmart_logo.jpg"
    test_text_content = "One\nTwo\nThree"
    test_images = [
        {"path": "test_resources/test_image_one.png", "title": "Side Panels 1-4"},
        {"path": "test_resources/test_image_two.png", "title": "PlayStation Case Topper"}
    ]
    
    print("🧪 Running presentation test...")
    print(f"📝 Title: {test_title}")
    print(f"🖼️  Logo: {test_logo}")
    print(f"📄 Text Content: {test_text_content}")
    print(f"🖼️  Images: {test_images}")
    print("-" * 50)
    
    try:
        # Ensure we're in the right directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Create input file with all test data
        with open('temp_input.txt', 'w') as f:
            f.write(test_title + '\n')  # Title input
            f.write(test_logo + '\n')   # Logo path input
            # Text content input (with double Enter to finish)
            for line in test_text_content.split('\n'):
                f.write(line + '\n')
            f.write('\n')  # First empty line
            f.write('\n')  # Second empty line to end text content
            # Image data input (with single Enter to finish)
            for image_data in test_images:
                f.write(image_data['path'] + '\n')  # Image path
                f.write(image_data['title'] + '\n')  # Image title
            f.write('\n')  # Empty line to end image list
            f.write('y\n')  # EQI input (yes for test)
        
        # Run the presentation script
        with open('temp_input.txt', 'r') as input_file:
            result = subprocess.run(
                [sys.executable, 'simple_presentation.py'],
                stdin=input_file,
                capture_output=True,
                text=True,
                cwd=script_dir
            )
        
        # Clean up temporary file
        if os.path.exists('temp_input.txt'):
            os.remove('temp_input.txt')
        
        # Display results
        print("📤 Output:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️  Errors:")
            print(result.stderr)
        
        # Check if presentation was created
        if os.path.exists("simple_presentation.pptx"):
            file_size = os.path.getsize("simple_presentation.pptx")
            print(f"✅ SUCCESS! Presentation created:")
            print(f"   📁 File: simple_presentation.pptx")
            print(f"   📊 Size: {file_size:,} bytes")
            print(f"   📍 Path: {os.path.abspath('simple_presentation.pptx')}")
        else:
            print("❌ FAILED: No presentation file created")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    main()
