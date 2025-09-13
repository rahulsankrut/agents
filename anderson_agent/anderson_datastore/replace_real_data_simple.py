"""
Replace dummy data with real project data using FirestoreManager
"""

from firestore_operations import FirestoreManager
from schema import ImageData
import uuid

def replace_with_real_data():
    """Replace dummy data with real project data."""
    
    print("🔄 REPLACING DUMMY DATA WITH REAL PROJECT DATA")
    print("=" * 60)
    
    # Initialize database manager
    db_manager = FirestoreManager(project_id="agent-space-465923")
    
    # Clear existing data
    print("🗑️  Clearing existing data...")
    customers = db_manager.list_customers()
    for customer in customers:
        db_manager.delete_customer(customer.customer_id)
    print(f"  ✅ Cleared {len(customers)} customers and their projects")
    
    # Real project data
    real_projects = [
        {
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "Colgate-Palmolive: Colgate TOP traited Priority Item OSA \"TEST to WIN\" (250 Clubs)",
            "project_overview": "Provide OSA stocking services for Oral Care, Personal Care, and Home Care items for Colgate-Palmolive brands across multi-Departments.\nService TOP store traited PRIORITY items in EACH(3) Categories.\nMerchandise (packout and price).\nService items flagged with zero sales.\nWork with store to request OH adjustments when applicable.\nPlace Rollback and New item flags when needed.\nSpecial Focus on Suavitel laundry Detergent items.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/1-1.png", "Image of Colgate-Palmolive project display."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/1-2.png", "Image of Colgate-Palmolive product stocking."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/1-3.png", "Image of Suavitel special focus item.")
            ]
        },
        {
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "Ghirardelli-Lindt: Chocolate Summer Grocery Premium Candy EndCap Set/Maintain (3354 Stores)",
            "project_overview": "Maintain the Grocery Endcap Feature through May-September.\nIF NOT set or display NOT located, Work to set.\nConfirm display set to MOD each visit.\nPackout and zone display EACH visit.\nReminder-Do NOT Discard PDQ Trays! Stores will NOT get replacements.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/2-1.png", "Image of Ghirardelli-Lindt premium candy endcap."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/2-2.png", "Image of summer grocery candy display."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/2-3.png", "Close-up of PDQ trays for the candy display.")
            ]
        },
        {
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "U&I Distributors: Game Signing (3623 Stores)",
            "project_overview": "Locate new Game Signing shipped via ShopComm Weekly.\nNew signage includes: Madden NFL 26 Side Panels and Case Topper.\nSet signage in D5 Gaming on the New Release Endcap and take a final set photo.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/3-1.png", "Image of Madden NFL 26 side panels."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/3-2.png", "Image of the new release endcap with case topper.")
            ]
        },
        {
            "customer_name": "Walmart",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/walmart-logo.png",
            "project_title": "TNT: Parking Lot Take Down Survey (Utah Stores) (37 Stores)",
            "project_overview": "The TNT Fireworks stand/tent outside of the store should be taken down.\nIs the tent/stand removed?\nDoes the general area look clean in appearance?\nReceiving any feedback from store management that TNT needs to address.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/4-1.png", "Image of the area where the TNT Fireworks tent was located."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/4-2.png", "Image showing the cleanliness of the parking lot after takedown.")
            ]
        },
        {
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Advil TABLET 2pk Vial Packouts (1981 Stores)",
            "project_overview": "Advil TABLET 2pk Vial could be located in (2) locations of the store: Front of Store Checklanes and or Trial and Travel Section.\nUtilize MyDevice/Store system to locate all traited Advil 2pk items.\nStock and Balance in their store traited location(s).\nUtilize UPC/DPCI number on packaging for proper placement.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/5-1.png", "Image of Advil 2pk vials in the checklane.")
            ]
        },
        {
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Advil Top Ten Validate SCAN (VSCAN) (1966 Stores)",
            "project_overview": "Confirm if Item(s) traited in Targets system using the Target MyDevice.\nFind items PlanOGram 'POG' location(s) on the sales floor.\nLocate the item in the backroom using the Target MyDevice.\nPackout item to the sales floor.\nValidate the On-Hands using the Target MyDevice.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/6-1.png", "Image of using the Target MyDevice to scan Advil products.")
            ]
        },
        {
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: Parodontax NEW Package Rotation (1966 Stores)",
            "project_overview": "Locate Parodontax toothpaste on shelf.\nROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through.\nLocate the Parodontax Mouthwash on the shelf.\nROTATE product with NEW packaging to the back of shelf & Old packaging to the front for sell through.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/7-1.png", "Image showing new and old Parodontax packaging on the shelf.")
            ]
        },
        {
            "customer_name": "Target",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/target-logo.png",
            "project_title": "Haleon: \"TEST\" Tums Multi-Vendor Corrugate SideCap Award Set/Maintain (250 Stores)",
            "project_overview": "Continue to work to set and Merchandise EACH visit.\nLocate if not already set the EMPTY flat SideCap shipped to store \"Hold for Anderson\".\nConfirm Feature is set to correct POG.\nPackout ONLY the (3)Tums SKUs.\nPlace pricing as needed.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/8-1.png", "Image of the Tums multi-vendor corrugate sidecap.")
            ]
        },
        {
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Colgate: Total Toothpaste ENDCAP Audit (598 Clubs)",
            "project_overview": "The Colgate Toothpaste Endcap is to be set in Health & Beauty.\nPackout, pull forward and place pricing as needed.\nIf a Feature is NOT set, work with club to place a display.",
            "eqi": "Yes",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/9-1.png", "Image of the Colgate Total Toothpaste endcap in Health & Beauty.")
            ]
        },
        {
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Colgate: Liquid Fabric Softener Audit (598 Clubs)",
            "project_overview": "We will be Auditing various Liquid Fabric Softeners monthly.\nLocate to confirm it is available the item in the Home Dept- Laundry care section of club.\nReport on pricing.\nTake a clear photo of the pallet AND Pricing.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/10-1.png", "Image of a pallet of liquid fabric softener in the laundry care section.")
            ]
        },
        {
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "TNT: Parking Lot Take Down Survey (Utah Clubs) (3 Clubs)",
            "project_overview": "The TNT Fireworks stand/tent outside of the Club should be taken down.\nIs the tent/stand removed?\nDoes the general area look clean in appearance?\nReceiving any feedback from Club management that TNT needs to address.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/11-1.png", "Image of the parking lot area after the fireworks tent has been removed."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/11-2.png", "Survey photo of the club's exterior.")
            ]
        },
        {
            "customer_name": "Sam's Club",
            "customer_logo_url": "https://storage.cloud.google.com/anderson_images/customer_logos/sams-club-logo.jpg",
            "project_title": "Square Block: Display Retrofit (Wave 1) (99 Clubs)",
            "project_overview": "Locate the Square Display shipment shipped DTS.\nLocate the original Square display on the sales floor.\nRefer to the installation guide provided to retrofit the new display.\nTake a photo in all Clubs.",
            "eqi": "No",
            "images": [
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/12-1.png", "Image of the original Square display on the sales floor."),
                ImageData("https://storage.cloud.google.com/anderson_images/project_images/12-2.png", "Image of the newly retrofitted Square display.")
            ]
        }
    ]
    
    # Add real projects
    print("\n🚀 Adding real project data...")
    for i, project_data in enumerate(real_projects, 1):
        try:
            project_id = db_manager.create_project(
                customer_name=project_data["customer_name"],
                customer_logo_url=project_data["customer_logo_url"],
                project_title=project_data["project_title"],
                project_overview=project_data["project_overview"],
                eqi=project_data["eqi"],
                images=project_data["images"]
            )
            print(f"  ✅ Added project {i}: {project_data['project_title']}")
        except Exception as e:
            print(f"  ❌ Failed to add project {i}: {e}")
    
    # Verify data
    print("\n🔍 Verifying new data...")
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
    
    print("\n🎉 Real data replacement completed successfully!")

if __name__ == "__main__":
    replace_with_real_data()
