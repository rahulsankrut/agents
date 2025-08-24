"""
Project Manager for handling project metadata and storage

This module manages project information, image analyses, and presentation
metadata using Google Cloud Storage.
"""

import logging
import json
import uuid
from typing import Dict, Any, List
from datetime import datetime
from google.cloud import storage

logger = logging.getLogger(__name__)

class ProjectManager:
    """
    Manages project metadata and storage operations
    """
    
    def __init__(self, storage_client: storage.Client):
        """
        Initialize ProjectManager
        
        Args:
            storage_client: Google Cloud Storage client
        """
        self.storage_client = storage_client
        self.metadata_bucket_name = 'weekly-metadata-465923'
        self._ensure_bucket_exists()
    
    def _ensure_bucket_exists(self):
        """Ensure the metadata bucket exists, create if it doesn't"""
        try:
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            if not bucket.exists():
                bucket = self.storage_client.create_bucket(self.metadata_bucket_name)
                logger.info(f"Created metadata bucket: {self.metadata_bucket_name}")
            else:
                logger.info(f"Using existing metadata bucket: {self.metadata_bucket_name}")
        except Exception as e:
            logger.error(f"Error ensuring metadata bucket exists: {str(e)}")
            # Use a default bucket name if creation fails
            self.metadata_bucket_name = 'weekly-project-presentations'
    
    def save_project_metadata(self, project_details: Dict[str, Any], image_analyses: List[Dict[str, Any]], presentation_filename: str) -> str:
        """
        Save project metadata to Cloud Storage
        
        Args:
            project_details: Project information
            image_analyses: List of analyzed images
            presentation_filename: Name of the generated presentation file
            
        Returns:
            Project ID string
        """
        try:
            # Generate unique project ID
            project_id = str(uuid.uuid4())
            
            # Create metadata structure
            metadata = {
                'project_id': project_id,
                'project_details': project_details,
                'image_analyses': image_analyses,
                'presentation_filename': presentation_filename,
                'created_at': datetime.now().isoformat(),
                'total_images': len(image_analyses),
                'status': 'completed'
            }
            
            # Calculate summary statistics
            if image_analyses:
                total_progress = sum(analysis.get('completion_percentage', 0) for analysis in image_analyses)
                avg_progress = total_progress / len(image_analyses)
                work_types = list(set(analysis.get('work_type', 'General') for analysis in image_analyses))
                
                metadata['summary'] = {
                    'average_completion': round(avg_progress, 1),
                    'work_types': work_types,
                    'total_progress': total_progress
                }
            
            # Save metadata to Cloud Storage
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            metadata_blob = bucket.blob(f"projects/{project_id}/metadata.json")
            
            metadata_blob.upload_from_string(
                json.dumps(metadata, indent=2, default=str),
                content_type='application/json'
            )
            
            # Save individual image analyses for easier access
            for i, analysis in enumerate(image_analyses):
                image_blob = bucket.blob(f"projects/{project_id}/images/{analysis['filename']}_analysis.json")
                image_blob.upload_from_string(
                    json.dumps(analysis, indent=2, default=str),
                    content_type='application/json'
                )
            
            logger.info(f"Project metadata saved successfully: {project_id}")
            return project_id
            
        except Exception as e:
            logger.error(f"Error saving project metadata: {str(e)}")
            raise
    
    def get_project_metadata(self, project_id: str) -> Dict[str, Any]:
        """
        Retrieve project metadata by ID
        
        Args:
            project_id: Unique project identifier
            
        Returns:
            Project metadata dictionary
        """
        try:
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            metadata_blob = bucket.blob(f"projects/{project_id}/metadata.json")
            
            if not metadata_blob.exists():
                raise ValueError(f"Project not found: {project_id}")
            
            metadata_content = metadata_blob.download_as_text()
            return json.loads(metadata_content)
            
        except Exception as e:
            logger.error(f"Error retrieving project metadata for {project_id}: {str(e)}")
            raise
    
    def list_projects(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List recent projects
        
        Args:
            limit: Maximum number of projects to return
            
        Returns:
            List of project summaries
        """
        try:
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            blobs = bucket.list_blobs(prefix="projects/", delimiter="/")
            
            projects = []
            project_ids = set()
            
            for blob in blobs:
                if blob.name.endswith('/metadata.json'):
                    project_id = blob.name.split('/')[1]
                    if project_id not in project_ids:
                        project_ids.add(project_id)
                        
                        try:
                            metadata = self.get_project_metadata(project_id)
                            projects.append({
                                'project_id': project_id,
                                'project_name': metadata['project_details']['project_name'],
                                'client_name': metadata['project_details']['client_name'],
                                'date_range': metadata['project_details']['date_range'],
                                'created_at': metadata['created_at'],
                                'total_images': metadata['total_images'],
                                'status': metadata['status']
                            })
                        except Exception as e:
                            logger.warning(f"Error loading project {project_id}: {str(e)}")
                            continue
            
            # Sort by creation date (newest first) and limit results
            projects.sort(key=lambda x: x['created_at'], reverse=True)
            return projects[:limit]
            
        except Exception as e:
            logger.error(f"Error listing projects: {str(e)}")
            return []
    
    def update_project_status(self, project_id: str, status: str, additional_info: Dict[str, Any] = None):
        """
        Update project status
        
        Args:
            project_id: Unique project identifier
            status: New status
            additional_info: Additional information to update
        """
        try:
            metadata = self.get_project_metadata(project_id)
            metadata['status'] = status
            metadata['updated_at'] = datetime.now().isoformat()
            
            if additional_info:
                metadata.update(additional_info)
            
            # Save updated metadata
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            metadata_blob = bucket.blob(f"projects/{project_id}/metadata.json")
            
            metadata_blob.upload_from_string(
                json.dumps(metadata, indent=2, default=str),
                content_type='application/json'
            )
            
            logger.info(f"Project {project_id} status updated to: {status}")
            
        except Exception as e:
            logger.error(f"Error updating project status for {project_id}: {str(e)}")
            raise
    
    def delete_project(self, project_id: str):
        """
        Delete project and all associated data
        
        Args:
            project_id: Unique project identifier
        """
        try:
            bucket = self.storage_client.bucket(self.metadata_bucket_name)
            
            # List all blobs for this project
            blobs = bucket.list_blobs(prefix=f"projects/{project_id}/")
            
            # Delete all project files
            for blob in blobs:
                blob.delete()
            
            logger.info(f"Project {project_id} deleted successfully")
            
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {str(e)}")
            raise
    
    def get_project_statistics(self) -> Dict[str, Any]:
        """
        Get overall project statistics
        
        Returns:
            Dictionary with project statistics
        """
        try:
            projects = self.list_projects(limit=1000)  # Get all projects
            
            if not projects:
                return {
                    'total_projects': 0,
                    'total_images_processed': 0,
                    'average_images_per_project': 0,
                    'projects_this_month': 0,
                    'projects_this_week': 0
                }
            
            total_projects = len(projects)
            total_images = sum(p['total_images'] for p in projects)
            avg_images = total_images / total_projects if total_projects > 0 else 0
            
            # Calculate time-based statistics
            now = datetime.now()
            this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            this_week = now.replace(hour=0, minute=0, second=0, microsecond=0)
            
            projects_this_month = sum(1 for p in projects if datetime.fromisoformat(p['created_at']) >= this_month)
            projects_this_week = sum(1 for p in projects if datetime.fromisoformat(p['created_at']) >= this_week)
            
            return {
                'total_projects': total_projects,
                'total_images_processed': total_images,
                'average_images_per_project': round(avg_images, 1),
                'projects_this_month': projects_this_month,
                'projects_this_week': projects_this_week,
                'last_updated': now.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting project statistics: {str(e)}")
            return {}
