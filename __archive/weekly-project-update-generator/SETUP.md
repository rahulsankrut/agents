# Weekly Project Update PowerPoint Generator - Setup Guide

This guide will walk you through setting up and deploying the complete application.

## 🏗️ Architecture Overview

The application consists of:
- **Frontend**: React.js web application with modern UI
- **Backend**: Google Cloud Functions (Python)
- **AI Engine**: Google Vertex AI with Gemini 2.5 Pro
- **Storage**: Google Cloud Storage for images and presentations
- **Hosting**: Firebase Hosting for the frontend

## 📋 Prerequisites

Before you begin, ensure you have:

1. **Google Cloud Account** with billing enabled
2. **Google Cloud CLI (gcloud)** installed and configured
3. **Node.js** (v16 or later) and npm
4. **Python** (3.8 or later) with pip
5. **Firebase CLI** installed globally

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd weekly-project-update-generator

# Install Python dependencies
cd functions
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### 2. Google Cloud Setup

```bash
# Login to Google Cloud
gcloud auth login

# Set your project
gcloud config set project YOUR_PROJECT_ID

# Run the deployment script
cd deployment
python deploy.py
cd ..
```

### 3. Frontend Deployment

```bash
# Build the React app
cd frontend
npm run build

# Deploy to Firebase
firebase deploy
```

## 🔧 Detailed Setup

### Step 1: Google Cloud Project Setup

1. **Create a new project** (or use existing):
   ```bash
   gcloud projects create weekly-update-generator --name="Weekly Update Generator"
   gcloud config set project weekly-update-generator
   ```

2. **Enable required APIs**:
   ```bash
   gcloud services enable cloudfunctions.googleapis.com
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable storage.googleapis.com
   gcloud services enable aiplatform.googleapis.com
   gcloud services enable logging.googleapis.com
   ```

3. **Create service account**:
   ```bash
   gcloud iam service-accounts create weekly-update-generator \
     --display-name="Weekly Update Generator"
   
   gcloud projects add-iam-policy-binding weekly-update-generator \
     --member="serviceAccount:weekly-update-generator@weekly-update-generator.iam.gserviceaccount.com" \
     --role="roles/storage.admin"
   
   gcloud projects add-iam-policy-binding weekly-update-generator \
     --member="serviceAccount:weekly-update-generator@weekly-update-generator.iam.gserviceaccount.com" \
     --role="roles/aiplatform.user"
   ```

### Step 2: Cloud Storage Setup

1. **Create storage buckets**:
   ```bash
   gsutil mb gs://weekly-project-presentations-weekly-update-generator
   gsutil mb gs://weekly-project-metadata-weekly-update-generator
   ```

2. **Set bucket permissions**:
   ```bash
   gsutil iam ch allUsers:objectViewer gs://weekly-project-presentations-weekly-update-generator
   ```

### Step 3: Deploy Cloud Functions

1. **Deploy the main function**:
   ```bash
   cd functions
   gcloud functions deploy generate_presentation \
     --runtime python311 \
     --trigger-http \
     --allow-unauthenticated \
     --source . \
     --entry-point generate_presentation \
     --set-env-vars GOOGLE_CLOUD_PROJECT=weekly-update-generator
   ```

2. **Get the function URL**:
   ```bash
   gcloud functions describe generate_presentation --format='value(httpsTrigger.url)'
   ```

### Step 4: Frontend Setup

1. **Install dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Update API configuration**:
   Edit `src/components/ProcessingPage.js` and replace the mock API call with your actual Cloud Function URL.

3. **Build the application**:
   ```bash
   npm run build
   ```

### Step 5: Firebase Hosting

1. **Initialize Firebase**:
   ```bash
   firebase login
   firebase init hosting
   ```

2. **Deploy to Firebase**:
   ```bash
   firebase deploy
   ```

## 🔐 Environment Variables

Set these environment variables in your Cloud Function:

```bash
GOOGLE_CLOUD_PROJECT=your-project-id
PRESENTATIONS_BUCKET=weekly-project-presentations-your-project-id
```

## 🧪 Testing

### Local Testing

1. **Test Cloud Function locally**:
   ```bash
   cd functions
   functions-framework --target generate_presentation --debug
   ```

2. **Test frontend locally**:
   ```bash
   cd frontend
   npm start
   ```

### Production Testing

1. Upload test images through the web interface
2. Verify the AI analysis works correctly
3. Check that PowerPoint files are generated
4. Verify download links work properly

## 📊 Monitoring and Logs

### View Cloud Function Logs

```bash
gcloud functions logs read generate_presentation
```

### Monitor Storage Usage

```bash
gsutil du -h gs://weekly-project-presentations-*
gsutil du -h gs://weekly-project-metadata-*
```

### Check API Usage

Visit the [Google Cloud Console](https://console.cloud.google.com) to monitor:
- Cloud Functions execution
- Vertex AI API usage
- Storage bucket usage
- Error logs

## 🚨 Troubleshooting

### Common Issues

1. **Authentication Errors**:
   - Ensure service account has proper permissions
   - Check that APIs are enabled
   - Verify project ID is correct

2. **Image Analysis Failures**:
   - Check Vertex AI API quotas
   - Verify image format and size
   - Check Cloud Function logs

3. **Storage Issues**:
   - Verify bucket permissions
   - Check bucket names match environment variables
   - Ensure service account has storage access

4. **Frontend Errors**:
   - Verify Cloud Function URL is correct
   - Check browser console for errors
   - Ensure CORS is properly configured

### Debug Commands

```bash
# Check function status
gcloud functions describe generate_presentation

# View recent logs
gcloud functions logs read generate_presentation --limit=50

# Test function directly
curl -X POST YOUR_FUNCTION_URL \
  -H "Content-Type: application/json" \
  -d '{"test": "data"}'
```

## 🔄 Updates and Maintenance

### Updating Cloud Functions

```bash
cd functions
gcloud functions deploy generate_presentation --source .
```

### Updating Frontend

```bash
cd frontend
npm run build
firebase deploy
```

### Scaling Considerations

- **Cloud Functions**: Automatically scale based on demand
- **Storage**: Monitor bucket usage and costs
- **AI API**: Set up quotas and billing alerts
- **Frontend**: Firebase Hosting handles scaling automatically

## 💰 Cost Optimization

1. **Set up billing alerts** in Google Cloud Console
2. **Monitor API usage** for Vertex AI
3. **Optimize image sizes** before upload
4. **Use appropriate storage classes** for different data types
5. **Set up automatic cleanup** for old presentations

## 🆘 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review Google Cloud Console logs
3. Check the GitHub issues page
4. Review Google Cloud documentation

## 📚 Additional Resources

- [Google Cloud Functions Documentation](https://cloud.google.com/functions/docs)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Firebase Hosting Documentation](https://firebase.google.com/docs/hosting)
- [React Documentation](https://reactjs.org/docs)

---

**Happy presenting! 🎉**
