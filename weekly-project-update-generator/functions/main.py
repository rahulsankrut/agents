"""
Main Cloud Function for Weekly Project Update PowerPoint Generator

This function orchestrates the entire workflow:
1. Receives project details and image uploads
2. Analyzes images using Gemini 2.5 Pro
3. Generates presentation content
4. Creates PowerPoint file
5. Returns download link
"""

import functions_framework
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
import base64
import tempfile
import os

from google.cloud import storage
from google.cloud import aiplatform
from google.cloud import logging as cloud_logging

from presentation_generator import PresentationGenerator
from image_analyzer import ImageAnalyzer
from project_manager import ProjectManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Google Cloud clients
storage_client = storage.Client()
aiplatform.init(project=os.getenv('GOOGLE_CLOUD_PROJECT'))

@functions_framework.http
def generate_presentation(request):
    """
    HTTP Cloud Function entry point
    
    Expected request format:
    {
        "project_name": "Oakwood Mall Renovation",
        "client_name": "Prime Properties Inc.",
        "date_range": "Week of August 18, 2025",
        "highlights": "Completed electrical wiring, installed drywall",
        "images": [
            {
                "filename": "image1.jpg",
                "data": "base64_encoded_image_data"
            }
        ]
    }
    """
    try:
        # Set CORS headers
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
            return ('', 204, headers)
        
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        }
        
        if request.method != 'POST':
            return (json.dumps({'error': 'Only POST method is supported'}), 405, headers)
        
        # Parse request data
        request_data = request.get_json()
        if not request_data:
            return (json.dumps({'error': 'No JSON data provided'}), 400, headers)
        
        # Validate required fields
        required_fields = ['project_name', 'client_name', 'date_range', 'images']
        for field in required_fields:
            if field not in request_data:
                return (json.dumps({'error': f'Missing required field: {field}'}), 400, headers)
        
        # Extract project details
        project_details = {
            'project_name': request_data['project_name'],
            'client_name': request_data['client_name'],
            'date_range': request_data['date_range'],
            'highlights': request_data.get('highlights', ''),
            'created_at': datetime.now().isoformat()
        }
        
        # Initialize components
        project_manager = ProjectManager(storage_client)
        image_analyzer = ImageAnalyzer()
        presentation_generator = PresentationGenerator()
        
        # Process images and generate content
        logger.info(f"Starting presentation generation for project: {project_details['project_name']}")
        
        # Analyze each image
        image_analyses = []
        for i, image_data in enumerate(request_data['images']):
            try:
                # Decode base64 image
                image_bytes = base64.b64decode(image_data['data'])
                
                # Analyze image with Gemini
                analysis = image_analyzer.analyze_image(
                    image_bytes, 
                    image_data['filename'],
                    project_details
                )
                image_analyses.append(analysis)
                logger.info(f"Analyzed image {i+1}/{len(request_data['images'])}: {image_data['filename']}")
                
            except Exception as e:
                logger.error(f"Error analyzing image {image_data['filename']}: {str(e)}")
                # Continue with other images
                continue
        
        if not image_analyses:
            return (json.dumps({'error': 'No images could be analyzed'}), 400, headers)
        
        # Generate presentation
        presentation_data = presentation_generator.generate_presentation(
            project_details, 
            image_analyses
        )
        
        # Save presentation to Cloud Storage
        bucket_name = os.getenv('PRESENTATIONS_BUCKET', 'weekly-project-presentations')
        presentation_filename = f"{project_details['project_name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
        
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(presentation_filename)
        blob.upload_from_string(presentation_data, content_type='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        
        # Generate signed URL for download (expires in 1 hour)
        download_url = blob.generate_signed_url(
            version="v4",
            expiration=3600,  # 1 hour
            method="GET"
        )
        
        # Save project metadata
        project_id = project_manager.save_project_metadata(project_details, image_analyses, presentation_filename)
        
        logger.info(f"Presentation generated successfully: {presentation_filename}")
        
        return (json.dumps({
            'success': True,
            'project_id': project_id,
            'presentation_filename': presentation_filename,
            'download_url': download_url,
            'message': 'Presentation generated successfully!'
        }), 200, headers)
        
    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}")
        return (json.dumps({
            'error': 'Internal server error',
            'message': str(e)
        }), 500, headers)
