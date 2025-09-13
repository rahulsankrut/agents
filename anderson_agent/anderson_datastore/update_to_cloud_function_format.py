#!/usr/bin/env python3
"""
Update Firestore database with cloud function format data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from firestore_operations import FirestoreManager
from schema import Project, ImageData
import json

def update_database_with_cloud_function_format():
    """Update database with cloud function format data"""
    
    # Initialize Firestore manager
    db_manager = FirestoreManager(project_id='agent-space-465923')
    
    print('🔄 UPDATING DATABASE WITH CLOUD FUNCTION FORMAT')
    print('=' * 60)
    
    # Clear existing data first
    print('🗑️  Clearing existing data...')
    try:
        # Get all existing projects
        existing_projects = db_manager.list_projects()
        for project in existing_projects:
            db_manager.delete_project(project.project_id)
        print(f'✅ Cleared {len(existing_projects)} existing projects')
    except Exception as e:
        print(f'⚠️  Error clearing data: {e}')
    
    # New data in cloud function format
    cloud_function_data = [
        {
            "project_id": "8c5a2c4e-6b7c-4f1e-9d2a-1b3d5f7a9e2d",
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "Colgate-Palmolive: Colgate TOP traited Priority Item OSA \"TEST to WIN\" (250 Clubs)",
            "project_overview": "• Provide OSA stocking services for Oral Care, Personal Care, and Home Care items for Colgate-Palmolive brands across multi-Departments .\n• Service TOP store traited PRIORITY items in EACH(3) Categories .\n• Merchandise (packout and price) .\n• Service items flagged with zero sales .\n• Work with store to request OH adjustments when applicable .\n• Place Rollback and New item flags when needed .\n• Special Focus on Suavitel laundry Detergent items.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/1-1.png",
                    "description": "Image for Colgate-Palmolive: Colgate TOP traited Priority Item OSA \"TEST to WIN\" (250 Clubs)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/1-2.png",
                    "description": "Image for Colgate-Palmolive: Colgate TOP traited Priority Item OSA \"TEST to WIN\" (250 Clubs)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/1-3.png",
                    "description": "Image for Colgate-Palmolive: Colgate TOP traited Priority Item OSA \"TEST to WIN\" (250 Clubs)"
                }
            ]
        },
        {
            "project_id": "9d6b3d5f-7c8d-5a2f-a0e3b-2c4e6a8b0f3e",
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)",
            "project_overview": "• Maintain the Grocery Endcap Feature through May-September .\n• IF NOT set or display NOT located, Work to set .\n• Confirm display set to MOD each visit .\n• Packout and zone display EACH visit.\n• Reminder-Do NOT Discard PDQ Trays! Stores will NOT get replacements.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/2-1.png",
                    "description": "Image for Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/2-2.png",
                    "description": "Image for Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/2-3.png",
                    "description": "Image for Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)"
                }
            ]
        },
        {
            "project_id": "a07c4e6a-8d9e-6b3a-b1f4c-3d5f7b9c1a4f",
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "U&I Distributors: Game Signing (3623 Stores)",
            "project_overview": "• Locate new Game Signing shipped via ShopComm Weekly .\n• New signage includes: Madden NFL 26 Side Panels and Case Topper .\n• Set signage in D5 Gaming on the New Release Endcap and take a final set photo.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/3-1.png",
                    "description": "Image for U&I Distributors: Game Signing (3623 Stores)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/3-2.png",
                    "description": "Image for U&I Distributors: Game Signing (3623 Stores)"
                }
            ]
        },
        {
            "project_id": "b18d5f7b-9e0f-7c4b-c2a5d-4e6a8ca2b5b0",
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "TNT: Parking Lot Take Down Survey (Utah Stores) (37 Stores)",
            "project_overview": "• The TNT Fireworks stand/tent outside of the store should be taken down .\n• Is the tent/stand removed? \n• Does the general area look clean in appearance? \n• Receiving any feedback from store management that TNT needs to address.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/4-1.png",
                    "description": "Image for TNT: Parking Lot Take Down Survey (Utah Stores) (37 Stores)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/4-2.png",
                    "description": "Image for TNT: Parking Lot Take Down Survey (Utah Stores) (37 Stores)"
                }
            ]
        },
        {
            "project_id": "c29e6a8c-a11a-8d5c-d3b6e-5f7b9db3c6c1",
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Advil TABLET 2pk Vial Packouts (1981 Stores)",
            "project_overview": "• Advil TABLET 2pk Vial could be located in (2) locations of the store: Front of Store Checklanes and or Trial and Travel Section .\n• Utilize MyDevice/Store system to locate all traited Advil 2pk items .\n• Stock and Balance in their store traited location(s) .\n• Utilize UPC/DPCI number on packaging for proper placement.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/5-1.png",
                    "description": "Image for Haleon: Advil TABLET 2pk Vial Packouts (1981 Stores)"
                }
            ]
        },
        {
            "project_id": "d3af7b9d-b22b-9e6d-e4c7f-6a8caec4d7d2",
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Advil Top Ten Validate SCAN (VSCAN) (1966 Stores)",
            "project_overview": "• Confirm if Item(s) traited in Targets system using the Target MyDevice .\n• Find items PlanOGram \"POG\" location(s) on the sales floor .\n• Locate the item in the backroom using the Target MyDevice .\n• Packout item to the sales floor .\n• Validate the On-Hands using the Target MyDevice.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/6-1.png",
                    "description": "Image for Haleon: Advil Top Ten Validate SCAN (VSCAN) (1966 Stores)"
                }
            ]
        },
        {
            "project_id": "e4b08cae-c33c-a07e-f5d8a-7b9dbfd5e8e3",
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Parodontax NEW Package Rotation (1966 Stores)",
            "project_overview": "• Locate Parodontax toothpaste on shelf .\n• ROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through .\n• Locate the Parodontax Mouthwash on the shelf .\n• ROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/7-1.png",
                    "description": "Image for Haleon: Parodontax NEW Package Rotation (1966 Stores)"
                }
            ]
        },
        {
            "project_id": "f5c19dbf-d44d-b18f-a6e9b-8caec0e6f9f4",
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: \"TEST\" Tums Multi-Vendor Corrugate SideCap Award Set/Maintain (250 Stores)",
            "project_overview": "• Continue to work to set and Merchandise EACH visit .\n• Locate if not already set the EMPTY flat SideCap shipped to store \"Hold for Anderson\" .\n• Confirm Feature is set to correct POG .\n• Packout ONLY the (3)Tums SKUs .\n• Place pricing as needed.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/8-1.png",
                    "description": "Image for Haleon: \"TEST\" Tums Multi-Vendor Corrugate SideCap Award Set/Maintain (250 Stores)"
                }
            ]
        },
        {
            "project_id": "a6d2aec0-e55e-c29a-b7fa-9dbfd1f7a0a5",
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Colgate: Total Toothpaste ENDCAP Audit (598 Clubs)",
            "project_overview": "• The Colgate Toothpaste Endcap is to be set in Health & Beauty .\n• Packout, pull forward and place pricing as needed .\n• If a Feature is NOT set, work with club to place a display.",
            "eqi": True,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/9-1.png",
                    "description": "Image for Colgate: Total Toothpaste ENDCAP Audit (598 Clubs)"
                }
            ]
        },
        {
            "project_id": "b7e3bfd1-f66f-d3ab-c80b-aec0e2a8b1b6",
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Colgate: Liquid Fabric Softener Audit (598 Clubs)",
            "project_overview": "• We will be Auditing various Liquid Fabric Softeners monthly .\n• Locate to confirm it is available the item in the Home Dept- Laundry care section of club .\n• Report on pricing .\n• Take a clear photo of the pallet AND Pricing.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/10-1.png",
                    "description": "Image for Colgate: Liquid Fabric Softener Audit (598 Clubs)"
                }
            ]
        },
        {
            "project_id": "c8f4c0e2-a77a-e4bc-d91c-bfd1f3b9c2c7",
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "TNT: Parking Lot Take Down Survey (Utah Clubs) (3 Clubs)",
            "project_overview": "• The TNT Fireworks stand/tent outside of the Club should be taken down .\n• Is the tent/stand removed?\n• Does the general area look clean in appearance? \n• Receiving any feedback from Club management that TNT needs to address.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/11-1.png",
                    "description": "Image for TNT: Parking Lot Take Down Survey (Utah Clubs) (3 Clubs)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/11-2.png",
                    "description": "Image for TNT: Parking Lot Take Down Survey (Utah Clubs) (3 Clubs)"
                }
            ]
        },
        {
            "project_id": "d9a5d1f3-b88b-f5cd-ea2d-c0e2a4cad3d8",
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Square Block: Display Retrofit (Wave 1) (99 Clubs)",
            "project_overview": "• Locate the Square Display shipment shipped DTS .\n• Locate the original Square display on the sales floor .\n• Refer to the installation guide provided to retrofit the new display .\n• Take a photo in all Clubs.",
            "eqi": False,
            "images": [
                {
                    "image_url": "gs://anderson_images/project_images/12-1.png",
                    "description": "Image for Square Block: Display Retrofit (Wave 1) (99 Clubs)"
                },
                {
                    "image_url": "gs://anderson_images/project_images/12-2.png",
                    "description": "Image for Square Block: Display Retrofit (Wave 1) (99 Clubs)"
                }
            ]
        }
    ]
    
    print(f'📊 Adding {len(cloud_function_data)} projects...')
    
    # Add each project to the database
    success_count = 0
    for i, project_data in enumerate(cloud_function_data, 1):
        try:
            # Convert image data
            images = []
            for img_data in project_data['images']:
                image = ImageData(
                    image_url=img_data['image_url'],
                    description=img_data['description']
                )
                images.append(image)
            
            # Create project
            project_id = db_manager.create_project(
                customer_name=project_data['customer_name'],
                customer_logo_url=project_data['customer_logo_url'],
                project_title=project_data['project_title'],
                project_overview=project_data['project_overview'],
                eqi="Yes" if project_data['eqi'] else "No",  # Convert boolean to Yes/No
                images=images
            )
            
            print(f'✅ Project {i}/{len(cloud_function_data)}: {project_data["project_title"][:50]}...')
            success_count += 1
            
        except Exception as e:
            print(f'❌ Error adding project {i}: {e}')
    
    print()
    print(f'🎉 Successfully added {success_count}/{len(cloud_function_data)} projects')
    
    # Verify the data
    print()
    print('🔍 VERIFYING DATABASE UPDATE')
    print('=' * 40)
    
    all_projects = db_manager.list_projects()
    print(f'📊 Total projects in database: {len(all_projects)}')
    
    # Count by customer
    customer_counts = {}
    for project in all_projects:
        customer_counts[project.customer_name] = customer_counts.get(project.customer_name, 0) + 1
    
    print('📈 Projects by customer:')
    for customer, count in customer_counts.items():
        print(f'  - {customer}: {count} projects')
    
    print()
    print('✅ Database update completed successfully!')

if __name__ == "__main__":
    update_database_with_cloud_function_format()
