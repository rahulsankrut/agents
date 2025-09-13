"""Enhanced tools for the presentation chatbot with GCS storage."""

import json
import logging
import requests
import os
import sys
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
from google.cloud import storage

# Add the anderson_datastore to the path for Firestore integration
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'anderson_datastore'))

try:
    from firestore_operations import FirestoreManager
    from schema import Project, Customer, ImageData as FirestoreImageData
    FIRESTORE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"Firestore integration not available: {e}")
    FIRESTORE_AVAILABLE = False

from ..config import config

logger = logging.getLogger(__name__)


def convert_to_gs_url(url: str) -> str:
    """Convert https://storage.googleapis.com/ or https://storage.cloud.google.com/ URLs to gs:// format."""
    if url.startswith('https://storage.googleapis.com/'):
        # Remove the https://storage.googleapis.com/ prefix
        path = url.replace('https://storage.googleapis.com/', '')
        # Convert to gs:// format
        return f"gs://{path}"
    elif url.startswith('https://storage.cloud.google.com/'):
        # Remove the https://storage.cloud.google.com/ prefix
        path = url.replace('https://storage.cloud.google.com/', '')
        # Convert to gs:// format
        return f"gs://{path}"
    return url


class ImageData(BaseModel):
    """Image data model."""
    
    gcs_url: str = Field(description="GCS URL of the image")
    title: str = Field(description="Title for the image")


class GeneratePresentationInput(BaseModel):
    """Input model for generating presentations."""
    
    title: str = Field(description="Presentation title")
    logo_gcs_url: Optional[str] = Field(default=None, description="GCS URL for logo image")
    text_content: List[str] = Field(description="Text content for the left box")
    image_data: List[ImageData] = Field(default=[], description="Images for the right box")
    include_eqi: bool = Field(default=True, description="Whether to include EQI")


class ProjectData(BaseModel):
    """Project data model for multi-slide presentations."""
    
    title: str = Field(description="Project title")
    logo_gcs_url: Optional[str] = Field(default=None, description="GCS URL for logo image")
    text_content: List[str] = Field(description="Text content for the project")
    image_data: List[ImageData] = Field(default=[], description="Images for the project")
    include_eqi: bool = Field(default=True, description="Whether to include EQI")


class GenerateMultiSlidePresentationInput(BaseModel):
    """Input model for generating multi-slide presentations."""
    
    projects: List[ProjectData] = Field(description="List of projects to include in the presentation")


def save_to_gcs(file_content: bytes, filename: str, bucket_name: Optional[str] = None) -> tuple[Optional[str], Optional[str]]:
    """Save presentation file to Google Cloud Storage."""
    try:
        # Use provided bucket or default to existing bucket
        if not bucket_name:
            bucket_name = "agent-space-465923-presentations"
        
        logger.info(f"Attempting to save {filename} to bucket: {bucket_name}")
        logger.info(f"File content size: {len(file_content)} bytes")
        
        # Initialize GCS client
        storage_client = storage.Client(project=config.project_id)
        logger.info(f"Initialized GCS client for project: {config.project_id}")
        
        # Get bucket (don't create if it doesn't exist)
        try:
            bucket = storage_client.get_bucket(bucket_name)
            logger.info(f"Successfully accessed bucket: {bucket_name}")
        except Exception as e:
            logger.error(f"Failed to access bucket {bucket_name}: {e}")
            return None, None
        
        # Create blob and upload
        blob_path = f"presentations/{filename}"
        blob = bucket.blob(blob_path)
        logger.info(f"Created blob at path: {blob_path}")
        
        # Upload the file content
        blob.upload_from_string(
            file_content, 
            content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation'
        )
        logger.info(f"Successfully uploaded file to GCS")
        
        gcs_url = f"gs://{bucket_name}/{blob_path}"
        
        logger.info(f"Presentation saved to GCS: {gcs_url}")
        
        return gcs_url, None
        
    except Exception as e:
        logger.error(f"Error saving to GCS: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return None, None


def generate_presentation(
    title: str,
    logo_gcs_url: Optional[str] = None,
    text_content: Optional[List[str]] = None,
    image_data: Optional[List[ImageData]] = None,
    include_eqi: bool = True,
) -> str:
    """
    Generate a PowerPoint presentation using the cloud function with Cloud Storage integration.
    
    Args:
        title: The presentation title (required)
        logo_gcs_url: GCS URL for the logo image (optional)
        text_content: List of text content for the left box
        image_data: List of image data with GCS URLs and titles
        include_eqi: Whether to include Execution Quality Index
        
    Returns:
        A message with Cloud Storage URL for the generated presentation
    """
    try:
        # Prepare the request data
        request_data = {
            "title": title,
            "include_eqi": include_eqi,
            "text_content": text_content or []
        }
        
        # Add logo if provided
        if logo_gcs_url:
            request_data["logo_gcs_url"] = convert_to_gs_url(logo_gcs_url)
            
        # Add image data if provided
        if image_data:
            logger.info(f"Processing {len(image_data)} images")
            request_data["image_data"] = []
            for i, img in enumerate(image_data):
                logger.info(f"Processing image {i}: {type(img)} - {img}")
                # Handle both dictionary and Pydantic model cases
                if isinstance(img, dict):
                    gcs_url = img.get("gcs_url")
                    img_title = img.get("title")
                else:
                    # Assume it's a Pydantic model
                    gcs_url = getattr(img, "gcs_url", None)
                    img_title = getattr(img, "title", None)
                
                if gcs_url and img_title:
                    converted_url = convert_to_gs_url(gcs_url)
                    logger.info(f"Converting URL: {gcs_url} -> {converted_url}")
                    request_data["image_data"].append({
                        "gcs_url": converted_url,
                        "title": img_title
                    })
                else:
                    logger.warning(f"Missing gcs_url or title for image {i}: gcs_url={gcs_url}, title={img_title}")
        
        # Get the cloud function URL from environment or use default
        cloud_function_url = config.cloud_function_url
        
        logger.info(f"Sending request to {cloud_function_url}/generate")
        logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
        
        # Make the request to the cloud function
        response = requests.post(
            f"{cloud_function_url}/generate",
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=60
        )
        
        if response.status_code == 200:
            # The response now contains JSON with Cloud Storage URL
            response_data = response.json()
            cloud_storage_url = response_data.get('presentation_url')
            filename = response_data.get('filename', f"{title.replace(' ', '_')}.pptx")
            
            logger.info(f"Presentation generated successfully: {filename}")
            logger.info(f"Cloud Storage URL: {cloud_storage_url}")
            
            return f"""✅ Presentation generated successfully!

📁 **File Details:**
- **Filename**: {filename}
- **Cloud Storage URL**: {cloud_storage_url}

🔗 **Access your presentation:**
1. **Direct Download**: Click the URL above to download directly
2. **GCS Console**: https://console.cloud.google.com/storage/browser/agent-space-465923-presentations
3. **gsutil command**: `gsutil cp {cloud_storage_url.replace('https://storage.googleapis.com/', 'gs://')} ./{filename}`

The presentation includes your title, text content, logos, and any images you provided."""
        else:
            error_msg = f"Failed to generate presentation: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
            
    except Exception as e:
        error_msg = f"Error generating presentation: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"


def generate_multi_slide_presentation(
    projects: List[ProjectData],
) -> str:
    """
    Generate a multi-slide PowerPoint presentation using the cloud function with Cloud Storage integration.
    
    Args:
        projects: List of project data to include in the presentation
        
    Returns:
        A message with Cloud Storage URL for the generated presentation
    """
    try:
        # Prepare the request data
        request_data = {
            "projects": []
        }
        
        # Process each project
        for i, project in enumerate(projects):
            logger.info(f"Processing project {i+1}: {project.title}")
            
            project_data = {
                "title": project.title,
                "include_eqi": project.include_eqi,
                "text_content": project.text_content or []
            }
            
            # Add logo if provided
            if project.logo_gcs_url:
                project_data["logo_gcs_url"] = convert_to_gs_url(project.logo_gcs_url)
                
            # Add image data if provided
            if project.image_data:
                logger.info(f"Processing {len(project.image_data)} images for project {i+1}")
                project_data["image_data"] = []
                for j, img in enumerate(project.image_data):
                    logger.info(f"Processing image {j} for project {i+1}: {type(img)} - {img}")
                    # Handle both dictionary and Pydantic model cases
                    if isinstance(img, dict):
                        gcs_url = img.get("gcs_url")
                        img_title = img.get("title")
                    else:
                        # Assume it's a Pydantic model
                        gcs_url = getattr(img, "gcs_url", None)
                        img_title = getattr(img, "title", None)
                    
                    if gcs_url and img_title:
                        converted_url = convert_to_gs_url(gcs_url)
                        logger.info(f"Converting URL: {gcs_url} -> {converted_url}")
                        project_data["image_data"].append({
                            "gcs_url": converted_url,
                            "title": img_title
                        })
                    else:
                        logger.warning(f"Missing gcs_url or title for image {j} in project {i+1}: gcs_url={gcs_url}, title={img_title}")
            
            request_data["projects"].append(project_data)
        
        # Get the cloud function URL from environment or use default
        cloud_function_url = config.cloud_function_url
        
        logger.info(f"Sending request to {cloud_function_url}/generate_multi")
        logger.info(f"Request data: {json.dumps(request_data, indent=2)}")
        
        # Make the request to the cloud function
        response = requests.post(
            f"{cloud_function_url}/generate_multi",
            json=request_data,
            headers={'Content-Type': 'application/json'},
            timeout=120  # Longer timeout for multi-slide presentations
        )
        
        if response.status_code == 200:
            # The response now contains JSON with Cloud Storage URL
            response_data = response.json()
            cloud_storage_url = response_data.get('presentation_url')
            filename = response_data.get('filename', 'multi_slide_presentation.pptx')
            project_count = response_data.get('project_count', len(projects))
            
            logger.info(f"Multi-slide presentation generated successfully: {filename}")
            logger.info(f"Cloud Storage URL: {cloud_storage_url}")
            logger.info(f"Project count: {project_count}")
            
            return f"""✅ Multi-slide presentation generated successfully!

📁 **File Details:**
- **Filename**: {filename}
- **Project Count**: {project_count}
- **Cloud Storage URL**: {cloud_storage_url}

🔗 **Access your presentation:**
1. **Direct Download**: Click the URL above to download directly
2. **GCS Console**: https://console.cloud.google.com/storage/browser/agent-space-465923-presentations
3. **gsutil command**: `gsutil cp {cloud_storage_url.replace('https://storage.googleapis.com/', 'gs://')} ./{filename}`

The presentation includes a title slide and individual slides for each project with logos, text content, and images."""
        else:
            error_msg = f"Failed to generate multi-slide presentation: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
            
    except Exception as e:
        error_msg = f"Error generating multi-slide presentation: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"


def create_weekly_presentation(customer_name: Optional[str] = None) -> str:
    """
    Create a presentation for all projects or a specific customer from Firestore.
    
    Args:
        customer_name: Optional customer name to filter projects (e.g., "Walmart", "Target")
        
    Returns:
        A message with Cloud Storage URL for the generated presentation
    """
    if not FIRESTORE_AVAILABLE:
        return "❌ Firestore integration is not available. Please check the database connection."
    
    try:
        # Initialize Firestore manager
        manager = FirestoreManager()
        
        # Get projects from Firestore
        if customer_name:
            logger.info(f"Getting projects for customer: {customer_name}")
            projects = manager.list_projects()
            # Filter by customer name
            filtered_projects = [p for p in projects if p.customer_name.lower() == customer_name.lower()]
            
            if not filtered_projects:
                return f"❌ No projects found for customer '{customer_name}'. Available customers: {', '.join(set(p.customer_name for p in projects))}"
            
            logger.info(f"Found {len(filtered_projects)} projects for {customer_name}")
        else:
            logger.info("Getting all projects")
            projects = manager.list_projects()
            filtered_projects = projects
            logger.info(f"Found {len(filtered_projects)} total projects")
        
        if not filtered_projects:
            return "❌ No projects found in the database."
        
        # Convert Firestore projects to ProjectData format
        project_data_list = []
        
        for i, project in enumerate(filtered_projects):
            logger.info(f"Processing project {i+1}: {project.project_title}")
            
            # Convert Firestore ImageData to chatbot ImageData
            image_data = []
            for img in project.images:
                image_data.append(ImageData(
                    gcs_url=img.image_url,
                    title=img.description
                ))
            
            # Convert EQI from string to boolean
            include_eqi = project.eqi.lower() == "yes"
            
            # Create text content from project overview
            text_content = project.project_overview.split('\n') if project.project_overview else []
            
            project_data = ProjectData(
                title=project.project_title,
                logo_gcs_url=project.customer_logo_url,
                text_content=text_content,
                image_data=image_data,
                include_eqi=include_eqi
            )
            
            project_data_list.append(project_data)
        
        # Generate the multi-slide presentation
        logger.info(f"Generating presentation with {len(project_data_list)} projects")
        result = generate_multi_slide_presentation(projects=project_data_list)
        
        # Add summary information
        customer_info = f" for {customer_name}" if customer_name else ""
        summary = f"\n\n📊 **Summary:**\n"
        summary += f"- **Total Projects**: {len(project_data_list)}\n"
        if customer_name:
            summary += f"- **Customer**: {customer_name}\n"
        else:
            customers = set(p.customer_name for p in filtered_projects)
            summary += f"- **Customers**: {', '.join(customers)}\n"
        
        return result + summary
        
    except Exception as e:
        error_msg = f"Error creating weekly presentation: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"


def list_customers() -> str:
    """
    List all available customers in the Firestore database.
    
    Returns:
        List of customers with project counts
    """
    if not FIRESTORE_AVAILABLE:
        return "❌ Firestore integration is not available. Please check the database connection."
    
    try:
        # Initialize Firestore manager
        manager = FirestoreManager()
        
        # Get all projects
        projects = manager.list_projects()
        
        if not projects:
            return "📭 No projects found in the database."
        
        # Group projects by customer
        customer_projects = {}
        for project in projects:
            customer = project.customer_name
            if customer not in customer_projects:
                customer_projects[customer] = []
            customer_projects[customer].append(project)
        
        # Create summary
        result = "👥 **Available Customers:**\n\n"
        
        for customer, customer_project_list in customer_projects.items():
            result += f"🏢 **{customer}**\n"
            result += f"   📊 Projects: {len(customer_project_list)}\n"
            
            # Show project titles
            for project in customer_project_list[:3]:  # Show first 3 projects
                result += f"   • {project.project_title}\n"
            
            if len(customer_project_list) > 3:
                result += f"   • ... and {len(customer_project_list) - 3} more\n"
            
            result += "\n"
        
        result += f"💡 **Usage:**\n"
        result += f"- Say 'Create the presentation for this week' for all projects\n"
        result += f"- Say 'Create the presentation for [Customer] for this week' for specific customer\n"
        
        return result
        
    except Exception as e:
        error_msg = f"Error listing customers: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}"


def get_presentation_templates() -> str:
    """
    Get available presentation templates.
    
    Returns:
        Information about available templates
    """
    try:
        cloud_function_url = config.cloud_function_url
        response = requests.get(f"{cloud_function_url}/templates", timeout=10)
        
        if response.status_code == 200:
            templates = response.json()
            return f"Available templates: {json.dumps(templates, indent=2)}"
        else:
            return f"Failed to get templates: {response.status_code}"
            
    except Exception as e:
        return f"Error getting templates: {str(e)}"


def list_presentations(bucket_name: Optional[str] = None) -> str:
    """
    List all presentations stored in Cloud Storage.
    
    Returns:
        List of presentations with download links
    """
    try:
        if not bucket_name:
            bucket_name = "agent-space-465923-presentations"
        
        storage_client = storage.Client(project=config.project_id)
        
        try:
            bucket = storage_client.get_bucket(bucket_name)
        except Exception:
            return f"❌ Bucket {bucket_name} not found. No presentations have been created yet."
        
        # List all presentation files (both root level and any subdirectories)
        blobs = bucket.list_blobs()
        presentations = []
        
        for blob in blobs:
            if blob.name.endswith('.pptx'):
                filename = blob.name.split('/')[-1]  # Get just the filename
                size = blob.size
                created = blob.time_created
                
                # Convert to public URL format
                public_url = f"https://storage.googleapis.com/{bucket_name}/{blob.name}"
                
                presentations.append({
                    "filename": filename,
                    "size": f"{size:,} bytes",
                    "created": created.strftime("%Y-%m-%d %H:%M:%S"),
                    "download_url": public_url,
                    "gcs_path": f"gs://{bucket_name}/{blob.name}"
                })
        
        if presentations:
            # Sort by creation time (newest first)
            presentations.sort(key=lambda x: x['created'], reverse=True)
            
            result = "📁 **Your Presentations:**\n\n"
            for i, pres in enumerate(presentations, 1):
                result += f"{i}. **{pres['filename']}**\n"
                result += f"   📅 Created: {pres['created']}\n"
                result += f"   📏 Size: {pres['size']}\n"
                result += f"   🔗 Direct Download: {pres['download_url']}\n"
                result += f"   📁 GCS Path: {pres['gcs_path']}\n\n"
            
            result += f"💾 **Storage Location**: gs://{bucket_name}/\n"
            result += f"🌐 **Console Access**: https://console.cloud.google.com/storage/browser/{bucket_name}"
            return result
        else:
            return f"📭 No presentations found in gs://{bucket_name}/"
            
    except Exception as e:
        return f"❌ Error listing presentations: {str(e)}"
