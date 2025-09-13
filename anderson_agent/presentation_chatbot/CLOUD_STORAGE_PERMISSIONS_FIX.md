# Cloud Storage Permissions Fix Guide

## 🎯 **Problem**
The cloud function `ppt-generator` cannot access the `anderson_images` bucket to download logos and images, causing presentations to be generated without logos and EQI.

## 🔧 **Solution**

### **Option 1: Automated Fix (Recommended)**
Run the automated fix script:
```bash
cd /Users/rahulkasanagottu/Desktop/agents/anderson_agent/presentation_chatbot
python fix_cloud_storage_permissions.py
```

### **Option 2: Manual Fix**
Run these commands manually:

```bash
# Set variables
PROJECT_ID="agent-space-465923"
FUNCTION_NAME="ppt-generator"
SERVICE_ACCOUNT="${PROJECT_ID}-compute@developer.gserviceaccount.com"

# Grant read access to anderson_images bucket
gsutil iam ch serviceAccount:${SERVICE_ACCOUNT}:objectViewer gs://anderson_images

# Grant write access to presentations bucket
gsutil iam ch serviceAccount:${SERVICE_ACCOUNT}:objectAdmin gs://agent-space-465923-presentations

# Make presentations bucket publicly readable
gsutil iam ch allUsers:objectViewer gs://agent-space-465923-presentations
```

### **Option 3: Using Cloud Console**
1. Go to [Cloud Storage Console](https://console.cloud.google.com/storage)
2. Select the `anderson_images` bucket
3. Click "Permissions" tab
4. Add the service account `${PROJECT_ID}-compute@developer.gserviceaccount.com` with "Storage Object Viewer" role
5. Repeat for `agent-space-465923-presentations` bucket with "Storage Object Admin" role
6. Make the presentations bucket publicly readable

## 🧪 **Testing**

After applying the fix, test with:

```bash
# Test 1: Check bucket access
gsutil ls gs://anderson_images/customer_logos/

# Test 2: Generate a test presentation
cd /Users/rahulkasanagottu/Desktop/agents/anderson_agent/presentation_chatbot
python test_cloud_function_direct.py

# Test 3: Generate Walmart presentation
python debug_url_conversion.py
```

## 🔍 **Verification**

The fix is successful when:
- ✅ Logos appear in generated presentations
- ✅ EQI sub-header appears when `include_eqi: true`
- ✅ Generated presentations are publicly accessible
- ✅ File sizes are > 100KB (not 298 bytes)

## 📋 **What This Fix Does**

1. **Read Access**: Allows cloud function to download logos and images from `anderson_images` bucket
2. **Write Access**: Allows cloud function to upload generated presentations to `agent-space-465923-presentations` bucket
3. **Public Access**: Makes generated presentations publicly downloadable
4. **Error Handling**: Ensures proper error reporting when assets can't be downloaded

## 🚨 **Troubleshooting**

If issues persist:

1. **Check Cloud Function Logs**:
   ```bash
   gcloud functions logs read ppt-generator --region=us-central1 --limit=50
   ```

2. **Verify Permissions**:
   ```bash
   gsutil iam get gs://anderson_images
   gsutil iam get gs://agent-space-465923-presentations
   ```

3. **Test Service Account**:
   ```bash
   gcloud functions describe ppt-generator --region=us-central1 --format='value(serviceAccountEmail)'
   ```

4. **Wait for Propagation**: Permissions can take 2-3 minutes to propagate

## 🎉 **Expected Result**

After the fix:
- Users can say "Create the presentation for this week" and get a complete presentation
- Presentations will include customer logos and EQI sub-headers
- All presentations will be automatically saved to Cloud Storage
- Users will get direct download links that work immediately
