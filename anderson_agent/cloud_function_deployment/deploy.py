#!/usr/bin/env python3
"""
Deployment script for PowerPoint Generation Cloud Function
Deploys the serverless API to Google Cloud Functions
"""

import os
import sys
import subprocess
import json
import argparse
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip(), result.stderr.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed: {command}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def check_gcloud_auth():
    """Check if gcloud is authenticated"""
    try:
        stdout, stderr = run_command("gcloud auth list --filter=status:ACTIVE --format='value(account)'")
        if stdout:
            print(f"✅ Authenticated as: {stdout}")
            return True
        else:
            print("❌ No active gcloud authentication found")
            return False
    except:
        print("❌ gcloud CLI not found or not working")
        return False

def get_project_id():
    """Get current gcloud project ID"""
    try:
        stdout, stderr = run_command("gcloud config get-value project")
        if stdout:
            print(f"✅ Current project: {stdout}")
            return stdout
        else:
            print("❌ No project set in gcloud config")
            return None
    except:
        print("❌ Could not get project ID")
        return None

def create_symlink_to_ppt_tool():
    """Create a symlink to the ppt_creator_tool for the function to access"""
    deployment_dir = Path(__file__).parent
    ppt_tool_dir = deployment_dir.parent / "ppt_creator_tool"
    
    # Create symlink in deployment directory
    symlink_path = deployment_dir / "ppt_creator_tool"
    
    if symlink_path.exists():
        if symlink_path.is_symlink():
            print("✅ Symlink to ppt_creator_tool already exists")
        else:
            print("⚠️  ppt_creator_tool directory exists but is not a symlink")
    else:
        try:
            symlink_path.symlink_to(ppt_tool_dir)
            print("✅ Created symlink to ppt_creator_tool")
        except Exception as e:
            print(f"❌ Failed to create symlink: {e}")
            return False
    
    return True

def deploy_function(project_id, region, function_name, memory="1GB", timeout="540s"):
    """Deploy the Cloud Function"""
    
    print(f"\n🚀 Deploying Cloud Function: {function_name}")
    print(f"   Project: {project_id}")
    print(f"   Region: {region}")
    print(f"   Memory: {memory}")
    print(f"   Timeout: {timeout}")
    
    # Create symlink to ppt_creator_tool
    if not create_symlink_to_ppt_tool():
        print("❌ Failed to create symlink, deployment aborted")
        return False
    
    # Build deployment command
    deployment_dir = Path(__file__).parent
    
    deploy_cmd = f"""
    gcloud functions deploy {function_name} \
        --gen2 \
        --runtime=python311 \
        --region={region} \
        --source={deployment_dir} \
        --entry-point=ppt_generator \
        --trigger-http \
        --allow-unauthenticated \
        --memory={memory} \
        --timeout={timeout} \
        --max-instances=10 \
        --cpu=1 \
        --set-env-vars="PPT_API_KEY=$PPT_API_KEY"
    """.strip()
    
    print(f"\n📋 Deployment command:")
    print(deploy_cmd)
    
    # Execute deployment
    try:
        stdout, stderr = run_command(deploy_cmd, cwd=deployment_dir)
        print("✅ Deployment successful!")
        print(stdout)
        return True
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return False

def get_function_url(project_id, region, function_name):
    """Get the deployed function URL"""
    try:
        stdout, stderr = run_command(f"gcloud functions describe {function_name} --region={region} --format='value(url)'")
        if stdout:
            return stdout
        else:
            return None
    except:
        return None

def test_deployment(function_url):
    """Test the deployed function"""
    if not function_url:
        print("❌ No function URL available for testing")
        return False
    
    print(f"\n🧪 Testing deployment at: {function_url}")
    
    # Test health endpoint
    try:
        import requests
        response = requests.get(f"{function_url}/health", timeout=30)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Deploy PowerPoint Generation Cloud Function")
    parser.add_argument("--project", help="Google Cloud Project ID")
    parser.add_argument("--region", default="us-central1", help="Deployment region (default: us-central1)")
    parser.add_argument("--function-name", default="ppt-generator", help="Function name (default: ppt-generator)")
    parser.add_argument("--memory", default="1GB", help="Memory allocation (default: 1GB)")
    parser.add_argument("--timeout", default="540s", help="Function timeout (default: 540s)")
    parser.add_argument("--skip-auth-check", action="store_true", help="Skip authentication check")
    parser.add_argument("--test-only", action="store_true", help="Only test existing deployment")
    
    args = parser.parse_args()
    
    print("🎯 PowerPoint Generation Cloud Function Deployment")
    print("=" * 50)
    
    # Check authentication
    if not args.skip_auth_check:
        if not check_gcloud_auth():
            print("\n💡 To authenticate, run: gcloud auth login")
            sys.exit(1)
    
    # Get project ID
    project_id = args.project or get_project_id()
    if not project_id:
        print("\n💡 To set project, run: gcloud config set project YOUR_PROJECT_ID")
        sys.exit(1)
    
    # Test only mode
    if args.test_only:
        function_url = get_function_url(project_id, args.region, args.function_name)
        if function_url:
            test_deployment(function_url)
        else:
            print(f"❌ Function {args.function_name} not found in region {args.region}")
        return
    
    # Deploy function
    success = deploy_function(
        project_id=project_id,
        region=args.region,
        function_name=args.function_name,
        memory=args.memory,
        timeout=args.timeout
    )
    
    if success:
        # Get function URL
        function_url = get_function_url(project_id, args.region, args.function_name)
        if function_url:
            print(f"\n🌐 Function URL: {function_url}")
            
            # Test deployment
            if test_deployment(function_url):
                print("\n🎉 Deployment completed successfully!")
                print(f"\n📚 API Documentation:")
                print(f"   Health Check: GET {function_url}/health")
                print(f"   Generate PPT: POST {function_url}/generate")
                print(f"   Templates: GET {function_url}/templates")
                
                print(f"\n🔑 Security:")
                print(f"   Set PPT_API_KEY environment variable for API key authentication")
                print(f"   Include X-API-Key header in requests")
            else:
                print("\n⚠️  Deployment completed but health check failed")
        else:
            print("\n⚠️  Deployment completed but could not retrieve function URL")
    else:
        print("\n❌ Deployment failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
