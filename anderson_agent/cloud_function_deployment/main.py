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
presentations_bucket_name = "agent-space-465923-presentations"
bucket = storage_client.bucket(bucket_name)
presentations_bucket = storage_client.bucket(presentations_bucket_name)

# Add ppt_creator_tool to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ppt_creator_tool'))

# Import PowerPoint generation functions
try:
    from simple_presentation import create_simple_presentation
    from multi_slide_presentation import create_multi_slide_presentation
    logger.info("Successfully imported PowerPoint generation functions")
except ImportError as e:
    logger.error(f"Failed to import PowerPoint generation functions: {e}")
    raise ImportError("PowerPoint generation modules not available")


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


def process_multiple_projects_data(data: dict) -> list:
    """Process and validate multiple projects data"""
    # Validate required fields
    projects = data.get('projects', [])
    if not projects:
        raise ValueError("Projects array is required")
    
    if not isinstance(projects, list):
        raise ValueError("Projects must be an array")
    
    processed_projects = []
    
    for i, project in enumerate(projects):
        try:
            # Validate project structure
            title = project.get('title')
            if not title:
                raise ValueError(f"Title is required for project {i+1}")
            
            # Extract parameters
            customer_name = project.get('customer_name', '')
            logo_gcs_url = project.get('logo_gcs_url')
            text_content = project.get('text_content', [])
            image_data = project.get('image_data', [])
            include_eqi = project.get('include_eqi', True)
            
            # Process logo data (GCS URL only)
            processed_logo_path = None
            if logo_gcs_url:
                try:
                    processed_logo_path = download_from_gcs(logo_gcs_url)
                    logger.info(f"Processed logo from GCS URL for project {i+1}")
                except Exception as e:
                    logger.error(f"Error processing logo GCS URL for project {i+1}: {e}")
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
                            logger.info(f"Processed image from GCS for project {i+1}: {img['gcs_url']}")
                        except Exception as e:
                            logger.error(f"Error processing image GCS URL for project {i+1}: {e}")
                            continue
            
            # Create processed project data
            processed_project = {
                'title': title,
                'customer_name': customer_name,
                'logo_path': processed_logo_path,
                'text_content': text_content,
                'image_data': processed_image_data,
                'include_eqi': include_eqi
            }
            
            processed_projects.append(processed_project)
            
        except Exception as e:
            logger.error(f"Error processing project {i+1}: {e}")
            raise ValueError(f"Error processing project {i+1}: {str(e)}")
    
    # Sort projects by customer name for consistent ordering
    processed_projects.sort(key=lambda x: x.get('customer_name', '').lower())
    
    logger.info(f"Processed and sorted {len(processed_projects)} projects by customer name")
    for project in processed_projects:
        logger.info(f"  - {project.get('customer_name', 'Unknown')}: {project.get('title', 'No title')}")
    
    return processed_projects


def upload_to_cloud_storage(file_path: str, filename: str) -> str:
    """Upload file to Cloud Storage and return the public URL"""
    try:
        # Create blob
        blob = presentations_bucket.blob(filename)
        
        # Upload file
        blob.upload_from_filename(file_path)
        
        # For uniform bucket-level access, we don't need to set individual ACLs
        # The bucket should be configured for public access if needed
        
        # Get public URL (this will work if bucket is configured for public access)
        public_url = blob.public_url
        
        logger.info(f"Uploaded {filename} to Cloud Storage: {public_url}")
        return public_url
        
    except Exception as e:
        logger.error(f"Error uploading to Cloud Storage: {e}")
        raise Exception(f"Failed to upload to Cloud Storage: {e}")


def generate_presentation(title: str, logo_path: str, text_content: list, 
                         image_data: list, include_eqi: bool) -> str:
    """Generate PowerPoint presentation and return Cloud Storage URL"""
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
        
        # Upload to Cloud Storage
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"presentation_{timestamp}.pptx"
        
        public_url = upload_to_cloud_storage(temp_file.name, filename)
        
        # Clean up temporary file
        os.unlink(temp_file.name)
        
        return public_url
        
    finally:
        # Restore original working directory
        os.chdir(original_cwd)


def generate_multi_slide_presentation(projects_data: list) -> str:
    """Generate multi-slide PowerPoint presentation and return Cloud Storage URL"""
    # Set working directory to ppt_creator_tool for resource access
    original_cwd = os.getcwd()
    ppt_tool_dir = os.path.join(os.path.dirname(__file__), 'ppt_creator_tool')
    
    try:
        if os.path.exists(ppt_tool_dir):
            os.chdir(ppt_tool_dir)
            logger.info(f"Changed working directory to: {ppt_tool_dir}")
        
        # Create the multi-slide presentation
        prs = create_multi_slide_presentation(projects_data)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pptx')
        prs.save(temp_file.name)
        temp_file.close()
        
        logger.info(f"Multi-slide presentation saved to: {temp_file.name}")
        
        # Upload to Cloud Storage
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"multi_slide_presentation_{timestamp}.pptx"
        
        public_url = upload_to_cloud_storage(temp_file.name, filename)
        
        # Clean up temporary file
        os.unlink(temp_file.name)
        
        return public_url
        
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
                "generate_multi": "POST /generate_multi",
                "templates": "GET /templates"
            }
        })
    
    elif request.path == '/templates':
        return jsonify({
            "templates": [
                {
                    "name": "simple_presentation",
                    "description": "Creates a simple PowerPoint presentation with one slide",
                    "endpoint": "/generate",
                    "parameters": {
                        "title": "string - Presentation title (required)",
                        "logo_gcs_url": "string - GCS URL for logo image (optional)",
                        "logo_path": "string - Path to logo image (optional)",
                        "text_content": "string/array - Text content for slides (optional)",
                        "image_data": "array - List of image objects with 'gcs_url', 'title' fields (optional)",
                        "include_eqi": "boolean - Whether to include EQI slide (default: True)"
                    }
                },
                {
                    "name": "multi_slide_presentation",
                    "description": "Creates a PowerPoint presentation with multiple slides from multiple projects",
                    "endpoint": "/generate_multi",
                    "parameters": {
                        "projects": "array - List of project objects (required)",
                        "project_object": {
                            "title": "string - Project title (required)",
                            "logo_gcs_url": "string - GCS URL for logo image (optional)",
                            "text_content": "string/array - Text content for slides (optional)",
                            "image_data": "array - List of image objects with 'gcs_url', 'title' fields (optional)",
                            "include_eqi": "boolean - Whether to include EQI slide (default: True)"
                        }
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
            cloud_storage_url = generate_presentation(title, logo_path, text_content, image_data, include_eqi)
            
            # Return JSON response with Cloud Storage URL
            return jsonify({
                "status": "success",
                "message": "Presentation generated successfully",
                "presentation_url": cloud_storage_url,
                "filename": f"{title.replace(' ', '_')}.pptx"
            })
                
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error generating presentation: {e}")
            return jsonify({"error": f"Failed to generate presentation: {str(e)}"}), 500
    
    elif request.path == '/generate_multi':
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
            
            # Process multiple projects data
            processed_projects = process_multiple_projects_data(data)
            
            # Generate multi-slide presentation
            cloud_storage_url = generate_multi_slide_presentation(processed_projects)
            
            # Return JSON response with Cloud Storage URL
            return jsonify({
                "status": "success",
                "message": "Multi-slide presentation generated successfully",
                "presentation_url": cloud_storage_url,
                "filename": "multi_slide_presentation.pptx",
                "project_count": len(processed_projects)
            })
                
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error generating multi-slide presentation: {e}")
            return jsonify({"error": f"Failed to generate multi-slide presentation: {str(e)}"}), 500
    
    else:
        return jsonify({"error": "Endpoint not found"}), 404