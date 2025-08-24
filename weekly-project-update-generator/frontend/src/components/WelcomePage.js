import React, { useState } from 'react';
import { ArrowRight, FileText, Image, Zap, Download } from 'lucide-react';
import ProjectForm from './ProjectForm';

const WelcomePage = ({ onStart }) => {
  const [showForm, setShowForm] = useState(false);

  const features = [
    {
      icon: <Image className="w-6 h-6" />,
      title: "Smart Image Analysis",
      description: "AI-powered analysis of construction photos using Google's Gemini 2.5 Pro"
    },
    {
      icon: <FileText className="w-6 h-6" />,
      title: "Professional Content",
      description: "Automatically generate slide titles, descriptions, and progress updates"
    },
    {
      icon: <Zap className="w-6 h-6" />,
      title: "Instant Generation",
      description: "Create polished PowerPoint presentations in minutes, not hours"
    },
    {
      icon: <Download className="w-6 h-6" />,
      title: "Ready to Share",
      description: "Download presentation files ready to send to clients"
    }
  ];

  if (showForm) {
    return <ProjectForm onSubmit={onStart} onBack={() => setShowForm(false)} />;
  }

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-20 h-20 bg-primary-100 rounded-full mb-6">
          <FileText className="w-10 h-10 text-primary-600" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Transform Your Weekly Updates
        </h1>
        
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Upload project photos and let AI create professional PowerPoint presentations 
          automatically. Save hours of work every week.
        </p>
        
        <button
          onClick={() => setShowForm(true)}
          className="inline-flex items-center px-8 py-4 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors shadow-lg hover:shadow-xl"
        >
          Start New Report
          <ArrowRight className="ml-2 w-5 h-5" />
        </button>
      </div>

      {/* Features Grid */}
      <div className="grid md:grid-cols-2 gap-8 mb-12">
        {features.map((feature, index) => (
          <div
            key={index}
            className="bg-white p-6 rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow"
          >
            <div className="flex items-start space-x-4">
              <div className="flex-shrink-0 w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center text-primary-600">
                {feature.icon}
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* How It Works */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          How It Works
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-4">
              1
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Upload Photos</h3>
            <p className="text-gray-600 text-sm">
              Upload your weekly project photos through our simple interface
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-4">
              2
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">AI Analysis</h3>
            <p className="text-gray-600 text-sm">
              Our AI analyzes each image and generates professional descriptions
            </p>
          </div>
          
          <div className="text-center">
            <div className="w-12 h-12 bg-primary-600 text-white rounded-full flex items-center justify-center font-bold text-lg mx-auto mb-4">
              3
            </div>
            <h3 className="font-semibold text-gray-900 mb-2">Download Ready</h3>
            <p className="text-gray-600 text-sm">
              Get your polished PowerPoint presentation ready to share with clients
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="text-center mt-12">
        <p className="text-gray-600 mb-4">
          Ready to streamline your weekly reporting?
        </p>
        <button
          onClick={() => setShowForm(true)}
          className="inline-flex items-center px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors"
        >
          Create Your First Report
          <ArrowRight className="ml-2 w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default WelcomePage;
