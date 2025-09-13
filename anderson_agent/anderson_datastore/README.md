# Anderson Firestore Database (anderson-db)

A comprehensive Firestore database solution for storing customer and project information with support for images and detailed descriptions.

## Overview

This database system is designed to store and manage:
- **Customer Information**: Name and logo
- **Project Details**: Title, overview, and associated images
- **Image Management**: Multiple images per project with descriptions
- **Google Cloud Storage Integration**: Links to images stored in GCS

## Database Schema

### Collections

#### Customers Collection (`customers`)
- `customer_id` (string): Unique identifier
- `customer_name` (string): Customer name (max 100 characters)
- `customer_logo_url` (string): Link to logo in Google Cloud Storage
- `projects` (array): List of project IDs associated with this customer
- `created_at` (timestamp): Creation timestamp
- `updated_at` (timestamp): Last update timestamp

#### Projects Collection (`projects`)
- `project_id` (string): Unique identifier
- `customer_name` (string): Name of the customer
- `customer_logo_url` (string): Link to customer logo in GCS
- `project_title` (string): Project title (max 500 characters)
- `project_overview` (string): Detailed project overview (max 5000 characters)
- `images` (array): List of image objects with URL and description
- `created_at` (timestamp): Creation timestamp
- `updated_at` (timestamp): Last update timestamp

### Image Data Structure
```python
{
    "image_url": "gs://bucket/path/to/image.png",
    "description": "Description of the image (max 1000 characters)"
}
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud authentication:
```bash
# Set your project ID
export GOOGLE_CLOUD_PROJECT=your-project-id

# Authenticate with Google Cloud
gcloud auth application-default login
```

## Usage

### Basic Operations

```python
from firestore_operations import FirestoreManager
from schema import ImageData

# Initialize the database manager
db_manager = FirestoreManager(project_id="your-project-id", database_id="anderson-db")

# Create a customer
customer_id = db_manager.create_customer(
    customer_name="Walmart Inc.",
    customer_logo_url="gs://your-bucket/logos/walmart-logo.png"
)

# Create a project with images
images = [
    ImageData(
        image_url="gs://your-bucket/projects/image1.png",
        description="Project overview image"
    ),
    ImageData(
        image_url="gs://your-bucket/projects/image2.jpg",
        description="Detailed implementation diagram"
    )
]

project_id = db_manager.create_project(
    customer_name="Walmart Inc.",
    customer_logo_url="gs://your-bucket/logos/walmart-logo.png",
    project_title="Store Optimization Project",
    project_overview="Comprehensive store optimization initiative...",
    images=images
)

# Retrieve data
customer = db_manager.get_customer(customer_id)
project = db_manager.get_project(project_id)

# List all customers and projects
customers = db_manager.list_customers()
projects = db_manager.list_projects()

# Get projects by customer
walmart_projects = db_manager.get_projects_by_customer_name("Walmart Inc.")
```

### Advanced Operations

```python
# Update project information
db_manager.update_project(
    project_id=project_id,
    project_title="Updated Project Title",
    images=new_images_list
)

# Update customer information
db_manager.update_customer(
    customer_id=customer_id,
    customer_name="Updated Customer Name"
)

# Delete operations
db_manager.delete_project(project_id)
db_manager.delete_customer(customer_id)  # Also deletes all associated projects
```

## File Structure

```
anderson_datastore/
├── schema.py                 # Data models and schema definitions
├── firestore_operations.py  # CRUD operations and database management
├── example_usage.py         # Usage examples and demonstrations
├── test_data.py             # Sample data for testing
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Data Validation

The system includes comprehensive validation:

- **Customer Name**: Required, max 100 characters
- **Project Title**: Required, max 500 characters  
- **Project Overview**: Required, max 5000 characters
- **Image URLs**: Required, must be valid Google Cloud Storage URLs
- **Image Descriptions**: Required, max 1000 characters

## Error Handling

All operations include proper error handling and validation:

```python
try:
    project_id = db_manager.create_project(...)
except ValueError as e:
    print(f"Validation error: {e}")
except Exception as e:
    print(f"Database error: {e}")
```

## Testing

Run the example usage to test the system:

```python
python example_usage.py
```

Load sample data for testing:

```python
from test_data import SAMPLE_PROJECTS, SAMPLE_CUSTOMERS
# Use the sample data to populate your database
```

## Google Cloud Storage Integration

Images are stored in Google Cloud Storage and referenced by their `gs://` URLs. Make sure your GCS bucket is properly configured and accessible.

### Example GCS URLs:
- `gs://your-bucket/logos/walmart-logo.png`
- `gs://your-bucket/projects/project-image-1.jpg`
- `gs://your-bucket/projects/detailed-diagram.png`

## Security Considerations

1. **Authentication**: Ensure proper Google Cloud authentication
2. **Permissions**: Set appropriate Firestore security rules
3. **Data Validation**: All inputs are validated before storage
4. **Access Control**: Implement proper access controls for your use case

## Performance Considerations

- **Indexing**: Firestore automatically creates indexes for queryable fields
- **Batch Operations**: Consider using batch writes for multiple operations
- **Pagination**: Use pagination for large result sets
- **Caching**: Implement caching strategies for frequently accessed data

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure Google Cloud authentication is set up correctly
2. **Permission Denied**: Check Firestore security rules and IAM permissions
3. **Validation Errors**: Verify input data meets length and format requirements
4. **Network Issues**: Check internet connectivity and firewall settings

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

When adding new features:

1. Update the schema in `schema.py`
2. Add corresponding operations in `firestore_operations.py`
3. Update validation rules as needed
4. Add tests and examples
5. Update this README

## License

This project is part of the Anderson Agent system.
