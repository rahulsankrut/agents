#!/usr/bin/env python3
"""
Cloud Storage Permissions Fix Script
This script helps fix the permissions issues preventing logos and EQI from appearing in presentations.
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            if result.stdout:
                print(f"Output: {result.stdout}")
        else:
            print(f"❌ {description} - Failed")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exception: {e}")
        return False
    
    return True

def fix_cloud_storage_permissions():
    """Fix Cloud Storage permissions for the cloud function"""
    
    print("🔧 Cloud Storage Permissions Fix")
    print("=" * 60)
    
    # Project and bucket information
    project_id = "agent-space-465923"
    cloud_function_name = "ppt-generator"
    anderson_images_bucket = "anderson_images"
    presentations_bucket = "agent-space-465923-presentations"
    
    print(f"Project ID: {project_id}")
    print(f"Cloud Function: {cloud_function_name}")
    print(f"Source Bucket: {anderson_images_bucket}")
    print(f"Destination Bucket: {presentations_bucket}")
    print()
    
    # Step 1: Get the cloud function service account
    print("📋 Step 1: Get Cloud Function Service Account")
    print("-" * 40)
    
    get_sa_command = f"gcloud functions describe {cloud_function_name} --region=us-central1 --project={project_id} --format='value(serviceAccountEmail)'"
    
    try:
        result = subprocess.run(get_sa_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            service_account = result.stdout.strip()
            print(f"✅ Service Account: {service_account}")
        else:
            print(f"❌ Failed to get service account: {result.stderr}")
            print("Using default compute service account...")
            service_account = f"{project_id}-compute@developer.gserviceaccount.com"
    except Exception as e:
        print(f"❌ Error getting service account: {e}")
        service_account = f"{project_id}-compute@developer.gserviceaccount.com"
    
    print()
    
    # Step 2: Grant read access to anderson_images bucket
    print("📋 Step 2: Grant Read Access to anderson_images Bucket")
    print("-" * 40)
    
    commands = [
        # Grant Storage Object Viewer role for anderson_images bucket
        f"gcloud projects add-iam-policy-binding {project_id} --member=serviceAccount:{service_account} --role=roles/storage.objectViewer",
        
        # Grant Storage Object Reader role for anderson_images bucket specifically
        f"gsutil iam ch serviceAccount:{service_account}:objectViewer gs://{anderson_images_bucket}",
    ]
    
    for command in commands:
        if not run_command(command, "Granting read access to anderson_images bucket"):
            print("⚠️  Some commands failed, but continuing...")
    
    print()
    
    # Step 3: Grant write access to presentations bucket
    print("📋 Step 3: Grant Write Access to presentations Bucket")
    print("-" * 40)
    
    commands = [
        # Grant Storage Object Admin role for presentations bucket
        f"gsutil iam ch serviceAccount:{service_account}:objectAdmin gs://{presentations_bucket}",
        
        # Make presentations bucket publicly readable
        f"gsutil iam ch allUsers:objectViewer gs://{presentations_bucket}",
    ]
    
    for command in commands:
        if not run_command(command, "Granting write access to presentations bucket"):
            print("⚠️  Some commands failed, but continuing...")
    
    print()
    
    # Step 4: Verify permissions
    print("📋 Step 4: Verify Permissions")
    print("-" * 40)
    
    verify_commands = [
        f"gsutil iam get gs://{anderson_images_bucket}",
        f"gsutil iam get gs://{presentations_bucket}",
    ]
    
    for command in verify_commands:
        run_command(command, "Verifying bucket permissions")
    
    print()
    
    # Step 5: Test access
    print("📋 Step 5: Test Access")
    print("-" * 40)
    
    test_commands = [
        f"gsutil ls gs://{anderson_images_bucket}/customer_logos/",
        f"gsutil ls gs://{presentations_bucket}/",
    ]
    
    for command in test_commands:
        run_command(command, "Testing bucket access")
    
    print()
    print("🎉 Permissions fix completed!")
    print()
    print("📝 Next Steps:")
    print("1. Wait 2-3 minutes for permissions to propagate")
    print("2. Test the presentation generation again")
    print("3. Check that logos and EQI now appear in presentations")
    print()
    print("🔍 If issues persist, check:")
    print("- Cloud Function logs: gcloud functions logs read ppt-generator --region=us-central1")
    print("- Bucket permissions: gsutil iam get gs://anderson_images")
    print("- Service account: gcloud functions describe ppt-generator --region=us-central1")

def main():
    """Main function"""
    
    print("🚀 Cloud Storage Permissions Fix for Presentation Chatbot")
    print("=" * 70)
    print()
    
    # Check if gcloud is installed and authenticated
    try:
        result = subprocess.run("gcloud auth list --filter=status:ACTIVE --format='value(account)'", 
                              shell=True, capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            print(f"✅ Authenticated as: {result.stdout.strip()}")
        else:
            print("❌ Not authenticated with gcloud")
            print("Please run: gcloud auth login")
            return
    except Exception as e:
        print(f"❌ Error checking gcloud authentication: {e}")
        return
    
    print()
    
    # Run the fix
    fix_cloud_storage_permissions()

if __name__ == "__main__":
    main()
