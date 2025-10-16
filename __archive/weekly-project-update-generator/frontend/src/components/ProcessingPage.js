import React, { useState, useEffect } from 'react';
import { Brain, Image as ImageIcon, FileText, Download, CheckCircle } from 'lucide-react';

const ProcessingPage = ({ projectData, onComplete }) => {
  const [currentStep, setCurrentStep] = useState('analyzing');
  const [progress, setProgress] = useState(0);
  const [currentImage, setCurrentImage] = useState(0);
  const [error, setError] = useState(null);

  const steps = [
    { id: 'analyzing', label: 'Analyzing Images', icon: Brain, description: 'AI is analyzing your project photos' },
    { id: 'generating', label: 'Generating Content', icon: FileText, description: 'Creating slide content and descriptions' },
    { id: 'creating', label: 'Building Presentation', icon: FileText, description: 'Assembling PowerPoint slides' },
    { id: 'finalizing', label: 'Finalizing', icon: Download, description: 'Preparing your presentation for download' }
  ];

  useEffect(() => {
    // Simulate processing steps
    const processImages = async () => {
      try {
        // Step 1: Analyzing Images
        setCurrentStep('analyzing');
        await simulateStep(2000, 25);
        
        // Step 2: Generating Content
        setCurrentStep('generating');
        await simulateStep(3000, 50);
        
        // Step 3: Creating Presentation
        setCurrentStep('creating');
        await simulateStep(2500, 75);
        
        // Step 4: Finalizing
        setCurrentStep('finalizing');
        await simulateStep(1500, 100);
        
        // Call the Cloud Function
        await callCloudFunction();
        
      } catch (error) {
        setError(error.message);
      }
    };

    processImages();
  }, []);

  const simulateStep = (duration, targetProgress) => {
    return new Promise((resolve) => {
      const startProgress = progress;
      const increment = (targetProgress - startProgress) / (duration / 50);
      
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= targetProgress) {
            clearInterval(interval);
            resolve();
            return targetProgress;
          }
          return prev + increment;
        });
      }, 50);
    });
  };

  const callCloudFunction = async () => {
    try {
      // Prepare the request payload
      const payload = {
        project_name: projectData.project_name,
        client_name: projectData.client_name,
        date_range: projectData.date_range,
        highlights: projectData.highlights || '',
        images: projectData.images
      };

      // In production, this would call your deployed Cloud Function
      // const response = await fetch('YOUR_CLOUD_FUNCTION_URL', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify(payload)
      // });

      // For demo purposes, simulate a successful response
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const mockResult = {
        success: true,
        project_id: 'demo-' + Date.now(),
        presentation_filename: `${projectData.project_name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pptx`,
        download_url: '#',
        message: 'Presentation generated successfully!'
      };

      onComplete(mockResult);
      
    } catch (error) {
      setError('Failed to generate presentation. Please try again.');
    }
  };

  const getCurrentStepIndex = () => {
    return steps.findIndex(step => step.id === currentStep);
  };

  const getStepIcon = (step, index) => {
    const Icon = step.icon;
    const isCompleted = index < getCurrentStepIndex();
    const isCurrent = step.id === currentStep;
    
    if (isCompleted) {
      return <CheckCircle className="w-6 h-6 text-success-500" />;
    } else if (isCurrent) {
      return <Icon className="w-6 h-6 text-primary-600" />;
    } else {
      return <Icon className="w-6 h-6 text-gray-400" />;
    }
  };

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-error-100 rounded-full mb-4">
          <Brain className="w-8 h-8 text-error-600" />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Something went wrong
        </h2>
        <p className="text-gray-600 mb-6">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div className="text-center mb-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          Generating Your Presentation
        </h1>
        <p className="text-xl text-gray-600">
          Our AI is analyzing your images and creating a professional PowerPoint presentation
        </p>
      </div>

      {/* Progress Steps */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <div className="space-y-6">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center space-x-4">
              <div className="flex-shrink-0">
                {getStepIcon(step, index)}
              </div>
              
              <div className="flex-1">
                <h3 className={`font-medium ${
                  index <= getCurrentStepIndex() ? 'text-gray-900' : 'text-gray-500'
                }`}>
                  {step.label}
                </h3>
                <p className={`text-sm ${
                  index <= getCurrentStepIndex() ? 'text-gray-600' : 'text-gray-400'
                }`}>
                  {step.description}
                </p>
              </div>
              
              {index === getCurrentStepIndex() && (
                <div className="flex-shrink-0">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Progress Bar */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8 mb-8">
        <div className="mb-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Overall Progress</span>
            <span className="text-sm font-medium text-primary-600">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-primary-600 h-3 rounded-full transition-all duration-300 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
        
        <div className="text-center text-sm text-gray-600">
          {currentStep === 'analyzing' && `Analyzing image ${currentImage + 1} of ${projectData.images.length}`}
          {currentStep === 'generating' && 'Generating slide content and descriptions'}
          {currentStep === 'creating' && 'Building PowerPoint presentation'}
          {currentStep === 'finalizing' && 'Preparing download...'}
        </div>
      </div>

      {/* Project Info */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          Processing Details
        </h3>
        
        <div className="grid md:grid-cols-2 gap-4 text-sm">
          <div>
            <span className="font-medium text-gray-700">Project:</span>
            <span className="ml-2 text-gray-900">{projectData.project_name}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Images:</span>
            <span className="ml-2 text-gray-900">{projectData.images.length} photos</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Client:</span>
            <span className="ml-2 text-gray-900">{projectData.client_name}</span>
          </div>
          <div>
            <span className="font-medium text-gray-700">Date Range:</span>
            <span className="ml-2 text-gray-900">{projectData.date_range}</span>
          </div>
        </div>
      </div>

      {/* Processing Tips */}
      <div className="mt-8 p-4 bg-primary-50 rounded-lg">
        <h3 className="text-sm font-medium text-primary-800 mb-2">
          ⏱️ Processing Time:
        </h3>
        <ul className="text-sm text-primary-700 space-y-1">
          <li>• Image analysis typically takes 10-30 seconds per image</li>
          <li>• Content generation and presentation assembly takes 1-2 minutes</li>
          <li>• Total time depends on the number of images uploaded</li>
          <li>• You'll receive a download link when processing is complete</li>
        </ul>
      </div>
    </div>
  );
};

export default ProcessingPage;
