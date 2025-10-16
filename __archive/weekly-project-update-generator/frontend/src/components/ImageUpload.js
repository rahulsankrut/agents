import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { ArrowLeft, Upload, X, Image as ImageIcon, CheckCircle } from 'lucide-react';

const ImageUpload = ({ projectData, onImagesUploaded, onBack }) => {
  const [uploadedImages, setUploadedImages] = useState([]);
  const [isUploading, setIsUploading] = useState(false);

  const onDrop = useCallback((acceptedFiles) => {
    const newImages = acceptedFiles.map(file => ({
      file,
      id: Math.random().toString(36).substr(2, 9),
      preview: URL.createObjectURL(file),
      status: 'ready'
    }));
    
    setUploadedImages(prev => [...prev, ...newImages]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png', '.gif', '.webp']
    },
    multiple: true,
    maxSize: 10 * 1024 * 1024 // 10MB max
  });

  const removeImage = (imageId) => {
    setUploadedImages(prev => {
      const image = prev.find(img => img.id === imageId);
      if (image) {
        URL.revokeObjectURL(image.preview);
      }
      return prev.filter(img => img.id !== imageId);
    });
  };

  const handleContinue = async () => {
    if (uploadedImages.length === 0) {
      alert('Please upload at least one image to continue.');
      return;
    }

    setIsUploading(true);
    
    try {
      // Convert images to base64 for API
      const imagesData = await Promise.all(
        uploadedImages.map(async (image) => {
          const base64 = await fileToBase64(image.file);
          return {
            filename: image.file.name,
            data: base64.split(',')[1] // Remove data:image/jpeg;base64, prefix
          };
        })
      );

      // Call the callback with the processed images
      onImagesUploaded(imagesData);
      
    } catch (error) {
      console.error('Error processing images:', error);
      alert('Error processing images. Please try again.');
      setIsUploading(false);
    }
  };

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="animate-slide-up">
      {/* Header */}
      <div className="flex items-center mb-8">
        <button
          onClick={onBack}
          className="flex items-center text-gray-600 hover:text-gray-900 transition-colors mr-4"
        >
          <ArrowLeft className="w-5 h-5 mr-2" />
          Back
        </button>
        <h1 className="text-3xl font-bold text-gray-900">
          Upload Project Images
        </h1>
      </div>

      {/* Project Summary */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">
          Project Summary
        </h2>
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Project:</span>
            <span className="ml-2 text-gray-900">{projectData.project_name}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Client:</span>
            <span className="ml-2 text-gray-900">{projectData.client_name}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Date Range:</span>
            <span className="ml-2 text-gray-900">{projectData.date_range}</span>
          </div>
          {projectData.highlights && (
            <div>
              <span className="font-medium text-gray-700">Highlights:</span>
              <span className="ml-2 text-gray-900">{projectData.highlights}</span>
            </div>
          )}
        </div>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <div className="text-center mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Upload Your Weekly Progress Photos
          </h2>
          <p className="text-gray-600">
            Drag and drop your images here, or click to browse. 
            We'll analyze each photo and create slides automatically.
          </p>
        </div>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
            isDragActive
              ? 'border-primary-400 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400 hover:bg-primary-50'
          }`}
        >
          <input {...getInputProps()} />
          
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          
          {isDragActive ? (
            <p className="text-primary-600 font-medium">
              Drop the images here...
            </p>
          ) : (
            <div>
              <p className="text-gray-600 mb-2">
                <span className="font-medium text-primary-600">Click to upload</span> or drag and drop
              </p>
              <p className="text-sm text-gray-500">
                PNG, JPG, GIF, WEBP up to 10MB each
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Uploaded Images */}
      {uploadedImages.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Uploaded Images ({uploadedImages.length})
          </h3>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {uploadedImages.map((image) => (
              <div
                key={image.id}
                className="relative border border-gray-200 rounded-lg overflow-hidden group"
              >
                <img
                  src={image.preview}
                  alt={image.file.name}
                  className="w-full h-32 object-cover"
                />
                
                <div className="p-3">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {image.file.name}
                  </p>
                  <p className="text-xs text-gray-500">
                    {formatFileSize(image.file.size)}
                  </p>
                </div>
                
                <button
                  onClick={() => removeImage(image.id)}
                  className="absolute top-2 right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity hover:bg-red-600"
                >
                  <X className="w-4 h-4" />
                </button>
                
                <div className="absolute top-2 left-2">
                  <CheckCircle className="w-5 h-5 text-success-500" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Continue Button */}
      <div className="text-center">
        <button
          onClick={handleContinue}
          disabled={uploadedImages.length === 0 || isUploading}
          className={`inline-flex items-center px-8 py-4 font-semibold rounded-lg transition-colors shadow-sm ${
            uploadedImages.length === 0 || isUploading
              ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
              : 'bg-primary-600 text-white hover:bg-primary-700 hover:shadow-md'
          }`}
        >
          {isUploading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
              Processing...
            </>
          ) : (
            <>
              Generate Presentation
              <ImageIcon className="ml-2 w-5 h-5" />
            </>
          )}
        </button>
        
        {uploadedImages.length === 0 && (
          <p className="text-sm text-gray-500 mt-2">
            Upload at least one image to continue
          </p>
        )}
      </div>

      {/* Help Text */}
      <div className="mt-8 p-4 bg-primary-50 rounded-lg">
        <h3 className="text-sm font-medium text-primary-800 mb-2">
          📸 Image Upload Tips:
        </h3>
        <ul className="text-sm text-primary-700 space-y-1">
          <li>• Upload clear, well-lit photos that show progress clearly</li>
          <li>• Include photos from different work areas and stages</li>
          <li>• Avoid blurry or dark images for better AI analysis</li>
          <li>• You can upload multiple images at once</li>
        </ul>
      </div>
    </div>
  );
};

export default ImageUpload;
