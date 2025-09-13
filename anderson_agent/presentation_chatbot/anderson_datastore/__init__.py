"""
Anderson Firestore Database Package

A comprehensive Firestore database solution for storing customer and project information
with support for images and detailed descriptions.
"""

from .schema import Project, Customer, ImageData, COLLECTIONS
from .firestore_operations import FirestoreManager

__version__ = "1.0.0"
__author__ = "Anderson Agent Team"

__all__ = [
    "Project",
    "Customer", 
    "ImageData",
    "FirestoreManager",
    "COLLECTIONS"
]
