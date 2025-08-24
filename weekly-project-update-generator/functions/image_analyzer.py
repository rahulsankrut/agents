"""
Image Analyzer using Google Vertex AI Gemini 2.5 Pro

This module handles the AI-powered analysis of project images to generate
descriptive content for PowerPoint slides.
"""

import logging
from typing import Dict, Any, List
import base64
from io import BytesIO
from PIL import Image
import json

from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel, Part

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    """
    Analyzes project images using Gemini 2.5 Pro to generate slide content
    """
    
    def __init__(self):
        """Initialize the ImageAnalyzer with Gemini model"""
        try:
            # Initialize Gemini 2.5 Pro model
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            logger.info("ImageAnalyzer initialized successfully with Gemini 2.0 Flash")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {str(e)}")
            raise
    
    def analyze_image(self, image_bytes: bytes, filename: str, project_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a single image and generate slide content
        
        Args:
            image_bytes: Raw image data
            filename: Name of the image file
            project_details: Project context information
            
        Returns:
            Dictionary containing slide content and metadata
        """
        try:
            # Prepare the image for Gemini
            image_part = Part.from_data(image_bytes, mime_type=self._get_mime_type(filename))
            
            # Create context-aware prompt
            prompt = self._create_analysis_prompt(project_details)
            
            # Generate analysis using Gemini
            response = self.model.generate_content([prompt, image_part])
            
            # Parse the response
            analysis = self._parse_gemini_response(response.text, filename)
            
            # Add metadata
            analysis['filename'] = filename
            analysis['project_name'] = project_details['project_name']
            analysis['analysis_timestamp'] = project_details['created_at']
            
            logger.info(f"Successfully analyzed image: {filename}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing image {filename}: {str(e)}")
            # Return a fallback analysis
            return self._create_fallback_analysis(filename, project_details)
    
    def _create_analysis_prompt(self, project_details: Dict[str, Any]) -> str:
        """
        Create a context-aware prompt for image analysis
        
        Args:
            project_details: Project context information
            
        Returns:
            Formatted prompt string
        """
        project_name = project_details.get('project_name', 'construction project')
        highlights = project_details.get('highlights', '')
        
        prompt = f"""
        You are an expert construction project manager analyzing a weekly progress report image for the project: {project_name}.
        
        {f'Key highlights for this week: {highlights}' if highlights else ''}
        
        Please analyze this image and provide a structured response in the following JSON format:
        {{
            "slide_title": "A concise, professional title for this slide (max 60 characters)",
            "description": "A detailed description of the work shown, progress made, and current status. Use bullet points for clarity. Be specific about what is visible in the image.",
            "progress_status": "Current status (e.g., 'In Progress', 'Completed', 'Ready for Inspection')",
            "work_type": "Type of work shown (e.g., 'Electrical', 'Plumbing', 'Structural', 'Finishing')",
            "notes": "Any observations, potential issues, or important details that should be highlighted to the client",
            "completion_percentage": "Estimated completion percentage for this specific work area (0-100)"
        }}
        
        Guidelines:
        - Be professional and client-friendly
        - Focus on progress and achievements
        - Identify any potential issues or delays
        - Use construction industry terminology appropriately
        - Be specific about what you can see in the image
        - If the image shows multiple work areas, describe each one
        
        Respond only with valid JSON. Do not include any additional text or explanations.
        """
        
        return prompt.strip()
    
    def _parse_gemini_response(self, response_text: str, filename: str) -> Dict[str, Any]:
        """
        Parse the Gemini response and extract structured data
        
        Args:
            response_text: Raw response from Gemini
            filename: Image filename for error context
            
        Returns:
            Parsed analysis dictionary
        """
        try:
            # Clean the response text
            cleaned_text = response_text.strip()
            
            # Remove markdown code blocks if present
            if cleaned_text.startswith('```json'):
                cleaned_text = cleaned_text[7:]
            if cleaned_text.endswith('```'):
                cleaned_text = cleaned_text[:-3]
            
            # Parse JSON
            analysis = json.loads(cleaned_text)
            
            # Validate required fields
            required_fields = ['slide_title', 'description', 'progress_status', 'work_type', 'notes', 'completion_percentage']
            for field in required_fields:
                if field not in analysis:
                    analysis[field] = self._get_default_value(field)
            
            # Ensure completion_percentage is numeric
            try:
                analysis['completion_percentage'] = int(analysis['completion_percentage'])
                if analysis['completion_percentage'] < 0:
                    analysis['completion_percentage'] = 0
                elif analysis['completion_percentage'] > 100:
                    analysis['completion_percentage'] = 100
            except (ValueError, TypeError):
                analysis['completion_percentage'] = 50
            
            return analysis
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse Gemini response for {filename}: {str(e)}")
            return self._create_fallback_analysis(filename, {})
        except Exception as e:
            logger.error(f"Unexpected error parsing response for {filename}: {str(e)}")
            return self._create_fallback_analysis(filename, {})
    
    def _create_fallback_analysis(self, filename: str, project_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a fallback analysis when Gemini fails
        
        Args:
            filename: Image filename
            project_details: Project context
            
        Returns:
            Basic fallback analysis
        """
        project_name = project_details.get('project_name', 'Construction Project')
        
        return {
            'slide_title': f'Progress Update - {filename}',
            'description': f'Image analysis for {project_name}. Please review this image manually for detailed progress information.',
            'progress_status': 'Under Review',
            'work_type': 'General Construction',
            'notes': 'AI analysis was unavailable for this image. Manual review recommended.',
            'completion_percentage': 50,
            'filename': filename,
            'project_name': project_name,
            'analysis_timestamp': project_details.get('created_at', ''),
            'is_fallback': True
        }
    
    def _get_default_value(self, field: str) -> Any:
        """Get default values for missing fields"""
        defaults = {
            'slide_title': 'Progress Update',
            'description': 'Work progress captured in this image.',
            'progress_status': 'In Progress',
            'work_type': 'General Construction',
            'notes': 'No additional notes available.',
            'completion_percentage': 50
        }
        return defaults.get(field, '')
    
    def _get_mime_type(self, filename: str) -> str:
        """Determine MIME type from filename"""
        filename_lower = filename.lower()
        if filename_lower.endswith('.jpg') or filename_lower.endswith('.jpeg'):
            return 'image/jpeg'
        elif filename_lower.endswith('.png'):
            return 'image/png'
        elif filename_lower.endswith('.gif'):
            return 'image/gif'
        elif filename_lower.endswith('.webp'):
            return 'image/webp'
        else:
            return 'image/jpeg'  # Default to JPEG
    
    def batch_analyze_images(self, images_data: List[Dict[str, Any]], project_details: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Analyze multiple images in batch
        
        Args:
            images_data: List of image data dictionaries
            project_details: Project context information
            
        Returns:
            List of analysis results
        """
        analyses = []
        
        for image_data in images_data:
            try:
                image_bytes = base64.b64decode(image_data['data'])
                analysis = self.analyze_image(image_bytes, image_data['filename'], project_details)
                analyses.append(analysis)
            except Exception as e:
                logger.error(f"Error in batch analysis for {image_data.get('filename', 'unknown')}: {str(e)}")
                # Continue with other images
                continue
        
        return analyses
