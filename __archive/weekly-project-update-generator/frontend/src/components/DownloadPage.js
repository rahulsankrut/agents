import React from 'react';
import { CheckCircle, Download, FileText, Plus, Share2 } from 'lucide-react';

const DownloadPage = ({ projectData, onNewProject }) => {
  const handleDownload = () => {
    // Check if we have a download URL from the Cloud Function
    if (projectData.result && projectData.result.download_url) {
      // If it's a real URL, download the file
      if (projectData.result.download_url.startsWith('http')) {
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = projectData.result.download_url;
        link.download = projectData.result.presentation_filename || 'presentation.pptx';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } else {
        // If it's a bucket path message, show it
        alert(projectData.result.download_url);
      }
    } else {
      // Fallback if no download URL
      alert('Download URL not available. Please try again.');
    }
  };

  const handleShare = () => {
    // In production, this could copy the download link to clipboard
    // or open sharing options
    if (navigator.share) {
      navigator.share({
        title: `Weekly Update: ${projectData.project_name}`,
        text: `Check out this week's progress update for ${projectData.project_name}`,
        url: window.location.href
      });
    } else {
      // Fallback: copy to clipboard
      navigator.clipboard.writeText(window.location.href);
      alert('Link copied to clipboard!');
    }
  };

  return (
    <div className="animate-fade-in">
      {/* Success Header */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-success-100 rounded-full mb-6">
          <CheckCircle className="w-10 h-10 text-success-600" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Presentation Ready!
        </h1>
        
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Your weekly project update PowerPoint has been generated successfully. 
          Download it below and share it with your client.
        </p>
      </div>

      {/* Download Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
            <FileText className="w-8 h-8 text-primary-600" />
          </div>
          
          <h2 className="text-2xl font-semibold text-gray-900 mb-2">
            {projectData.result.presentation_filename}
          </h2>
          
          <p className="text-gray-600">
            Professional PowerPoint presentation with {projectData.images.length} slides
          </p>
        </div>

        {/* Download Button */}
        <div className="text-center mb-6">
          <button
            onClick={handleDownload}
            className="inline-flex items-center px-8 py-4 bg-success-600 text-white font-semibold rounded-lg hover:bg-success-700 focus:outline-none focus:ring-2 focus:ring-success-500 focus:ring-offset-2 transition-colors shadow-lg hover:shadow-xl"
          >
            <Download className="w-5 h-5 mr-2" />
            Download PowerPoint
          </button>
        </div>

        {/* Project Summary */}
        <div className="bg-gray-50 rounded-lg p-6">
          <h3 className="font-semibold text-gray-900 mb-4">Project Summary</h3>
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
            <div>
              <span className="font-medium text-gray-700">Images Processed:</span>
              <span className="ml-2 text-gray-900">{projectData.images.length} photos</span>
            </div>
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
        <button
          onClick={handleShare}
          className="inline-flex items-center justify-center px-6 py-3 bg-gray-100 text-gray-700 font-medium rounded-lg hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
        >
          <Share2 className="w-4 h-4 mr-2" />
          Share Project
        </button>
        
        <button
          onClick={onNewProject}
          className="inline-flex items-center justify-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
        >
          <Plus className="w-4 h-4 mr-2" />
          Create New Report
        </button>
      </div>

      {/* What's Next */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">
          What's Next?
        </h2>
        
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Download className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Download & Review</h3>
            <p className="text-sm text-gray-600">
              Download your presentation and review the content before sharing
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Share2 className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Share with Client</h3>
            <p className="text-sm text-gray-600">
              Send the presentation to your client via email or file sharing
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mx-auto mb-3">
              <Plus className="w-6 h-6 text-primary-600" />
            </div>
            <h3 className="font-medium text-gray-900 mb-2">Create Next Report</h3>
            <p className="text-sm text-gray-600">
              Start working on next week's progress update
            </p>
          </div>
        </div>
      </div>

      {/* Tips */}
      <div className="bg-success-50 rounded-lg p-6">
        <h3 className="text-sm font-medium text-success-800 mb-2">
          🎉 Congratulations! Your presentation is ready.
        </h3>
        <ul className="text-sm text-success-700 space-y-1">
          <li>• The presentation includes a title slide, summary, and individual content slides</li>
          <li>• Each image has been analyzed and described by our AI</li>
          <li>• The file is ready to use and can be opened in PowerPoint, Google Slides, or similar</li>
          <li>• You can edit the content further if needed before sharing</li>
        </ul>
      </div>
    </div>
  );
};

export default DownloadPage;
