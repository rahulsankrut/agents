import React, { useState } from 'react';
import { ArrowLeft, Building2, Calendar, User, FileText } from 'lucide-react';

const ProjectForm = ({ onSubmit, onBack }) => {
  const [formData, setFormData] = useState({
    project_name: '',
    client_name: '',
    date_range: '',
    highlights: ''
  });

  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.project_name.trim()) {
      newErrors.project_name = 'Project name is required';
    }
    
    if (!formData.client_name.trim()) {
      newErrors.client_name = 'Client name is required';
    }
    
    if (!formData.date_range.trim()) {
      newErrors.date_range = 'Date range is required';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit(formData);
    }
  };

  const inputFields = [
    {
      name: 'project_name',
      label: 'Project Name',
      placeholder: 'e.g., Oakwood Mall Renovation',
      icon: <Building2 className="w-5 h-5" />,
      required: true
    },
    {
      name: 'client_name',
      label: 'Client Name',
      placeholder: 'e.g., Prime Properties Inc.',
      icon: <User className="w-5 h-5" />,
      required: true
    },
    {
      name: 'date_range',
      label: 'Week/Date Range',
      placeholder: 'e.g., Week of August 18, 2025',
      icon: <Calendar className="w-5 h-5" />,
      required: true
    },
    {
      name: 'highlights',
      label: 'Key Highlights (Optional)',
      placeholder: 'e.g., Completed electrical wiring, installed drywall',
      icon: <FileText className="w-5 h-5" />,
      required: false,
      multiline: true
    }
  ];

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
          Project Details
        </h1>
      </div>

      {/* Form */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Tell us about your project
          </h2>
          <p className="text-gray-600">
            Provide basic information about the project and this week's work. 
            This helps our AI generate more relevant and accurate content.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {inputFields.map((field) => (
            <div key={field.name}>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {field.label}
                {field.required && <span className="text-error-600 ml-1">*</span>}
              </label>
              
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
                  {field.icon}
                </div>
                
                {field.multiline ? (
                  <textarea
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleInputChange}
                    placeholder={field.placeholder}
                    rows={3}
                    className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                      errors[field.name] 
                        ? 'border-error-300 focus:border-error-500 focus:ring-error-500' 
                        : 'border-gray-300'
                    }`}
                  />
                ) : (
                  <input
                    type="text"
                    name={field.name}
                    value={formData[field.name]}
                    onChange={handleInputChange}
                    placeholder={field.placeholder}
                    className={`block w-full pl-10 pr-3 py-3 border rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors ${
                      errors[field.name] 
                        ? 'border-error-300 focus:border-error-500 focus:ring-error-500' 
                        : 'border-gray-300'
                    }`}
                  />
                )}
              </div>
              
              {errors[field.name] && (
                <p className="mt-1 text-sm text-error-600">
                  {errors[field.name]}
                </p>
              )}
            </div>
          ))}

          {/* Submit Button */}
          <div className="pt-4">
            <button
              type="submit"
              className="w-full bg-primary-600 text-white font-semibold py-3 px-6 rounded-lg hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 transition-colors shadow-sm hover:shadow-md"
            >
              Continue to Image Upload
            </button>
          </div>
        </form>

        {/* Help Text */}
        <div className="mt-6 p-4 bg-primary-50 rounded-lg">
          <h3 className="text-sm font-medium text-primary-800 mb-2">
            💡 Tips for better results:
          </h3>
          <ul className="text-sm text-primary-700 space-y-1">
            <li>• Use descriptive project names that clearly identify the work</li>
            <li>• Include specific highlights to help AI understand the week's focus</li>
            <li>• Be consistent with date ranges (e.g., "Week of [Date]")</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ProjectForm;
