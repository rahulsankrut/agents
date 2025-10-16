import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import WelcomePage from './components/WelcomePage';
import ProjectForm from './components/ProjectForm';
import ImageUpload from './components/ImageUpload';
import ProcessingPage from './components/ProcessingPage';
import DownloadPage from './components/DownloadPage';
import './App.css';

function App() {
  const [projectData, setProjectData] = useState(null);
  const [currentStep, setCurrentStep] = useState('welcome');

  const handleProjectSubmit = (data) => {
    setProjectData(data);
    setCurrentStep('upload');
  };

  const handleImagesUploaded = (images) => {
    setProjectData(prev => ({ ...prev, images }));
    setCurrentStep('processing');
  };

  const handleProcessingComplete = (result) => {
    setProjectData(prev => ({ ...prev, result }));
    setCurrentStep('download');
  };

  const resetToWelcome = () => {
    setProjectData(null);
    setCurrentStep('welcome');
  };

  return (
    <Router>
      <div className="App min-h-screen bg-gray-50">
        <Header />
        
        <main className="container mx-auto px-4 py-8 max-w-4xl">
          <Routes>
            <Route path="/" element={
              currentStep === 'welcome' ? (
                <WelcomePage onStart={handleProjectSubmit} />
              ) : currentStep === 'upload' ? (
                <ImageUpload 
                  projectData={projectData}
                  onImagesUploaded={handleImagesUploaded}
                  onBack={() => setCurrentStep('welcome')}
                />
              ) : currentStep === 'processing' ? (
                <ProcessingPage 
                  projectData={projectData}
                  onComplete={handleProcessingComplete}
                />
              ) : currentStep === 'download' ? (
                <DownloadPage 
                  projectData={projectData}
                  onNewProject={resetToWelcome}
                />
              ) : (
                <WelcomePage onStart={handleProjectSubmit} />
              )
            } />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
