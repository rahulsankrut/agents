"""Enhanced tools for the presentation chatbot with GCS storage."""

import json
import logging
import requests
import os
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, Field
from google.cloud import storage
from ..config import config

logger = logging.getLogger(__name__)


def convert_to_gs_url(url: str) -> str:
    """Convert https://storage.googleapis.com/ URLs to gs:// format."""
    if url.startswith('https://storage.googleapis.com/'):
        # Remove the https://storage.googleapis.com/ prefix
        path = url.replace('https://storage.googleapis.com/', '')
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
    Generate a PowerPoint presentation using the cloud function and save to GCS.
    
    Args:
        title: The presentation title (required)
        logo_gcs_url: GCS URL for the logo image (optional)
        text_content: List of text content for the left box
        image_data: List of image data with GCS URLs and titles
        include_eqi: Whether to include Execution Quality Index
        
    Returns:
        A message with GCS URLs for the generated presentation
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
                    title = img.get("title")
                else:
                    # Assume it's a Pydantic model
                    gcs_url = getattr(img, "gcs_url", None)
                    title = getattr(img, "title", None)
                
                if gcs_url and title:
                    converted_url = convert_to_gs_url(gcs_url)
                    logger.info(f"Converting URL: {gcs_url} -> {converted_url}")
                    request_data["image_data"].append({
                        "gcs_url": converted_url,
                        "title": title
                    })
                else:
                    logger.warning(f"Missing gcs_url or title for image {i}: gcs_url={gcs_url}, title={title}")
        
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
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_title = title.replace(' ', '_').replace('/', '_').replace('\\', '_')
            filename = f"{safe_title}_{timestamp}.pptx"
            
            # Save to GCS
            gcs_url, signed_url = save_to_gcs(response.content, filename)
            
            file_size = len(response.content)
            logger.info(f"Presentation generated successfully: {filename} ({file_size:,} bytes)")
            
            if gcs_url:
                return f"""✅ Presentation generated successfully!

📁 **File Details:**
- **Filename**: {filename}
- **Size**: {file_size:,} bytes
- **GCS Location**: {gcs_url}

🔗 **Access your presentation:**
1. **GCS Console**: https://console.cloud.google.com/storage/browser/{gcs_url.replace('gs://', '')}
2. **gsutil command**: `gsutil cp {gcs_url} ./{filename}`
3. **Download via gsutil**: Run `gsutil cp {gcs_url} ./{filename}` in your terminal

The presentation includes your title, text content, and any images you provided."""
            else:
                return f"✅ Presentation generated successfully! File saved as '{filename}' ({file_size:,} bytes). However, GCS upload failed."
        else:
            error_msg = f"Failed to generate presentation: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return f"❌ {error_msg}"
            
    except Exception as e:
        error_msg = f"Error generating presentation: {str(e)}"
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
    List all presentations stored in GCS.
    
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
        
        # List all presentation files
        blobs = bucket.list_blobs(prefix="presentations/")
        presentations = []
        
        for blob in blobs:
            if blob.name.endswith('.pptx'):
                filename = blob.name.replace('presentations/', '')
                size = blob.size
                created = blob.time_created
                
                presentations.append({
                    "filename": filename,
                    "size": f"{size:,} bytes",
                    "created": created.strftime("%Y-%m-%d %H:%M:%S"),
                    "download_url": f"gs://{bucket_name}/{blob.name}"
                })
        
        if presentations:
            result = "📁 **Your Presentations:**\n\n"
            for i, pres in enumerate(presentations, 1):
                result += f"{i}. **{pres['filename']}**\n"
                result += f"   📅 Created: {pres['created']}\n"
                result += f"   📏 Size: {pres['size']}\n"
                result += f"   🔗 Download: {pres['download_url']}\n\n"
            
            result += f"💾 **Storage Location**: gs://{bucket_name}/presentations/"
            return result
        else:
            return f"📭 No presentations found in gs://{bucket_name}/presentations/"
            
    except Exception as e:
        return f"❌ Error listing presentations: {str(e)}"
