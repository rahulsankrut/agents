"""
Firestore Database Schema for Anderson Agent
Defines the structure for storing customer and project information.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime


@dataclass
class ImageData:
    """Represents an image with its description and Google Cloud Storage link."""
    image_url: str  # Link to image in Google Cloud Storage
    description: str  # Description for the image


@dataclass
class Project:
    """Represents a project with all its associated data."""
    project_id: str  # Unique identifier for the project
    customer_name: str  # Small text - Customer Name
    customer_logo_url: str  # Link to customer logo in Google Cloud Storage
    project_title: str  # Long text - Project Title
    project_overview: str  # Long text - Project Overview
    eqi: str  # EQI (Yes/No) - Environmental Quality Index
    images: List[ImageData] = field(default_factory=list)  # List of images with descriptions
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Customer:
    """Represents a customer with basic information."""
    customer_id: str  # Unique identifier for the customer
    customer_name: str  # Small text - Customer Name
    customer_logo_url: str  # Link to customer logo in Google Cloud Storage
    projects: List[str] = field(default_factory=list)  # List of project IDs
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


# Firestore Collection Names
COLLECTIONS = {
    'CUSTOMERS': 'customers',
    'PROJECTS': 'projects'
}

# Field validation constants
MAX_CUSTOMER_NAME_LENGTH = 100
MAX_PROJECT_TITLE_LENGTH = 500
MAX_PROJECT_OVERVIEW_LENGTH = 5000
MAX_IMAGE_DESCRIPTION_LENGTH = 1000
