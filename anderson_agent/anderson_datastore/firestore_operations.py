"""
Firestore Database Operations for Anderson Agent
Handles CRUD operations for customers and projects.
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import logging

from schema import Project, Customer, ImageData, COLLECTIONS, MAX_CUSTOMER_NAME_LENGTH, MAX_PROJECT_TITLE_LENGTH, MAX_PROJECT_OVERVIEW_LENGTH, MAX_IMAGE_DESCRIPTION_LENGTH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FirestoreManager:
    """Manages Firestore database operations for customers and projects."""
    
    def __init__(self, project_id: str = None, database_id: str = "anderson-db"):
        """
        Initialize Firestore client.
        
        Args:
            project_id: Google Cloud Project ID. If None, uses default project.
            database_id: Firestore database ID. Defaults to "anderson-db".
        """
        self.db = firestore.Client(project=project_id, database=database_id)
        self.customers_collection = self.db.collection(COLLECTIONS['CUSTOMERS'])
        self.projects_collection = self.db.collection(COLLECTIONS['PROJECTS'])
    
    def _validate_customer_data(self, customer_name: str, customer_logo_url: str) -> None:
        """Validate customer data before saving."""
        if not customer_name or len(customer_name.strip()) == 0:
            raise ValueError("Customer name cannot be empty")
        if len(customer_name) > MAX_CUSTOMER_NAME_LENGTH:
            raise ValueError(f"Customer name cannot exceed {MAX_CUSTOMER_NAME_LENGTH} characters")
        if not customer_logo_url or len(customer_logo_url.strip()) == 0:
            raise ValueError("Customer logo URL cannot be empty")
    
    def _validate_project_data(self, project_title: str, project_overview: str, images: List[ImageData]) -> None:
        """Validate project data before saving."""
        if not project_title or len(project_title.strip()) == 0:
            raise ValueError("Project title cannot be empty")
        if len(project_title) > MAX_PROJECT_TITLE_LENGTH:
            raise ValueError(f"Project title cannot exceed {MAX_PROJECT_TITLE_LENGTH} characters")
        
        if not project_overview or len(project_overview.strip()) == 0:
            raise ValueError("Project overview cannot be empty")
        if len(project_overview) > MAX_PROJECT_OVERVIEW_LENGTH:
            raise ValueError(f"Project overview cannot exceed {MAX_PROJECT_OVERVIEW_LENGTH} characters")
        
        for image in images:
            if not image.image_url or len(image.image_url.strip()) == 0:
                raise ValueError("Image URL cannot be empty")
            if not image.description or len(image.description.strip()) == 0:
                raise ValueError("Image description cannot be empty")
            if len(image.description) > MAX_IMAGE_DESCRIPTION_LENGTH:
                raise ValueError(f"Image description cannot exceed {MAX_IMAGE_DESCRIPTION_LENGTH} characters")
    
    def _project_to_dict(self, project: Project) -> Dict[str, Any]:
        """Convert Project object to dictionary for Firestore."""
        return {
            'project_id': project.project_id,
            'customer_name': project.customer_name,
            'customer_logo_url': project.customer_logo_url,
            'project_title': project.project_title,
            'project_overview': project.project_overview,
            'eqi': project.eqi,
            'images': [
                {
                    'image_url': img.image_url,
                    'description': img.description
                } for img in project.images
            ],
            'created_at': project.created_at,
            'updated_at': project.updated_at
        }
    
    def _dict_to_project(self, data: Dict[str, Any]) -> Project:
        """Convert Firestore document to Project object."""
        images = [ImageData(img['image_url'], img['description']) for img in data.get('images', [])]
        return Project(
            project_id=data['project_id'],
            customer_name=data['customer_name'],
            customer_logo_url=data['customer_logo_url'],
            project_title=data['project_title'],
            project_overview=data['project_overview'],
            eqi=data.get('eqi', 'No'),  # Default to "No" if not present
            images=images,
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at', datetime.now())
        )
    
    def _customer_to_dict(self, customer: Customer) -> Dict[str, Any]:
        """Convert Customer object to dictionary for Firestore."""
        return {
            'customer_id': customer.customer_id,
            'customer_name': customer.customer_name,
            'customer_logo_url': customer.customer_logo_url,
            'projects': customer.projects,
            'created_at': customer.created_at,
            'updated_at': customer.updated_at
        }
    
    def _dict_to_customer(self, data: Dict[str, Any]) -> Customer:
        """Convert Firestore document to Customer object."""
        return Customer(
            customer_id=data['customer_id'],
            customer_name=data['customer_name'],
            customer_logo_url=data['customer_logo_url'],
            projects=data.get('projects', []),
            created_at=data.get('created_at', datetime.now()),
            updated_at=data.get('updated_at', datetime.now())
        )
    
    # Customer Operations
    def create_customer(self, customer_name: str, customer_logo_url: str) -> str:
        """
        Create a new customer.
        
        Args:
            customer_name: Name of the customer
            customer_logo_url: URL to customer logo in Google Cloud Storage
            
        Returns:
            customer_id: Unique identifier for the created customer
        """
        self._validate_customer_data(customer_name, customer_logo_url)
        
        customer_id = str(uuid.uuid4())
        customer = Customer(
            customer_id=customer_id,
            customer_name=customer_name.strip(),
            customer_logo_url=customer_logo_url.strip()
        )
        
        self.customers_collection.document(customer_id).set(self._customer_to_dict(customer))
        logger.info(f"Created customer: {customer_name} with ID: {customer_id}")
        return customer_id
    
    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Get a customer by ID."""
        doc = self.customers_collection.document(customer_id).get()
        if doc.exists:
            return self._dict_to_customer(doc.to_dict())
        return None
    
    def get_customer_by_name(self, customer_name: str) -> Optional[Customer]:
        """Get a customer by name."""
        query = self.customers_collection.where(filter=FieldFilter("customer_name", "==", customer_name.strip()))
        docs = query.limit(1).stream()
        
        for doc in docs:
            return self._dict_to_customer(doc.to_dict())
        return None
    
    def list_customers(self) -> List[Customer]:
        """List all customers."""
        docs = self.customers_collection.stream()
        return [self._dict_to_customer(doc.to_dict()) for doc in docs]
    
    def update_customer(self, customer_id: str, customer_name: str = None, customer_logo_url: str = None) -> bool:
        """Update customer information."""
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        
        if customer_name is not None:
            self._validate_customer_data(customer_name, customer.customer_logo_url)
            customer.customer_name = customer_name.strip()
        
        if customer_logo_url is not None:
            self._validate_customer_data(customer.customer_name, customer_logo_url)
            customer.customer_logo_url = customer_logo_url.strip()
        
        customer.updated_at = datetime.now()
        self.customers_collection.document(customer_id).set(self._customer_to_dict(customer))
        logger.info(f"Updated customer: {customer_id}")
        return True
    
    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer and all associated projects."""
        customer = self.get_customer(customer_id)
        if not customer:
            return False
        
        # Delete all projects for this customer
        projects = self.get_projects_by_customer(customer_id)
        for project in projects:
            self.delete_project(project.project_id)
        
        # Delete the customer
        self.customers_collection.document(customer_id).delete()
        logger.info(f"Deleted customer: {customer_id}")
        return True
    
    # Project Operations
    def create_project(self, customer_name: str, customer_logo_url: str, project_title: str, 
                      project_overview: str, eqi: str, images: List[ImageData]) -> str:
        """
        Create a new project.
        
        Args:
            customer_name: Name of the customer
            customer_logo_url: URL to customer logo in Google Cloud Storage
            project_title: Title of the project
            project_overview: Overview of the project
            eqi: Environmental Quality Index ("Yes" or "No")
            images: List of images with descriptions
            
        Returns:
            project_id: Unique identifier for the created project
        """
        self._validate_customer_data(customer_name, customer_logo_url)
        self._validate_project_data(project_title, project_overview, images)
        
        project_id = str(uuid.uuid4())
        project = Project(
            project_id=project_id,
            customer_name=customer_name.strip(),
            customer_logo_url=customer_logo_url.strip(),
            project_title=project_title.strip(),
            project_overview=project_overview.strip(),
            eqi=eqi,
            images=images
        )
        
        # Check if customer exists, create if not
        customer = self.get_customer_by_name(customer_name)
        if not customer:
            customer_id = self.create_customer(customer_name, customer_logo_url)
        else:
            customer_id = customer.customer_id
        
        # Add project to customer's project list
        customer = self.get_customer(customer_id)
        if project_id not in customer.projects:
            customer.projects.append(project_id)
            customer.updated_at = datetime.now()
            self.customers_collection.document(customer_id).set(self._customer_to_dict(customer))
        
        # Save the project
        self.projects_collection.document(project_id).set(self._project_to_dict(project))
        logger.info(f"Created project: {project_title} with ID: {project_id}")
        return project_id
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        doc = self.projects_collection.document(project_id).get()
        if doc.exists:
            return self._dict_to_project(doc.to_dict())
        return None
    
    def get_projects_by_customer(self, customer_id: str) -> List[Project]:
        """Get all projects for a specific customer."""
        customer = self.get_customer(customer_id)
        if not customer:
            return []
        
        projects = []
        for project_id in customer.projects:
            project = self.get_project(project_id)
            if project:
                projects.append(project)
        return projects
    
    def get_projects_by_customer_name(self, customer_name: str) -> List[Project]:
        """Get all projects for a customer by name."""
        customer = self.get_customer_by_name(customer_name)
        if not customer:
            return []
        return self.get_projects_by_customer(customer.customer_id)
    
    def list_projects(self) -> List[Project]:
        """List all projects."""
        docs = self.projects_collection.stream()
        return [self._dict_to_project(doc.to_dict()) for doc in docs]
    
    def update_project(self, project_id: str, project_title: str = None, project_overview: str = None, 
                      eqi: str = None, images: List[ImageData] = None) -> bool:
        """Update project information."""
        project = self.get_project(project_id)
        if not project:
            return False
        
        if project_title is not None:
            self._validate_project_data(project_title, project.project_overview, project.images)
            project.project_title = project_title.strip()
        
        if project_overview is not None:
            self._validate_project_data(project.project_title, project_overview, project.images)
            project.project_overview = project_overview.strip()
        
        if eqi is not None:
            project.eqi = eqi
        
        if images is not None:
            self._validate_project_data(project.project_title, project.project_overview, images)
            project.images = images
        
        project.updated_at = datetime.now()
        self.projects_collection.document(project_id).set(self._project_to_dict(project))
        logger.info(f"Updated project: {project_id}")
        return True
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project."""
        project = self.get_project(project_id)
        if not project:
            return False
        
        # Remove project from customer's project list
        customer = self.get_customer_by_name(project.customer_name)
        if customer and project_id in customer.projects:
            customer.projects.remove(project_id)
            customer.updated_at = datetime.now()
            self.customers_collection.document(customer.customer_id).set(self._customer_to_dict(customer))
        
        # Delete the project
        self.projects_collection.document(project_id).delete()
        logger.info(f"Deleted project: {project_id}")
        return True
