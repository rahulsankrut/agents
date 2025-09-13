"""
Replace dummy data with real project data
"""

from firestore_operations import FirestoreManager
from schema import ImageData
from google.cloud import firestore
import json

# Your real data
REAL_PROJECT_DATA = [
[
  {
    "project_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
    "customer_name": "Walmart",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
    "project_title": "Colgate-Palmolive: Colgate TOP traited Priority Item OSA “TEST to WIN” (250 Clubs)",
    "project_overview": "Provide OSA stocking services for Oral Care, Personal Care, and Home Care items for Colgate-Palmolive brands across multi-Departments.\nService TOP store traited PRIORITY items in EACH(3) Categories.\nMerchandise (packout and price).\nService items flagged with zero sales.\nWork with store to request OH adjustments when applicable.\nPlace Rollback and New item flags when needed.\nSpecial Focus on Suavitel laundry Detergent items.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/1-1.png",
        "description": "Image of Colgate-Palmolive project display."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/1-2.png",
        "description": "Image of Colgate-Palmolive product stocking."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/1-3.png",
        "description": "Image of Suavitel special focus item."
      }
    ]
  },
  {
    "project_id": "b2c3d4e5-f6a7-8901-2345-67890abcdef1",
    "customer_name": "Walmart",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
    "project_title": "Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)",
    "project_overview": "Maintain the Grocery Endcap Feature through May-September.\nIF NOT set or display NOT located, Work to set.\nConfirm display set to MOD each visit.\nPackout and zone display EACH visit.\nReminder-Do NOT Discard PDQ Trays! Stores will NOT get replacements.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/2-1.png",
        "description": "Image of Ghirardelli-Lindt premium candy endcap."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/2-2.png",
        "description": "Image of summer grocery candy display."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/2-3.png",
        "description": "Close-up of PDQ trays for the candy display."
      }
    ]
  },
  {
    "project_id": "c3d4e5f6-a7b8-9012-3456-7890abcdef12",
    "customer_name": "Walmart",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
    "project_title": "U&I Distributors: Game Signing (3623 Stores)",
    "project_overview": "Locate new Game Signing shipped via ShopComm Weekly.\nNew signage includes: Madden NFL 26 Side Panels and Case Topper.\nSet signage in D5 Gaming on the New Release Endcap and take a final set photo.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/3-1.png",
        "description": "Image of Madden NFL 26 side panels."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/3-2.png",
        "description": "Image of the new release endcap with case topper."
      }
    ]
  },
  {
    "project_id": "d4e5f6a7-b8c9-0123-4567-890abcdef123",
    "customer_name": "Walmart",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
    "project_title": "TNT: Parking Lot Take Down Survey (Utah Stores) (37 Stores)",
    "project_overview": "The TNT Fireworks stand/tent outside of the store should be taken down.\nIs the tent/stand removed?\nDoes the general area look clean in appearance?\nReceiving any feedback from store management that TNT needs to address.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/4-1.png",
        "description": "Image of the area where the TNT Fireworks tent was located."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/4-2.png",
        "description": "Image showing the cleanliness of the parking lot after takedown."
      }
    ]
  },
  {
    "project_id": "e5f6a7b8-c9d0-1234-5678-90abcdef1234",
    "customer_name": "Target",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
    "project_title": "Haleon: Advil TABLET 2pk Vial Packouts (1981 Stores)",
    "project_overview": "Advil TABLET 2pk Vial could be located in (2) locations of the store: Front of Store Checklanes and or Trial and Travel Section.\nUtilize MyDevice/Store system to locate all traited Advil 2pk items.\nStock and Balance in their store traited location(s).\nUtilize UPC/DPCI number on packaging for proper placement.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/5-1.png",
        "description": "Image of Advil 2pk vials in the checklane."
      }
    ]
  },
  {
    "project_id": "f6a7b8c9-d0e1-2345-6789-0abcdef12345",
    "customer_name": "Target",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
    "project_title": "Haleon: Advil Top Ten Validate SCAN (VSCAN) (1966 Stores)",
    "project_overview": "Confirm if Item(s) traited in Targets system using the Target MyDevice.\nFind items PlanOGram 'POG' location(s) on the sales floor.\nLocate the item in the backroom using the Target MyDevice.\nPackout item to the sales floor.\nValidate the On-Hands using the Target MyDevice.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/6-1.png",
        "description": "Image of using the Target MyDevice to scan Advil products."
      }
    ]
  },
  {
    "project_id": "a7b8c9d0-e1f2-3456-7890-abcdef123456",
    "customer_name": "Target",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
    "project_title": "Haleon: Parodontax NEW Package Rotation (1966 Stores)",
    "project_overview": "Locate Parodontax toothpaste on shelf.\nROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through.\nLocate the Parodontax Mouthwash on the shelf.\nROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/7-1.png",
        "description": "Image showing new and old Parodontax packaging on the shelf."
      }
    ]
  },
  {
    "project_id": "b8c9d0e1-f2a3-4567-8901-bcdef1234567",
    "customer_name": "Target",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
    "project_title": "Haleon: “TEST” Tums Multi-Vendor Corrugate SideCap Award Set/Maintain (250 Stores)",
    "project_overview": "Continue to work to set and Merchandise EACH visit.\nLocate if not already set the EMPTY flat SideCap shipped to store “Hold for Anderson”.\nConfirm Feature is set to correct POG.\nPackout ONLY the (3)Tums SKUs.\nPlace pricing as needed.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/8-1.png",
        "description": "Image of the Tums multi-vendor corrugate sidecap."
      }
    ]
  },
  {
    "project_id": "c9d0e1f2-a3b4-5678-9012-cdef12345678",
    "customer_name": "Sam's Club",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
    "project_title": "Colgate: Total Toothpaste ENDCAP Audit (598 Clubs)",
    "project_overview": "The Colgate Toothpaste Endcap is to be set in Health & Beauty.\nPackout, pull forward and place pricing as needed.\nIf a Feature is NOT set, work with club to place a display.",
    "eqi": True,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/9-1.png",
        "description": "Image of the Colgate Total Toothpaste endcap in Health & Beauty."
      }
    ]
  },
  {
    "project_id": "d0e1f2a3-b4c5-6789-0123-def123456789",
    "customer_name": "Sam's Club",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
    "project_title": "Colgate: Liquid Fabric Softener Audit (598 Clubs)",
    "project_overview": "We will be Auditing various Liquid Fabric Softeners monthly.\nLocate to confirm it is available the item in the Home Dept- Laundry care section of club.\nReport on pricing.\nTake a clear photo of the pallet AND Pricing.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/10-1.png",
        "description": "Image of a pallet of liquid fabric softener in the laundry care section."
      }
    ]
  },
  {
    "project_id": "e1f2a3b4-c5d6-7890-1234-ef1234567890",
    "customer_name": "Sam's Club",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
    "project_title": "TNT: Parking Lot Take Down Survey (Utah Clubs) (3 Clubs)",
    "project_overview": "The TNT Fireworks stand/tent outside of the Club should be taken down.\nIs the tent/stand removed?\nDoes the general area look clean in appearance?\nReceiving any feedback from Club management that TNT needs to address.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/11-1.png",
        "description": "Image of the parking lot area after the fireworks tent has been removed."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/11-2.png",
        "description": "Survey photo of the club's exterior."
      }
    ]
  },
  {
    "project_id": "f2a3b4c5-d6e7-8901-2345-f12345678901",
    "customer_name": "Sam's Club",
    "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
    "project_title": "Square Block: Display Retrofit (Wave 1) (99 Clubs)",
    "project_overview": "Locate the Square Display shipment shipped DTS.\nLocate the original Square display on the sales floor.\nRefer to the installation guide provided to retrofit the new display.\nTake a photo in all Clubs.",
    "eqi": False,
    "images": [
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/12-1.png",
        "description": "Image of the original Square display on the sales floor."
      },
      {
        "image_url": "https://storage.cloud.google.com/anderson_images/project_images/12-2.png",
        "description": "Image of the newly retrofitted Square display."
      }
    ]
  }
]
]

def clear_existing_data():
    """Clear all existing customers and projects."""
    
    print("🗑️  Clearing existing data...")
    
    # Connect to database
    db = firestore.Client(project="agent-space-465923", database="anderson-db")
    
    # Delete all projects
    projects_ref = db.collection('projects')
    projects = list(projects_ref.stream())
    for project_doc in projects:
        projects_ref.document(project_doc.id).delete()
    print(f"  ✅ Deleted {len(projects)} projects")
    
    # Delete all customers
    customers_ref = db.collection('customers')
    customers = list(customers_ref.stream())
    for customer_doc in customers:
        customers_ref.document(customer_doc.id).delete()
    print(f"  ✅ Deleted {len(customers)} customers")
    
    print("✅ Existing data cleared!")

def add_real_data():
    """Add the real project data."""
    
    print("\n🚀 Adding real project data...")
    
    # Connect to database
    db = firestore.Client(project="agent-space-465923", database="anderson-db")
    
    # Track customers and their projects
    customers_data = {}
    
    for project_data in REAL_PROJECT_DATA:
        customer_name = project_data["customer_name"]
        
        # Initialize customer data if not exists
        if customer_name not in customers_data:
            customers_data[customer_name] = {
                "customer_id": project_data["project_id"][:8] + "-" + project_data["project_id"][9:13] + "-" + project_data["project_id"][14:18] + "-" + project_data["project_id"][19:23] + "-" + project_data["project_id"][24:36],
                "customer_name": customer_name,
                "customer_logo_url": project_data["customer_logo_url"],
                "projects": []
            }
        
        # Add project to customer
        customers_data[customer_name]["projects"].append(project_data["project_id"])
        
        # Prepare project document
        project_doc = {
            "project_id": project_data["project_id"],
            "customer_name": project_data["customer_name"],
            "customer_logo_url": project_data["customer_logo_url"],
            "project_title": project_data["project_title"],
            "project_overview": project_data["project_overview"],
            "eqi": project_data["eqi"],
            "images": project_data["images"],
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP
        }
        
        # Save project
        db.collection('projects').document(project_data["project_id"]).set(project_doc)
        print(f"  ✅ Added project: {project_data['project_title']}")
    
    # Save customers
    for customer_name, customer_data in customers_data.items():
        customer_doc = {
            "customer_id": customer_data["customer_id"],
            "customer_name": customer_data["customer_name"],
            "customer_logo_url": customer_data["customer_logo_url"],
            "projects": customer_data["projects"],
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP
        }
        
        db.collection('customers').document(customer_data["customer_id"]).set(customer_doc)
        print(f"  ✅ Added customer: {customer_name} ({len(customer_data['projects'])} projects)")
    
    print(f"\n🎉 Real data added successfully!")
    print(f"📊 Summary:")
    print(f"  - Customers: {len(customers_data)}")
    print(f"  - Projects: {len(REAL_PROJECT_DATA)}")

def verify_data():
    """Verify the new data."""
    
    print("\n🔍 Verifying new data...")
    
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Get all customers and projects
    customers = db_manager.list_customers()
    projects = db_manager.list_projects()
    
    print(f"📊 Database Contents:")
    print(f"  - Customers: {len(customers)}")
    print(f"  - Projects: {len(projects)}")
    
    print(f"\n📋 Customer-Project Breakdown:")
    for customer in customers:
        customer_projects = db_manager.get_projects_by_customer(customer.customer_id)
        print(f"  🏢 {customer.customer_name}")
        print(f"    - Projects: {len(customer_projects)}")
        for project in customer_projects:
            print(f"      📁 {project.project_title}")
            print(f"        - EQI: {project.eqi}")
            print(f"        - Images: {len(project.images)}")
    
    print("\n✅ Data verification completed!")

def main():
    """Main function to replace dummy data with real data."""
    
    print("=" * 60)
    print("🔄 REPLACING DUMMY DATA WITH REAL PROJECT DATA")
    print("=" * 60)
    
    # Step 1: Clear existing data
    clear_existing_data()
    
    # Step 2: Add real data
    add_real_data()
    
    # Step 3: Verify data
    verify_data()
    
    print("\n" + "=" * 60)
    print("🎉 DATA REPLACEMENT COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
