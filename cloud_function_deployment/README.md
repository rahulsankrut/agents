# PowerPoint Generation Cloud Function API

A serverless Google Cloud Function that provides a REST API for generating PowerPoint presentations programmatically.

## 🚀 Features

- **Serverless Architecture**: Deploy on Google Cloud Functions for automatic scaling
- **REST API**: Simple HTTP endpoints for PowerPoint generation
- **Multiple Output Formats**: Download as file or receive base64 encoded data
- **Image Support**: Upload images via file paths or base64 encoding
- **Security**: API key authentication support
- **Error Handling**: Comprehensive validation and error responses
- **Template System**: Extensible template-based presentation generation

## 📋 Prerequisites

- Google Cloud Platform account
- Google Cloud CLI (`gcloud`) installed and configured
- Python 3.11+ (for local development)
- Active Google Cloud project with Cloud Functions API enabled

## 🛠️ Installation & Deployment

### 1. Setup Google Cloud

```bash
# Install Google Cloud CLI (if not already installed)
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable cloudfunctions.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 2. Deploy the Function

```bash
# Navigate to deployment directory
cd anderson_agent/deployment

# Deploy with default settings
python deploy.py

# Or deploy with custom settings
python deploy.py --project YOUR_PROJECT_ID --region us-central1 --function-name ppt-generator
```

### 3. Set Environment Variables (Optional)

```bash
# Set API key for authentication
export PPT_API_KEY="your-secret-api-key"

# Deploy with API key
python deploy.py
```

## 📚 API Documentation

### Base URL
```
https://REGION-PROJECT_ID.cloudfunctions.net/FUNCTION_NAME
```

### Authentication
Include the API key in the request header (if configured):
```
X-API-Key: your-secret-api-key
```

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "PowerPoint Generation API",
  "version": "1.0.0"
}
```

#### 2. Generate Presentation (File Download)
```http
POST /generate
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "My Presentation Title",
  "logo_path": "path/to/logo.png",
  "text_content": "• First bullet point\n• Second bullet point\n• Third bullet point",
  "image_data": [
    {
      "path": "path/to/image1.png",
      "title": "Image 1 Title"
    },
    {
      "path": "path/to/image2.png", 
      "title": "Image 2 Title"
    }
  ],
  "include_eqi": true
}
```

**Response:** PowerPoint file download

#### 3. Generate Presentation (Base64)
```http
POST /generate-base64
Content-Type: application/json
```

**Request Body:** Same as `/generate`

**Response:**
```json
{
  "success": true,
  "filename": "My_Presentation_Title.pptx",
  "data": "base64-encoded-file-data",
  "size": 1234567
}
```

#### 4. Get Templates
```http
GET /templates
```

**Response:**
```json
{
  "templates": [
    {
      "name": "simple_presentation",
      "description": "Basic presentation with header, title, text content, and images",
      "parameters": {
        "title": {
          "type": "string",
          "required": true,
          "description": "Presentation title"
        },
        // ... more parameters
      }
    }
  ]
}
```

### Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `title` | string | Yes | Presentation title |
| `logo_path` | string | No | Path to logo image file |
| `logo_base64` | string | No | Base64 encoded logo image |
| `text_content` | string | No | Text content for left panel (supports newlines) |
| `image_data` | array | No | Array of image objects |
| `include_eqi` | boolean | No | Include Execution Quality Index (default: false) |

### Image Data Format

```json
{
  "image_data": [
    {
      "path": "path/to/image.png",
      "title": "Image Title"
    },
    {
      "base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
      "title": "Base64 Image Title"
    }
  ]
}
```

## 💻 Usage Examples

### Python Example

```python
import requests
import base64

# Function URL (replace with your actual URL)
FUNCTION_URL = "https://us-central1-your-project.cloudfunctions.net/ppt-generator"

# API Key (if configured)
API_KEY = "your-secret-api-key"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

# Example 1: Simple presentation
data = {
    "title": "Q1 2024 Project Update",
    "text_content": "• Project Status: On Track\n• Key Milestones Completed\n• Upcoming Deliverables",
    "include_eqi": True
}

response = requests.post(f"{FUNCTION_URL}/generate", json=data, headers=headers)

if response.status_code == 200:
    with open("presentation.pptx", "wb") as f:
        f.write(response.content)
    print("✅ Presentation saved!")
else:
    print(f"❌ Error: {response.json()}")

# Example 2: With base64 images
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode('utf-8')

data = {
    "title": "Marketing Campaign Results",
    "logo_base64": encode_image_to_base64("logo.png"),
    "text_content": "• Campaign launched successfully\n• 25% increase in engagement\n• ROI exceeded expectations",
    "image_data": [
        {
            "base64": encode_image_to_base64("chart1.png"),
            "title": "Engagement Metrics"
        },
        {
            "base64": encode_image_to_base64("chart2.png"),
            "title": "ROI Analysis"
        }
    ],
    "include_eqi": False
}

response = requests.post(f"{FUNCTION_URL}/generate-base64", json=data, headers=headers)

if response.status_code == 200:
    result = response.json()
    # Decode and save the presentation
    with open(result["filename"], "wb") as f:
        f.write(base64.b64decode(result["data"]))
    print(f"✅ Presentation saved as {result['filename']}")
else:
    print(f"❌ Error: {response.json()}")
```

### cURL Example

```bash
# Health check
curl -X GET "https://us-central1-your-project.cloudfunctions.net/ppt-generator/health"

# Generate presentation
curl -X POST "https://us-central1-your-project.cloudfunctions.net/ppt-generator/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "title": "Project Status Update",
    "text_content": "• Phase 1 Complete\n• Phase 2 In Progress\n• Phase 3 Planned",
    "include_eqi": true
  }' \
  --output presentation.pptx
```

### JavaScript/Node.js Example

```javascript
const axios = require('axios');
const fs = require('fs');

const FUNCTION_URL = 'https://us-central1-your-project.cloudfunctions.net/ppt-generator';
const API_KEY = 'your-secret-api-key';

async function generatePresentation() {
  try {
    const response = await axios.post(`${FUNCTION_URL}/generate-base64`, {
      title: 'Monthly Report',
      text_content: '• Revenue: $1.2M\n• Growth: 15%\n• New Customers: 150',
      include_eqi: true
    }, {
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': API_KEY
      }
    });

    if (response.data.success) {
      // Save the base64 decoded file
      const buffer = Buffer.from(response.data.data, 'base64');
      fs.writeFileSync(response.data.filename, buffer);
      console.log(`✅ Presentation saved as ${response.data.filename}`);
    }
  } catch (error) {
    console.error('❌ Error:', error.response?.data || error.message);
  }
}

generatePresentation();
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PPT_API_KEY` | API key for authentication | None (no auth required) |

### Function Settings

| Setting | Default | Description |
|---------|---------|-------------|
| Runtime | python311 | Python runtime version |
| Memory | 1GB | Function memory allocation |
| Timeout | 540s | Function execution timeout |
| Max Instances | 10 | Maximum concurrent instances |

## 🚨 Error Handling

The API returns appropriate HTTP status codes and error messages:

- `200`: Success
- `400`: Bad Request (invalid parameters)
- `401`: Unauthorized (invalid API key)
- `404`: Not Found (invalid endpoint)
- `405`: Method Not Allowed
- `500`: Internal Server Error

**Error Response Format:**
```json
{
  "error": "Error description"
}
```

## 🔒 Security

- **API Key Authentication**: Optional API key validation
- **Input Validation**: Comprehensive request parameter validation
- **File Size Limits**: Built-in limits to prevent abuse
- **Temporary Files**: Automatic cleanup of temporary files
- **HTTPS Only**: All communications encrypted in transit

## 📊 Monitoring & Logging

- **Cloud Logging**: All function executions logged to Google Cloud Logging
- **Cloud Monitoring**: Built-in metrics and monitoring
- **Error Tracking**: Detailed error logging for debugging

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test endpoints
curl http://localhost:8080/health
```

## 📝 License

This project is part of the Anderson Agent toolkit and follows the same licensing terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the logs in Google Cloud Console
- Review the API documentation
- Test with the health endpoint first
- Verify your request format matches the examples
