#!/usr/bin/env python3
"""
Deployment script for Weekly Project Update PowerPoint Generator (2nd Gen Functions)

This script deploys the Cloud Functions as 2nd gen functions and sets up the necessary infrastructure.
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check if gcloud is installed
    try:
        subprocess.run(["gcloud", "--version"], check=True, capture_output=True)
        print("✅ Google Cloud CLI (gcloud) is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Google Cloud CLI (gcloud) is not installed")
        print("Please install it from: https://cloud.google.com/sdk/docs/install")
        sys.exit(1)
    
    # Check if functions-framework is available
    try:
        subprocess.run(["python", "-c", "import functions_framework"], check=True, capture_output=True)
        print("✅ functions-framework is available")
    except subprocess.CalledProcessError:
        print("❌ functions-framework is not available")
        print("Please install it: pip install functions-framework")
        sys.exit(1)

def setup_project():
    """Set up the Google Cloud project"""
    print("\n🚀 Setting up Google Cloud project...")
    
    # Get current project
    current_project = run_command("gcloud config get-value project")
    print(f"Current project: {current_project.strip()}")
    
    # Ask user if they want to change project
    change_project = input("Do you want to change the project? (y/N): ").strip().lower()
    
    if change_project == 'y':
        # List available projects
        print("\nAvailable projects:")
        run_command("gcloud projects list --format='table(projectId,name)'")
        
        new_project = input("Enter project ID: ").strip()
        run_command(f"gcloud config set project {new_project}")
        print(f"✅ Project set to: {new_project}")

def enable_apis():
    """Enable required Google Cloud APIs"""
    print("\n🔌 Enabling required APIs...")
    
    apis = [
        "cloudfunctions.googleapis.com",
        "cloudbuild.googleapis.com",
        "storage.googleapis.com",
        "aiplatform.googleapis.com",
        "logging.googleapis.com",
        "run.googleapis.com"  # Required for 2nd gen functions
    ]
    
    for api in apis:
        print(f"Enabling {api}...")
        run_command(f"gcloud services enable {api}")

def create_storage_buckets():
    """Create required Cloud Storage buckets"""
    print("\n🪣 Creating storage buckets...")
    
    project_id = run_command("gcloud config get-value project").strip()
    
    buckets = [
        "weekly-project-presentations",
        "weekly-project-metadata"
    ]
    
    for bucket in buckets:
        bucket_name = f"{bucket}-{project_id}"
        print(f"Creating bucket: {bucket_name}")
        
        try:
            run_command(f"gsutil mb gs://{bucket_name}")
            print(f"✅ Bucket {bucket_name} created")
        except:
            print(f"ℹ️ Bucket {bucket_name} already exists or creation failed")

def deploy_functions():
    """Deploy the Cloud Functions as 2nd gen"""
    print("\n🚀 Deploying Cloud Functions (2nd Gen)...")
    
    functions_dir = Path(__file__).parent.parent / "functions"
    
    # Deploy main function as 2nd gen
    print("Deploying main function as 2nd gen...")
    run_command(
        f"gcloud functions deploy generate_presentation "
        f"--gen2 "
        f"--runtime python311 "
        f"--trigger-http "
        f"--allow-unauthenticated "
        f"--source {functions_dir} "
        f"--entry-point generate_presentation "
        f"--set-env-vars GOOGLE_CLOUD_PROJECT=$(gcloud config get-value project) "
        f"--region us-central1 "
        f"--memory 2Gi "
        f"--timeout 540s",
        cwd=functions_dir
    )
    
    print("✅ Cloud Function deployed successfully")

def setup_authentication():
    """Set up authentication for the Cloud Function"""
    print("\n🔐 Setting up authentication...")
    
    # Create service account
    service_account_name = "weekly-update-generator"
    service_account_email = f"{service_account_name}@$(gcloud config get-value project).iam.gserviceaccount.com"
    
    try:
        run_command(f"gcloud iam service-accounts create {service_account_name} --display-name='Weekly Update Generator'")
        print(f"✅ Service account created: {service_account_email}")
    except:
        print(f"ℹ️ Service account {service_account_name} already exists")
    
    # Grant necessary permissions
    roles = [
        "roles/storage.admin",
        "roles/aiplatform.user",
        "roles/logging.logWriter",
        "roles/run.invoker"  # Required for 2nd gen functions
    ]
    
    for role in roles:
        run_command(f"gcloud projects add-iam-policy-binding $(gcloud config get-value project) --member=serviceAccount:{service_account_email} --role={role}")
        print(f"✅ Role {role} granted to service account")

def main():
    """Main deployment function"""
    print("🚀 Weekly Project Update PowerPoint Generator - Deployment (2nd Gen)")
    print("=" * 70)
    
    # Check prerequisites
    check_prerequisites()
    
    # Setup project
    setup_project()
    
    # Enable APIs
    enable_apis()
    
    # Create storage buckets
    create_storage_buckets()
    
    # Setup authentication
    setup_authentication()
    
    # Deploy functions
    deploy_functions()
    
    print("\n🎉 Deployment completed successfully!")
    print("\nNext steps:")
    print("1. Set up your environment variables in the Cloud Function")
    print("2. Deploy your React frontend to Firebase Hosting")
    print("3. Update the frontend to use your Cloud Function URL")
    print("4. Test the complete workflow")
    
    # Get function URL
    try:
        function_url = run_command("gcloud functions describe generate_presentation --gen2 --region us-central1 --format='value(serviceConfig.uri)'")
        print(f"\n🌐 Your Cloud Function URL: {function_url.strip()}")
    except:
        print("\n⚠️ Could not retrieve function URL. Check the Google Cloud Console.")

if __name__ == "__main__":
    main()
