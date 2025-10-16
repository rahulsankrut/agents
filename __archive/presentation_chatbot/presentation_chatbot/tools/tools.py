"""Tools for the presentation chatbot."""

import json
import logging
import requests
from typing import List, Optional
from pydantic import BaseModel, Field
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


def generate_presentation(
    title: str,
    logo_gcs_url: Optional[str] = None,
    text_content: Optional[List[str]] = None,
    image_data: Optional[List[ImageData]] = None,
    include_eqi: bool = True,
) -> str:
    """
    Generate a PowerPoint presentation using the cloud function.
    
    Args:
        title: The presentation title (required)
        logo_gcs_url: GCS URL for the logo image (optional)
        text_content: List of text content for the left box
        image_data: List of image data with GCS URLs and titles
        include_eqi: Whether to include Execution Quality Index
        
    Returns:
        A message confirming the presentation was generated
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
            # Save the presentation file
            filename = f"{title.replace(' ', '_')}.pptx"
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            file_size = len(response.content)
            logger.info(f"Presentation generated successfully: {filename} ({file_size:,} bytes)")
            logger.info(f"Response headers: {dict(response.headers)}")
            
            return f"✅ Presentation generated successfully! File saved as '{filename}' ({file_size:,} bytes). The presentation includes your title, text content, and any images you provided."
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
