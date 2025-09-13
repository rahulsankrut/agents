"""
Simple Firestore connection test
"""

import os
from google.cloud import firestore

# Set project ID
PROJECT_ID = "agent-space-465923"

def test_firestore_connection():
    """Test basic Firestore connection."""
    
    print(f"Testing Firestore connection for project: {PROJECT_ID}")
    
    try:
        # Initialize Firestore client
        db = firestore.Client(project=PROJECT_ID, database="anderson-db")
        print("✅ Firestore client initialized for anderson-db")
        
        # Try to access a collection
        test_collection = db.collection('test')
        print("✅ Collection reference created")
        
        # Try to add a test document
        test_doc = test_collection.document('test-doc')
        test_doc.set({
            'message': 'Hello Firestore!',
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        print("✅ Test document created")
        
        # Read the document back
        doc = test_doc.get()
        if doc.exists:
            print(f"✅ Document read successfully: {doc.to_dict()}")
        
        # Clean up - delete the test document
        test_doc.delete()
        print("✅ Test document deleted")
        
        print("\n🎉 Firestore connection test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Firestore connection test failed: {e}")
        return False

if __name__ == "__main__":
    test_firestore_connection()
