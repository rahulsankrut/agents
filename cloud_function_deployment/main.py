#!/usr/bin/env python3
"""
PowerPoint Generation Cloud Function
Deploys the simple_presentation.py script as a Google Cloud Function
"""

import functions_framework
import os
import sys
import logging
import tempfile
from io import BytesIO
from flask import request, jsonify, send_file
from werkzeug.exceptions import BadRequest
from google.cloud import storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Cloud Storage client
storage_client = storage.Client()
bucket_name = "agent-space-465923-presentation-staging"
bucket = storage_client.bucket(bucket_name)

# Add ppt_creator_tool to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ppt_creator_tool'))

# Import PowerPoint generation function
try:
    from simple_presentation import create_simple_presentation
    logger.info("Successfully imported create_simple_presentation")
except ImportError as e:
    logger.error(f"Failed to import create_simple_presentation: {e}")
    raise ImportError("PowerPoint generation module not available")


def download_from_gcs(gcs_url: str) -> str:
    """Download image from Cloud Storage and return local file path"""
    try:
        # Extract bucket name and blob name from GCS URL
        if gcs_url.startswith('gs://'):
            # Remove 'gs://' prefix and split into bucket and blob
            path_parts = gcs_url[5:].split('/', 1)
            bucket_name = path_parts[0]
            blob_name = path_parts[1] if len(path_parts) > 1 else ""
        else:
            # Assume it's just a blob name in the default bucket
            bucket_name = "agent-space-465923-presentation-staging"
            blob_name = gcs_url
        
        # Get the specific bucket
        specific_bucket = storage_client.bucket(bucket_name)
        
        # Download to temporary file
        blob = specific_bucket.blob(blob_name)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        blob.download_to_filename(temp_file.name)
        
        logger.info(f"Downloaded image from GCS: {gcs_url} -> {temp_file.name}")
        return temp_file.name
        
    except Exception as e:
        logger.error(f"Error downloading from GCS: {e}")
        raise BadRequest(f"Failed to download image from Cloud Storage: {e}")


def process_request_data(data: dict) -> tuple:
    """Process and validate request data"""
    # Validate required fields
    title = data.get('title')
    if not title:
        raise ValueError("Title is required")
    
    # Extract parameters
    logo_path = data.get('logo_path')
    logo_gcs_url = data.get('logo_gcs_url')
    text_content = data.get('text_content', [])
    image_data = data.get('image_data', [])
    include_eqi = data.get('include_eqi', True)
    
    # Process logo data (GCS URL only)
    processed_logo_path = logo_path
    if logo_gcs_url:
        try:
            processed_logo_path = download_from_gcs(logo_gcs_url)
            logger.info("Processed logo from GCS URL")
        except Exception as e:
            logger.error(f"Error processing logo GCS URL: {e}")
            processed_logo_path = None
    
    # Process image data (GCS URLs only)
    processed_image_data = []
    if image_data:
        for img in image_data:
            if 'gcs_url' in img and img['gcs_url']:
                try:
                    temp_file = download_from_gcs(img['gcs_url'])
                    processed_image_data.append({
                        'path': temp_file,
                        'title': img.get('title', 'Image')
                    })
                    logger.info(f"Processed image from GCS: {img['gcs_url']}")
                except Exception as e:
                    logger.error(f"Error processing image GCS URL: {e}")
                    continue
    
    return title, processed_logo_path, text_content, processed_image_data, include_eqi


def generate_presentation(title: str, logo_path: str, text_content: list, 
                         image_data: list, include_eqi: bool) -> str:
    """Generate PowerPoint presentation and return temporary file path"""
    # Set working directory to ppt_creator_tool for resource access
    original_cwd = os.getcwd()
    ppt_tool_dir = os.path.join(os.path.dirname(__file__), 'ppt_creator_tool')
    
    try:
        if os.path.exists(ppt_tool_dir):
            os.chdir(ppt_tool_dir)
            logger.info(f"Changed working directory to: {ppt_tool_dir}")
        
        # Create the presentation
        prs = create_simple_presentation(
            title=title,
            logo_path=logo_path,
            text_content=text_content,
            image_data=image_data,
            include_eqi=include_eqi
        )
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
        prs.save(temp_file.name)
        temp_file.close()
        
        logger.info(f"Presentation saved to: {temp_file.name}")
        return temp_file.name
        
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


@functions_framework.http
def ppt_generator(request):
    """PowerPoint Generation Cloud Function"""
    
    # Handle different endpoints
    if request.path == '/health' or request.path == '/':
        return jsonify({
            "status": "success",
            "message": "PowerPoint Generator Cloud Function is running",
            "endpoints": {
                "health": "GET /health",
                "generate": "POST /generate",
                "templates": "GET /templates"
            }
        })
    
    elif request.path == '/templates':
        return jsonify({
            "templates": [
                {
                    "name": "simple_presentation",
                    "description": "Creates a simple PowerPoint presentation",
                    "parameters": {
                        "title": "string - Presentation title (required)",
                        "logo_gcs_url": "string - GCS URL for logo image (optional)",
                        "logo_path": "string - Path to logo image (optional)",
                        "text_content": "string/array - Text content for slides (optional)",
                        "image_data": "array - List of image objects with 'gcs_url', 'title' fields (optional)",
                        "include_eqi": "boolean - Whether to include EQI slide (default: True)"
                    }
                }
            ]
        })
    
    elif request.path == '/generate':
        if request.method != 'POST':
            return jsonify({"error": "Method not allowed"}), 405
        
        try:
            # Get and validate request data
            try:
                data = request.get_json()
            except Exception as e:
                return jsonify({"error": "Invalid JSON format"}), 400
            
            if not data:
                return jsonify({"error": "No JSON data provided"}), 400
            
            # Process request data
            title, logo_path, text_content, image_data, include_eqi = process_request_data(data)
            
            # Generate presentation
            temp_file_path = generate_presentation(title, logo_path, text_content, image_data, include_eqi)
            
            # Return file download
            return send_file(
                temp_file_path,
                as_attachment=True,
                download_name=f"{title.replace(' ', '_')}.pptx",
                mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation'
            )
                
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error generating presentation: {e}")
            return jsonify({"error": f"Failed to generate presentation: {str(e)}"}), 500
    
    else:
        return jsonify({"error": "Endpoint not found"}), 404