"""
Test data for Anderson Firestore Database
Contains sample customer and project data for testing purposes.
"""

from schema import ImageData


# Sample test data
SAMPLE_CUSTOMERS = [
    {
        "customer_name": "Walmart Inc.",
        "customer_logo_url": "gs://anderson-agent-storage/logos/walmart-logo.png"
    },
    {
        "customer_name": "Target Corporation", 
        "customer_logo_url": "gs://anderson-agent-storage/logos/target-logo.png"
    },
    {
        "customer_name": "Amazon",
        "customer_logo_url": "gs://anderson-agent-storage/logos/amazon-logo.png"
    },
    {
        "customer_name": "Home Depot",
        "customer_logo_url": "gs://anderson-agent-storage/logos/homedepot-logo.png"
    },
    {
        "customer_name": "Costco Wholesale",
        "customer_logo_url": "gs://anderson-agent-storage/logos/costco-logo.png"
    }
]

SAMPLE_PROJECTS = [
    {
        "customer_name": "Walmart Inc.",
        "customer_logo_url": "gs://anderson-agent-storage/logos/walmart-logo.png",
        "project_title": "Walmart Store Optimization Initiative",
        "project_overview": """This comprehensive project focuses on optimizing Walmart store operations 
        through advanced analytics and process improvements. The initiative includes:
        
        1. Store Layout Optimization: Redesigning store layouts to improve customer flow and increase sales
        2. Inventory Management: Implementing AI-powered inventory tracking and restocking systems
        3. Checkout Process Enhancement: Reducing wait times through better queue management and self-checkout integration
        4. Employee Training: Comprehensive training programs for staff on new systems and processes
        
        Expected outcomes include a 15% increase in customer satisfaction, 20% reduction in checkout wait times,
        and 10% improvement in inventory turnover rates.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/walmart-store-layout.png",
                description="Store layout optimization showing improved customer flow"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/walmart-inventory-system.jpg",
                description="New inventory management system dashboard"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/walmart-checkout-process.png",
                description="Streamlined checkout process with reduced wait times"
            )
        ]
    },
    {
        "customer_name": "Target Corporation",
        "customer_logo_url": "gs://anderson-agent-storage/logos/target-logo.png",
        "project_title": "Target Digital Transformation",
        "project_overview": """Comprehensive digital transformation initiative focusing on e-commerce platform 
        enhancement, mobile app optimization, and omnichannel customer experience. This project includes:
        
        1. Mobile App Redesign: Complete overhaul of the Target mobile application with improved UX/UI
        2. E-commerce Platform Enhancement: Upgrading the online shopping platform with better search and recommendations
        3. Omnichannel Integration: Seamless integration between online and in-store experiences
        4. Personalization Engine: AI-driven personalization for product recommendations and marketing
        
        The project aims to increase online sales by 25% and improve customer engagement metrics by 30%.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/target-mobile-app.png",
                description="Redesigned mobile app interface with improved navigation"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/target-ecommerce-platform.jpg",
                description="Enhanced e-commerce platform dashboard with analytics"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/target-personalization-engine.png",
                description="AI-powered personalization engine interface"
            )
        ]
    },
    {
        "customer_name": "Amazon",
        "customer_logo_url": "gs://anderson-agent-storage/logos/amazon-logo.png",
        "project_title": "Amazon Warehouse Automation",
        "project_overview": """Implementation of advanced robotics and AI systems for warehouse operations, 
        including automated picking, sorting, and inventory management. This project encompasses:
        
        1. Robotic Picking Systems: Advanced robotics for automated product picking and sorting
        2. Warehouse Layout Optimization: AI-driven warehouse design for maximum efficiency
        3. Inventory Management AI: Machine learning systems for predictive inventory management
        4. Quality Control Automation: Automated quality control processes using computer vision
        
        Expected results include 40% reduction in processing time, 25% decrease in errors, 
        and 30% improvement in warehouse capacity utilization.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/amazon-robotics-system.png",
                description="Robotic picking system in action at Amazon fulfillment center"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/amazon-warehouse-layout.jpg",
                description="Optimized warehouse layout design with automated systems"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/amazon-inventory-ai.png",
                description="AI-powered inventory management system dashboard"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/amazon-quality-control.png",
                description="Automated quality control system using computer vision"
            )
        ]
    },
    {
        "customer_name": "Home Depot",
        "customer_logo_url": "gs://anderson-agent-storage/logos/homedepot-logo.png",
        "project_title": "Home Depot Customer Experience Enhancement",
        "project_overview": """Multi-faceted project to improve customer experience through better store navigation, 
        enhanced product discovery, and personalized recommendations. Key components include:
        
        1. Interactive Store Navigation: Digital kiosks and mobile app integration for store navigation
        2. Product Discovery Enhancement: Improved search and filtering capabilities
        3. Personalized Recommendations: AI-driven product recommendations based on customer behavior
        4. Augmented Reality Tools: AR applications for product visualization and project planning
        
        The project targets a 20% increase in customer satisfaction scores and 15% improvement in average transaction value.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/homedepot-store-navigation.png",
                description="Interactive store navigation system with digital kiosks"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/homedepot-product-recommendations.jpg",
                description="AI-powered product recommendation engine interface"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/homedepot-ar-tools.png",
                description="Augmented reality tools for product visualization"
            )
        ]
    },
    {
        "customer_name": "Costco Wholesale",
        "customer_logo_url": "gs://anderson-agent-storage/logos/costco-logo.png",
        "project_title": "Costco Membership Analytics Platform",
        "project_overview": """Development of an advanced analytics platform to optimize membership programs, 
        customer retention, and purchasing behavior analysis. This project includes:
        
        1. Membership Analytics Dashboard: Comprehensive analytics for membership trends and patterns
        2. Customer Retention AI: Machine learning models for predicting and preventing customer churn
        3. Purchase Behavior Analysis: Deep insights into customer purchasing patterns and preferences
        4. Personalized Marketing Engine: Targeted marketing campaigns based on customer data
        
        Goals include increasing membership retention by 12% and improving customer lifetime value by 18%.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/costco-membership-dashboard.png",
                description="Comprehensive membership analytics dashboard"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/costco-retention-ai.jpg",
                description="AI-powered customer retention prediction system"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/costco-purchase-analytics.png",
                description="Advanced purchase behavior analysis interface"
            )
        ]
    }
]

# Additional test scenarios
TEST_SCENARIOS = {
    "empty_project": {
        "customer_name": "Test Customer",
        "customer_logo_url": "gs://anderson-agent-storage/logos/test-logo.png",
        "project_title": "Empty Project Test",
        "project_overview": "This is a test project with no images to test edge cases.",
        "images": []
    },
    "single_image_project": {
        "customer_name": "Single Image Corp",
        "customer_logo_url": "gs://anderson-agent-storage/logos/single-image-logo.png",
        "project_title": "Single Image Project",
        "project_overview": "A project with only one image for testing purposes.",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/single-image.png",
                description="The only image in this project"
            )
        ]
    },
    "long_description_project": {
        "customer_name": "Long Description Inc",
        "customer_logo_url": "gs://anderson-agent-storage/logos/long-desc-logo.png",
        "project_title": "Project with Very Long Description",
        "project_overview": """This is a test project designed to validate the handling of very long project descriptions. 
        The description contains multiple paragraphs and extensive details to ensure that the system can properly 
        store and retrieve lengthy text content without any issues. This is particularly important for projects 
        that require comprehensive documentation and detailed explanations of their scope, objectives, and expected outcomes.
        
        The project encompasses multiple phases including initial planning, detailed analysis, implementation, testing, 
        and final deployment. Each phase has specific deliverables and milestones that need to be tracked and managed 
        effectively. The success of this project depends on careful coordination between various teams and stakeholders.
        
        Key performance indicators include customer satisfaction scores, system performance metrics, and business 
        impact measurements. Regular reporting and monitoring will ensure that the project stays on track and meets 
        all established objectives within the specified timeline and budget constraints.""",
        "images": [
            ImageData(
                image_url="gs://anderson-agent-storage/projects/long-desc-image1.png",
                description="First image for the long description project"
            ),
            ImageData(
                image_url="gs://anderson-agent-storage/projects/long-desc-image2.jpg",
                description="Second image showing detailed project components"
            )
        ]
    }
}
