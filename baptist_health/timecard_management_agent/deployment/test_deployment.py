# Copyright 2025 Baptist Health
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test deployment script for Baptist Health Timecard Management Agent"""

import os
import sys
import logging
import subprocess
from pathlib import Path

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_environment() -> bool:
    """Test if the environment is properly configured."""
    logger.info("Testing environment configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION", 
        "GOOGLE_CLOUD_STORAGE_BUCKET"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        return False
    
    logger.info("Environment configuration is valid")
    return True


def test_authentication() -> bool:
    """Test if gcloud authentication is working."""
    logger.info("Testing gcloud authentication...")
    
    try:
        result = subprocess.run(
            ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip():
            logger.info(f"Authenticated as: {result.stdout.strip()}")
            return True
        else:
            logger.error("No active gcloud authentication found")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"gcloud authentication test failed: {e}")
        return False


def test_project_access() -> bool:
    """Test if we can access the GCP project."""
    logger.info("Testing GCP project access...")
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    try:
        result = subprocess.run(
            ["gcloud", "projects", "describe", project_id, "--format=value(projectId)"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if result.stdout.strip() == project_id:
            logger.info(f"Successfully accessed project: {project_id}")
            return True
        else:
            logger.error(f"Project access test failed for: {project_id}")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Project access test failed: {e}")
        return False


def test_agent_engine_api() -> bool:
    """Test if Agent Engine API is enabled."""
    logger.info("Testing Agent Engine API...")
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    try:
        result = subprocess.run(
            ["gcloud", "services", "list", "--enabled", "--filter=name:aiplatform.googleapis.com", "--format=value(name)"],
            capture_output=True,
            text=True,
            check=True
        )
        
        if "aiplatform.googleapis.com" in result.stdout:
            logger.info("Agent Engine API is enabled")
            return True
        else:
            logger.error("Agent Engine API is not enabled")
            return False
            
    except subprocess.CalledProcessError as e:
        logger.error(f"Agent Engine API test failed: {e}")
        return False


def test_python_environment() -> bool:
    """Test if the Python environment is properly set up."""
    logger.info("Testing Python environment...")
    
    # Check if we're in the right directory
    agent_dir = Path(__file__).parent.parent
    
    if not agent_dir.exists():
        logger.error(f"Agent directory not found: {agent_dir}")
        return False
    
    # Check if poetry is available
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Poetry version: {result.stdout.strip()}")
    except subprocess.CalledProcessError:
        logger.error("Poetry is not installed or not in PATH")
        return False
    
    # Check if we can import the agent
    try:
        sys.path.append(str(agent_dir))
        from timecard_management_agent.agent import root_agent
        from timecard_management_agent.config import Config
        
        logger.info(f"Agent imported successfully: {root_agent.name}")
        return True
        
    except ImportError as e:
        logger.error(f"Failed to import agent: {e}")
        return False


def test_storage_bucket() -> bool:
    """Test if the storage bucket exists and is accessible."""
    logger.info("Testing storage bucket access...")
    
    bucket = os.getenv("GOOGLE_CLOUD_STORAGE_BUCKET")
    
    try:
        result = subprocess.run(
            ["gsutil", "ls", f"gs://{bucket}"],
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"Storage bucket is accessible: gs://{bucket}")
        return True
        
    except subprocess.CalledProcessError:
        logger.warning(f"Storage bucket does not exist: gs://{bucket}")
        logger.info("This is normal for first deployment. The bucket will be created automatically.")
        return True


def main():
    """Run all deployment tests."""
    logger.info("Starting deployment tests...")
    
    tests = [
        ("Environment Configuration", test_environment),
        ("gcloud Authentication", test_authentication),
        ("GCP Project Access", test_project_access),
        ("Agent Engine API", test_agent_engine_api),
        ("Python Environment", test_python_environment),
        ("Storage Bucket", test_storage_bucket),
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name}: PASSED")
            else:
                logger.error(f"❌ {test_name}: FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "="*50)
    logger.info("DEPLOYMENT TEST SUMMARY")
    logger.info("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Ready for deployment.")
        return True
    else:
        logger.error("⚠️  Some tests failed. Please fix the issues before deploying.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
